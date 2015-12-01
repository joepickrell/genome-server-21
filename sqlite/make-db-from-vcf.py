#!/usr/bin/env python3

import sys, os, gzip
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


infile = gzip.open(sys.argv[1])
dbfile = sys.argv[2]


Base = declarative_base()
 
class Variant(Base):
	__tablename__ = 'variants'
	id = Column(Integer, primary_key=True)
	chr = Column(String(100))
	pos = Column(Integer)
	rsid = Column(String(100))
	ref = Column(String(10))
	alt = Column(String(10))
	geno = Column(String(3))
	genolk = Column(String(20))
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
  
 
class Phenotype(Base):
    __tablename__ = 'phenotypes'
    id = Column(Integer, primary_key=True)
    pheno_name = Column(String(250))
    pheno_value = Column(String(250))
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

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///'+dbfile)
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#
# add some phenotypes
#
new_pheno = Phenotype(name="height (cm)", value="175")
session.add(new_pheno)
session.commit()

new_pheno = Phenotype(name="weight (lb)", value="145")
session.add(new_pheno)
session.commit()

#
# read in genotypes
#

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
	print(gt, gtlk)
	newvariant = Variant(chr=chr, pos=pos, rsid=snpid, ref=ref, alt=alt, geno=gt, genolk=gtlk)
	session.add(newvariant)
	line = infile.readline()

session.commit()

infile.close()	
