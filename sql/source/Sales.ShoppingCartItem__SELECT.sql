SELECT [ShoppingCartItemID]
      ,[ShoppingCartID]
      ,[Quantity]
      ,[ProductID]
      ,[DateCreated]
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[ShoppingCartItem]