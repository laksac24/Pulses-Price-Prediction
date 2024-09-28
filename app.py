import pickle
from flask import Flask, render_template, request
import pandas as pd

app=Flask(__name__)
model=pickle.load(open("Pulses_prices.pkl","rb"))
data=pd.read_csv('pulses_price_prediction_10000.csv')

@app.route("/")
def index():
    crops = sorted(data['Pulse Type'].unique())
    return render_template("index2.html", crops=crops)

@app.route("/predict", methods=['GET','POST'])
def predict():
    croops = ['Chickpeas','Green Peas','Pigeon Peas','Lentils','Kidney Beans','Black Beans']
    temperature = float(request.form.get('temp'))
    rain = float(request.form.get('rain'))
    supply = int(request.form.get('supply'))
    demand = int(request.form.get('demand'))
    CROP = request.form.get('CROP')
    crops = sorted(data['Pulse Type'].unique())

    prediction=model.predict([[croops.index(CROP) + 1,temperature,rain,supply,demand]])
    output=round(prediction[0],2)
    return render_template("index2.html", prediction_text=f'Pulse Price: Rs {output}', crops=crops)

if __name__=="__main__":
    app.run(debug=True)