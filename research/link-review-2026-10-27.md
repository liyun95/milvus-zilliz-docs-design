# 链接映射表待判断条目（2026-10-27）

用 `shared-docs links-seed` 在 milvus-docs `v3.0.x` `d6311836` 与 zdoc dev `9b2db5d` 上生成。User Guide 中被链接的 Milvus 页面共 197 个：同名 65 个（不用登记），工具已给出结果 93 个（标题相同 51、反推 5、按类别指向 milvus.io 37），**待人工判断 39 个**，见下表。

每一行在“决定”一栏填三种之一：Cloud 页面标识（如 `filtering-overview`）、`https://milvus.io/docs/<文件名>`，或“不登记”（这一页暂不接入共享页，遇到时再定）。

“被链接”是 User Guide 中链接到它的页面数，越多越先定。


## A. 自部署工具（Birdwatcher、CDC、Backup）（7 个）

建议：`https://milvus.io/docs/<文件名>`：Cloud 没有这些自部署工具

| Milvus 页面 | 标题 | 被链接 | 工具找到的相近 Cloud 页 | 决定 |
|---|---|---:|---|---|
| `cdc_failover.md` | Failover | 2 | `switchover-and-failover`（Switchover and Failover） | |
| `cdc_switchover.md` | Switchover | 2 | `switchover-and-failover`（Switchover and Failover） | |
| `set_up_cdc_replication.md` | Set Up CDC Replication | 2 | `setup-a-private-link-aws`（Set up a PrivateLink (AWS)）, `setup-console-ip-allowlist`（Set Up Console IP Allowlist）, `setup-whitelist`（Set up Cluster IP Allowlist） | |
| `birdwatcher_usage_guides.md` | Use Birdwatcher | 1 | `use-bulkwriter`（Use BulkWriter）, `use-mmap`（Use mmap）, `use-large-topk`（Use Large TopK） | |
| `bulk_import_in_cdc_replication.md` | Bulk Import in CDC Replication | 1 | `zilliz-import-prompts`（Import）, `import-data`（Import Data）, `import-data-on-web-ui`（Import Data (Console)） | |
| `milvus_backup_overview.md` | Milvus Backup | 1 | `create-backup`（Create Backup）, `backup-to-other-regions`（Cross-Region Backup）, `export-backup-files`（Export Backup Files） | |
| `milvus_cdc_overview.md` | Milvus CDC | 1 | `elasticsearch-queries-to-milvus`（Elasticsearch Queries to Milvus）, `migrate-from-milvus`（Migrate from Milvus to Zilliz Cloud）, `via-endpoint`（Migrate from Milvus to Zilliz Cloud Via Endpoint） | |

## B. 安装页面（2 个）

建议：`https://milvus.io/docs/<文件名>`：Cloud 不需要安装

| Milvus 页面 | 标题 | 被链接 | 工具找到的相近 Cloud 页 | 决定 |
|---|---|---:|---|---|
| `install_standalone-helm.md` ⚠ 反推结果指向的 Cloud 页已不存在 | Install Milvus Standalone with Kubernetes | 1 | `install-sdks`（Install SDKs） | |
| `install_standalone-operator.md` ⚠ 反推结果指向的 Cloud 页已不存在 | Install Milvus Standalone with Milvus Operator | 1 | `install-sdks`（Install SDKs） | |

## C. Embedding 与 Reranking 的服务商页面（14 个）

建议：看 Cloud 是否有对应页（相近页常是 `function-and-model-inference-overview` 或某个服务商页）；没有就指向 milvus.io

