from flask import Flask, request, jsonify
import qapipeline  # Assuming you have a function in this script to get a response
import os
from dotenv import load_dotenv

load_dotenv("../.env")
openai_key = os.getenv("OPENAI_API_KEY")

links = ["https://www.gracedupage.org/about-us",
            'https://www.gracedupage.org/who-is-jesus',
            'https://www.gracedupage.org/purpose',
            'https://www.gracedupage.org/history',
            'https://www.gracedupage.org/pastoral-ministries',
            'https://www.gracedupage.org/leadership',
            'https://www.gracedupage.org/baptism-and-membership'
            ]

app = Flask(__name__)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['user_input']
    response = your_llm_script.get_response(user_input)  # Replace with your function
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(port=5000)
