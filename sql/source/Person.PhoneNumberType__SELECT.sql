SELECT [PhoneNumberTypeID]
      ,[Name]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Person].[PhoneNumberType]