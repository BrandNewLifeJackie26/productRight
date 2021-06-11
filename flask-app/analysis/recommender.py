import numpy as np
import pandas as pd
from collections import defaultdict
from numpy import dot
from numpy.linalg import norm

class Recommender:
    '''
    Recommender Class representating the backbone of the recommendation system. Supports functions: find_nearest_item and uses helper functions for pre-processing data.
    '''
    def __init__(self) -> None:
        pass

    '''Recommendation Methods'''
    def find_nearest_item(self, itemid, item_to_user, user_to_item, top=10):
        '''
        Returns a list of ItemIDs of the most similiar items to the given input item.
        :param itemid: item ID of the item
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
        ClosestItem = None
        candidateItems = set()
        users = item_to_user[itemid]
        similarities = []

        # reduce the search space of the candidate items
        for u in users:
            candidateItems = candidateItems.union(user_to_item[u])

        for item in candidateItems:
            if item==itemid:
                continue
            
            # score = CalcScore_cosine(item,itemid)
            score = self.jaccard(users, item_to_user[item])
            if score==float('nan'):
                continue

            similarities.append((score, item))
        similarities.sort(reverse=True)
        
        return similarities[:top]


    def find_nearest_user(self, userid, item_to_user, user_to_item, top=10):
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
            score = self.jaccard(items, user_to_item[user])
            if score==float('nan'):
                continue

            similarities.append((score, user))
        similarities.sort(reverse=True)
        
        return similarities[:top]

    
    def find_nearest_users_from_item(self, target_item, item_to_user, user_to_item, user_history):
        target_users = set()
        purchased_users = item_to_user[target_item]

        for user in purchased_users:
            users = self.find_nearest_user(user, item_to_user, user_to_item)
            if len(users) == 0:
                continue
            set_users = set(list(zip(*users))[1])
            new_users = set_users.difference(purchased_users)
            target_users = target_users.union(new_users)

        target_users = list(target_users)
        views = []
        purchases = []
        carts = []
        amount = []
        for userid in target_users:
            views.append(user_history.loc[userid, 'view'])
            purchases.append(user_history.loc[userid, 'purchase'])
            carts.append(user_history.loc[userid, 'cart'])
            amount.append(user_history.loc[userid, 'price'])
        
        target_df = pd.DataFrame(data={ 'Target users': target_users,
                                        '#Views': views,
                                        '#Purchases': purchases,
                                        '#AddedToCart': carts,
                                        'Amount Spent (USD)': amount})

        return target_df


    '''Helper'''
    def one_hot_encode(self, item, unique_user, item_to_user, user_to_idx):
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

    def CalcScore_cosine(self, item1, item2, unique_user, item_to_user, user_to_idx):
        '''
        Calculates the cosine similirity between two item IDs. Uses OneHotEncode helper function to retrieve one hot encodings for itemIDs.
        :param item1: item ID of item1
        :type item1: int
        :param item2: item ID of item2
        :type item2: int
        :return: Cosine Similarity Score
        :rtype: float
        '''
        a,b = self.one_hot_encode(item1, unique_user, item_to_user, user_to_idx), self.one_hot_encode(item2, unique_user, item_to_user, user_to_idx)

        cos_sim = dot(a, b)/(norm(a)*norm(b))
        return cos_sim

    def jaccard(self, s1, s2):
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