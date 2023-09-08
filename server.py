from flask import Flask, request, jsonify
from flask_cors import CORS 
from chatbot import ask_chatbot
app = Flask(__name__)
CORS(app) 

@app.route('/chatbot', methods=['POST'])
def get_hello():
    try:
        data = request.get_json()
        user_query = data.get("ask")
        response = ask_chatbot(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/health')
def health_check():
    return 'Healthy', 200

if __name__ == '__main__':
    app.run(host='localhost', port=8080)