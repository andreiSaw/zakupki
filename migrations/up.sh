#!/bin/bash
createdb $ZAKUPKI_ACTIVE_DB
psql -d $ZAKUPKI_ACTIVE_DB -a -f add_enums.sql
psql -d $ZAKUPKI_ACTIVE_DB -a -f create_suppliers.sql
psql -d $ZAKUPKI_ACTIVE_DB -a -f initial_up.sql
gunzip -c regions.gz | psql $ZAKUPKI_ACTIVE_DB
gunzip -c cats.gz | psql $ZAKUPKI_ACTIVE_DB
gunzip -c sposobs.gz | psql $ZAKUPKI_ACTIVE_DB
#psql -d $ZAKUPKI_ACTIVE_DB -a -f add_constraints.sql