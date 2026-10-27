# 下周共享页批量接入候选调研（2026-10-27）

建议把 **View Collections、Alter Collection Field、StructArray Overview、VarChar Field、RRF Ranker** 作为 2026-11-02 至 11-08 的 **5 篇内容对齐后接入批次**。它们均有明确的上游修正未反映到 Cloud，没有 Cloud 独有业务章节，快照均为 `current`，Guides/BYOC 均有现存页面。Delete Entities 按已完成试点排除。

**这不是 5 篇可以原样切换的页面。** 按“凡 Cloud 有而 Milvus 无的内容都算 Cloud-only”的严格口径，其中 4 篇仍有 **37 个新增语言代码块**，RRF 还有 Go/cURL 占位待补齐；必须先把可共用示例回补到 Milvus、对齐正文，再接入。若本批要求完全不做上游内容对齐、也不用 WP10，则本次没有足够证据推荐满足条件的 5–10 篇，不能为了凑数把缺失代码说成零成本。下面把“独有业务章节”和“上游缺失的通用代码/图片”分别列出，后者同样属于接入前的阻断项。

本报告只读取两份源仓库与快照，唯一交付是设计仓库中的本文件；未修改 zdoc / milvus-docs，未在它们开 PR，也未运行 Fetch、Translation、接入或激活。推荐是未来的工作范围，不代表本次已实施。

## 固定输入与覆盖范围

