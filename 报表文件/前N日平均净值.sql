with t as(
SELECT ROW_NUMBER() over (order by [净值日期]) as id,[基金代码]
      ,[简称]
      ,[累计净值]
      ,[净值日期]
  FROM [symbol].[dbo].[基金净值中心] as t
  where [基金代码] ='160716' 
)
select * 
,(select avg([累计净值]) from t as n 
	where t.[基金代码]=n.[基金代码]
	and n.净值日期<=t.[净值日期]
	and n.id>t.id-30) as 前N日平均净值
from t







with t as(
select row_number() over (order by [净值日期]) as id,* 
from (
	select [基金代码]
		  ,[简称]
		  ,[累计净值]
		  ,[净值日期]
	  from [symbol].[dbo].[基金净值中心] as t
	  where [基金代码] ='160706'
	union 
	select [基金代码]
		  ,[简称]
		  ,[累计净值]
		  ,[净值日期]
	from [基金净值中心_his] 
	where [基金代码] ='160706') as m  
)
select t.id
	,t.[基金代码]
	,t.[简称]
	,t.[累计净值]
	,t.[净值日期]
	,avg(t1.累计净值) as 前N日均值
	,t.[累计净值]-avg(t1.累计净值) as 离差
from t join t as t1 
on t.基金代码=t1.基金代码
and t1.净值日期<=t.净值日期
and t1.id>t.id-80
group by t.id
	,t.[基金代码]
	,t.[简称]
	,t.[累计净值]
	,t.[净值日期] 
	
	





with t as(
select row_number() over (order by [净值日期]) as id,* 
from (
	select [基金代码]
		  ,[简称]
		  ,[累计净值]
		  ,[净值日期]
	  from [symbol].[dbo].[基金净值中心] as t
	  where [基金代码] ='160706'
	union 
	select [基金代码]
		  ,[简称]
		  ,[累计净值]
		  ,[净值日期]
	from [基金净值中心_his] 
	where [基金代码] ='160706') as m  
)
select t.id
	,t.[基金代码]
	,t.[简称]
	,t.[净值日期]
	,t.[累计净值]
	,(select avg(累计净值) from t as t1
		where t.基金代码=t1.基金代码
		and t1.净值日期<=t.净值日期
		and t1.id>t.id-80
	  ) as 前80日均值
	,(select avg(累计净值) from t as t1
		where t.基金代码=t1.基金代码
		and t1.净值日期<=t.净值日期
		and t1.id>t.id-60
	  ) as 前60日均值
	,(select avg(累计净值) from t as t1
		where t.基金代码=t1.基金代码
		and t1.净值日期<=t.净值日期
		and t1.id>t.id-300
	  ) as 前30日均值
from t 	