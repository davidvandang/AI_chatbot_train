from flask import Flask, render_template, url_for, request
from Chatbot import Chatbot

CB = Chatbot("chatbot.db")
app = Flask(__name__)
@app.route('/')

# Find html
def index():
  return render_template('chat.html')

# Getting the user input from html
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    bot_response = CB.get_input_from_frontend(user_input)
    return {'bot_response': bot_response}

if __name__ == "__main__":
    app.run(port=5000)



