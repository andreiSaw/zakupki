alter table buyers
  add constraint buyers_regions_code_fk
    foreign key (region) references regions (code);
alter table suppliers
  add constraint suppliers_regions_code_fk
    foreign key (region) references regions (code);
alter table procurements
  add constraint procurements_buyers_inn_fk
    foreign key (buyer_inn) references buyers (inn);
alter table lots
  add constraint lots_procurements_p_id_fk
    foreign key (p_id) references procurements (p_id);
alter table bids
  add constraint bids_lots_guid_fk
    foreign key (guid) references lots (guid);
alter table bids
  add constraint bids_suppliers_inn_fk
    foreign key (supplier_inn) references suppliers (inn);
alter table freq
  add constraint table_name_pk
    primary key (id);
ALTER TABLE words
  ADD PRIMARY KEY (guid, word_id);
ALTER TABLE bids
  ADD PRIMARY KEY (guid, bid_date, supplier_inn);