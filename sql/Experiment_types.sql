prompt Importing table experiments...
set feedback off
set define off
insert into experiments (EXPERIMENT_ID, EXPERIMENT_NAME, EXPERI_STEP, EXPERI_TYPE)
values (2, '测量工序', 0, 'CAI');

insert into experiments (EXPERIMENT_ID, EXPERIMENT_NAME, EXPERI_STEP, EXPERI_TYPE)
values (3, '无损工序', 1, 'CAI');

insert into experiments (EXPERIMENT_ID, EXPERIMENT_NAME, EXPERI_STEP, EXPERI_TYPE)
values (4, '冲击工序', 2, 'CAI');

insert into experiments (EXPERIMENT_ID, EXPERIMENT_NAME, EXPERI_STEP, EXPERI_TYPE)
values (5, '无损工序', 3, 'CAI');

insert into experiments (EXPERIMENT_ID, EXPERIMENT_NAME, EXPERI_STEP, EXPERI_TYPE)
values (6, '应变剂黏贴工序', 4, 'CAI');

insert into experiments (EXPERIMENT_ID, EXPERIMENT_NAME, EXPERI_STEP, EXPERI_TYPE)
values (7, '压缩工序', 5, 'CAI');

prompt Done.
