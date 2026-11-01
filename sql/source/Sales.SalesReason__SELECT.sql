SELECT [SalesReasonID]
      ,[Name]
      ,[ReasonType]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SalesReason]