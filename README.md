# Sentiment Analysis API

This project provides a simple web application for uploading XLSX or CSV files containing customer reviews and performing sentiment analysis using the Groq API. The application will analyze each review and categorize it as positive, negative, or neutral.

## Features

- **File Upload:** Users can upload XLSX or CSV files containing customer reviews.
- **Sentiment Analysis:** The application uses the Groq API to analyze the sentiment of each review.
- **Results Display:** The results are displayed as counts of positive, negative, and neutral sentiments.

## Technologies Used

- **Flask:** A lightweight WSGI web application framework for Python.
- **Pandas:** A data manipulation and analysis library for Python.
- **Groq:** An AI-powered API for natural language processing.
- **Flask-CORS:** A Flask extension for handling Cross-Origin Resource Sharing (CORS).

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your Groq API key in the code where `client = Groq(api_key="GRQ_API_KEY")` is defined.

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Upload an XLSX or CSV file that contains a column named "Review".

4. After the file is processed, you will receive a JSON response with the counts of positive, negative, and neutral sentiments.

## Error Handling

The application includes basic error handling for:

- Missing files in the request
- Invalid file formats
- Absence of the "Review" column in the uploaded file
- General exceptions during file processing or API requests