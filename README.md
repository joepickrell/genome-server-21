# genome-server-21

Testing how to use the 21 bitcoin computer to sell API calls to your genotypes and phenotypes. Genotypes/phenotypes stored in sqlite database, also can sell bulk access to a VCF file.

Setup
-----

1. configure

```
	$ git clone https://github.com/joepickrell/genome-server-21.git

	$ cd genome-server-21 

	$ sudo pip3 install Flask-SQLAlchemy sqlite3

```
2. make the database of genotypes/phenotypes, serve
```
	$ python3 genome-server.py vcffile/testvcf2.vcf.gz
```
3. Is it working?
```
	$ curl -i http://localhost:5000/phenotypes
```
You should get a JSON list of phenotypes, like

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 224
Server: Werkzeug/0.11.2 Python/3.4.2
Date: Fri, 04 Dec 2015 03:30:13 GMT

{
  "pheno_list": [
    {
      "pheno_name": "height (cm)",
      "uri": "http://localhost:5000/buyphenotype/1"
    },
    {
      "pheno_name": "weight (lb)",
      "uri": "http://localhost:5000/buyphenotype/2"
    }
  ]
}
```
If you try to see the actual value of the phenotype, however:

```
	$ curl -i http://localhost:5000/buyphenotype/1
```

this will fail with error 402: payment required (1 satoshi). Using the 21 libraries, this can be successfully requested with the following python code:

```
# Import methods from the 21 Bitcoin Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# Configure your Bitcoin wallet.
username = Config().username
wallet = Wallet()
requests = BitTransferRequests(wallet, username)

test = requests.get(url="http://localhost:5000/buyphenotype/1")
print(test.content)
```

# Endpoints

GET /phenotypes : list of phenotypes, uri for each

GET /variants : list of genotypes, uri for each

GET /vcf : list of VCF files

GET [cost: 1 satoshi] /buyvariant/[chr]/[pos] : returns the VCF genotype and genotype likelihoods at chromosome chr and position pos

GET [cost: 1 satoshi] /buypheno/[phenoid] : returns the phenotype value for phenotype phenoid


