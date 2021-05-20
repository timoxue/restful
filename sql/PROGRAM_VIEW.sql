CREATE OR REPLACE VIEW sfincident.PROGRAM_INSTORE_VIEW
AS
SELECT  a.pro_name, a.pro_id , a.task_id , a.order_number,a.ORDER_ID,
a.task_form_id , a.program_code,
 a.program_id , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num, sum(case when c.is_status = 0 then c.is_num else 0 end) AS w_sum, 
b.res_name, b.create_name 
, b.finish_time , b.create_time , b.pro_name as project_name,
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address,b.id as project_id,
sum(c.in_store_num) as in_store_num 
FROM sfincident.program a RIGHT JOIN sfincident.project b ON b.id = a.pro_id JOIN sfincident.instore c ON c.order_number = a.order_number

GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.ORDER_ID,
a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number,b.res_name, b.create_name 
, b.finish_time , b.create_time , 
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address,b.id,b.pro_name;

CREATE OR REPLACE VIEW sfincident.PROGRAM_COMPONENT_VIEW
AS
SELECT  a.pro_name, a.pro_id , a.task_id , a.order_number,a.ORDER_ID,
a.task_form_id , a.program_code,
 a.program_id , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num,
sum(case when d.component_status1  = 1  then 1 else 0 end) in_experiment,
sum(case when d.component_status1  = 2  then 1 else 0 end) is_finish 
from sfincident.program a  
JOIN sfincident.components d ON d.order_number = a.order_number 
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.ORDER_ID,
a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number;

CREATE OR REPLACE VIEW sfincident.PROGRAM_VIEW
AS 
SELECT a.pro_name,
       a.pro_id,
       a.ORDER_ID,
       a.task_id,
         a.order_number,
         a.task_form_id,
         a.program_code,
         a.program_id,
         a.task_name_book,
         a.order_time,
         a.remarks,
         a.test_item,
         a.contract_id,
         a.sample_name,
         a.sample_material,
         a.sample_num,
         a.w_sum,
         a.res_name,
         a.create_name,
         a.finish_time,
         a.create_time,
         a.company,
         a.category,
         a.postcode,
         a.contact,
         a.tele_phone,
         a.u_email,
         a.address,
         a.project_id,
         a.project_name,
         a.in_store_num,b.in_experiment,b.is_finish from sfincident.PROGRAM_INSTORE_VIEW a
         JOIN sfincident.PROGRAM_COMPONENT_VIEW b ON b.order_number = a.order_number;

CREATE OR REPLACE VIEW 
sfincident.PROGRAM_COMPONENT_VIEW AS SELECT  
a.pro_name, a.pro_id , a.task_id , a.order_number,a.ORDER_ID, 
a.task_form_id , a.program_code,  a.program_id , a.task_name_book,
a.order_time , a.remarks  , a.test_item , a.contract_id , a.sample_name , a.sample_material ,  
a.sample_num, sum(case when d.component_status1  = 1  then 1 else 0 end) in_experiment, 
sum(case when d.component_status1  = 2  then 1 else 0 end) is_finish from sfincident.program a  
JOIN sfincident.components d ON d.order_number = a.order_number 
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.ORDER_ID, a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name,  a.sample_material, a.sample_num, a.order_number;

CREATE OR REPLACE VIEW sfincident.PROGRAM_PROCESS AS
SELECT  a.pro_name, a.pro_id , a.order_number, 
c.incident_id, count(*) as sumprocess,count( if( c.process_status = 4 ,1,null)  = 0) as completed,count( if( c.process_status = 0 ,1,null)  = 0) as inprocess
from sfincident.program a right join sfincident.incidents b ON b.order_number = a.order_number
left JOIN sfincident.processes c ON c.incident_id = b.incident_id group by pro_id,pro_name,order_number,incident_id;