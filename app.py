import pandas as pd
import json
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)
prices = pd.read_csv('master_list.csv')

with open('suppliers.JSON', 'r') as f:
    supplier_dict = json.load(f)

supplier_list = list(supplier_dict.keys())

@app.route('/')
def home():
    return '''
    <h1> Sherman Gallery Tools </h1>
    <li> <a href = "/frame"> Frame Price</a> </li>
    <li> <a href = "/quote"> Full Quote </a> </li>
    '''

# http://0.0.0.0:5000/frame
# @app.route('/frame', methods=['POST'])
@app.route('/frame', methods=['POST', 'GET'])
def frame():
    # Rule of minimum frame size = 40

    if request.method == 'POST':
    
        supplier = str(request.form['supplier'])
        weight = supplier_dict[supplier]['weight']
        constant = supplier_dict[supplier]['constant']

        inches = float(request.form['inches'])
        frame = str(request.form['frame']).upper()

        try:
            length_price = float(prices[(prices['supplier'] == supplier) & (prices['frame'] == frame)]['price'])
            length_price_adj = (length_price * weight) + constant

            frame_quote = round(length_price_adj * inches, 2)
            frame_quote = "Frame Price = $" + str(frame_quote)
        except:
            frame_quote = " Didn't recognise frame code"

        return render_template('frame.html',
                                 frame_price='{}'.format(frame_quote),
                                 supplier_list=supplier_list)
    else:
        return render_template('frame.html',
                                supplier_list=supplier_list)


@app.route('/quote')
def quote():
    return '''
    <h1> Working On It </h1>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')