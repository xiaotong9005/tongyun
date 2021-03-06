--价值投机,起伏中套现
use [symbol];

with xianjinliu as(
select  [symbol]
      ,sum([basiceps]) as [basiceps]
      ,sum([opercashpershare]) as [opercashpershare]
  from [symbol].[dbo].[finance]
  where  reportdate in ('20170930','20170630','20170331','20161231')
  group by [symbol]
      ,[name]
      ,[compcode] 
	having sum([opercashpershare])>=sum([basiceps]) --每股现金流大于基本每股收益
	and sum([opercashpershare])>0					----每股现金流大于零
)

select *,iif(pb!=0,pe_lyr/pb,'') as roe_lyr,iif(pb!=0,pe_ttm/pb,'') as roe_ttm
  from [symbol].[dbo].[ma20]
  where pe_ttm<20	--市值/净利润
  and pb<=1.8	--市值/净资产
  --and price<ma20
  --and (name_cn not like '%银行%' or name_cn='平安银行')
  and time=(select max([time]) from [symbol].[dbo].symbol)
  and symbol in(
	select distinct [code] from [symbol].[dbo].[indexes] 
		where indexes in ('000903','000925'))
  and symbol in(
	select symbol from xianjinliu
	)
  order by pb
  