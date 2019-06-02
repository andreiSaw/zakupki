psql -d zakupki -a -f initial_up.sql
psql -d zakupki -a -f zakupki_public_regions.sql
psql -d zakupki -a -f add_constraints.sql

