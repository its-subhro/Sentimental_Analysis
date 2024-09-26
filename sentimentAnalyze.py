from flask import Flask, request, jsonify
import pandas as pd
import re
from flask_cors import CORS
from groq import Groq
import traceback  # For detailed exception handling

app = Flask(__name__)
CORS(app)

# Initialize Groq API client
client = Groq(api_key="GRQ_API_KEY")

# Route to serve the HTML form
@app.route('/')
def upload_form():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload File for Sentiment Analysis</title>
    </head>
    <body>
        <h1>Upload XLSX or CSV File</h1>
        <form action="/analyze" method="POST" enctype="multipart/form-data">
            <label for="file">Choose XLSX/CSV file:</label>
            <input type="file" id="file" name="file" accept=".xlsx, .csv" required><br><br>
            <input type="submit" value="Upload and Analyze">
        </form>
    </body>
    </html>
    '''

# Function to read and extract reviews from the input file
def extract_reviews(file):
    try:
        if file.filename.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            data = pd.read_excel(file)
        else:
            raise ValueError("Invalid file format. Only CSV and XLSX files are supported.")
        
        # Assuming the reviews are in a column named 'Review'
        if 'Review' not in data.columns:
            raise ValueError("The file must contain a 'Review' column.")

        return data['Review'].tolist()
    
    except Exception as e:
        print(f"Error reading file: {e}")
        raise e

# Function to perform sentiment analysis via Groq API
def analyze_sentiment_groq(review):
    data = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": "Not worth the price at all.🙁"
            },
            {
                "role": "assistant",
                "content": "Negative"
            },
            {
                "role": "user",
                "content": "Better than expected!"
            },
            {
                "role": "assistant",
                "content": "Neutral"
            },
            {
                "role": "user",
                "content": "Would definitely recommend to others."
            },
            {
                "role": "assistant",
                "content": "Positive"
            },
            {
                "role": "user",
                "content": "Does the job, no complaints."
            },
            {
                "role": "assistant",
                "content": "Neutral"
            },
            {
                "role": "user",
                "content": "Very underwhelming experience."
            },
            {
                "role": "assistant",
                "content": "Negative"
            },
            {
                "role": "user",
                "content": "Great value for money!😃"
            },
            {
                "role": "assistant",
                "content": "Positive"
            },
            {
                "role": "user",
                "content": "Arrived damaged, very disappointed."
            },
            {
                "role": "assistant",
                "content": "Negative"
            },
            {
                "role": "user",
                "content": "Arrived damaged, very disappointed."
            },
            {
                "role": "assistant",
                "content": "Negative"
            },
            {
                "role": "user",
                "content": f"""{review}"""
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    sentiment_result = ""  # Initialize an empty string to hold the result
    for chunk in data:
        content = chunk.choices[0].delta.content or ""  # Extract the content
        sentiment_result += re.sub(r"\s+", "", content)  # Concatenate and clean the content
    
    return sentiment_result

# API endpoint to handle file upload and sentiment analysis
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Extract reviews from the file
        reviews = extract_reviews(file)
        
        # Initialize sentiment counters
        positive, negative, neutral = 0, 0, 0
        
        # Loop through each review and perform sentiment analysis using Groq
        for review in reviews:
            sentiment = analyze_sentiment_groq(review)
            print(f"Sentiment result for review '{review}': {sentiment}")
            if "Positive" in sentiment:
                positive += 1
            elif "Negative" in sentiment:
                negative += 1
            elif "Neutral" in sentiment:
                neutral += 1
        
        # Return the structured response
        return jsonify({
            "positive": positive,
            "negative": negative,
            "neutral": neutral
        })
    
    except ValueError as ve:
        print(f"Value error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()  # For detailed stack trace in the logs
        return jsonify({"error": "An error occurred while processing the file or API request"}), 500

# Basic error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
