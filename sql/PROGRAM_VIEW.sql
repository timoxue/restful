
Use sfincident

CREATE OR REPLACE VIEW PROGRAM_INSTORE_VIEW
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

FROM project b LEFT JOIN program a ON b.id = a.pro_id LEFT JOIN instore c ON c.order_number = a.order_number
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.order_id,
a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number,b.res_name, b.create_name 
, b.finish_time , b.create_time , 
b.company , b.category, b.postcode , 
b.contact , b.tele_phone, b.u_email , b.address,b.id,b.pro_name;

CREATE OR REPLACE VIEW PROGRAM_COMPONENT_VIEW
AS
SELECT  a.pro_name, a.pro_id , a.task_id , a.order_number,a.order_id,
a.task_form_id , a.program_code,
 a.program_id , a.task_name_book,
  a.order_time , a.remarks 
, a.test_item , a.contract_id , a.sample_name , a.sample_material , 
a.sample_num,
sum(case when (d.component_status1  = 2 or d.component_status1=3) then 1 else 0 end) in_experiment,
sum(case when (d.component_status1 = 6 or d.component_status1=5 ) then 1 else 0 end) is_finish 
from program a  LEFT
JOIN components d ON d.order_number = a.order_number 
GROUP BY a.pro_name, a.pro_id, a.task_id, a.task_form_id, a.order_id,
a.program_code, a.program_id, a.task_name_book, a.order_time, a.remarks, a.test_item, a.contract_id, a.sample_name, 
a.sample_material, a.sample_num, a.order_number;

CREATE OR REPLACE VIEW PROGRAM_VIEW
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
         a.in_store_num,b.in_experiment,b.is_finish from PROGRAM_INSTORE_VIEW a
         left JOIN PROGRAM_COMPONENT_VIEW b ON b.order_number = a.order_number;




CREATE OR REPLACE VIEW PROGRAM_PROCESS AS
SELECT  a.pro_name, a.pro_id ,
 count(*) as sumprocess,count( if( c.process_status = 4 ,1,null)  = 0) as completed,
count( if( c.process_status = 0 ,1,null)  = 0) as inprocess,
ROUND(((count( if( c.process_status = 4 ,1,null)  = 0)) / count(*) )*100,2)  as percent
from program a  join incidents b ON b.order_number = a.order_number
 JOIN processes c ON c.incident_id = b.incident_id group by pro_id,pro_name;
 
 
 
 
CREATE OR REPLACE VIEW component_series AS
SELECT
	cast(update_at AS date) AS 'date',
	count( if( (component_status1 = 3 or component_status1 = 6)  ,1,null)  = 0) as finish
FROM
	components
GROUP BY
	cast(update_at AS date) desc;
    
CREATE OR REPLACE VIEW PROCESS_ALERT AS 
SELECT a.process_name,a.start_time_d,a.end_time_d,a.incident_id,b.experi_project,c.pro_name FROM SFINCIDENT.processes  a left join incidents b on a.incident_id = b.incident_id left join program c on c.order_number = b.order_number 
where cast(a.end_time_d AS date) < cast(now() As date) and a.process_status != 4;

CREATE OR REPLACE VIEW SFINCIDENT.PROGRAM_ALERT AS 
select * from PROGRAM_VIEW where cast(finish_time AS date) < cast(now() As date) and is_finish < sample_num;


CREATE OR REPLACE VIEW SFINCIDENT.efficiency as
select count(*) as c_count,experimenter from components where component_status1 = 3 or component_status1 =6 group by experimenter order by c_count desc;


CREATE OR REPLACE  VIEW `sub_process_view`  AS
select `a`.`experimenter` AS `experimenter`,`b`.`process_id` AS `process_id`,`b`.`process_name` AS 
`process_name`,`b`.`end_time_d` AS `end_time_d`,`b`.`start_time_d` AS `start_time_d`,`a`.`component_status` AS 
`component_status`,
c.create_name as create_name,`d`.`pro_name` AS `pro_name`,`c`.`incident_id` AS
 `incident_id`,(case 
 when count(if(a.component_status1=2 or a.component_status1=4,true,null)) > 0  
 then 3 
when   
 count(if(a.component_status1=1,true,null) ) > 0 
 then 2 
when   
count(if(a.component_status1=0,true,null)) > 0
 then 0 
 when
a.component_status1
then 4
end) AS `subProStatus` from (((`components` `a` join `processes` `b` 
on((`a`.`process_id` = `b`.`process_id`))) join `incidents` `c` on((`b`.`incident_id` = `c`.`incident_id`))) join `program` `d` on((`d`.`order_number` = `c`.`order_number`)))
 group by `a`.`experimenter`,`b`.`process_id`,`b`.`process_name`,`b`.`end_time_d`,`b`.`start_time_d`,`d`.`pro_name`,`c`.`incident_id`,c.create_name
union

 select `a`.`experimenter` AS `experimenter`,`b`.`process_id` AS `process_id`,`b`.`process_name` AS 
`process_name`,`b`.`end_time_d` AS `end_time_d`,`b`.`start_time_d` AS `start_time_d`,`a`.`component_status` AS 
`component_status`,
c.create_name as create_name,
`d`.`pro_name` AS `pro_name`,`c`.`incident_id` AS
 `incident_id`,(case 
when count(if(a.component_status1=2 or a.component_status1=4,true,null)) > 0  
 then 3 
  when   
 count(if(a.component_status1=1,true,null) ) > 0 
 then 2 
when   
count(if(a.component_status1=0,true,null)) > 0
 then 0 
 when
a.component_status1
then 4
end) AS `subProStatus` from (((`components_his` `a` join `processes` `b` 
on((`a`.`process_id` = `b`.`process_id`))) join `incidents` `c` on((`b`.`incident_id` = `c`.`incident_id`))) join `program` `d` on((`d`.`order_number` = `c`.`order_number`))) group by `a`.`experimenter`,`b`.`process_id`,`b`.`process_name`,`b`.`end_time_d`,`b`.`start_time_d`,`d`.`pro_name`,`c`.`incident_id`,c.create_name