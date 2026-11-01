SELECT [SalesOrderID]
      ,[SalesOrderDetailID]
      ,[CarrierTrackingNumber]
      ,[OrderQty]
      ,[ProductID]
      ,[SpecialOfferID]
      ,[UnitPrice] = CAST(UnitPrice AS DECIMAL(18,2))
      ,[UnitPriceDiscount] = CAST(UnitPriceDiscount AS DECIMAL(18,2))
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SalesOrderDetail]