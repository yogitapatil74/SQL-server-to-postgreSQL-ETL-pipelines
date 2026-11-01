SELECT [BusinessEntityID]
      ,[EmailAddressID]
      ,[EmailAddress]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Person].[EmailAddress]