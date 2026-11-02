# 10 SDK Reference：从 web-content 生成（Rust 试点）

本篇定义怎样把 web-content 中的 SDK Reference 生成到 zdoc，先以 Rust 试点。要交付什么行为、文档工程师怎样写，见 [SDK Reference 产品需求](../prd-sdk-reference.md)；调研与选项见 [Rust SDK Reference 接入调研](../../research/rust-sdk-reference.md)。本篇只写工程上选定的做法。

**参与方**：zdoc 生成（shared-docs）、zdoc 发布（Fetch）。

**状态**：草稿，2026-11-02 与 SDK Reference 产品需求同步：页面内支持 `remove / replace`，不支持 `add`。字段与验收是拟实现的约定；外部集成事项见文末“待确认”，不因本次改稿视为已确认。

## 目标与范围

- **试点：** Rust SDK Reference。Cloud 上还没有 Rust 手册，不涉及从飞书迁移、切换与归属。以后其他 SDK 照同一条路迁过来，REST 最后。
- **原文：** web-content 的 `API_Reference/milvus-sdk-rust/v3.0.x/`。它在 web-content 中手写维护（web-content 的 `AGENTS.md`：“hand-curated”），不是 md2md 的输出，没有变量。
- **不改上游的发布：** 不改 milvus.io 的构建与 Milvus 的发布流程。web-content 在 Cloud 要删除或替换内容的地方加命名块（HTML 注释，milvus.io 不显示）。
- **只做 v3.0.x、只做英文。** 中文由现有的机器翻译从 dev 生成，不做人工校对。
- **与 Guides 的区别：** Guides 以页面为单位接入、变换与激活；SDK Reference 以整本手册为单位配置和更新，页面内只开放删除与替换，不开放增加内容。

## 约定

### 组目录

