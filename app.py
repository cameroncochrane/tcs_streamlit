# https://tcs-app-libertasdata.streamlit.app/ 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import TCS_functions as tcs

st.set_page_config(layout="wide")

#### FUNCTIONS FOR EACH PAGE TYPE

def home_page():
    st.title("Toy Car Sales")
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
        nest_col_1_1, nest_col_1_2 = st.columns((1,1))

        with nest_col_1_1:
            st.write("Sales by Country")
            st.dataframe(top_sales)
        
        with nest_col_1_2:
            st.write("Orders by Country")
            st.dataframe(top_sales)

        chart = tcs.plot_total_sales_by_country()
        st.pyplot(fig=chart,use_container_width=True)

        st.subheader("Product Comparisons")
        product_table, product_chart = tcs.product_popularity()


        nest_col_2_1, nest_col_2_2 = st.columns((1,1))

        with  nest_col_2_1:
            st.dataframe(product_table)
        with nest_col_2_2:
            st.pyplot(fig=product_chart,use_container_width=True)

        
    with col2:
        st.subheader("Worldwide and Europe")
        world_map = tcs.plot_sales_world_map()
        st.plotly_chart(world_map)

        world_map = tcs.plot_sales_europe_map()
        st.plotly_chart(world_map)

#### EXECUTE THIS FUNCTION TO LOAD THE APP ####
def load_app():

    countries = tcs.country_list()

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

#### ENTERING THE APP WITH A PASSWORD ####

# Set the correct password
correct_password = "toycarsales"

# Function to check the password
def check_password():
    st.session_state["password_correct"] = st.session_state["password"] == correct_password

def input_password():
    st.text_input("Enter the password", type="password", on_change=check_password, key="password")
    st.button("Submit")
    # Ask the user for the password


# Input for the password
if "password_correct" not in st.session_state:
    # Ask the user for the password
    input_password()
else:
    # Check if the password is correct
    if st.session_state["password_correct"]:
        load_app()
        
    else:
        st.session_state.pop("password_correct")
        st.write("Incorrect password.")
        # Optionally, clear the incorrect password input
        input_password()

