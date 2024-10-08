import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import plotly.express as px


# NEED TO MAKE SCRIPT HERE WHICH WOULD PLOT THE DATAFRAMES BELOW FORMED FOR EACH COUNTRY IN A PIPELINE. HARD TO DO ONE BY ONE FOR EACH COUNTRY.
def TCSpipelineCountry(country,generate_excel=False):
    """
    Returns a list of dataframes featuring the 7 different sales figures for a given country of the 'Toy Car Sales' dataset.

    If 'generate_excel' is set to True, the function will also generate an excel workbook with the dataframes as sheets.

    CC 2024
    
    """

    raw_data = pd.read_csv("sales_data_sample_formatted.csv")
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

# These are here so 'fill_m_q()' works. Don't need to use them when importing these modules:
def add_missing_months(dataframe):

    dataframe.sort_index()
    all_months = list(range(1,13))
    missing_months = [month for month in all_months if month not in dataframe.index]
    missing_df = pd.DataFrame(0,index=missing_months,columns=[0])
    new_dataframe = dataframe._append(missing_df).sort_index()

    return new_dataframe

def add_missing_quarters(dataframe):

    dataframe.sort_index()
    all_quarters = list(range(1,5))
    missing_quarters = [quarter for quarter in all_quarters if quarter not in dataframe.index]
    missing_df = pd.DataFrame(0,index=missing_quarters,columns=[0])
    new_dataframe = dataframe._append(missing_df).sort_index()

    return new_dataframe

def add_missing_products(dataframe):
    
    all_products = ['Vintage Cars','Motorcycles','Classic Cars','Trucks and Buses','Trains','Ships','Planes']
    missing_products = [product for product in all_products if product not in dataframe.index]
    missing_df = pd.DataFrame(0,index=missing_products,columns=[0])
    new_dataframe = dataframe._append(missing_df)

    return new_dataframe


# Use this function to fill in the missing months, quarters and procucts:
def fill_m_q_p(df_list):
    """
    Fills in the missing months, quarters and products in the list of dataframes for a particular country.

    CC 2024
    """
    
    df_name_index = {'country_orders_by_month':0,
    'country_orders_by_quarter':1,
    'country_monthly_total_sales':2,
    'country_quarterly_total_sales':3,
    'country_average_sale_per_order_monthly':4,
    'country_average_sale_per_order_quarterly':5,
    'country_orders_per_product':6}

    df_list[df_name_index['country_orders_by_month']] = add_missing_months(df_list[df_name_index['country_orders_by_month']])
    df_list[df_name_index['country_orders_by_quarter']] = add_missing_quarters(df_list[df_name_index['country_orders_by_quarter']])
    df_list[df_name_index['country_monthly_total_sales']] = add_missing_months(df_list[df_name_index['country_monthly_total_sales']])
    df_list[df_name_index['country_quarterly_total_sales']] = add_missing_quarters(df_list[df_name_index['country_quarterly_total_sales']])
    df_list[df_name_index['country_average_sale_per_order_monthly']] = add_missing_months(df_list[df_name_index['country_average_sale_per_order_monthly']])
    df_list[df_name_index['country_average_sale_per_order_quarterly']] = add_missing_quarters(df_list[df_name_index['country_average_sale_per_order_quarterly']])
    df_list[df_name_index['country_orders_per_product']] = add_missing_products(df_list[df_name_index['country_orders_per_product']])

