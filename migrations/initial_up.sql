create table suppliers
(
  inn    varchar not null
    constraint suppliers_pk
      primary key,
  name   varchar,
  region varchar
);
create unique index suppliers_inn_uindex
  on suppliers (inn);

create table buyers
(
  inn        varchar not null
    constraint buyers_pk primary key,
  "fullName" varchar,
  region     varchar
);
create unique index buyers_inn_uindex
  on buyers (inn);

create table procurements
(
  p_id       varchar                             not null,
  buyer_inn  varchar,
  date       timestamp,
  id_sposob  integer    default 0,
  status     varchar,
  obfuscated obfuscated default 'OK'::obfuscated not null,
  result     status     default 'OK'::status     not null,
  num_lots   integer    default 0                not null
);
create unique index procurements_p_id_uindex
  on procurements (p_id);

create table lots
(
  guid         uuid    not null
    constraint lots_pk primary key,
  p_id         varchar not null,
  "initialSum" varchar,
  subject      varchar,
  category     varchar
);
create unique index lots_guid_uindex
  on lots (guid);

create table bids
(
  guid               uuid    not null,
  bid_date           timestamp,
  price              varchar,
  supplier_inn       varchar,
  "winnerIndication" boolean not null
);

CREATE TABLE words
(
  guid
    uuid not null ,
  word_id
    BIGINT not null ,
  num_words
    int
);

CREATE TABLE freq
(
  id
       BIGINT not null ,
  freq int not null ,
  token
       varchar not null
);
create unique index table_name_column_1_uindex
  on freq (id);