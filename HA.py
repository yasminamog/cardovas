#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:55:50 2023

@author: user
"""
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import hydralit_components as hc 


# Load data
df=pd.read_csv("cardiovascular-disease-death-rates.csv")
print(df.head())

# Rename columns to include spaces
df = df.rename(columns={"Entity":"Country","Deaths - Cardiovascular diseases - Sex: Both - Age: Age-standardized (Rate)":"Rate"})
print(df.head())

# data info
df.info()
df.isna().sum()

# Remove rows with missing values in the 'Code' column
df_cleaned = df.dropna(subset=['Code'])
df_cleaned.isna().sum()

# Check for duplicates
df_cleaned.duplicated().sum()

# Set the color and style using CSS
color_style = "color: darkblue"
font_style = "font-style: italic"

# Add a markdown component with the color and style
st.sidebar.markdown(f'<p style="{color_style}; {font_style}">Cardiovascular disease (CVD) stands as the leading cause of death globally, posing a significant challenge to public health. This project aims to delve into the rising trends of CVD death rates across various countries. By investigating the underlying factors contributing to this alarming pattern, we seek to enhance our understanding of CVD and develop effective strategies to combat its impact. Given its status as the primary disease burden, addressing CVD on a global scale is of utmost importance to improve health outcomes and reduce mortality rates..</p>', unsafe_allow_html=True)

# Tab layout
menu_data = [
    {'label': "Introduction", 'icon': '📊'},
    {'label': 'Line Graph & Map', 'icon': '🗺️'},
    {'label': 'Table', 'icon': '📄'},
    {'label': "Bar Plot", 'icon': '📊'},
    {'label': "Recommendations", 'icon': '💡'}
]

baby_blue_color = 'rgb(137, 207, 240)'

selected_menu = hc.nav_bar(
    menu_definition=menu_data,
    override_theme={
        'txc_inactive': 'white',
        'menu_background': baby_blue_color,
        'option_active': 'white'
    },
    hide_streamlit_markers=True,
    sticky_nav=True,
    sticky_mode='sticky'
)

# Page 1: Introduction
if selected_menu == "Introduction":
    st.title('The Final beat: Charting the Path of Cardiovascular Death Rates Across the Globe')
    st.write("Welcome to the Cardiovascular Disease Analysis App! This app aims to provide insights into the prevalence and impact of cardiovascular diseases worldwide.")
    st.image('Types_of_heart_diseases.jpg', use_column_width=True)
    
    st.header("Understanding Cardiovascular Diseases")
    st.write("Cardiovascular diseases (CVDs) encompass a range of conditions that affect the heart and blood vessels. These conditions include hypertension (high blood pressure), coronary heart disease (heart attack), cerebrovascular disease (stroke), heart failure, and other heart-related ailments.")
    df2=pd.read_csv("annual-number-of-deaths-by-cause.csv")
    df2.info()
    df2.isna().sum()
    # Drop rows with missing values
    df2_cleaned = df2.dropna()
    df2_cleaned.isna().sum()


    # Remove leading/trailing spaces from the column names
    df2_cleaned.columns = df2_cleaned.columns.str.strip()

    # Create a list of disease column names
    disease_columns = [
        'Meningitis', 'Alzheimer', 'Parkinson', 'Nutritional', 'Malaria', 'Drowning',
        'Interpersonal violence', 'Maternal disorders', 'HIV/AIDS', 'Drug',
        'Tuberculosis', 'Cardiovascular diseases', 'Lower respiratory infections',
        'Neonatal disorders', 'Alcohol', 'Self-harm', 'Diarrheal',
        'Environmental heat and cold exposure', 'Neoplasms',
        'Conflict and terrorism', 'Diabetes mellitus', 'Chronic kidney disease',
        'Poisonings', 'Protein-energy malnutrition', 'Road injuries',
        'Chronic respiratory diseases', 'Cirrhosis and other chronic liver diseases',
        'Digestive diseases', 'Fire, heat, and hot substances', 'Acute hepatitis'
    ]

    # Create a slider widget to select the year
    min_year = df2_cleaned['Year'].min()
    max_year = df2_cleaned['Year'].max()
    print(df2_cleaned['Year'].dtype)
    selected_year = st.slider("Select Year", min_value=min_year, max_value=max_year)

    # Create an empty list to store the cumulative rates
    cumulative_rates = []

    # Calculate the cumulative rate for each disease
    for disease in disease_columns:
        cumulative_rate = df2_cleaned.loc[df2_cleaned['Year'] <= selected_year, disease].mean()
        cumulative_rates.append(cumulative_rate)

    # Sort the diseases based on the cumulative rates in descending order
    sorted_diseases, sorted_rates = zip(*sorted(zip(disease_columns, cumulative_rates), key=lambda x: x[1], reverse=True))

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(18, 14))  # Increase the figure size
    bars = ax.barh(range(len(sorted_diseases)), sorted_rates[::-1])  # Reverse the order
    ax.set_yticks(range(len(sorted_diseases)))
    ax.set_yticklabels(sorted_diseases[::-1], fontsize=18)  # Reverse the order and increase the font size
    ax.set_xlabel('Cumulative Rate')
    ax.set_ylabel('Disease')
    ax.set_title(f"Cumulative Death Rate of Diseases up to {selected_year}", fontsize=20)

    # Add labels with values next to each bar
    for i, rate in enumerate(sorted_rates[::-1]):  # Reverse the order
        width = bars[i].get_width()
        ax.text(width, bars[i].get_y() + bars[i].get_height() / 2, f'{rate:.2f}', ha='left', va='center', fontsize=16)  # Increase the font size

    # Remove the list table from Streamlit app
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Display the bar plot
    st.pyplot(fig)
    
    st.write("CVDs pose a significant global health challenge, being one of the leading causes of death worldwide. The risk factors associated with CVDs include high blood pressure, elevated cholesterol levels, tobacco use, poor dietary choices, physical inactivity, obesity, and diabetes. Understanding these risk factors and their impact on cardiovascular health is crucial for implementing effective prevention strategies.")
    
    st.write("The objective of this app is to analyze and visualize data on death rates attributable to cardiovascular diseases across different countries and over time. By examining these trends, we can gain valuable insights into the burden of CVDs, identify high-risk regions, and inform evidence-based interventions and policy decisions.")

import time
import plotly.express as px
import streamlit as st

# Page 2: Scatter Plot and Choropleth Map
if selected_menu == "Line Graph & Map":
    st.title('Cardiovascular Death Rates Analysis')
    
    st.header('Scatter Plot')
    
    def load_data():
        return df_cleaned

    data = load_data()

    Unique_country = data['Country'].unique()

    # Select countries
    selected_countries = st.multiselect('Select countries', ["All"]+list(Unique_country), default="All")
    if 'All' in selected_countries:
        selected_countries = Unique_country

    # Filter the data
    filtered_data = data[data['Country'].isin(selected_countries)]

    # Create the scatter plot
    fig = px.scatter(filtered_data, x='Year', y='Rate', color='Country', hover_name='Country', log_x=True,
                     size_max=10, range_x=[filtered_data['Year'].min(), filtered_data['Year'].max()],
                     range_y=[filtered_data['Rate'].min(), filtered_data['Rate'].max()],
                     animation_frame='Year', animation_group='Country')

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Cardiovascular Death Rate'
    )

    # Display the scatter plot
    st.plotly_chart(fig)

    st.header('Choropleth Map')

    def load_data():
        return df_cleaned

    data = load_data()

    # Define the year range
    min_year = 1990
    max_year = 2019

    # Select year using a scrubber
    selected_year = st.slider('Select year', min_value=min_year, max_value=max_year, value=min_year, step=1, key='year_slider')

    # Filter the data
    filtered_data = data[data['Year'] == selected_year]

    # Create the map plot
    fig = px.choropleth(filtered_data, locations='Country', locationmode='country names',
                        color='Rate', hover_name='Country', range_color=[filtered_data['Rate'].min(), filtered_data['Rate'].max()],
                        color_continuous_scale='RdYlBu_r', labels={'Rate': 'Cardiovascular Death Rate'},
                        title='Cardiovascular Death Rates by Country',
                        animation_frame='Year', animation_group='Year')

    fig.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))

    # Display the map plot
    st.plotly_chart(fig)

# Page 3: Table
if selected_menu == "Table":
    st.title('Cardiovascular Disease Rate Comparison')

    # Create a multiselect box to select countries
    selected_countries = st.multiselect('Select countries', ['All'] + list(df_cleaned['Country'].unique()), default='All')

    # Create a slider widget to select the start and end years
    min_year = df_cleaned['Year'].min()
    max_year = df_cleaned['Year'].max()
    year_start, year_end = st.slider("Select Years", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    # Filter the data for the selected countries and years
    if 'All' in selected_countries:
        filtered_df = df_cleaned[(df_cleaned['Year'] >= year_start) & (df_cleaned['Year'] <= year_end)]
    else:
        filtered_df = df_cleaned[(df_cleaned['Country'].isin(selected_countries)) &
                                 (df_cleaned['Year'] >= year_start) &
                                 (df_cleaned['Year'] <= year_end)]

    # Group the data by country
    grouped_df = filtered_df.groupby('Country')

    # Create the table dataframe
    table_df = pd.DataFrame(columns=['Country', f'Rate ({year_start})', f'Rate ({year_end})', 'Relative Change', 'Absolute Change'])

    for country, data in grouped_df:
        rate_start = data[data['Year'] == year_start]['Rate'].values[0]
        rate_end = data[data['Year'] == year_end]['Rate'].values[0]
        relative_change = ((rate_end - rate_start) / rate_start) * 100
        absolute_change = rate_end - rate_start
        table_df = table_df.append({'Country': country, f'Rate ({year_start})': rate_start,
                                    f'Rate ({year_end})': rate_end, 'Relative Change': f'{relative_change:.2f}%',
                                    'Absolute Change': absolute_change}, ignore_index=True)

    # Display the table
    st.table(table_df)

import streamlit as st
import plotly.express as px

# Page 4: Bar Plot
if selected_menu == "Bar Plot":
    st.title('Cardiovascular Death Rates')

    # Create a filter for unique countries and years
    unique_countries = df_cleaned['Country'].unique()
    unique_years = df_cleaned['Year'].unique()

    # Create the multiselect box for countries
    selected_countries = st.multiselect('Select countries', unique_countries)

    # Create the dropdown box for years
    selected_year = st.selectbox('Select year', unique_years)

    # Filter the data based on selected countries and year
    filtered_data = df_cleaned[(df_cleaned['Country'].isin(selected_countries)) & (df_cleaned['Year'] == selected_year)]

    # Create the bar plot
    fig = px.bar(filtered_data, x='Country', y='Rate',
                 labels={'Rate': 'Death Rate'}, color='Country',
                 title=f'Cardiovascular Death Rate in {selected_year}')

    # Update the layout
    fig.update_layout(xaxis_title='Country', yaxis_title='Death Rate')

    # Display the plot
    st.plotly_chart(fig)

if selected_menu == "Recommendations":
    st.subheader("Recommendations")

    recommendations = [
        ("Implement higher tax rates on alcohol, tobacco products, and derivatives to discourage consumption and reduce cardiovascular risk factors. 💰🚭"),
        ("Investigate the correlation between healthcare sector investment and economic growth to emphasize the economic benefits of prioritizing healthcare. 💼💉"),
        ("Strengthen healthcare infrastructure by investing in the construction and renovation of facilities, particularly in underserved areas. 🏥🏗️"),
        ("Enhance healthcare workforce capacity by increasing medical schools, offering incentives for professionals to work in underserved areas, and providing continuous training opportunities. 👨‍⚕️👩‍⚕️📚"),
        ("Implement comprehensive screening and early detection programs for cardiovascular diseases. 🩺🔍"),
        ("Promote research and innovation in cardiovascular diseases through grants, collaborations, and knowledge sharing. 🧪🔬📝")
    ]

    for recommendation in recommendations:
        st.markdown(f"- {recommendation}")
  




   
















