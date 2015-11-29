#!/usr/bin/env python3
import os
import json
import random

from flask import Flask
from flask import request
from flask import send_from_directory

# import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

# path to the VCF file to sell
vcf_path = '/home/twenty-server/genome-server/vcffile'


# simple content model: dictionary of files w/ prices
files = {}

# get a list of the files in the directory
file_list = os.listdir(vcf_path)

for file_id in range(len(file_list)):
	files[file_id] = file_list[file_id], 1000

# endpoint to look up VCF files to buy
@app.route('/vcf')
def file_lookup():
    return json.dumps(files)

# return the price of the selected file
def get_price_from_request(request):
    id = int(request.args.get('selection'))
    return files[id][1]

# machine-payable endpoint that returns selected file if payment made
@app.route('/buyvcf')
@payment.required(get_price_from_request)
def buy_file():

    # extract selection from client request
    sel = int(request.args.get('selection'))

    # check if selection is valid
    # note you still pay for this
    if(sel < 0 or sel >= len(file_list)):
        return 'Invalid selection.'
    else:
        return send_from_directory(vcf_path,file_list[int(sel)])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
