# SDK Reference 产品需求（Rust 试点）

**状态**：草稿，2026-10-30 与文档负责人讨论（会议文档在飞书，与本文同步）。会上定下的结论写回本文后，并入[产品需求](./prd.md)，系统行为届时编号并写进 `requirements.json`。工程细节见[技术设计 10](./design/10-sdk-reference.md)，调研见 [Rust SDK Reference 接入调研](../research/rust-sdk-reference.md)。

**方案**：Rust SDK Reference 直接从 web-content 生成到 zdoc，不经过飞书，也不改 web-content 和 Milvus 的发布流程。整本手册一份配置，放进 Fetch 现有的 SDK 分组；手册登记合并后，第一次 Fetch 就写入 dev。

## 会上要定的事

| 事项 | 我们的方案 | 结论 |
|---|---|---|
| 新增来源类型 | `registry.ts` 的来源类型里加 `shared`：Fetch 的 fetch 一步遇到它时，调用 shared-docs 生成页面（见场景 R4） | |
| workflow 里 REST 的例外 | `_fetch-content-group.yml` 里写死的 `$GROUP != rest`（除 REST 外每个分组都必须有飞书快照），改成按“这个分组没有飞书来源”判断 | |
| 地址与标题 | `/reference/rust/rust/<模块>-<文件名>`，不加 `v2-`；标题后缀 `\| Rust`。上线后不能再改 | |
| 不发布的模块与页面 | 先照 Go 排除 ResourceGroup，副本管理也在这个模块里；CDC、Snapshots 逐页核对 | |
| 页面里的 `token` 填什么 | 每个 zdoc 页面的 front matter 都有 `token`（原本是飞书文档 ID）和 `type`（来源类型）。Rust 没有飞书文档，照已上线的 Guides 共享页，填 `token: shared-rust-<模块>-<文件名>`、`type: origin`。请确认翻译、修订记录、侧边栏等工具不要求它是真实的飞书 ID | |
| dev 上的初始内容 | 新手册第一次 Fetch 前，dev 上要先有页面、侧边栏、清单文件三样（原因见场景 R4）。照 C++ 的先例，我们准备一个分支，请文档负责人检查后放进 dev；中文侧边栏是否也要放 | |
| Phase 1 不区分 current / next | 上游更新 PR 同时改这两个值。SDK Reference 写的是已经发布的 SDK，不需要先只在 UAT 显示 | |
| 以后迁移其他 SDK | 每个 SDK 一个组目录，各有自己的 `source.yaml`、`Variables.json`、lock，与 Fetch 的分组一一对应 | |

## 概述

### 背景

2026-10-26 与文档负责人定了：Rust 作为 SDK Reference 的试点，原文来自 web-content，shared-docs 按 Fetch 分组建子目录。之后 Guides 已有 16 篇接入、15 篇激活，其中第三批是第一批用变换的生产页面。

### 范围

- 只做 web-content 中的 `API_Reference/milvus-sdk-rust/v3.0.x/`，164 页；Cloud 上每个 SDK 只发布一个版本。
- 只做英文，中文由现有的机器翻译从 dev 生成。
- 不改 web-content 的写法，不改 milvus.io 的构建与 Milvus 的发布流程。
- Rust 在 Cloud 上还没有手册，不涉及从飞书迁移与切换。

### 与 Guides 的区别

| | Guides 共享页 | Rust SDK Reference |
|---|---|---|
| 原文 | milvus-docs，有变量与命名块 | web-content，手写维护，没有变量与命名块 |
| 配置 | 每页一份 `page.yaml`、一个 `lock.yaml` | 整本手册一份 `manual.yaml`、一个 `lock.yaml` |
| Cloud 的差异 | 变量、页面内的增加 / 替换 / 删除 | 按模块或页面排除、连接值认回变量、元数据的例外；不支持页面内的定制 |
| 上线 | 换掉飞书表格中的 `Docs` 链接 | 在 `registry.ts` 登记手册，第一次 Fetch 即写入 dev |
| 上游更新 | 每页一个 PR，UAT 可以先于 Prod | 整本手册一个 PR，两者一起更新 |

### 整体流程

