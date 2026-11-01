SELECT [SalesTaxRateID]
      ,[StateProvinceID]
      ,[TaxType]
      ,[TaxRate] = CONVERT(VARCHAR,TaxRate)
      ,[Name]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SalesTaxRate]