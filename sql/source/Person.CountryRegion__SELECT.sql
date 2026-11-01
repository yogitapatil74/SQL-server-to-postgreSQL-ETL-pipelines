SELECT [CountryRegionCode]
      ,[Name]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Person].[CountryRegion]