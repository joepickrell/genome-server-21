#!/usr/bin/env python3
import os, sys, gzip
import json
import random

from flask import Flask, render_template, jsonify, abort, make_response
from flask import request, url_for
from flask import send_from_directory

#going to use Flask-SQLAlchemy to interact with the database
from flask_sqlalchemy import SQLAlchemy

# import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)

#going to serve all variants in a VCF file given at command line
infile = gzip.open(sys.argv[1])


#DB -- set to test.db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Models
class Variant(db.Model):
        __tablename__ = "variants"
        id = db.Column(db.Integer, primary_key=True)
        chr = db.Column(db.String(100))
        pos = db.Column(db.Integer)
        rsid = db.Column(db.String(100))
        ref = db.Column(db.String(10))
        alt = db.Column(db.String(10))
        geno = db.Column(db.String(3))
        genolk = db.Column(db.String(20))
        def __init__(self, chr, pos, rsid, ref, alt, geno, genolk):
                self.chr = chr
                self.pos = pos
                self.rsid = rsid
                self.ref = ref
                self.alt = alt
                self.geno = geno
                self.genolk = genolk
        @property
        def serialize(self):
                return{
                        'id':  self.id,
                        'chr': self.chr,
                        'pos': self.pos,
                        'rsid': self.rsid,
                        'ref': self.ref,
                        'alt': self.alt,
                        'geno': self.geno,
                        'genolk': self.genolk
                }
        @property
        def serialize_nogt(self):
                return{
                        'id':  self.id,
                        'chr': self.chr,
                        'pos': self.pos,
                        'rsid': self.rsid,
                        'ref': self.ref,
                        'alt': self.alt
                }


class Phenotype(db.Model):
    __tablename__ = "phenos"
    id = db.Column(db.Integer, primary_key=True)
    pheno_name = db.Column(db.String(250))
    pheno_value = db.Column(db.String(250))
    def __init__(self, name, value):
        self.pheno_name = name
        self.pheno_value = value
    @property
    def serialize(self):
        return{
                'id':  self.id,
                'pheno_name': self.pheno_name,
                'pheno_value': self.pheno_value
        }


db.create_all()

# add some phenotypes
new_pheno = Phenotype(name="height (cm)", value="175")
db.session.add(new_pheno)
db.session.commit()

new_pheno = Phenotype(name="weight (lb)", value="145")
db.session.add(new_pheno)
db.session.commit()

# add some genotypes

line = infile.readline()
while line:
        line = bytes.decode(line)
        line = line.strip().split()
        if line[0][0] == "#":
                line = infile.readline()
                continue
        chr = line[0]
        pos = line[1]
        snpid = line[2]
        ref = line[3]
        alt = line[4]
        fields = line[8].split(":")
        gtfields = line[9].split(":")
        gt = "9/9"
        gtlk = "NA,NA,NA"
        for i in range(len(fields)):
                f = fields[i]
                if f == "GT":
                        gt = gtfields[i]
                elif f == "GL":
                        gtlk = gtfields[i]
        print(chr, pos, gt)
        newvariant = Variant(chr=chr, pos=pos, rsid=snpid, ref=ref, alt=alt, geno=gt, genolk=gtlk)
        db.session.add(newvariant)
        line = infile.readline()

db.session.commit()

#Wallet
wallet = Wallet()
payment = Payment(app, wallet)

# path to the bulk VCF files to sell
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

@app.route('/variants', methods=['GET'])
def get_variants():
	snpquery = db.session.query(Variant)
	return jsonify(snp_list = [i.serialize_nogt for i in snpquery.all()])

@app.route('/phenotypes', methods=['GET'])
def get_phenos():
	snpquery = db.session.query(Phenotype)
	return jsonify(snp_list = [i.serialize for i in snpquery.all()])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
