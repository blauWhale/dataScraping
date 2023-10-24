import json

# Load JSON data from the "fbref_data.json" file
with open("fbref_data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Define the desired statistics
desired_stats = [
    "Most Goals",
    "Most Assists",
    "Clean Sheets",
    "Goals per 90",
    "Shots per 90",
    "Total Cards",
]

# Create a dictionary to map JSON titles to desired titles
title_mapping = {
    "Non-Penalty Goals": "Most Goals",
    "Assists": "Most Assists",
    "Clean Sheets": "Clean Sheets",
    "Non-Penalty Goals/90": "Goals per 90",
    "Shots Total/90": "Shots per 90",
    "Yellow Cards": "Total Cards",
    "Red Cards": "Total Cards",
}

# Extract and clean the desired stats
cleaned_data = []
for item in data:
    if title_mapping.get(item["Title"], "") in desired_stats:
        cleaned_data.append(item)

# Save the cleaned data into "cleaned_fbref_data.json"
with open("cleaned_fbref_data.json", "w", encoding="utf-8") as output_file:
    json.dump(cleaned_data, output_file, indent=4, ensure_ascii=False)

print("Cleaned data saved to 'cleaned_fbref_data.json'")
