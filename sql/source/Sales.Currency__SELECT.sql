SELECT [CurrencyCode]
      ,[Name]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[Currency]