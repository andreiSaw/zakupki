Database 
***
It uses *postgresql* database

``` shell
# create database and schemas
./up.sh

# dumps db
pg_dump zakupki | gzip > zakupki.gz

# dumps table from db
pg_dump zakupki --table regions | gzip > regions.gz

# loads database from dump
./migrate.sh

# drops database
./down.sh
```

`zakupki_regions` was originally sourced from [here](https://www.datafix.io/data-source/2118/lists-of-rural-localities-in-russia-wikipedia/)

ER model
![zakupki](https://github.com/andreiSaw/zakupki/raw/master/migrations/er_model.png "er model")
