import streamlit as st
import pandas as pd
from pathlib import Path

# Function to load data from file
def load_initial_data():
    try:
        # Construct the path relative to the script's location
        file_path = Path(__file__).parent / "datasets" / "sub_2024q3.txt"
        return pd.read_csv(file_path, sep='\t', low_memory=False)
    except FileNotFoundError:
        st.error("Initial data file not found. Please ensure 'sub_2024q3.txt' exists in the sec_data_research/datasets directory.")
        return pd.DataFrame()  # Return empty DataFrame if file not found

# Function to load additional data
def load_additional_data(file):
    try:
        df = pd.read_csv(file, sep="\t", low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading additional data: {str(e)}")
        return pd.DataFrame()

# Load initial dataset
@st.cache_data
def get_initial_data():
    return load_initial_data()

# Streamlit App
st.title("SEC Company Explorer")

# Load initial dataset
df = get_initial_data()
total_companies = len(df)  # Total number of companies
st.write("Initial Dataset Loaded Successfully!")
st.write(f"Total Companies in Dataset: {total_companies}")

st.info("For more SEC data files, refer to sub.txt files from: https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets")

# Option to load additional data
additional_file = st.file_uploader("Upload Additional SEC Dataset (CSV or TSV format)", type=["csv", "txt"])
if additional_file:
    additional_df = load_additional_data(additional_file)
    df = pd.concat([df, additional_df], ignore_index=True)
    total_companies = len(df)  # Update total companies count
    st.write("Additional Dataset Loaded and Merged!")
    st.write(f"Updated Total Companies in Dataset: {total_companies}")

# Show initial data
st.write("Sample Data:", df.head())

# Filtering options
st.sidebar.header("Filter Options")

# Location Filters
country_filter = st.sidebar.text_input("Country (e.g., US)")
state_filter = st.sidebar.text_input("State/Province (e.g., CA)")
city_filter = st.sidebar.text_input("City (e.g., San Francisco)")

# Industry Filter
industry_code = st.sidebar.text_input("Industry SIC Code (e.g., 2834)")

# Incorporation Filters
country_inc_filter = st.sidebar.text_input("Country of Incorporation")
state_inc_filter = st.sidebar.text_input("State of Incorporation")

# Reset Filters Button
reset_filters = st.sidebar.button("Reset Filters")

# Apply filters
if st.sidebar.button("Apply Filters") or reset_filters:
    filtered_df = df.copy()

    # Apply location filters
    if country_filter and not reset_filters:
        filtered_df = filtered_df[filtered_df['countryba'] == country_filter]
    if state_filter and not reset_filters:
        filtered_df = filtered_df[filtered_df['stprba'] == state_filter]
    if city_filter and not reset_filters:
        filtered_df = filtered_df[filtered_df['cityba'] == city_filter]
    
    # Apply industry filter
    if industry_code and not reset_filters:
        filtered_df = filtered_df[filtered_df['sic'] == int(industry_code)]
    
    # Apply incorporation filters
    if country_inc_filter and not reset_filters:
        filtered_df = filtered_df[filtered_df['countryinc'] == country_inc_filter]
    if state_inc_filter and not reset_filters:
        filtered_df = filtered_df[filtered_df['stprinc'] == state_inc_filter]

    # Count of filtered companies
    filtered_companies_count = len(filtered_df)

    # Show results and counts
    st.write(f"Total Companies in Dataset: {total_companies}")
    st.write(f"Filtered Companies: {filtered_companies_count}")
    st.write("Filtered Results", filtered_df)
    
    # Option to download results
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download Filtered Data", data=csv, file_name="filtered_companies.csv", mime="text/csv")

# Add a section for notes or comments
st.header("Notes")
notes = st.text_area("Add any general notes or reminders here")
if st.button("Save Notes"):
    st.success("Notes saved successfully!")
