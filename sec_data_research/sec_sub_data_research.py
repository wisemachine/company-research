import streamlit as st
import pandas as pd
import datetime

# Function to load data from file
def load_initial_data():
    file_path = "/Users/harinikannan/Downloads/2024q3/sub.txt"
    return pd.read_csv(file_path, sep='\t', low_memory=False)

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
st.title("Job Application Tracker - SEC Company Database")

# Load initial dataset
df = get_initial_data()
st.write("Initial Dataset Loaded Successfully!")

st.info("For more SEC data files, refer to sub.txt files from: https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets")

# Option to load additional data
additional_file = st.file_uploader("Upload Additional SEC Dataset (CSV or TSV format)", type=["csv", "txt"])
if additional_file:
    additional_df = load_additional_data(additional_file)
    df = pd.concat([df, additional_df], ignore_index=True)
    st.write("Additional Dataset Loaded and Merged!")

# Add 'Applied' and 'Application Date' columns if they don't exist
if 'Applied' not in df.columns:
    df['Applied'] = False
if 'Application Date' not in df.columns:
    df['Application Date'] = pd.NaT

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

# Application Status Filter
application_status = st.sidebar.radio("Application Status", ["All", "Applied", "Not Applied"])

# Apply filters
if st.sidebar.button("Apply Filters"):
    filtered_df = df.copy()

    # Apply location filters
    if country_filter:
        filtered_df = filtered_df[filtered_df['countryba'] == country_filter]
    if state_filter:
        filtered_df = filtered_df[filtered_df['stprba'] == state_filter]
    if city_filter:
        filtered_df = filtered_df[filtered_df['cityba'] == city_filter]
    
    # Apply industry filter
    if industry_code:
        filtered_df = filtered_df[filtered_df['sic'] == int(industry_code)]
    
    # Apply incorporation filters
    if country_inc_filter:
        filtered_df = filtered_df[filtered_df['countryinc'] == country_inc_filter]
    if state_inc_filter:
        filtered_df = filtered_df[filtered_df['stprinc'] == state_inc_filter]
    
    # Apply application status filter
    if application_status == "Applied":
        filtered_df = filtered_df[filtered_df['Applied'] == True]
    elif application_status == "Not Applied":
        filtered_df = filtered_df[filtered_df['Applied'] == False]
    
    # Show results
    st.write("Filtered Results")
    
    # Create an editable dataframe
    edited_df = st.data_editor(
        filtered_df,
        column_config={
            "Applied": st.column_config.CheckboxColumn(
                "Applied",
                help="Mark if you've applied to this company",
                default=False,
            ),
            "Application Date": st.column_config.DateColumn(
                "Application Date",
                help="Date when you applied",
                format="YYYY-MM-DD",
            ),
        },
        hide_index=True,
    )
    
    # Update the main dataframe with edited values
    df.update(edited_df)
    
    st.write(f"Total Results Found: {filtered_df.shape[0]}")
    
    # Option to download results
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download Filtered Data", data=csv, file_name="filtered_companies.csv", mime="text/csv")

# Add a section for application statistics
st.header("Application Statistics")
total_companies = len(df)
applied_companies = df['Applied'].sum()
not_applied_companies = total_companies - applied_companies

col1, col2, col3 = st.columns(3)
col1.metric("Total Companies", total_companies)
col2.metric("Applied", applied_companies)
col3.metric("Not Applied", not_applied_companies)

# Add a chart to show application progress over time
st.subheader("Application Progress Over Time")
application_dates = df[df['Applied']]['Application Date'].value_counts().sort_index()
st.line_chart(application_dates.cumsum())

# Add a section for notes or comments
st.header("Notes")
notes = st.text_area("Add any general notes or reminders here")
if st.button("Save Notes"):
    # Here you would typically save the notes to a database or file
    st.success("Notes saved successfully!")
