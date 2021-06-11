import numpy as np
import pytest
import altair as alt
import pandas as pd
import datetime as dt

def generate_base_counts(data,metrics,grouped,top,asc=False,subset=(),choice = ()):
    if subset is not ():
        data_up = data.loc[data[subset]==choice]
        data_up = data_up.groupby([grouped]).count().loc[:,[metrics]]
    else:
        data_up = data.groupby([grouped]).count().loc[:,[metrics]] 
    data_up.reset_index(inplace = True)
    data_up = data_up.sort_values(by=metrics, axis = 0,ascending = asc)

    return data_up.iloc[:top,:]


def generate_base_sum(data,metrics,grouped,top,asc=False,subset=(),choice = ()):
    if subset is not ():
        data_up = data.loc[data[subset]==choice]
        data_up = data_up.groupby([grouped]).sum().loc[:,[metrics]]
    else:
        data_up = data.groupby([grouped]).sum().loc[:,[metrics]]
    data_up.reset_index(inplace = True)
    data_up = data_up.sort_values(by=metrics, axis = 0,ascending = asc)

    return data_up.iloc[:top,:]


def conversions(data,grouped,metric,comp,subset=(),choice = ()):
    if subset is not ():
        nov_grouped = data.loc[data[subset]==choice]
        nov_grouped = nov_grouped.groupby([grouped,'event_type']).count().loc[:,[metric]]
    else:
        nov_grouped = data.groupby([grouped,'event_type']).count().loc[:,[metric]]
       
    nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
    nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
    nov_grouped=nov_grouped.pivot(index=grouped, columns='event_type', values=metric).reset_index()
    nov_grouped['v2c: views to cart'] = (nov_grouped.cart/nov_grouped.view)
    nov_grouped['c2p: cart to payment'] = (nov_grouped.purchase/nov_grouped.cart)
    nov_grouped['v2p: views to payment'] = (nov_grouped.purchase/nov_grouped.view)
    nov_grouped = nov_grouped.loc[nov_grouped[grouped].isin(list(comp[grouped].unique()))]
    nov_grouped_t = nov_grouped.T.loc[[grouped,'v2c: views to cart','c2p: cart to payment','v2p: views to payment']]
    nov_grouped_t.columns = nov_grouped_t.loc[grouped,:]
    nov_grouped_t = nov_grouped_t.drop(grouped)
    nov_grouped_t.reset_index(inplace=True)
    nov_grouped_t=nov_grouped_t.melt(id_vars=['event_type'], 
            var_name=grouped, 
            value_name="conversion_value")
    return nov_grouped_t

def funnel(data,grouped,metric,subset=(),choice = ()):
        if subset is not ():
            nov_grouped = data.loc[data[subset]==choice]
            nov_grouped = nov_grouped.groupby([grouped,'event_type']).count().loc[:,[metric]]
        else:
            nov_grouped = data.groupby([grouped,'event_type']).count().loc[:,[metric]]

        nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
        nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
        nov_grouped=nov_grouped.pivot(index=grouped, columns='event_type', values=metric).reset_index()
        nov_grouped = nov_grouped.dropna().T
        nov_grouped.columns = nov_grouped.loc[grouped,:]
        nov_grouped = nov_grouped.drop(grouped)
        nov_grouped.reset_index(inplace=True)
        nov_grouped =nov_grouped.melt(id_vars=['event_type'], 
                var_name=grouped, 
                value_name="funnel_value")
        return nov_grouped



nov = pd.read_csv('main_TopTranNv.csv')
nov.event_time = pd.to_datetime(nov["event_time"]).dt.date
sales_nov = nov.loc[nov.event_type=='purchase']
carts_nov = nov.loc[nov.event_type=='cart']
views_nov = nov.loc[nov.event_type=='view']


top_10_cat_sales = generate_base_counts(sales_nov,metrics = 'product_id',grouped = 'category_code',top = 10)
nov_funnel = funnel(nov,grouped = 'category_code',metric = 'user_session')
# print(nov_funnel)

top_10_cat_rev = generate_base_sum(sales_nov,metrics = 'price',grouped = 'category_code',top = 10)
nov_conversions = conversions(nov,grouped = 'category_code',metric = 'user_session',comp = top_10_cat_sales )
# print(top_10_cat_rev)


def plot_top_cat(top_10_cat_sales,top_10_cat_rev):
    c1 = alt.Chart(top_10_cat_sales,title = 'Top 10 categories by # of Sales').mark_bar().encode(
    x=alt.X('product_id:Q',title = '# of sales'),
    y = alt.Y('category_code:N',sort = '-x') ,
)
    c2 = alt.Chart(top_10_cat_rev,title = 'Total Revenue').mark_text().encode(
    y=alt.Y('category_code:N',axis = None,sort = '-text'),
    text='price:Q'
).properties(width=100)
    c3 = c1|c2
    return c3

def plot_cat_con(nov_funnel):
    categories = list(nov_funnel.category_code.unique())
    top_10_cat_funnel = nov_funnel.loc[nov_funnel['category_code'].isin(categories)]

    cat_dropdown = alt.binding_select(options=categories)
    cat_select = alt.selection_single(fields=['category_code'], bind=cat_dropdown, name="Category")

    c4 = alt.Chart(top_10_cat_funnel,title = 'Novemeber:Conversion for top 10 category_codes').mark_bar().encode(
    x=alt.X('event_type:N',sort = ('view','cart','purchase')),
    y = alt.Y('funnel_value:Q'),
  
).properties(
    width=200,
    height=300
).resolve_scale(y='independent').add_selection(
    cat_select
).transform_filter(
    cat_select
).properties(title="Select a Category to view Customer Behavior")
    return c4



