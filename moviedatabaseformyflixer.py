import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm

# Create a Streamlit app
st.title("Movie Name and First Four Digits Extraction App")

# Input for the URLs from the user
st.write("Enter the URLs of the movie pages (one URL per line):")
urls_input = st.text_area("URLs")

# Split the user input into a list of URLs
urls = urls_input.split('\n') if urls_input else []

# Display the total number of user-inputted URLs
total_urls = len(urls)
st.write(f"Total inputted URLs: {total_urls}")

# Create an empty set to store unique data
unique_data_set = set()

# Function to scrape movie name
def scrape_movie_name(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the movie name element
            name_element = soup.find("h2", class_="heading-name")

            # Extract the text from the element
            movie_name = name_element.text.strip() if name_element else "Not found"

            return movie_name
        else:
            return None
    except Exception as e:
        return None

# Function to scrape and extract the first four digits from text within a class
def scrape_first_four_digits_from_class(url, class_name):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the element with the specified class name
            info_element = soup.find("div", class_=class_name)

            # Extract the text from the element
            info_text = info_element.text.strip() if info_element else "Not found"

            # Use regular expressions to find the first four digits
            digits = re.search(r'\d{4}', info_text)

            # Extract the first four digits if found
            if digits:
                return digits.group()
            else:
                return "No digits found"
        else:
            return None
    except Exception as e:
        return None

# Create a progress bar to show the percentage completion
progress_bar = st.progress(0)

# Process the URLs and populate the unique_data_set
for i, url in enumerate(tqdm(urls, desc="Processing URLs"), start=1):
    movie_name = scrape_movie_name(url)
    info_class_name = "col-xl-5 col-lg-6 col-md-8 col-sm-12"
    digit_text = scrape_first_four_digits_from_class(url, info_class_name)

    unique_data_set.add((url, movie_name, digit_text))  # Store as a tuple for uniqueness

    # Update the progress bar
    progress = i / total_urls
    progress_bar.progress(progress)

# Create a DataFrame from the unique data set
unique_data_list = list(unique_data_set)
df = pd.DataFrame(unique_data_list, columns=['URL', 'Movie Name', 'First Four Digits'])

# Display the DataFrame
st.write("Unique Data extracted from URLs:")
st.write(df)

# Save unique data to Excel (.xlsx) and HTML files
if st.button("Save Unique Data"):
    df.to_excel("unique_movie_data.xlsx", index=False)
    df.to_html("unique_movie_data.html", index=False)
    st.success("Unique data saved to 'unique_movie_data.xlsx' and 'unique_movie_data.html'.")