def plot_data(data,country_name:str,save_image:bool,image_path:str):
    """
    - data (list): The list of dataframes generated by the 'TCSpipelineCountry' function.
    - country (str): The name of the country to be plotted.
    - image_path (str): The desired path name of the image of the charts plotted to be saved as.
    
    
    For the best results, use this function after firstly generating the data and then applying the 'fill_m_q_p()' function.
    
    e.g
    >>> usa_data = TCSpipelineCountry(country='USA',generate_excel=False)
    >>> fill_m_q_p(usa_data)
    >>> plot_data(usa_data,'USA',True,'USA_charts.png')

    CC 2024
    """
    df_names = {'country_orders_by_month':0,
    'country_orders_by_quarter':1,
    'country_monthly_total_sales':2,
    'country_quarterly_total_sales':3,
    'country_average_sale_per_order_monthly':4,
    'country_average_sale_per_order_quarterly':5,
    'country_orders_per_product':6}

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    quarters = ['Q1','Q2','Q3','Q4']

    fig, axs = plt.subplots(2,4, figsize=(20,10))

    # 1: Country Orders By Month
    ax = axs[0, 0]
    df = data[df_names['country_orders_by_month']]
    ax.bar(months, df[0], color='blue')
    ax.set_title(f'{country_name} Orders by Month')
    ax.set_xlabel('Month')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.set_ylabel('Orders')

    #2: Country Orders By Quarter
    ax = axs[0, 1]
    df = data[df_names['country_orders_by_quarter']]
    ax.bar(quarters, df[0], color='blue')
    ax.set_title(f'{country_name} Orders by Quarter')
    ax.set_xlabel('Quarter')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.set_ylabel('Orders')

    #3: Country Total Sales by Month
    ax = axs[0, 2]
    df = data[df_names['country_monthly_total_sales']]
    ax.bar(months, df[0], color='red')
    ax.set_title(f'{country_name} Total Sales by Month')
    ax.set_xlabel('Month')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')

    #4: Country Total Sales by Quarter
    ax = axs[0, 3]
    df = data[df_names['country_quarterly_total_sales']]
    ax.bar(quarters, df[0], color='red')
    ax.set_title(f'{country_name} Total Sales by Quarter')
    ax.set_xlabel('Quarter')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')

    #5: Country Average Sale per Order by Month
    ax = axs[1, 0]
    df = data[df_names['country_average_sale_per_order_monthly']]
    ax.bar(months, df[0], color='green')
    ax.set_title(f'{country_name} Average Sale per Order by Month')
    ax.set_xlabel('Month')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')
    #ax.set_ylim(3000,4000)

    #6: Country Average Sale per Order by Quarterly
    ax = axs[1, 1]
    df = data[df_names['country_average_sale_per_order_quarterly']]
    ax.bar(quarters, df[0], color='green')
    ax.set_title(f'{country_name} Average Sale per Order by Quarter')
    ax.set_xlabel('Quarter')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')
    #ax.set_ylim(3400,3800)

    #7: Country Orders per Product
    ax = axs[1, 2]
    df = data[df_names['country_orders_per_product']]
    ax.bar(df.index, df[0], color='orange')
    ax.set_title(f'{country_name} Orders per Product')
    ax.set_xlabel('Product')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Orders')

    if save_image == True:
        plt.savefig(image_path,format='png', dpi=300)
    
    plt.show()

def return_plot(data,country_name:str):
    
    df_names = {'country_orders_by_month':0,
    'country_orders_by_quarter':1,
    'country_monthly_total_sales':2,
    'country_quarterly_total_sales':3,
    'country_average_sale_per_order_monthly':4,
    'country_average_sale_per_order_quarterly':5,
    'country_orders_per_product':6}

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    quarters = ['Q1','Q2','Q3','Q4']

    fig, axs = plt.subplots(2,4, figsize=(20,10))

    # 1: Country Orders By Month
    ax = axs[0, 0]
    df = data[df_names['country_orders_by_month']]
    ax.bar(months, df[0], color='blue')
    ax.set_title(f'{country_name} Orders by Month')
    ax.set_xlabel('Month')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.set_ylabel('Orders')

    #2: Country Orders By Quarter
    ax = axs[0, 1]
    df = data[df_names['country_orders_by_quarter']]
    ax.bar(quarters, df[0], color='blue')
    ax.set_title(f'{country_name} Orders by Quarter')
    ax.set_xlabel('Quarter')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.set_ylabel('Orders')

    #3: Country Total Sales by Month
    ax = axs[0, 2]
    df = data[df_names['country_monthly_total_sales']]
    ax.bar(months, df[0], color='red')
    ax.set_title(f'{country_name} Total Sales by Month')
    ax.set_xlabel('Month')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')

    #4: Country Total Sales by Quarter
    ax = axs[0, 3]
    df = data[df_names['country_quarterly_total_sales']]
    ax.bar(quarters, df[0], color='red')
    ax.set_title(f'{country_name} Total Sales by Quarter')
    ax.set_xlabel('Quarter')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')

    #5: Country Average Sale per Order by Month
    ax = axs[1, 0]
    df = data[df_names['country_average_sale_per_order_monthly']]
    ax.bar(months, df[0], color='green')
    ax.set_title(f'{country_name} Average Sale per Order by Month')
    ax.set_xlabel('Month')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')
    #ax.set_ylim(3000,4000)

    #6: Country Average Sale per Order by Quarterly
    ax = axs[1, 1]
    df = data[df_names['country_average_sale_per_order_quarterly']]
    ax.bar(quarters, df[0], color='green')
    ax.set_title(f'{country_name} Average Sale per Order by Quarter')
    ax.set_xlabel('Quarter')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Sales')
    #ax.set_ylim(3400,3800)

    #7: Country Orders per Product
    ax = axs[1, 2]
    df = data[df_names['country_orders_per_product']]
    ax.bar(df.index, df[0], color='orange')
    ax.set_title(f'{country_name} Orders per Product')
    ax.set_xlabel('Product')
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.tick_params(axis='y',labelsize=8)
    ax.set_ylabel('Orders')

    # Normally to plot the chart, 'plt.show()' is used. If we want to return the chart, we don't do 'return plt', we do 'return x',
    # where x is what we put the chart in at the start (x, axes = plt.subplots()). It's 'fig' in this instance.
    return fig

