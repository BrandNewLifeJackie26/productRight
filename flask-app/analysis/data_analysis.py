from pandas.core.frame import DataFrame
from .data_manager import *
from .recommender import *
from .analyser import *

"""
    DataAnalysis:
    1. Get data using DataManager
    2. Analyze data using Analyzer
    3. Make recommendation using Recommender
"""


class DataAnalysis:
    def __init__(self, data_path='') -> None:
        self.dm = DataManager(data_path)
        self.data = self.dm.fetch()

        # Data for basic analysis
        self.sales_nov, self.carts_nov, self.views_nov = None, None, None
        self.analyser = Analyser()
        self.data_preprocess_for_analysis()

        # Data for recommendation
        # Unique user and item
        self.unique_user, self.unique_item = set(), set()
        self.user_to_item, self.item_to_user = defaultdict(set), defaultdict(set)
        self.item_history = defaultdict(dict)
        self.user_history = pd.DataFrame({})
        self.user_to_idx, self.itemid_to_category_code, self.itemid_to_brand = dict(), dict(), dict()
        self.recommender = Recommender()
        self.data_preprocess_for_recommendation()

    def data_preprocess_for_analysis(self):
        if not (self.sales_nov and self.carts_nov and self.views_nov):
            self.data.event_time = pd.to_datetime(self.data["event_time"]).dt.date
            self.sales_nov = self.data.loc[self.data.event_type == 'purchase']
            self.carts_nov = self.data.loc[self.data.event_type == 'cart']
            self.views_nov = self.data.loc[self.data.event_type == 'view']

    def data_preprocess_for_recommendation(self):
        # Loop through all the rows and create a unique user and item set
        idx = 0
        for _, row in self.data.iterrows():
            userid, itemid, categorycode, brand, event_type, price = row[8], row[3], row[5], row[6], row[2], row[7] # TODO: wrongly indexed
            self.unique_user.add(userid)
            self.unique_item.add(itemid)

            if userid not in self.user_to_idx:
                self.user_to_idx[userid] = idx
                idx += 1

            if itemid not in self.item_history:
                self.item_history[itemid]['view']=0
                self.item_history[itemid]['purchase']=0
                self.item_history[itemid]['cart']=0
                self.item_history[itemid]['price']=price

            self.user_to_item[userid].add(itemid)
            self.item_to_user[itemid].add(userid)
            self.itemid_to_category_code[itemid] = categorycode
            self.itemid_to_brand[itemid] = brand
            self.item_history[itemid][event_type] += 1

            # User history
            userhistory_price = self.data[['price', 'user_id']]
            userhistory_event = self.data[['event_type', 'user_id']]

            one_hot_event = pd.get_dummies(userhistory_event['event_type'])
            userhistory_event = userhistory_event.drop('event_type',axis = 1)
            userhistory_event = userhistory_event.join(one_hot_event)

            price_df = userhistory_price.groupby(by='user_id').sum()
            event_df = userhistory_event.groupby(by='user_id').sum()
            self.user_history = price_df.join(event_df)

    '''Basic data processing'''
    def get_item(self, item_id=None):
        if item_id == None:
            return DataFrame()
        return self.data[self.data.product_id==item_id].iloc[0]

    '''Supported analyses'''
    # TODO: exceptions
    # By category
    def top_categories_by_sales(self, top=10):
        return self.analyser.generate_base_counts(
            self.sales_nov, metrics='product_id', grouped='category_code', top=top)

    def top_categories_by_revenues(self, top=10):
        return self.analyser.generate_base_sum(
            self.sales_nov, metrics='price', grouped='category_code', top=top)

    def conversions_by_category(self):
        top_10_cat_sales = self.top_categories_by_sales()
        return self.analyser.conversions(
            self.data, grouped='category_code', metric='user_session', comp=top_10_cat_sales)

    def funnel_by_category(self):
        return self.analyser.funnel(self.data, grouped='category_code', metric='user_session')

    def brands_by_category(self):
        return self.analyser.brands_by_category(self.sales_nov)

    def top_items_by_category(self):
        return self.analyser.top_items_by_category(self.sales_nov)

    # By brand
    def top_brands_by_sales(self, top=10):
        return self.analyser.generate_base_counts(self.sales_nov, metrics='product_id', grouped='brand', top=top)

    def top_brands_by_revenues(self, top=10):
        return self.analyser.generate_base_sum(self.sales_nov, metrics='price', grouped='brand', top=top)

    def funnel_by_brand(self):
        return self.analyser.funnel(self.data, grouped='brand', metric='user_session')

    def top_items_by_brand(self):
        return self.analyser.top_items_by_brand(self.sales_nov)

    # By date
    def daily_sales_by_category_and_brand(self):
        return self.analyser.daily_sales_by_category_and_brand(self.sales_nov)

    # Others
    def funnel_by_category_and_brand(self):
        return self.analyser.funnel_by_category_and_brand(self.data)

    '''Supported recommendations'''
    def find_nearest_item(self, item=None):
        if not item:
            return pd.DataFrame({})
        
        nearest_items = self.recommender.find_nearest_item(item, self.item_to_user, self.user_to_item)
        items_df = pd.DataFrame([{
            'item_id': item_id,
            'category': self.itemid_to_category_code[item_id],
            'brand': self.itemid_to_brand[item_id],
            'price (USD)': self.item_history[item_id]['price']
        } for _, item_id in nearest_items]).transpose()

        return items_df

    def find_nearest_users_from_item(self, item=None):
        if not item:
            return pd.DataFrame({})
        
        nearest_users = self.recommender.find_nearest_users_from_item(item, self.item_to_user, self.user_to_item, self.user_history)
        return nearest_users.transpose()
        