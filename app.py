

from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("Car Price Predicton RF.pkl", 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods =    ['POST'])
def predict():
    transmission_Manual = 0
    transmission_Automatic = 0
    fueltype_Diesel = 0
    fueltype_Hybrid = 0
    fuelType_Petrol = 0
    if request.method == 'POST':
        year = int(request.form['year'])
        number_of_years = pd.datetime.now().year - year
        print('years', number_of_years)
        
        mileage = int(request.form['Mileage'])
        print('milage', mileage)

        
        transmission = request.form['Transmission']
        if(transmission == 'Manual'):
            transmission_Manual = 1
            transmission_Automatic = 0

        elif(transmission == 'SemiAuto'):
            transmission_Manual = 0
            transmission_Automatic = 1
        
        else:
            transmission_Manual = 0
            transmission_Automatic = 0

        print('transmission', transmission_Manual)
        print('transmission_semiAuto', transmission_Automatic)
        
        
        fueltype = request.form['Fueltype']
        if(fueltype == 'Petrol'):
            fuelType_Petrol = 1
            fuelType_Diesel = 0
            fuelType_Hybrid = 0

        elif(fueltype == 'Diesel'):
            fuelType_Petrol = 0
            fuelType_Diesel = 1
            fuelType_Hybrid = 0

        elif(fueltype == 'Hybrid'):
            fuelType_Petrol = 0
            fuelType_Diesel = 0
            fuelType_Hybrid = 1

        else:
            fuelType_Petrol = 0
            fuelType_Diesel = 0
            fuelType_Hybrid = 0

        print('fueltype', fuelType_Petrol)
        print('fueltype_Diesel', fuelType_Diesel)
        print('fueltype_Hybrid', fuelType_Hybrid)  

        mpg = float(request.form['mpg'])
        print('mpg', mpg)

        engineSize = float(request.form['EngineSize'])
        engineSize = round(engineSize*0.001, 2)
        print('enginesize', engineSize)

        tax = int(request.form['Tax'])
        print('tax', tax)

        prediction = model.predict([[mileage, tax, mpg, engineSize, number_of_years, transmission_Automatic, transmission_Manual, fuelType_Diesel, fuelType_Hybrid, fuelType_Petrol]])
        output = round(prediction[0],2)
        
        if output<0:
            return render_template('index.html',prediction_text = "Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text = "You Can Sell The Car at {} Rs".format(output))
            print('sell car at {}'.format(output))
    else:
        return render_template('index.html')
    

if __name__=="__main__":
    app.run(debug=True) 
