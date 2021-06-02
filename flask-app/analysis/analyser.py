import pandas as pd


"""
    Analyser: provides functions to analyze pandas.DataFrame and output stats about them
"""


class Analyser:
    def __init__(self) -> None:
        pass

    '''Helpers'''

    def generate_base_counts(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).count().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).count().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]

    def generate_base_sum(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).sum().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).sum().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]

    def conversions(self, data, grouped, metric, comp, subset=(), choice=()):
        if subset != ():
            nov_grouped = data.loc[data[subset] == choice]
            nov_grouped = nov_grouped.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]
        else:
            nov_grouped = data.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]

        nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
        nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
        nov_grouped = nov_grouped.pivot(
            index=grouped, columns='event_type', values=metric).reset_index()
        nov_grouped['v2c: views to cart'] = (nov_grouped.cart/nov_grouped.view)
        nov_grouped['c2p: cart to payment'] = (
            nov_grouped.purchase/nov_grouped.cart)
        nov_grouped['v2p: views to payment'] = (
            nov_grouped.purchase/nov_grouped.view)
        nov_grouped = nov_grouped.loc[nov_grouped[grouped].isin(
            list(comp[grouped].unique()))]
        nov_grouped_t = nov_grouped.T.loc[[
            grouped, 'v2c: views to cart', 'c2p: cart to payment', 'v2p: views to payment']]
        nov_grouped_t.columns = nov_grouped_t.loc[grouped, :]
        nov_grouped_t = nov_grouped_t.drop(grouped)
        nov_grouped_t.reset_index(inplace=True)
        nov_grouped_t = nov_grouped_t.melt(id_vars=['event_type'],
                                           var_name=grouped,
                                           value_name="conversion_value")
        return nov_grouped_t

    def funnel(self, data, grouped, metric, subset=(), choice=()):
        if subset != ():
            nov_grouped = data.loc[data[subset] == choice]
            nov_grouped = nov_grouped.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]
        else:
            nov_grouped = data.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]

        nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
        nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
        nov_grouped = nov_grouped.pivot(
            index=grouped, columns='event_type', values=metric).reset_index()
        nov_grouped = nov_grouped.dropna().T
        nov_grouped.columns = nov_grouped.loc[grouped, :]
        nov_grouped = nov_grouped.drop(grouped)
        nov_grouped.reset_index(inplace=True)
        nov_grouped = nov_grouped.melt(id_vars=['event_type'],
                                       var_name=grouped,
                                       value_name="funnel_value")
        return nov_grouped

    def daily_sales_by_category_and_brand(self, sales_data):
        sales_by_date = sales_data.groupby(['event_time','brand','category_code']).sum()
        sales_by_date.reset_index(inplace=True)
        sales_by_date = sales_by_date[['event_time','brand','price','category_code']]
        sales_by_date.columns=['event_time','brand','sales','category_code']
        sales_by_date['event_time'] = sales_by_date['event_time'].apply(lambda x:x.toordinal())
        sales_by_date['event_time'] = sales_by_date['event_time'] - sales_by_date['event_time'].iloc[0]
        return sales_by_date

    def funnel_by_category_and_brand(self, data):
        funnel_grouped = data.groupby(['category_code','brand', 'event_type']).agg({'user_session':'count', 'price':'sum'})
        funnel_grouped= funnel_grouped.reset_index()
        return funnel_grouped

    def brands_by_category(self, sales_data):
        sales_by_brands = sales_data.groupby(['brand','category_code']).sum()
        sales_by_brands.reset_index(inplace=True)
        sales_by_brands = sales_by_brands[['brand','price','category_code']]
        sales_by_brands.columns=['brand','sales','category_code']
        return sales_by_brands

    def top_items_by_category(self, sales_data):
        cat_top_prods = sales_data.groupby(['category_code','product_id']).count()
        cat_top_prods.reset_index(inplace=True)
        cat_top_prods = cat_top_prods[['category_code','product_id','user_session']]
        cat_top_prods.columns=['category_code','product_id','user_session']
        cat_top_prods = cat_top_prods.groupby(['category_code']).apply(lambda x: x.nlargest(10,['user_session'])).reset_index(drop=True)
        return cat_top_prods

    def top_items_by_brand(self, sales_data):
        brand_top_prods = sales_data.groupby(['brand','product_id']).count()
        brand_top_prods.reset_index(inplace=True)
        brand_top_prods = brand_top_prods [['brand','product_id','user_session']]
        brand_top_prods.columns=['brand','product_id','user_session']
        brand_top_prods = brand_top_prods.groupby(['brand']).apply(lambda x: x.nlargest(10,['user_session'])).reset_index(drop=True)
        return brand_top_prods
