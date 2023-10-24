import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import json


# Replace the URL with the actual URL of the page you want to scrape
url = "https://fbref.com/en/comps/57/Swiss-Super-League-Stats"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the commented-out div with the specified ID
    goal_table = None
    for element in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if "id=\"leaders_goals\"" in element:
            goal_table = BeautifulSoup(element, "html.parser")
            break

    # Save the HTML content to a file
    with open("fbref_page.html", "w", encoding="utf-8") as file:
        file.write(str(goal_table))

    print("HTML saved to 'fbref_page.html'")

    # Now you can parse and extract the table data with titles
    if goal_table:
        tables = goal_table.find_all("table", {"class": "columns"})
        data = []
        titles = [caption.text.strip() for caption in goal_table.find_all("caption", {"class": "poptip"})]

        for i, table in enumerate(tables):
            table_data = []

            for row in table.find_all("tr"):
                row_data = [cell.text.strip() for cell in row.find_all("td")]
                table_data.append(row_data)

            # Exclude tables with empty titles
            if titles[i]:
                data.append({"Title": titles[i], "Data": table_data})

        # Save the data to a JSON file
        with open("fbref_data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print("Data saved to 'fbref_data.json'")

else:
    print("Failed to retrieve the webpage")