web-content（`API_Reference/milvus-sdk-rust/v3.0.x/`，手写维护）→ 按 `lock.yaml` 中的 commit 读取 → 生成 Rust 页面（展开成每页一份、连接值换成 Cloud 的值、站点适配、链接、产品名检查）→ Fetch 的 `rust` 分组 → 校验与发布，写入 dev，中文机器翻译 → Cloud 文档站（UAT 检查，发版上 Prod）。手册配置与着陆页在 zdoc master。

## 一本手册的文件

Rust 是 shared-docs 中的一个组，组目录放在 zdoc master：

```
shared-docs/rust/
  source.yaml          # 上游仓库与跟踪分支：web-content，master（写一次）
  manual.yaml          # 手册配置（文档工程师）
  lock.yaml            # 采用的 web-content commit（工具写入）
  Variables.json       # Cloud 的连接值（文档工程师，写一次）
  product-names.yaml   # 产品名检查规则（文档工程师）
```

| 谁写 | 文件 | 在哪里 | 写什么 | 什么时候 |
|---|---|---|---|---|
| 不改 | Rust 原文 | web-content `API_Reference/milvus-sdk-rust/v3.0.x/` | — | 由上游维护 |
| 文档工程师 | `source.yaml` | zdoc master `shared-docs/rust/` | 上游仓库 web-content，跟踪分支 master | 接入时写一次 |
| 文档工程师 | `manual.yaml` | 同上 | 原文目录、不发布的模块与页面、原文中写死的 Milvus 值、元数据的例外 | 接入时写；以后排除页面、改元数据都改这里 |
| 文档工程师 | `Variables.json` | 同上 | Cloud 的连接值，如 `YOUR_CLUSTER_ENDPOINT` | 接入时写一次 |
| 文档工程师 | `product-names.yaml` | 同上 | 检查哪些写法，每条是失败还是警告 | 接入时写；发现新写法时补 |
| 文档工程师 | 着陆页 `rust.md` | zdoc master `content/en/reference/api/rust/rust/` | Cloud 版的 SDK 介绍，包括怎样连接 Zilliz Cloud | 接入时写；登记为 master 维护，与其他 SDK 相同 |
| 工具 | `lock.yaml` | zdoc master `shared-docs/rust/` | 采用的 web-content commit | 接入 PR 中由 bot 写入，与 Guides 相同；之后由上游更新 PR 修改 |
| 工具 | 生成的页面、侧边栏、记录文件 | zdoc dev | — | 每次 Fetch |
| 一次性搭建 | `registry.ts` 登记、`rust` 分组、workflow 中的判断、翻译分组等 | zdoc master 的工具代码 | — | WP-R2，一次 |
| 一次性搭建 | dev 上的初始内容 | zdoc dev | 页面、侧边栏、清单文件，见场景 R4 | 第一次 Fetch 前，一次 |

**以后迁移其他 SDK：** 每个 SDK 一个组目录（`shared-docs/go/`、`shared-docs/python/`……），各有自己的 `source.yaml`、`Variables.json` 和 lock。这些文件在各 SDK 之间几乎相同，但每个 SDK 可以各自更新、各自失败：Go 的上游有问题，不会卡住 Rust。这也与 Fetch 一个 SDK 一个分组相对应。

## 场景 R1：接入一本手册

**谁**：文档工程师

**用户故事**：作为文档工程师，我在 zdoc 中为一本 SDK Reference 写一份手册配置，就能从 web-content 生成整本手册的 Cloud 版本，不用逐页配置，也不用复制正文。

**怎样操作**

1. 在 zdoc master 新建 `shared-docs/rust/`，写 `source.yaml`、`Variables.json`、`product-names.yaml`。
2. 写 `manual.yaml`，例子见下方。
3. 提交 PR，不写 `lock.yaml`：bot 取 web-content master 的最新提交写入同一个 PR，然后生成全部页面做校验。
4. 在 PR 校验中查看生成结果，通过后合并。合并后网站上还看不到 Rust，见场景 R4。

