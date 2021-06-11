<p align="center">
<img src="./react-app/src/assets/logo.svg" alt="productRight" width="100">
</p>
<h1 align="center">ProductRight</h1>

> A Customized Product Dashboard

# Introduction
`ProductRight` is a business monitoring tool that displays the Sales (Revenue, # of orders) and
Product (Conversion and Funnel) KPI’s, top selling/low selling products in each category, recommends
discount bundles of products, and trends in customer behavior. The Dashboard will provide further
drill-drown filtering at a customer cohort, category, and brand level.

# Dataset
The [dataset](https://www.kaggle.com/mkechinov/ecommerce-behavior-data-from-multi-category-store) that we are using is from a middle-eastern, multi-department ecommerce company and has
user-event level data for the months of November and October of 2019. This is an extremely relevant
dataset as competitors to Amazon are resurfacing to disrupt the market. In fact, user-event level data
also plays a significant role in most product companies that want to track customer journeys to assess
product performance and customer stickiness.

Therefore, having a real-time tracking dashboard makes
it easier for cross-functioning teams to have consistent monitoring of what is selling and how it is selling
on their website. Moreover, having a dashboard that is interactive and also provides recommendations
and insights provides business teams with more strategies to leverage and reduces the time that they
would take to arrive at these forecasts.

# Visuals
One of the interactive plots will run a recommendation engine at its backend. It will take a product’s id as
input, and it will recommend top N users that can be targeted with that product’s advertisement. User
can also select any of the recommended user’s profile and check their purchase history.

Another visualization is week on week and month on month trends of individual categories/products
sales and views in order to see areas of growth/decline.


# User Story
The primary user is a business executive (likely a logistic/ procurement manager, product manager or
marketer), of an ecommerce website who is in charge of monitoring the health of the products,
identifying gaps and successes in the ecommerce business and creating new incentives and strategies
to optimize sales.
1) As a sales & marketing team member, I want to use promotions to attract more customers based
on correlation in selling different categories of goods.
2) I am a marketing manager at my ecommerce company and am in charge of identifying the
products that are frequently viewed together so that I can design bundle discount packages to
increase acquisition. I would like this info split at a customer cohort level for personalized
marketing offers.