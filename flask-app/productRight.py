import time
from flask import Flask

import vega_datasets
import altair as alt

from analysis import *

app = Flask(__name__)

# Initialize DataAnalysis class
mock_nov_data = '../mock-data/2019-Nov.csv'
data_analysis = DataAnalysis(data_path=mock_nov_data)


@app.route('/time')
def get_time():
    return {'time': time.time()}


@app.route('/vega')
def get_vega_js():
    cars = vega_datasets.data('cars')
    chart = alt.Chart(cars)
    chart = chart.mark_point().encode(x='Displacement')
    return chart.to_json()


'''Basic search'''
@app.route('/get-item/<item_id>')
def get_item(item_id):
    df = data_analysis.get_item(int(item_id))
    return df.to_json()


'''Basic analysis/ visualization'''
# By category
# TODO: top x
@app.route('/top-categories-by-sales-with-revenue')
def get_top_categories_by_sales_with_revenue():
    top_cat_sales = data_analysis.top_categories_by_sales()
    chart_sales = alt.Chart(top_cat_sales, title='Top 10 categories by # of Sales').mark_bar().encode(
        x=alt.X('product_id:Q', title='# of sales'),
        y=alt.Y('category_code:N', sort='-x'),
    )

    top_ten_cat_by_revenues = data_analysis.top_categories_by_revenues()
    chart_revenues = alt.Chart(top_ten_cat_by_revenues, title='Total Revenue').mark_text().encode(
        y=alt.Y('category_code:N', axis=None, sort='-text'),
        text='price:Q'
    ).properties(width=100)

    chart = chart_sales | chart_revenues
    return chart.to_json()


@app.route('/top-categories-by-revenues')
def get_top_categories_by_revenues():
    top_ten_cat_by_revenues = data_analysis.top_categories_by_revenues()
    chart = alt.Chart(top_ten_cat_by_revenues, title='Total Revenue').mark_text().encode(
        y=alt.Y('category_code:N', axis=None, sort='-text'),
        text='price:Q'
    ).properties(width=100)
    return chart.to_json()

# TODO: top x
@app.route('/customer-behavior-by-category')
def get_customer_behavior_by_category():
    nov_funnel = data_analysis.funnel_by_category()
    categories = list(nov_funnel.category_code.unique())

    top_10_cat_funnel = nov_funnel.loc[nov_funnel['category_code'].isin(
        categories)]

    cat_dropdown = alt.binding_select(options=categories)
    cat_select = alt.selection_single(
        fields=['category_code'], bind=cat_dropdown, name="Category")

    chart = alt.Chart(top_10_cat_funnel, title='Novemeber:Conversion for top 10 category_codes').mark_bar().encode(
        x=alt.X('event_type:N', sort=('view', 'cart', 'purchase')),
        y=alt.Y('funnel_value:Q'),
    ).properties(
        width=200,
        height=300
    ).resolve_scale(y='independent').add_selection(
        cat_select
    ).transform_filter(
        cat_select
    ).properties(title="Select a Category to view Customer Behavior")
    return chart.to_json()

# By brand
@app.route('/top-brands-by-sales-with-revenues')
def get_top_brands_by_sales():
    chart1 = alt.Chart(data_analysis.top_brands_by_sales(), title='Top 10 brands by # of Sales').mark_bar().encode(
        x=alt.X('product_id:Q', title='# of sales'),
        y=alt.Y('brand:N', sort='-x'),
    )

    chart2 = alt.Chart(data_analysis.top_brands_by_revenues(), title='Total Revenue').mark_text().encode(
        y=alt.Y('brand:N', axis=None, sort='-text'),
        text='price:Q'
    ).properties(width=100)

    chart = chart1 | chart2
    return chart.to_json()


@app.route('/customer-behavior-by-brand')
def get_customer_behavior_by_brand():
    nov_funnel_by_brand = data_analysis.funnel_by_brand()

    brands = list(nov_funnel_by_brand.brand.unique())
    brand_dropdown = alt.binding_select(options=brands)
    brand_select = alt.selection_single(
        fields=['brand'], bind=brand_dropdown, name="Brand")

    chart = alt.Chart(nov_funnel_by_brand, title='Novemeber:Conversion for top 10 brands').mark_bar().encode(
        x=alt.X('event_type:N', sort=('view', 'cart', 'purchase')),
        y=alt.Y('funnel_value:Q'),

    ).properties(
        width=200,
        height=300
    ).resolve_scale(y='independent').add_selection(
        brand_select
    ).transform_filter(
        brand_select
    ).properties(title="Select a Brand to view Customer Behavior")
    return chart.to_json()

@app.route('/brands-by-category')
def get_brands_by_category():
    brands_by_category = data_analysis.brands_by_category()

    # Get category list
    categories_sbd = list(brands_by_category.category_code.unique())
    cat_dropdown_sbd = alt.binding_select(options=categories_sbd)
    cat_select_sbd = alt.selection_single(fields=['category_code'], bind=cat_dropdown_sbd, name="Category")

    chart = alt.Chart(brands_by_category,title = 'Top Brands For Selected Category').mark_bar(size=8).encode(
        x = 'sales:Q',
        y = alt.Y('brand:N', sort='-x')
    ).properties(
        width=600,
        height=400
    ).resolve_scale(y='independent').add_selection(
        cat_select_sbd
    ).transform_filter(
        cat_select_sbd
    ).properties(title="Select a Category to view Top Brands")
    return chart.to_json()

# By date
@app.route('/daily-sales-by-category-and-brand')
def get_daily_sales_by_category_and_brand():
    sales_by_date = data_analysis.daily_sales_by_category_and_brand()

    # Get brand list
    brands_sbd = list(sales_by_date.brand.unique())
    brand_dropdown_sbd = alt.binding_select(options=brands_sbd)
    brand_select_sbd = alt.selection_single(
        fields=['brand'], bind=brand_dropdown_sbd, name="Brand")

    # Get category list
    categories_sbd = list(sales_by_date.category_code.unique())
    cat_dropdown_sbd = alt.binding_select(options=categories_sbd)
    cat_select_sbd = alt.selection_single(
        fields=['category_code'], bind=cat_dropdown_sbd, name="Category")

    chart = alt.Chart(sales_by_date, title='Sales by Date').mark_bar().encode(
        x=alt.X('event_time', scale=alt.Scale(domain=(1, 30))),
        y='sales:Q',
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
    return chart.to_json()

# Others
@app.route('/customer-behavior-by-category-and-brand')
def get_customer_behavior_by_category_and_brand():
    funnel_grouped = data_analysis.funnel_by_category_and_brand()

    # Get brand list
    brands_sbd = list(funnel_grouped.brand.unique())
    brand_dropdown_sbd = alt.binding_select(options=brands_sbd)
    brand_select_sbd = alt.selection_single(
        fields=['brand'], bind=brand_dropdown_sbd, name="Brand")

    # Get category list
    categories_sbd = list(funnel_grouped.category_code.unique())
    cat_dropdown_sbd = alt.binding_select(options=categories_sbd)
    cat_select_sbd = alt.selection_single(
        fields=['category_code'], bind=cat_dropdown_sbd, name="Category")

    chart = alt.Chart(funnel_grouped, title = 'Cat-> brand test').mark_bar().encode(
        x = alt.X('event_type:N'),
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
    return chart.to_json()

'''Recommendation'''
@app.route('/nearest-items/<item_id>')
def get_nearest_items(item_id):
    df = data_analysis.find_nearest_item(int(item_id))
    return df.to_json()
