import pandas as pd
import json
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

def list_maker(df, category):
    ''' 
    just for the sherman gallery spreadsheets
    '''
    return list(df[df.CATEGORY == category].SERVICE.unique())

#importing price lists
prices = pd.read_csv('master_list.csv')
services_1 = pd.read_excel('service_prices.xlsx', sheet_name='Sheet1', engine='openpyxl')
services_2 = pd.read_excel('service_prices.xlsx', sheet_name='Sheet2', engine='openpyxl')

#lists to generate dropdown menus
supplier_list = list(prices.supplier.unique())
supplier_list.sort()

service_list = list_maker(services_1, 'SERVICE')
mount_list = list_maker(services_1, 'MOUNT')
back_list = list_maker(services_1, 'BACK')
space_list = list_maker(services_1, 'SPACE')
glass_list = list_maker(services_1, 'GLASS')
paper_mat_list = list_maker(services_2, 'PAPER MATS')
fabric_mat_list = list_maker(services_2, 'FAB MATS / 1-PIECE LINERS')
fabric_liner_list = list_maker(services_2, 'FAB LINERS / SPACERS')
customer_material_list = list_maker(services_2, 'CUSTOMERS MATERIALS')
misc_list = list_maker(services_2, 'MISCELLANEOUS')

#for supplier discounts and extra costs
with open('suppliers.JSON', 'r') as f:
    supplier_dict = json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/frame', methods=['POST', 'GET'])
def frame():

    if request.method == 'POST':

        # Request Data. 
        # Information in forms refreshes after every submit.
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
                                 supplier_list=supplier_list,
                                 selected_supplier=supplier)
    else:
        return render_template('frame.html',
                                supplier_list=supplier_list)



@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':

        return render_template('test.html', 
                                supplier_list=supplier_list,
                                service_list=service_list,
                                mount_list=mount_list,
                                back_list=back_list,
                                space_list=space_list,
                                glass_list=glass_list,
                                paper_mat_list=paper_mat_list,
                                fabric_mat_list=fabric_mat_list,
                                fabric_liner_list=fabric_liner_list,
                                customer_material_list=customer_material_list,
                                misc_list=misc_list)
    else:
        return render_template('test.html', 
                                supplier_list=supplier_list,
                                service_list=service_list,
                                mount_list=mount_list,
                                back_list=back_list,
                                space_list=space_list,
                                glass_list=glass_list,
                                paper_mat_list=paper_mat_list,
                                fabric_mat_list=fabric_mat_list,
                                fabric_liner_list=fabric_liner_list,
                                customer_material_list=customer_material_list,
                                misc_list=misc_list)

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')