SELECT [BusinessEntityID]
      ,[CreditCardID]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[PersonCreditCard]