| Milvus 页面 | 标题 | 被链接 | 工具找到的相近 Cloud 页 | 决定 |
|---|---|---:|---|---|
| `embedding-function-overview.md` | Embedding Function Overview | 11 | `function-and-model-inference-overview`（Function Overview）, `analyzer-overview`（Analyzer Overview）, `bm25-function`（BM25 Function） | |
| `model-ranker-overview.md` | Model Ranker Overview | 8 | `decay-ranker-oveview`（Decay Ranker Overview）, `analyzer-overview`（Analyzer Overview）, `boost-ranker`（Boost Ranker） | |
| `hugging-face-tei.md` | Hugging Face TEI | 3 | `hugging-face`（Hugging Face）, `hugging-face-ranker`（Hugging Face Ranker） | |
| `embeddings.md` | Embedding Overview | 2 | `analyzer-overview`（Analyzer Overview）, `function-and-model-inference-overview`（Function Overview）, `use-array-of-structs`（StructArray Overview） | |
| `tei-ranker.md` | TEI Ranker | 2 | `boost-ranker`（Boost Ranker）, `cohere-model-ranker`（Cohere Ranker）, `reranking-rrf`（RRF Ranker） | |
| `azure-openai.md` | Azure OpenAI | 1 | `openai`（OpenAI）, `integrate-with-azure-blob-storage`（Integrate with Azure Blob Storage）, `setup-a-private-link-azure`（Set up a Private Link (Azure)） | |
| `bedrock.md` | Bedrock | 1 | — | |
| `dashscope-ranker.md` | DashScope Ranker | 1 | `boost-ranker`（Boost Ranker）, `cohere-model-ranker`（Cohere Ranker）, `reranking-rrf`（RRF Ranker） | |
| `dashscope.md` | DashScope | 1 | — | |
| `siliconflow-ranker.md` | SiliconFlow Ranker | 1 | `boost-ranker`（Boost Ranker）, `cohere-model-ranker`（Cohere Ranker）, `reranking-rrf`（RRF Ranker） | |
| `siliconflow.md` | SiliconFLow | 1 | — | |
| `vertex-ai.md` | Vertex AI | 1 | `voyage-ai`（Voyage AI）, `zilliz-ai-prompts`（AI Prompts）, `voyage-ai-model-ranker`（Voyage AI Ranker） | |
| `vllm-ranker.md` | vLLM Ranker | 1 | `boost-ranker`（Boost Ranker）, `cohere-model-ranker`（Cohere Ranker）, `reranking-rrf`（RRF Ranker） | |
| `yandex-cloud.md` | Yandex Cloud | 1 | `cloud-providers-and-regions`（Cloud Providers & Regions）, `faq-account`（FAQ: Account | CLOUD）, `faq-authentication`（FAQ: Authentication | CLOUD） | CLOUD）, faq-authentication（FAQ: Authentication | CLOUD） | |

## D. 其他功能页（16 个）

建议：逐条判断：Cloud 有对应页就填页面标识；Cloud 不支持的功能指向 milvus.io

