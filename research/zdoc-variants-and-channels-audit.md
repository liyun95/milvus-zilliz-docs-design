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

**后续决定（2026-10-12）：** 为避免 Cloud 的代码进入 Milvus 原文、Milvus 发布链新增过滤，共享原文不写产品指令；代码行差异改由 zdoc 在页面配置中按连续整行定位处理，见[接口设计 02《共享页配置》](../docs/interfaces/02-page-config.md)。上面的结论保留为核验记录。

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

**后续建议（2026-10-12）：** 包裹命名块只适合“新增一段”；修改已有内容时 Prod 无法保留旧文，细碎改动也难以逐处加命名块。建议改为 lock 记录 `current` 与 `next` 两个版本，由工具按块比较并成对生成 `<NextChannel>`，见[接口设计 04《通道与 commit 记录》](../docs/interfaces/04-channels-and-lock.md)。上面的结论保留为核验记录。

### 2.1 补充核验（2026-10-14）

为定义 lock（[接口设计 04《通道与 commit 记录》](../docs/interfaces/04-channels-and-lock.md)），在 zdoc master [`eb9827c`](https://github.com/zilliztech/zdoc/tree/eb9827c054a87e75e84d33817e5b7f52e2761ff9) 与 milvus-docs 上补充核对：

| 事实 | 来源 |
|---|---|
| UAT 与 Prod 部署同一镜像，通道在容器启动时由 `ZDOC_RELEASE_CHANNEL` 注入，默认 `current` | zdoc README “Release Channel gating” |
| 提升按页进行：整页在多维表格中把 `NEXT` 改为 `CURRENT` 后重新 Fetch；块级去掉 `<NextChannel>` 标签 | 同上 |
| 分支归属：`content`、`generated`、`i18n`、snapshot 等路径归 dev，只由发布工作流写入；其余由 master 管理，经同步 PR 进入 dev | [`master-tooling-sync.json`](https://github.com/zilliztech/zdoc/blob/eb9827c054a87e75e84d33817e5b7f52e2761ff9/deploy/contracts/master-tooling-sync.json) |
| 飞书来源的 source snapshot 按记录保存 `doc_token`、`source_hash`、`release_channel` 等字段 | [`sourceSnapshot.js`](https://github.com/zilliztech/zdoc/blob/eb9827c054a87e75e84d33817e5b7f52e2761ff9/packages/docs-tooling/src/lark/sourceSnapshot.js) |
| milvus-docs 默认分支为 `v3.0.x`，2026-07-14 起提交超过 100 个 | GitHub API |
| milvus-docs `preview` 分支相对 `v3.0.x` 多 265 个、少 1424 个提交；近期合并的 40 个 PR 中 18 个合入 `preview`、20 个合入 `v3.0.x` | GitHub API |
| zdoc 的标题锚点由生成器按标题文字算出并显式写入（如 `## Authentication\{#authentication}`），英文 Guides 中有 2609 个；标题改名即锚点改变 | `larkDocWriter.js` 的 `__heading` |
| zdoc 英文内容中指向三个试点页锚点的链接共 3 处：2 处 `delete-entities#delete-entities-from-partitions`，1 处 `openai#model-choices` | 源码检索 |
| milvus-docs 的 `check-link.js` 在 PR 中运行，比较链接前去掉 `#` 之后的部分，不校验锚点 | `check-link.js` |
| milvus.io 的标题锚点保留大小写（Delete Entities 页为 `#Delete-Entities-by-Filtering-Conditions`），docs.zilliz.com 全部小写（如 `#insert-entities-into-a-partition`） | 两站页面 DOM，2026-10-15 |
| milvus-docs 中跨页带锚点的链接 284 个，其中 274 个含大写；指向本页标题的锚点 52 个含大写（其余小写的多为代码组的语言切换） | 源码检索 |
| milvus-docs 全站链接：页内锚点 2415、站内页面 2074、外部网站 1643、milvus.io 完整地址 455、以 `/` 开头的站内路径 26；User Guide 与 Embeddings 的 837 个站内页面链接中，32% 的目标在 Cloud 有同名页面 | 源码检索，与 zdoc 英文 Guides 的 366 个 slug 对比 |
| milvus-docs 全站图片：Milvus 存储 251、其他外部地址 136、仓库内文件 54；zdoc 英文 Guides 有 397 张图片在 zdoc 的阿里云 OSS，3 处直接引用 Milvus 存储 | 源码检索 |

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
