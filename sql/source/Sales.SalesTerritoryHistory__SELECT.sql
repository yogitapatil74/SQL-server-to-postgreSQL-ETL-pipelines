SELECT [BusinessEntityID]
      ,[TerritoryID]
      ,[StartDate]
      ,[EndDate]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SalesTerritoryHistory]