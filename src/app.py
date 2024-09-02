import os
from openai import AzureOpenAI
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api_key = os.getenv('HUGGUNG_FACE_API_KEY')


@app.route("/api/generateMail", methods=['POST'])
@cross_origin()
def generateMail():
    if request.method == 'POST':
        try:
            inputMsg = request.json['text']
            client = OpenAI()
            prompt = f"""Turn the following mail {inputMsg} into a professional academic email 
            to a professor and also provide suggestions separately as a feedback 
            on the original email along with subject line so that students 
            can learn from it. Also follow those suggestions in your email. Provide a valid JSON output."""
            schema = {
                "type": "object",
                "properties": {
                        "mail": {
                        "type": "string",
                        "description": "corrected email with proper formatting."
                        },
                        "suggestions": {
                        "type": "string",
                        "description": "feedback given to the orignal mail."
                        },
                        "subject": {
                        "type": "string",
                        "description": "subject of the mail."
                        },
                    }
                }
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    { "role": "system", "content": """You are a helpful email assistant for students 
                     and provides necessary sugesstions and subject line for the students emails.""" },
                    { "role": "user", "content": prompt }],
                functions= [{"name": "email_assistant", "parameters": schema }],
                function_call= {"name": "email_assistant"}
            )
            generated_text = completion.choices[0].message.function_call.arguments
            generated_text =  json.loads(generated_text)
            return jsonify(generated_text), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)