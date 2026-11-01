SELECT [SalesOrderID]
      ,[RevisionNumber]
      ,[OrderDate] = CONVERT(VARCHAR,OrderDate,120)
      ,[DueDate] = CONVERT(VARCHAR,DueDate,120)
      ,[ShipDate] = CONVERT(VARCHAR,ShipDate,120)
      ,[Status]
      ,[OnlineOrderFlag] = CAST(CAST(OnlineOrderFlag AS BIT) AS CHAR(1))
      ,[PurchaseOrderNumber]
      ,[AccountNumber]
      ,[CustomerID]
      ,[SalesPersonID]
      ,[TerritoryID]
      ,[BillToAddressID]
      ,[ShipToAddressID]
      ,[ShipMethodID]
      ,[CreditCardID]
      ,[CreditCardApprovalCode]
      ,[CurrencyRateID]
      ,[SubTotal] = CAST(Subtotal AS DECIMAL(18,2))
      ,[TaxAmt] = CAST(Subtotal AS DECIMAL(18,2))
      ,[Freight] = CAST(Subtotal AS DECIMAL(18,2))
      ,[Comment]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SalesOrderHeader]   