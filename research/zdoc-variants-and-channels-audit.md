# zdoc 产品代码变体与发布通道核验

日期：2026-10-12。目的：确认 zdoc 现有的产品差异与 Current/Next 机制，判断共享内容能否复用。只读取源码与说明，未运行构建或部署。

| 仓库 | 分支 | 固定修订 |
|---|---|---|
| zilliztech/zdoc | dev | `784788d3aa0064d4c0f1c448a6ab4865ce2f7130` |
| zilliztech/zdoc | master | `3777ec0b322546d716485e8f88da8412b0265e71`（文件清单） |
| milvus-io/milvus-docs | v3.0.x | `7d87b0bf26d7cbc713f40af6453ea2f925367901` |

## 1. 产品代码变体

[CODE_VARIANTS.md](https://github.com/zilliztech/zdoc/blob/784788d3aa0064d4c0f1c448a6ab4865ce2f7130/packages/docs-tooling/src/lark/CODE_VARIANTS.md) 规定代码块内的产品指令：

- 指令体：`include-next-line TARGET`、`exclude-next-line TARGET`、`include-start TARGET` / `include-end`、`exclude-start TARGET` / `exclude-end`。
- 指令独占一行，可用 `#`、`//`、`/* */`、`<!-- -->`、`{/* */}` 五种注释形式；指令行与被排除的行整行删除，不留空行。
- 目标包括 `zilliz`、`saas`、`paas`、`milvus`，按点分目标规则匹配。
- 规范的第一个示例就是 `integration_id`（zilliz）与 `credential`（milvus）二选一。
- 产品过滤在 Fetch 阶段执行，当前输入是飞书文档。实现为 `codeVariantFilter.js`，其测试 10 项通过（见[复用审计](./md2md-zdoc-reuse-audit.md)）。
- 段落内的产品过滤沿用 HTML 形式的 `<include target>` / `<exclude target>` 标签。

**对共享方案的结论：** 代码行差异可以沿用这套语法写在共享原文中。Cloud 侧需要在 Git 输入上调用同一过滤器；Milvus 发布链需新增相同语法的过滤，删除 `zilliz` 等非 Milvus 目标的行并移除指令行。段落级差异不采用源内标签，仍由 zdoc 的命名块变换处理。

## 2. 发布通道（Current / Next）

同一构建同时包含 Current 与 Next 内容，部署时按通道过滤，因此 UAT 与 Prod 可以使用同一镜像。

| 粒度 | 写法 | 实现 |
|---|---|---|
| 整页 | 飞书多维表格记录的 `Release Channel` 字段（`CURRENT` / `NEXT` / `RETIRE-IN-NEXT`，新记录默认 `NEXT`），Fetch 渲染为 front matter `channel: next` | `apps/docs/plugins/release-channel-routes`；说明见 zdoc [README](https://github.com/zilliztech/zdoc/blob/784788d3aa0064d4c0f1c448a6ab4865ce2f7130/README.md) |
| 内容块 | 飞书正文中的 `<NextChannel action="include">…</NextChannel>`；`action="exclude"` 包住上线后要被替换的旧说法；上线时去掉标签（promotion） | `packages/docs-ui/.../NextChannel`、`apps/docs/plugins/next-channel-view.js` |
| 代码行 | `next-channel-next-line`、`next-channel-start` / `-end`，以及对应的 `current-channel-*` | `packages/docs-ui/.../ChannelCode` |

- 产品过滤在 Fetch 阶段执行，通道过滤在渲染阶段执行，两者可以叠加。
- `.md` 副本、`llms.txt` 等静态产物按 Current 视图输出；未闭合的 include 块按失败关闭处理，避免未发布内容泄漏。
- 整页通道的来源是飞书多维表格字段，除读取页面自身 front matter 外，还按飞书文档 `token` 传递到各语言译文，避免旧译文漏标。Git 来源页面既没有多维表格记录也没有飞书 token，接入时需要等价的通道字段与页面身份。

**对共享方案的结论：** Cloud 自有片段可以直接使用 `<NextChannel>`；整页通道可放在 Cloud 页面配置中；共享原文中需要只在 Next 显示的内容，由 zdoc 用 `<NextChannel>` 包裹对应命名块，原文不写通道标记。仍需与文档负责人确认此类情况的频率与常见粒度。

## 3. OpenAI 页对照

对照 [Milvus 原文](https://github.com/milvus-io/milvus-docs/blob/7d87b0bf26d7cbc713f40af6453ea2f925367901/site/en/userGuide/embeddings-reranking/embedding-function/openai.md)与 [Cloud 页面](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/content/en/guides/tutorials/development/function/text-embedding-functions/openai.md)：

| 内容 | Milvus | Cloud | 判断 |
|---|---|---|---|
| 前提条件 | “Configure credentials”：`milvus.yaml` 或环境变量配置 API key | “Before you start”：在控制台创建模型提供方集成并获取 integration ID | 真实差异，整节 |
| 函数凭证参数 | 注释掉的可选 `"credential": "apikey_dev"` | 必填 `"integration_id": "YOUR_INTEGRATION_ID"` | 真实差异，各语言各一行 |
| 模型表与说明 | 一致，标题为 “Choose an embedding model” | 一致，标题为 “Model choices” | 历史漂移 |
| 示例语言 | 仅 Python | Python、Java、NodeJS、Go、cURL、C++ | 历史漂移 |
| 覆盖步骤 | 定义 schema 与函数，后续步骤链接到 Function Overview | 另有建索引、建 collection、插入与搜索 | 历史漂移 |

Cloud 的 Cohere、Voyage AI embedding 页及对应 ranker 页属于同一模式；milvus-docs v3.0.x User Guide 中有 17 个文件使用 `"credential"`。
