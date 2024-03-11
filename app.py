
from flask import Flask, render_template, jsonify
import json
import threading
from main2 import main as main2_main

app = Flask(__name__)
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

@app.route('/antarctica')
def antarctica():
    return render_template('antarctica.html')


@app.route('/mushrooms')
def get_mushrooms():
    try:
        with open('static/data.json', 'r') as file:
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

 