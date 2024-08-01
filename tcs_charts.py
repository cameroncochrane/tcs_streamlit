import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import TCS_pipeline as tcs


def show_country_page(country:str):
    data = tcs.TCSpipelineCountry(country=country)
    tcs.fill_m_q_p(data)

    data_chart = tcs.return_plot(data=data,country_name=country)

    st.title(f"{country} Sales Data")
    st.pyplot(fig=data_chart,use_container_width=True)

    tcs.name_columns_rows(data)
    tcs.add_df_titles(df_list=data,country=country)

    for i in range(0,len(data)):
        st.dataframe(data[i],use_container_width=True)

def home_page():
    st.title("Toy Car Sales Pipeline")
    st.write("This is a Streamlit dashboard which allows you to view the sales data of the Toy Car Sales dataset.")
    st.write("The dataset is a sample of sales data from a company selling toys. The data is formatted in a way that allows us to easily view the sales figures for each country.")

countries = tcs.country_list()
circle_icons = []
for i in range(0,len(countries)):
    circle_icons.append(f"{i+1}-circle") #Icons for the items in the sidebar list

with st.sidebar:
    selected = option_menu(menu_title="Main Menu",
        options= ["Home","Overview"] + countries,
        icons=["house","binoculars"] + circle_icons,#Uses bootstrap logos. See here for more icons: https://icons.getbootstrap.com/
        menu_icon="list",
        default_index=0)

if selected == "Home":
    home_page()

if selected in countries:
    show_country_page(selected)

#abc