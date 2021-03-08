select * from program

insert into instore (ID, IS_TYPE, IN_DATE, PROGRAM_CODE, order_number,IS_STATUS, IS_NUM, IN_STORE_NUM, CHECK_NAME, CHECK_TIME, CREATE_NAME, STORE_NAME, LOCATION, CHECK_FORM_PATH)
values (35, 0, '20210303', '12345', 'order1',0, 100, 0, null, null, 'admin', 'tets', 'test', 'test');

insert into PROGRAM (ID, PRO_NAME, PRO_ID, TASK_ID, TASK_PATH, PROGRAM_CODE, order_number,PROGRAM_CODE_PATH, TASK_NAME_BOOK, ORDER_TIME, REMARKS, TEST_ITEM, CONTRACT_ID, SAMPLE_NAME, SAMPLE_MATERIAL, SAMPLE_NUM)
values (1, 'test', 24, '1234', '12345', '1234','order1', '12345', null, '20200910', null, null, null, null, null, null);

insert into PROGRAM (ID, PRO_NAME, PRO_ID, TASK_ID, TASK_PATH, PROGRAM_CODE, order_number,PROGRAM_CODE_PATH, TASK_NAME_BOOK, ORDER_TIME, REMARKS, TEST_ITEM, CONTRACT_ID, SAMPLE_NAME, SAMPLE_MATERIAL, SAMPLE_NUM)
values (2, 'admintestkerry', 30, '12345', 'test', 'test','order2' ,'test', 'test', '20100910', null, null, null, null, null, null);
