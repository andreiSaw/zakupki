psql -c 'create database zakupki;' -U postgres
psql -d zakupki -a -f migrations/initial_up.sql
psql -d zakupki -a -f migrations/zakupki_public_regions.sql
