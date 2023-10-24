from flask import Flask, render_template
import json

app = Flask(__name__)

# Load your data from the JSON file
with open('price_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

@app.route('/')
def display_data():
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
