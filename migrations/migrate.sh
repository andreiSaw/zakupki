psql -c 'create database zakupki;' -U postgres
gunzip -c zakupki2019*.gz | psql zakupki