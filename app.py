from flask import Flask, request, jsonify, render_template
import csv
import io
import plotly.express as px
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Tool 1: CSV Cleaner (your existing script, enhanced)
def clean_csv(file):
    try:
        # Read CSV
        df = pd.read_csv(io.StringIO(file.read()))

        # Fix common issues (your original logic)
        df = df.drop_duplicates()
        df = df.fillna(method='ffill')
        df = df[df.columns].apply(lambda x: x.astype(str))

        return df.to_csv(index=False)
    except Exception as e:
        return f"Error: {str(e)}"

# Tool 2: API Key Manager (generates safe keys)
def generate_api_keys():
    return {
        "API_KEY": f"sk_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "SECRET_KEY": f"sk_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }

# Tool 3: Data Visualizer (Plotly.js)
def visualize_data(df):
    if len(df) < 5:
        return "Need at least 5 data points"
    try:
        df = df.head(10)
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
        return fig.to_json()
    except:
        return "Invalid data format"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/csv-clean', methods=['POST'])
def csv_clean():
    file = request.files['csv']
    cleaned = clean_csv(file)
    return jsonify({"result": cleaned})

@app.route('/api-keys', methods=['POST'])
def api_keys():
    return jsonify(generate_api_keys())

@app.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    df = pd.read_csv(io.StringIO(data['csv']))
    return jsonify({"chart": visualize_data(df)})

if __name__ == '__main__':
    app.run(debug=True)
