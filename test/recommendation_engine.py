import pytest
import unittest
import pandas as pd
import sys
import os

import numpy as np
import pandas as pd
from collections import defaultdict
from numpy import dot
from numpy.linalg import norm

#dummy data frame for testing
dummy_df = {'event_time':  ['test','test','test','test','test'],
        'event_type': ['view','cart','purchase','view','cart'],
        'product_id': [1,2,3,2,1],
        'category_id': [101,102,103,102,101],
        'category_code': ['electronics','kids','kitchen','kids','electronics'],
        'brand': ['brand1','brand2','brand3','brand2','brand1'],
        'price': [100,101,102,101,100],
        'user_id': [1,2,3,1,1],
        'user_session': ['test','test','test','test','test']
        }

dummy_df = pd.DataFrame (dummy_df, columns = list(dummy_df.keys()))

#Pre-processing part
#Unique user and item
unique_user = set()
unique_item = set()
user_to_idx = {}

user_to_item = defaultdict(set)
item_to_user = defaultdict(set)

itemid_to_category_code = {}
itemid_to_brand = {}
item_history = defaultdict(dict)

#Loop through all the rows and create a unique user and item set
idx = 0
for i, row in dummy_df.iterrows():
    userid,itemid,categorycode,brand,event_type,price = row[7],row[2],row[4],row[5],row[1],row[6]
    unique_user.add(userid)
    unique_item.add(itemid)

    if userid not in user_to_idx:
        user_to_idx[userid] = idx
        idx+=1

    if itemid not in item_history:
        item_history[itemid]['view']=0
        item_history[itemid]['purchase']=0
        item_history[itemid]['cart']=0
        item_history[itemid]['price']=price

    user_to_item[userid].add(itemid)
    item_to_user[itemid].add(userid)
    itemid_to_category_code[itemid] = categorycode
    itemid_to_brand[itemid] = brand
    item_history[itemid][event_type]+=1

def OneHotEncode(item):
  '''
  Returns one-hot encoded vector for a given item ID indicating the purchase history of a user
  :param item: item ID of the item
  :type item: int
  :return: one hot encoded vector
  :rtype: list[int]
  '''
  vector = [0 for _ in range(len(unique_user))]

  for user in item_to_user[item]:
      vector[user_to_idx[user]]=1
  
  return vector


def CalcScore_cosine(item1, item2):
  '''
  Calculates the cosine similirity between two item IDs. Uses OneHotEncode helper function to retrieve one hot encodings for itemIDs.
  :param item1: item ID of item1
  :type item1: int
  :param item2: item ID of item2
  :type item2: int
  :return: Cosine Similarity Score
  :rtype: float
  '''
  a,b = OneHotEncode(item1), OneHotEncode(item2)

  cos_sim = dot(a, b)/(norm(a)*norm(b))
  return cos_sim

def jaccard(s1, s2):
  '''
  Calculates the cosine similirity between two input vectors.
  :param s1: first input vector
  :type s1: list[int]
  :param s2: second input vector
  :type s2: list[int]
  :return: Jaccard Similarity Score
  :rtype: float
  '''
  numer = len(s1.intersection(s2))
  denom = len(s1.union(s2))
  return numer/denom
  
def findNearestItem(itemid):
  '''
  Returns a list of itemIDs of the most similiar 50 items to the given input item.
  :param itemid: item ID of the item
  :type itemid: int
  :return: list of itemIDs of closest similar items
  :rtype: list[int]
  '''

  maxSimilarityScore = float('-inf')
  ClosestItem = None
  candidateItems = set()
  users = item_to_user[itemid]
  similarities = []

  #reduce the search space of the candidate items
  for u in users:
      candidateItems = candidateItems.union(user_to_item[u])

  for item in candidateItems:
      if item==itemid:
          continue
      
      # score = CalcScore_cosine(item,itemid)
      score = jaccard(users, item_to_user[item])
      if score==float('nan'):
          continue

      similarities.append((score, item))
  similarities.sort(reverse=True)
  
  return similarities[:50]

def find_Nearest_User(userid, item_to_user, user_to_item, top=10):
  '''
  Returns a list of UserIDs of the most similiar users to the given input user.
  :param userid: item ID of the item
  :type itemid: int
  :param item_to_user: dict which stores item to user list information
  :type item_to_user: dict
  :param user_to_item: dict which stores user to item list information
  :type user_to_item: dict
  :param top: parameter to control number of returned similar users
  :type top: int
  :return: list of userIDs of closest similar users
  :rtype: list[int]
  '''

  maxSimilarityScore = float('-inf')
  candidateUsers = set()
  items = user_to_item[userid]
  similarities = []

  #reduce the search space of the candidate items
  for i in items:
      candidateUsers = candidateUsers.union(item_to_user[i])

  for user in candidateUsers:
      if user==userid:
          continue
      
      # score = CalcScore_cosine(item,itemid)
      score = jaccard(items, user_to_item[user])
      if score==float('nan'):
          continue

      similarities.append((score, user))
  similarities.sort(reverse=True)
  
  return similarities[:top]



userhistory_price = dummy_df[['price', 'user_id']]
userhistory_event = dummy_df[['event_type', 'user_id']]

one_hot_event = pd.get_dummies(userhistory_event['event_type'])
userhistory_event = userhistory_event.drop('event_type',axis = 1)
userhistory_event = userhistory_event.join(one_hot_event)

price_df = userhistory_price.groupby(by='user_id').sum()
event_df = userhistory_event.groupby(by='user_id').sum()
userHistory = price_df.join(event_df)

def findNearestUsersfromItem(target_item, item_to_user, user_to_item):
  '''
  Returns a list of potential buyer list for the target item.

  :param target_item:  itemID of the item
  :type target_item: int
  :param item_to_user: dict which stores item to user list information
  :type item_to_user: dict
  :param user_to_item: dict which stores user to item list information
  :type user_to_item: dict
  :return: list of potential buyer userIDs
  :rtype: list[int]
  '''
  target_users = set()
  purchased_users = item_to_user[target_item]

  for user in purchased_users:
      set_users = set(list(zip(*find_Nearest_User(user, item_to_user, user_to_item)))[1])
      new_users = set_users.difference(purchased_users)
      target_users = target_users.union(new_users)

  target_users = list(target_users)
  views = []
  purchases = []
  carts = []
  amount = []
  for userid in target_users:
      views.append(userHistory.loc[userid, 'view'])
      purchases.append(userHistory.loc[userid, 'purchase'])
      carts.append(userHistory.loc[userid, 'cart'])
      amount.append(userHistory.loc[userid, 'price'])
  
  target_df = pd.DataFrame(data={ 'Target users': target_users,
                                  '#Views': views,
                                  '#Purchases': purchases,
                                  '#AddedToCart': carts,
                                  'Amount Spent': amount})


  return target_df