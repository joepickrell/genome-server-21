# genome-server-21

[in progress]

Use the 21 bitcoin computer to sell API calls to your genotypes and phenotypes. Genotypes/phenotypes stored in sqlite database, also can sell bulk access to a VCF file.

Setup:

1. configure

>git clone https://github.com/joepickrell/genome-server-21.git

>sudo pip3 install Flask-SQLAlchemy sqlite3

2. make the database of genotypes/phenotypes, serve

>python3 genome-server.py vcffile/testvcf.vcf.gz