| 输入 | 精确修订 / 说明 |
|---|---|
| `milvus-io/milvus-docs` `v3.0.x` | [`d631183688a0e53acd092ae6d923fca28c2b9f5c`](https://github.com/milvus-io/milvus-docs/commit/d631183688a0e53acd092ae6d923fca28c2b9f5c) |
| `zilliztech/zdoc` `dev` | [`008e48a0705efbfa041333efa197119a7fd6900d`](https://github.com/zilliztech/zdoc/commit/008e48a0705efbfa041333efa197119a7fd6900d) |
| `liyun95/milvus-zilliz-docs-design` `main` | [`2135a6d717031de311aa98b0ffe26dfda4dcd8d4`](https://github.com/liyun95/milvus-zilliz-docs-design/commit/2135a6d717031de311aa98b0ffe26dfda4dcd8d4) |
| Release Channel 快照 | [packages/docs-tooling/src/lark/meta/snapshots/guides-uat-last-success.json](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/packages/docs-tooling/src/lark/meta/snapshots/guides-uat-last-success.json)；`generated_at=2026-10-26T10:47:45.798Z`，最后提交 `d151bc9e76693eaed00552e12d17b23bd4c1d10f` |
| 范围与约束依据 | [实现指南](https://github.com/liyun95/milvus-zilliz-docs-design/blob/2135a6d717031de311aa98b0ffe26dfda4dcd8d4/docs/implementation/README.md)、[PRD 场景 3](https://github.com/liyun95/milvus-zilliz-docs-design/blob/2135a6d717031de311aa98b0ffe26dfda4dcd8d4/docs/prd.md)、[链接审查清单](https://github.com/liyun95/milvus-zilliz-docs-design/blob/2135a6d717031de311aa98b0ffe26dfda4dcd8d4/research/link-review-2026-10-27.md)；WP10 未开始，接入不等于激活 |

扫描 Milvus `site/en/userGuide/` 的 **203** 个 Markdown 文件，与 Cloud Guides/BYOC 共 **704** 个 Markdown/MDX 文件匹配：**123 篇命中，80 篇无同 slug/同标题而跳过**；123 篇中排除已完成 Delete Entities 后还有 **122 篇**。前 20 名逐篇人工复核，附录保留其他 102 篇及试点的机器测量与未决项，不把未复核页标成可接入。

两个源仓库均使用非 shallow 的临时 bare 副本；读取完整分支历史，不设 `--since`。前 20 页另外用 `git log --follow` 追踪重命名。Cloud 文件提交是生成物最后落 Git 的时间，**不是飞书作者最后改正文的时间**；快照的 `obj_edit_time` 也不能证明某条 Milvus 修正已同步。所有日期统一为北京时间（UTC+8），具体提交链接可查看原始时区。

快照 `records` 的 **403 条 `release_channel` 全为 `current`，NEXT=0**；前 20 页通过 slug、front matter token 和记录 doc_token 交叉核验，发布目标包含对应手册。快照 `output_paths` 为空，路径取固定 dev 文件树，不臆造快照路径。`PUBLIC`/`PRIVATE` 是功能标签，不能当作整页 `NEXT`。结论只代表这份快照，接入前仍应读新快照。

## 前 20 名：收益与正文分叉

排序为人工排期：先看已证实的修正遗漏，再看是否需要 Cloud 专属变换、缺失代码规模、图片与待判链接；同层优先短页及纠错收益。不是按差异百分比机械排序。1–5 为建议批次；6–9 为高收益备选但仍有更大的代码或语义障碍；10–15 为高成本分叉；16–18 未证实近期遗漏；19–20 最新修正已在 Cloud，降低追赶优先级。

`M` 路径前缀为 `site/en/userGuide/`；`G/B` 为 Guides/BYOC。`−/+` 是 Milvus→Cloud 的删除/新增规范化 token 数，百分比为 `(删除+新增)/(两端 token 总数)`；不是遗漏比例或代码正确率。19 篇同时有 G/B，且两端测量数值一致；Snapshots 只有 Guides（BYOC 无匹配页），下表以 G-only 标记。具体路径和提交见逐页证据。

| 排名 | Milvus 页 / 源路径 | Cloud slug | 最后提交 M → G/B（北京时间） | 差异 −/+（比例） | 判断 / 优先原因 |
|---:|---|---|---|---|---|
| 1 | **View Collections**<br>[collections/view-collections.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/view-collections.md) | `view-collections` | 2026-10-26 → 2026-10-25 | −125/+675（34.2%） | 已证实；首批；两个短章节，Python 只差连接值，0 图、0 待判链接。 |
| 2 | **Alter Collection Field**<br>[schema/alter-collection-field.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/alter-collection-field.md) | `alter-collection-field` | 2026-10-26 → 2026-10-25 | −134/+922（33.4%） | 已证实；首批；单句纠错有明确收益，先保留并回补 Cloud 的 SDK 示例。 |
| 3 | **StructArray Overview**<br>[schema/array-of-structs.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/array-of-structs.md) | `use-array-of-structs` | 2026-10-26 → 2026-09-15 | −57/+17（2.4%） | 已证实；首批；规范化差异小，0 图；需验证现有渲染器能保留双栏内容及锚点。 |
| 4 | **VarChar Field**<br>[schema/string.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/string.md) | `use-string-field` | 2026-10-26 → 2026-10-19 | −301/+3132（22.6%） | 已证实；首批；先把通用参数修正和新增语言回补上游；不能机械覆盖 Cloud。 |
| 5 | **RRF Ranker**<br>[embeddings-reranking/reranking/rrf-ranker.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md) | `reranking-rrf` | 2026-10-26 → 2026-10-25 | −133/+1366（31.9%） | 已证实；首批；可修复参数表错误；NodeJS 已同步，其他 SDK 形式需核验，1 张图需迁移。 |
| 6 | **Multi-language Analyzers**<br>[schema/analyzer/multi-language-analyzers.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/multi-language-analyzers.md) | `multi-language-analyzers` | 2026-10-26 → 2026-10-24 | −1179/+4617（34.0%） | 已证实；备选；24 个新增语言块，且 Arabic/Thai 的可用性差异需判断，工作量超过首批。 |
| 7 | **Filtered Search with StructArray**<br>[search-query-get/filtered-search-with-structarray.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/filtered-search-with-structarray.md) | `filtered-search-with-struct-arrays` | 2026-10-26 → 2026-10-25 | −85/+7080（67.0%） | 已证实；备选；28 个新增语言块及 API 参数差异需先验证，不能把这些都当作排版。 |
| 8 | **StructArray Limits**<br>[schema/structarray-limits.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/structarray-limits.md) | `struct-array-limits` | 2026-10-26 → 2026-09-03 | −101/+105（5.9%） | 已证实；备选；不能因 diff 小就跳过同节产品适用范围改写；涉及历史支持范围，需人工对齐。 |
| 9 | **Array Field**<br>[schema/array_data_type.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/array_data_type.md) | `use-array-fields` | 2026-10-26 → 2026-10-24 | −908/+3633（33.4%） | 已证实；暂缓；先确认产品/版本差异，再决定回补还是变换，不能仅按同标题合并。 |
| 10 | **Use Partition Key**<br>[search-query-get/use-partition-key.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/use-partition-key.md) | `use-partition-key` | 2026-10-26 → 2026-10-25 | −1034/+1249（32.4%） | 已证实；暂缓；原文新增索引建议有价值，但 CLI 需要 WP10 或另行确定来源。 |
| 11 | **Basic Operators**<br>[search-query-get/boolean/basic-operators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/basic-operators.md) | `basic-filtering-operators` | 2026-10-26 → 2026-10-24 | −1334/+3640（61.4%） | 已证实；暂缓；Cloud 也有更完整内容，必须双向对齐，不能以最新时间决定整页胜负。 |
| 12 | **StructArray Operators**<br>[search-query-get/boolean/struct-array-operators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/struct-array-operators.md) | `struct-array-filtering` | 2026-10-26 → 2026-10-24 | −810/+763（37.7%） | 部分已反映；暂缓；先合并两套例子并纠正冲突，再确认是否能全共享。 |
| 13 | **Phrase Match**<br>[search-query-get/phrase-match.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/phrase-match.md) | `phrase-match` | 2026-10-26 → 2026-10-25 | −2620/+6972（55.6%） | 已证实；暂缓；Cloud 功能步骤与 CLI 都要保留。 |
| 14 | **Snapshots**<br>[search-query-get/snapshots.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/snapshots.md) | `snapshots` | 2026-10-23 → 2026-08-17（G-only） | −73/+32（7.6%） | 已证实；暂缓；2 个待判链接目标、3 次引用；备份目标和 DocCardList 处理先明确。 |
| 15 | **Create an External Collection**<br>[collections/create-an-external-collection.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/create-an-external-collection.md) | `create-external-collection` | 2026-10-22 → 2026-10-15 | −1548/+2448（44.2%） | 部分已反映；暂缓；成本高，需 WP10；不要用同标题推断可整篇复用。 |
| 16 | **Search with EmbeddingLists: ColBERT and ColPali**<br>[search-query-get/search-with-embedding-lists.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/search-with-embedding-lists.md) | `tutorial-colbert-colpali` | 2026-07-29 → 2026-09-15 | −2/+14（0.2%） | 未证实近期遗漏；备选但不进首批；0.2% 差异掩盖缺图，先把图与兼容条件整理进可共享来源。 |
| 17 | **Membership Match**<br>[search-query-get/boolean/membership-match.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/membership-match.md) | `membership-match` | 2026-10-13 → 2026-10-26 | −483/+45（11.3%） | 未证实近期遗漏；暂缓；原文 4 次 milvus.yaml，需 WP10/内容重构。 |
| 18 | **Filtered Search**<br>[search-query-get/filtered-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/filtered-search.md) | `filtered-search` | 2026-05-14 → 2026-10-24 | −59/+1842（22.0%） | 未证实近期遗漏；延续既有试点计划；不挤入本次零业务专属章节批次。 |
| 19 | **Full Text Search**<br>[search-query-get/full-text-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/full-text-search.md) | `full-text-search` | 2026-10-26 → 2026-10-10 | −1033/+2122（25.9%） | 最新修正已反映；暂缓；需要产品参数变换。 |
| 20 | **Query**<br>[search-query-get/get-and-scalar-query.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/get-and-scalar-query.md) | `get-and-scalar-query` | 2026-10-26 → 2026-10-25 | −1797/+8919（39.5%） | 最新修正已反映；暂缓；业务示例和 CLI 都需处理。 |

## 前 20 名：接入成本

命中字面量只数 Milvus **正文（不含 front matter）**，区分大小写；四元组为 `localhost / root:Milvus / 独立单词 Milvus / milvus.yaml`。`Milvus` 的原始命中包含 `root:Milvus`、版本名等，需要逐处判断，不能全部替换；不计 `MilvusClient` 等 SDK 标识。

代码栏列 Milvus 围栏语言 → Cloud 非空 Tab 集；`json/text/plaintext/sql` 等示例数据也列在逐页证据中，未放进 Tabs 的代码不会凭空当成 Tab。`c++` 与 `cpp` 在新增语言判断时视为同一种。空白 Tab 不计，注释占位单列。图片数是引用次数，不是下载、去重或视觉相同的证明。

| # | 字面量四元组 | Milvus 围栏 → Cloud Tab | 图 M→G/B | 新增语言块（每手册） | Cloud 独有内容/同节差异 | Channel |
|---:|---|---|---|---:|---|---|
| 1 | 4 / 4 / 4 / 0 | bash, go, java, javascript, json, plaintext, python → bash, c++, csharp, go, java, javascript, python, rust | 0→0 | 6 | 0 个独有业务章节；新增 C++/C#/Rust 通用示例，需先回补上游。 | CURRENT |
| 2 | 3 / 2 / 3 / 0 | bash, go, java, javascript, python → bash, c++, csharp, go, java, javascript, python, rust | 0→0 | 9 | 0 个独有业务章节；新增 C++/C#/Rust 通用示例。 | CURRENT |
| 3 | 0 / 0 / 1 / 0 | json → — | 0→0 | 0 | 0 个独有内容章节/新增语言块；HTML 双栏表与 Cloud Grid 是排版差异。 | CURRENT |
| 4 | 4 / 0 / 6 / 0 | bash, go, java, javascript, python → bash, c++, go, java, javascript, python, rust | 0→0 | 16 | 0 个独有业务章节；新增 C++/Rust 通用示例；Cloud 已把 `enable_dynamic_fields` 修成 `enable_dynamic_field`，不可回退。 | CURRENT |
| 5 | 3 / 0 / 3 / 0 | bash, go, java, javascript, python → bash, c++, csharp, go, java, javascript, python, rust；M 占位：go, bash | 1→1 | 6 | 0 个独有业务章节；新增 C++/C#/Rust 示例；Milvus Go/bash 围栏只是注释占位，还需补齐。 | CURRENT |
| 6 | 5 / 2 / 18 / 0 | bash, go, java, javascript, python → bash, c++, csharp, go, java, javascript, python, rust | 1→1 | 24 | 没有独有业务整节；Step 1–4 是原有标题加前缀。Cloud 另补 `load_collection()`，原文有 Arabic/Thai 配置而 Cloud 没有。 | CURRENT |
| 7 | 1 / 1 / 1 / 0 | python → bash, c++, csharp, go, java, javascript, python, rust | 0→0 | 28 | 无独有业务整节；Cloud 补 EmbeddingList 构造及 hybrid search 参数，并把输出 `hit["id"]` 改成 `hit["doc_id"]`。 | CURRENT |
| 8 | 0 / 0 / 6 / 0 | — → — | 0→0 | 0 | 无独有标题；Nullable/Dynamic add 表格改为 Cloud On-Demand 范围，部分措辞只在 Cloud 表格中。原文后文已有 Cloud/Serving 限制，仍需整合。 | CURRENT |
| 9 | 3 / 0 / 7 / 0 | bash, go, java, javascript, json, python → bash, c++, csharp, go, java, javascript, python, rust | 0→0 | 21 | 0 个独有整节，但 Cloud 声称 element_type 支持 JSON/STRUCT，原文明确排除 JSON；存在实质性内容冲突。 | CURRENT |
| 10 | 6 / 5 / 23 / 0 | bash, go, java, javascript, python → bash, c++, csharp, go, java, javascript, python, rust, shell | 3→3 | 16 | 首段增加 namespace/tenant 场景表述，另有 Zilliz CLI 专属 Tab；保留这些需要来源或变换。 | CURRENT |
| 11 | 0 / 0 / 12 / 0 | python → bash, c++, csharp, go, java, javascript, python, rust | 0→0 | 147 | 至少 Bitwise operators、向量 NULL 过滤示例/行为说明等 Cloud 新增内容；147 个新增语言块。 | CURRENT |
| 12 | 0 / 0 / 0 / 0 | python → — | 0→0 | 0 | Example data、Entity A/B 结果解释只在 Cloud；Subfield access/ARRAY operators 与上游新节有语义重叠，不能全算独有。 | CURRENT |
| 13 | 4 / 4 / 11 / 0 | bash, cpp, go, java, javascript, python → bash, c++, csharp, go, java, javascript, python, shell | 1→1 | 16 | Cloud 另补 default/custom analyzer 说明与创建、插入、索引、加载的展开示例；不是两个标题重命名就能消除。 | CURRENT |
| 14 | 0 / 0 / 8 / 0 | text → — | 0→0 | 0 | 没有新增业务整节；Further readings 用 DocCardList 替代 Milvus 链接列表，属于 Cloud 导航组件。 | CURRENT |
| 15 | 3 / 3 / 23 / 1 | bash, go, java, javascript, json, python → bash, c++, go, java, javascript, python, rust | 2→2 | 10 | Preparation（API key/存储集成/External Volume）、更多数据源、on-demand session 与 Follow-ups 都是 Cloud 独有。 | CURRENT |
| 16 | 1 / 1 / 6 / 0 | Shell, python → — | 0→2 | 0 | 无新增业务标题，但 Cloud 独有 2 张插图及集群兼容版本措辞；Milvus 正文仍引用不存在的 above diagram。 | CURRENT |
| 17 | 1 / 0 / 1 / 4 | go, java, javascript, python, text → go, java, javascript, python | 1→2 | 0 | Cloud 多 1 张选型图及配套解读；删除自部署配置段也需要 remove 规则或共享改写。 | CURRENT |
| 18 | 10 / 10 / 16 / 0 | bash, go, java, javascript, json, python → bash, c++, csharp, go, java, javascript, python, rust, shell | 2→2 | 8 | Cloud 独有 Zilliz CLI 两个示例；新增 C++/C#/Rust 通用示例。 | CURRENT |
| 19 | 5 / 4 / 16 / 0 | bash, cpp, go, java, javascript, python → bash, c++, go, java, javascript, python, rust, shell | 1→1 | 14 | 同节中有 Cloud 的 `params.level` / Tune Recall Rate 说明、AUTOINDEX 差异和 CLI 示例，不能用标题差集判为 0。 | CURRENT |
| 20 | 26 / 24 / 29 / 0 | bash, cpp, go, java, javascript, python → bash, c++, csharp, go, java, javascript, python, rust, shell | 0→0 | 39 | PUBLIC 标记本身不是新章节；Cloud 在聚合章节另有 composite groups、limit 等更完整例子，以及 CLI Tab。 | CURRENT |

“新增语言块”按 Cloud TabItem 内有非空围栏、且该语言未出现在 Milvus 围栏集中计数；是**最低工作量**，不包括同语言新示例、参数改动、Milvus 注释占位补全。Guides/BYOC 相同内容只算一套对齐工作，不把 37 块翻倍为 74。

## 建议批次与交付边界

| 页 | 为什么进本批 | 接入前必须完成 |
|---|---|---|
| View Collections | 已证实遗漏；0 Cloud 独有业务章节；CURRENT | 补 `has_collection()` 说明；把 Cloud 6 个 C++/C#/Rust 代码块回补成通用原文，连接值使用共享变量。 |
| Alter Collection Field | 已证实遗漏；0 Cloud 独有业务章节；CURRENT | 同步 bytes 修正；回补 9 个通用语言块，保留 VarChar、ARRAY、mmap 三个现有章节。 |
| StructArray Overview | 已证实遗漏；0 Cloud 独有业务章节；CURRENT | 同步行级路径过滤两处说明；核验原文 HTML 表格与 Cloud Grid 的文字等价及生成兼容性；不引入专属块。 |
| VarChar Field | 已证实遗漏；0 Cloud 独有业务章节；CURRENT | 同步 UTF-8 示例；回补 16 个 C++/Rust 代码块和正确的 `enable_dynamic_field`；核对 TEXT/NGRAM 链接与适用范围。 |
| RRF Ranker | 已证实遗漏；0 Cloud 独有业务章节；CURRENT | 同步 RRF 修复并核验每种 SDK 的调用形式；回补 6 个新增语言块及 Go/cURL 占位，核验 1 张图。 |

以上 5 页都不需要为了保留 **Cloud 专属业务章节**而等待 WP10；但新增代码若留在 Cloud 一侧、没有回补为共享来源，就仍然需要 named blocks/transforms，届时不符合本批门槛。**禁止通过删除 Cloud 现有语言 Tab 来伪造零差异。** 内容对齐后才能冻结新 source commit、生成比较、审 golden、提交 `page.yaml`；本次固定 SHA 仅用于调研，不应冒充对齐后的接入 lock。

若只能做零内容对齐的纯配置接入，本次不推荐凑足 5 篇；StructArray Overview 是最接近的一篇，也仍需把两处遗漏反映出来并验证渲染。若首批进度允许，优先再评估 #6/#7；先解决语言示例与可用性差异，不直接扩到有 CLI、Cloud API/存储集成或新图的页面。

## 逐页证据、链接负担与精确提交

这里的链接范围同时覆盖链接审查清单的 **39 个待判目标 U** 与附录 **93 个已有建议目标 S**，不是把全部 132 个都叫“坏链接”。M 是原文引用次数；C 是 Cloud 中经现存映射/同标题对应关系还原后的目标次数，每手册计数。没有 M 链接不等于没有站外链接。缺失锚点、URL 可达性与最终 `links.yaml` 是否已登记未在本次跑站点验证。

### 1. View Collections（`view-collections`）

- 源：[site/en/userGuide/collections/view-collections.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/view-collections.md)。
- Cloud：[guides/tutorials/development/collection/view-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/view-collections.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/collection/view-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/view-collections.md)；匹配依据：同 slug。
- 漂移：Cloud 缺少 10-26 新增的 `list_collections()` 不用于存在性检查、应调用 `has_collection()` 的说明。
- 上游最后提交：[b534c3820d](https://github.com/milvus-io/milvus-docs/commit/b534c3820d465d2aed3b5a06dc41fe3484a7c01f)（`b534c3820d465d2aed3b5a06dc41fe3484a7c01f`），2026-10-26；`--follow` 历史 9 个提交。
- guides 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−125/+675（34.2%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, json, python, rust, sql。
- byoc 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−125/+675（34.2%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, json, python, rust, sql。
- 快照记录：`recvlPs8qTFnJf`，`current`，对应手册 token 匹配。
- 清单链接 M：—；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：—。

### 2. Alter Collection Field（`alter-collection-field`）

- 源：[site/en/userGuide/schema/alter-collection-field.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/alter-collection-field.md)。
- Cloud：[guides/tutorials/development/schema/alter-collection-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/alter-collection-field.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/schema/alter-collection-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/alter-collection-field.md)；匹配依据：同 slug。
- 漂移：Milvus 把 `max_length` 的含义修成 bytes；Cloud 的 Alter VarChar field 仍写 characters。
- 上游最后提交：[c7378f5c6c](https://github.com/milvus-io/milvus-docs/commit/c7378f5c6c0d8b466260d651de90a3a0473c5303)（`c7378f5c6c0d8b466260d651de90a3a0473c5303`），2026-10-26；`--follow` 历史 5 个提交。
- guides 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−134/+922（33.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- byoc 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−134/+922（33.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- 快照记录：`recvlPtzpXFjxH`，`current`，对应手册 token 匹配。
- 清单链接 M：—；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：—。

### 3. StructArray Overview（`array-of-structs`）

- 源：[site/en/userGuide/schema/array-of-structs.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/array-of-structs.md)。
- Cloud：[guides/tutorials/development/schema/struct-array/use-array-of-structs.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/struct-array/use-array-of-structs.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/schema/struct-array/use-array-of-structs.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/struct-array/use-array-of-structs.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 的 Documentation map 与 Key limits to check first 均未包含新增的行级 StructArray 路径过滤说明。
- 上游最后提交：[d24c03d010](https://github.com/milvus-io/milvus-docs/commit/d24c03d010da4d0ce393a9f5d0baac0a2ad8c509)（`d24c03d010da4d0ce393a9f5d0baac0a2ad8c509`），2026-10-26；`--follow` 历史 14 个提交。
- guides 最后提交：[437c9308ae](https://github.com/zilliztech/zdoc/commit/437c9308ae84c11115667b936e75b03c68562007)（`437c9308ae84c11115667b936e75b03c68562007`），2026-09-15；−57/+17（2.4%）；完整代码围栏集：json。
- byoc 最后提交：[437c9308ae](https://github.com/zilliztech/zdoc/commit/437c9308ae84c11115667b936e75b03c68562007)（`437c9308ae84c11115667b936e75b03c68562007`），2026-09-15；−57/+17（2.4%）；完整代码围栏集：json。
- 快照记录：`recvmiX4gMiGuY`，`current`，对应手册 token 匹配。
- 清单链接 M：`basic-vector-search-with-structarray.md`×3、`create-structarray-field.md`×3、`filtered-search-with-structarray.md`×3、`grouping-search-with-structarray.md`×2、`hybrid-search-with-structarray.md`×2、`index-structarray-fields.md`×2、`insert-data-into-structarray-fields.md`×3、`range-search-with-structarray.md`×2、`search-with-embedding-lists.md`×2、`struct-array-operators.md`×3、`structarray-limits.md`×2；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`basic-vector-search-with-structarray.md`×3、`create-structarray-field.md`×3、`filtered-search-with-structarray.md`×3、`grouping-search-with-structarray.md`×2、`hybrid-search-with-structarray.md`×2、`index-structarray-fields.md`×2、`insert-data-into-structarray-fields.md`×3、`range-search-with-structarray.md`×2、`search-with-embedding-lists.md`×2、`struct-array-operators.md`×3、`structarray-limits.md`×2。

### 4. VarChar Field（`string`）

- 源：[site/en/userGuide/schema/string.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/string.md)。
- Cloud：[guides/tutorials/development/schema/use-string-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-string-field.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/schema/use-string-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-string-field.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 缺少 UTF-8 bytes 与 10 个中文字符占 30 字节的例子；没有原文关于 TEXT 超过 65,535 字节的提示。
- 上游最后提交：[c7378f5c6c](https://github.com/milvus-io/milvus-docs/commit/c7378f5c6c0d8b466260d651de90a3a0473c5303)（`c7378f5c6c0d8b466260d651de90a3a0473c5303`），2026-10-26；`--follow` 历史 15 个提交。
- guides 最后提交：[e02d9b0ef0](https://github.com/zilliztech/zdoc/commit/e02d9b0ef061918683cd15f518b1a48e94f9b70d)（`e02d9b0ef061918683cd15f518b1a48e94f9b70d`），2026-10-19；−301/+3132（22.6%）；完整代码围栏集：bash, c++, go, java, javascript, python, rust。
- byoc 最后提交：[e02d9b0ef0](https://github.com/zilliztech/zdoc/commit/e02d9b0ef061918683cd15f518b1a48e94f9b70d)（`e02d9b0ef061918683cd15f518b1a48e94f9b70d`），2026-10-19；−301/+3132（22.6%）；完整代码围栏集：bash, c++, go, java, javascript, python, rust。
- 快照记录：`recvlPt5P3vHmN`，`current`，对应手册 token 匹配。
- 清单链接 M：`index-explained.md`×1、`ngram.md`×1、`nullable-and-default.md`×1、`text.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`nullable-and-default.md`×1、`text.md`×1。

### 5. RRF Ranker（`rrf-ranker`）

- 源：[site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md)。
- Cloud：[guides/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-rrf.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-rrf.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-rrf.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-rrf.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 参数表的 `params.reranker` 示例仍为 `weighted`，应为 `rrf`；NodeJS 的 `rrf`/`k`/`type` 已提前修好。Python/Java 使用 Function 对象而上游改用 RRFRanker，需核验 SDK 兼容性，不能一概说未同步。
- 上游最后提交：[5a0b1037d0](https://github.com/milvus-io/milvus-docs/commit/5a0b1037d0d3265a7c57b59655769ac921a2db46)（`5a0b1037d0d3265a7c57b59655769ac921a2db46`），2026-10-26；`--follow` 历史 11 个提交。
- guides 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−133/+1366（31.9%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- byoc 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−133/+1366（31.9%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- 快照记录：`recvlUWzUlvYoV`，`current`，对应手册 token 匹配。
- 清单链接 M：`multi-vector-search.md`×1、`rrf-ranker.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`multi-vector-search.md`×1、`rrf-ranker.md`×1。

### 6. Multi-language Analyzers（`multi-language-analyzers`）

- 源：[site/en/userGuide/schema/analyzer/multi-language-analyzers.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/multi-language-analyzers.md)。
- Cloud：[guides/tutorials/development/analyzer/multi-language-analyzers.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/multi-language-analyzers.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/analyzer/multi-language-analyzers.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/multi-language-analyzers.md)；匹配依据：同 slug。
- 漂移：Cloud Python 的两处 max_length 注释仍未写 in bytes。
- 上游最后提交：[c7378f5c6c](https://github.com/milvus-io/milvus-docs/commit/c7378f5c6c0d8b466260d651de90a3a0473c5303)（`c7378f5c6c0d8b466260d651de90a3a0473c5303`），2026-10-26；`--follow` 历史 8 个提交。
- guides 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−1179/+4617（34.0%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- byoc 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−1179/+4617（34.0%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- 快照记录：`recvlPv5VDWiEw`，`current`，对应手册 token 匹配。
- 清单链接 M：`sparse_vector.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`sparse_vector.md`×1。

### 7. Filtered Search with StructArray（`filtered-search-with-structarray`）

- 源：[site/en/userGuide/search-query-get/filtered-search-with-structarray.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/filtered-search-with-structarray.md)。
- Cloud：[guides/tutorials/development/search-and-query/struct-array-search/filtered-search-with-struct-arrays.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/struct-array-search/filtered-search-with-struct-arrays.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/search-and-query/struct-array-search/filtered-search-with-struct-arrays.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/struct-array-search/filtered-search-with-struct-arrays.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 的开头选型表未包含新增的 row-level StructArray paths 一行。
- 上游最后提交：[d24c03d010](https://github.com/milvus-io/milvus-docs/commit/d24c03d010da4d0ce393a9f5d0baac0a2ad8c509)（`d24c03d010da4d0ce393a9f5d0baac0a2ad8c509`），2026-10-26；`--follow` 历史 2 个提交。
- guides 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−85/+7080（67.0%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- byoc 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−85/+7080（67.0%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- 快照记录：`recvmiYazRHkb7`，`current`，对应手册 token 匹配。
- 清单链接 M：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`hybrid-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`struct-array-operators.md`×4、`structarray-limits.md`×2；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`hybrid-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`struct-array-operators.md`×3、`structarray-limits.md`×2。

### 8. StructArray Limits（`structarray-limits`）

- 源：[site/en/userGuide/schema/structarray-limits.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/structarray-limits.md)。
- Cloud：[guides/tutorials/development/schema/struct-array/struct-array-limits.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/struct-array/struct-array-limits.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/schema/struct-array/struct-array-limits.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/struct-array/struct-array-limits.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 缺少新增的 positional path、array_length、array_contains 与 IS NULL 概述。
- 上游最后提交：[d24c03d010](https://github.com/milvus-io/milvus-docs/commit/d24c03d010da4d0ce393a9f5d0baac0a2ad8c509)（`d24c03d010da4d0ce393a9f5d0baac0a2ad8c509`），2026-10-26；`--follow` 历史 3 个提交。
- guides 最后提交：[deab0e42cf](https://github.com/zilliztech/zdoc/commit/deab0e42cfc0645f7bfa67181340476c8bc676b5)（`deab0e42cfc0645f7bfa67181340476c8bc676b5`），2026-09-03；−101/+105（5.9%）；完整代码围栏集：—。
- byoc 最后提交：[deab0e42cf](https://github.com/zilliztech/zdoc/commit/deab0e42cfc0645f7bfa67181340476c8bc676b5)（`deab0e42cfc0645f7bfa67181340476c8bc676b5`），2026-09-03；−101/+105（5.9%）；完整代码围栏集：—。
- 快照记录：`recvmiXheOIXXi`，`current`，对应手册 token 匹配。
- 清单链接 M：`create-structarray-field.md`×2、`index-structarray-fields.md`×2、`insert-data-into-structarray-fields.md`×2、`struct-array-operators.md`×2；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`create-structarray-field.md`×2、`index-structarray-fields.md`×2、`insert-data-into-structarray-fields.md`×2、`struct-array-operators.md`×2。

### 9. Array Field（`array_data_type`）

- 源：[site/en/userGuide/schema/array_data_type.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/array_data_type.md)。
- Cloud：[guides/tutorials/development/schema/use-array-fields.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-array-fields.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/schema/use-array-fields.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-array-fields.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 缺少每个 VARCHAR array element 的 max_length 按 bytes 计算这一修正。
- 上游最后提交：[c7378f5c6c](https://github.com/milvus-io/milvus-docs/commit/c7378f5c6c0d8b466260d651de90a3a0473c5303)（`c7378f5c6c0d8b466260d651de90a3a0473c5303`），2026-10-26；`--follow` 历史 14 个提交。
- guides 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−908/+3633（33.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, json, python, rust。
- byoc 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−908/+3633（33.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, json, python, rust。
- 快照记录：`recvlPtinkuviw`，`current`，对应手册 token 匹配。
- 清单链接 M：`array-operators.md`×1、`index-explained.md`×1、`nullable-and-default.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`array-operators.md`×1、`nullable-and-default.md`×1。

### 10. Use Partition Key（`use-partition-key`）

- 源：[site/en/userGuide/search-query-get/use-partition-key.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/use-partition-key.md)。
- Cloud：[guides/tutorials/development/search-and-query/use-partition-key.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/use-partition-key.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/search-and-query/use-partition-key.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/use-partition-key.md)；匹配依据：同 slug。
- 漂移：Cloud 缺少 Index Partition Key 及新增的索引创建说明；Partition Key Isolation 的 HNSW 条件措辞也不同。
- 上游最后提交：[71c4bd3415](https://github.com/milvus-io/milvus-docs/commit/71c4bd34150ce80ac37ab01ecbf92cc385385132)（`71c4bd34150ce80ac37ab01ecbf92cc385385132`），2026-10-26；`--follow` 历史 14 个提交。
- guides 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−1034/+1249（32.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust, shell。
- byoc 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−1034/+1249（32.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust, shell。
- 快照记录：`recvlPrgAAOJzT`，`current`，对应手册 token 匹配。
- 清单链接 M：`bitmap.md`×1、`create-collection.md`×1、`inverted.md`×1、`stl-sort.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：—。

### 11. Basic Operators（`basic-operators`）

- 源：[site/en/userGuide/search-query-get/boolean/basic-operators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/basic-operators.md)。
- Cloud：[guides/tutorials/development/search-and-query/filtering/basic-filtering-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/basic-filtering-operators.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/search-and-query/filtering/basic-filtering-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/basic-filtering-operators.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 缺少“算术表达式只能单字段与常量，price * quantity 不支持”的上游修正。
- 上游最后提交：[4e089e1fc1](https://github.com/milvus-io/milvus-docs/commit/4e089e1fc192e8139621950d741f19b8dbdee376)（`4e089e1fc192e8139621950d741f19b8dbdee376`），2026-10-26；`--follow` 历史 8 个提交。
- guides 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−1334/+3640（61.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- byoc 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−1334/+3640（61.4%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, rust。
- 快照记录：`recvlPpnGdYFm8`，`current`，对应手册 token 匹配。
- 清单链接 M：`array_data_type.md`×1、`ngram.md`×1、`pattern-matching.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`array_data_type.md`×1、`default-values.md`×1、`ngram.md`×1、`nullable-and-default.md`×2、`pattern-matching.md`×1、`struct-array-operators.md`×1、`text.md`×1。

### 12. StructArray Operators（`struct-array-operators`）

- 源：[site/en/userGuide/search-query-get/boolean/struct-array-operators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/struct-array-operators.md)。
- Cloud：[guides/tutorials/development/search-and-query/filtering/struct-array-filtering.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/struct-array-filtering.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/search-and-query/filtering/struct-array-filtering.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/struct-array-filtering.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 已有位置访问、ARRAY_CONTAINS/ARRAY_LENGTH 的说明，但没有上游完整的 IS NULL、跨元素与同元素语义边界；不是整段未同步。
- 上游最后提交：[d24c03d010](https://github.com/milvus-io/milvus-docs/commit/d24c03d010da4d0ce393a9f5d0baac0a2ad8c509)（`d24c03d010da4d0ce393a9f5d0baac0a2ad8c509`），2026-10-26；`--follow` 历史 3 个提交。
- guides 最后提交：[68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)（`68fe3930467cee0e791183c138c9d80c1675aa3e`），2026-10-24；−810/+763（37.7%）；完整代码围栏集：json, python。
- byoc 最后提交：[68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)（`68fe3930467cee0e791183c138c9d80c1675aa3e`），2026-10-24；−810/+763（37.7%）；完整代码围栏集：json, python。
- 快照记录：`recvlPpvCPSjHn`，`current`，对应手册 token 匹配。
- 清单链接 M：`basic-vector-search-with-structarray.md`×1、`filtered-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`structarray-limits.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`basic-vector-search-with-structarray.md`×1、`filtered-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`struct-array-operators.md`×10、`structarray-limits.md`×1。

### 13. Phrase Match（`phrase-match`）

- 源：[site/en/userGuide/search-query-get/phrase-match.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/phrase-match.md)。
- Cloud：[guides/tutorials/development/search-and-query/phrase-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/phrase-match.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/search-and-query/phrase-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/phrase-match.md)；匹配依据：同 slug。
- 漂移：Cloud Python max_length 注释仍为 Maximum string length，没有原文新增的 in bytes。
- 上游最后提交：[c7378f5c6c](https://github.com/milvus-io/milvus-docs/commit/c7378f5c6c0d8b466260d651de90a3a0473c5303)（`c7378f5c6c0d8b466260d651de90a3a0473c5303`），2026-10-26；`--follow` 历史 7 个提交。
- guides 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−2620/+6972（55.6%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, shell。
- byoc 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−2620/+6972（55.6%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, python, shell。
- 快照记录：`recvlPqMlqof4j`，`current`，对应手册 token 匹配。
- 清单链接 M：`keyword-match.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：—。

### 14. Snapshots（`snapshots`）

- 源：[site/en/userGuide/search-query-get/snapshots.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/snapshots.md)。
- Cloud：[guides/tutorials/development/snapshots/snapshots.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/snapshots/snapshots.md)；匹配依据：同 slug。
- 漂移：Cloud 仍是去重前的引言；另有 “refer to .” 与未完成的 “Track … and” 句子。仅匹配 Guides，BYOC 没有对应页面。Guides 当前路径最后提交为 08-17，但 --follow 最后给出 07-27（0e4c39287ad6b22c60953bd7c181e9258fe497b5）；本表采用当前路径日期，重命名/历史简化结果不作正文同步证据。
- 上游最后提交：[cb7176658a](https://github.com/milvus-io/milvus-docs/commit/cb7176658a851233d39c8d66343a287c6f0a2b9f)（`cb7176658a851233d39c8d66343a287c6f0a2b9f`），2026-10-23；`--follow` 历史 3 个提交。
- guides 最后提交：[af476aea78](https://github.com/zilliztech/zdoc/commit/af476aea78fad03f8360834d61eff89039601594)（`af476aea78fad03f8360834d61eff89039601594`），2026-08-17；−73/+32（7.6%）；完整代码围栏集：python。
- 快照记录：`recvlPnHgnRg7i`，`current`，对应手册 token 匹配。
- 清单链接 M：`milvus_backup_overview.md`×2、`snapshot-use-cases.md`×1；其中待判 U：`milvus_backup_overview.md`×2、`snapshot-use-cases.md`×1。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：—。

### 15. Create an External Collection（`create-an-external-collection`）

- 源：[site/en/userGuide/collections/create-an-external-collection.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/create-an-external-collection.md)。
- Cloud：[guides/tutorials/development/collection/create-external-collection/create-external-collection.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/create-external-collection/create-external-collection.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/collection/create-external-collection/create-external-collection.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/create-external-collection/create-external-collection.md)；匹配依据：去手册后缀后同标题。
- 漂移：Cloud 已说明 Iceberg metadata.json，但没有同一份 Milvus IAM 部署配置；这部分是产品路径分叉，不能判成纯遗漏。
- 上游最后提交：[e6ce1fd9de](https://github.com/milvus-io/milvus-docs/commit/e6ce1fd9dee3fd44ad67a4716bb4fafc1609e749)（`e6ce1fd9dee3fd44ad67a4716bb4fafc1609e749`），2026-10-22；`--follow` 历史 4 个提交。
- guides 最后提交：[af8a9170ab](https://github.com/zilliztech/zdoc/commit/af8a9170abcfae773e7ebd57669e3b66d244c035)（`af8a9170abcfae773e7ebd57669e3b66d244c035`），2026-10-15；−1548/+2448（44.2%）；完整代码围栏集：bash, c++, go, java, javascript, python, rust。
- byoc 最后提交：[af8a9170ab](https://github.com/zilliztech/zdoc/commit/af8a9170abcfae773e7ebd57669e3b66d244c035)（`af8a9170abcfae773e7ebd57669e3b66d244c035`），2026-10-15；−1548/+2448（44.2%）；完整代码围栏集：bash, c++, go, java, javascript, python, rust。
- 快照记录：`recvlPs65wqwyk`，`current`，对应手册 token 匹配。
- 清单链接 M：`storage-v3.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：—。

### 16. Search with EmbeddingLists: ColBERT and ColPali（`search-with-embedding-lists`）

- 源：[site/en/userGuide/search-query-get/search-with-embedding-lists.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/search-with-embedding-lists.md)。
- Cloud：[guides/tutorials/development/search-and-query/struct-array-search/tutorial-colbert-colpali.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/struct-array-search/tutorial-colbert-colpali.md)；匹配依据：去手册后缀后同标题。
- Cloud：[byoc/tutorials/development/search-and-query/struct-array-search/tutorial-colbert-colpali.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/struct-array-search/tutorial-colbert-colpali.md)；匹配依据：去手册后缀后同标题。
- 漂移：文字/代码最接近；Milvus 最近文件提交为 7 月，不是追赶近期修正的高收益页。
- 上游最后提交：[95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)（`95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84`），2026-07-29；`--follow` 历史 3 个提交。
- guides 最后提交：[437c9308ae](https://github.com/zilliztech/zdoc/commit/437c9308ae84c11115667b936e75b03c68562007)（`437c9308ae84c11115667b936e75b03c68562007`），2026-09-15；−2/+14（0.2%）；完整代码围栏集：python, shell。
- byoc 最后提交：[437c9308ae](https://github.com/zilliztech/zdoc/commit/437c9308ae84c11115667b936e75b03c68562007)（`437c9308ae84c11115667b936e75b03c68562007`），2026-09-15；−2/+14（0.2%）；完整代码围栏集：python, shell。
- 快照记录：`recvmiYb14LJdy`，`current`，对应手册 token 匹配。
- 清单链接 M：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×2、`index-structarray-fields.md`×2、`search-with-embedding-lists.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×2、`index-structarray-fields.md`×2、`metric.md`×1、`search-with-embedding-lists.md`×1。

### 17. Membership Match（`membership-match`）

- 源：[site/en/userGuide/search-query-get/boolean/membership-match.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/membership-match.md)。
- Cloud：[guides/tutorials/development/search-and-query/filtering/membership-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/membership-match.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/search-and-query/filtering/membership-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/membership-match.md)；匹配依据：同 slug。
- 漂移：Cloud 改了选型说明、删去 Milvus Operational limits；不能据较小 diff 认定已完全同步。
- 上游最后提交：[1997ce9678](https://github.com/milvus-io/milvus-docs/commit/1997ce96782b31f8628f22d31fad11007e4b924b)（`1997ce96782b31f8628f22d31fad11007e4b924b`），2026-10-13；`--follow` 历史 1 个提交。
- guides 最后提交：[490244cfb5](https://github.com/zilliztech/zdoc/commit/490244cfb5224548cf2de21825544e989ba9c29e)（`490244cfb5224548cf2de21825544e989ba9c29e`），2026-10-26；−483/+45（11.3%）；完整代码围栏集：go, java, javascript, plaintext, python。
- byoc 最后提交：[490244cfb5](https://github.com/zilliztech/zdoc/commit/490244cfb5224548cf2de21825544e989ba9c29e)（`490244cfb5224548cf2de21825544e989ba9c29e`），2026-10-26；−483/+45（11.3%）；完整代码围栏集：go, java, javascript, plaintext, python。
- 快照记录：`reczz28R4unn2WlF`，`current`，对应手册 token 匹配。
- 清单链接 M：—；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：—。

### 18. Filtered Search（`filtered-search`）

- 源：[site/en/userGuide/search-query-get/filtered-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/filtered-search.md)。
- Cloud：[guides/tutorials/development/search-and-query/filtered-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtered-search.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/search-and-query/filtered-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtered-search.md)；匹配依据：同 slug。
- 漂移：共用正文接近，但 Cloud 新增 SDK 与 CLI；本次没有证据证明 5 月的最后 Milvus 修改仍未反映。
- 上游最后提交：[99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)（`99af73514248e0cf21dbaf1d470b748932131e12`），2026-05-14；`--follow` 历史 11 个提交。
- guides 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−59/+1842（22.0%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, json, python, rust, shell。
- byoc 最后提交：[95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)（`95a7f2ec930334d166bf393e376787c115d5d118`），2026-10-24；−59/+1842（22.0%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, json, python, rust, shell。
- 快照记录：`recvlPp3B7L5Gj`，`current`，对应手册 token 匹配。
- 清单链接 M：—；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`boolean.md`×1。

### 19. Full Text Search（`full-text-search`）

- 源：[site/en/userGuide/search-query-get/full-text-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/full-text-search.md)。
- Cloud：[guides/tutorials/development/search-and-query/full-text-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/full-text-search.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/search-and-query/full-text-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/full-text-search.md)；匹配依据：同 slug。
- 漂移：Cloud 已写 Must set enable_analyzer=True，10-26 的最新补丁并非遗漏；它的生成提交更旧，也不能据日期判落后。
- 上游最后提交：[074a1b3a8c](https://github.com/milvus-io/milvus-docs/commit/074a1b3a8c3e7a8cd4e10ab0c7f2b09009643f42)（`074a1b3a8c3e7a8cd4e10ab0c7f2b09009643f42`），2026-10-26；`--follow` 历史 41 个提交。
- guides 最后提交：[c883fe86ea](https://github.com/zilliztech/zdoc/commit/c883fe86eae118f948887078977af92eb8aaffbf)（`c883fe86eae118f948887078977af92eb8aaffbf`），2026-10-10；−1033/+2122（25.9%）；完整代码围栏集：bash, c++, go, java, javascript, python, rust, shell。
- byoc 最后提交：[c883fe86ea](https://github.com/zilliztech/zdoc/commit/c883fe86eae118f948887078977af92eb8aaffbf)（`c883fe86eae118f948887078977af92eb8aaffbf`），2026-10-10；−1033/+2122（25.9%）；完整代码围栏集：bash, c++, go, java, javascript, python, rust, shell。
- 快照记录：`recvlPqEajVvUb`，`current`，对应手册 token 匹配。
- 清单链接 M：`multi-vector-search.md`×1、`sparse-inverted-index.md`×1、`sparse_vector.md`×2、`text.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`multi-vector-search.md`×1、`sparse_vector.md`×1、`text.md`×1。

### 20. Query（`get-and-scalar-query`）

- 源：[site/en/userGuide/search-query-get/get-and-scalar-query.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/get-and-scalar-query.md)。
- Cloud：[guides/tutorials/development/search-and-query/get-and-scalar-query.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/get-and-scalar-query.md)；匹配依据：同 slug。
- Cloud：[byoc/tutorials/development/search-and-query/get-and-scalar-query.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/get-and-scalar-query.md)；匹配依据：同 slug。
- 漂移：10-26 最新补丁把 Python 的 partitionNames 改为 partition_names；Cloud 两处已正确。Cloud 未写 FLOAT/DOUBLE 的扩展说明是另一处正文差异，不冒充这次补丁遗漏。
- 上游最后提交：[0bde10848a](https://github.com/milvus-io/milvus-docs/commit/0bde10848a76442fee29f2c6f504f274674d63cc)（`0bde10848a76442fee29f2c6f504f274674d63cc`），2026-10-26；`--follow` 历史 31 个提交。
- guides 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−1797/+8919（39.5%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, plaintext, python, rust, shell。
- byoc 最后提交：[60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)（`60907c1fa81be4ddd9289de7093e2270d90a2f24`），2026-10-25；−1797/+8919（39.5%）；完整代码围栏集：bash, c++, csharp, go, java, javascript, plaintext, python, rust, shell。
- 快照记录：`recvlPpiienCU8`，`current`，对应手册 token 匹配。
- 清单链接 M：`basic-operators.md`×1、`random-sampling.md`×1、`timestamptz-field.md`×1；其中待判 U：—。
- 清单链接 C（双手册页 G/B 相同；单手册页仅 G）：`boolean.md`×2、`random-sampling.md`×1、`timestamptz-field.md`×1。

## 其余匹配页：完整初筛账本

下表覆盖剩余 **102** 篇；Delete Entities 另列一行，仅为覆盖核对。每格中的 G/B 路径均指向固定 dev；存在多个标题命中时全部保留。H=Cloud 独有标题候选数，**只是机器预警，不等于独有章节数**；即使 H=0，正文段落/代码仍可能独有。未经逐段人工复核的页面均不进入首批。

为避免巨宽表，每页用三行记录全部输入：第一行路径与日期/差异，第二行命中/语言/图片/通道，第三行 Cloud 独有章节候选及清单链接。

<details><summary>Alter Collection Schema — add-fields-to-an-existing-collection（未逐段复核）</summary>

M：[site/en/userGuide/schema/add-fields-to-an-existing-collection.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/add-fields-to-an-existing-collection.md)；2026-08-05 / [b752e5d162](https://github.com/milvus-io/milvus-docs/commit/b752e5d1625737d0d9bd6aa28c1981ed617243d8)；字面量 `9/0/30/0`；围栏 `plaintext, python`；图 0。

C：[guides/tutorials/development/schema/add-fields-to-an-existing-collection.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/add-fields-to-an-existing-collection.md)（slug）；2026-10-26 / [490244cfb5](https://github.com/zilliztech/zdoc/commit/490244cfb5224548cf2de21825544e989ba9c29e)；−467/+8276（54.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 70；H=7：Add user-defined scalar fields；Add StructArray fields \| PUBLIC；Add user-defined vector fields；Add a Function and its generated vector field \| PUBLIC；Drop user-defined fields \| PUBLIC；Drop a Function and its generated vector field \| PUBLIC；Can I add a BM25 Function and its generated sparse vector field to an existing collection?。

C：[byoc/tutorials/development/schema/add-fields-to-an-existing-collection.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/add-fields-to-an-existing-collection.md)（slug）；2026-10-26 / [490244cfb5](https://github.com/zilliztech/zdoc/commit/490244cfb5224548cf2de21825544e989ba9c29e)；−467/+8276（54.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 70；H=7：Add user-defined scalar fields；Add StructArray fields \| PUBLIC；Add user-defined vector fields；Add a Function and its generated vector field \| PUBLIC；Drop user-defined fields \| PUBLIC；Drop a Function and its generated vector field \| PUBLIC；Can I add a BM25 Function and its generated sparse vector field to an existing collection?。

清单链接 M：`limitations.md`×1、`modify-collection.md`×1、`nullable-and-default.md`×2、`structarray-limits.md`×1；待判 U：`limitations.md`×1。
C（guides/add-fields-to-an-existing-collection）：`array-of-structs.md`×1、`modify-collection.md`×1、`nullable-and-default.md`×2。
C（byoc/add-fields-to-an-existing-collection）：`array-of-structs.md`×1、`modify-collection.md`×1、`nullable-and-default.md`×2。

</details>

<details><summary>Alphanumonly — alphanumonly-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/alphanumonly-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/alphanumonly-filter.md)；2025-07-15 / [eb009dd1b0](https://github.com/milvus-io/milvus-docs/commit/eb009dd1b065b7023825428f62c7b9394bcfaf52)；字面量 `3/1/9/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/alphanumonly-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/alphanumonly-filter.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−63/+1045（43.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-filters/alphanumonly-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/alphanumonly-filter.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−63/+1045（43.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/alphanumonly-filter）：—。
C（byoc/alphanumonly-filter）：—。

</details>

<details><summary>Alter External Collection Schema — alter-external-collection-schema（未逐段复核）</summary>

M：[site/en/userGuide/schema/alter-external-collection-schema.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/alter-external-collection-schema.md)；2026-07-29 / [d3173805f6](https://github.com/milvus-io/milvus-docs/commit/d3173805f6cb180dbce5f306affb675bcf1735e0)；字面量 `2/2/9/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/schema/alter-external-collection-schema.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/alter-external-collection-schema.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−5/+2468（62.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/alter-external-collection-schema.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/alter-external-collection-schema.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−5/+2468（62.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/alter-external-collection-schema）：—。
C（byoc/alter-external-collection-schema）：—。

</details>

<details><summary>Analyzer Overview — analyzer-overview（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/analyzer-overview.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/analyzer-overview.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `4/0/21/0`；围栏 `bash, go, java, javascript, plaintext, python, sql`；图 1。

C：[guides/tutorials/development/analyzer/analyzer-overview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-overview.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−714/+4788（37.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust, sql`；图 1；新增语言块 33；H=2：Step 3: Add analyzer to schema field；Example use on the Zilliz Cloud console。

C：[byoc/tutorials/development/analyzer/analyzer-overview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-overview.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−714/+4788（37.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust, sql`；图 1；新增语言块 33；H=2：Step 3: Add analyzer to schema field；Example use on the Zilliz Cloud console。

清单链接 M：`keyword-match.md`×2；待判 U：—。
C（guides/analyzer-overview）：`keyword-match.md`×2。
C（byoc/analyzer-overview）：`keyword-match.md`×2。

</details>

<details><summary>Arabic — arabic-analyzer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/analyzer/arabic-analyzer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/analyzer/arabic-analyzer.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/4/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/analyzer/built-in-analyzer/arabic-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/built-in-analyzer/arabic-analyzer.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1/+1999（65.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 35；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/built-in-analyzer/arabic-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/built-in-analyzer/arabic-analyzer.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1/+1999（65.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 35；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/arabic-analyzer）：—。
C（byoc/arabic-analyzer）：—。

</details>

<details><summary>Arabic Normalization — arabic-normalization-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/arabic-normalization-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/arabic-normalization-filter.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/0/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/arabic-normalization.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/arabic-normalization.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1/+1526（69.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-filters/arabic-normalization.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/arabic-normalization.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1/+1526（69.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/arabic-normalization）：—。
C（byoc/arabic-normalization）：—。

</details>

<details><summary>ARRAY Operators — array-operators（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/boolean/array-operators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/array-operators.md)；2026-07-29 / [e17315d537](https://github.com/milvus-io/milvus-docs/commit/e17315d53777c730ae71110abd5bfc1aee3cd847)；字面量 `2/2/9/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/filtering/array-filtering-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/array-filtering-operators.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−86/+1810（51.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 42；H=2：ARRAY_APPEND；ARRAY_REMOVE。

C：[byoc/tutorials/development/search-and-query/filtering/array-filtering-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/array-filtering-operators.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−86/+1810（51.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 42；H=2：ARRAY_APPEND；ARRAY_REMOVE。

清单链接 M：`array-operators.md`×6；待判 U：—。
C（guides/array-filtering-operators）：`array-operators.md`×6。
C（byoc/array-filtering-operators）：`array-operators.md`×6。

</details>

<details><summary>ASCII folding — ascii-folding-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/ascii-folding-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/ascii-folding-filter.md)；2025-07-15 / [eb009dd1b0](https://github.com/milvus-io/milvus-docs/commit/eb009dd1b065b7023825428f62c7b9394bcfaf52)；字面量 `3/1/5/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/ascii-folding-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/ascii-folding-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−62/+927（40.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-filters/ascii-folding-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/ascii-folding-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−62/+927（40.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/ascii-folding-filter）：—。
C（byoc/ascii-folding-filter）：—。

</details>

<details><summary>Basic Vector Search with StructArray — basic-vector-search-with-structarray（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/basic-vector-search-with-structarray.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/basic-vector-search-with-structarray.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/1/1/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/struct-array-search/search-with-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/struct-array-search/search-with-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−24/+3243（56.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 14；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/struct-array-search/search-with-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/struct-array-search/search-with-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−24/+3243（56.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 14；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`create-structarray-field.md`×2、`filtered-search-with-structarray.md`×1、`grouping-search-with-structarray.md`×1、`hybrid-search-with-structarray.md`×1、`index-structarray-fields.md`×2、`insert-data-into-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`search-with-embedding-lists.md`×1、`structarray-limits.md`×1；待判 U：—。
C（guides/search-with-struct-array）：`create-structarray-field.md`×2、`filtered-search-with-structarray.md`×1、`grouping-search-with-structarray.md`×1、`hybrid-search-with-structarray.md`×1、`index-structarray-fields.md`×2、`insert-data-into-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`search-with-embedding-lists.md`×1、`structarray-limits.md`×1。
C（byoc/search-with-struct-array）：`create-structarray-field.md`×2、`filtered-search-with-structarray.md`×1、`grouping-search-with-structarray.md`×1、`hybrid-search-with-structarray.md`×1、`index-structarray-fields.md`×2、`insert-data-into-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`search-with-embedding-lists.md`×1、`structarray-limits.md`×1。

</details>

<details><summary>Data Model Design with an Array of Structs — best-practices-for-array-of-structs（未逐段复核）</summary>

M：[site/en/userGuide/schema/best-practices-for-array-of-structs.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/best-practices-for-array-of-structs.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/0/5/0`；围栏 `python`；图 1。

C：[guides/tutorials/development/schema/schema-best-practices/schema-design-with-structs.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/schema-best-practices/schema-design-with-structs.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−56/+11577（61.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 42；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/schema-best-practices/schema-design-with-structs.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/schema-best-practices/schema-design-with-structs.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−56/+11577（61.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 42；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`array-of-structs.md`×1、`schema-hands-on.md`×1；待判 U：—。
C（guides/schema-design-with-structs）：`array-of-structs.md`×1、`schema-hands-on.md`×1。
C（byoc/schema-design-with-structs）：`array-of-structs.md`×1、`schema-hands-on.md`×1。

</details>

<details><summary>Binary Vector — binary-vector（未逐段复核）</summary>

M：[site/en/userGuide/schema/binary-vector.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/binary-vector.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `5/0/6/0`；围栏 `bash, go, java, javascript, python`；图 2。

C：[guides/tutorials/development/schema/use-binary-vector.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-binary-vector.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−664/+2546（34.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 2；新增语言块 15；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/use-binary-vector.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-binary-vector.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−664/+2546（34.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 2；新增语言块 15；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`dense-vector.md`×1、`index-explained.md`×1、`metric.md`×1、`sparse_vector.md`×1；待判 U：—。
C（guides/use-binary-vector）：`dense-vector.md`×1、`metric.md`×1、`sparse_vector.md`×1。
C（byoc/use-binary-vector）：`dense-vector.md`×1、`metric.md`×1、`sparse_vector.md`×1。

</details>

<details><summary>BITMAP — bitmap（未逐段复核）</summary>

M：[site/en/userGuide/indexes/scalar/bitmap.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/indexes/scalar/bitmap.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/0/1/0`；围栏 `python`；图 1。

C：[guides/tutorials/development/scalar-index/bitmap-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/scalar-index/bitmap-index-type.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−69/+1388（44.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 14；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/scalar-index/bitmap-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/scalar-index/bitmap-index-type.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−69/+1388（44.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 14；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`boolean.md`×1；待判 U：—。
C（guides/bitmap-index-type）：`boolean.md`×1。
C（byoc/bitmap-index-type）：`boolean.md`×1。

</details>

<details><summary>BM25 Function — bm25-function（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/embedding-function/bm25-function.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/embedding-function/bm25-function.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `4/4/14/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/function/bm25-function.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/bm25-function.md)（slug）；2026-10-10 / [c883fe86ea](https://github.com/zilliztech/zdoc/commit/c883fe86eae118f948887078977af92eb8aaffbf)；−47/+1711（19.1%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust, shell`，围栏 `bash, c++, go, java, javascript, plaintext, python, rust, shell`；图 0；新增语言块 18；H=2：Via SDK；Via web console。

C：[byoc/tutorials/development/function/bm25-function.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/bm25-function.md)（slug）；2026-10-10 / [c883fe86ea](https://github.com/zilliztech/zdoc/commit/c883fe86eae118f948887078977af92eb8aaffbf)；−47/+1711（19.1%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust, shell`，围栏 `bash, c++, go, java, javascript, plaintext, python, rust, shell`；图 0；新增语言块 18；H=2：Via SDK；Via web console。

清单链接 M：—；待判 U：—。
C（guides/bm25-function）：—。
C（byoc/bm25-function）：—。

</details>

<details><summary>Filtering Explained — boolean（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/boolean/boolean.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/boolean.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `0/0/12/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/filtering/filtering-overview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/filtering-overview.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−46/+2653（50.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 98；H=1：`PHRASE_MATCH` operator。

C：[byoc/tutorials/development/search-and-query/filtering/filtering-overview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/filtering-overview.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−46/+2653（50.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 98；H=1：`PHRASE_MATCH` operator。

清单链接 M：`array-operators.md`×1、`basic-operators.md`×3、`json-operators.md`×1、`keyword-match.md`×1、`pattern-matching.md`×3；待判 U：—。
C（guides/filtering-overview）：`array-operators.md`×1、`basic-operators.md`×3、`json-operators.md`×1、`pattern-matching.md`×3。
C（byoc/filtering-overview）：`array-operators.md`×1、`basic-operators.md`×3、`json-operators.md`×1、`pattern-matching.md`×3。

</details>

<details><summary>Boost Ranker — boost-ranker（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/boost-ranker.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/boost-ranker.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `3/3/12/0`；围栏 `bash, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/function/reranking-functions/rule-based-rerankers/boost-ranker.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/rule-based-rerankers/boost-ranker.md)（slug）；2026-10-10 / [6d7d8be206](https://github.com/zilliztech/zdoc/commit/6d7d8be206a8e173cd3d45e239f5a8c470a8402a)；−61/+2428（28.7%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/boost-ranker.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/boost-ranker.md)（slug）；2026-10-10 / [6d7d8be206](https://github.com/zilliztech/zdoc/commit/6d7d8be206a8e173cd3d45e239f5a8c470a8402a)；−61/+2428（28.7%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`boolean.md`×1；待判 U：—。
C（guides/boost-ranker）：`boolean.md`×1。
C（byoc/boost-ranker）：`boolean.md`×1。

</details>

<details><summary>Chinese — chinese-analyzer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/analyzer/chinese-analyzer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/analyzer/chinese-analyzer.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `3/1/6/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/built-in-analyzer/chinese-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/built-in-analyzer/chinese-analyzer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−77/+877（38.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 12；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/built-in-analyzer/chinese-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/built-in-analyzer/chinese-analyzer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−77/+877（38.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 12；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/chinese-analyzer）：—。
C（byoc/chinese-analyzer）：—。

</details>

<details><summary>Choose the Right Analyzer for Your Use Case — choose-the-right-analyzer-for-your-use-case（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/choose-the-right-analyzer-for-your-use-case.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/choose-the-right-analyzer-for-your-use-case.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `0/0/8/0`；围栏 `json, plaintext, python`；图 1。

C：[guides/tutorials/development/analyzer/choose-the-right-analyzer-for-your-use-case.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/choose-the-right-analyzer-for-your-use-case.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−918/+2872（39.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust`；图 1；新增语言块 28；H=20：Quick concept: How analyzers work；Step 1: Do you need to choose an analyzer?；Step 2: Check if the standard analyzer meets your needs；Step 3: Choose your path；Quick recipes by use case；English；Arabic；Bengali；French；German；Hindi；Korean；Japanese；Portuguese；Russian；Spanish；Swahili；Turkish；Urdu；Configure and preview analyzers in Zilliz Cloud。

C：[byoc/tutorials/development/analyzer/choose-the-right-analyzer-for-your-use-case.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/choose-the-right-analyzer-for-your-use-case.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−918/+2872（39.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust`；图 1；新增语言块 28；H=20：Quick concept: How analyzers work；Step 1: Do you need to choose an analyzer?；Step 2: Check if the standard analyzer meets your needs；Step 3: Choose your path；Quick recipes by use case；English；Arabic；Bengali；French；German；Hindi；Korean；Japanese；Portuguese；Russian；Spanish；Swahili；Turkish；Urdu；Configure and preview analyzers in Zilliz Cloud。

清单链接 M：`keyword-match.md`×3、`language-identifier.md`×4、`removepunct-filter.md`×1；待判 U：—。
C（guides/choose-the-right-analyzer-for-your-use-case）：`keyword-match.md`×2、`language-identifier.md`×4、`removepunct-filter.md`×1。
C（byoc/choose-the-right-analyzer-for-your-use-case）：`keyword-match.md`×2、`language-identifier.md`×4、`removepunct-filter.md`×1。

</details>

<details><summary>Cnalphanumonly — cnalphanumonly-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/cnalphanumonly-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/cnalphanumonly-filter.md)；2025-07-15 / [eb009dd1b0](https://github.com/milvus-io/milvus-docs/commit/eb009dd1b065b7023825428f62c7b9394bcfaf52)；字面量 `3/1/9/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/cnalphanumonly-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/cnalphanumonly-filter.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−67/+937（40.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-filters/cnalphanumonly-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/cnalphanumonly-filter.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−67/+937（40.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/cnalphanumonly-filter）：—。
C（byoc/cnalphanumonly-filter）：—。

</details>

<details><summary>Cncharonly — cncharonly-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/cncharonly-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/cncharonly-filter.md)；2025-07-15 / [eb009dd1b0](https://github.com/milvus-io/milvus-docs/commit/eb009dd1b065b7023825428f62c7b9394bcfaf52)；字面量 `3/1/8/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/cncharonly-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/cncharonly-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−45/+947（39.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-filters/cncharonly-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/cncharonly-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−45/+947（39.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/cncharonly-filter）：—。
C（byoc/cncharonly-filter）：—。

</details>

<details><summary>Cohere — cohere（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/embedding-function/cohere.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/embedding-function/cohere.md)；2025-09-18 / [3a9f46f9cf](https://github.com/milvus-io/milvus-docs/commit/3a9f46f9cf5a702346da327e2b26e47de075fbd5)；字面量 `1/0/16/6`；围栏 `python, yaml`；图 0。

C：[guides/tutorials/development/function/text-embedding-funcs/cohere.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/text-embedding-funcs/cohere.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−520/+4856（76.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 42；H=9：Model choices；Before you start；Step 1: Create a collection with a text embedding function；Define schema fields；Define the text embedding function；Configure the index；Create the collection；Step 2: Insert data；Step 3: Search with text。

清单链接 M：`configure-docker.md`×1、`embedding-function-overview.md`×1；待判 U：`embedding-function-overview.md`×1。
C（guides/cohere）：—。

</details>

<details><summary>Cohere Ranker — cohere-ranker（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/cohere-ranker.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/cohere-ranker.md)；2026-01-14 / [a43bd1aaff](https://github.com/milvus-io/milvus-docs/commit/a43bd1aaff56abf0d4b02e79698bf0ad50ca97f1)；字面量 `3/0/6/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/function/reranking-functions/model-based-rerankers/cohere-model-ranker.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/model-based-rerankers/cohere-model-ranker.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−653/+6432（89.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=6：Before you start；Use Cohere Ranker；Preparations；Define the rerank function；Search with the rerank function；Next steps。

清单链接 M：`cohere-ranker.md`×1、`model-ranker-overview.md`×1；待判 U：`model-ranker-overview.md`×1。
C（guides/cohere-model-ranker）：`multi-vector-search.md`×1。

</details>

<details><summary>Create a StructArray Field — create-structarray-field（未逐段复核）</summary>

M：[site/en/userGuide/schema/create-structarray-field.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/create-structarray-field.md)；2026-08-11 / [1a8032447c](https://github.com/milvus-io/milvus-docs/commit/1a8032447c7621d4ff1d05eddae116de2127df95)；字面量 `1/1/4/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/schema/struct-array/create-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/struct-array/create-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−12/+7106（61.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/struct-array/create-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/struct-array/create-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−12/+7106（61.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`basic-vector-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`insert-data-into-structarray-fields.md`×1、`structarray-limits.md`×3；待判 U：—。
C（guides/create-struct-array）：`basic-vector-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`insert-data-into-structarray-fields.md`×1、`structarray-limits.md`×3。
C（byoc/create-struct-array）：`basic-vector-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`insert-data-into-structarray-fields.md`×1、`structarray-limits.md`×3。

</details>

<details><summary>Decay Ranker Overview — decay-ranker-overview（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/decay-ranker-overview.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/decay-ranker-overview.md)；2026-01-14 / [a43bd1aaff](https://github.com/milvus-io/milvus-docs/commit/a43bd1aaff56abf0d4b02e79698bf0ad50ca97f1)；字面量 `0/0/9/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/decay-ranker-oveview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/decay-ranker-oveview.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−13/+1112（19.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/decay-ranker-oveview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/decay-ranker-oveview.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−13/+1112（19.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`decay-ranker-overview.md`×2、`tutorial-implement-a-time-based-ranking-in-milvus.md`×1；待判 U：—。
C（guides/decay-ranker-oveview）：`decay-ranker-overview.md`×2、`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。
C（byoc/decay-ranker-oveview）：`decay-ranker-overview.md`×2、`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。

</details>

<details><summary>Decompounder — decompounder-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/decompounder-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/decompounder-filter.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `4/1/6/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/decompounder-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/decompounder-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−461/+1358（43.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-filters/decompounder-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/decompounder-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−461/+1358（43.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`manage-file-resources.md`×2；待判 U：`manage-file-resources.md`×2。
C（guides/decompounder-filter）：—。
C（byoc/decompounder-filter）：—。

</details>

<details><summary>Default Values — default-values（未逐段复核）</summary>

M：[site/en/userGuide/schema/default-values.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/default-values.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/0/5/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/schema/default-fields.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/default-fields.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−17/+8549（76.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/default-fields.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/default-fields.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−17/+8549（76.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/default-fields）：—。
C（byoc/default-fields）：—。

</details>

<details><summary>Delete Entities — delete-entities（已完成试点，排除）</summary>

M：[site/en/userGuide/insert-and-delete/delete-entities.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/insert-and-delete/delete-entities.md)；2026-10-26 / [114bf75950](https://github.com/milvus-io/milvus-docs/commit/114bf75950044fc1466b78ce2bd9e9af436deebd)；字面量 `0/0/8/0`；围栏 `bash, cpp, csharp, go, java, javascript, python, rust`；图 0。

C：[guides/tutorials/development/insert-and-delete/delete-entities.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/insert-and-delete/delete-entities.md)（slug）；2026-10-26 / [d151bc9e76](https://github.com/zilliztech/zdoc/commit/d151bc9e76693eaed00552e12d17b23bd4c1d10f)；−134/+26（3.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 0；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/insert-and-delete/delete-entities.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/insert-and-delete/delete-entities.md)（slug）；2026-10-26 / [d151bc9e76](https://github.com/zilliztech/zdoc/commit/d151bc9e76693eaed00552e12d17b23bd4c1d10f)；−134/+26（3.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 0；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`boolean.md`×1；待判 U：—。
C（guides/delete-entities）：`boolean.md`×1。
C（byoc/delete-entities）：`boolean.md`×1。

</details>

<details><summary>Dense Vector — dense-vector（未逐段复核）</summary>

M：[site/en/userGuide/schema/dense-vector.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/dense-vector.md)；2026-08-25 / [bb4425c33d](https://github.com/milvus-io/milvus-docs/commit/bb4425c33df6ebd6e6c4c9d87371f71f9813f058)；字面量 `5/0/10/0`；围栏 `bash, go, java, javascript, json, python`；图 2。

C：[guides/tutorials/development/schema/use-dense-vector.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-dense-vector.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−479/+2378（31.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 2；新增语言块 15；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/use-dense-vector.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-dense-vector.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−479/+2378（31.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 2；新增语言块 15；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`binary-vector.md`×1、`index-explained.md`×1、`metric.md`×1、`sparse_vector.md`×1；待判 U：—。
C（guides/use-dense-vector）：`binary-vector.md`×1、`metric.md`×1、`sparse_vector.md`×1。
C（byoc/use-dense-vector）：`binary-vector.md`×1、`metric.md`×1、`sparse_vector.md`×1。

</details>

<details><summary>Drop Collection — drop-collection（未逐段复核）</summary>

M：[site/en/userGuide/collections/drop-collection.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/drop-collection.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `4/5/6/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/collection/drop-collection.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/drop-collection.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−82/+380（37.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 3；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/collection/drop-collection.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/drop-collection.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−82/+351（36.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 3；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/drop-collection）：—。
C（byoc/drop-collection）：—。

</details>

<details><summary>Elasticsearch Queries to Milvus — elasticsearch-queries-to-milvus（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/elasticsearch-queries-to-milvus.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/elasticsearch-queries-to-milvus.md)；2025-12-31 / [e9f6c95e22](https://github.com/milvus-io/milvus-docs/commit/e9f6c95e229a4ad8c4a6f4d749c039ba99ab678b)；字面量 `0/0/37/0`；围栏 `bash, python`；图 0。

C：[guides/tutorials/development/search-and-query/elasticsearch-queries-to-milvus.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/elasticsearch-queries-to-milvus.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−29/+7315（55.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 60；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/elasticsearch-queries-to-milvus.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/elasticsearch-queries-to-milvus.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−29/+7315（55.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 60；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`basic-operators.md`×6、`weighted-ranker.md`×1；待判 U：—。
C（guides/elasticsearch-queries-to-milvus）：`basic-operators.md`×7、`boolean.md`×1、`index-explained.md`×1、`weighted-ranker.md`×1。
C（byoc/elasticsearch-queries-to-milvus）：`basic-operators.md`×7、`boolean.md`×1、`index-explained.md`×1、`weighted-ranker.md`×1。

</details>

<details><summary>Dynamic Field — enable-dynamic-field（未逐段复核）</summary>

M：[site/en/userGuide/schema/enable-dynamic-field.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/enable-dynamic-field.md)；2026-07-29 / [d3173805f6](https://github.com/milvus-io/milvus-docs/commit/d3173805f6cb180dbce5f306affb675bcf1735e0)；字面量 `7/3/15/0`；围栏 `bash, go, java, javascript, json, python`；图 0。

C：[guides/tutorials/development/schema/enable-dynamic-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/enable-dynamic-field.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−664/+4878（32.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 0；新增语言块 21；H=2：Index keys in the dynamic field；Use JSON cast functions for type conversion。

C：[byoc/tutorials/development/schema/enable-dynamic-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/enable-dynamic-field.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−664/+4878（32.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 0；新增语言块 21；H=2：Index keys in the dynamic field；Use JSON cast functions for type conversion。

清单链接 M：`create-collection.md`×1、`json-operators.md`×1、`load-and-release.md`×1、`modify-collection.md`×1、`use-json-fields.md`×2；待判 U：—。
C（guides/enable-dynamic-field）：`json-operators.md`×1、`load-and-release.md`×1、`modify-collection.md`×1、`use-json-fields.md`×2。
C（byoc/enable-dynamic-field）：`json-operators.md`×1、`load-and-release.md`×1、`modify-collection.md`×1、`use-json-fields.md`×2。

</details>

<details><summary>English — english-analyzer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/analyzer/english-analyzer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/analyzer/english-analyzer.md)；2025-07-15 / [eb009dd1b0](https://github.com/milvus-io/milvus-docs/commit/eb009dd1b065b7023825428f62c7b9394bcfaf52)；字面量 `3/1/7/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/built-in-analyzer/english-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/built-in-analyzer/english-analyzer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−122/+1508（38.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 15；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/built-in-analyzer/english-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/built-in-analyzer/english-analyzer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−122/+1508（38.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 15；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/english-analyzer）：—。
C（byoc/english-analyzer）：—。

</details>

<details><summary>Exponential Decay — exponential-decay（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/exponential-decay.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/exponential-decay.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/0/1/0`；围栏 `bash, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/exponential-decay.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/exponential-decay.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−30/+1763（36.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/exponential-decay.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/exponential-decay.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−30/+1763（36.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1；待判 U：—。
C（guides/exponential-decay）：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。
C（byoc/exponential-decay）：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。

</details>

<details><summary>Filter Templating — filtering-templating（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/boolean/filtering-templating.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/filtering-templating.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `0/0/9/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/filtering/filtering-templating.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/filtering-templating.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−15/+4659（74.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 42；H=1：Regex filter templates。

C：[byoc/tutorials/development/search-and-query/filtering/filtering-templating.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/filtering-templating.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−15/+4659（74.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 42；H=1：Regex filter templates。

清单链接 M：—；待判 U：—。
C（guides/filtering-templating）：`struct-array-operators.md`×1。
C（byoc/filtering-templating）：`struct-array-operators.md`×1。

</details>

<details><summary>Gaussian Decay — gaussian-decay（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/gaussian-decay.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/gaussian-decay.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `0/0/2/0`；围栏 `bash, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/gaussian-decay.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/gaussian-decay.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−25/+1373（33.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/gaussian-decay.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/gaussian-decay.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−25/+1373（33.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1；待判 U：—。
C（guides/gaussian-decay）：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。
C（byoc/gaussian-decay）：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。

</details>

<details><summary>Geometry Field — geometry-field（未逐段复核）</summary>

M：[site/en/userGuide/schema/geometry-field.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/geometry-field.md)；2025-11-05 / [e37516e5e4](https://github.com/milvus-io/milvus-docs/commit/e37516e5e4172c29e3d35669c0eee75f65d3f253)；字面量 `3/1/4/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/schema/use-geometry-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-geometry-field.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−403/+8902（52.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/use-geometry-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-geometry-field.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−403/+8902（52.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`nullable-and-default.md`×2、`rtree.md`×1；待判 U：—。
C（guides/use-geometry-field）：`mmap.md`×1、`nullable-and-default.md`×2、`rtree.md`×1。
C（byoc/use-geometry-field）：`mmap.md`×1、`nullable-and-default.md`×2、`rtree.md`×1。

</details>

<details><summary>Geometry Operators — geometry-operators（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/boolean/geometry-operators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/geometry-operators.md)；2025-11-05 / [e37516e5e4](https://github.com/milvus-io/milvus-docs/commit/e37516e5e4172c29e3d35669c0eee75f65d3f253)；字面量 `0/0/3/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/filtering/geometry-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/geometry-operators.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−1/+2218（42.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 56；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/filtering/geometry-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/geometry-operators.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−1/+2218（42.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 56；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`geometry-field.md`×2；待判 U：—。
C（guides/geometry-operators）：`geometry-field.md`×2。
C（byoc/geometry-operators）：`geometry-field.md`×2。

</details>

<details><summary>Grouping Search — grouping-search（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/grouping-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/grouping-search.md)；2026-09-09 / [126c1f872c](https://github.com/milvus-io/milvus-docs/commit/126c1f872c683b91b146e4afaebde7c5c904034c)；字面量 `9/7/18/0`；围栏 `bash, cpp, go, java, javascript, python`；图 2。

C：[guides/tutorials/development/search-and-query/grouping-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/grouping-search.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1036/+1784（24.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, shell`；图 2；新增语言块 6；H=1：Order groups by a scalar field \| PUBLIC。

C：[byoc/tutorials/development/search-and-query/grouping-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/grouping-search.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1036/+1784（24.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, shell`；图 2；新增语言块 6；H=1：Order groups by a scalar field \| PUBLIC。

清单链接 M：—；待判 U：—。
C（guides/grouping-search）：—。
C（byoc/grouping-search）：—。

</details>

<details><summary>Grouping Search with StructArray — grouping-search-with-structarray（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/grouping-search-with-structarray.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/grouping-search-with-structarray.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/1/1/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/struct-array-search/grouping-search-with-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/struct-array-search/grouping-search-with-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−4/+5428（65.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/struct-array-search/grouping-search-with-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/struct-array-search/grouping-search-with-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−4/+5428（65.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`basic-vector-search-with-structarray.md`×2、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`structarray-limits.md`×1；待判 U：—。
C（guides/grouping-search-with-struct-array）：`basic-vector-search-with-structarray.md`×2、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`structarray-limits.md`×1。
C（byoc/grouping-search-with-struct-array）：`basic-vector-search-with-structarray.md`×2、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`structarray-limits.md`×1。

</details>

<details><summary>Hugging Face — hugging-face（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/embedding-function/hugging-face.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/embedding-function/hugging-face.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/21/5`；围栏 `python, text, yaml`；图 1。

C：[guides/tutorials/development/function/text-embedding-funcs/hugging-face.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/text-embedding-funcs/hugging-face.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−808/+5246（78.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 42；H=9：Model compatibility；Define schema fields；Define the text embedding function；Configure the index；Create the collection；Step 2: Insert data；Step 3: Search with text；The model is unavailable for the feature-extraction task；The returned vector dimension does not match the schema。

清单链接 M：`configure-docker.md`×1、`embedding-function-overview.md`×1、`hugging-face-tei.md`×1；待判 U：`embedding-function-overview.md`×1、`hugging-face-tei.md`×1。
C（guides/hugging-face）：—。

</details>

<details><summary>Hugging Face Ranker — hugging-face-ranker（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/hugging-face-ranker.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/hugging-face-ranker.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/13/6`；围栏 `python, text, yaml`；图 2。

C：[guides/tutorials/development/function/reranking-functions/model-based-rerankers/hugging-face-ranker.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/model-based-rerankers/hugging-face-ranker.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−692/+5953（75.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 2；新增语言块 21；H=5：Preparations；Define the rerank function；Search with the rerank function；The model is unavailable for the sentence-similarity task；The number of query texts does not match the search request。

清单链接 M：`model-ranker-overview.md`×1、`multi-vector-search.md`×1、`tei-ranker.md`×1；待判 U：`model-ranker-overview.md`×1、`tei-ranker.md`×1。
C（guides/hugging-face-ranker）：`multi-vector-search.md`×1。

</details>

<details><summary>Hybrid Search with StructArray — hybrid-search-with-structarray（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/hybrid-search-with-structarray.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/hybrid-search-with-structarray.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/1/1/0`；围栏 `—`；图 0。

C：[guides/tutorials/development/search-and-query/struct-array-search/hybrid-search-with-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/struct-array-search/hybrid-search-with-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−2/+6399（60.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 24；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/struct-array-search/hybrid-search-with-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/struct-array-search/hybrid-search-with-struct-array.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−2/+6399（60.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 24；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`grouping-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`structarray-limits.md`×1；待判 U：—。
C（guides/hybrid-search-with-struct-array）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`grouping-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`structarray-limits.md`×1。
C（byoc/hybrid-search-with-struct-array）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`grouping-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`range-search-with-structarray.md`×1、`structarray-limits.md`×1。

</details>

<details><summary>ICU — icu-tokenizer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/tokenizer/icu-tokenizer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/tokenizer/icu-tokenizer.md)；2025-07-16 / [d41442d2f9](https://github.com/milvus-io/milvus-docs/commit/d41442d2f90cf91fa2b67bdfad1faa0d58c66c9d)；字面量 `3/1/2/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/icu-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/icu-tokenizer.md)（slug）；2026-10-15 / [f7efb1e7cb](https://github.com/zilliztech/zdoc/commit/f7efb1e7cbd5f9ba0144bd8c08a03646bf479673)；−41/+731（33.4%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 8；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/icu-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/icu-tokenizer.md)（slug）；2026-10-15 / [f7efb1e7cb](https://github.com/zilliztech/zdoc/commit/f7efb1e7cbd5f9ba0144bd8c08a03646bf479673)；−41/+731（33.4%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 8；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`removepunct-filter.md`×2；待判 U：—。
C（guides/icu-tokenizer）：`removepunct-filter.md`×2。
C（byoc/icu-tokenizer）：`removepunct-filter.md`×2。

</details>

<details><summary>Import Data — import-data（未逐段复核）</summary>

M：[site/en/userGuide/data-import/import-data.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/data-import/import-data.md)；2026-10-26 / [d31ca16c69](https://github.com/milvus-io/milvus-docs/commit/d31ca16c69bbe0141da424682231455d9a302f6f)；字面量 `6/0/6/0`；围栏 `java, json, python, shell`；图 0。

C：[guides/tutorials/development/data-import/import-data/import-data.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/data-import/import-data/import-data.md)（slug）；2026-07-27 / [0e4c39287a](https://github.com/zilliztech/zdoc/commit/0e4c39287ad6b22c60953bd7c181e9258fe497b5)；−2265/+23（98.5%）；Channel `current`；Tab `—`，围栏 `—`；图 0；新增语言块 0；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/data-import/import-data/import-data.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/data-import/import-data/import-data.md)（slug）；2026-07-27 / [0e4c39287a](https://github.com/zilliztech/zdoc/commit/0e4c39287ad6b22c60953bd7c181e9258fe497b5)；−2265/+23（98.5%）；Channel `current`；Tab `—`，围栏 `—`；图 0；新增语言块 0；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`idempotent-import.md`×1、`prepare-source-data.md`×1；待判 U：`idempotent-import.md`×1、`prepare-source-data.md`×1。
C（guides/import-data）：—。
C（byoc/import-data）：—。
歧义：同 slug 命中 Cloud 导航容器/DocCardList，正文仅很少 token，不是 Milvus 导入教程的等价内容；不把约 98% 差异当作最高迁移收益。

</details>

<details><summary>Index StructArray Fields — index-structarray-fields（未逐段复核）</summary>

M：[site/en/userGuide/schema/index-structarray-fields.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/index-structarray-fields.md)；2026-08-11 / [1a8032447c](https://github.com/milvus-io/milvus-docs/commit/1a8032447c7621d4ff1d05eddae116de2127df95)；字面量 `1/1/2/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/schema/struct-array/index-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/struct-array/index-struct-array.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−234/+3305（60.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 28；H=1：Applicable metric types。

C：[byoc/tutorials/development/schema/struct-array/index-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/struct-array/index-struct-array.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−234/+3305（60.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 28；H=1：Applicable metric types。

清单链接 M：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`structarray-limits.md`×2；待判 U：—。
C（guides/index-struct-array）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`structarray-limits.md`×2。
C（byoc/index-struct-array）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×1、`structarray-limits.md`×2。

</details>

<details><summary>Insert Data into StructArray Fields — insert-data-into-structarray-fields（未逐段复核）</summary>

M：[site/en/userGuide/schema/insert-data-into-structarray-fields.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/insert-data-into-structarray-fields.md)；2026-08-11 / [1a8032447c](https://github.com/milvus-io/milvus-docs/commit/1a8032447c7621d4ff1d05eddae116de2127df95)；字面量 `1/1/2/0`；围栏 `json, python`；图 0。

C：[guides/tutorials/development/schema/struct-array/insert-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/struct-array/insert-struct-array.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−3/+7616（65.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/struct-array/insert-struct-array.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/struct-array/insert-struct-array.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−3/+7616（65.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`index-structarray-fields.md`×1、`structarray-limits.md`×1；待判 U：—。
C（guides/insert-struct-array）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`index-structarray-fields.md`×1、`structarray-limits.md`×1。
C（byoc/insert-struct-array）：`basic-vector-search-with-structarray.md`×1、`create-structarray-field.md`×1、`index-structarray-fields.md`×1、`structarray-limits.md`×1。

</details>

<details><summary>Insert Entities — insert-update-delete（未逐段复核）</summary>

M：[site/en/userGuide/insert-and-delete/insert-update-delete.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/insert-and-delete/insert-update-delete.md)；2026-07-29 / [d3173805f6](https://github.com/milvus-io/milvus-docs/commit/d3173805f6cb180dbce5f306affb675bcf1735e0)；字面量 `6/5/8/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/insert-and-delete/insert-entities.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/insert-and-delete/insert-entities.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−776/+4567（34.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/insert-and-delete/insert-entities.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/insert-and-delete/insert-entities.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−776/+4567（34.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/insert-entities）：—。
C（byoc/insert-entities）：—。

</details>

<details><summary>INVERTED — inverted（未逐段复核）</summary>

M：[site/en/userGuide/indexes/scalar/inverted.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/indexes/scalar/inverted.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/0/5/0`；围栏 `python`；图 1。

C：[guides/tutorials/development/scalar-index/inverted-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/scalar-index/inverted-index-type.md)（title）；2026-10-14 / [fe7b4dfcd3](https://github.com/zilliztech/zdoc/commit/fe7b4dfcd3dc8993b5db77e80b7e8b49e6acac06)；−36/+2423（60.0%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 1；新增语言块 30；H=1：Create indexes on JSON fields。

C：[byoc/tutorials/development/scalar-index/inverted-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/scalar-index/inverted-index-type.md)（title）；2026-10-14 / [fe7b4dfcd3](https://github.com/zilliztech/zdoc/commit/fe7b4dfcd3dc8993b5db77e80b7e8b49e6acac06)；−36/+2423（60.0%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 1；新增语言块 30；H=1：Create indexes on JSON fields。

清单链接 M：`index-explained.md`×1；待判 U：—。
C（guides/inverted-index-type）：—。
C（byoc/inverted-index-type）：—。

</details>

<details><summary>Jieba — jieba-tokenizer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/tokenizer/jieba-tokenizer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/tokenizer/jieba-tokenizer.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `4/3/7/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/jieba-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/jieba-tokenizer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−71/+3075（44.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 21；H=1：Custom configuration with a dictionary file \| PUBLIC。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/jieba-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/jieba-tokenizer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−560/+1628（42.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 15；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`manage-file-resources.md`×1、`removepunct-filter.md`×1；待判 U：`manage-file-resources.md`×1。
C（guides/jieba-tokenizer）：`removepunct-filter.md`×1。
C（byoc/jieba-tokenizer）：`removepunct-filter.md`×1。

</details>

<details><summary>JSON Field Overview — json-field-overview（未逐段复核）</summary>

M：[site/en/userGuide/schema/json-field-overview.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/json-field-overview.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/7/0`；围栏 `json, plaintext, python`；图 0。

C：[guides/tutorials/development/schema/json-fields/json-field-overview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/json-fields/json-field-overview.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−15/+8947（66.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust`；图 0；新增语言块 49；H=1：How does Zilliz Cloud handle string values in JSON fields?。

C：[byoc/tutorials/development/schema/json-fields/json-field-overview.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/json-fields/json-field-overview.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−15/+8947（66.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust`；图 0；新增语言块 49；H=1：How does Zilliz Cloud handle string values in JSON fields?。

清单链接 M：`json-operators.md`×1、`ngram.md`×1、`nullable-and-default.md`×2；待判 U：—。
C（guides/json-field-overview）：`json-operators.md`×1、`ngram.md`×1、`nullable-and-default.md`×2。
C（byoc/json-field-overview）：`json-operators.md`×1、`ngram.md`×1、`nullable-and-default.md`×2。

</details>

<details><summary>JSON Indexing — json-indexing（未逐段复核）</summary>

M：[site/en/userGuide/schema/json-indexing.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/json-indexing.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/25/0`；围栏 `json, python`；图 0。

C：[guides/tutorials/development/schema/json-fields/json-indexing.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/json-fields/json-indexing.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−180/+8650（53.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 0；新增语言块 84；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/json-fields/json-indexing.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/json-fields/json-indexing.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−180/+8650（53.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, python, rust`；图 0；新增语言块 84；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`bitmap.md`×1、`inverted.md`×1、`stl-sort.md`×1；待判 U：—。
C（guides/json-indexing）：`bitmap.md`×1、`inverted.md`×1、`stl-sort.md`×1。
C（byoc/json-indexing）：`bitmap.md`×1、`inverted.md`×1、`stl-sort.md`×1。

</details>

<details><summary>JSON Operators — json-operators（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/boolean/json-operators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/json-operators.md)；2025-04-23 / [a68ca86be4](https://github.com/milvus-io/milvus-docs/commit/a68ca86be4d4b82bbd43771c963f7877e41826b0)；字面量 `0/0/5/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/filtering/json-filtering-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/json-filtering-operators.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−0/+1070（42.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/filtering/json-filtering-operators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/json-filtering-operators.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−0/+1070（42.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/json-filtering-operators）：`json-operators.md`×3。
C（byoc/json-filtering-operators）：`json-operators.md`×3。

</details>

<details><summary>JSON Shredding — json-shredding（未逐段复核）</summary>

M：[site/en/userGuide/schema/json-shredding.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/json-shredding.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `0/0/9/3`；围栏 `json, yaml`；图 2。

C：[guides/tutorials/development/schema/json-fields/json-shredding.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/json-fields/json-shredding.md)（slug）；2026-08-01 / [f36ed93589](https://github.com/zilliztech/zdoc/commit/f36ed9358915fa9d0232d3865df82491d42ef5df)；−594/+0（21.3%）；Channel `current`；Tab `—`，围栏 `json`；图 1；新增语言块 0；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/json-fields/json-shredding.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/json-fields/json-shredding.md)（slug）；2026-08-01 / [f36ed93589](https://github.com/zilliztech/zdoc/commit/f36ed9358915fa9d0232d3865df82491d42ef5df)；−594/+0（21.3%）；Channel `current`；Tab `—`，围栏 `json`；图 1；新增语言块 0；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`birdwatcher_usage_guides.md`×2、`mmap.md`×1；待判 U：`birdwatcher_usage_guides.md`×2。
C（guides/json-shredding）：`use-json-fields.md`×1。
C（byoc/json-shredding）：`use-json-fields.md`×1。

</details>

<details><summary>Text Match — keyword-match（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/keyword-match.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/keyword-match.md)；2026-09-18 / [d0695adbdf](https://github.com/milvus-io/milvus-docs/commit/d0695adbdfe935225a92787a053b8ad38413e2c9)；字面量 `2/2/13/0`；围栏 `bash, cpp, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/search-and-query/text-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/text-match.md)（title）；2026-10-24 / [248b3349ba](https://github.com/zilliztech/zdoc/commit/248b3349ba58169187be1aa4b342096bdf5682ef)；−649/+1292（20.3%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, shell`，围栏 `bash, c++, go, java, javascript, plaintext, python, shell`；图 1；新增语言块 8；H=1：TEXT_MATCH_FUZZY expression syntax \| PUBLIC。

C：[byoc/tutorials/development/search-and-query/text-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/text-match.md)（title）；2026-10-24 / [248b3349ba](https://github.com/zilliztech/zdoc/commit/248b3349ba58169187be1aa4b342096bdf5682ef)；−649/+1292（20.3%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, shell`，围栏 `bash, c++, go, java, javascript, plaintext, python, shell`；图 1；新增语言块 8；H=1：TEXT_MATCH_FUZZY expression syntax \| PUBLIC。

清单链接 M：`index-explained.md`×1、`string.md`×1、`text.md`×1；待判 U：—。
C（guides/text-match）：`index-explained.md`×1、`string.md`×1。
C（byoc/text-match）：`index-explained.md`×1、`string.md`×1。

</details>

<details><summary>Language Identifier — language-identifier（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/tokenizer/language-identifier.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/tokenizer/language-identifier.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/1/10/0`；围栏 `python`；图 1。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/language-identifier-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/language-identifier-tokenizer.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−0/+5919（59.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/language-identifier-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/language-identifier-tokenizer.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−0/+5919（59.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/language-identifier-tokenizer）：—。
C（byoc/language-identifier-tokenizer）：—。

</details>

<details><summary>Length — length-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/length-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/length-filter.md)；2025-07-15 / [eb009dd1b0](https://github.com/milvus-io/milvus-docs/commit/eb009dd1b065b7023825428f62c7b9394bcfaf52)；字面量 `3/1/5/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/length-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/length-filter.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−108/+1548（46.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-filters/length-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/length-filter.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−108/+1548（46.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/length-filter）：—。
C（byoc/length-filter）：—。

</details>

<details><summary>Lindera — lindera-tokenizer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/tokenizer/lindera-tokenizer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/tokenizer/lindera-tokenizer.md)；2026-03-13 / [8109adab94](https://github.com/milvus-io/milvus-docs/commit/8109adab9426aa992928b2c6b2eff35148a6c034)；字面量 `6/1/5/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/lindera-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/lindera-tokenizer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−312/+3760（43.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/lindera-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/lindera-tokenizer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−312/+3760（43.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/lindera-tokenizer）：—。
C（byoc/lindera-tokenizer）：—。

</details>

<details><summary>Linear Decay — linear-decay（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/linear-decay.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/linear-decay.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `0/0/1/0`；围栏 `bash, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/linear-decay.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/linear-decay.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−16/+1127（26.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/linear-decay.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/reranking-functions/rule-based-rerankers/decay-rankers/linear-decay.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−16/+1127（26.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1；待判 U：—。
C（guides/linear-decay）：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。
C（byoc/linear-decay）：`tutorial-implement-a-time-based-ranking-in-milvus.md`×1。

</details>

<details><summary>Load & Release — load-and-release（未逐段复核）</summary>

M：[site/en/userGuide/collections/load-and-release.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/load-and-release.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `6/5/8/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/collection/load-release-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/load-release-collections.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−276/+1640（36.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=2：Prerequisites；Loading behaviors。

C：[byoc/tutorials/development/collection/load-release-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/load-release-collections.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−276/+1640（36.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=2：Prerequisites；Loading behaviors。

清单链接 M：—；待判 U：—。
C（guides/load-release-collections）：—。
C（byoc/load-release-collections）：—。

</details>

<details><summary>Lowercase — lowercase-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/lowercase-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/lowercase-filter.md)；2025-07-15 / [eb009dd1b0](https://github.com/milvus-io/milvus-docs/commit/eb009dd1b065b7023825428f62c7b9394bcfaf52)；字面量 `3/1/4/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/lowercase-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/lowercase-filter.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−63/+995（41.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-filters/lowercase-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/lowercase-filter.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−63/+995（41.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/lowercase-filter）：—。
C（byoc/lowercase-filter）：—。

</details>

<details><summary>Manage Aliases — manage-aliases（未逐段复核）</summary>

M：[site/en/userGuide/collections/manage-aliases.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/manage-aliases.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `9/8/11/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/collection/manage-aliases.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/manage-aliases.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−439/+2376（35.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 15；H=1：Why Use an Alias。

C：[byoc/tutorials/development/collection/manage-aliases.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/manage-aliases.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−439/+2376（35.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 15；H=1：Why Use an Alias。

清单链接 M：—；待判 U：—。
C（guides/manage-aliases）：—。
C（byoc/manage-aliases）：—。

</details>

<details><summary>Collection Explained — manage-collections（未逐段复核）</summary>

M：[site/en/userGuide/collections/manage-collections.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/manage-collections.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `0/0/9/0`；围栏 `—`；图 1。

C：[guides/tutorials/development/collection/manage-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/manage-collections.md)（slug）；2026-08-01 / [f36ed93589](https://github.com/zilliztech/zdoc/commit/f36ed9358915fa9d0232d3865df82491d42ef5df)；−21/+50（3.0%）；Channel `current`；Tab `—`，围栏 `—`；图 1；新增语言块 0；H=1：Limits。

C：[byoc/tutorials/development/collection/manage-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/manage-collections.md)（slug）；2026-07-24 / [4c30dbeabd](https://github.com/zilliztech/zdoc/commit/4c30dbeabd0c270d24fda817e6f2be684f501074)；−21/+50（3.0%）；Channel `current`；Tab `—`，围栏 `—`；图 1；新增语言块 0；H=1：Limits。

清单链接 M：`clustering-compaction.md`×1、`create-collection.md`×1、`keyword-match.md`×1、`load-and-release.md`×1、`metric.md`×1、`mmap.md`×1、`multi-vector-search.md`×1、`nullable-and-default.md`×1、`primary-field.md`×1、`schema.md`×2、`tune_consistency.md`×1；待判 U：`clustering-compaction.md`×1。
C（guides/manage-collections）：`create-collection.md`×1、`keyword-match.md`×1、`load-and-release.md`×1、`metric.md`×1、`mmap.md`×1、`multi-vector-search.md`×1、`nullable-and-default.md`×1、`primary-field.md`×1、`schema.md`×2、`tune_consistency.md`×1。
C（byoc/manage-collections）：`create-collection.md`×1、`keyword-match.md`×1、`load-and-release.md`×1、`metric.md`×1、`mmap.md`×1、`multi-vector-search.md`×1、`nullable-and-default.md`×1、`primary-field.md`×1、`schema.md`×2、`tune_consistency.md`×1。

</details>

<details><summary>Manage Partitions — manage-partitions（未逐段复核）</summary>

M：[site/en/userGuide/collections/manage-partitions.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/manage-partitions.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `10/9/13/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/collection/manage-partitions.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/manage-partitions.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−351/+2506（31.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/collection/manage-partitions.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/manage-partitions.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−351/+2498（31.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`insert-update-delete.md`×1；待判 U：—。
C（guides/manage-partitions）：`insert-update-delete.md`×1。
C（byoc/manage-partitions）：`insert-update-delete.md`×1。

</details>

<details><summary>Manage Snapshots — manage-snapshots（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/manage-snapshots.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/manage-snapshots.md)；2026-08-03 / [9500467564](https://github.com/milvus-io/milvus-docs/commit/9500467564cd2784d99301e3aa8c02d540ee4e88)；字面量 `2/2/2/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/snapshots/manage-snapshots.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/snapshots/manage-snapshots.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−126/+3843（55.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 24；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/manage-snapshots）：—。

</details>

<details><summary>Metric Types — metric（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/metric.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/metric.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `0/0/4/0`；围栏 `—`；图 7。

C：[guides/tutorials/development/search-and-query/search-metrics-explained.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/search-metrics-explained.md)（title）；2026-09-15 / [437c9308ae](https://github.com/zilliztech/zdoc/commit/437c9308ae84c11115667b936e75b03c68562007)；−100/+485（14.5%）；Channel `current`；Tab `—`，围栏 `—`；图 8；新增语言块 0；H=1：Maximum similarity。

C：[byoc/tutorials/development/search-and-query/search-metrics-explained.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/search-metrics-explained.md)（title）；2026-09-15 / [437c9308ae](https://github.com/zilliztech/zdoc/commit/437c9308ae84c11115667b936e75b03c68562007)；−100/+485（14.5%）；Channel `current`；Tab `—`，围栏 `—`；图 8；新增语言块 0；H=1：Maximum similarity。

清单链接 M：`array-of-structs.md`×1；待判 U：—。
C（guides/search-metrics-explained）：—。
C（byoc/search-metrics-explained）：—。

</details>

<details><summary>MinHash Function — minhash-function（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/embedding-function/minhash-function.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/embedding-function/minhash-function.md)；2026-08-04 / [8e25c100f9](https://github.com/milvus-io/milvus-docs/commit/8e25c100f92bceacbad8df62d75052823eca0dcd)；字面量 `1/1/12/0`；围栏 `bash, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/function/minhash-function.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/minhash-function.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−24/+4633（53.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/function/minhash-function.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/minhash-function.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−24/+4633（53.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/minhash-function）：—。
C（byoc/minhash-function）：—。

</details>

<details><summary>MINHASH_LSH — minhash-lsh（未逐段复核）</summary>

M：[site/en/userGuide/indexes/binary/minhash-lsh.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/indexes/binary/minhash-lsh.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/0/15/0`；围栏 `bash, go, java, javascript, python`；图 5。

C：[guides/tutorials/development/vector-index/minhash-lsh.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/vector-index/minhash-lsh.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−40/+6219（50.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 5；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/vector-index/minhash-lsh.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/vector-index/minhash-lsh.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−40/+6219（50.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 5；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`binary-vector.md`×1、`metric.md`×1；待判 U：—。
C（guides/minhash-lsh）：`binary-vector.md`×1、`metric.md`×1。
C（byoc/minhash-lsh）：`binary-vector.md`×1、`metric.md`×1。

</details>

<details><summary>Use mmap — mmap（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/mmap.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/mmap.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `4/5/29/1`；围栏 `bash, go, java, javascript, python, yaml`；图 1。

C：[guides/tutorials/development/search-and-query/use-mmap.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/use-mmap.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−801/+3716（46.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 12；H=4：Global mmap strategy；Configure mmap for specific fields；Configure mmap for scalar indexes；Configure mmap in collection。

C：[byoc/tutorials/development/search-and-query/use-mmap.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/use-mmap.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−801/+3704（46.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 12；H=4：Global mmap strategy；Configure mmap for specific fields；Configure mmap for scalar indexes；Configure mmap in collection。

清单链接 M：`configure-helm.md`×1、`configure_operator.md`×1；待判 U：—。
C（guides/use-mmap）：—。
C（byoc/use-mmap）：—。

</details>

<details><summary>Modify Collection — modify-collection（未逐段复核）</summary>

M：[site/en/userGuide/collections/modify-collection.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/modify-collection.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `11/6/15/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/collection/modify-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/modify-collections.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−321/+2450（35.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 27；H=1：Example 2: Set entity-level TTL \| PUBLIC。

C：[byoc/tutorials/development/collection/modify-collections.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/modify-collections.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−462/+2081（34.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 24；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`mmap.md`×1、`timestamptz-field.md`×1；待判 U：—。
C（guides/modify-collections）：`mmap.md`×2、`modify-collection.md`×1、`timestamptz-field.md`×1。
C（byoc/modify-collections）：`mmap.md`×2、`timestamptz-field.md`×1。

</details>

<details><summary>Multi-Vector Hybrid Search — multi-vector-search（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/multi-vector-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/multi-vector-search.md)；2026-09-16 / [d104216a11](https://github.com/milvus-io/milvus-docs/commit/d104216a11f1a57d4641a9d4376ec84bb07b209c)；字面量 `6/5/9/0`；围栏 `bash, cpp, go, java, javascript, python, text`；图 1。

C：[guides/tutorials/development/search-and-query/hybrid-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/hybrid-search.md)（title）；2026-10-26 / [d151bc9e76](https://github.com/zilliztech/zdoc/commit/d151bc9e76693eaed00552e12d17b23bd4c1d10f)；−2757/+3044（32.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, shell`；图 1；新增语言块 14；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/hybrid-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/hybrid-search.md)（title）；2026-10-26 / [d151bc9e76](https://github.com/zilliztech/zdoc/commit/d151bc9e76693eaed00552e12d17b23bd4c1d10f)；−2757/+3044（32.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, shell`；图 1；新增语言块 14；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`boolean.md`×1、`configure_proxy.md`×1、`dense-vector.md`×1、`full_text_search_with_milvus.md`×1、`index-vector-fields.md`×1、`rrf-ranker.md`×1、`sparse_vector.md`×1、`timestamptz-field.md`×1、`weighted-ranker.md`×1；待判 U：`full_text_search_with_milvus.md`×1、`index-vector-fields.md`×1。
C（guides/hybrid-search）：`boolean.md`×1、`dense-vector.md`×1、`full_text_search_with_milvus.md`×1、`rrf-ranker.md`×1、`sparse_vector.md`×1、`weighted-ranker.md`×1。
C（byoc/hybrid-search）：`boolean.md`×1、`dense-vector.md`×1、`full_text_search_with_milvus.md`×1、`rrf-ranker.md`×1、`sparse_vector.md`×1、`weighted-ranker.md`×1。

</details>

<details><summary>NGRAM — ngram（未逐段复核）</summary>

M：[site/en/userGuide/indexes/scalar/ngram.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/indexes/scalar/ngram.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/16/0`；围栏 `python`；图 3。

C：[guides/tutorials/development/scalar-index/ngram-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/scalar-index/ngram-index-type.md)（title）；2026-10-19 / [e02d9b0ef0](https://github.com/zilliztech/zdoc/commit/e02d9b0ef061918683cd15f518b1a48e94f9b70d)；−56/+1964（30.9%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 3；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/scalar-index/ngram-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/scalar-index/ngram-index-type.md)（title）；2026-10-19 / [e02d9b0ef0](https://github.com/zilliztech/zdoc/commit/e02d9b0ef061918683cd15f518b1a48e94f9b70d)；−56/+1964（30.9%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 3；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`pattern-matching.md`×2；待判 U：—。
C（guides/ngram-index-type）：`mmap.md`×1、`pattern-matching.md`×2。
C（byoc/ngram-index-type）：`mmap.md`×1、`pattern-matching.md`×2。

</details>

<details><summary>Nullable Fields — nullable-and-default（未逐段复核）</summary>

M：[site/en/userGuide/schema/nullable-and-default.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/nullable-and-default.md)；2026-09-02 / [701b40341d](https://github.com/milvus-io/milvus-docs/commit/701b40341dd2731fe1c311309e6d23c5bbf4d49a)；字面量 `5/4/22/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/schema/nullable-fields.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/nullable-fields.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−799/+2931（35.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=2：Query & filtering implications；Applicable rules。

C：[byoc/tutorials/development/schema/nullable-fields.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/nullable-fields.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−799/+2931（35.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=2：Query & filtering implications；Applicable rules。

清单链接 M：`array-of-structs.md`×1、`default-values.md`×2、`structarray-limits.md`×1；待判 U：—。
C（guides/nullable-fields）：`default-values.md`×1、`nullable-and-default.md`×1、`structarray-limits.md`×1。
C（byoc/nullable-fields）：`default-values.md`×1、`nullable-and-default.md`×1、`structarray-limits.md`×1。

</details>

<details><summary>OpenAI — openai（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/embedding-function/openai.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/embedding-function/openai.md)；2025-09-18 / [3a9f46f9cf](https://github.com/milvus-io/milvus-docs/commit/3a9f46f9cf5a702346da327e2b26e47de075fbd5)；字面量 `1/0/18/7`；围栏 `python, yaml`；图 0。

C：[guides/tutorials/development/function/text-embedding-funcs/openai.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/text-embedding-funcs/openai.md)（slug）；2026-10-26 / [d151bc9e76](https://github.com/zilliztech/zdoc/commit/d151bc9e76693eaed00552e12d17b23bd4c1d10f)；−594/+5002（78.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 42；H=9：Model choices；Before you start；Step 1: Create a collection with a text embedding function；Define schema fields；Define the text embedding function；Configure the index；Create the collection；Step 2: Insert data；Step 3: Search with text。

清单链接 M：`configure-docker.md`×1、`embedding-function-overview.md`×1；待判 U：`embedding-function-overview.md`×1。
C（guides/openai）：`embeddings.md`×1。

</details>

<details><summary>Pattern Matching — pattern-matching（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/boolean/pattern-matching.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/pattern-matching.md)；2026-09-16 / [071897a9ac](https://github.com/milvus-io/milvus-docs/commit/071897a9ac68d585d46f30c173aeca62e5cf44d9)；字面量 `6/2/15/0`；围栏 `bash, cpp, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/search-and-query/filtering/pattern-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/pattern-match.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−283/+534（11.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, shell`；图 0；新增语言块 14；H=2：Use regex \| PUBLIC；Using raw string literals。

C：[byoc/tutorials/development/search-and-query/filtering/pattern-match.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/pattern-match.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−283/+534（11.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, shell`；图 0；新增语言块 14；H=2：Use regex \| PUBLIC；Using raw string literals。

清单链接 M：`bitmap.md`×1、`inverted.md`×1、`ngram.md`×1、`stl-sort.md`×1；待判 U：—。
C（guides/pattern-match）：`bitmap.md`×1、`inverted.md`×1、`ngram.md`×1、`stl-sort.md`×1、`struct-array-operators.md`×1。
C（byoc/pattern-match）：`bitmap.md`×1、`inverted.md`×1、`ngram.md`×1、`stl-sort.md`×1、`struct-array-operators.md`×1。

</details>

<details><summary>Pinyin — pinyin-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/pinyin-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/pinyin-filter.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/1/0`；围栏 `plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/pinyin-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/pinyin-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−0/+3578（71.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 42；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-filters/pinyin-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/pinyin-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−0/+3578（71.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 42；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/pinyin-filter）：—。
C（byoc/pinyin-filter）：—。

</details>

<details><summary>Primary Field & AutoID — primary-field（未逐段复核）</summary>

M：[site/en/userGuide/schema/primary-field.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/primary-field.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `10/0/14/1`；围栏 `bash, go, java, javascript, plaintext, python, yaml`；图 0。

C：[guides/tutorials/development/schema/primary-field-auto-id.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/primary-field-auto-id.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−333/+3582（39.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/primary-field-auto-id.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/primary-field-auto-id.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−333/+3582（39.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`modify-collection.md`×1、`primary-field.md`×2；待判 U：—。
C（guides/primary-field-auto-id）：`primary-field.md`×1。
C（byoc/primary-field-auto-id）：`primary-field.md`×1。

</details>

<details><summary>Primary-Key Search — primary-key-search（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/primary-key-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/primary-key-search.md)；2026-09-10 / [79360fe5f1](https://github.com/milvus-io/milvus-docs/commit/79360fe5f19ef3fdbbc5a37c2e6bbebc9663d8d5)；字面量 `8/8/12/0`；围栏 `bash, cpp, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/search-and-query/primary-key-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/primary-key-search.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−745/+1496（27.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, shell`；图 0；新增语言块 8；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/primary-key-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/primary-key-search.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−745/+1496（27.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, shell`；图 0；新增语言块 8；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/primary-key-search）：—。
C（byoc/primary-key-search）：—。

</details>

<details><summary>Random Sampling — random-sampling（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/boolean/random-sampling.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/boolean/random-sampling.md)；2025-07-04 / [6e8822e211](https://github.com/milvus-io/milvus-docs/commit/6e8822e2117881980d2779bd2ea4e079e8faf577)；字面量 `3/0/1/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/search-and-query/filtering/ramdom-sampling.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/filtering/ramdom-sampling.md)（title）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−87/+3457（44.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/filtering/ramdom-sampling.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/filtering/ramdom-sampling.md)（title）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−87/+3457（44.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/ramdom-sampling）：—。
C（byoc/ramdom-sampling）：—。

</details>

<details><summary>Range Search — range-search（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/range-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/range-search.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `5/4/7/0`；围栏 `bash, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/search-and-query/range-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/range-search.md)（slug）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−59/+844（23.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 1；新增语言块 4；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/range-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/range-search.md)（slug）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−59/+844（23.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 1；新增语言块 4；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/range-search）：—。
C（byoc/range-search）：—。

</details>

<details><summary>Range Search with StructArray — range-search-with-structarray（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/range-search-with-structarray.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/range-search-with-structarray.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/1/1/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/search-and-query/struct-array-search/range-search-with-struct-arrays.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/struct-array-search/range-search-with-struct-arrays.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−3/+5062（62.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/struct-array-search/range-search-with-struct-arrays.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/struct-array-search/range-search-with-struct-arrays.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−3/+5062（62.6%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`basic-vector-search-with-structarray.md`×2、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×2、`grouping-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`structarray-limits.md`×1；待判 U：—。
C（guides/range-search-with-struct-arrays）：`basic-vector-search-with-structarray.md`×2、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×2、`grouping-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`structarray-limits.md`×1。
C（byoc/range-search-with-struct-arrays）：`basic-vector-search-with-structarray.md`×2、`create-structarray-field.md`×1、`filtered-search-with-structarray.md`×2、`grouping-search-with-structarray.md`×1、`index-structarray-fields.md`×1、`structarray-limits.md`×1。

</details>

<details><summary>Regex Analyzer Filter — regex-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/regex-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/regex-filter.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `3/1/3/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/regex-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/regex-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−37/+1274（41.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-filters/regex-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/regex-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−37/+1274（41.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`pattern-matching.md`×1；待判 U：—。
C（guides/regex-filter）：`pattern-matching.md`×1。
C（byoc/regex-filter）：`pattern-matching.md`×1。

</details>

<details><summary>Remove Punct — removepunct-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/removepunct-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/removepunct-filter.md)；2026-09-22 / [59e7df2f56](https://github.com/milvus-io/milvus-docs/commit/59e7df2f5617847f683c09895da38614cf95925a)；字面量 `3/1/3/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/remove-punct-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/remove-punct-filter.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−33/+851（37.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-filters/remove-punct-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/remove-punct-filter.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−33/+851（37.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/remove-punct-filter）：—。
C（byoc/remove-punct-filter）：—。

</details>

<details><summary>RTREE — rtree（未逐段复核）</summary>

M：[site/en/userGuide/indexes/scalar/rtree.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/indexes/scalar/rtree.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `1/0/3/0`；围栏 `python`；图 1。

C：[guides/tutorials/development/scalar-index/rtree-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/scalar-index/rtree-index-type.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−26/+2969（65.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/scalar-index/rtree-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/scalar-index/rtree-index-type.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−26/+2969（65.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`geometry-field.md`×1；待判 U：—。
C（guides/rtree-index-type）：`geometry-field.md`×1。
C（byoc/rtree-index-type）：`geometry-field.md`×1。

</details>

<details><summary>Schema Explained — schema（未逐段复核）</summary>

M：[site/en/userGuide/schema/schema.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/schema.md)；2026-07-29 / [d3173805f6](https://github.com/milvus-io/milvus-docs/commit/d3173805f6cb180dbce5f306affb675bcf1735e0)；字面量 `0/0/11/0`；围栏 `curl, java, javascript, python`；图 1。

C：[guides/tutorials/development/schema/schema-explained.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/schema-explained.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−373/+1589（32.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 45；H=11：Overview；Create Schema；Add Primary Field；Add Vector Fields；Add Scalar Fields；Add VarChar Fields；Add Number Fields；Add Boolean Fields；Add Composite Fields；Add JSON fields；Add Array Fields。

C：[byoc/tutorials/development/schema/schema-explained.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/schema-explained.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−373/+1589（32.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 45；H=11：Overview；Create Schema；Add Primary Field；Add Vector Fields；Add Scalar Fields；Add VarChar Fields；Add Number Fields；Add Boolean Fields；Add Composite Fields；Add JSON fields；Add Array Fields。

清单链接 M：`array_data_type.md`×1、`number.md`×1、`primary-field.md`×1、`schema-hands-on.md`×1、`string.md`×1、`text.md`×1、`use-json-fields.md`×1；待判 U：—。
C（guides/schema-explained）：`array_data_type.md`×1、`number.md`×1、`primary-field.md`×1、`schema-hands-on.md`×1、`string.md`×1、`text.md`×1、`use-json-fields.md`×1。
C（byoc/schema-explained）：`array_data_type.md`×1、`number.md`×1、`primary-field.md`×1、`schema-hands-on.md`×1、`string.md`×1、`text.md`×1、`use-json-fields.md`×1。

</details>

<details><summary>Search Aggregation — search-aggregation（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/search-aggregation.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/search-aggregation.md)；2026-08-26 / [3592946eb3](https://github.com/milvus-io/milvus-docs/commit/3592946eb3e576f3fa8f3c49b5724a83be11b121)；字面量 `4/3/27/0`；围栏 `bash, go, java, javascript, json, python, text`；图 2。

C：[guides/tutorials/development/search-and-query/search-aggregation.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/search-aggregation.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−206/+6978（23.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust`；图 2；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/search-aggregation.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/search-aggregation.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−206/+6978（23.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust`；图 2；新增语言块 21；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/search-aggregation）：—。
C（byoc/search-aggregation）：—。

</details>

<details><summary>Set Collection TTL — set-collection-ttl（未逐段复核）</summary>

M：[site/en/userGuide/collections/set-collection-ttl.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/collections/set-collection-ttl.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `32/1/4/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/collection/set-collection-ttl.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/collection/set-collection-ttl.md)（slug）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−196/+15825（55.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 33；H=3：Set entity-level TTL \| PUBLIC；Migrate between the two modes \| PRIVATE；When will the CU capacity decrease?。

C：[byoc/tutorials/development/collection/set-collection-ttl.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/collection/set-collection-ttl.md)（slug）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−1196/+12193（55.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 27；H=2：Set entity-level TTL \| PUBLIC；When will the CU capacity decrease?。

清单链接 M：—；待判 U：—。
C（guides/set-collection-ttl）：—。
C（byoc/set-collection-ttl）：—。

</details>

<details><summary>Basic Vector Search — single-vector-search（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/single-vector-search.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/single-vector-search.md)；2026-09-08 / [b3f22b9868](https://github.com/milvus-io/milvus-docs/commit/b3f22b986863373cbd990496db9756255d036b57)；字面量 `12/11/32/0`；围栏 `bash, cpp, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/search-and-query/single-vector-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/single-vector-search.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1108/+7485（29.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 0；新增语言块 33；H=4：Primary-Key Search；Sort Search Results by Scalar Fields \| PUBLIC；Use Level；Get Recall Rate。

C：[byoc/tutorials/development/search-and-query/single-vector-search.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/single-vector-search.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−1108/+7516（29.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 0；新增语言块 33；H=4：Primary-Key Search；Sort Search Results by Scalar Fields \| PUBLIC；Use Level；Get Recall Rate。

清单链接 M：`boolean.md`×1、`clustering-compaction.md`×1、`decay-ranker-overview.md`×1、`keyword-match.md`×1、`mmap.md`×1、`model-ranker-overview.md`×1、`multi-vector-search.md`×1、`timestamptz-field.md`×1；待判 U：`clustering-compaction.md`×1、`model-ranker-overview.md`×1。
C（guides/single-vector-search）：`boolean.md`×1、`keyword-match.md`×1、`metric.md`×1、`mmap.md`×1、`multi-vector-search.md`×1、`timestamptz-field.md`×1。
C（byoc/single-vector-search）：`boolean.md`×1、`keyword-match.md`×1、`metric.md`×1、`mmap.md`×1、`multi-vector-search.md`×1、`timestamptz-field.md`×1。

</details>

<details><summary>Sparse Vector — sparse_vector（未逐段复核）</summary>

M：[site/en/userGuide/schema/sparse_vector.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/sparse_vector.md)；2026-05-14 / [99af735142](https://github.com/milvus-io/milvus-docs/commit/99af73514248e0cf21dbaf1d470b748932131e12)；字面量 `4/0/7/0`；围栏 `bash, go, java, javascript, python`；图 2。

C：[guides/tutorials/development/schema/use-sparse-vector.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-sparse-vector.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−542/+2691（29.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 2；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/use-sparse-vector.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-sparse-vector.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−542/+2691（29.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 2；新增语言块 18；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`binary-vector.md`×1、`create-collection.md`×1、`dense-vector.md`×2、`embeddings.md`×2、`metric.md`×1、`sparse-inverted-index.md`×1；待判 U：`embeddings.md`×2。
C（guides/use-sparse-vector）：`binary-vector.md`×1、`create-collection.md`×1、`dense-vector.md`×2、`embeddings.md`×2、`metric.md`×1。
C（byoc/use-sparse-vector）：`binary-vector.md`×1、`create-collection.md`×1、`dense-vector.md`×2、`embeddings.md`×2、`metric.md`×1。

</details>

<details><summary>Standard Analyzer — standard-analyzer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/analyzer/standard-analyzer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/analyzer/standard-analyzer.md)；2026-09-22 / [59e7df2f56](https://github.com/milvus-io/milvus-docs/commit/59e7df2f5617847f683c09895da38614cf95925a)；字面量 `3/3/8/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/built-in-analyzer/standard-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/built-in-analyzer/standard-analyzer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−117/+1200（36.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, sql`；图 0；新增语言块 15；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/built-in-analyzer/standard-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/built-in-analyzer/standard-analyzer.md)（slug）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−117/+1200（36.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, sql`；图 0；新增语言块 15；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/standard-analyzer）：—。
C（byoc/standard-analyzer）：—。

</details>

<details><summary>Standard Tokenizer — standard-tokenizer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/tokenizer/standard-tokenizer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/tokenizer/standard-tokenizer.md)；2026-09-22 / [59e7df2f56](https://github.com/milvus-io/milvus-docs/commit/59e7df2f5617847f683c09895da38614cf95925a)；字面量 `3/3/8/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/standard-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/standard-tokenizer.md)（slug）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−48/+994（31.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, sql`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/standard-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/standard-tokenizer.md)（slug）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−48/+994（31.1%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, sql`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/standard-tokenizer）：—。
C（byoc/standard-tokenizer）：—。

</details>

<details><summary>Stemmer — stemmer-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/stemmer-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/stemmer-filter.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `3/1/4/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/stemmer-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/stemmer-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−144/+1218（39.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-filters/stemmer-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/stemmer-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−144/+1218（39.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/stemmer-filter）：—。
C（byoc/stemmer-filter）：—。

</details>

<details><summary>STL_SORT — stl-sort（未逐段复核）</summary>

M：[site/en/userGuide/indexes/scalar/stl-sort.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/indexes/scalar/stl-sort.md)；2025-11-21 / [5a7b74004e](https://github.com/milvus-io/milvus-docs/commit/5a7b74004e04e7ceac04c1c75e11354b31edf53f)；字面量 `1/0/6/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/scalar-index/slt-sort-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/scalar-index/slt-sort-index-type.md)（title）；2026-10-08 / [9caba94ec7](https://github.com/zilliztech/zdoc/commit/9caba94ec782a26e1e242d5c3b4c9bbd6b01807f)；−38/+1264（54.9%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/scalar-index/slt-sort-index-type.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/scalar-index/slt-sort-index-type.md)（title）；2026-10-08 / [9caba94ec7](https://github.com/zilliztech/zdoc/commit/9caba94ec782a26e1e242d5c3b4c9bbd6b01807f)；−38/+1264（54.9%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`number.md`×2、`string.md`×1、`timestamptz-field.md`×2；待判 U：—。
C（guides/slt-sort-index-type）：`number.md`×2、`string.md`×1、`timestamptz-field.md`×2。
C（byoc/slt-sort-index-type）：`number.md`×2、`string.md`×1、`timestamptz-field.md`×2。

</details>

<details><summary>Stop — stop-filter（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/filter/stop-filter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/filter/stop-filter.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `4/1/5/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-filters/stop-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-filters/stop-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−500/+1344（42.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-filters/stop-filter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-filters/stop-filter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−500/+1344（42.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 9；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`manage-file-resources.md`×1；待判 U：`manage-file-resources.md`×1。
C（guides/stop-filter）：—。
C（byoc/stop-filter）：—。

</details>

<details><summary>Text Field — text（未逐段复核）</summary>

M：[site/en/userGuide/schema/text.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/text.md)；2026-08-05 / [b752e5d162](https://github.com/milvus-io/milvus-docs/commit/b752e5d1625737d0d9bd6aa28c1981ed617243d8)；字面量 `1/0/21/0`；围栏 `python`；图 1。

C：[guides/tutorials/development/schema/use-text-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-text-field.md)（title）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−722/+4981（68.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 0；新增语言块 48；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/use-text-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-text-field.md)（title）；2026-10-25 / [c4046ef798](https://github.com/zilliztech/zdoc/commit/c4046ef798f68edc6c1941de1b3b220f47b38bd4)；−722/+4981（68.5%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 0；新增语言块 48；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`configure_common.md`×1、`configure_datacoord.md`×1、`configure_datanode.md`×2、`keyword-match.md`×1、`nullable-and-default.md`×1、`string.md`×1；待判 U：—。
C（guides/use-text-field）：`nullable-and-default.md`×1、`string.md`×1。
C（byoc/use-text-field）：`nullable-and-default.md`×1、`string.md`×1。

</details>

<details><summary>Text Highlighter — text-highlighter（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/text-highlighter.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/text-highlighter.md)；2026-01-04 / [5e98546f43](https://github.com/milvus-io/milvus-docs/commit/5e98546f43f85529c5ab1fe856372ad41938d391)；字面量 `1/0/26/0`；围栏 `json, plaintext, python`；图 0。

C：[guides/tutorials/development/search-and-query/text-highlighter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/text-highlighter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−10/+9193（58.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust, shell`；图 0；新增语言块 96；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/text-highlighter.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/text-highlighter.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−10/+9193（58.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, json, plaintext, python, rust, shell`；图 0；新增语言块 96；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`keyword-match.md`×1；待判 U：—。
C（guides/text-highlighter）：`keyword-match.md`×1。
C（byoc/text-highlighter）：`keyword-match.md`×1。

</details>

<details><summary>Thai — thai-analyzer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/analyzer/thai-analyzer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/analyzer/thai-analyzer.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/5/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−281/+1656（79.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[guides/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−0/+1831（62.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 35；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md)（title）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−281/+1656（79.0%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md)（slug）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−0/+1831（62.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 35；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/thai-tokenizer）：—。
C（guides/thai-analyzer）：—。
C（byoc/thai-tokenizer）：—。
C（byoc/thai-analyzer）：—。
歧义：两个 Cloud 页都叫 Thai；按标题产生交叉命中。应优先同 slug 并按 tokenizer/analyzer 路径确认，不能把两组 diff 混成一个。

</details>

<details><summary>Thai — thai-tokenizer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/tokenizer/thai-tokenizer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/tokenizer/thai-tokenizer.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/2/0`；围栏 `python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−0/+1423（59.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[guides/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md)（title）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−250/+2129（83.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 35；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/thai-tokenizer.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−0/+1423（59.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 28；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/built-in-analyzer/thai-analyzer.md)（title）；2026-10-24 / [68fe393046](https://github.com/zilliztech/zdoc/commit/68fe3930467cee0e791183c138c9d80c1675aa3e)；−250/+2129（83.2%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, plaintext, python, rust`；图 0；新增语言块 35；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`decimaldigit-filter.md`×1；待判 U：`decimaldigit-filter.md`×1。
C（guides/thai-tokenizer）：—。
C（guides/thai-analyzer）：—。
C（byoc/thai-tokenizer）：—。
C（byoc/thai-analyzer）：—。
歧义：两个 Cloud 页都叫 Thai；按标题产生交叉命中。应优先同 slug 并按 tokenizer/analyzer 路径确认，不能把两组 diff 混成一个。

</details>

<details><summary>TIMESTAMPTZ Field — timestamptz-field（未逐段复核）</summary>

M：[site/en/userGuide/schema/timestamptz-field.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/timestamptz-field.md)；2026-07-29 / [95fbb2bd2e](https://github.com/milvus-io/milvus-docs/commit/95fbb2bd2e0e24bd3309128aa8354e0f7ef3fd84)；字面量 `1/0/4/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/schema/use-timestamptz-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/schema/use-timestamptz-field.md)（title）；2026-10-06 / [00d35fe140](https://github.com/zilliztech/zdoc/commit/00d35fe140ebe4b163136708beb2df0262dfc44d)；−180/+7288（61.6%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/schema/use-timestamptz-field.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/schema/use-timestamptz-field.md)（title）；2026-10-06 / [00d35fe140](https://github.com/zilliztech/zdoc/commit/00d35fe140ebe4b163136708beb2df0262dfc44d)；−180/+7288（61.6%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 0；新增语言块 12；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`basic-operators.md`×1、`manage_databases.md`×1、`modify-collection.md`×1、`multi-vector-search.md`×2、`nullable-and-default.md`×1、`stl-sort.md`×1；待判 U：`manage_databases.md`×1。
C（guides/use-timestamptz-field）：`basic-operators.md`×1、`modify-collection.md`×1、`multi-vector-search.md`×2、`nullable-and-default.md`×1、`stl-sort.md`×1。
C（byoc/use-timestamptz-field）：`basic-operators.md`×1、`modify-collection.md`×1、`multi-vector-search.md`×2、`nullable-and-default.md`×1、`stl-sort.md`×1。

</details>

<details><summary>Upsert Entities — upsert-entities（未逐段复核）</summary>

M：[site/en/userGuide/insert-and-delete/upsert-entities.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/insert-and-delete/upsert-entities.md)；2026-09-11 / [05e05baa20](https://github.com/milvus-io/milvus-docs/commit/05e05baa2089f24d1bc289ad2327af9458b209cd)；字面量 `9/7/23/0`；围栏 `bash, go, java, javascript, python`；图 2。

C：[guides/tutorials/development/insert-and-delete/upsert-entities.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/insert-and-delete/upsert-entities.md)（slug）；2026-10-10 / [c883fe86ea](https://github.com/zilliztech/zdoc/commit/c883fe86eae118f948887078977af92eb8aaffbf)；−1053/+10758（51.0%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 2；新增语言块 14；H=4：Upsert in merge mode；Update field values；Upsert entities in merge mode；Upsert ARRAY fields in merge mode。

C：[byoc/tutorials/development/insert-and-delete/upsert-entities.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/insert-and-delete/upsert-entities.md)（slug）；2026-10-10 / [c883fe86ea](https://github.com/zilliztech/zdoc/commit/c883fe86eae118f948887078977af92eb8aaffbf)；−1053/+10758（51.0%）；Channel `current`；Tab `bash, c++, go, java, javascript, python, rust`，围栏 `bash, c++, go, java, javascript, python, rust`；图 2；新增语言块 14；H=4：Upsert in merge mode；Update field values；Upsert entities in merge mode；Upsert ARRAY fields in merge mode。

清单链接 M：—；待判 U：—。
C（guides/upsert-entities）：—。
C（byoc/upsert-entities）：—。

</details>

<details><summary>Voyage AI — voyage-ai（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/embedding-function/voyage-ai.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/embedding-function/voyage-ai.md)；2025-09-18 / [3a9f46f9cf](https://github.com/milvus-io/milvus-docs/commit/3a9f46f9cf5a702346da327e2b26e47de075fbd5)；字面量 `1/0/16/6`；围栏 `python, yaml`；图 0。

C：[guides/tutorials/development/function/text-embedding-funcs/voyage-ai.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/text-embedding-funcs/voyage-ai.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−519/+5169（76.7%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 42；H=9：Model choices；Before you start；Step 1: Create a collection with a text embedding function；Define schema fields；Define the text embedding function；Configure the index；Create the collection；Step 2: Insert data；Step 3: Search with text。

清单链接 M：`configure-docker.md`×1、`embedding-function-overview.md`×1；待判 U：`embedding-function-overview.md`×1。
C（guides/voyage-ai）：—。

</details>

<details><summary>Voyage AI Ranker — voyage-ai-ranker（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/voyage-ai-ranker.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/voyage-ai-ranker.md)；2026-01-14 / [a43bd1aaff](https://github.com/milvus-io/milvus-docs/commit/a43bd1aaff56abf0d4b02e79698bf0ad50ca97f1)；字面量 `3/0/6/0`；围栏 `bash, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/function/reranking-functions/model-based-rerankers/voyage-ai-model-ranker.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/model-based-rerankers/voyage-ai-model-ranker.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−727/+5094（85.4%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 0；新增语言块 9；H=6：Before you start；Use Voyage AI Ranker；Preparations；Define the rerank function；Search with the rerank function；Next steps。

清单链接 M：`model-ranker-overview.md`×1；待判 U：`model-ranker-overview.md`×1。
C（guides/voyage-ai-model-ranker）：`multi-vector-search.md`×1。

</details>

<details><summary>Weighted Ranker — weighted-ranker（未逐段复核）</summary>

M：[site/en/userGuide/embeddings-reranking/reranking/weighted-ranker.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/embeddings-reranking/reranking/weighted-ranker.md)；2026-05-09 / [befdc216a5](https://github.com/milvus-io/milvus-docs/commit/befdc216a57c75e3d3f4f7fc0d36be62e39a02f9)；字面量 `3/0/2/0`；围栏 `bash, go, java, javascript, python`；图 1。

C：[guides/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-weighted-reranker.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-weighted-reranker.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−131/+1569（32.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-weighted-reranker.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/function/reranking-functions/hybrid-search-rerankers/reranking-weighted-reranker.md)（title）；2026-10-25 / [60907c1fa8](https://github.com/zilliztech/zdoc/commit/60907c1fa81be4ddd9289de7093e2270d90a2f24)；−131/+1569（32.3%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust`；图 1；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：`multi-vector-search.md`×1、`weighted-ranker.md`×2；待判 U：—。
C（guides/reranking-weighted-reranker）：`multi-vector-search.md`×1、`weighted-ranker.md`×2。
C（byoc/reranking-weighted-reranker）：`multi-vector-search.md`×1、`weighted-ranker.md`×2。

</details>

<details><summary>Whitespace — whitespace-tokenizer（未逐段复核）</summary>

M：[site/en/userGuide/schema/analyzer/tokenizer/whitespace-tokenizer.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/schema/analyzer/tokenizer/whitespace-tokenizer.md)；2026-09-22 / [59e7df2f56](https://github.com/milvus-io/milvus-docs/commit/59e7df2f5617847f683c09895da38614cf95925a)；字面量 `3/1/6/0`；围栏 `bash, go, java, javascript, plaintext, python`；图 0。

C：[guides/tutorials/development/analyzer/analyzer-tokenizers/whitespace-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/analyzer/analyzer-tokenizers/whitespace-tokenizer.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−56/+1207（37.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, sql`；图 0；新增语言块 12；H=1：Verification using `run_analyzer`。

C：[byoc/tutorials/development/analyzer/analyzer-tokenizers/whitespace-tokenizer.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/analyzer/analyzer-tokenizers/whitespace-tokenizer.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−56/+1207（37.9%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, sql`；图 0；新增语言块 12；H=1：Verification using `run_analyzer`。

清单链接 M：—；待判 U：—。
C（guides/whitespace-tokenizer）：—。
C（byoc/whitespace-tokenizer）：—。

</details>

<details><summary>Search Iterator — with-iterators（未逐段复核）</summary>

M：[site/en/userGuide/search-query-get/with-iterators.md](https://github.com/milvus-io/milvus-docs/blob/d631183688a0e53acd092ae6d923fca28c2b9f5c/site/en/userGuide/search-query-get/with-iterators.md)；2026-09-18 / [d0695adbdf](https://github.com/milvus-io/milvus-docs/commit/d0695adbdfe935225a92787a053b8ad38413e2c9)；字面量 `6/6/6/0`；围栏 `bash, cpp, go, java, javascript, python`；图 0。

C：[guides/tutorials/development/search-and-query/with-iterators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/guides/tutorials/development/search-and-query/with-iterators.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−520/+1366（42.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 0；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

C：[byoc/tutorials/development/search-and-query/with-iterators.md](https://github.com/zilliztech/zdoc/blob/008e48a0705efbfa041333efa197119a7fd6900d/content/en/byoc/tutorials/development/search-and-query/with-iterators.md)（slug）；2026-10-24 / [95a7f2ec93](https://github.com/zilliztech/zdoc/commit/95a7f2ec930334d166bf393e376787c115d5d118)；−520/+1366（42.8%）；Channel `current`；Tab `bash, c++, csharp, go, java, javascript, python, rust, shell`，围栏 `bash, c++, csharp, go, java, javascript, python, rust, shell`；图 0；新增语言块 6；H=0：无新增标题，正文仍待人工复核。

清单链接 M：—；待判 U：—。
C（guides/with-iterators）：—。
C（byoc/with-iterators）：—。

</details>

## 方法、复算与不确定性

1. 用 GitHub 实时分支头冻结上表 SHA；在临时目录创建完整历史的 bare 副本并导出所需路径，未向源仓库写任何提交或引用。读取设计仓库固定 main 的场景 3、WP 状态与链接清单。
2. Milvus 页面标识优先取 front matter `id` 去 `.md`；Cloud 取 `slug` 去前导 `/`。同 slug **或** title 去掉 `| Cloud`/`| BYOC` 后忽略大小写、首尾空白相同即保留。不做 fuzzy match；80 篇无匹配直接跳过，不凭主题相近补配对。标题命中冲突保留多候选并标歧义。
3. 页面的最后提交用 `git log -1 --format=%H|%cI|%s <sha> -- <path>`；前 20 再用 `--follow` 读取完整历史，检查最后补丁及当前两端正文。只有在补丁的新事实/修正仍缺失时写“已证实”，并注明部分已同步或产品分叉；时间先后只提供线索。未逐段复核的其余页不宣称确定漂移。
4. 文本规范化：去 YAML front matter、import、代码语言围栏标记、Tabs/TabItem 与常见 HTML/MDX 排版标签、锚点、注释与高亮标记；Markdown 链接保留标签、图片替成统一标记；表格边框、标题符号归一。把独立产品名 Milvus/Zilliz Cloud、常见 endpoint/token 归一。保留代码正文及版本、参数、数字，token 为 `\w+|[^\w\s]`，以 Python `difflib.SequenceMatcher(autojunk=False)` 计算 delete/insert/replace 长度；replace 两边分别计数。
5. 审 Cloud-only 时额外看去代码后的正文 diff 与每种语言代码：标题增减仅用来定位，不把 PUBLIC、Step 前缀、Grid 重排误算独有节；CLI、专属配置/API、无上游来源的例子/图片都记录。自动的代码/图片/标题计数是成本提示，不是语义等价证明。
6. 链接抽取 Markdown 与 HTML href，去 query/fragment 后按文件名匹配清单；Cloud 用清单给出的映射与本次同标题配对反查目标。只统计匹配到清单的引用，不访问外链、不判断锚点、不认定映射已批准。快照按 slug 匹配 Release Channel；前 20 再核验 doc_token 与发布 targets。

**已知局限/歧义：**

- 规范化是明示规则的文本启发式，不是完整 Markdown/MDX AST 或 SDK 语义比较；HTML 转义、少量布局标记、代码格式仍可能贡献差异，统一连接值也会隐藏这部分实际接入工作。没有下载图片或比较像素；图片引用数相同不保证同图。
- 全文 diff 包含 Cloud 的新增 SDK 语言，数值大不一定是原文陈旧；反过来 0.2% 的 Search with Embedding Lists 也仍有 2 张缺源图片。Cloud 生成提交很新也不表示上游修正已同步。
- 快照所有记录为 CURRENT 是实际观测，不是默认填充。但这是 10-26 的 retained snapshot，未实时查询飞书；11 月接入批次应再核查 Channel、导航归属与页面来源。
- `array_data_type` 的 JSON/STRUCT 支持、StructArray nullable 的适用集群、multi-language 的 Arabic/Thai 配置等不能靠文字 diff 判定产品事实；明确排除首批或列为内容对齐阻断，不做猜测。
- 其他 102 页只有自动初筛；独有章节候选需要人工逐段复核。Thai 同标题多义与 Import Data 导航容器已单列。无匹配的 80 页按任务要求跳过，不能据此推断 Cloud 没有任何语义对应页。
- 本次未跑产品构建、链接映射校验、SDK 示例执行或激活比较；这些属于接入实施验证，不能用本报告替代。

复算输入的最小命令（目录用自己的临时位置，源仓库无写操作）：

```bash
git clone --bare --filter=blob:none --single-branch --branch v3.0.x https://github.com/milvus-io/milvus-docs.git milvus.git
git clone --bare --filter=blob:none --single-branch --branch dev https://github.com/zilliztech/zdoc.git zdoc.git
git --git-dir=milvus.git rev-parse --is-shallow-repository
git --git-dir=zdoc.git rev-parse --is-shallow-repository
git --git-dir=milvus.git archive d631183688a0e53acd092ae6d923fca28c2b9f5c site/en/userGuide > milvus-user-guide.tar
git --git-dir=zdoc.git archive 008e48a0705efbfa041333efa197119a7fd6900d content/en/guides content/en/byoc packages/docs-tooling/src/lark/meta/snapshots/guides-uat-last-success.json > cloud-guides.tar
git --git-dir=milvus.git log --follow --format="%H|%cI|%s" d631183688a0e53acd092ae6d923fca28c2b9f5c -- site/en/userGuide/collections/view-collections.md
```

下面是本次实际使用的规范化与差异计算核心；输入 `body` 已去 front matter，输出数值与前述表格同口径。为保持单文件交付，将核心代码附在报告中。

<details><summary>规范化核心（Python 3 标准库）</summary>

```python
import re, html, difflib
def base_norm(s):
 s=re.sub(r'^import .*?;\s*$','',s,flags=re.M)
 s=re.sub(r'<div class="multipleCode">.*?</div>','',s,flags=re.S)
 s=re.sub(r'<Tabs\b[^\n]*>','',s)
 s=re.sub(r'<!--.*?-->','',s,flags=re.S)
 s=re.sub(r'</?(?:TabItem|Tabs|Admonition|div|NextChannel|CurrentChannel|p|br|a)\b[^>]*>','',s)
 s=re.sub(r'!?\[([^\]]*)\]\([^\n]*?\)',lambda m: '[IMAGE]' if m[0].startswith('!') else m[1],s)
 s=re.sub(r'\\?\{#[^}]+\}','',s)
 s=re.sub(r'```[^\n]*','',s)
 s=re.sub(r'(?m)^\s*(?:#|//|<!--)\s*highlight-(?:start|end).*?$','',s)
 s=re.sub(r'http://localhost:19530|https?://(?:your[-_])?cluster[-_]endpoint|YOUR_CLUSTER_ENDPOINT','ENDPOINT',s,flags=re.I)
 s=s.replace('root:Milvus','TOKEN').replace('YOUR_CLUSTER_TOKEN','TOKEN')
 s=re.sub(r'\bZilliz Cloud\b|\bMilvus\b','PRODUCT',s)
 s=html.unescape(s).replace('\\','').replace('`','').replace('**','').replace('’',"'").replace('“','"').replace('”','"')
 return re.findall(r'\w+|[^\w\s]',s)
def norm(s):
 s=re.sub(r'</?(?:Grid|table|thead|tbody|tr|th|td|ul|ol|li|strong|em|code|h[1-6]|details|summary)\b[^>]*>',' ',s)
 s=re.sub(r'(?m)^\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)+\|?\s*$','',s)
 s=re.sub(r'(?m)^(\s*)#{1,6}\s+',r'\1',s)
 # Markdown table cell separators are layout, not prose.
 lines=[]; inside=False
 for line in s.splitlines():
  if line.strip().startswith('```'): inside=not inside
  if not inside and line.lstrip().startswith('|'): line=line.replace('|',' ')
  lines.append(line)
 return base_norm('\n'.join(lines))

def compare(milvus_body, cloud_body):
    a, b = norm(milvus_body), norm(cloud_body)
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    deleted = sum(i2-i for tag, i, i2, j, j2 in ops if tag != "equal")
    added = sum(j2-j for tag, i, i2, j, j2 in ops if tag != "equal")
    return deleted, added, round(100*(deleted+added)/(len(a)+len(b)), 1)
```

</details>
