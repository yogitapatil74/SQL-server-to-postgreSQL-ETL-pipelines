SELECT [ProductModelID]
      ,[Name]
      ,[CatalogDescription] = CONVERT(VARCHAR(MAX),CatalogDescription)
      ,[Instructions] = CONVERT(VARCHAR(MAX),Instructions)
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Production].[ProductModel]