def return_pie_plot_orders_country(data,country_name:str):
    """
    Creates a pie chart of the orders per product for a given country. 'data' should be generated from the 'TCSpipelineCountry' function,
    and should also have been transformed using the 'fill_m_q_p' function. 'country_name' is used in the chart title.
    """
    data_indices = df_indice_list()
    country_product_orders_index = data_indices['country_orders_per_product']
    product_data = data[country_product_orders_index]
    orders = list(product_data[0].values)
    products = list(product_data[0].index)

    fig, ax = plt.subplots(figsize=(8,3))
    ax.pie(orders)
    ax.set_title(f'{country_name} Orders by Product')
    ax.legend(products, loc="center left", bbox_to_anchor=(1, 0.5))
    
    return fig 

def country_list():
    country_list = ['USA', 'Germany', 'Norway', 'Spain', 'Denmark', 'Italy',
        'Philippines', 'UK', 'Sweden', 'France', 'Belgium', 'Singapore',
        'Austria', 'Australia', 'Finland', 'Canada', 'Japan', 'Ireland',
        'Switzerland']
    
    return country_list

def df_indice_list():
    
    df_indices = {'country_orders_by_month':0,
    'country_orders_by_quarter':1,
    'country_monthly_total_sales':2,
    'country_quarterly_total_sales':3,
    'country_average_sale_per_order_monthly':4,
    'country_average_sale_per_order_quarterly':5,
    'country_orders_per_product':6}

    return df_indices

def name_columns_rows(df_list:list):
    """
    Uses the list of dataframes that has beed generated from 'TCSpipelineCountry()', and gone through 'fill_m_q_p()' functions.
    """

    df_indices = {'country_orders_by_month': 0,
    'country_orders_by_quarter': 1,
    'country_monthly_total_sales': 2,
    'country_quarterly_total_sales': 3,
    'country_average_sale_per_order_monthly': 4,
    'country_average_sale_per_order_quarterly': 5,
    'country_orders_per_product': 6}

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    
    monthly_dfs = [df_list[df_indices['country_orders_by_month']],
                   df_list[df_indices['country_monthly_total_sales']],
                   df_list[df_indices['country_average_sale_per_order_monthly']]]
    
    for df in monthly_dfs:
        df.index = months
    
    quarterly_dfs = [df_list[df_indices['country_orders_by_quarter']],
                   df_list[df_indices['country_quarterly_total_sales']],
                   df_list[df_indices['country_average_sale_per_order_quarterly']]]
    
    for df in quarterly_dfs:
        df.index = quarters
    
    orders_dfs = [df_list[df_indices['country_orders_by_month']],
                  df_list[df_indices['country_orders_by_quarter']],
                  df_list[df_indices['country_orders_per_product']]]

    sales_dfs = [df_list[df_indices['country_monthly_total_sales']],
                 df_list[df_indices['country_quarterly_total_sales']]]

    misc_list = [df_list[df_indices['country_average_sale_per_order_monthly']],
                 df_list[df_indices['country_average_sale_per_order_quarterly']]]
    
    for df in orders_dfs:
        df.columns = ['Orders']
    
    for df in sales_dfs:
        df.columns = ['Sales ($)']
    
    for df in misc_list:
        df.columns = ['Average Sale per Order ($)']

    #Works nicely

def add_df_titles(country:str,df_list:list):
    """
    
    """

    df_indices = {'country_orders_by_month': 0,
    'country_orders_by_quarter': 1,
    'country_monthly_total_sales': 2,
    'country_quarterly_total_sales': 3,
    'country_average_sale_per_order_monthly': 4,
    'country_average_sale_per_order_quarterly': 5,
    'country_orders_per_product': 6}

    df_names = [f'{country} Orders by Month',
                f'{country} Orders by Quarter',
                f'{country} Total Sales by Month',
                f'{country} Total Sales by Quarter',
                f'{country} Average Sale per Order by Month',
                f'{country} Average Sale per Order by Quarter',
                f'{country} Orders per Product']
        
    for item in list(df_indices.keys()):
        df_list[df_indices[item]].columns = pd.MultiIndex.from_product([[df_names[df_indices[item]]], list(df_list[df_indices[item]].columns)])

def generate_all_data():
    """
    Uses a combination of the above functions to return a dictionary of dataframe lists of each country
    """

    countries = country_list()

    data_list = []

    for country in countries:
        data = TCSpipelineCountry(country=country)
        fill_m_q_p(data)
        name_columns_rows(data)
        add_df_titles(df_list=data,country=country)

        data_list.append(data)
    
    data_dict = dict(zip(countries,data_list))

    return data_dict