```yaml
# shared-docs/rust/manual.yaml

# 配置格式的版本，固定为 1
schema_version: 1

# 原文在上游仓库中的位置
source:
  # 这本手册的原文目录：目录下的每个 .md 是一页，一级子目录是一个模块
  dir: API_Reference/milvus-sdk-rust/v3.0.x
  # 上一个版本的目录，只用来推出 added_since：两个目录都有的页面写 v2.6.x
  previous: API_Reference/milvus-sdk-rust/v2.6.x

# 发布到哪本手册
publish:
  # registry.ts 中登记的手册 ID；地址前缀、标题后缀、侧边栏名都从登记中取
  manual: rust

# 不发布的内容；没有列出的模块和页面都发布，新增的页面也自动发布
exclude:
  # 不发布的模块，即 source.dir 下的一级目录
  modules: [ResourceGroup]
  # 不发布的页面，路径相对于 source.dir
  pages: [About.md]            # 着陆页由 Cloud 编写

# 原文中写死的 Milvus 值，键是 Variables.json 中的变量名
# 生成时只在代码块中，把这些值换成同名变量的 Cloud 值
milvus_values:
  example_endpoint: "http://localhost:19530"
  example_token: "root:Milvus"

# 元数据的例外，只写和默认值不同的地方
# 以 / 结尾的是模块，对模块下的每一页生效；.md 结尾的是一页；同一字段以页面为准
metadata:
  Snapshots/:
    beta: ON REQUEST
  Collections/add_collection_function.md:
    deprecate_since: v3.0.x
```

**`manual.yaml` 的字段**

| 字段 | 必填 | 写什么 |
|---|---|---|
| `schema_version` | 是 | 固定为 `1` |
| `source.dir` | 是 | 原文目录，相对于上游仓库根目录。目录下每个 `.md` 是一页，一级子目录是一个模块 |
| `source.previous` | 否 | 上一个版本的目录，只用来推出 `added_since` |
| `publish.manual` | 是 | `registry.ts` 中的手册 ID |
| `exclude.modules` | 否 | 不发布的模块 |
| `exclude.pages` | 否 | 不发布的页面，路径相对于 `source.dir` |
| `milvus_values.<变量名>` | 否 | 这个变量在原文中写死的 Milvus 值；变量名与 `Variables.json` 中的一致 |
| `metadata.<模块>/` | 否 | 对整个模块生效的元数据，只能写 `beta` |
| `metadata.<页面>.md` | 否 | 对一页生效的元数据，可以写 `beta`、`deprecate_since`、`added_since`、`description` |

**生成后的页面**（以 `Authentication/create_user.md` 为例）

| 字段 | 规则 | 结果 |
|---|---|---|
| 地址 | `/reference/rust/rust/<模块>-<文件名>` | `/reference/rust/rust/Authentication-create_user` |
| `title` | H1，加 `\| Rust` | `create_user() \| Rust` |
| `description` | H1 下的第一段，加 `\| Rust` | `Creates a user account with a username and password. \| Rust` |
| `added_since` | 页面在 v2.6.x 中也有：`v2.6.x`；否则 `v3.0.x` | `v2.6.x` |
| `last_modified` | `FALSE`。网站取三个版本字段中的最大值，显示为 “Minimum SDK version”；写 `v3.0.x` 会让 v2.6 就有的方法也显示 v3.0.x | `FALSE` |
| `beta`、`deprecate_since` | 默认 `false`，`metadata` 中可以改 | `false` |
| 侧边栏 | 模块按目录名、模块内按文件名的字母顺序，不区分大小写，与 Go、C++ 现在的顺序一致 | Authentication 模块下，按文件名排序 |

