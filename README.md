[![Build Status](https://travis-ci.com/andreiSaw/zakupki.svg?branch=master)](https://travis-ci.com/andreiSaw/zakupki)
# Fraud detection of government procurement in Russia
## term project 2018 - 2019
---
[Published on Tableau Online](https://public.tableau.com/profile/andrei.ysaev#!/vizhome/cars_procurements_rf_2017_2019/total)
***
**HOW TO**

1. install lib with `pip install -e .`
2. Setup env veriable `ZAKUPKI_ACTIVE_DB` with `export ZAKUPKI_ACTIVE_DB='zakupki'`
2. Test it

    <!-- language: shell--> 
        ./run_test.sh
    <!-- --> OR
        cd tests/ && pytest -s -v test_io.py
3. If you want to activate proxy, you need to set up an environment variables
`PROXY_ZAKUPKI_HTTP` and `PROXY_ZAKUPKI_HTTPS` with you `host:port`
# Version 1.1.0