delete from public.item;
delete from public.item_group;
insert into public.item_group(id, group_name, active) values (10, '性别', True);
insert into public.item(group_id, item_id, item_order, item_name, active) values (10, 1001, 1, '男', True);
insert into public.item(group_id, item_id, item_order, item_name, active) values (10, 1002, 2, '女', True);

insert into public.item_group(id, group_name, active) values (20, '仓库类别', True);
insert into public.item(group_id, item_id, item_order, item_name, active) values (20, 2001, 1, '成品仓', True);
insert into public.item(group_id, item_id, item_order, item_name, active) values (20, 2002, 2, '纸仓', True);
insert into public.item(group_id, item_id, item_order, item_name, active) values (20, 2003, 3, '辅料', True);

delete from public.job;
insert into public.job(job_name, active) values('总经理', True);
insert into public.job(job_name, active) values('采购经理', True);
insert into public.job(job_name, active) values('业务经理', True);
insert into public.job(job_name, active) values('财务经理', True);
insert into public.job(job_name, active) values('仓库主管', True);

delete from public.department;
insert into public.department(dept_name, active) values('采购部', True);
insert into public.department(dept_name, active) values('销售部', True);
insert into public.department(dept_name, active) values('生产车间', True);
insert into public.department(dept_name, active) values('仓库', True);


