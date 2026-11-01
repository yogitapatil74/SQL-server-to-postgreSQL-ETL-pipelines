SELECT [UnitMeasureCode]
      ,[Name]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Production].[UnitMeasure]