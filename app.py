import os
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__, template_folder = 'templates')
app.config["DEBUG"] = True

contacts = [
        {
            'id': 0,
            'first_name': 'Greg',
            'last_name': 'Meow',
            'email' : 'gmeow@hotmail.com',
            'phone' : 4051231234,
            'created' : '1/14/2020'},
        {
            'id': 1,
            'first_name': 'Tony',
            'last_name': 'Hawk',
            'email' : 'hawky12@hotmail.com',
            'phone' : 9543494939,
            'created' : '2/09/2020'}
        ]

@app.route('/')
def home():
        return render_template('home.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/api/contacts/all', methods=['GET'])
def api_all():
    print(jsonify(contacts))
    return jsonify(contacts)


if __name__ == '__main__':
    app.run()
