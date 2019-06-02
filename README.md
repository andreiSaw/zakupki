[![Build Status](https://travis-ci.com/andreiSaw/zakupki.svg?branch=master)](https://travis-ci.com/andreiSaw/zakupki)
# Fraud detection of government procurement in Russia
## term project 2018 - 2019
---
install lib
``` shell
pip install -e .
```
Test it
```shell
./run_test.sh
```
OR
```shell
cd tests/ && pytest -s -v test_io.py
```
If you want to activate proxy, you need to set up an environment variables
`PROXY_ZAKUPKI_HTTP` and `PROXY_ZAKUPKI_HTTPS` with you `host:port`
# Version 1.1.0