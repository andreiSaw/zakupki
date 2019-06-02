alter table buyers
  add constraint buyers_regions_code_fk
    foreign key (region) references regions (code);
alter table suppliers
  add constraint suppliers_regions_code_fk
    foreign key (region) references regions (code);