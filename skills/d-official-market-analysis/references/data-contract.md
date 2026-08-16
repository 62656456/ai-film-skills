# D 原始数据合同

## 必填字段

```text
source_name
source_type
publisher
source_url
published_at
retrieved_at
data_period_start
data_period_end
region
platform
content_type
metric_name
metric_value
metric_unit
statistical_scope
methodology
sample_size
evidence_level
raw_excerpt
limitations
```

日期使用 `YYYY-MM-DD`。`evidence_level` 仅允许 S/A/B/C/D。`source_url` 必须是原始页面或原始文件链接。未知值保持为空，不用 0 代替。

## 推荐扩展字段

```text
title_name
genre
plot_engine
relationship_tag
emotion_value
narrative_structure
fact_type
access_status
metric_definition
is_head_sample
is_low_performance_sample
calculation_id
notes
```

## 不可直接合并的指标

- 播放次数、有效播放、观看人数。
- 平台热度值、播放量、搜索指数。
- 点赞率、评论率、转发率、收藏率。
- 充值金额、分账收入、票房、广告转化。
- 不同平台内部定义的完播率、留存率和热度值。

跨平台展示时按“同名同定义同周期同单位”比较；否则分栏或标准化为平台内排名/分位，并说明转换方法。任何标准化值都属于分析计算，不是官方原始指标。

## 缺失与冲突

日期、统计范围、指标定义、单位或口径缺失时，不进入排名计算。保留原记录并在 `limitations` 标注缺口。来源冲突时保留多行，不覆盖、不平均。

