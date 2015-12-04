# genome-server-21

[warning: untested, likely buggy code]

Use the 21 bitcoin computer to sell API calls to your genotypes and phenotypes. Genotypes/phenotypes stored in sqlite database, also can sell bulk access to a VCF file.

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

You should get a JSON list of phenotypes for sale (all are 1 satoshi in this demo), like



# Endpoints

/phenotypes: list of phenotypes for sale, url for each

/variants: list of genotypes for sale, url for each


