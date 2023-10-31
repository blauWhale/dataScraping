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

# Function to clean the percentage values
def clean_percentage(percentage):
    # Extract numeric part and convert to float or use 0.0 as the default
    numeric_part = ''.join(filter(lambda x: x.isdigit() or x in '.-', percentage))
    return float(numeric_part) if numeric_part else 0.0

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
                if len(cols) >= 3:  # Ensure that the row has at least 3 columns
                    # Extract the "Party" and "Votes Percentage" columns
                    party = cols[0].text.strip()
                    percentage = clean_percentage(cols[2].text.strip())
                    party_and_percentage_data.append([party, percentage])

# Create a DataFrame from the extracted data
column_names = ['Party', 'Votes Percentage']
df = pd.DataFrame(party_and_percentage_data, columns=column_names)

# Remove the first row, which contains column headers
df = df.iloc[1:]

@app.route('/')
def pie_chart():
    # Assuming df contains your data
    data = df.to_dict(orient='list')
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
