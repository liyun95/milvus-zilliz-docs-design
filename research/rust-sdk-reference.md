# Rust SDK Reference 接入调研（2026-10-29）

本文为 Rust SDK Reference 从 web-content 生成到 zdoc 做准备：先列出已经定下的前提和两边的现状，再按问题列出可选做法和依据。讨论中定下的结论记在“讨论结论”一节，之后写进设计文档。

固定输入：web-content [`5cf99ab`](https://github.com/milvus-io/web-content/commit/5cf99ab)（2026-10-29），zdoc master [`6cf9e3020`](https://github.com/zilliztech/zdoc/commit/6cf9e3020)、dev（2026-10-29）。只读取，未修改任何仓库。

## 已定的前提

来自 2026-10-26 与文档负责人的会议（会前稿与纪要在飞书中）：

- Rust 是 Phase 1 中 SDK Reference 的试点：Cloud 上还没有 Rust 手册，不涉及从飞书迁移；以后其他 SDK 也迁到 shared-docs，REST 最后。
- 原文是 web-content 的 `API_Reference/milvus-sdk-rust/`，不经过飞书，也不经过 milvus-docs。
- shared-docs 按 Fetch 的发布组分子目录（WP8c 已实现），每组有自己的 `source.yaml`，可以指向不同的上游仓库。
- 在 zdoc 现有框架上扩展，不改框架的能力。
- 中文由现有的机器翻译从 dev 生成，SDK Reference 不做人工校对。
- SDK 的 Base 链接不能像 Guides 那样换成页面目录地址：激活只为 Guides 表实现（文档负责人的 agent，2026-10-28）。

## 讨论结论（2026-10-29）

推动者在讨论中定下，整体设计再与文档负责人对一遍（见“需要向文档负责人确认的事”）后进入实现：

| 问题 | 结论 | 依据 |
|---|---|---|
| 版本 | 只做 v3.0.x | Cloud 上每个 SDK 只发布一个版本：Go 的 v3.0 是 `active`，v2.6 只为 v3.0 缺少的页面补位（`fallback`），输出只有一棵目录树 |
| 发布哪些内容 | 手册配置中按模块（目录）和页面列出不发布的部分；FileResources 照现有 SDK 发布 | 见下方“模块与页面的差异” |
| 原文 | 直接读 web-content 的 `API_Reference/milvus-sdk-rust/v3.0.x/` | 它是手写的原文（web-content 的 AGENTS.md：“hand-curated”），不是 md2md 的输出；不改 web-content，也不改 Milvus 的发布流程 |
| 正文中的产品名 | “Milvus Rust SDK”“`milvus::`”这类 SDK 名称保留；版本号（“Milvus 2.6.17 or later”）与同时说两种部署的句子（“open-source Milvus …”）保留；指代服务端的“Milvus server”“Milvus instance”等，由上游逐步改成中性的说法 | Rust 正文中共 24 处，约 14 处指代服务端；推动者认为 Cloud 的 Go Reference 保留这些说法是历史文档没有处理好 |
| 残留的严重程度 | 连接值残留：构建失败。措辞残留：只警告，照常生成，在上游更新 PR 的说明与构建摘要中列出位置。产品名检查要能按组设置严重程度，Guides 组不变 | 整本手册只有一个 lock，一处措辞问题就会卡住全部页面的更新；措辞不影响使用，连接值会让用户连不上 |
| 配置粒度 | 整本手册一份配置、一个 `lock.yaml`；工具读取时在内存中展开成每页一份的虚拟页面配置，之后的生成步骤照原样复用 | 一次提交常常改几十页；页面之间互相链接多；整本手册应来自同一个 commit |
| 配置文件名 | `shared-docs/rust/manual.yaml`，与 zdoc `registry.ts` 中“手册”（manual）的叫法一致；`publish` 下只写 `manual: rust`，地址前缀、标题后缀从 `registry.ts` 取，不在配置中重复 | `registry.ts` 已登记每本手册的地址前缀、文档路径与显示名 |
| 地址与标题 | 沿用现有 SDK 的规则：`/reference/rust/rust/<模块>-<页面>`，不加 `v2-` 这一层；标题取 H1，后缀 `\| Rust` | Go、Java 的 `v2-`、Python 的 `MilvusClient` 是历史上多代 API 留下的；Rust 只有一套 API |
| `last_modified` | 写 `FALSE` | 网站的 `DocMetaTags.tsx` 取三个版本字段中最大的一个，显示为 “Minimum SDK version”；全部写 `v3.0.x` 会让 v2.6 就有的方法也显示 v3.0.x |
| `added_since` | 页面在 v2.6.x 目录中也有，写 `v2.6.x`，否则写 `v3.0.x` | 两个版本目录的文件名已统一 |
| `description` | 取 H1 下的第一段 | — |
| 元数据覆盖 | 只开放 4 个字段：`beta` 可以按模块（`defaults`）或按页面（`overrides`）设置；`deprecate_since`、`added_since`、`description` 只能按页面设置。页面级优先于模块级，模块级优先于默认值。其他字段由规则生成，不开放 | Cloud 上 5 个 SDK 共 1040 页：`beta` 基本按模块（各 SDK 的 Snapshot 为 `ON REQUEST`）；`deprecate_since` 只有 C++ 的 2 页；`added_since` 少数精确到小版本 |
| 页面内容的定制 | 不支持页面内的 `add` / `replace` / `remove`。Cloud 的定制只有：按模块或页面不发布、代码中的连接值认回变量、产品名检查（措辞只警告）、元数据覆盖、Cloud 自己的着陆页 | 变换都要以原文中的命名块为目标；web-content 中没有命名块，也定了不改 web-content |
| 在哪里生成 | 新增 `rust` 分组，放进现有的 `produce_sdk_reference` 矩阵，不新建任务；fetch 一步调用 shared-docs 生成，validate、publish 两步与其他 SDK 共用 | `fetch-docs.yml` 中各 SDK 分组都跑 `_fetch-content-group.yml` 的 `publish-group` 三步 |
| 原文来源的类型 | 在 `registry.ts` 中新增一种来源类型（如 `shared('shared-docs/rust')`）：按 lock 中的 commit 取 web-content 原文，用 shared-docs 生成，写到 `content/en/reference/api/rust/rust/`。workflow 中几处 `$GROUP != rest` 的判断改为按“没有飞书来源”判断 | web-content 不在 zdoc 仓库中，不能像 REST 那样读 master 中的文件；`_fetch-content-group.yml` 要求 REST 以外的分组都有飞书快照 |
| 上线 | 手册登记合并后的第一次 Fetch 就写入 dev；发版前在 UAT 上检查。不做开关、不做手册级的通道 | UAT 与 Prod 用同一个 dev SHA，Prod 只在发版时更新；Rust 是新手册，没有切换与归属的问题 |
| 新手册的 7 步 | 按 `manuals/README.md` 手工走一遍，写成任务卡中的清单。dev 上的初始内容（内容、`rust.sidebar.js`、`localization-inputs.inventory.json`）用 `shared-docs build` 的输出，由文档负责人放到 dev；翻译分组在 master 上改 | `content/`、`generated/` 归 dev，master 的检查会拦下，同步也不会搬；README 写明新手册的初始内容只能由维护者手工放 |
| 工作包 | 两个：WP-R1 只改 shared-docs（手册配置、展开、front matter、连接值、产品名检查的严重程度、排除、侧边栏、`build` 输出），发 FYI；WP-R2 做 Fetch 与上线（来源类型、分组、workflow 的判断、登记、着陆页、7 步），需要文档负责人评审 | R1 的输出可以在 PR 校验中看到，拿真实结果与文档负责人讨论 R2 |
| 着陆页 | 不用 `About.md`；照其他 SDK，由 Cloud 写一份，放在 master，登记在 `masterAuthoritativePaths` | Go 的 `go.md` 由 Cloud 编写，有 “Connect to Zilliz Cloud” 一节 |
| 连接值 | 把已展开的 Milvus 值认回变量，再换成 Cloud 的值；替换后仍残留 Milvus 值时构建失败 | 见下方说明 |

**连接值的做法。** web-content 中的 `http://localhost:19530`、`root:Milvus` 就是 milvus-docs `Variables.json` 中 `example_endpoint`、`example_token` 的 Milvus 值，相当于变量已经按 Milvus 展开过。生成 Cloud 版时：

1. 只在代码块中，把这几个已知的 Milvus 值认回对应的变量，不碰产品名，避免改到 `milvus::` 这类 crate 名；
2. 按 Cloud 的变量换成 `YOUR_CLUSTER_ENDPOINT` 等；
3. 替换后页面中仍有 `localhost:19530` 或 `root:Milvus` 时构建失败，上游出现新写法时能马上发现。

涉及 4 页：`Client/ConnectConfig.md`、`Client/MilvusClientV2.md`、`DataImport/BulkImport.md`、`CDC/update_replicate_configuration.md`。

**模块与页面的差异。** 对照 web-content 各 SDK 的 v3.0.x 与 Cloud 上的同一 SDK：

| 差异 | 情况 |
|---|---|
| ResourceGroup 模块 | web-content 的 Node、Go、C++、Rust 都有；Cloud 上所有 SDK 都没有 |
| CDC 模块 | web-content 的 Go、C++、Rust 有；Cloud 只有 Go 有，C++ 没有 |
| 模块中的个别页面 | Go 中 Cloud 不发布的：副本管理（`DescribeReplica`、`TransferReplica`、`ReplicaInfo`）、`UpdateReplicateConfiguration`、`ExportSnapshot`、GPU 索引与部分只在自建部署中使用的索引类型 |
| Cloud 独有的模块 | Python、Java 有 Volume，web-content 没有；Rust 不涉及 |

所以排除要能按模块，也要能按页面。不发布的页面被别的页面链接时，链接怎样处理，在设计中定。

## 现状

### web-content 中的 Rust Reference

| 项目 | 现状 |
|---|---|
| 版本 | `v2.6.x`（122 个文件）、`v3.0.x`（164 个文件） |
| 目录（v3.0.x） | Authentication 30、Collections 35、Management 31、Vector 18、Snapshots 11、ResourceGroup 8、Database 7、Partitions 7、DataImport 5、CDC 4、Client 4、FileResources 3，外加 `About.md` |
| 文件名 | 方法页用 snake_case（`create_user.md`），类型页用 PascalCase（`RowPolicyType.md`）。10-27 与 10-29 有三次“Format check”提交，统一过标题、文件名与枚举页 |
| front matter | 没有。标题取 H1，如 `# create_user()` |
| 链接 | 全部是相对的 `.md` 链接，如 `Ids.md`、`../Collections/ConsistencyLevel.md`；外部链接只有 4 处 GitHub |
| 图片、提示框 | 没有。`![` 的匹配都是 Rust 的 `vec![…]` |
| 连接值 | 5 页写死了 `localhost:19530` 或 `root:Milvus`：`About.md`、`Client/ConnectConfig.md`、`Client/MilvusClientV2.md`、`DataImport/BulkImport.md`、`CDC/update_replicate_configuration.md` |
| 产品名 | 16 页的正文写了 “Milvus”，如 “Milvus server”“Milvus version”“Milvus Rust SDK” |
| 更新频率 | 10-26 到 10-29 共 5 次提交（版本升级到 3.0.3、格式整理） |

<details>
<summary>页面示例：create_user.md</summary>

````markdown
# create_user()

Creates a user account with a username and password.

```rust
pub async fn create_user(&self, request: CreateUserRequest) -> Result<()>
```

The caller must have the corresponding administrative privilege. Milvus can accept RBAC
management calls with authorization disabled; ...

## Request Syntax
...
**REQUEST FIELDS:**

- `username: String`
...
## Example
...
````

</details>

### zdoc 中现有的 SDK Reference

| 项目 | 现状（以 Go 为例） |
|---|---|
| 手册登记 | `packages/docs-tooling/src/manuals/registry.ts`：cli、cpp、go、java、node、python、rest，没有 rust |
| 原文来源 | 飞书：每个 SDK 版本一个 Drive 文件夹（`remote('drive', …)`），中文为 `local('content/zh-CN/…')`。REST 是例外：`rest('…/openapi')`，从 master 中的 OpenAPI 文件生成，不经过飞书 |
| 输出位置 | `content/en/reference/api/go/go/v2/v2-Authentication/v2-Authentication-CreateUser.md` |
| front matter | `title: "CreateUser \| Go \| v2"`、`slug: /go/go/v2-Authentication-CreateUser`、`added_since`、`last_modified`、`beta`、`keywords`、`sidebar_position`、`displayed_sidebar: goSidebar`。`added_since` 等来自飞书 Base 的记录 |
| 侧边栏 | `generated/en/sidebars/<手册>.sidebar.js`，由 Fetch 生成 |
| 着陆页 | `content/en/reference/api/go/go/go.md`，归 master 维护，登记在 `masterAuthoritativePaths` |
| Cloud 与 Milvus 的目录差异 | Cloud 的 Go 没有 ResourceGroup；有 CDC、FileResources、Snapshot。Management 拆成了 Management 与 Management-Index。DataImport 15 页，比 web-content 多 5 页 |
| 新增手册的步骤 | `manuals/README.md` 的 7 步：登记 → 重新生成派生的工具文件 → 着陆页 → 静态约定（侧边栏恢复列表、路径过滤、翻译分组）→ 首次在 dev 上放种子 → Fetch → 同步。文档说明“目前没有自动的新手册命令” |
| Fetch 分组 | `workflows/groups.ts`：all、guides、python、java、node、go、cli、rest、cpp |

### shared-docs 中可以复用的部分

| 模块 | 能否用于 Rust |
|---|---|
| 按 commit 读原文、`lock.yaml`、写 lock 与 PR 校验的工作流（WP3、WP8） | 可以，`source.yaml` 指向 web-content 即可 |
| md2md 预处理（变量、片段） | web-content 的原文没有变量；要用，需要 web-content 改写原文，并且 milvus.io 的构建要能处理变量 |
| 站点适配（WP4） | 是为 Guides 写的：Tabs 规则、提示框、`\| Cloud` 后缀。Reference 的 front matter、标题后缀（`\| Rust \| v2`）、slug 规则都不同 |
| 链接换算（WP5） | 按 `links.yaml` 与文件名找 Cloud 页面；Reference 内部的相对链接要换成 Reference 的 slug，规则不同 |
| 产品名检查（WP6） | 可以，规则放在组目录中 |
| 变换（WP10） | 可以，但要在 web-content 中加命名块 |
| Fetch 接入（WP9） | 以 Guides 表为单位，按 `Docs` 链接分流；Rust 没有飞书记录，不走这条路 |
| 写死的 Guides 路径 | `sharedPageBundle.js`、`sharedPagePublication.js` 中写死了 `content/en/(guides\|byoc)/tutorials/`（文档负责人审 WP9a 时的 P2），接入第二个组前要改 |

## 问题与可选做法

### 1. 范围

| 问题 | 可选 | 依据 |
|---|---|---|
| 版本 | A. 只做 v3.0.x；B. v2.6.x 与 v3.0.x 都做 | Cloud 上每个 SDK 只发布一个版本（Go：v3.0 为 active，v2.6 只为缺少的页面补位）；Rust 在 Cloud 上是新手册，没有旧版本要保留 |
| 目录 | A. 全部发布；B. 按 Cloud 的 Go 的做法排除 ResourceGroup；C. 再逐个核对 CDC、FileResources、Snapshots 在 Cloud 上是否可用 | 已确认 Cloud 不支持 file resource（2026-10-28），但 Cloud 的 Go Reference 仍有 FileResources 目录；Go 的做法与产品实际不完全一致 |
| 语言 | A. 只做英文，中文由机器翻译生成；B. 中文暂不发布 | 已定中文走机器翻译；需要确认新手册加入翻译分组的步骤（7 步中的第 4 步） |

### 2. 页面配置的粒度

| 可选 | 内容 | 代价 |
|---|---|---|
| A. 每页一份，和 Guides 一样 | 每页 `page.yaml` + `lock.yaml` | 164 页就是 328 个文件；web-content 一次提交常常改几十页，每页一个上游更新 PR 太多 |
| B. 整个手册一份 | 一份手册配置（版本目录、排除的目录与页面、Cloud 规则）+ 一个 `lock.yaml` | 现有的 lock、写 lock 工作流和上游更新（WP12）都按页面设计，要支持“一个 lock 管一个目录” |
| C. 每个版本一份 | 与 B 相同，按版本各一份 | 两个版本分别跟踪 web-content 的同一个分支，lock 可能总是相同 |

### 3. Cloud 的差异怎样表达

| 差异 | 可选 | 依据 |
|---|---|---|
| 连接值（5 页） | A. web-content 改用变量，md2md 展开；B. zdoc 中按整个手册定义替换规则（如 `http://localhost:19530` → `YOUR_CLUSTER_ENDPOINT`）；C. 每页用代码行变换 | A 要 milvus.io 的构建支持变量；B 是新的规则类型，Guides 中没有；C 只涉及 5 页，但每次上游改代码都可能找不到定位行 |
| 正文中的产品名（16 页） | A. web-content 改用 `{{var.product_name}}`；B. 手册级的替换规则；C. 产品名检查只放行，不替换 | “Milvus server”“Milvus version”这类说法在 Cloud 上需要改写，不能只是放行 |
| 不适用于 Cloud 的方法 | A. 按目录或页面排除；B. 在 web-content 中加命名块，用 `remove` | 现在看到的差异都是整页或整个目录，没有页面内部的差异 |

### 4. front matter 与侧边栏

| 字段 | 可选 | 依据 |
|---|---|---|
| `title`、`slug`、`sidebar_label`、`displayed_sidebar` | 按目录和文件名生成，规则仿照其他 SDK（`<方法> \| Rust \| v2`、`/rust/rust/v2-<目录>-<页面>`） | 需要和文档负责人确认 slug 规则；生成后不能再改，否则 URL 变化 |
| `added_since`、`last_modified` | A. 按页面在哪些版本目录中出现推出（只在 v3.0.x 中的为 `v3.0.x`）；B. 在手册配置中按页面写；C. 新建飞书 Base 记录 | 其他 SDK 来自 Base；Rust 不经过飞书，C 会把飞书带回这条线 |
| `beta`、`keywords` | A. 手册级的默认值；B. 按页面写在配置中 | Go 的 `keywords` 是固定的几个词加方法名与版本标记 |
| `sidebar_position` 与侧边栏 | A. 按 web-content 的目录和文件名排序；B. 在配置中写顺序 | web-content 没有排序信息，milvus.io 的侧边栏由它自己的构建生成 |

### 5. 接入 Fetch 与上线

| 问题 | 可选 | 依据 |
|---|---|---|
| 在哪里生成 | A. 新增一个 Fetch 分组 `rust`，在这个分组中调用 shared-docs 生成；B. 加进现有的某个分组 | 其他 SDK 都是一个手册一个分组；分组决定 dev 中归它写的路径 |
| 原文来源的类型 | A. 在 `registry.ts` 中新增一种来源类型（如 `shared`），由 shared-docs 生成；B. 仿照 REST 的 `rest(…)`，读 master 中的文件 | REST 已经是“不经过飞书、从仓库文件生成”的先例；A 要改来源类型的定义，需要确认是否属于“改框架” |
| 怎样上线 | A. 手册登记后的第一次 Fetch 就发布；B. 加一个开关，开关打开后才写 dev，并写入 `active.json`；C. 先只在 UAT 显示（整本手册的通道） | 文档负责人的 agent 提出过“开关 + `active.json`”；Rust 是新手册，没有旧页面需要归属保护 |
| 新手册的 7 步 | A. 按 README 手工走一遍；B. 把其中可以自动的步骤做进工具 | README 的“常见错误”列了 8 种失败，每一种都来自真实运行 |
| 着陆页 | A. 用 web-content 的 `About.md` 生成；B. 照其他 SDK，着陆页写在 master，登记在 `masterAuthoritativePaths` | 会上提到着陆页现在在 dev 上特批维护，迁到 shared-docs 后可以来自原文；`About.md` 中有 Quick Start 和写死的连接值 |

### 6. 工作包怎样划分

| 可选 | 内容 |
|---|---|
| A. 一个工作包 | 组目录与手册配置、生成、Fetch 分组、新手册的 7 步一起做 |
| B. 两个工作包 | 先做 shared-docs 侧：手册配置、front matter、链接、Cloud 规则、`build` 输出，可以在 PR 校验中看到结果；再做 Fetch 侧：分组、来源类型、上线方式、7 步 |
| C. 先手工上线一次 | 用 `shared-docs build` 生成后，按 7 步手工放进 dev，Fetch 接入以后再做 |

## 需要向文档负责人确认的事

| 事项 | 我们的方案 |
|---|---|
| 新增来源类型、手册级的 lock，是否算改框架 | 在 `registry.ts` 中新增一种来源类型；整本手册一个 `lock.yaml`，上游更新开一个 PR |
| workflow 中 `$GROUP != rest` 的判断 | 改为按“没有飞书来源”判断 |
| 地址与标题 | `/reference/rust/rust/<模块>-<页面>`，不加 `v2-`；标题后缀 `\| Rust` |
| 不发布的模块与页面 | 先照 Go：ResourceGroup、副本管理；CDC、Snapshots 逐页核对 |
| Snapshots 的 `beta` | 照其他 SDK 写 `ON REQUEST` |
| 着陆页 | 由 Cloud 编写，放在 master，登记在 `masterAuthoritativePaths` |
| 上线 | 手册登记合并后的第一次 Fetch 就写入 dev，发版前在 UAT 检查 |
| dev 上的初始内容 | 由我们准备 `shared-docs build` 的输出，请文档负责人放到 dev |
