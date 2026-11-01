SELECT [BusinessEntityID]
      ,[PhoneNumber]
      ,[PhoneNumberTypeID]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Person].[PersonPhone]