| Milvus 页面 | 标题 | 被链接 | 工具找到的相近 Cloud 页 | 决定 |
|---|---|---:|---|---|
| `clustering-compaction.md` | Clustering Compaction | 4 | `k-means-clustering`（K-Means Clustering） | |
| `manage-file-resources.md` | Manage File Resources | 4 | `manage-aliases`（Manage Aliases）, `manage-cluster`（Manage Cluster）, `manage-invoice`（Manage Invoices） | |
| `index-vector-fields.md` | Index Vector Fields | 3 | `index-struct-array`（Index StructArray Fields）, `nullable-fields`（Nullable Fields）, `use-binary-vector`（Binary Vector） | |
| `eviction.md` | Eviction | 2 | — | |
| `index-scalar-fields.md` | Index Scalar Fields | 2 | `index-struct-array`（Index StructArray Fields）, `nullable-fields`（Nullable Fields）, `tune-index-build-level`（Tune Index Build Level） | |
| `limitations.md` | Milvus Limits | 2 | `struct-array-limits`（StructArray Limits）, `external-collection-limits`（External Collection Limits）, `limits`（Zilliz Cloud Limits） | |
| `manage_databases.md` | Database | 2 | `database-concept`（Database Explained）, `database`（Database in Serving Clusters）, `on-demand-database`（Database for On-Demand Search） | |
| `synonym-filter.md` | Synonym | 2 | — | |
| `tiered-storage-overview.md` | Tiered Storage Overview | 2 | `analyzer-overview`（Analyzer Overview）, `data-import-storage-options`（Storage Options）, `function-and-model-inference-overview`（Function Overview） | |
| `decimaldigit-filter.md` | Decimal Digit | 1 | — | |
| `full_text_search_with_milvus.md` | Using Full-Text Search with LangChain and Milvus | 1 | `full-text-search`（Full Text Search）, `tutorial-colbert-colpali`（Search with EmbeddingLists: ColBERT and ColPali）, `filtered-search-with-struct-arrays`（Filtered Search with StructArray） | |
| `idempotent-import.md` | Idempotent Bulk Import | 1 | `zilliz-import-prompts`（Import）, `import-data`（Import Data）, `import-data-on-web-ui`（Import Data (Console)） | |
| `prepare-source-data.md` | Prepare Source Data | 1 | `use-milvus-snapshot-as-data-source`（Use Snapshot as Data Source）, `data-backfill`（Data Backfill）, `data-resilience`（Data Resilience） | |
| `search_with_svs_vamana.md` | Search with SVS Vamana and Milvus | 1 | `tutorial-colbert-colpali`（Search with EmbeddingLists: ColBERT and ColPali）, `filtered-search-with-struct-arrays`（Filtered Search with StructArray）, `grouping-search-with-struct-array`（Grouping Search with StructArray） | |
| `snapshot-use-cases.md` | Snapshot Use Cases | 1 | `use-milvus-snapshot-as-data-source`（Use Snapshot as Data Source）, `use-bulkwriter`（Use BulkWriter）, `use-mmap`（Use mmap） | |
| `warm-up.md` | Warm Up | 1 | `setup-a-private-link-aws`（Set up a PrivateLink (AWS)）, `setup-console-ip-allowlist`（Set Up Console IP Allowlist）, `setup-whitelist`（Set up Cluster IP Allowlist） | |

<details>
<summary>工具已给出结果的 93 条（扫一眼即可，有错的标出来）</summary>

