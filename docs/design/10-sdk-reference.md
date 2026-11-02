# 10 SDK Reference：从 web-content 生成（Rust 试点）

本篇定义怎样把 web-content 中的 SDK Reference 生成到 zdoc，先以 Rust 试点。要交付什么行为、文档工程师怎样写，见 [SDK Reference 产品需求](../prd-sdk-reference.md)；调研与选项见 [Rust SDK Reference 接入调研](../../research/rust-sdk-reference.md)。本篇只写工程上选定的做法。

**参与方**：zdoc 生成（shared-docs）、zdoc 发布（Fetch）。

**状态**：2026-11-02 会议及会后讨论已对齐，待实现：页内 `add / replace / remove`、zdoc 本地 Cloud 独有页面、整本手册 `current / next` 与提升。新增字段是拟实现的契约；外部接入仍需验证，见文末。

## 目标与范围

- **试点：** Rust SDK Reference。Cloud 上还没有 Rust 手册，不涉及从飞书迁移、切换与归属。以后其他 SDK 照同一条路迁过来，REST 最后。
- **原文：** web-content 的 `API_Reference/milvus-sdk-rust/v3.0.x/`。它在 web-content 中手写维护（web-content 的 `AGENTS.md`：“hand-curated”），不是 md2md 的输出，没有变量。
- **不改上游的发布：** 不改 milvus.io 的构建与 Milvus 的发布流程。web-content 在 Cloud 变换需要定位的地方加命名块（HTML 注释，milvus.io 不显示）。
- **只做 v3.0.x、只做英文。** 中文由现有的机器翻译从 dev 生成，不做人工校对。
- **与 Guides 的区别：** Guides 以页面为单位接入；SDK Reference 以整本手册为单位配置、锁定、校验和提升，复用其变换与通道机制。
- **Cloud 专属内容：** 完整页面与片段提交到 zdoc master。首版按核实过的能力清单覆盖专有方法、属性和对象；人或 agent 编写后经核验审核，Fetch 只读取已提交文件，不新增运行时生成正文的 agent 步骤。

## 约定

### 组目录

