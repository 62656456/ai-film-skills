# D-Official-Market-Data 连接器合同

专属 MCP 或数据连接器只访问、整理和导出原始市场数据，不生成主观结论。

## 建议能力

`search_official_sources`、`fetch_official_report`、`fetch_platform_rankings`、`fetch_company_filings`、`fetch_industry_reports`、`fetch_title_performance`、`fetch_creator_reports`、`fetch_market_statistics`、`normalize_metrics`、`compare_sources`、`export_dataset`。

## 每条响应必须保留

原始链接、发布机构、发布时间、统计周期、指标定义、样本范围、数据值、单位、抓取时间、来源等级、使用限制。检索结果必须能回到原始页面或原始文件，不能只返回搜索摘要。

不同来源不一致时返回独立记录和口径差异，不在连接器层平均、覆盖或擅自合并。无法访问付费/登录数据时返回明确访问状态，不用二手估算补齐。
