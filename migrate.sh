psql -d zakupki -a -f migrations/initial_up.sql
psql -d zakupki -a -f migrations/zakupki_public_regions.sql
