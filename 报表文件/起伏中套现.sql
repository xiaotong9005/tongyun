﻿
--价值投机
use [symbol]

select *,iif(pb!=0,pe_lyr/pb,'') as roe_lyr,iif(pb!=0,pe_ttm/pb,'') as roe_ttm
  from [symbol].[dbo].[ma20]
  where price<ma20
  and pe_ttm<20	--市值/净利润
  and pb<=1.5	--市值/净资产
  --and (name_cn not like '%银行%' or name_cn='平安银行')
  and time=(select max([time]) from [symbol].[dbo].symbol)
  and symbol in(
	select distinct [code] from [symbol].[dbo].[indexes] 
		where indexes in ('000903','000925'))
  order by pb,pe_lyr
