# SDK Reference 产品需求（Rust 试点）

**状态**：草稿。2026-11-02 调整配置叙事，Phase 1 支持页面内 `remove` 与 `replace`，不支持 `add`。本文描述拟交付的行为，不代表已实现；文末会议事项仍待确认。确认后并入[产品需求](./prd.md)并编号。工程约定见[技术设计 10](./design/10-sdk-reference.md)，调研见 [Rust SDK Reference 接入调研](../research/rust-sdk-reference.md)。

**方案**：Rust SDK Reference 从 web-content 生成到 zdoc，不经过飞书。一本手册用一份 `manual.yaml` 管理全部页面，配套来源配置、Cloud 变量表和检查规则。Fetch 按整本手册生成和发布，中文由现有机器翻译从 dev 生成。

## 范围与阅读顺序

- 原文取 `API_Reference/milvus-sdk-rust/v3.0.x/`。调研时有 164 页，实际发布排除规则之外的页面。
- 不改 Milvus 的发布流程；需要删除或替换的原文用命名块标记（HTML 注释，网页上不显示）。
- Rust 在 Cloud 上还没有手册，不涉及飞书迁移。Cloud 每个 SDK 只发布一个版本。

| 场景 | 回答的问题 |
|---|---|
| R1 接入一本手册 | 要准备哪些文件，每个文件写什么？ |
| R2 写 Cloud 的差异 | 怎样排除页面、映射连接值、删除或替换内容？ |
| R3 审核上游更新 | 原文变了，怎样检查和采用？ |
| R4 上线 | 配置合并后，怎样进入 dev、UAT 和 Prod？ |

## 场景 R1：接入一本手册

**用户故事**：作为文档工程师，我为整本 SDK Reference 配置一次，就能生成 Cloud 版本，不用逐页配置和复制正文。

### 文件分工

在 zdoc master 的 `shared-docs/rust/` 中准备这些文件。文件名沿用现有约定：`manual.yaml`、`Variables.json`（注意大小写）。

```text
shared-docs/rust/
  source.yaml          # 上游仓库与跟踪分支
  manual.yaml          # 手册目录、发布目标和差异
  Variables.json       # Cloud 的连接示例值
  product-names.yaml   # 生成后的残留与措辞检查
  lock.yaml            # 采用的上游 commit，由工具写入
  content/             # 需要替换大段内容时才创建，见 R2
```

| 文件 | 文档工程师写什么 |
|---|---|
| `source.yaml` | 从哪个仓库、哪个分支发现更新 |
| `manual.yaml` | 仓库中的手册目录、发布到哪本手册，以及 Cloud 的差异 |
| `Variables.json` | 连接地址、token 等示例值在 Cloud 中写成什么 |
| `product-names.yaml` | 哪些残留使生成失败，哪些措辞只提示复核 |
| `lock.yaml` | 不手写；bot 在接入 PR 中记录实际采用的 commit |

以下配置建立手册的基本结构；页面内变换先留空，到 R2 再填写。示例中的警告规则属于本次拟扩展的能力。

<details>
<summary>展开四份配置的基本写法</summary>

**`source.yaml`：仓库与分支。** 分支用于发现版本，实际生成读取 lock 固定的 commit。

```yaml
schema_version: 1
repository: https://github.com/milvus-io/web-content
track: master
```

**`manual.yaml`：手册的基本结构。** `source` 写仓库内路径，与上面的仓库配置分工不同。

```yaml
schema_version: 1

source:
  dir: API_Reference/milvus-sdk-rust/v3.0.x
  # 用来判断页面最早出现在哪个 SDK 版本，可省略
  previous: API_Reference/milvus-sdk-rust/v2.6.x

publish:
  manual: rust                # registry.ts 中登记的手册 ID

exclude:
  modules: [ResourceGroup]
  pages: [About.md]            # Cloud 单独编写着陆页

# 原文中的连接值，与 Variables.json 用同名键对应
milvus_values:
  example_endpoint: "http://localhost:19530"
  example_token: "root:Milvus"

metadata: {}                   # 元数据例外，见 R2
transforms: {}                 # 按页面删除或替换内容，见 R2
```

