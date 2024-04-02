# server side code for the web application
from flask import Flask, render_template, jsonify, send_from_directory, request
import requests
import json
import threading
import os
import re
from main2 import main as main2_main

app = Flask(__name__)
@app.route('/update-js', methods=['POST'])
def update_js_file():
    content = request.json
    file_name = content['file_name']
    n_value = content['n']

    file_path = os.path.join('static', file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            file_data = file.read()

        # Regex pattern to find 'let n ='
        pattern = re.compile(r'(let n = )(.+?);')
        matches = pattern.findall(file_data)
        if matches:
            new_file_data, count = re.subn(pattern, r'\g<1>' + json.dumps(n_value) + ';', file_data)
            if count > 0:
                with open(file_path, 'w') as file:
                    file.write(new_file_data)
                return jsonify({'status': 'success'}), 200
            else:
                # No need to update if the current value is the same as the new value
                return jsonify({'status': 'success', 'message': 'Parameter n already set to the requested value'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Parameter n not found'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'File not found'}), 404

@app.route('/')
def home():
    return render_template('home.html')
 
@app.route('/master') 
def working():
    return render_template('Master.html')

@app.route('/ch')
def ch():
    return render_template('ch.html')

@app.route('/tokyo')
def tokyo():
    return render_template('tokyo.html')

@app.route('/north_america')
def north_america():
    return render_template('north_america.html')

@app.route('/south_america')
def south_america():
    return render_template('south_america.html')

@app.route('/africa')
def africa():
    return render_template('africa.html')

@app.route('/australia')
def australia():
    return render_template('australia.html')

@app.route( '/antarctica')
def antarctica():
    return render_template('antarctica.html')


@app.route('/mushrooms')
def get_mushrooms():
    try:
        with open('data/data.json', 'r') as file:
            mushrooms = json.load(file)
        return jsonify(mushrooms)
    except Exception as e:
        return jsonify({"error": str(e)}), 550

def run_main2():
    main2_main()  # Call the main function from main2.py

if __name__ == '__main__':
    # Start main2.py in a separate thread
    thread = threading.Thread(target=run_main2)
    thread.daemon = True  
    thread.start()

# Start the Flask app
app.run(debug=True)