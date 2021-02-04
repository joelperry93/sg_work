import pandas as pd
import requests
import json
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

prices = pd.read_csv('master_list.csv')
supplier_list = list(prices.supplier.unique())


@app.route('/frame')
def home():
    return render_template('home.html')

# http://0.0.0.0:5000/frame
@app.route('/frame', methods=['POST'])
def frame():
    # Rule of minimum frame size = 40
    inches = float(request.form['inches'])
    inches = max(inches, 40)

    supplier = str(request.form['supplier'])
    frame = str(request.form['frame']).upper()

    try:
        length_price = float(prices[(prices['supplier'] == supplier) & (prices['frame'] == frame)]['price'])
        frame_quote = length_price * float(inches)
    except:
        frame_quote = " Didn't recognise frame code"

    return render_template('home.html', 
                        frame_price='Frame Price = ${}'.format(frame_quote),
                        supplier_list=supplier_list
                            
                            )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')