CREATE OR REPLACE VIEW PROGRAM_INSTORE_VIEW
AS
SELECT  a.pro_name, a.pro_id , a.task_id , a.order_number,
a.task_path , a.program_code,
 a.program_code_path , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num, sum(c.is_num - c.in_store_num) AS w_sum,
b.res_name, b.create_name 
, b.finish_time , b.create_time , b.pro_name as project_name,
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address,b.id as project_id,
sum(c.in_store_num) as in_store_num 
FROM program a RIGHT JOIN project b ON b.id = a.pro_id

FULL OUTER JOIN instore c ON c.order_number = a.order_number

GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_path, 
a.program_code, a.program_code_path, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number,b.res_name, b.create_name 
, b.finish_time , b.create_time , 
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address,b.id,b.pro_name

CREATE OR REPLACE VIEW PROGRAM_COMPONENT_VIEW
AS
SELECT  a.pro_name, a.pro_id , a.task_id , a.order_number,
a.task_path , a.program_code,
 a.program_code_path , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num,


count(decode(d.component_status1, 1, 1, null)) in_experiment,
count(decode(d.component_status1, 2, 1, null)) is_finish from program a  

FULL OUTER JOIN components d ON d.order_number = a.order_number 
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_path, 
a.program_code, a.program_code_path, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number

CREATE OR REPLACE VIEW PROGRAM_VIEW
AS 
SELECT a.pro_name,
       a.pro_id,
       a.task_id,
         a.order_number,
         a.task_path,
         a.program_code,
         a.program_code_path,
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
         a.in_store_num,b.in_experiment,b.is_finish from PROGRAM_INSTORE_VIEW a
        FULL OUTER JOIN PROGRAM_COMPONENT_VIEW b ON b.order_number = a.order_number 

