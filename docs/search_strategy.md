# 数据库检索策略与语法（协议 v2）

正式检索覆盖2018年至检索截止年份；2026年为部分年度。经典基础研究可经前后向引文追踪补充。数据库导出批次及实际执行信息不在公开仓库中重新分发。

## 1. 冻结的概念检索式

以下A–E为统一语义源；换库时只改变字段名、通配符与界面要求，不改变词组逻辑。

### A 风险估计与校准

```text
("autonomous driving" OR "automated driving" OR "autonomous vehicle*" OR "automated vehicle*" OR "connected and autonomous vehicle*" OR "intelligent vehicle*" OR "self-driving")
AND ("trajectory prediction" OR "motion prediction" OR "motion forecasting" OR "trajectory planning" OR "motion planning" OR "behavior prediction" OR planner* OR "decision making" OR "end-to-end driving")
AND (uncertaint* OR calibrat* OR "conformal prediction" OR "prediction interval*" OR "perceptual uncertainty" OR "collision risk*" OR "risk estimation" OR "failure prediction" OR "risk-aware")
```

### B 分布偏移与监测

```text
("autonomous driving" OR "automated driving" OR "autonomous vehicle*" OR "automated vehicle*" OR "intelligent vehicle*" OR "self-driving")
AND ("trajectory prediction" OR "motion prediction" OR "trajectory planning" OR "motion planning" OR planner* OR "decision making" OR policy)
AND ("distribution shift" OR "distribution drift" OR "out-of-distribution" OR "change detection" OR "corner case*" OR "edge case*" OR anomal* OR "safety-critical scenario*" OR "runtime monitor*" OR "failure prediction" OR "failure detection" OR "risk monitoring")
```

### C 运行时保障与干预

```text
("autonomous driving" OR "automated driving" OR "autonomous vehicle*" OR "connected autonomous vehicle*" OR "intelligent vehicle*" OR "self-driving")
AND ("runtime assurance" OR "runtime monitor*" OR "risk monitor*" OR "safety filter*" OR "safety shield*" OR "safety layer*" OR "control filter*" OR "policy filter*" OR "control revision" OR "fallback control" OR "trajectory rejection" OR "safe replanning" OR "emergency braking" OR "minimal intervention")
AND (prediction OR planning OR planner* OR trajectory OR control OR action OR "decision risk")
```

### D 预测—规划风险接口

```text
("autonomous driving" OR "automated driving" OR "autonomous vehicle*" OR "automated vehicle*" OR "intelligent vehicle*" OR "self-driving")
AND ("motion prediction" OR "trajectory prediction" OR "behavior prediction" OR predictor* OR "perceptual uncertainty" OR "prediction failure")
AND ("motion planning" OR "trajectory planning" OR planner* OR control OR "decision making" OR "collision risk*")
AND ("uncertainty propagation" OR "uncertainty-aware planning" OR "decision risk" OR "risk-aware planning" OR "risk-aware decision making" OR "risk estimation" OR "collision risk*" OR "chance constraint*" OR "safety constraint*" OR "prediction set*" OR "conformal prediction")
```

### E 最近综述审计

```text
("autonomous driving" OR "automated driving" OR "autonomous vehicle*" OR "intelligent vehicle*" OR "autonomous system*")
AND TITLE(survey OR review OR overview OR "unified view")
AND (uncertaint* OR risk OR calibrat* OR "conformal prediction" OR "runtime assurance" OR "runtime monitoring" OR "safety filter*" OR "safe control" OR "formal verification" OR "motion prediction" OR planning)
```

## 2. 四库字段语法

每个数据库都按上面同一Query的三或四个括号组展开。下表是冻结的翻译规则；例如A在WoS中写为`TS=(A1) AND TS=(A2) AND TS=(A3)`，A在Scopus中写为`TITLE-ABS-KEY(A1) AND TITLE-ABS-KEY(A2) AND TITLE-ABS-KEY(A3)`。`A1`等不是实际提交变量，而是上节对应的完整括号内容；执行日志必须保存展开后的完整字符串。