Rust 是 shared-docs 的一个组（技术设计 [02](./02-page-config.md#shared-docs-的位置)），与 Guides 的组目录结构不同：没有 `pages/`，一本手册一份配置、一个 lock。

```
shared-docs/rust/
  source.yaml          # 上游仓库与跟踪分支：web-content，master
  manual.yaml          # 手册配置
  lock.yaml            # 整本手册 current / next 的 web-content commit
  Variables.json       # Cloud 变量：连接值
  product-names.yaml   # 产品名检查规则
  content/             # Cloud 独有页面与页内片段，源文件由 master 维护
```

“manual”（手册）沿用 zdoc `packages/docs-tooling/src/manuals/registry.ts` 的叫法：网站上每一本可以独立导航的文档是一个 manual。

### 配置契约

四份作者配置的基本写法见 [PRD 场景 R1](../prd-sdk-reference.md#场景-r1接入一本手册)，差异与变换示例见 [R2](../prd-sdk-reference.md#场景-r2写-cloud-的差异)。这里只补充实现约束。

| 输入 | 约定 |
|---|---|
| `source.yaml` | 沿用 Guides 的 `schema_version / repository / track`；lock 与上游更新工具从这里发现 commit |
| `manual.yaml` | 必填 `schema_version: 1`、`source.dir`、`publish.manual`；`exclude`、`milvus_values`、`metadata`、`cloud_pages`、`transforms` 可省略；不支持 `source.previous` |
| 路径 | `source.dir` 相对于上游仓库；排除与变换的路径相对于 `source.dir`；本地页面用相同格式的手册内逻辑路径，元数据可引用两种来源。一级子目录为模块 |
| `metadata` | 模块仅可设 `beta`；页面可设 `beta / deprecate_since / added_since / description`。页面优先于模块，再取默认值 |
| `transforms` | 上游页面路径 → 变换列表；接受 `add / remove / replace`，复用 Guides 的 `target / content / position / channel` 及其操作约束；不引入通用变换或新字段 `replacement` |
| `cloud_pages` | 手册内逻辑路径 → `{ file, channel? }`；`file` 指向组内 `content/` 的完整 Markdown 页面，必须含 H1。`channel` 省略或为 `current` 表示两边存在，`next` 仅 UAT，`retire-in-next` 仅 Prod，映射到现有整页通道；与 Transform 的通道枚举和含义分别校验 |
| `Variables.json` | 沿用组级变量表；每个 `milvus_values` 键必须有同名字符串值，缺失或类型不符时配置校验失败 |
| `content.file` | 相对于 `manual.yaml` 所在目录，须位于该组 `content/` 内；解析真实路径后仍须在该目录内，拒绝绝对路径、越界及符号链接逃逸 |

`publish.manual` 必须在当前生成环境的 registry 中已登记。WP-R1 用测试登记做隔离生成验证，不修改生产 registry，也不跳过登记校验；WP-R2 提供真实登记后，才能完成正式配置 PR 的端到端生成校验。路径在两个锁定版本及本地页面的并集中校验；`exclude` 只作用于上游，不能用它覆盖同名页面。变换按通道检查目标，已排除页面不能配置变换，没有可执行页面的规则也报错。新增上游页面默认进入其所在通道，上游更新 PR 必须列出。

本地页的逻辑路径、输出地址不得与任一锁定版本的上游页面（包括排除项）、其他本地页或保留着陆页冲突。`cloud_pages.file` 沿用 `content.file` 的路径安全约束。本地页直接维护正文，不接受对它再配置 Transform。

### `lock.yaml`

格式与 Guides 的页面 lock 相同（技术设计 [04](./04-channels-and-lock.md#每页一份-lockyaml)），只是整本手册一份。接入时由工具取跟踪分支的最新提交写入，`current` 与 `next` 相同；上游更新只改 `next`，提升才让 `current` 跟上。commit 格式、可读取性与祖先关系校验沿用 Guides；不以 `none` 表示整本手册的状态。

lock 只固定上游原文。`manual.yaml`、变量表与 Cloud 文件只有一份，取本次生成固定的 zdoc 工具／配置 SHA；两次生成共用这些文件，通道差异由规则和标记表达，不增加两套本地快照。

### 生成

工具按 `current / next` 分别列举未排除的上游页面，加入该通道可见的 `cloud_pages`，建立整本手册的页面与链接清单，再展开成内存页面配置。上游页面共用同一个 lock，绑定各自的 Transform；本地页面读取 zdoc 文件，不伪造上游路径或 commit。读取、适配和校验尽量复用 Guides（技术设计 [02](./02-page-config.md)、[02b](./02b-links-and-images.md)、[07](./07-site-adaptation.md)）。不运行 md2md 的变量／片段／产品预处理或整仓生成；允许复用其现有命名块解析与去标记库，不另写一套解析器。

一页的处理顺序：

1. 按当前处理通道的 commit 读原文，或读取该通道可见的本地页面；
2. 对上游页筛选适用通道的 `add / remove / replace`，在带命名块的原文上定位，检查目标冲突和内容文件；
3. 执行变换，仅在保留的上游代码片段中映射连接值。本地页、Cloud 片段与 `content.lines` 均不经过映射；保留来源信息，之后清除命名块标记。不得先改连接值再匹配原文代码行；
4. 站点适配，生成 front matter；
5. 链接换算；
6. 产品名检查；
7. MDX 编译。

两边分别校验后复用 WP11 合并，差异用 `NextChannel` 表达；只在一边存在的页面使用整页通道，导航按部署通道处理，搜索与静态产物采用下文规定的 current 视图。配置可让相同 commit 产生不同输出，不得以 `current == next` 跳过通道处理。合并结果再次检查 MDX；手写标记落在生成的差异区域内按 `MERGE_NESTED_CHANNEL` 失败。两版 front matter 不同时沿用 current 并记入报告；next 独有页使用自己的元数据。

复用的是变换、合并等核心能力，SDK 需单独编排来源读取、front matter 和链接清单，不能直接套用要求两个 commit 都存在同一路径的 Guides 页面入口。UAT 对已有页面预览 next 正文，标题、描述等 front matter 仍取 current；整页通道为 next／retire-in-next 时沿用现有校验，禁止再包含块级 `NextChannel`。

### 地址、路径与 front matter

沿用现有 SDK 的规则，不加 `v2-` 这一层（Go、Java 的 `v2-`、Python 的 `MilvusClient` 是多代 API 留下的，Rust 只有一套）。以 `Authentication/create_user.md` 为例：

| 项目 | 规则 | 例子 |
|---|---|---|
| 输出路径 | `content/en/reference/api/rust/rust/<模块>/<模块>-<文件名>.md` | `…/rust/rust/Authentication/Authentication-create_user.md` |
| `slug` | `/rust/rust/<模块>-<文件名>` | `/rust/rust/Authentication-create_user`，网址 `/reference/rust/rust/Authentication-create_user` |
| `title` | H1，加后缀 `\| Rust` | `create_user() \| Rust` |
| `sidebar_label` | H1 | `create_user()` |
| `description` | H1 下的第一段，加后缀 `\| Rust`；`metadata` 可以改写 | `Creates a user account with a username and password. \| Rust` |
| `added_since` | 已确认的上游接口引入版本；`metadata` 可补充或更正；未知则不输出该字段 | 不从 `v3.0.x` 目录推断 |
| `last_modified` | `FALSE` | — |
| `deprecate_since` | 已确认的上游废弃版本；`metadata` 可补充或更正；未知为 `false` | — |
| `beta` | `false`；`metadata` 可以改写 | Snapshots 模块为 `ON REQUEST` |
| `keywords` | 复用 Fetch 的 `keyword_picker`，加上版本标记 `rustv30` | — |
| `displayed_sidebar` | 从 `registry.ts` 取 | `rustSidebar` |
| `sidebar_position` | 模块按目录名、模块内按文件名的字母顺序，不区分大小写 | — |
| `type`、`token` | 见“接入前待验证” | — |

- **生命周期。** 保留接口正文中明确的引入、变更内容和废弃说明；本地补充需要可核对的来源，记录在 PR 中。仅将可确定属于该接口、该 SDK 的引入／废弃版本写入上述字段，不把服务端版本要求转成 SDK 生命周期；正文表述不明确时保留原文，不猜版本。完整变更历史不压缩成 `last_modified`。WP-R1 必须验证缺省版本不被适配器补成目录版本；生命周期与 Cloud 发布通道独立。
- **生命周期展示。** Rust 的“最低 SDK 版本”只读 `added_since`，未知则不显示；`deprecate_since` 单独显示废弃提示，不能参与最低版本计算。例如 v3.0.0 引入、v3.1.0 废弃，最低版本仍为 v3.0.0；仅知道废弃版本时只显示废弃提示。现有 [DocMetaTags](https://github.com/zilliztech/zdoc/blob/34498a57295e3ab99327e9b00ddd767cab956f6a/packages/docs-ui/src/shared/theme/Heading/DocMetaTags.tsx#L38)取多个字段的最高版本，不能直接复用：WP-R1 负责正确输出元数据，WP-R2 负责按 Rust 手册身份接入此展示规则及中英文文案，保持其他 SDK 的现有行为。
- **地址变更须显式审核。** 地址由逻辑路径派生；上游改名或本地逻辑路径改动会产生候选地址变化，不能静默提升。更新 PR 列出旧／新地址及引用，按现有站点规则处理旧链接并验证后才可提升；不将“自动派生”视为旧地址永远稳定的保证。
- **侧边栏。** 输出 `generated/en/sidebars/rust.sidebar.js`，格式与其他 SDK 相同：最前面是着陆页，之后每个模块一个分类。由哪段现有代码生成（Fetch 的侧边栏生成，或 `reference/sidebarDerivation.ts`）在 WP-R2 的计划中确定；`sidebarDerivation.ts` 会按 front matter 的 `type: folder` 认分类的着陆页，`type` 的取值要与之相容。

### 链接

原文中的链接都是相对的 `.md` 链接，例如 `Ids.md`、`../Collections/ConsistencyLevel.md`。链接清单同时包含上游页和本地页，按通道校验目标及锚点；本地页按逻辑路径解析相对链接，片段按消费页面的逻辑路径解析。

| 链接指向 | 处理 |
|---|---|
| 手册内发布的页面 | 换成这一页的地址，锚点照 zdoc 的规则换算 |
| 手册内被排除的页面 | 去掉链接，保留文字，给出提示 `LINK_TARGET_EXCLUDED`，不失败 |
| 目标仅在另一通道存在 | 当前通道不输出可点击的失效链接，保留文字并提示；链接在目标可见的通道正常输出。手写通道块中的链接按其可见通道检查 |
| 手册之外的 `.md` | 生成失败（`LINK_UNKNOWN_FORM`）：Rust 的原文中没有这种链接，出现时由人判断 |
| 外部地址 | 不变 |

被排除的页面只给提示，是因为整本手册只有一个 lock：一处链接失败，会卡住全部页面的更新。

### 着陆页

不用原文的 `About.md`。照其他 SDK，由 Cloud 编写 `content/en/reference/api/rust/rust/rust.md`，放在 master，登记在 `deploy/contracts/master-tooling-sync.json` 的 `masterAuthoritativePaths` 与 `registry.ts` 的 `landingPage`。Go 的 `go.md` 就是这样，其中的 “Connect to Zilliz Cloud” 一节是 Cloud 独有的。

着陆页是单独维护的例外，不由上游 lock 控制；延后上线的段落仍须写通道标记，改动参与手册验收。它属于 master 保留文件，不混入生成器拥有的页面集合；指向被排除 About 页的链接仍按排除规则处理，不隐式改指着陆页。

## Cloud 的差异

| 差异 | 做法 |
|---|---|
| 不适用于 Cloud 的模块或页面 | `exclude` |
| 代码中的连接值 | 认回变量，换成 Cloud 的值 |
| 正文中指代产品的说法 | 由上游逐步改成中性的说法；zdoc 只警告 |
| 元数据 | `metadata` |
| 着陆页 | Cloud 编写 |
| 页面内 Cloud 不暴露的参数或代码行 | 命名块定位，`transforms` 中写 `remove` |
| 参数说明或调用方式不同 | 同样定位目标，写 `replace`，用 `content.file / content.lines` 提供 Cloud 内容 |
| 现有页面补充 Cloud 内容 | `add` 引用本地片段，复用 Guides 插入定位 |
| Cloud 独有完整页面 | `cloud_pages` 指向 zdoc 内的 Markdown 文件，直接参与整本生成 |

### 连接值

`milvus_values` 记上游写死的值，`Variables.json` 记同名键的 Cloud 值。只在保留的上游代码块中精确匹配，以同名键的 Cloud 值替换；不处理正文，不对新写入的 Cloud 内容做二次映射，也不要求上游使用变量占位符。

本期 `milvus_values` 的值为非空字符串；一个变量需要匹配多个写法时，先核对并统一上游示例，字符串列表扩展不在本次设计内。不同映射的源值相同或互相包含时配置失败，避免结果依赖执行顺序；按原文匹配一次，不对替换结果级联执行其他映射。

替换后由 `product-names.yaml` 扫描完整生成结果。连接值残留使整本手册失败（`PRODUCT_NAME_FOUND`），不能因它来自 Cloud 文件而跳过。调研涉及 `Client/ConnectConfig.md`、`Client/MilvusClientV2.md`、`DataImport/BulkImport.md`、`CDC/update_replicate_configuration.md` 四页。

### 产品名

| 写法 | 例子 | 处理 |
|---|---|---|
| SDK 的名字 | “Milvus Rust SDK”、`milvus::`、`milvus-sdk-rust` | 放行 |
| 服务端的版本 | “require Milvus 2.6.17 or later”、“Deprecated since Milvus 2.5.4” | 放行：Cloud 集群也用 Milvus 内核，版本说法成立 |
| 同时讲两种部署 | “open-source Milvus with `files`, Zilliz Cloud object storage with …” | 放行 |
| 指代服务端 | “the connected Milvus server”、“a specific Milvus instance” | 警告：照常生成，在构建摘要与上游更新 PR 中列出位置；上游改成中性的说法，例如 “the connected server” |
| 连接值 | `localhost:19530`、`root:Milvus` | 失败 |

`check` 保留现有字符串写法，等价于 `error`；新增 `{ text: <单行文本>, severity: error | warning }` 写法，对象中省略 `severity` 也按 `error`。`allow` 仍用字符串列表，匹配与放行语义沿用现有实现。未知严重程度或空文本使配置失败；warning 随诊断输出但不阻断生成。PRD 的起始示例仅列两条措辞，实际接入应覆盖调研中的约 14 处服务端称谓。Guides 现有配置与失败行为不变。

### 页面内的新增、删除与替换

支持块、语言、代码行三级 `add / remove / replace`，复用 WP10 的定位、冲突检查和缩进处理。`add` 在块或代码行前后插入必须写 `position: before / after`；添加一种语言不写 position，且该语言不能已存在。`remove / replace` 禁止 position。参数替换必须同时核对说明与调用示例，生成成功不代表 SDK／服务端支持该参数。

Rust 已知删除目标是 `Collections/load_collection.md` 的副本／资源组参数和示例、`Partitions/load_partitions.md` 的同类参数，以及 `Client/MilvusClientV2.md` 的 ResourceGroup 介绍。替换案例见 PRD R2，是配置示意，不新增未经核实的 Rust 方法需求。历史调研与参数差异证据保留在 research 中。

- **上游标记：** 三种变换都按上游命名块定位，由 web-content 维护者配合添加；其生成 skill 必须保留标记并在提交前检查成对、唯一、结构合法。zdoc 对目标缺失仍报错，不自动改用模糊匹配。具体上游接线需在接入时验证。
- **执行校验：** 先对原文定位全部目标，再执行变换。缺失或多义匹配、重叠规则、无效内容使整本手册失败。`target.lines / content.lines` 沿用 Guides：最多定位连续 5 行、忽略行首缩进及行尾空格、其余精确匹配，禁止空行、围栏和命名块，写回时恢复缩进。
- **内容形式：** 块或语言级新增／替换用 `content.file`；代码行级用 `content.lines`，两者不可同时提供。`remove` 不可提供内容，`add / replace` 必须提供与目标类型相符的内容。
- **Cloud 文件：** 放在组内 `content/`，使用 Markdown 和代码围栏；新增／替换一种语言时文件只含该语言的一个代码块。完整页面写 H1 与正文。直接写 Cloud 值，拒绝变量／片段占位符、命名块、手写 Tabs 和产品过滤指令；允许 `NextChannel`，按通道规则校验。本期不支持组内本地图片，外部图片沿用共享图片处理与校验。
- **链接：** Cloud 片段中的相对 `.md` 链接按消费页面目录解析；完整本地页按 `cloud_pages` 的逻辑路径解析，均非相对于物理 `content/`。使用包含两类页面的链接映射，复用片段时逐个消费页面检查。
- **依赖与来源：** 记录实际使用的 Cloud 文件及摘要，使文件变化触发重新生成并进入记录文件的输入身份；诊断指向 Cloud 文件或 `manual.yaml` 中的代码行。被覆盖原文的变化单独进入上游更新报告，不只比较生成输出。

## 接入 Fetch

### 来源类型与分组

- **登记：** `registry.ts` 中新增手册 `rust`，`kind: 'reference'`。英文的来源是新增的来源类型 `shared`，例如 `shared('shared-docs/rust')`；中文的来源与其他 SDK 相同，是 `local('content/zh-CN/reference/api/rust/rust')`。`manuals/schema.ts` 的 `sourceType` 增加 `shared`。
- **分组：** `workflows/groups.ts` 新增 `rust` 分组，进入 `fetch-docs.yml` 现有的 `produce_sdk_reference` 矩阵，不新建任务。
- **fetch 一步：** `publish-group --stage fetch` 遇到 `shared` 来源时，按 `lock.yaml` 的两个 commit 稀疏取 web-content 的 `source.dir`，结合固定工具／配置 SHA 中的本地文件生成两版合并产物，写到输出路径。validate、publish 两步与其他 SDK 共用。
- **记录文件：** 每次生成写一份独立的手册级记录，契约见下节。复用技术设计 [05](./05-publish-handoff.md#记录文件)的输入／输出摘要原则，不复用其单页 schema 或 validator。
- **不写 `active.json`：** Rust 没有飞书记录，没有切换与归属。

### 手册级记录与恢复

采用一种新的手册级 schema，不再附加逐页 receipt。记录放在 `generated/en/manifests/shared-manuals/rust.json`，与现有 Guides 记录分开。以下是必须表达的数据；WP-R1 在接口中固定字段类型与规范化摘要算法，WP-R2 按同一契约接入发布消费者。

| 层次 | 必须记录与验证的内容 |
|---|---|
| 类型与身份 | `kind: shared-manual`、独立 `schema_version: 1`、组与手册 ID、站点；未知类型或版本拒绝读取，不能落入 Guides 单页 validator |
| 输入 | 上游仓库、目录、current/next SHA，固定 zdoc 工具／配置 SHA，配置、变量、Cloud 文件及实际使用的图片和导航依赖摘要；不得只用上游 commit 作为缓存身份 |
| 页面集合 | 每页的逻辑路径、独立 token、来源种类和位置、整页通道、输出路径与字节摘要；上游来源记录实际存在的版本，本地来源记录 zdoc 文件，不伪造上游身份 |
| 手册产物 | 完整页面集合及其摘要、生成侧边栏等附属产物的路径和摘要；保留着陆页记为外部依赖，不宣称由生成器拥有 |

同一手册允许多页，但 token、逻辑路径和输出路径必须唯一；逐页核对 front matter 的身份与通道，并核对输出集合完整性，不能只检查已列出的文件。页面缺失、额外生成页、摘要不符或记录缺失都使候选发布失败。输入身份与最终输出摘要必须在发布前认证，不能仅因为 JSON 能解析就采用。

WP-R1 提供记录数据模型、生成和纯校验；WP-R2 把记录路径纳入该分组的 checkpoint 归属、保留产物、最终认证、恢复和完整性检查。页面、侧边栏及记录必须作为同一候选结果被保留和恢复；删除页面沿用 Reference reconciliation 的证据链，不能因新记录不再列出就跳过删除核验。适配现有 SDK 发布／恢复入口，不扩建发布架构；保持 Guides 的记录与校验不变。

### 搜索与其他派生产物

Phase 1 的 Rust 搜索统一使用 **current 视图**，UAT 与 Prod 均不承诺能搜到 next 专有内容；UAT 可通过导航和直接地址验收 next。此范围只约束新接入的 Rust，不顺带改其他手册的搜索行为。

| 消费者 | WP-R2 的接入与验收责任 |
|---|---|
| 中文本地搜索 | 先按 current 页集合过滤 next 整页，再把正文投影为 current 后交给索引器；不能只在点击结果时拦截，标题、摘要及匹配文本都不得含 next 专有内容 |
| 英文 Inkeep | 确认 Rust 索引读取 current 输出，核对抓取范围、更新／删除及缓存；用实际检索验证 next-only 页标题和段落不可见，不能从 NextChannel 渲染测试推断搜索通过 |
| 导航、页面与译文 | 页面、侧边栏、DocCard、TOC 及直接地址遵守各自 current/next 通道；翻译保留通道语义 |
| 静态 Markdown、llms、sitemap | 对外输出 current 页面集合与内容，验证 next 整页、块及锚点不进入这些 current 产物 |

现有[通道运行手册](https://github.com/zilliztech/zdoc/blob/34498a57295e3ab99327e9b00ddd767cab956f6a/runbook/release-channel-gating.md#L41)记录了中文搜索仍收录 NEXT 标题的限制，WP-R2 必须补上 Rust 的索引输入适配；搜索验证未通过则 Rust 首次上线验收不通过。通道约束针对读者可见的页面及上述产物，不承诺共用浏览器构建文件里没有 next 字节，也不为此新增双构建。

### workflow 中的判断

`_fetch-content-group.yml` 中有几处写死了 REST 例外，例如：

```bash
if [[ "$GROUP" != rest && -z "$SNAPSHOTS" ]]; then
  echo "Publication group $GROUP must resolve at least one source snapshot" >&2
  exit 1
fi
```

除 REST 外，每个分组都必须有飞书快照，否则失败。改为按“这个分组的手册都没有飞书来源”判断，由 `scripts/docs-workflow/content-groups.js` 给出，不在 workflow 中写分组名。WP-R2 同时检查 revision、翻译归属、checkpoint 与恢复中的相关分支，不能只修改这一处 SNAPSHOTS 判断。

## 上线

- **第一次 Fetch 写入 dev。** `registry.ts` 的登记合并后，第一次 Fetch 写入 dev；不另设激活开关。UAT 与 Prod 共用产物，运行时分别选择 next/current。进入 dev 不等于提升，也不能代替 Prod 的通道检查。
- **dev 上的初始内容。** 按 `manuals/README.md` 的“First-publish bootstrap”，新手册第一次正式 Fetch 前，dev 上要已经有手册的内容、`generated/en/sidebars/rust.sidebar.js` 与重新生成的 `deploy/contracts/localization-inputs.inventory.json`。`content/`、`generated/` 归 dev，不能经 master 提交，同步也不会搬，由文档负责人手工放一次；页面和侧边栏取生成结果；inventory 用专用生成命令重建。
- **工具链同步。** 最终通过经过验证的 master→dev 同步 PR 带入登记、站点配置等工具代码；保留现有 PR 同步路径。
- **首次 Fetch 与同步的顺序待验证。** 2026-11-02 核对的[根 README](https://github.com/zilliztech/zdoc/blob/master/README.md#before-publishing)要求发布前先同步工具链；[新手册运行手册](https://github.com/zilliztech/zdoc/blob/master/packages/docs-tooling/src/manuals/README.md#ordering-fetch-before-sync)要求新手册 Fetch 在同步之前，以补齐同步校验需要的生成状态。两处指引不一致，WP-R2 必须用新手册的隔离回放验证，并由文档负责人确认执行顺序后才能上线，不能直接照抄旧的七步表。
- **Fetch 的输入分工。** [现行工作流](https://github.com/zilliztech/zdoc/blob/master/.github/workflows/fetch-docs.yml)默认 `tooling_ref=master`、`source_ref=dev`，解析成固定 SHA：从前者取工具与配置，以后者为内容基线。这解释了读取位置，但不能代替上述发布顺序验证。
- **WP-R2 接入清单。** 按新手册运行手册补齐 registry、派生站点配置、reconciliation/lark 配置、着陆页保留策略、侧边栏恢复及其测试、路径过滤、翻译分组与归属映射、workflow 分组。初始内容的 inventory 在暂存侧边栏后通过 `generate:localization-input-inventory` 重新生成，不手写；记录两种语言所需的初始文件及验证结果。

## 上游更新与提升

上游更新只改 `next`，Prod 保留 `current`；整本手册共用同一对 commit，不做每页锁定或提升。Cloud 配置与文件只有一份：默认两边生效，延后发布的改动用 Transform 的 `channel`、整页通道或手写 `NextChannel` 表达。变量表改动同样立即影响两边，需要分通道的值先用页面级规则表达，不新增变量版本表。

上游更新（技术设计 [06](./06-upstream-changes.md)）对整本手册开一个滚动更新的 PR，不按页面拆。PR 中列出：

- 改动的页面与生成结果的差异；
- 新增、删除、改名的页面，以及因此改变的地址；
- 产品名警告；
- 被 `replace` 覆盖的上游内容变化，即使 Cloud 输出未变也提示复核；保留原文对比，代码行目标附所在代码组上下文（沿用技术设计 06）；
- 新出现的模块（默认发布，由审核的人决定是否排除）。

**提升 PR 的范围。** 按整本手册验收，固定被验收的 `next` 与配置／Cloud 文件摘要；PR 基线或相关输入变化后重新生成校验并重新确认验收，自动校验通过不能替代人工对新内容的确认。PR 将 `current` 设为该 `next`，删除临时 `channel: current` Transform、解除 `channel: next` 限定；`cloud_pages` 中 next 页转为 current，retire-in-next 页移除配置并处理引用。该手册的待提升规则和页面须一起准备就绪。

提升候选还须列出从两版并集中消失的页面／模块及全部配置引用，包括 `metadata`、`exclude`、`transforms`、导航和正文链接。按已批准的删除意图清理，无法确定意图时由作者处理；残留无效路径仍阻止提升，不静默忽略，也不自动猜测改名。移除本地退役页时同样执行此检查，不自动删除可能仍被其他页面引用的物理文件。

手写 `NextChannel` 单独列入 PR 供审核，不批量清除：与本次同时上线的 include 内容解除包裹、exclude 旧内容删除；较晚上线的段落可保留。仅改本地规则或页面时，即使 `current == next` 也必须能提升，不能仅用 commit 是否不同判断候选。提升后重新生成两通道并校验整本手册；生成失败不发布任何部分结果。

**复用与实现边界。** [Guides 通道设计](./04-channels-and-lock.md)提供行为约定，[WP11 PR #921](https://github.com/zilliztech/zdoc/pull/921)已合入两版生成。2026-11-02 核对的 zdoc master [`34498a57`](https://github.com/zilliztech/zdoc/tree/34498a57295e3ab99327e9b00ddd767cab956f6a)有 Transform 通道筛选、合并与 NextChannel 渲染，但 23 篇共享页的锁定版本仍相同，未见完整的更新／提升工作流。SDK 需补齐本地整页、手册级更新与提升；不能把 Guides 的基础能力当作 SDK 发布闭环已验收。

## 出错时

| 情况 | 错误码 | 影响 |
|---|---|---|
| `manual.yaml` 格式不对、有不认识的字段、`publish.manual` 未登记 | 现有的 `CONFIG_*` | 整本手册生成失败 |
| `exclude`、`metadata`、`transforms` 的路径不属于允许的页面集合 | `CONFIG_PATH_UNKNOWN` | 整本手册生成失败 |
| 两个文件生成同一个地址（如只差大小写） | 新增 `CONFIG_SLUG_DUPLICATE` | 整本手册生成失败 |
| 连接值残留 | `PRODUCT_NAME_FOUND` | 整本手册生成失败 |
| 指代服务端的说法 | `PRODUCT_NAME_FOUND`，严重程度为 `warning` | 只提示 |
| 链接指向被排除的页面 | 新增 `LINK_TARGET_EXCLUDED`（提示） | 只提示 |
| 链接指向手册之外的 `.md` | `LINK_UNKNOWN_FORM` | 整本手册生成失败 |
| 目标缺失、多义匹配、变换重叠、内容与目标类型不符 | WP10 的 `TRANSFORM_*`、`LINE_*` | 整本手册生成失败 |
| 本地文件缺失／越界、使用不支持的内容语法、连接映射无效 | 复用适用的配置／变换错误，WP-R1 明确映射；不另建宽松兜底 | 整本手册生成失败 |
| 操作与 `position / content` 不相容、非法通道或规则没有对应通道的页面 | 复用 Guides 配置／变换错误 | 整本手册生成失败，指出通道 |
| 本地逻辑路径冲突，或本地页又配置 Transform | 配置校验错误；地址碰撞用 `CONFIG_SLUG_DUPLICATE` | 整本手册生成失败 |
| 手写通道标记落入生成的差异包裹 | `MERGE_NESTED_CHANNEL` | 整本手册生成失败，指向本地文件 |
| MDX 编译失败 | `ADAPT_MDX_INVALID` | 整本手册生成失败 |

整本手册只有一个 lock，所以任何错误都让整本手册的这次更新失败：PR 校验不通过；Fetch 中保留 dev 上现有的版本，其他分组照常发布。

## 接入前待验证

| 事项 | 我们的方案 |
|---|---|
| 新增来源类型 `shared`、手册级的 lock | 按本文方案实现，并验证现有 Fetch 合约兼容 |
| workflow 中 REST 的例外 | 改为按“没有飞书来源”判断 |
| 地址与标题 | `/reference/rust/rust/<模块>-<文件名>`，不加 `v2-`；后缀 `\| Rust` |
| 不发布的模块与页面 | 先照 Go 排除 ResourceGroup（Rust 的副本管理 `describe_replicas`、`transfer_replica` 也在这个模块中）；CDC、Snapshots 逐页核对 |
| Snapshots 的 `beta` | `ON REQUEST`，与其他 SDK 一致 |
| `type`、`token` | 共享的 Guides 页面用 `type: origin`、`token: shared-<页面>`。Rust 建议 `type: origin`、`token: shared-rust-<模块>-<文件名>`，需要确认翻译与其他工具对 `token` 的用法 |
| 记录文件与恢复 | 独立手册 schema，路径 `generated/en/manifests/shared-manuals/rust.json`；验证多页、多通道的认证，以及 checkpoint 和恢复均携带该记录 |
| 着陆页 | Cloud 编写，master 维护 |
| 上线 | 登记合并后的第一次 Fetch 写入 dev；按通道验收并按整本提升 |
| dev 上的初始内容与同步顺序 | 我们准备文件；WP-R2 验证首次 Fetch 与同步的顺序，文档负责人确认，并确定是否需要中文侧边栏 |
| 上游命名块 | 三种变换共用命名块；上游 skill 保留与校验标记，接入时验证不会被重生成覆盖 |
| Cloud 内容完整性 | 首版专有方法、属性和对象需对照源码与能力清单核实；源码比对或 agent 生成更新 PR 的自动化后续再接，不进入本期 Fetch |
| 两通道完整旅程 | 验证真实 `current != next`、相同 commit 的本地差异、独有页与整本提升，并核对翻译及搜索等派生产物 |
| 生命周期 UI 与搜索 | WP-R2 接入 Rust 专用生命周期展示及 current 搜索输入；英文索引抓取、缓存和实际检索需外部验证 |

## 工作包

| 工作包 | 内容 | 审阅 |
|---|---|---|
| **WP-R1**（只改 shared-docs） | 手册展开与来源编排、三种变换（WP10）、双版本合并（WP11）、本地整页通道、手册记录模型与纯校验、生命周期元数据、连接值、检查、排除、导航输入与链接、手册级 lock/build 与 PR 校验 | 发 FYI；提供测试登记下整本手册两通道的隔离生成结果及记录契约 |
| **WP-R2**（站点、Fetch 与上线） | 登记与分组、无飞书来源接线、记录认证及 checkpoint／恢复、实际英文侧边栏生成与中文派生、Rust 生命周期 UI、current 搜索和其他派生产物、着陆页、正式 PR 校验与首次上线顺序 | 文档负责人评审；只生成不发布的 Fetch、隔离恢复回放及中英文展示／搜索证据，分别验收 |
| 上游更新的手册级 PR | WP12：只更新 `next`，与 Guides 的逐页 PR 共用发现与 PR 逻辑 | 随 WP12 |
| 整本手册提升 | WP13：锁定版本、通道规则和独有页在同一 PR 处理，清理消失页配置引用，列出手写标记；包括本地-only 提升及验收输入变化后的重新确认 | 随 WP13；上线前提供双通道完整旅程证据 |

WP-R1 做完，用真实的生成结果与文档负责人讨论 WP-R2。

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么整本手册一份配置。** Rust 有 164 页，web-content 一次提交常常改几十页（10-27、10-29 两次格式整理都改了全部页面）。每页一份配置意味着 328 个文件、每次几十个上游更新 PR；页面之间互相链接很多，整本手册也应该来自同一个 commit。展开成虚拟页面后复用变换与合并核心；来源、SDK 适配、链接和发布记录按手册接入。

**为什么保留变量表。** 连接示例值用同名键对应，沿用 Guides 的变量命名；参数和用法差异交给页面级 `transforms`。不为简单连接值新增通用变换、匹配范围和规则优先级。

**为什么同时支持 add 和本地整页。** Cloud 有上游未包含的方法、属性和对象。页内补充复用 Guides 的 add；完整页面直接读 zdoc 文件，不为它虚构命名块。两种内容都经 Git 审核，并参与同一本手册的导航、校验和发布。

**为什么措辞只警告。** 整本手册只有一个 lock，一处措辞就会卡住全部页面的更新；措辞不影响使用，连接值会让用户连不上，所以只有连接值失败。

**为什么不在 web-content 中用变量。** milvus.io 直接渲染 `API_Reference/`，不经过 md2md；写成变量，Milvus 网站上会显示 `{{var.…}}`，除非改 milvus.io 的构建。

**为什么不新增激活开关。** Rust 是新手册，登记后即可进入 Fetch；UAT 与 Prod 的内容差异由已有通道机制表达，整本手册的提升负责把已验收内容交给 Prod。

**为什么保留 current / next，仍只维护一份 Cloud 文件。** 上游更新和 Cloud 上线并不同时发生；两版原文让 Prod 保留旧内容，Cloud 配置和文件通过通道表达差异。复用 Guides 生成机制，避免维护两套本地目录。接口生命周期记录历史事实，通道管理当前可见性，两者不能互相替代。

</details>

## 验收

- `shared-docs build` 对 `shared-docs/rust/` 生成两个锁定版本中全部未排除的页面及声明的 Cloud 页面，退出码 0；输出中没有禁止连接值与被排除内容。Cloud 专有内容按经核实的清单验收，不能以语法检查替代完整性核验。
- 每页的 front matter 符合上表；侧边栏中模块与页面按字母顺序排列。
- 指向被排除页面的链接变成文字，并给出提示；手册内其他链接都能打开。
- 第一次 Fetch 后，dev 上有 Rust 的全部页面、侧边栏与记录文件，UAT 上可以浏览；Guides 与其他 SDK 的输出不变。
- 块／语言／代码行三级 `add / remove / replace` 都有生成用例；说明与代码一致；本地完整页和片段的链接、图片、产品名与 MDX 均校验，冲突逻辑路径被拒绝。
- 缺失变量值、重复或包含的映射、目标不存在／匹配不唯一、规则重叠、文件越界、非法占位符、操作与 position/content 不相容、非法通道均被拒绝。
- 原文目标按映射前内容匹配；Cloud 替换内容不被二次映射，但其中的禁止连接值仍使生成失败。仅改 Cloud 文件也会触发重新生成并改变输入摘要。
- 上游更新 PR 一次列出整本手册的变化；被替换原文改变但输出未变时仍提示复核，目标失效时校验失败。报告集成由 WP12 验收，WP-R1 提供来源与依赖信息。
- 生命周期有明确来源时保留；未知不猜，不把服务端要求混为 SDK 引入版本。WP-R2 验证“只有废弃版本”“废弃晚于引入”和“两者均未知”：最低版本只取引入值，废弃提示单列；其他 SDK 显示不变。
- 验证 `current != next` 和相同 commit 的通道规则差异；上游新增／删除页、Cloud next／retire-in-next 页及跨来源、跨通道链接均覆盖。已有页的 UAT front matter 保持 current，next 独有页用自己的元数据；整页 next／retire-in-next 内再写块级通道标记被拒绝。
- WP-R2 分别验证导航与直接地址的两通道行为，以及中英文 Rust 搜索、静态 Markdown、llms、sitemap 的 current 视图。用 next-only 页标题和段落检查搜索标题、摘要与匹配文本，提升后重建／更新索引再验证可检索；UAT 搜索也只覆盖 current，译文维持通道语义。
- 手册记录覆盖同手册多页与混合通道；缺失或多余输出、错误 token/channel、摘要不符、记录丢失都拒绝采用。WP-R2 用隔离远端回放 checkpoint 与旧基线恢复，核对页面、侧边栏及记录的完整集合和字节摘要，不用真实 origin 或付费翻译填补证据。
- 整本提升覆盖上游版本、仅本地变化、临时规则、独有页和消失页的配置清理；模拟验收 A 后 next 推进到 B，旧验收不得采用 B。失败时整本保留旧发布结果，手写标记逐项审核。WP13 提供完整旅程证据。
