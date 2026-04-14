from numerize import numerize




# load datasets
import pandas as pd
import matplotlib.pylab as plt
import numpy as np

df_sales = pd.read_csv('Sales.csv', encoding='latin1')                      # Cleaned
df_customers = pd.read_csv('Customers.csv', encoding='latin1')              # Cleaned
df_products = pd.read_csv('Products.csv', encoding='latin1')                # Cleaned
df_stores = pd.read_csv('Stores.csv', encoding='latin1')                    # Cleaned
df_fx = pd.read_csv('Exchange_Rates.csv', encoding='latin1')



df_sales['Order Date'] = pd.to_datetime(df_sales['Order Date'])
df_sales['Delivery Date'] = pd.to_datetime(df_sales['Delivery Date'])
null_value_delivery_date = df_sales['Delivery Date'].isnull().mean() * 100

df_sales['order_month'] = df_sales['Order Date'].dt.to_period('M')
df_sales['order_year'] = df_sales['Order Date'].dt.year

for col in ['Unit Cost USD', 'Unit Price USD']:
    df_products[col] = (
        df_products[col]
        .astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
    )
    
for col in ['Unit Cost USD', 'Unit Price USD']:
    df_products[col] = pd.to_numeric(df_products[col], errors='coerce')



df_customers['Birthday'] = pd.to_datetime(df_customers['Birthday'])


df_stores['Open Date'] = pd.to_datetime(df_stores['Open Date'])
# Joining products dataframe and sales
main_df = pd.merge(df_sales, df_products, how='left', on='ProductKey')




main_df['Revenue'] = main_df['Quantity'] * main_df['Unit Price USD']
main_df['Profit'] = (main_df['Quantity'] * main_df['Unit Price USD']) - (main_df['Quantity'] * main_df['Unit Cost USD'])
# Cost per transaction
main_df['Cost'] = main_df['Quantity'] * main_df['Unit Cost USD']

# profit margin per product
main_df['Profit Margin'] = np.where(
    main_df['Revenue'] != 0,
    (main_df['Profit'] / main_df['Revenue']) * 100,
    0
)





# find out the main KPIs
total_revenue = main_df['Revenue'].sum()
total_profit = main_df['Profit'].sum()
total_costs = main_df['Cost'].sum()
overall_profit_margin = (total_profit / total_revenue) * 100

total_volume = main_df['Quantity'].sum()


# year groups
year_groups = main_df.groupby('order_year')[['Revenue', 'Cost', 'Profit']].sum().reset_index()

# first year grouping
year_month = main_df.groupby(["order_year", "order_month"])[["Revenue", "Cost", "Profit"]].sum().reset_index()

# best profit grouping by revenue, costs and profit
top_products = main_df.groupby(['Product Name'])[['Revenue', 'Cost', 'Profit']].sum().sort_values('Profit', ascending=False).head(5).reset_index()



# volatility years
volatility_years = (
    main_df.groupby('order_year')['Revenue']
    .agg(std='std', mean='mean')
    .reset_index()
)
volatility_years['CV'] = (volatility_years['std'] / volatility_years['mean']) * 100
volatility_years.rename(columns={'order_year': 'Year'}, inplace=True)
volatility_years = volatility_years.sort_values('CV', ascending=False)




# merge customers
main_df = pd.merge(main_df, df_customers, on='CustomerKey', how='left')



# countries and cities
# top and lowest earning countries
top_five_revenue_countries = (
    main_df.groupby('Country')[['Quantity', 'Revenue', 'Profit']]
    .sum()
    .sort_values('Revenue', ascending=False)
    .reset_index()
    .head(5)
)
# top_five_revenue_countries = main_df.groupby(['Country'])[['Quantity', 'Revenue', 'Profit']].sum().sort_values('Revenue', ascending=False).reset_index().head(5)
lowest_five_revenue_countries = main_df.groupby(['Country'])[['Quantity', 'Revenue', 'Profit']].sum().sort_values('Revenue', ascending=True).reset_index().head(5)


top_five_revenue_cities = main_df.groupby(['City'])[['Quantity', 'Revenue', 'Profit']].sum().sort_values('Revenue', ascending=False).reset_index().head(5)
lowest_five_revenue_cities = main_df.groupby(['City'])[['Quantity', 'Revenue', 'Profit']].sum().sort_values('Revenue', ascending=True).reset_index().head(5)