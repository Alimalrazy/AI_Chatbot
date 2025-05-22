from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)

# Define your 404 error handler to redirect to the index page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            import dotenv
            dotenv.load_dotenv()  # Load environment variables from .env file if present

            api_key = os.getenv('GEMINI_API_KEY')  # Read API key from environment variable

            # Debug print for API key (masked)
            print(f"Loaded API key: {api_key[:4]}{'*' * (len(api_key) - 8)}{api_key[-4:]}")

            # Gemini API endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

            # Debug print for request URL
            print(f"Request URL: {url}")

            # Request headers
            headers = {
                'Content-Type': 'application/json',
            }

            # Request body
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }

            # Make the API call
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                # Parse the response
                response_json = response.json()
                if 'candidates' in response_json and len(response_json['candidates']) > 0:
                    return response_json['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "Sorry, I couldn't get a valid response from Gemini."
            else:
                return f"API Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('index.html', **locals())
#AIzaSyC35mil4vDAAmBkEVFVGyY8XEA5qGP3HSs
if __name__ == '__main__':
    app.run(debug=True)