**`Variables.json`：Cloud 的连接示例值。** 这些是给读者看的占位值，不填真实凭据。

```json
{
  "example_endpoint": "YOUR_CLUSTER_ENDPOINT",
  "example_token": "YOUR_CLUSTER_TOKEN"
}
```

**`product-names.yaml`：检查生成结果。** 字符串规则沿用 Guides，命中即失败；对象形式新增 `severity`，可以只警告。下面是起始示例，接入时补齐需要检查的措辞。

```yaml
check:
  - "localhost:19530"
  - "root:Milvus"
  - text: "the connected Milvus server"
    severity: warning
  - text: "a specific Milvus instance"
    severity: warning
allow: []
```

</details>

### 提交与检查

配置可以先准备；正式 PR 的整本生成校验需要 WP-R2 提供 `rust` 手册登记。WP-R1 开发期间在隔离验证中使用测试登记预览，不代表手册已接入生产。

1. 提交配置 PR，不手写 `lock.yaml`。bot 取跟踪分支的 commit，写入 lock，并生成全部未排除页面。
2. 在 PR 中检查页面、导航、警告和错误。任一错误使整本手册校验失败，修正后再合并。
3. 配置合并不等于网站上线；手册登记、初始内容和第一次 Fetch 见 R4。

以后迁移 Go、Python 等 SDK，各自建组目录，使用各自的配置和 lock，与 Fetch 分组对应。

## 场景 R2：写 Cloud 的差异

**用户故事**：作为文档工程师，我保留可共用的原文，只配置 Cloud 不同的部分。

| 差异 | 写在哪里 | 规则 |
|---|---|---|
| 不发布整页或整个模块 | `manual.yaml` 的 `exclude` | 相对于 `source.dir`；未列出的内容默认发布，包括新增页面。其他页面指向被排除页的链接变成文字并给出提示 |
| 连接示例值不同 | `milvus_values` 与 `Variables.json` | 按同名键映射，只改上游代码块中的值 |
| 元数据例外 | `metadata` | 模块以 `/` 结尾，只可设 `beta`；页面以 `.md` 结尾，可设 `beta`、`deprecate_since`、`added_since`、`description`；页面优先 |
| 删除不支持的参数或内容 | `transforms` 中的 `remove` | 定位上游命名块、代码语言或连续代码行 |
| 参数说明或调用方式不同 | `transforms` 中的 `replace` | 同样定位目标，用 `content.file` 或 `content.lines` 提供 Cloud 内容 |
| SDK 介绍和连接指引 | Cloud 着陆页 `rust.md` | 在 master 单独维护，替代原文的 `About.md`，见 R4 |

### 连接值与元数据

连接值映射例如：`http://localhost:19530` → `example_endpoint` → `YOUR_CLUSTER_ENDPOINT`。`milvus_values` 的键必须在 `Variables.json` 中存在，否则失败。正文不做连接值替换；生成后仍残留禁止的连接值时，检查失败。

变量表适用于用法不变、示例值不同的情况。API key 改为 integration ID 涉及参数含义与调用方式，应使用下面的 `replace`，并确认实际 SDK／接口支持这种用法。

<details>
<summary>元数据例外示例</summary>

```yaml
metadata:
  Snapshots/:
    beta: ON REQUEST
  Collections/add_collection_function.md:
    deprecate_since: v3.0.x
```

