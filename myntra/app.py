from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-items')
def get_items():
    # Read CSV file
    csv_file = './unique-products.csv'  # Replace with your CSV file name
    items = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)

    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)
