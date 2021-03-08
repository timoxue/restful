CREATE OR REPLACE VIEW PROGRAM_VIEW
AS 
SELECT  a.pro_name, a.pro_id , a.task_id , 
a.task_path , a.program_code,
 a.program_code_path , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num ,  
 b.res_name, b.create_name 
, b.finish_time , b.create_time , 
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address , sum(c.is_num - c.in_store_num) AS w_sum,
sum(c.in_store_num) as in_store_num
FROM program a LEFT OUTER JOIN project b ON b.id = a.pro_id LEFT OUTER JOIN instore c ON c.program_code = a.program_code
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_path, 
a.program_code, a.program_code_path, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, 
b.res_name, b.create_name, b.finish_time, b.create_time, b.company, b.category, b.postcode, b.contact, b.tele_phone, b.u_email, b.address
