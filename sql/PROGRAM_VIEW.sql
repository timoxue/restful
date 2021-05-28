CREATE OR REPLACE VIEW sfincident.PROGRAM_INSTORE_VIEW
AS
SELECT  a.pro_name, a.pro_id , a.task_id , a.order_number,a.order_id,
a.task_form_id , a.program_code,
 a.program_id , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num, sum(case when c.is_status = 0 then c.is_num else 0 end) AS w_sum, 
b.res_name, b.create_name 
, b.finish_time , b.create_time , b.pro_name as project_name,
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address,b.id as project_id,

SUM(CASE WHEN c.is_type = 0 THEN c.in_store_num ELSE 0 END )  as in_store_num

FROM sfincident.project b LEFT JOIN sfincident.program a ON b.id = a.pro_id LEFT JOIN sfincident.instore c ON c.order_number = a.order_number
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.order_id,
a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number,b.res_name, b.create_name 
, b.finish_time , b.create_time , 
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address,b.id,b.pro_name;

CREATE OR REPLACE VIEW sfincident.PROGRAM_COMPONENT_VIEW
AS
SELECT  a.pro_name, a.pro_id , a.task_id , a.order_number,a.order_id,
a.task_form_id , a.program_code,
 a.program_id , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num,
sum(case when d.component_status1  = 2  then 1 else 0 end) in_experiment,
sum(case when d.component_status1 = 6  then 1 else 0 end) is_finish 
from sfincident.program a  LEFT
JOIN sfincident.components d ON d.order_number = a.order_number 
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.order_id,
a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number;

CREATE OR REPLACE VIEW sfincident.PROGRAM_VIEW
AS 
SELECT a.pro_name,
       a.pro_id,
       a.order_id,
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
         left JOIN sfincident.PROGRAM_COMPONENT_VIEW b ON b.order_number = a.order_number;

CREATE OR REPLACE VIEW 
sfincident.PROGRAM_COMPONENT_VIEW AS SELECT  
a.pro_name, a.pro_id , a.task_id , a.order_number,a.order_id, 
a.task_form_id , a.program_code,  a.program_id , a.task_name_book,
a.order_time , a.remarks  , a.test_item , a.contract_id , a.sample_name , a.sample_material ,  
a.sample_num, sum(case when d.component_status1  = 1  then 1 else 0 end) in_experiment, 
sum(case when d.component_status1  = 2  then 1 else 0 end) is_finish from sfincident.program a  
JOIN sfincident.components d ON d.order_number = a.order_number 
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.order_id, a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name,  a.sample_material, a.sample_num, a.order_number;

CREATE OR REPLACE VIEW sfincident.PROGRAM_PROCESS AS
SELECT  a.pro_name, a.pro_id , a.order_number, 
c.incident_id, count(*) as sumprocess,count( if( c.process_status = 4 ,1,null)  = 0) as completed,
count( if( c.process_status = 0 ,1,null)  = 0) as inprocess,
ROUND(((count( if( c.process_status = 4 ,1,null)  = 0)) / count(*) )*100,2)     as percent
from sfincident.program a  join sfincident.incidents b ON b.order_number = a.order_number
 JOIN sfincident.processes c ON c.incident_id = b.incident_id group by pro_id,pro_name,order_number,incident_id;
 
 
 
 
CREATE OR REPLACE VIEW sfincident.component_series AS
SELECT
	cast(update_at AS date) AS 'date',
	count( if( (component_status1 = 3 or component_status1 = 6)  ,1,null)  = 0) as finish
FROM
	sfincident.components
GROUP BY
	cast(update_at AS date)