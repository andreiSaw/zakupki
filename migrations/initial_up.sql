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
  p_id      varchar not null
    constraint procurements_pk
      primary key,
  buyer_inn varchar not null,
  date      timestamp,
  lots_num  integer,
  p_link    varchar not null
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
  category     varchar,
  num_bids     integer
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