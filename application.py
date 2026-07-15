import numpy as np
import pandas as pd  # Added to structure the input features
from flask import Flask, request, jsonify, render_template
import pickle

application = Flask(__name__) #Initialize the flask App
model = pickle.load(open('model.pkl', 'rb'))

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # 1. Grab inputs from the HTML form
    int_features = [int(x) for x in request.form.values()]
    
    # 2. Define exact feature names used during training
    feature_names = ["experience", "test_score", "interview_score"]
    
    # 3. Convert features into a 2D array and then into a DataFrame
    final_features = pd.DataFrame([int_features], columns=feature_names)
    
    # 4. Predict safely without scikit-learn warnings
    prediction = model.predict(final_features)
    output = round(float(prediction[0]), 2)
    
    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))

if __name__ == "__main__":
    application.run(debug=True)