其余字段由工具生成：标题取 H1 并加 `| Rust`；描述默认取 H1 下第一段并加相同后缀；在 `source.previous` 中已存在的页记为 `v2.6.x`，否则为 `v3.0.x`。`last_modified` 为 `FALSE`，避免把所有页面的最低 SDK 版本误标成 v3.0.x；`beta`、`deprecate_since` 默认 `false`。完整规则见[技术设计 10](./design/10-sdk-reference.md#地址路径与-front-matter)。

</details>

### 页面内删除与替换

`transforms` 的键是相对于 `source.dir` 的页面路径，每页下面是一组规则。每条规则与 [Guides 的变换](./prd.md#场景-4写-cloud-的差异)一致，使用 `operation / target / content`；Phase 1 只开放 `remove` 和 `replace`，写 `add` 会失败。

| 要改的范围 | `target` | `replace` 的新内容 |
|---|---|---|
| 整个命名块 | `block` | `content.file` |
| 代码组中的一种语言 | `block` + `language` | `content.file`，只含该语言的一个代码块 |
| 一种语言中的连续几行 | `block` + `language` + `lines` | `content.lines` |

`remove` 不写 `content`。两种操作都不写 `position`；本期也不写 `channel`，原因见 R3。命名块需先在 web-content 中标出，不能用配置替代上游标记。

<details>
<summary>删除示例：Cloud 不支持的副本参数</summary>

```yaml
transforms:
  Collections/load_collection.md:
    - operation: remove
      target:
        block: load-collection-replica-fields
    - operation: remove
      target:
        block: load-collection-example
        language: rust
        lines: |
          .replica_number(1)
```

这是需要上游配合添加的标记方案。调研发现还需处理 `Partitions/load_partitions.md` 的同类参数，以及 `Client/MilvusClientV2.md` 中介绍 ResourceGroup 的一条。若示例有多处相同行，要分别定位，不能用一条规则含糊匹配。

</details>

<details>
<summary>替换示例：参数说明与调用代码一起改</summary>

下面的页面名、命名块和方法调用仅用于说明配置格式，不表示 Rust SDK 已有或支持这些方法。接入真实页面前，先核对接口，再把参数说明和代码示例一起调整。

```yaml
transforms:
  SomeModule/example.md:
    - operation: replace
      target:
        block: authentication-parameters
      content:
        file: content/authentication-parameters.md
    - operation: replace
      target:
        block: request-example
        language: rust
        lines: |
          .api_key("YOUR_API_KEY")
      content:
        lines: |
          .integration_id("YOUR_INTEGRATION_ID")
```

`content/authentication-parameters.md` 写 Cloud 参数的名称、含义和要求。路径相对于 `manual.yaml` 所在目录，文件放在该组的 `content/` 下；不能引用组外文件。

</details>

**写规则时注意：** 代码行从上游复制，最多连续 5 行，必须在指定语言中恰好匹配一次，不能含空行；更大的改动用文件替换。Cloud 内容文件使用普通 Markdown 和代码围栏，直接写 Cloud 的值，不写变量／片段占位符、命名块或手写 Tabs；它不再经过连接值映射。内容中的链接、图片和产品名仍要校验，具体边界见技术设计 10。

**检查与维护：** 目标缺失、代码行匹配不唯一、规则重叠、替换文件缺失或越界，都会阻止这次生成。连接值残留使生成失败；SDK 名称与版本可以保留，指代服务端的 Milvus 措辞只警告。Cloud 替换内容由文档工程师维护，上游对应内容变动时需要复核，见 R3。

## 场景 R3：审核上游更新

**用户故事**：作为文档工程师，我在一个 PR 中查看整本手册的变化，决定是否采用。

- 每本手册一个滚动更新 PR，同时更新 lock 的 `current` 与 `next`。合并后下一次 Fetch 写入 dev，UAT 检查后随发版进入 Prod。
- PR 列出页面及生成结果的变化、新增模块、页面新增／删除／改名、地址变化和产品名警告。
- **被 `replace` 覆盖的上游内容有变化，即使 Cloud 输出没变，也列为需复核。** 审核人检查 Cloud 替换文件或代码行是否仍正确；工具不自动合并两份内容，也不能判断接口语义。
- 生成失败时仍开 PR 并标明原因，dev 保留已采用版本；修正配置或内容后再合并。

Phase 1 的 `current` 与 `next` 始终相同，不支持同一页在 UAT、Prod 显示不同版本。SDK 已发布不代表 Cloud 服务端已支持全部能力：整页用 `exclude`，页面内用 `remove / replace`，可见性标记用 `metadata`；整次更新尚不能采用时暂不合并。若需要长期保留两版内容，应重新评估此约束。

## 场景 R4：上线

**用户故事**：作为文档工程师，我知道配置通过后，还要完成哪些工程步骤才能上线。

| 步骤 | 做什么 | 负责方 |
|---|---|---|
| 工程接入（WP-R2） | 在 `registry.ts` 登记 `rust`，来源类型为 `shared`；接入 Fetch SDK 矩阵和翻译分组；将 Cloud 着陆页登记为 master 维护 | 实现者，文档负责人评审 |
| 准备 dev 初始内容 | 从 dev 建 `seed/rust-reference` 分支，准备生成的英文页面、`generated/en/sidebars/rust.sidebar.js` 和重新生成的 `deploy/contracts/localization-inputs.inventory.json` | 我们准备，文档负责人检查后放入 dev |
| 第一次 Fetch | 按配置和 lock 生成并写入 dev，之后由 Fetch 正常维护 | 现有发布流程 |
| 同步工具链 | 通过验证过的 master→dev 同步 PR 带入手册登记和站点配置；与首次 Fetch 的先后顺序需按新手册流程验证，见下方说明 | 实现者，文档负责人确认 |
| UAT 与 Prod 验收 | 核对导航、链接、连接值、删除结果，以及替换后的参数说明和代码示例；发版后检查 Prod | 文档工程师 |

表中列出所需环节，首次 Fetch 与工具链同步的先后顺序尚待验证：当前根 README 要求发布前同步工具链，新手册运行手册却要求首次 Fetch 在同步之前（来源与验证要求见技术设计 10）。

登记合并后的第一次正式 Fetch 前，必须先准备好 dev 初始内容。现有新手册流程要求侧边栏已存在，否则首次 Fetch 无法通过；不另设激活开关。配置、变量表、替换文件和着陆页在 master，生成页面、侧边栏由 dev 管理。UAT 与 Prod 构建同一个 dev SHA，Prod 随发版更新；流程细节见[技术设计 10](./design/10-sdk-reference.md#上线)。

## 会上要定的事

配置写法按本文讨论方案调整；以下外部集成事项尚未确认，不因本次改稿视为已定。

| 事项 | 我们的方案 | 结论 |
|---|---|---|
| 来源类型与 workflow | 新增 `shared`；无飞书来源的分组不要求飞书快照，不在 workflow 中继续列举 REST 等例外 | |
| 地址与标题 | `/reference/rust/rust/<模块>-<文件名>`，不加 `v2-`；标题后缀 `\| Rust`，上线后保持稳定 | |
| 排除范围 | 先排除 ResourceGroup；CDC、Snapshots 逐页核对 | |
| 页面身份 | 建议 `token: shared-rust-<模块>-<文件名>`、`type: origin`；确认翻译、修订记录、侧边栏不要求真实飞书 ID | |
| dev 初始内容与同步顺序 | 按 R4 准备英文页面、侧边栏、清单；确认是否还需中文侧边栏，并通过隔离验证确定首次 Fetch 与同步的顺序，消除两份运行指引的冲突 | |
| 上游命名块 | 为删除或替换目标加标记，需要 web-content 维护者配合；具体目标按真实接口与页面核对 | |
| current / next | 本期一起更新；确认是否常需让 SDK 内容跨多次 Cloud 发版仍只在 UAT 显示 | |
| 后续 SDK | 每个 SDK 各有组目录、来源、变量表和 lock，与 Fetch 分组对应 | |

## 分工与验收

| 工作包 | 范围与完成标准 |
|---|---|
| WP-R1：shared-docs | 手册配置与展开、连接值映射、`remove / replace` 与 Cloud 内容文件、产品名检查、排除、链接与元数据。隔离验证用测试登记生成全部未排除页面，结果随 PR 提供；目标或文件错误会失败，`add` 被拒绝 |
| WP-R2：Fetch 与上线 | 登记手册、分组、来源类型、着陆页和记录文件，打通正式 PR 生成校验；文档负责人评审，合并前验证只生成不发布的 Fetch |
| WP12：上游更新 | 整本手册一个 PR，包含被替换原文的变化提示；沿用共享文档的上游更新工作包 |

WP-R1 完成后用生成结果讨论 WP-R2；上线按 R4 执行。实现状态与证据记录在实现指南，不以本文中的示例代替验证。
