# https://tcs-app-libertasdata.streamlit.app/ 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import TCS_functions as tcs

st.set_page_config(layout="wide")

countries = tcs.country_list()

def home_page():
    st.title("Toy Car Sales Pipeline")
    st.write("This is a Streamlit dashboard which allows you to view the sales data of the Toy Car Sales dataset.")
    st.write("The dataset is a sample of sales data from a company selling toys. The data is formatted in a way that allows us to easily view the sales figures for each country.")

def show_country_page(country:str):
    data = tcs.TCSpipelineCountry(country=country)
    data_index = tcs.df_indice_list
    tcs.fill_m_q_p(data)

    data_chart = tcs.return_plot(data=data,country_name=country)

    st.title(f"{country} Sales Data")
    st.pyplot(fig=data_chart,use_container_width=True)

    tcs.name_columns_rows(data)
    tcs.add_df_titles(df_list=data,country=country)

    for i in range(0,len(data)):
        st.dataframe(data[i],use_container_width=True)

    data_products = tcs.TCSpipelineCountry(country=country)
    tcs.fill_m_q_p(data_products)
    products_pie = tcs.return_pie_plot_orders_country(data=data_products,country_name=country)
    
    st.pyplot(fig=products_pie,use_container_width=False)

def sales_dashboard_page():

    st.title("Toy Car Sales Dashboard")

    col1, col2 = st.columns((1,1),gap='large')

    with col1:
        st.subheader("Country Comparisons")
        top_orders,top_sales = tcs.top_three_country()
        nest_col_1, nest_col_2 = st.columns((1,1))

        with nest_col_1:
            st.write("Sales by Country")
            st.dataframe(top_sales)
        
        with nest_col_2:
            st.write("Orders by Country")
            st.dataframe(top_sales)

        chart = tcs.plot_total_sales_by_country()
        st.pyplot(fig=chart,use_container_width=True)

        
    with col2:
        st.subheader("Worldwide and Europe")
        world_map = tcs.plot_sales_world_map()
        st.plotly_chart(world_map)

        world_map = tcs.plot_sales_europe_map()
        st.plotly_chart(world_map)


with st.sidebar:
    selected = option_menu(menu_title="Main Menu",
        options= ["Home","Sales Dashboard"] + countries,
        icons=["house","binoculars"], #Uses bootstrap logos. See here for more icons: https://icons.getbootstrap.com/
        menu_icon="list",
        default_index=0)

if selected == "Home":
    home_page()

if selected == "Sales Dashboard":
    sales_dashboard_page()

if selected in countries:
    show_country_page(selected)

