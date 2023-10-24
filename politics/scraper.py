import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Send an HTTP GET request to the URL
url = "https://de.wikipedia.org/wiki/Schweizer_Parlamentswahlen_2023/Resultate_Nationalratswahlen"
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all h2 elements
h2_elements = soup.find_all('h2')

# Initialize an empty list to store the party and votes percentage data
party_and_percentage_data = []

# Flag to check if we found the first table after the specified h2 element
found_first_table = False

# Iterate through the h2 elements
for h2_element in h2_elements:
    if "Kanton Zürich" in h2_element.text:
        found_first_table = True
    if found_first_table:
        table = h2_element.find_next('table', {'class': 'wikitable'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                # Extract the "Party" and "Votes Percentage" columns
                party = cols[0].text.strip()
                percentage = cols[2].text.strip()
                party_and_percentage_data.append([party, percentage])

# Create a DataFrame from the extracted data
column_names = ['Party', 'Votes Percentage']
df = pd.DataFrame(party_and_percentage_data, columns=column_names)

# Remove the first row, which contains column headers
df = df.iloc[1:]

@app.route('/')
def display_table():
    # Render the DataFrame as an HTML table
    table_html = df.to_html(classes='table table-hover', index=False, escape=False)
    
    # Get the party names and percentage data as lists for JavaScript
    party_names = df['Party'].tolist()
    percentage_data = df['Votes Percentage'].tolist()

    return render_template('index.html', table_html=table_html, party_names=party_names, percentage_data=percentage_data)

if __name__ == '__main__':
    app.run(debug=True)
