# 10 SDK Reference：从 web-content 生成（Rust 试点）

本篇定义怎样把 web-content 中的 SDK Reference 生成到 zdoc，先以 Rust 试点。要交付什么行为、文档工程师怎样写，见 [SDK Reference 产品需求](../prd-sdk-reference.md)；调研与选项见 [Rust SDK Reference 接入调研](../../research/rust-sdk-reference.md)。本篇只写工程上选定的做法。

**参与方**：zdoc 生成（shared-docs）、zdoc 发布（Fetch）。

**状态**：草稿，待与文档负责人确认（见文末“待确认”）。确认后，行为与作者的写法拆进产品需求，并在 Phase 1 实施计划中加上这一块范围（原范围不含 SDK Reference）。

## 目标与范围

- **试点：** Rust SDK Reference。Cloud 上还没有 Rust 手册，不涉及从飞书迁移、切换与归属。以后其他 SDK 照同一条路迁过来，REST 最后。
- **原文：** web-content 的 `API_Reference/milvus-sdk-rust/v3.0.x/`。它在 web-content 中手写维护（web-content 的 `AGENTS.md`：“hand-curated”），不是 md2md 的输出，没有变量。
- **不改上游：** 不改 web-content 的内容格式，不改 milvus.io 的构建与 Milvus 的发布流程。
- **只做 v3.0.x、只做英文。** 中文由现有的机器翻译从 dev 生成，不做人工校对。
- **与 Guides 的区别：** Guides 以页面为单位接入、变换与激活；SDK Reference 以整本手册为单位，不做页面内的内容定制（原因见下文“Cloud 的差异”）。

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
```

“manual”（手册）沿用 zdoc `packages/docs-tooling/src/manuals/registry.ts` 的叫法：网站上每一本可以独立导航的文档是一个 manual。

### `manual.yaml`

<details>
<summary>例子：Rust 的完整 manual.yaml</summary>

```yaml
# 配置格式的版本，固定为 1
schema_version: 1

# 原文在上游仓库中的位置
source:
  # 这本手册的原文目录：目录下的每个 .md 是一页，一级子目录是一个模块
  dir: API_Reference/milvus-sdk-rust/v3.0.x
  # 上一个版本的目录，只用来推出 added_since
  previous: API_Reference/milvus-sdk-rust/v2.6.x

# 发布到哪本手册：registry.ts 中的手册 ID
publish:
  manual: rust

# 不发布的内容；没有列出的模块和页面都发布，新增的页面也自动发布
exclude:
  modules: [ResourceGroup]        # source.dir 下的一级目录
  pages:
    - About.md                    # 着陆页由 Cloud 编写，见下文

# 原文中写死的 Milvus 值，键是 Variables.json 中的变量名
milvus_values:
  example_endpoint: "http://localhost:19530"
  example_token: "root:Milvus"

# 元数据的例外：以 / 结尾的是模块，.md 结尾的是一页；同一字段以页面为准
metadata:
  Snapshots/:
    beta: ON REQUEST
  Collections/add_collection_function.md:
    deprecate_since: v3.0.x
  Collections/drop_collection_function.md:
    deprecate_since: v3.0.x
