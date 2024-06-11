import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from pandas import ExcelWriter
import openpyxl

# NEED TO MAKE SCRIPT HERE WHICH WOULD PLOT THE DATAFRAMES BELOW FORMED FOR EACH COUNTRY IN A PIPELINE. HARD TO DO ONE BY ONE FOR EACH COUNTRY.


def TCSpipelineCountry(country,generate_excel=False):
    """
    Returns a list of dataframes featuring the 7 different sales figures for a given country of the 'Toy Car Sales' dataset.

    If 'generate_excel' is set to True, the function will also generate an excel workbook with the dataframes as sheets.

    CC 2024
    
    """

    raw_data = pd.read_csv("Data/sales_data_sample_formatted.csv")
    data = raw_data.copy()

    data.drop(columns=["ORDERNUMBER","ORDERLINENUMBER"])

    ## Separating the dataset into its unique countries

    column_to_filter ='COUNTRY'
    unique_values = data[column_to_filter].unique()

    countryDictDFs = {val: data[data[column_to_filter] == val] for val in unique_values}

    # countryDictDFs is a dictionary of dataframes, one dataframe for each country.

    ## Selecting a country to process:

    countries = data["COUNTRY"].unique()
   

    country_data = countryDictDFs[country]

    # Total Number of Orders:
    country_total_orders = country_data.shape[0]

    # Average Sale Size per Order:
    country_average_sale_per_order = country_data["SALES"].mean()


    # Total Number of Orders (by Month):

    country_monthly_array = []
    for i in range(1,13):
        month_quant = country_data[country_data['MONTH_ID'] == i].shape[0]
        country_monthly_array.append(month_quant)

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    country_orders_by_month = {key:value for key, value in zip(months, country_monthly_array)}


    # Total Number of Orders (by Quarter):

    country_quarterly_array = []
    for i in range(1,5):
        quarter_quant = country_data[country_data['QTR_ID'] == i].shape[0]
        country_quarterly_array.append(quarter_quant)

    quarters = [1,2,3,4]
    country_orders_by_quarter = {key:value for key, value in zip(quarters, country_quarterly_array)}


    # Total Sales (by Month):

    column_to_filter = 'MONTH_ID'
    unique_values = country_data[column_to_filter].unique()

    country_months_dict_dfs = {val: country_data[country_data[column_to_filter] == val] for val in unique_values}
    country_monthly_total_sales = {val: country_months_dict_dfs[val]['SALES'].sum() for val in unique_values}


    # Total Sales (by Quarter):

    column_to_filter = 'QTR_ID'
    unique_values = country_data[column_to_filter].unique()

    country_quarter_dict_dfs = {val: country_data[country_data[column_to_filter] == val] for val in unique_values}
    country_quarterly_total_sales = {val: country_quarter_dict_dfs[val]['SALES'].sum() for val in unique_values}


    # Average Sales Amount per Order (by Month):

    column_to_filter = 'MONTH_ID'
    unique_values = country_data[column_to_filter].unique()
    country_average_sale_per_order_monthly = {val: country_months_dict_dfs[val]['SALES'].mean() for val in unique_values}


    # Average Sales Amount per Order (by Quarter):

    column_to_filter = 'QTR_ID'
    unique_values = country_data[column_to_filter].unique()
    country_average_sale_per_order_quarterly = {val: country_quarter_dict_dfs[val]['SALES'].mean() for val in unique_values}

    # Popular Product Categories:

    product_types = country_data['PRODUCTLINE'].unique()
    orders_per_product = []

    for item in product_types:
        order_quant = country_data[country_data['PRODUCTLINE'] == item].shape[0]
        orders_per_product.append(order_quant)

    country_orders_per_product = {key:value for key, value in zip(product_types, orders_per_product)}

    ## EXPORTING THE DATA TO EXCEL WORKBOOK(s) ##

    ## Firstly: Convert the dictionaries / arrays to be exported into dataframes:

    country_orders_by_month = pd.DataFrame(data=country_orders_by_month,index=[0]).transpose()
    country_orders_by_quarter = pd.DataFrame(data=country_orders_by_quarter,index=[0]).transpose()
    country_monthly_total_sales = pd.DataFrame(data=country_monthly_total_sales,index=[0]).transpose()
    country_quarterly_total_sales = pd.DataFrame(data=country_quarterly_total_sales,index=[0]).transpose()
    country_average_sale_per_order_monthly = pd.DataFrame(data=country_average_sale_per_order_monthly,index=[0]).transpose()
    country_average_sale_per_order_quarterly = pd.DataFrame(data=country_average_sale_per_order_quarterly,index=[0]).transpose()
    country_orders_per_product = pd.DataFrame(data=country_orders_per_product,index=[0]).transpose()


    # Getting the data into an excel workbook
    if generate_excel == True:
        country_sheet_name = str(f'{country}_Data_Analysed.xlsx')
        with pd.ExcelWriter(country_sheet_name) as writer:
            country_orders_by_month.to_excel(writer, sheet_name="TTL_ORDERS_M")
            country_orders_by_quarter.to_excel(writer, sheet_name="TTL_ORDERS_Q")
            country_monthly_total_sales.to_excel(writer, sheet_name="TTL_SALES_M")
            country_quarterly_total_sales.to_excel(writer, sheet_name="TTL_SALES_Q")
            country_average_sale_per_order_monthly.to_excel(writer, sheet_name="MEAN_SALES_M")
            country_average_sale_per_order_quarterly.to_excel(writer, sheet_name="MEAN_SALES_Q")
            country_orders_per_product.to_excel(writer, sheet_name="TTL_ORDERS_PROD")
    
    combined_metrics = [country_orders_by_month,
                        country_orders_by_quarter,
                        country_monthly_total_sales,
                        country_quarterly_total_sales,
                        country_average_sale_per_order_monthly,
                        country_average_sale_per_order_quarterly,
                        country_orders_per_product]
    
    return combined_metrics
            

def plot_country(country_data_clean):
    """
    Generates some (7) matplotlib plots for the given country data as a grid.
    """
    pass


country_list = ['USA', 'Germany', 'Norway', 'Spain', 'Denmark', 'Italy',
       'Philippines', 'UK', 'Sweden', 'France', 'Belgium', 'Singapore',
       'Austria', 'Australia', 'Finland', 'Canada', 'Japan', 'Ireland',
       'Switzerland']

for country in country_list:
    globals()[f"{country}_combined_metrics"] = TCSpipelineCountry(country,generate_excel=False)

plot_country(country_data_clean=USA_combined_metrics)