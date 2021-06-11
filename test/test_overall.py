import pytest
import unittest
from recommendation_engine import *
from analysis_engine import *


def test_Initialpreprocessing():
  '''
  test for data_preprocess_for_recommendation() method of data_analysis.py
  '''
  assert isinstance(unique_item,set)
  assert isinstance(unique_user,set)
  assert isinstance(user_to_idx,dict)
  assert isinstance(user_to_item,dict)
  assert isinstance(item_to_user,dict)
  assert isinstance(itemid_to_category_code,dict)
  assert isinstance(itemid_to_brand,dict)
  assert isinstance(item_history,dict)

def test_OneHotEncode():
  '''
  tests for OneHotEncoding function 
  '''
  sample_item = 2

  test_vector = OneHotEncode(sample_item)
  assert isinstance(test_vector,list)
  for i in test_vector:
      assert i==0 or i==1

  assert test_vector==[1,1,0]
  

def test_CalcScore_cosine():
  '''
  tests for CalcScore_cosine function
  '''
  test_item1, test_item2 = 1, 2

  cos_score = CalcScore_cosine(test_item1, test_item2)
  assert cos_score==0.7071067811865475

  assert isinstance(cos_score,float)


def test_jaccard():
  '''
  tests for jaccard function
  '''
  test_item1, test_item2 = item_to_user[1], item_to_user[2]
  score = jaccard(test_item1, test_item2)

  assert score==0.5
  assert isinstance(score,float)
  
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

def test_findNearestItem():
  '''
  tests for findNearestItem function
  '''
  test_item=1

  nearestItemList = findNearestItem(test_item)
  assert isinstance(nearestItemList,list)
  assert nearestItemList[0][1] in unique_item
  assert nearestItemList[0][0]==0.5

 
def test_findNearestUser():
  '''
  tests for findNearestUser function
  '''
  test_user=2

  nearestUserList = find_Nearest_User(test_user,item_to_user,user_to_item)
  assert isinstance(nearestUserList,list)
  assert nearestUserList[0][1] in unique_user
  assert nearestUserList[0][0]==0.5

def test_findNearestUsersfromItem():
  '''
  tests for findNearestUsersfromItem function
  '''
  test_item=1

  targetUserList = findNearestUsersfromItem(test_item,item_to_user,user_to_item)
  first_row = targetUserList.head(2)
  assert int(first_row['Target users']) ==2
  assert int(first_row['#Views']) ==0
  assert int(first_row['#Purchases'] ==0)
  assert int(first_row['#AddedToCart'] ==1)
  assert int(first_row['Amount Spent'] ==101)


#Testing for analytial window

def test_generate_base_counts():
    d = {'product_id':[1,2,1,3,1,2],'cat_id':[1,2,1,1,2,2]}
    test_data = pd.DataFrame(data=d)
    test_result = generate_base_counts(test_data,metrics = 'product_id',grouped = 'cat_id',top = 1)
    expected_result = [1]
    assert test_result['cat_id'].values == expected_result

def test_generate_base_sum():
    d = {'price':[1,3,4,5,6,7,1,5,6,7],'cat_id' :[1,2,3,2,3,1,3,2,1,1]}
    test_data = pd.DataFrame(data = d)
    test_result = generate_base_sum(test_data,metrics = 'price',grouped = 'cat_id',top = 2)
    expected_result = np.array([[1,21],[2,13]])
    assert np.all(test_result==expected_result)==True

def test_conversions():
    d = {'cat_id':[1,2,2,1,1,2,1,1,2,2],'user_session':[1,2,3,4,5,6,7,8,9,10],
         'event_type' : ['cart','view','purchase','purchase','view','view','cart','cart','purchase','view']}
    test_data = pd.DataFrame(data = d)
    test_1 ={'cat_id':[1,1,1,1,1,1,1,1,1,1]}
    test_2 = pd.DataFrame(data = test_1)
    test_result = conversions(test_data,grouped = 'cat_id',metric = 'user_session',comp = test_2 )
    expected_result1 = np.array(['v2c: views to cart','c2p: cart to payment','v2p: views to payment'])
    expected_result2 = np.array([1.0,1.0,1.0])
    expected_result3 = np.array([3.0,1/3,1.0])
    assert np.all(test_result['event_type'].values==expected_result1)==True
    assert np.all(test_result['cat_id'].values==expected_result2)==True
    assert np.all(test_result['conversion_value'].values==expected_result3)==True


def test_funnel():
    d = {'cat_id':[1,2,2,1,1,2,1,1,2,2],'user_session':[1,2,3,4,5,6,7,8,9,10],
         'event_type' : ['cart','view','purchase','purchase','view','view','cart','cart','purchase','view']}
    test_data = pd.DataFrame(data = d)
    test_result = funnel(test_data,grouped = 'cat_id',metric = 'user_session')
    expected_result1 = np.array(['cart','purchase','view'])
    expected_result2 = np.array([1.0,1.0,1.0])
    expected_result3 = np.array([3.0,1.0,1.0])
    assert np.all(test_result['event_type'].values==expected_result1)==True
    assert np.all(test_result['cat_id'].values==expected_result2)==True
    assert np.all(test_result['funnel_value'].values==expected_result3)==True
    

