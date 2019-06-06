psql -c 'create database zakupki;' -U postgres
psql -d zakupki -a -f initial_up.sql
gunzip -c regions.gz | psql zakupki
psql -d zakupki -a -f add_constraints.sql