# 产品名替换抽样（人工判断）

来源：milvus-docs `upstream/v3.0.x`（86a5df11）`site/en/userGuide` 正文中，排除代码块、链接、行内代码和 `Milvus Lite`、`PyMilvus`、`milvus.yaml`、版本号等之后的 1237 处 “Milvus”，以随机种子 7 抽取 40 处。

判断标准：把这一处直接换成 “Zilliz Cloud” 后，句子对 Cloud 是否仍然正确。判断由调研者人工完成，仅作参考。

| # | 文件 | 上下文 | 判断 |
|---|---|---|---|
| 1 | array_data_type.md | ld  and the ARRAY field , both using the  index type. With this type, Milvus automatically selects the most suitable index based on the | 替换正确 |
| 2 | hugging-face-ranker.md | Milvus first retrieves candidates from , then uses the query text | 替换正确 |
| 3 | use-json-fields.md | To accelerate scalar filtering on JSON fields, Milvus supports the following types of indexes: | 替换正确 |
| 4 | cohere.md | Keep your API keys in ; Milvus reads them at startup and overrides any environment variabl | 部署或凭证配置语境 |
| 5 | embedding-function-overview.md | Milvus follows this credential resolution order: | 部署或凭证配置语境 |
| 6 | use-partition-key.md | can restrict the Partition Key value within a specific range so that Milvus restricts the search scope within the corresponding partiti | 替换正确 |
| 7 | hugging-face.md | return normalized embeddings. Supported values are  and . If omitted, Milvus does not set this option in the request. \| | 替换正确 |
| 8 | number.md | Indexing helps improve search and query performance. In Milvus, indexing is mandatory for vector fields but optional for s | 替换正确 |
| 9 | set_up_cdc_replication.md | -  as the namespace for Milvus clusters. | Milvus 专属页面 |
| 10 | dashscope.md | ner, leaving your host OS untouched. For details, refer to [Configure Milvus with Docker Compose]. | 部署或凭证配置语境 |
| 11 | search-aggregation.md | Milvus ignores  when  is set. Use the root  value to control the n | 替换正确 |
| 12 | bitmap.md | To create a bitmap index in Milvus, use the  method and set the  parameter to . | 替换正确 |
| 13 | bedrock.md | Keep your credentials in ; Milvus reads them at startup and overrides any environment variabl | 部署或凭证配置语境 |
| 14 | hugging-face-tei.md | additional configuration is required as TEI is enabled by default in Milvus. | 部署或凭证配置语境 |
| 15 | clustering-compaction.md | The Clustering Compaction feature in Milvus is highly configurable. You can choose to trigger it manual | 替换正确 |
| 16 | json-operators.md | In this case, Milvus will return all products that have at least one of the tags | 替换正确 |
| 17 | embedding-function-overview.md | <code>FunctionType.TEXTEMBEDDING</code>.</p><p><strong>Note</strong>: Milvus accepts <code>FunctionType.BM25</code> (for sparse-embeddin | 替换正确 |
| 18 | load_balance.md | <td>ID(s) of the segment(s) you want to transfer. Milvus transfers all sealed segment(s) in the source query node to | Milvus 专属页面 |
| 19 | hugging-face.md | Milvus stores the vector in the Function output field. During search, Milvus uses the vector as the query vector. | 替换正确 |
| 20 | cli_commands.md | Creates a database in Milvus. | Milvus 专属页面 |
| 21 | random-sampling.md | h other filtering expressions using logical . When combining filters, Milvus first applies the other conditions and then performs random | 替换正确 |
| 22 | embedding-function-overview.md | The Function module in Milvus allows you to transform raw text data into vector embedding | 替换正确 |
| 23 | milvus_backup_api.md | s data backup and restoration features to ensure the security of your Milvus data. | Milvus 专属页面 |
| 24 | voyage-ai.md | Milvus supports embedding models provided by Voyage AI. Below are | 替换正确 |
| 25 | ngram.md | Milvus supports both  (zero or more characters) and  (exactly one | 替换正确 |
| 26 | embedding-function-overview.md | 1. **Generate embeddings**: The Function module within Milvus automatically calls the configured model provider to conver | 替换正确 |
| 27 | milvus_backup_overview.md | table lists the backup and restore compatibilities between different Milvus versions since Milvus Backup v0.5.7. | Milvus 专属页面 |
| 28 | set_up_cdc_replication.md | C pods can also reach that address. The pchannel list must match your Milvus deployment. Do not copy the example values without checking | Milvus 专属页面 |
| 29 | use-json-fields.md | 1. **Infer types automatically** – For each value, Milvus determines its type in the following order: | 替换正确 |
| 30 | cohere.md | Use this method when you run Milvus with Docker Compose and prefer to keep secrets out of files | 部署或凭证配置语境 |
| 31 | ngram.md | between the two values (inclusive). For example, with  and the word , Milvus generates: | 替换正确 |
| 32 | cohere.md | Milvus must know your Cohere API key before it can request embeddi | 部署或凭证配置语境 |
| 33 | cli_overview.md | \|  Milvus   \| PyMilvus \| Milvus_CLI \| | Milvus 专属页面 |
| 34 | boost-ranker.md | When a search request includes a Boost Ranker function, Milvus uses the optional filtering condition within the function t | 替换正确 |
| 35 | cnalphanumonly-filter.md | apply them to a  field when defining a collection schema. This allows Milvus to process the text in that field using the specified analy | 替换正确 |
| 36 | pattern-matching.md | ession assigned to . You can use the same filter expression syntax in Milvus operations that accept a scalar filter, such as , , and hyb | 替换正确 |
| 37 | decay-ranker-overview.md | pplied to both standard vector search and hybrid search operations in Milvus. Below are the key code snippets for implementing this feat | 替换正确 |
| 38 | tiered-storage-overview.md | To reduce the first-hit latency introduced by [lazy load], Milvus provides a *Warm Up* mechanism. | 替换正确 |
| 39 | vertex-ai.md | Before Milvus can call Vertex AI, it needs access to your GCP service acc | 部署或凭证配置语境 |
| 40 | milvus_backup_cli.md | If you run an empty local Milvus instance at the default port, use the example Python script | Milvus 专属页面 |

合计：替换正确 24；Milvus 专属页面 8；部署或凭证配置语境 8。
