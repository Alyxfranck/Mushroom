
from flask import Flask, render_template, jsonify
import json
import threading
from main2 import main as main2_main

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('ch.html')

 
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

 