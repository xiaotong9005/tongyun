﻿select m.[symbol]
      ,m.[name_cn]
      ,m.[time]
      ,[price]
      ,[dateid]
      ,[avg_price]
  from [symbol].[dbo].[ma30] as m join symbol as s on m.symbol=s.symbol and m.time=s.time
  where m.time=(select max(time) from symbol)
  and price<=avg_price
  and m.symbol in (select code from [indexes] where indexes='000925')
	and pe_lyr<20