Rust 是 shared-docs 的一个组（技术设计 [02](./02-page-config.md#shared-docs-的位置)），与 Guides 的组目录结构不同：没有 `pages/`，一本手册一份配置、一个 lock。

```
shared-docs/rust/
  source.yaml          # 上游仓库与跟踪分支：web-content，master
  manual.yaml          # 手册配置
  lock.yaml            # 整本手册采用的 web-content commit，由工具写入
  Variables.json       # Cloud 变量：连接值
  product-names.yaml   # 产品名检查规则
  content/             # Cloud 替换文件，按需创建
```

“manual”（手册）沿用 zdoc `packages/docs-tooling/src/manuals/registry.ts` 的叫法：网站上每一本可以独立导航的文档是一个 manual。

### 配置契约

四份作者配置的基本写法见 [PRD 场景 R1](../prd-sdk-reference.md#场景-r1接入一本手册)，差异与变换示例见 [R2](../prd-sdk-reference.md#场景-r2写-cloud-的差异)。这里只补充实现约束。

| 输入 | 约定 |
|---|---|
| `source.yaml` | 沿用 Guides 的 `schema_version / repository / track`；lock 与上游更新工具从这里发现 commit |
| `manual.yaml` | 必填 `schema_version: 1`、`source.dir`、`publish.manual`；`source.previous`、`exclude`、`milvus_values`、`metadata`、`transforms` 可省略 |
| 路径 | `source.dir / previous` 相对于上游仓库；排除、元数据和变换的页面路径相对于 `source.dir`。一级子目录为模块 |
| `metadata` | 模块仅可设 `beta`；页面可设 `beta / deprecate_since / added_since / description`。页面优先于模块，再取默认值 |
| `transforms` | 页面路径 → 变换列表；仅接受 `remove / replace`，复用 Guides 的 `target / content`。拒绝 `add`、`position`、`channel`；不引入通用变换或新字段 `replacement` |
| `Variables.json` | 沿用组级变量表；每个 `milvus_values` 键必须有同名字符串值，缺失或类型不符时配置校验失败 |
| `content.file` | 相对于 `manual.yaml` 所在目录，须位于该组 `content/` 内；解析真实路径后仍须在该目录内，拒绝绝对路径、越界及符号链接逃逸 |

`publish.manual` 必须在当前生成环境的 registry 中已登记。WP-R1 用测试登记做隔离生成验证，不修改生产 registry，也不跳过登记校验；WP-R2 提供真实登记后，才能完成正式配置 PR 的端到端生成校验。排除、元数据和变换指向的模块或页面必须存在；对已排除页面配置变换时报错，避免规则被静默忽略。没有列入排除项的新增页面默认发布，上游更新 PR 必须列出。

### `lock.yaml`

格式与 Guides 的页面 lock 相同（技术设计 [04](./04-channels-and-lock.md#每页一份-lockyaml)），只是整本手册一份。接入时由工具取跟踪分支的最新提交写入，`current` 与 `next` 相同。Phase 1 中两者始终一起移动，见下文“上游更新”。

### 生成

工具读取 `manual.yaml` 时，把 `source.dir` 下每个未排除的 `.md` 文件展开成内存中的一份页面配置，所有页面共用同一个 lock；`transforms` 中这一页的变换放进这份页面配置。之后的读取、站点适配、链接、产品名检查与 MDX 编译沿用 Guides 的实现（技术设计 [02](./02-page-config.md)、[02b](./02b-links-and-images.md)、[07](./07-site-adaptation.md)）。不调用 md2md：原文没有变量与片段，Cloud 替换内容也不支持变量／片段占位符。

一页的处理顺序：

1. 按 lock 中的 commit 读原文；
2. 在带命名块的原文上校验并定位全部 `remove / replace`，按原文内容匹配代码行，检查目标冲突和替换文件；
3. 执行变换，并仅在保留的上游代码片段中映射连接值。Cloud 替换文件和 `content.lines` 不经过映射；保留来源信息，之后清除命名块标记。不得先改连接值再匹配原文代码行；
4. 站点适配，生成 front matter；
5. 链接换算；
6. 产品名检查；
7. MDX 编译。

### 地址、路径与 front matter

沿用现有 SDK 的规则，不加 `v2-` 这一层（Go、Java 的 `v2-`、Python 的 `MilvusClient` 是多代 API 留下的，Rust 只有一套）。以 `Authentication/create_user.md` 为例：

| 项目 | 规则 | 例子 |
|---|---|---|
| 输出路径 | `content/en/reference/api/rust/rust/<模块>/<模块>-<文件名>.md` | `…/rust/rust/Authentication/Authentication-create_user.md` |
| `slug` | `/rust/rust/<模块>-<文件名>` | `/rust/rust/Authentication-create_user`，网址 `/reference/rust/rust/Authentication-create_user` |
| `title` | H1，加后缀 `\| Rust` | `create_user() \| Rust` |
| `sidebar_label` | H1 | `create_user()` |
| `description` | H1 下的第一段，加后缀 `\| Rust`；`metadata` 可以改写 | `Creates a user account with a username and password. \| Rust` |
| `added_since` | 页面在 `source.previous` 中也有：`v2.6.x`；否则 `v3.0.x`；`metadata` 可以改写 | `v2.6.x` |
| `last_modified` | `FALSE` | — |
| `deprecate_since` | `false`；`metadata` 可以改写 | — |
| `beta` | `false`；`metadata` 可以改写 | Snapshots 模块为 `ON REQUEST` |
| `keywords` | 复用 Fetch 的 `keyword_picker`，加上版本标记 `rustv30` | — |
| `displayed_sidebar` | 从 `registry.ts` 取 | `rustSidebar` |
| `sidebar_position` | 模块按目录名、模块内按文件名的字母顺序，不区分大小写 | — |
| `type`、`token` | 见“待确认” | — |

- **`last_modified` 为什么写 `FALSE`。** 网站的 `docs-ui` `DocMetaTags.tsx` 取 `added_since`、`last_modified`、`deprecate_since` 中最大的版本，显示为 “Minimum SDK version”。全部写 `v3.0.x` 会让 v2.6 就有的方法也显示 v3.0.x。
- **地址上线后不能改。** 原文文件名改了，地址随之改变。web-content 改名时，上游更新 PR 中列出改变的地址，由人确认。
- **侧边栏。** 输出 `generated/en/sidebars/rust.sidebar.js`，格式与其他 SDK 相同：最前面是着陆页，之后每个模块一个分类。由哪段现有代码生成（Fetch 的侧边栏生成，或 `reference/sidebarDerivation.ts`）在 WP-R2 的计划中确定；`sidebarDerivation.ts` 会按 front matter 的 `type: folder` 认分类的着陆页，`type` 的取值要与之相容。

### 链接

原文中的链接都是相对的 `.md` 链接，例如 `Ids.md`、`../Collections/ConsistencyLevel.md`。

| 链接指向 | 处理 |
|---|---|
| 手册内发布的页面 | 换成这一页的地址，锚点照 zdoc 的规则换算 |
| 手册内被排除的页面 | 去掉链接，保留文字，给出提示 `LINK_TARGET_EXCLUDED`，不失败 |
| 手册之外的 `.md` | 生成失败（`LINK_UNKNOWN_FORM`）：Rust 的原文中没有这种链接，出现时由人判断 |
| 外部地址 | 不变 |

被排除的页面只给提示，是因为整本手册只有一个 lock：一处链接失败，会卡住全部页面的更新。

### 着陆页

不用原文的 `About.md`。照其他 SDK，由 Cloud 编写 `content/en/reference/api/rust/rust/rust.md`，放在 master，登记在 `deploy/contracts/master-tooling-sync.json` 的 `masterAuthoritativePaths` 与 `registry.ts` 的 `landingPage`。Go 的 `go.md` 就是这样，其中的 “Connect to Zilliz Cloud” 一节是 Cloud 独有的。

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

### 页面内的删除与替换

支持块、语言、代码行三级 `remove / replace`，复用 WP10 的定位、冲突检查和缩进处理；不支持 `add`。参数替换必须同时核对参数说明与调用示例，生成成功不代表 SDK／服务端支持该参数。

Rust 已知删除目标是 `Collections/load_collection.md` 的副本／资源组参数和示例、`Partitions/load_partitions.md` 的同类参数，以及 `Client/MilvusClientV2.md` 的 ResourceGroup 介绍。替换案例见 PRD R2，是配置示意，不新增未经核实的 Rust 方法需求。历史调研与参数差异证据保留在 research 中。

- **上游标记：** 对删除和替换目标都需要命名块，由 web-content 维护者配合添加；标记不改变 Milvus 的发布流程。
- **执行校验：** 先对原文定位全部目标，再执行变换。缺失或多义匹配、重叠规则、无效内容使整本手册失败。`target.lines / content.lines` 沿用 Guides：最多定位连续 5 行、忽略行首缩进及行尾空格、其余精确匹配，禁止空行、围栏和命名块，写回时恢复缩进。
- **内容形式：** 整块或整种语言替换用 `content.file`；代码行替换用 `content.lines`，两者不可同时提供。`remove` 不可提供内容，`replace` 必须提供与目标类型相符的内容。
- **Cloud 文件：** 放在组内 `content/`，使用 Markdown 和代码围栏；替换一种语言时文件中只写该语言的一个代码块。直接写 Cloud 值，拒绝变量／片段占位符、命名块、手写 Tabs 和产品过滤指令；Rust 本期只有一个发布目标，不新增内容预处理能力。本期不支持组内本地图片，外部图片沿用共享图片处理与校验。
- **链接：** Cloud 文件中的相对 `.md` 链接按被替换的上游页面目录解析，使用本手册的链接映射；不是相对于 `content/`。复用文件时，每个消费页面分别检查。其他链接和锚点按现有适配规则校验。
- **依赖与来源：** 记录实际使用的 Cloud 文件及摘要，使文件变化触发重新生成并进入记录文件的输入身份；诊断指向 Cloud 文件或 `manual.yaml` 中的代码行。被覆盖原文的变化单独进入上游更新报告，不只比较生成输出。

## 接入 Fetch

### 来源类型与分组

- **登记：** `registry.ts` 中新增手册 `rust`，`kind: 'reference'`。英文的来源是新增的来源类型 `shared`，例如 `shared('shared-docs/rust')`；中文的来源与其他 SDK 相同，是 `local('content/zh-CN/reference/api/rust/rust')`。`manuals/schema.ts` 的 `sourceType` 增加 `shared`。
- **分组：** `workflows/groups.ts` 新增 `rust` 分组，进入 `fetch-docs.yml` 现有的 `produce_sdk_reference` 矩阵，不新建任务。
- **fetch 一步：** `publish-group --stage fetch` 遇到 `shared` 来源时，按 `lock.yaml` 的 commit 稀疏取 web-content 的 `source.dir`，调用 shared-docs 生成，写到输出路径。validate、publish 两步与其他 SDK 共用。
- **记录文件：** 每次生成写一份手册的记录文件，格式同技术设计 [05](./05-publish-handoff.md#记录文件)，`outputs` 列出全部页面。路径见“待确认”。
- **不写 `active.json`：** Rust 没有飞书记录，没有切换与归属。

### workflow 中的判断

`_fetch-content-group.yml` 中有几处写死了 REST 例外，例如：

```bash
if [[ "$GROUP" != rest && -z "$SNAPSHOTS" ]]; then
  echo "Publication group $GROUP must resolve at least one source snapshot" >&2
  exit 1
fi
```

除 REST 外，每个分组都必须有飞书快照，否则失败。改为按“这个分组的手册都没有飞书来源”判断，由 `scripts/docs-workflow/content-groups.js` 给出，不在 workflow 中写分组名。

## 上线

- **第一次 Fetch 就发布。** `registry.ts` 的登记合并后，第一次 Fetch 写入 dev。UAT 与 Prod 构建同一个 dev SHA，Prod 只在发版时更新，所以发版前在 UAT 上检查。不做开关，不做整本手册的通道。
- **dev 上的初始内容。** 按 `manuals/README.md` 的“First-publish bootstrap”，新手册第一次正式 Fetch 前，dev 上要已经有手册的内容、`generated/en/sidebars/rust.sidebar.js` 与重新生成的 `deploy/contracts/localization-inputs.inventory.json`。`content/`、`generated/` 归 dev，不能经 master 提交，同步也不会搬，由文档负责人手工放一次；页面和侧边栏取生成结果；inventory 用专用生成命令重建。
- **工具链同步。** 最终通过经过验证的 master→dev 同步 PR 带入登记、站点配置等工具代码；保留现有 PR 同步路径。
- **首次 Fetch 与同步的顺序待验证。** 2026-11-02 核对的[根 README](https://github.com/zilliztech/zdoc/blob/master/README.md#before-publishing)要求发布前先同步工具链；[新手册运行手册](https://github.com/zilliztech/zdoc/blob/master/packages/docs-tooling/src/manuals/README.md#ordering-fetch-before-sync)要求新手册 Fetch 在同步之前，以补齐同步校验需要的生成状态。两处指引不一致，WP-R2 必须用新手册的隔离回放验证，并由文档负责人确认执行顺序后才能上线，不能直接照抄旧的七步表。
- **Fetch 的输入分工。** [现行工作流](https://github.com/zilliztech/zdoc/blob/master/.github/workflows/fetch-docs.yml)默认 `tooling_ref=master`、`source_ref=dev`，解析成固定 SHA：从前者取工具与配置，以后者为内容基线。这解释了读取位置，但不能代替上述发布顺序验证。
- **WP-R2 接入清单。** 按新手册运行手册补齐 registry、派生站点配置、reconciliation/lark 配置、着陆页保留策略、侧边栏恢复及其测试、路径过滤、翻译分组与归属映射、workflow 分组。初始内容的 inventory 在暂存侧边栏后通过 `generate:localization-input-inventory` 重新生成，不手写；记录两种语言所需的初始文件及验证结果。

## 上游更新

Phase 1 中 Rust 的 `current` 与 `next` 始终相同：上游更新 PR 同时改两者，合并后下一次 Fetch 写入 dev，发版时上 Prod。本期选择不提供同一页的两版内容，因此 Rust 不使用两版合并（WP11）。SDK 已发布不代表 Cloud 服务端已开放全部能力；用排除、删除、替换和元数据表达产品差异，整体尚不可用时暂不合并更新。

上游更新（技术设计 [06](./06-upstream-changes.md)）对整本手册开一个滚动更新的 PR，不按页面拆。PR 中列出：

- 改动的页面与生成结果的差异；
- 新增、删除、改名的页面，以及因此改变的地址；
- 产品名警告；
- 被 `replace` 覆盖的上游内容变化，即使 Cloud 输出未变也提示复核；保留原文对比，代码行目标附所在代码组上下文（沿用技术设计 06）；
- 新出现的模块（默认发布，由审核的人决定是否排除）。

## 出错时

| 情况 | 错误码 | 影响 |
|---|---|---|
| `manual.yaml` 格式不对、有不认识的字段、`publish.manual` 未登记 | 现有的 `CONFIG_*` | 整本手册生成失败 |
| `exclude`、`metadata` 中的模块或页面在原文中不存在 | `CONFIG_PATH_UNKNOWN` | 整本手册生成失败 |
| 两个文件生成同一个地址（如只差大小写） | 新增 `CONFIG_SLUG_DUPLICATE` | 整本手册生成失败 |
| 连接值残留 | `PRODUCT_NAME_FOUND` | 整本手册生成失败 |
| 指代服务端的说法 | `PRODUCT_NAME_FOUND`，严重程度为 `warning` | 只提示 |
| 链接指向被排除的页面 | 新增 `LINK_TARGET_EXCLUDED`（提示） | 只提示 |
| 链接指向手册之外的 `.md` | `LINK_UNKNOWN_FORM` | 整本手册生成失败 |
| 目标缺失、多义匹配、变换重叠、内容与目标类型不符 | WP10 的 `TRANSFORM_*`、`LINE_*` | 整本手册生成失败 |
| 替换文件缺失／越界、使用不支持的内容语法、连接映射无效 | 复用适用的配置／变换错误，WP-R1 明确映射；不另建宽松兜底 | 整本手册生成失败 |
| 写了 `add`、`position` 或 `channel` | `CONFIG_FIELD_UNKNOWN` | 整本手册生成失败 |
| MDX 编译失败 | `ADAPT_MDX_INVALID` | 整本手册生成失败 |

整本手册只有一个 lock，所以任何错误都让整本手册的这次更新失败：PR 校验不通过；Fetch 中保留 dev 上现有的版本，其他分组照常发布。

## 待确认

| 事项 | 我们的方案 |
|---|---|
| 新增来源类型 `shared`、手册级的 lock，是否算改框架 | 如上文 |
| workflow 中 REST 的例外 | 改为按“没有飞书来源”判断 |
| 地址与标题 | `/reference/rust/rust/<模块>-<文件名>`，不加 `v2-`；后缀 `\| Rust` |
| 不发布的模块与页面 | 先照 Go 排除 ResourceGroup（Rust 的副本管理 `describe_replicas`、`transfer_replica` 也在这个模块中）；CDC、Snapshots 逐页核对 |
| Snapshots 的 `beta` | `ON REQUEST`，与其他 SDK 一致 |
| `type`、`token` | 共享的 Guides 页面用 `type: origin`、`token: shared-<页面>`。Rust 建议 `type: origin`、`token: shared-rust-<模块>-<文件名>`，需要确认翻译与其他工具对 `token` 的用法 |
| 记录文件的路径 | 建议 `generated/en/manifests/shared-pages/rust/rust.json` |
| 着陆页 | Cloud 编写，master 维护 |
| 上线 | 登记合并后的第一次 Fetch 即写入 dev |
| dev 上的初始内容与同步顺序 | 我们准备文件；WP-R2 验证首次 Fetch 与同步的顺序，文档负责人确认，并确定是否需要中文侧边栏 |
| 上游命名块 | 本地设计采用 `remove / replace`；具体上游目标与标记仍需 web-content 维护者配合确认 |
| Phase 1 不区分 `current` 与 `next` | 上游更新同时改两者 |

## 工作包

| 工作包 | 内容 | 审阅 |
|---|---|---|
| **WP-R1**（只改 shared-docs） | 组目录与 `manual.yaml`、展开成虚拟页面、页面内的 `remove / replace` 与 Cloud 内容文件（复用 WP10）、内容依赖与来源记录、front matter、连接值、产品名检查的严重程度、排除、模块顺序、链接、`shared-docs lock` 与 `build` 支持手册组、PR 校验 | 发 FYI；随 PR 提供测试登记下全部未排除页面的隔离生成结果 |
| **WP-R2**（Fetch 与上线） | `shared` 来源类型、`rust` 分组、workflow 中的判断、记录文件、`registry.ts` 登记与上线接入清单中 master 维护的部分、着陆页、正式配置 PR 生成校验、首次上线顺序验证 | 文档负责人评审；合并前跑一次只生成不发布的 Fetch |
| 上游更新的手册级 PR | 在 WP12 中实现，与 Guides 的逐页 PR 共用发现与 PR 的逻辑 | 随 WP12 |

WP-R1 做完，用真实的生成结果与文档负责人讨论 WP-R2。

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么整本手册一份配置。** Rust 有 164 页，web-content 一次提交常常改几十页（10-27、10-29 两次格式整理都改了全部页面）。每页一份配置意味着 328 个文件、每次几十个上游更新 PR；页面之间互相链接很多，整本手册也应该来自同一个 commit。展开成虚拟页面后，生成步骤照原样复用，只需扩展 lock、校验与上游更新。

**为什么保留变量表。** 连接示例值用同名键对应，沿用 Guides 的变量命名；参数和用法差异交给页面级 `transforms`。不为简单连接值新增通用变换、匹配范围和规则优先级。

**为什么支持 replace，暂不支持 add。** Cloud 可能使用不同参数或调用方式，删除不能完整表达。复用 Guides 的替换格式并维护必要的 Cloud 内容；上游对应内容变化时提示复核。本期不新增独立内容，`add` 仍拒绝。

**为什么措辞只警告。** 整本手册只有一个 lock，一处措辞就会卡住全部页面的更新；措辞不影响使用，连接值会让用户连不上，所以只有连接值失败。

**为什么不在 web-content 中用变量。** milvus.io 直接渲染 `API_Reference/`，不经过 md2md；写成变量，Milvus 网站上会显示 `{{var.…}}`，除非改 milvus.io 的构建。

**为什么第一次 Fetch 就发布。** Rust 是新手册，没有旧页面需要切换或保护；发版本身就是一道关，发版前可以在 UAT 上检查。开关与整本手册的通道都要新写代码，换来的只是“晚一点发布”，控制登记的合并时间就能做到。

**为什么 Phase 1 不区分 `current` 与 `next`。** 本期用配置处理 Cloud 支持差异，采用整本手册一起更新；发布前仍在 UAT 检查。若需要让同一页面的新内容跨多次发版只在 UAT 可见，再评估两版方案。

</details>

## 验收

- `shared-docs build` 对 `shared-docs/rust/` 生成 web-content v3.0.x 中全部未排除的页面，退出码 0；输出中没有 `localhost:19530`、`root:Milvus`，没有被排除的模块与页面。
- 每页的 front matter 符合上表；侧边栏中模块与页面按字母顺序排列。
- 指向被排除页面的链接变成文字，并给出提示；手册内其他链接都能打开。
- 第一次 Fetch 后，dev 上有 Rust 的全部页面、侧边栏与记录文件，UAT 上可以浏览；Guides 与其他 SDK 的输出不变。
- `remove` 与块／语言／代码行三级 `replace` 都有生成用例；参数说明与代码示例一致；新增 Cloud 文件的链接、图片、产品名与 MDX 均校验。
- 缺失变量值、重复或包含的映射、目标不存在／匹配不唯一、规则重叠、文件越界、非法占位符，以及 `add / position / channel` 都被拒绝。
- 原文目标按映射前内容匹配；Cloud 替换内容不被二次映射，但其中的禁止连接值仍使生成失败。仅改 Cloud 文件也会触发重新生成并改变输入摘要。
- 上游更新 PR 一次列出整本手册的变化；被替换原文改变但输出未变时仍提示复核，目标失效时校验失败。报告集成由 WP12 验收，WP-R1 提供来源与依赖信息。