| 数据库 | A–D字段 | E文献类型字段 | 年份过滤 | v2注意事项 |
|---|---|---|---|---|
| Web of Science Core Collection | `TS=(group)` | `TI=(survey OR review OR overview OR "unified view")`，其余组用`TS` | 界面选择2018–检索年 | `TS`覆盖Title、Abstract、Author Keywords、Keywords Plus；保留连字符短语和右截断`*` |
| Scopus | `TITLE-ABS-KEY(group)` | `TITLE(survey OR review OR overview OR "unified view")` | `PUBYEAR > 2017 AND PUBYEAR < 下一年` | 每个逻辑组分别加字段；不要把E类型词放回摘要字段 |
| IEEE Xplore | 每个term用`"All Metadata":term`，同组OR、组间AND | 每个类型term用`"Document Title":term` | 界面Publication Year 2018–检索年 | 在Command Search执行；若短语通配受限，拆成单复数并记录 |
| ACM Digital Library | `AllField:(group)` | `Title:(survey OR review OR overview OR "unified view")` | 界面Publication Date 2018–检索年 | ACM界面语法可能随版本变化；执行前用Advanced Search预览确认字段标签并保留字段设置 |

## 3. 可复制模板

可直接生成任一数据库、任一Query的完整展开字符串：

```bash
conda run -n py39 python scripts/generate_database_query.py --database wos --query A
conda run -n py39 python scripts/generate_database_query.py --database scopus --query D --year-end 2026
conda run -n py39 python scripts/generate_database_query.py --database ieee --query E
conda run -n py39 python scripts/generate_database_query.py --database acm --query C
```

`--database`可取`wos/scopus/ieee/acm`，`--query`可取`A/B/C/D/E`。因此20个库×检索式版本均由同一冻结词表生成，避免人工复制漂移。

### Web of Science

```text
TS=(GROUP_1) AND TS=(GROUP_2) AND TS=(GROUP_3)
TS=(GROUP_1) AND TS=(GROUP_2) AND TS=(GROUP_3) AND TS=(GROUP_4)  [仅D]
TS=(E_DOMAIN) AND TI=(survey OR review OR overview OR "unified view") AND TS=(E_TOPIC)  [仅E]
```

### Scopus

```text
TITLE-ABS-KEY(GROUP_1) AND TITLE-ABS-KEY(GROUP_2) AND TITLE-ABS-KEY(GROUP_3) AND PUBYEAR > 2017 AND PUBYEAR < 2027
TITLE-ABS-KEY(GROUP_1) AND TITLE-ABS-KEY(GROUP_2) AND TITLE-ABS-KEY(GROUP_3) AND TITLE-ABS-KEY(GROUP_4) AND PUBYEAR > 2017 AND PUBYEAR < 2027  [仅D]
TITLE-ABS-KEY(E_DOMAIN) AND TITLE(survey OR review OR overview OR "unified view") AND TITLE-ABS-KEY(E_TOPIC) AND PUBYEAR > 2017 AND PUBYEAR < 2027  [仅E]
```

2027年及以后更新检索时，将上界改为“执行年份+1”，并在日志注明；不能静默修改冻结文件。

### IEEE Xplore

```text
(("All Metadata":TERM_1) OR ("All Metadata":TERM_2) ...)
AND (("All Metadata":TERM_N) OR ...)
```

E的类型组改用`"Document Title"`。执行时将每个概念式中的term逐项展开，年份由左侧筛选器设置。

### ACM Digital Library

```text
AllField:(GROUP_1) AND AllField:(GROUP_2) AND AllField:(GROUP_3)
AllField:(GROUP_1) AND AllField:(GROUP_2) AND AllField:(GROUP_3) AND AllField:(GROUP_4)  [仅D]
AllField:(E_DOMAIN) AND Title:(survey OR review OR overview OR "unified view") AND AllField:(E_TOPIC)  [仅E]
```

## 4. 检索执行前检查

- 不把同义词组间的AND改为OR。
- 不以数据库的“AI改写/智能扩展”结果替代固定布尔检索。
- 分别保存A–E命中数和导出文件，再合并去重。
- 若某库不接受某个短语通配符，只做等价单复数展开，并保留在受限访问的检索日志中。
- 正式检索前用3篇代表性必召回条目做界面内spot-check；失败即停止导出并修正语法。
