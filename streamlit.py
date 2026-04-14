import streamlit as st
import pandas as pd
import plotly.express as px


from analysis import *
# wide layout
st.set_page_config(layout="wide")


# title and subtitle
st.title("Global Electronics Retailer Dashboard")
st.subheader("Key Performance Indicators (KPIs)")

# Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
with col3:
    st.metric(label="Total Costs", value=f"${total_costs:,.2f}")
with col4:
    st.metric(label="Overall Profit Margin", value=f"{overall_profit_margin:.2f}%")



# yearly performance with buttons for each year
st.markdown("### Yearly Performance Overview")
st.write("Analyse revenue for each year. Please select the dropdown for specific years")
col5, col6 = st.columns(2)
with col5:
    year = st.selectbox("Select Year",sorted(year_month['order_year'].unique()))
    df_year = year_month[year_month['order_year'] == year].copy()
    df_year = df_year.sort_values('order_month')
    df_year['order_month'] = df_year['order_month'].dt.strftime('%b')
    st.bar_chart(df_year.set_index('order_month')['Revenue'])

# Volatility years
with col6:
    fig = px.bar(
        volatility_years,
        x='Year',
        y='CV',                          # ← was 'Volatility'
        title='Yearly volatility in revenue',
        color='CV',                      # ← was 'Volatility'
        color_continuous_scale='Blues',
        text=volatility_years['CV'].map('{:.1f}%'.format),
        labels={'CV': 'Coefficient of Variation (%)'}
    )
    fig.update_layout(
        height=460,
        coloraxis_showscale=False,
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


st.divider()
# top 20 products
st.markdown('### Top 5 products')
st.write('Explore top 5 products that brings the most income')
top_products_display = top_products.copy()
top_products_display['Profit'] = top_products_display['Profit'].apply(lambda x: numerize.numerize(x))
top_products_display['Revenue'] = top_products_display['Revenue'].apply(lambda x: numerize.numerize(x))
top_products_display['Cost'] = top_products_display['Cost'].apply(lambda x: numerize.numerize(x))

st.dataframe(top_products_display, width='stretch', height='auto')




st.divider()
st.header('Revenue by location')
col7, col8 = st.columns(2)

# with col 7 add a dropdown with option 'Lowest countries' and 'Top countries'
with col7:
    top_lower = st.selectbox(
        'Select Option',
        ['Top Countries', 'Lowest Countries'],
        key='country_selector'
    )
    if top_lower == 'Top Countries':
        fig = px.bar(
            top_five_revenue_countries,
            x='Country',
            y='Revenue',
            title='Top 5 Countries by Revenue'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(
            lowest_five_revenue_countries,
            x='Country',
            y='Revenue',
            title='Lowest 5 Countries by Revenue'
        )
        st.plotly_chart(fig, use_container_width=True)

# top_five_revenue_cities, lowest_five_revenue_cities col8 display with toggle
with col8:
    cities_toggle = st.selectbox('Select Option', ['Top Cities', 'Lowest Cities'], key='city_selector')
    if cities_toggle == 'Top Cities':
        fig = px.bar(
            top_five_revenue_cities,
            x='City',
            y='Revenue',
            title='Top 5 Cities by Revenue'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(
            lowest_five_revenue_cities,
            x='City',
            y='Revenue',
            title='Lowest 5 Cities by Revenue'
        )
        st.plotly_chart(fig, use_container_width=True)