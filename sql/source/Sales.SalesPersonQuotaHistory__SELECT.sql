SELECT [BusinessEntityID]
      ,[QuotaDate]
      ,[SalesQuota]
      ,[rowguid] = CONVERT(VARCHAR(36),rowguid)
      ,[ModifiedDate] = CONVERT(VARCHAR,ModifiedDate,120)
  FROM [Sales].[SalesPersonQuotaHistory]