**出错时**：整本手册只有一个 lock，任何一处错误都会让这次更新整体失败：PR 校验不通过，Fetch 中保留 dev 上现有的版本。各种错误见[技术设计 10](./design/10-sdk-reference.md#出错时)。

## 场景 R2：写 Cloud 的差异

**用户故事**：作为文档工程师，我不改 web-content，就能让 Cloud 版不出现只适用于 Milvus 的模块和连接值。

| 差异 | 写在哪里 | 怎样写 |
|---|---|---|
| 不适用于 Cloud 的模块或页面 | `manual.yaml` 的 `exclude` | `modules` 列模块，`pages` 列页面。新出现的模块和页面默认发布，在上游更新 PR 中单独列出，由审核的人决定是否排除。其他页面链接到被排除的页面时，链接变成文字，只给提示 |
| 代码中的连接值 | `manual.yaml` 的 `milvus_values` 与 `Variables.json` | `milvus_values` 记变量在原文中写死的 Milvus 值，`Variables.json` 记它的 Cloud 值，两者都是“变量名 → 值”。工具只在代码块中把前者换成后者。涉及 4 页；替换后仍残留 Milvus 值时失败 |
| 正文中的产品名 | `product-names.yaml` | 见下表 |
| 元数据 | `manual.yaml` 的 `metadata` | `beta` 可以按模块或按页面；`deprecate_since`、`added_since`、`description` 只能按页面 |
| 着陆页 | 着陆页 `rust.md` | 由 Cloud 编写，不用原文的 `About.md` |

| 产品名的写法 | 例子 | 处理 |
|---|---|---|
| SDK 的名字 | “Milvus Rust SDK”、`milvus::` | 放行 |
| 服务端的版本 | “require Milvus 2.6.17 or later” | 放行 |
| 同时讲两种部署 | “open-source Milvus with files, Zilliz Cloud object storage with …” | 放行 |
| 指代服务端 | “the connected Milvus server”、“a specific Milvus instance”（约 14 处） | 只警告，照常发布；上游逐步改成中性的说法 |
| 连接值残留 | `localhost:19530`、`root:Milvus` | 失败 |

**不支持页面内的增加、替换、删除。** Guides 的变换都以原文中的命名块为目标，web-content 中没有命名块，也定了不改 web-content。以后确实需要时，可以在 web-content 中加命名块、复用 Guides 的变换。

## 场景 R3：审核上游更新

**用户故事**：作为文档工程师，web-content 的 Rust 原文更新后，我在一个 PR 中看到整本手册的变化，决定是否采用。

- 工具对整本手册开一个滚动更新的 PR，不按页面拆；同时改 `lock.yaml` 中的 `current` 与 `next`，合并后下一次 Fetch 写入 dev，发版时上 Prod。
- PR 中列出改动的页面与生成结果的差异；新增、删除、改名的页面及因此改变的地址；产品名警告；新出现的模块。
- 生成失败时 PR 照样开，标明失败原因；dev 上保持已采用的版本。

## 场景 R4：上线

**用户故事**：作为文档工程师，接入的配置合并后，我知道 Rust 什么时候、经过哪些步骤出现在 Cloud 网站上。

1. **工程接入（WP-R2）合并**：在 `registry.ts` 登记 `rust` 手册，来源类型为 `shared`；`rust` 分组放进 Fetch 的 SDK 矩阵；着陆页登记为 master 维护；加进翻译分组。
2. **放初始内容**：我们准备一个分支 `seed/rust-reference`，从 dev 拉出，只加三样：页面（`content/en/reference/api/rust/rust/…`）、侧边栏（`generated/en/sidebars/rust.sidebar.js`）、清单文件（`deploy/contracts/localization-inputs.inventory.json`），都用 `shared-docs build` 生成。文档负责人检查后放进 dev。
3. **第一次 Fetch**：写入 dev，之后由 Fetch 正常维护。
4. **UAT 检查，发版上 Prod**：UAT 与 Prod 构建同一个 dev SHA，Prod 只在发版时更新。

**为什么要放初始内容**：Fetch 生成页面前，要求这本手册的侧边栏文件已经在 dev 上；而这个文件本来要由 Fetch 生成，第一次跑时还不存在，第一次 Fetch 会失败。zdoc 的新手册都这样处理：C++ 手册当初由维护者直接提交到 dev（提交 `07ae595c5`，“seed C++ reference content, sidebar, and localization inventory”）。这三样不能经 master 提交：`content/`、`generated/` 归 dev，master 的检查会拦下，同步也不会搬。

## 分工与节奏

1. **WP-R1，只改 shared-docs**：手册配置、生成、连接值、产品名检查、排除规则。做完后，PR 校验里就能看到 164 页的生成结果。
2. **WP-R2，接入 Fetch 与上线**：场景 R4 第 1 步的全部内容，需要文档负责人评审。
3. **上线**：场景 R4 第 2–4 步。