def test_plot_top_cat():
    test1 = pd.DataFrame(data = {'product_id':[102,111,32],'category_code':[1,2,3]})
    test2 = pd.DataFrame(data = {'price':[1020,1110,320],
                                 'category_code':[1,2,3]})
    ctest = plot_top_cat(test1,test2)
    test_dict = ctest.to_dict()
    assert test_dict["hconcat"][0]["mark"]=='bar'
    assert test_dict["hconcat"][0]['encoding']['y']['sort'] == '-x'
    assert test_dict["hconcat"][1]['encoding']['y']['sort'] =='-text'
    assert test_dict["hconcat"][1]['width'] ==100

def test_cat_con():
    test = pd.DataFrame(data = {'event_type':['view','purchase','view','cart','view','purchase'],
                               'category_code':[1,2,2,2,1,1],'funnel_value' :[5,6,4,3,9,10]})
    test_result = plot_cat_con(test)
    test_dict = test_result.to_dict()
    assert test_dict['mark']=='bar'
    assert test_dict['encoding']['x']['sort']== ['view', 'cart', 'purchase']
    assert test_dict['selection']['Category']['fields'] == ['category_code']
    assert test_dict['selection']['Category']['bind']['options'] == [1.0, 2.0]

def test_plot_top_brand():
    test1 = pd.DataFrame(data = {'product_id':[102,111,32,45,1,34,90,12,5,1],'brand':[1,2,3,2,1,3,3,2,1,3]})
    test2 = pd.DataFrame(data = {'price':[1020,1110,320,450,10,349,909,152,56,13],
                                 'brand':[1,2,3,2,1,3,3,2,1,3]})
    ctest = plot_top_brand(test1,test2)
    test_dict = ctest.to_dict()
    assert test_dict["hconcat"][0]["mark"]=='bar'
    assert test_dict["hconcat"][0]['encoding']['y']['sort'] == '-x'
    assert test_dict["hconcat"][1]['encoding']['y']['sort'] =='-text'
    assert test_dict["hconcat"][1]['width'] ==100
    


def test_plot_brand_con():
    test = pd.DataFrame(data = {'event_type':['view','purchase','view','cart','view','purchase'],
                               'brand':[1,2,2,2,1,1],'funnel_value' :[5,6,4,3,9,10]})
    test_result = plot_brand_con(test)
    test_dict = test_result.to_dict()
    assert test_dict['mark']=='bar'
    assert test_dict['encoding']['x']['sort']== ['view', 'cart', 'purchase']
    assert test_dict['selection']['Brand']['fields'] == ['brand']
    assert test_dict['selection']['Brand']['bind']['options'] == [1.0, 2.0]

def test_plot_daily_sale():
    test = pd.DataFrame(data = {'event_time':[1,2,3,1,3,2,3,1,2,2],'brand':[1,2,1,2,1,2,1,2,1,2],
                               'category_code' :[3,4,3,4,3,4,3,4,3,4],'price':[1,2,3,4,5,6,7,8,9,3]})
    date = pd.DataFrame({'year': [2015, 2015,2015,2015,2015,2015, 2015,2015,2015,2015],

                   'month': [2, 2,2,2,2,2,2,2,2,2],

                   'day': [1,1,1,2,2,2,3,3,3,1]})
    temp = pd.to_datetime(date)
    test['event_time'] = temp
    test_result = plot_daily_sale(test)
    test_dict = test_result.to_dict()
    assert test_dict['mark'] == 'bar'
    assert test_dict['height'] == 200
    assert test_dict['width'] == 300
    assert test_dict['selection']['Brand']['fields'] == ['brand']
    assert test_dict['selection']['Brand']['bind']['options'] == [1.0, 2.0]
    assert test_dict['selection']['Category']['fields'] == ['category_code']
    assert test_dict['selection']['Category']['bind']['options'] == [3.0,4.0]
    assert test_dict['encoding']['x']['scale']['domain'] == [1,30]


def test_general_con():
    test = pd.DataFrame(data = {'category_code':[1,2,2,1,1,1,1,1,2,2],'brand':[3,4,4,3,4,4,4,3,4,3],
                               'event_type': ['view','purchase','view','purchase',
                                              'view','cart','view','purchase','cart','cart'],
                               'user_session':[0,1,2,3,4,5,6,7,8,9],
                               'price':[34,43,23,56,12,3,5,87,9,22]})
    test_result = plot_general_con(test)
    test_dict = test_result.to_dict()
    assert test_dict['mark']=='bar'
    assert test_dict['width']==200
    assert test_dict['height']==300
    assert test_dict['selection']['Category']['fields'] == ['category_code']
    assert test_dict['selection']['Brand']['fields'] == ['brand'] 
    assert test_dict['selection']['Brand']['bind']['options'] == [3.0,4.0]
    assert test_dict['selection']['Category']['bind']['options'] == [1.0,2.0]

test_Initialpreprocessing()
test_OneHotEncode()
test_CalcScore_cosine()
test_jaccard()
test_findNearestItem()
test_findNearestUser()
test_findNearestUsersfromItem()

test_general_con()
test_plot_daily_sale()
test_plot_brand_con()
test_plot_top_brand
test_cat_con()
test_plot_top_cat()
test_funnel()
test_conversions()
test_generate_base_sum()
test_generate_base_counts()