```

</details>

| 字段 | 必填 | 写什么 |
|---|---|---|
| `schema_version` | 是 | `1` |
| `source.dir` | 是 | 原文目录，相对于上游仓库根目录 |
| `source.previous` | 否 | 上一个版本的目录，只用来推出 `added_since` |
| `publish.manual` | 是 | `registry.ts` 中的手册 ID。地址前缀、标题后缀、侧边栏名从登记中取，不在这里重复 |
| `exclude.modules` | 否 | 不发布的模块，即 `source.dir` 下的一级目录 |
| `exclude.pages` | 否 | 不发布的页面，相对于 `source.dir` |
| `milvus_values.<变量名>` | 否 | 这个变量在原文中写死的 Milvus 值；变量名与 `Variables.json` 中的一致 |
| `metadata.<模块>/` | 否 | 对整个模块生效的元数据，只能写 `beta` |
| `metadata.<页面>.md` | 否 | 对一页生效的元数据，可以写 `beta`、`deprecate_since`、`added_since`、`description` |

优先级：页面级高于模块级，模块级高于默认值。其他 front matter 字段由规则生成，不开放覆盖。`source.dir` 下新增的模块与页面默认发布，不需要改配置；它们在上游更新 PR 中单独列出，由审核的人决定是否排除。

### `lock.yaml`

格式与 Guides 的页面 lock 相同（技术设计 [04](./04-channels-and-lock.md#每页一份-lockyaml)），只是整本手册一份。接入时由工具取跟踪分支的最新提交写入，`current` 与 `next` 相同。Phase 1 中两者始终一起移动，见下文“上游更新”。

### 生成

工具读取 `manual.yaml` 时，把 `source.dir` 下每个未排除的 `.md` 文件展开成内存中的一份页面配置，所有页面共用同一个 lock。之后的读取、站点适配、链接、产品名检查与 MDX 编译沿用 Guides 的实现（技术设计 [02](./02-page-config.md)、[02b](./02b-links-and-images.md)、[07](./07-site-adaptation.md)）。不调用 md2md：原文中没有变量与片段。

一页的处理顺序：

1. 按 lock 中的 commit 读原文；
2. 连接值认回变量，换成 Cloud 的值（见下文）；
3. 站点适配，生成 front matter；
4. 链接换算；
5. 产品名检查；
6. MDX 编译。

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
| 页面内的增加、替换、删除 | 不支持 |

### 连接值

web-content 中的 `http://localhost:19530`、`root:Milvus` 就是 milvus-docs `Variables.json` 中 `example_endpoint`、`example_token` 的 Milvus 值，相当于变量已经按 Milvus 展开过。工具只在代码块中，把 `milvus_values` 中列出的值认回变量，再按组目录的 `Variables.json` 换成 Cloud 的值，例如 `YOUR_CLUSTER_ENDPOINT`。正文中的值不认回：正文说的是 Milvus 的默认地址，由产品名检查发现。

替换之后，`product-names.yaml` 仍检查 `localhost:19530`、`root:Milvus`，出现即失败（`PRODUCT_NAME_FOUND`）。上游出现新写法时（例如不带 `http://`），由人在 `milvus_values` 中补一行。

涉及 4 页：`Client/ConnectConfig.md`、`Client/MilvusClientV2.md`、`DataImport/BulkImport.md`、`CDC/update_replicate_configuration.md`。

### 产品名

| 写法 | 例子 | 处理 |
|---|---|---|
| SDK 的名字 | “Milvus Rust SDK”、`milvus::`、`milvus-sdk-rust` | 放行 |
| 服务端的版本 | “require Milvus 2.6.17 or later”、“Deprecated since Milvus 2.5.4” | 放行：Cloud 集群也用 Milvus 内核，版本说法成立 |
| 同时讲两种部署 | “open-source Milvus with `files`, Zilliz Cloud object storage with …” | 放行 |
| 指代服务端 | “the connected Milvus server”、“a specific Milvus instance” | 警告：照常生成，在构建摘要与上游更新 PR 中列出位置；上游改成中性的说法，例如 “the connected server” |
| 连接值 | `localhost:19530`、`root:Milvus` | 失败 |

这要求 `product-names.yaml` 的规则可以按条写严重程度（`error` 或 `warning`，默认 `error`）。Guides 组的规则不写，行为不变。Rust 的正文中共 24 处 “Milvus”，约 14 处属于“指代服务端”。

### 为什么不支持页面内的内容定制

