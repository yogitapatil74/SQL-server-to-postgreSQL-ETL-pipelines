SELECT [CountryRegionCode]
      ,[CurrencyCode]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[CountryRegionCurrency]