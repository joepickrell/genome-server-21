# genome-server-21

Testing how to use the 21 bitcoin computer to sell API calls to your genotypes and phenotypes. Genotypes/phenotypes stored in sqlite database, also can sell bulk access to a VCF file.

Setup
-----

1. configure

	$ git clone https://github.com/joepickrell/genome-server-21.git

	$ cd genome-server-21 

	$ sudo pip3 install Flask-SQLAlchemy sqlite3

2. make the database of genotypes/phenotypes, serve

	$ python3 genome-server.py vcffile/testvcf.vcf.gz

3. Is it working?

	$ curl -i http://localhost:5000/phenotypes

You should get a JSON list of phenotypes, like



# Endpoints

GET /phenotypes : list of phenotypes, uri for each

GET /variants : list of genotypes, uri for each

GET /vcf : list of VCF files

GET /buyvariant/<chromosome>/<int:position> : genotype at chromosome and position [1 satoshi]

GET /buyphenotype/<int:phenoid> : phenotype with id phenoid [1 satoshi]