def plot_total_sales_by_country():

    index = df_indice_list()
    data = generate_all_data()
    countries = country_list()
    sales = []

    for country in countries:
        sales.append(data[f'{country}'][index['country_monthly_total_sales']][f'{country} Total Sales by Month']['Sales ($)'].sum())

    data = list(zip(countries,sales))
    data.sort(key=lambda x: x[1], reverse=True)
    sorted_countries,sorted_sales = zip(*data)

    blue_colors_hex = [
    "#00008B",  # DarkBlue
    "#0000CD",  # MediumBlue
    "#0000FF",  # Blue
    "#191970",  # MidnightBlue
    "#4169E1",  # RoyalBlue
    "#4682B4",  # SteelBlue
    "#1E90FF",  # DodgerBlue
    "#6495ED",  # CornflowerBlue
    "#00BFFF",  # DeepSkyBlue
    "#87CEEB",  # SkyBlue
    "#87CEFA",  # LightSkyBlue
    "#00CED1",  # DarkTurquoise
    "#48D1CC",  # MediumTurquoise
    "#40E0D0",  # Turquoise
    "#AFEEEE",  # PaleTurquoise
    "#B0E0E6",  # PowderBlue
    "#ADD8E6",  # LightBlue
    "#B0C4DE",  # LightSteelBlue
    "#F0F8FF",  # AliceBlue
    ]

    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(x=sorted_countries,height=sorted_sales,color=blue_colors_hex)
    ax.set_title(f'Total Sales by Country')
    ax.set_xlabel('Country')
    ax.tick_params(axis='x', labelsize=10, rotation=30)
    ax.set_ylabel('Sales ($)')

    return fig

def plot_sales_world_map():
    
    index = df_indice_list()
    data = generate_all_data()
    countries = country_list()
    sales = []

    for country in countries:
            sales.append(data[f'{country}'][index['country_monthly_total_sales']][f'{country} Total Sales by Month']['Sales ($)'].sum())

    data_dict = {'Country':countries,'Sales ($)':sales}
    data_df = pd.DataFrame(data_dict)

    fig = px.choropleth(data_dict, locations="Country",
                    locationmode='country names',
                    color="Sales ($)",
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Plasma)

    fig.update_layout(title='Sales Data by Country (Worldwide)')
    
    return fig

def plot_sales_europe_map():
    
    index = df_indice_list()
    data = generate_all_data()
    countries = country_list()
    sales = []

    for country in countries:
            sales.append(data[f'{country}'][index['country_monthly_total_sales']][f'{country} Total Sales by Month']['Sales ($)'].sum())

    data_dict = {'Country':countries,'Sales ($)':sales}
    data_df = pd.DataFrame(data_dict)

    drop_countries = ['USA','Australia','Singapore','Canada','Japan','Philippines']
    condition = data_df['Country'].isin(drop_countries)

    # Drop rows based on the condition
    df_europe = data_df.drop(data_df[condition].index)

    fig = px.choropleth(df_europe, locations="Country",
                    locationmode='country names',
                    color="Sales ($)",
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Plasma)

    fig.update_layout(title='Sales Data by Country (Europe)')

    fig.update_geos(
    scope="europe",
    projection_type="mercator"
    )
    
    return fig

def top_three_country():
    index = df_indice_list()
    data = generate_all_data()
    countries = country_list()
    sales = []
    orders = []

    for country in countries:
            sales.append(data[f'{country}'][index['country_monthly_total_sales']][f'{country} Total Sales by Month']['Sales ($)'].sum())
            orders.append(data[f'{country}'][index['country_orders_by_month']][f'{country} Orders by Month']['Orders'].sum())

    orders_dict = {'Country':countries,'Orders':orders}
    sales_dict = {'Country':countries,'Sales ($)':sales}

    orders_df = pd.DataFrame(orders_dict).sort_values(by='Orders',ascending=False)
    sales_df = pd.DataFrame(sales_dict).sort_values(by='Sales ($)',ascending=False)

    orders_df = orders_df.head(3)
    sales_df = sales_df.head(3)

    return orders_df, sales_df

def product_popularity():
    """
    Returns a dataframe and histogram chart of the number of orders for each product type.
    """

    data = pd.read_csv("sales_data_sample_formatted.csv")
    product_counts = data['PRODUCTLINE'].value_counts().reset_index()
    product_counts.columns = ['Product','Count']

    fig, ax = plt.subplots(figsize=(5,4))

    colors = ['#1157e3',
              '#59cf76',
              '#04ea3d',
              '#24e311',
              '#243922',
              '#2e347d',
              '#26855a']

    ax.bar(x=product_counts['Product'],height=product_counts['Count'],color=colors)
    ax.set_title('Product Popularity')
    ax.set_xlabel('Product')
    ax.tick_params(axis='x', labelsize=10, rotation=30)
    ax.set_ylabel('Number of Orders')

    return product_counts, fig