变换（技术设计 [02](./02-page-config.md#变换的执行)）都以原文中的命名块为目标，代码行级的变换也要先指定命名块。web-content 中没有命名块，又定了不改 web-content，所以没有目标可用。以后某一页确实需要 Cloud 独有的内容，可以在 web-content 中加命名块、复用 WP10；前提是 milvus.io 渲染 `API_Reference/` 时不显示 HTML 注释，并且 web-content 的维护者愿意配合。

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
- **dev 上的初始内容。** 按 `manuals/README.md` 的“First-publish bootstrap”，新手册第一次正式 Fetch 前，dev 上要已经有手册的内容、`generated/en/sidebars/rust.sidebar.js` 与重新生成的 `deploy/contracts/localization-inputs.inventory.json`。`content/`、`generated/` 归 dev，不能经 master 提交，同步也不会搬，由文档负责人手工放一次；三样文件用 `shared-docs build` 的输出。
- **新手册的 7 步**（`manuals/README.md`）：

| 步骤 | 内容 | 提交到 |
|---|---|---|
| 1 | 在 `registry.ts` 中登记 `rust` | master |
| 2 | 重新生成派生文件：`generate:reference-presentation`、`generate:reconciliation-policy`、`generate:lark-config` | master |
| 3 | 着陆页 `rust.md`，加入 `masterAuthoritativePaths` | master |
| 4 | 静态约定：侧边栏恢复列表（`scripts/restore-generated-state.sh`）、`deploy/contracts/path-filters.json`、翻译分组（`scripts/translation/selection.js`） | master |
| 5 | dev 上的初始内容 | dev，由文档负责人放 |
| 6 | Fetch | — |
| 7 | 同步 master 到 dev | — |

## 上游更新

Phase 1 中 Rust 的 `current` 与 `next` 始终相同：上游更新 PR 同时改两者，合并后下一次 Fetch 写入 dev，发版时上 Prod。SDK Reference 记录的是已经发布的 SDK，web-content 在 SDK 发版之后更新，不需要先只在 UAT 显示。所以 Rust 用不到两版合并（WP11）。

上游更新（技术设计 [06](./06-upstream-changes.md)）对整本手册开一个滚动更新的 PR，不按页面拆。PR 中列出：

- 改动的页面与生成结果的差异；
- 新增、删除、改名的页面，以及因此改变的地址；
- 产品名警告；
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
| dev 上的初始内容 | 我们准备文件，文档负责人放到 dev |
| Phase 1 不区分 `current` 与 `next` | 上游更新同时改两者 |

## 工作包

| 工作包 | 内容 | 审阅 |
|---|---|---|
| **WP-R1**（只改 shared-docs） | 组目录与 `manual.yaml`、展开成虚拟页面、front matter、连接值、产品名检查的严重程度、排除、模块顺序、链接、`shared-docs lock` 与 `build` 支持手册组、PR 校验 | 发 FYI；PR 校验中能看到全部页面的生成结果 |
| **WP-R2**（Fetch 与上线） | `shared` 来源类型、`rust` 分组、workflow 中的判断、记录文件、`registry.ts` 登记与 7 步中 master 上的部分、着陆页 | 文档负责人评审；合并前跑一次只生成不发布的 Fetch |
| 上游更新的手册级 PR | 在 WP12 中实现，与 Guides 的逐页 PR 共用发现与 PR 的逻辑 | 随 WP12 |

WP-R1 做完，用真实的生成结果与文档负责人讨论 WP-R2。

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么整本手册一份配置。** Rust 有 164 页，web-content 一次提交常常改几十页（10-27、10-29 两次格式整理都改了全部页面）。每页一份配置意味着 328 个文件、每次几十个上游更新 PR；页面之间互相链接很多，整本手册也应该来自同一个 commit。展开成虚拟页面后，生成步骤照原样复用，只需扩展 lock、校验与上游更新。

**为什么认回变量，而不是写一张替换表。** 要匹配的值就是 milvus-docs `Variables.json` 中已有的 Milvus 值，不另起一套；只在代码块中认回，不会改到正文与 `milvus::` 这类名字；替换后的检查让上游的新写法马上暴露。

**为什么措辞只警告。** 整本手册只有一个 lock，一处措辞就会卡住全部页面的更新；措辞不影响使用，连接值会让用户连不上，所以只有连接值失败。

**为什么不在 web-content 中用变量。** milvus.io 直接渲染 `API_Reference/`，不经过 md2md；写成变量，Milvus 网站上会显示 `{{var.…}}`，除非改 milvus.io 的构建。

**为什么第一次 Fetch 就发布。** Rust 是新手册，没有旧页面需要切换或保护；发版本身就是一道关，发版前可以在 UAT 上检查。开关与整本手册的通道都要新写代码，换来的只是“晚一点发布”，控制登记的合并时间就能做到。

**为什么 Phase 1 不区分 `current` 与 `next`。** Guides 要让未上线功能的文档先只在 UAT 显示；SDK Reference 写的是已经发布的 SDK，不存在这种情况。

</details>

## 验收

- `shared-docs build` 对 `shared-docs/rust/` 生成 web-content v3.0.x 中全部未排除的页面，退出码 0；输出中没有 `localhost:19530`、`root:Milvus`，没有被排除的模块与页面。
- 每页的 front matter 符合上表；侧边栏中模块与页面按字母顺序排列。
- 指向被排除页面的链接变成文字，并给出提示；手册内其他链接都能打开。
- 第一次 Fetch 后，dev 上有 Rust 的全部页面、侧边栏与记录文件，UAT 上可以浏览；Guides 与其他 SDK 的输出不变。
- 上游改了若干页后，上游更新 PR 一次列出全部改动，合并后的 Fetch 只改这些页面。
