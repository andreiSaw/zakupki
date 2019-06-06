-- buyers on delete cascade;
alter table buyers
  add constraint buyers_regions_code_fk
    foreign key (region) references regions (code);
-- suppliers
alter table suppliers
  add constraint suppliers_regions_code_fk
    foreign key (region) references regions (code);
-- procurements
alter table procurements
  add constraint procurements_buyers_inn_fk
    foreign key (buyer_inn) references buyers (inn);
-- lots
alter table lots
  add constraint lots_procurements_p_id_fk
    foreign key (p_id) references procurements (p_id);
--bids
alter table bids
  add constraint bids_lots_guid_fk
    foreign key (guid) references lots (guid);
alter table bids
  add constraint bids_suppliers_inn_fk
    foreign key (supplier_inn) references suppliers (inn);
ALTER TABLE bids
  ADD PRIMARY KEY (guid, bid_date, supplier_inn);
-- freq
alter table freq
  add constraint table_name_pk
    primary key (id);
-- words
ALTER TABLE words
  ADD PRIMARY KEY (guid, word_id);
alter table words
  add constraint words_freq_id_fk
    foreign key (word_id) references freq;
alter table words
  add constraint words_lots_guid_fk
    foreign key (guid) references lots;