top_10_brand_sales = generate_base_counts(sales_nov,metrics = 'product_id',grouped = 'brand',top = 10)
top_10_brand_rev = generate_base_sum(sales_nov,metrics = 'price',grouped = 'brand',top = 10)
nov_brand_conversions = conversions(nov,grouped = 'brand',metric = 'user_session',comp = top_10_brand_sales )
nov_brand_funnel = funnel(nov,grouped = 'brand',metric = 'user_session')



def plot_top_brand(top_10_brand_sales,top_10_brand_rev):
    c5 = alt.Chart(top_10_brand_sales,title = 'Top 10 brands by # of Sales').mark_bar().encode(
    x=alt.X('product_id:Q',title = '# of sales'),
    y = alt.Y('brand:N',sort = '-x') ,
)

    c6 = alt.Chart(top_10_brand_rev,title = 'Total Revenue').mark_text().encode(
    y=alt.Y('brand:N',axis = None,sort = '-text'),
    text='price:Q'
).properties(width=100)

    c7 = c5 |c6
    return c7


def plot_brand_con(nov_brand_funnel):
    brands = list(nov_brand_funnel.brand.unique())
    brand_dropdown = alt.binding_select(options=brands)
    brand_select = alt.selection_single(fields=['brand'], bind=brand_dropdown, name="Brand")

    c8 = alt.Chart(nov_brand_funnel,title = 'Novemeber:Conversion for top 10 brands').mark_bar().encode(
    x=alt.X('event_type:N',sort = ('view','cart','purchase')),
    y = alt.Y('funnel_value:Q'),

).properties(
    width=200,
    height=300
).resolve_scale(y='independent').add_selection(
    brand_select
).transform_filter(
    brand_select
).properties(title="Select a Brand to view Customer Behavior")
    return c8



def plot_daily_sale(sales_nov):
    sales_by_date = sales_nov.groupby(['event_time','brand','category_code']).sum()
    sales_by_date.reset_index(inplace=True)
    sales_by_date = sales_by_date[['event_time','brand','price','category_code']]
    sales_by_date.columns=['event_time','brand','sales','category_code']
    sales_by_date['event_time'] = sales_by_date['event_time'].apply(lambda x:x.toordinal())
    sales_by_date['event_time']  = sales_by_date['event_time'] - sales_by_date['event_time'].iloc[0]
    brands_sbd = list(sales_by_date.brand.unique())
    brand_dropdown_sbd = alt.binding_select(options=brands_sbd)
    brand_select_sbd = alt.selection_single(fields=['brand'], bind=brand_dropdown_sbd, name="Brand")
    categories_sbd = list(sales_by_date.category_code.unique())
    cat_dropdown_sbd = alt.binding_select(options=categories_sbd)
    cat_select_sbd = alt.selection_single(fields=['category_code'], bind=cat_dropdown_sbd, name="Category")
    #Sales by date & brand &cat
    c9 = alt.Chart(sales_by_date,title = 'Sales by Date').mark_bar().encode(
    x = alt.X('event_time',scale=alt.Scale(domain=(1, 30))),
    y = 'sales:Q',

).properties(
    width=300,
    height=200
).resolve_scale(y='independent').add_selection(
    cat_select_sbd
).transform_filter(
    cat_select_sbd
).add_selection(
    brand_select_sbd
).transform_filter(
    brand_select_sbd
).properties(title="Select category and Brand to View Sales by Date")
    return c9



date = pd.DataFrame({'year': [2015, 2015,2015,2015,2015,2015, 2015,2015,2015,2015],

                   'month': [2, 2,2,2,2,2,2,2,2,2],

                   'day': [1,1,1,2,2,2,3,3,3,1]})
temp = pd.to_datetime(date)


def plot_general_con(nov):
    brands_sbd = list(nov.brand.unique())
    brand_dropdown_sbd = alt.binding_select(options=brands_sbd)
    brand_select_sbd = alt.selection_single(fields=['brand'], bind=brand_dropdown_sbd, name="Brand")
    
    categories_sbd = list(nov.category_code.unique())
    cat_dropdown_sbd = alt.binding_select(options=categories_sbd)
    cat_select_sbd = alt.selection_single(fields=['category_code'], bind=cat_dropdown_sbd, name="Category")

    master_grouped = nov.groupby(['category_code','brand', 'event_type']).agg({'user_session':'count', 'price':'sum'})
    master_grouped= master_grouped.reset_index()
    c10 = alt.Chart(master_grouped, title = 'Cat-> brand test').mark_bar().encode(
    x=alt.X('event_type:N'),
    y = alt.Y('user_session:Q',axis=alt.Axis(tickMinStep=1)),
).properties(
    width=200,
    height=300
).resolve_scale(y='independent').add_selection(
    cat_select_sbd 
).transform_filter(
    cat_select_sbd 
).add_selection(
    brand_select_sbd
).transform_filter(
    brand_select_sbd 
).properties(title="Select category and Brand to View Customer Behavior")
    return c10