```yaml
"array-of-structs.md": "use-array-of-structs" # same title; same title: use-array-of-structs; inferred votes: use-array-of-structs (1)
"array-operators.md": "array-filtering-operators" # same title; same title: array-filtering-operators; inferred votes: array-filtering-operators (8)
"array_data_type.md": "use-array-fields" # same title; same title: use-array-fields; inferred votes: use-array-fields (2)
"basic-operators.md": "basic-filtering-operators" # same title; same title: basic-filtering-operators; inferred votes: basic-filtering-operators (7)
"basic-vector-search-with-structarray.md": "search-with-struct-array" # same title; same title: search-with-struct-array; inferred votes: search-with-struct-array (14)
"bin-ivf-flat.md": "https://milvus.io/docs/bin-ivf-flat.md" # category
"binary-vector.md": "use-binary-vector" # same title; same title: use-binary-vector; inferred votes: use-binary-vector (3)
"bitmap.md": "bitmap-index-type" # same title; same title: bitmap-index-type; inferred votes: bitmap-index-type (2)
"boolean.md": "filtering-overview" # same title; same title: filtering-overview; inferred votes: filtering-overview (5)
"cohere-ranker.md": "cohere-model-ranker" # same title; same title: cohere-model-ranker
"configure-docker.md": "https://milvus.io/docs/configure-docker.md" # category
"configure-helm.md": "https://milvus.io/docs/configure-helm.md" # category
"configure_common.md": "https://milvus.io/docs/configure_common.md" # category
"configure_datacoord.md": "https://milvus.io/docs/configure_datacoord.md" # category
"configure_datanode.md": "https://milvus.io/docs/configure_datanode.md" # category
"configure_operator.md": "https://milvus.io/docs/configure_operator.md" # category
"configure_proxy.md": "https://milvus.io/docs/configure_proxy.md" # category
"configure_querycoord.md": "https://milvus.io/docs/configure_querycoord.md" # category
"create-collection.md": "manage-collections-sdks" # inferred; inferred votes: manage-collections-sdks (1)
"create-structarray-field.md": "create-struct-array" # same title; same title: create-struct-array; inferred votes: create-struct-array (15)
"decay-ranker-overview.md": "decay-ranker-oveview" # same title; same title: decay-ranker-oveview; inferred votes: decay-ranker-oveview (2)
"default-values.md": "default-fields" # same title; same title: default-fields; inferred votes: default-fields (2)
"dense-vector.md": "use-dense-vector" # same title; same title: use-dense-vector; inferred votes: use-dense-vector (4)
"diskann.md": "https://milvus.io/docs/diskann.md" # category
"dynamic_config.md": "https://milvus.io/docs/dynamic_config.md" # category
"filtered-search-with-structarray.md": "filtered-search-with-struct-arrays" # same title; same title: filtered-search-with-struct-arrays; inferred votes: filtered-search-with-struct-arrays (10)
"geometry-field.md": "use-geometry-field" # same title; same title: use-geometry-field; inferred votes: use-geometry-field (3)
"glossary.md": "https://milvus.io/docs/glossary.md" # category
"gpu-brute-force.md": "https://milvus.io/docs/gpu-brute-force.md" # category
"gpu-cagra.md": "https://milvus.io/docs/gpu-cagra.md" # category
"gpu-index-overview.md": "https://milvus.io/docs/gpu-index-overview.md" # category
"gpu-ivf-flat.md": "https://milvus.io/docs/gpu-ivf-flat.md" # category
"gpu-ivf-pq.md": "https://milvus.io/docs/gpu-ivf-pq.md" # category
"gpu_index.md": "https://milvus.io/docs/gpu_index.md" # category
"grouping-search-with-structarray.md": "grouping-search-with-struct-array" # same title; same title: grouping-search-with-struct-array; inferred votes: grouping-search-with-struct-array (5)
"hnsw-pq.md": "https://milvus.io/docs/hnsw-pq.md" # category
"hnsw-prq.md": "https://milvus.io/docs/hnsw-prq.md" # category
"hnsw-sq.md": "https://milvus.io/docs/hnsw-sq.md" # category
"hnsw.md": "https://milvus.io/docs/hnsw.md" # category
"hybrid-search-with-structarray.md": "hybrid-search-with-struct-array" # same title; same title: hybrid-search-with-struct-array; inferred votes: hybrid-search-with-struct-array (4)
"index-explained.md": "indexes" # inferred; inferred votes: indexes (1)
"index-structarray-fields.md": "index-struct-array" # same title; same title: index-struct-array; inferred votes: index-struct-array (15)
"index.md": "https://milvus.io/docs/index.md" # category
"insert-data-into-structarray-fields.md": "insert-struct-array" # same title; same title: insert-struct-array; inferred votes: insert-struct-array (7)
"insert-update-delete.md": "insert-entities" # same title; same title: insert-entities; inferred votes: insert-entities (1)
"install-pymilvus.md": "https://milvus.io/docs/install-pymilvus.md" # category
"install_cluster-helm.md": "https://milvus.io/docs/install_cluster-helm.md" # category
"install_cluster-milvusoperator.md": "https://milvus.io/docs/install_cluster-milvusoperator.md" # category
"install_standalone-docker.md": "https://milvus.io/docs/install_standalone-docker.md" # category
"inverted.md": "inverted-index-type" # same title; same title: inverted-index-type; inferred votes: inverted-index-type (2)
"ivf-flat.md": "https://milvus.io/docs/ivf-flat.md" # category
"ivf-pq.md": "https://milvus.io/docs/ivf-pq.md" # category
"ivf-rabitq-fastscan.md": "https://milvus.io/docs/ivf-rabitq-fastscan.md" # category
"ivf-rabitq.md": "https://milvus.io/docs/ivf-rabitq.md" # category
"ivf-sq8.md": "https://milvus.io/docs/ivf-sq8.md" # category
"json-operators.md": "json-filtering-operators" # same title; same title: json-filtering-operators; inferred votes: json-filtering-operators (3)
"keyword-match.md": "text-match" # same title; same title: text-match; inferred votes: text-match (8)
"language-identifier.md": "language-identifier-tokenizer" # same title; same title: language-identifier-tokenizer; inferred votes: language-identifier-tokenizer (4)
"load-and-release.md": "load-release-collections" # same title; same title: load-release-collections; inferred votes: load-release-collections (2)
"metric.md": "search-metrics-explained" # same title; same title: search-metrics-explained; inferred votes: search-metrics-explained (5)
"mmap.md": "use-mmap" # same title; same title: use-mmap; inferred votes: use-mmap (3)
"modify-collection.md": "modify-collections" # same title; same title: modify-collections; inferred votes: modify-collections (3)
"multi-vector-search.md": "hybrid-search" # same title; same title: hybrid-search; inferred votes: hybrid-search (8)
"ngram.md": "ngram-index-type" # same title; same title: ngram-index-type; inferred votes: ngram-index-type (3)
"nullable-and-default.md": "nullable-fields" # same title; same title: nullable-fields; inferred votes: nullable-fields (10)
"number.md": "use-number-field" # inferred; inferred votes: use-number-field (3)
"pattern-matching.md": "pattern-match" # same title; same title: pattern-match; inferred votes: pattern-match (7)
"primary-field.md": "primary-field-auto-id" # same title; same title: primary-field-auto-id; inferred votes: primary-field-auto-id (3)
"random-sampling.md": "ramdom-sampling" # same title; same title: ramdom-sampling; inferred votes: ramdom-sampling (1)
"range-search-with-structarray.md": "range-search-with-struct-arrays" # same title; same title: range-search-with-struct-arrays; inferred votes: range-search-with-struct-arrays (5)
"rbac.md": "https://milvus.io/docs/rbac.md" # category
"removepunct-filter.md": "remove-punct-filter" # same title; same title: remove-punct-filter; inferred votes: remove-punct-filter (4)
"rrf-ranker.md": "reranking-rrf" # same title; same title: reranking-rrf; inferred votes: reranking-rrf (2)
"rtree.md": "rtree-index-type" # same title; same title: rtree-index-type; inferred votes: rtree-index-type (1)
"scalar_index.md": "https://milvus.io/docs/scalar_index.md" # category
"scann.md": "https://milvus.io/docs/scann.md" # category
"schema-hands-on.md": "schema-design-hands-on" # same title; same title: schema-design-hands-on; inferred votes: schema-design-hands-on (2)
"schema.md": "schema-explained" # same title; same title: schema-explained; inferred votes: schema-explained (2)
"search-with-embedding-lists.md": "tutorial-colbert-colpali" # same title; same title: tutorial-colbert-colpali; inferred votes: tutorial-colbert-colpali (4)
"sparse-inverted-index.md": "https://milvus.io/docs/sparse-inverted-index.md" # category
"sparse_vector.md": "use-sparse-vector" # same title; same title: use-sparse-vector; inferred votes: use-sparse-vector (6)
"stl-sort.md": "slt-sort-index-type" # same title; same title: slt-sort-index-type; inferred votes: slt-sort-index-type (3)
"storage-v3.md": "https://milvus.io/docs/storage-v3.md" # category
"string.md": "use-string-field" # same title; same title: use-string-field; inferred votes: use-string-field (2)
"struct-array-operators.md": "struct-array-filtering" # same title; same title: struct-array-filtering; inferred votes: struct-array-filtering (9)
"structarray-limits.md": "struct-array-limits" # same title; same title: struct-array-limits; inferred votes: struct-array-limits (16)
"text.md": "use-text-field" # same title; same title: use-text-field; inferred votes: use-text-field (3)
"timestamptz-field.md": "use-timestamptz-field" # same title; same title: use-timestamptz-field; inferred votes: use-timestamptz-field (5)
"tune_consistency.md": "consistency-level" # same title; same title: consistency-level; inferred votes: consistency-level (1)
"tutorial-implement-a-time-based-ranking-in-milvus.md": "tutorial-implement-time-based-ranking" # inferred; inferred votes: tutorial-implement-time-based-ranking (4)
"use-json-fields.md": "json-field-overview" # inferred; inferred votes: json-field-overview (1)
"voyage-ai-ranker.md": "voyage-ai-model-ranker" # same title; same title: voyage-ai-model-ranker
"weighted-ranker.md": "reranking-weighted-reranker" # same title; same title: reranking-weighted-reranker; inferred votes: reranking-weighted-reranker (3)
```

</details>
