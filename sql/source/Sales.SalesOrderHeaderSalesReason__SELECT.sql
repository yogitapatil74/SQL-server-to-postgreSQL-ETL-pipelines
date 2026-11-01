SELECT [SalesOrderID]
      ,[SalesReasonID]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SalesOrderHeaderSalesReason]