SELECT [SpecialOfferID]
      ,[ProductID]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SpecialOfferProduct]