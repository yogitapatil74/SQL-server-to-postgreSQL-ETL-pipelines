SELECT [ProductID]
      ,[Name]
      ,[ProductNumber]
      ,[MakeFlag] = CAST(CAST(MakeFlag AS BIT) AS CHAR(1))
      ,[FinishedGoodsFlag] = CAST(CAST(FinishedGoodsFlag AS BIT) AS CHAR(1))
      ,[Color]
      ,[SafetyStockLevel]
      ,[ReorderPoint]
      ,[StandardCost]
      ,[ListPrice]
      ,[Size]
      ,[SizeUnitMeasureCode]
      ,[WeightUnitMeasureCode]
      ,[Weight]
      ,[DaysToManufacture]
      ,[ProductLine] = RTRIM(ProductLine)
      ,[Class] = RTRIM(Class)
      ,[Style] = RTRIM(Style)
      ,[ProductSubcategoryID]
      ,[ProductModelID]
      ,[SellStartDate]
      ,[SellEndDate]
      ,[DiscontinuedDate]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Production].[Product]