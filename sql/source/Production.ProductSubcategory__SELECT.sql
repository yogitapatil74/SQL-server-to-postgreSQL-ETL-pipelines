SELECT [ProductSubcategoryID]
      ,[ProductCategoryID]
      ,[Name]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Production].[ProductSubcategory]