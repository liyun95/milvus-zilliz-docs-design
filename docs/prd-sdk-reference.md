# SDK Reference 产品需求（Rust 试点）

**状态**：方案已按 2026-11-02 会议及会后讨论对齐，待实现。Phase 1 包含页内 `add / replace / remove`、zdoc 本地 Cloud 独有页面，以及整本手册的 `current / next`。本文描述拟交付的行为；文末列出仍需验证的接入事项。工程约定见[技术设计 10](./design/10-sdk-reference.md)，调研见 [Rust SDK Reference 接入调研](../research/rust-sdk-reference.md)。

**方案**：Milvus 原文从 web-content 读取，Cloud 独有页面和片段放在 zdoc，不经过飞书。一本手册用一份 `manual.yaml` 管理，配套来源配置、Cloud 变量表和检查规则。Fetch 读取已提交的文件，按整本手册生成；UAT 验收后按整本手册提升，中文由现有机器翻译从 dev 生成。

## 范围与阅读顺序

- 原文取 `API_Reference/milvus-sdk-rust/v3.0.x/`。调研时有 164 页，实际发布排除规则之外的页面。
- 不改 Milvus 的发布流程；页内变换依赖的原文位置用命名块标记（HTML 注释，网页上不显示）。
- Rust 在 Cloud 上还没有手册，不涉及飞书迁移。Cloud 每个 SDK 只发布一个版本。
- 首版需覆盖经核实的 Cloud 专有方法、属性和对象。人或 agent 可以辅助编写，内容经审核提交到 zdoc；Fetch 不负责临时生成 Cloud 正文。

| 场景 | 回答的问题 |
|---|---|
| R1 接入一本手册 | 要准备哪些文件，每个文件写什么？ |
| R2 写 Cloud 的差异 | 怎样补充独有页面、映射连接值、增删和替换内容？ |
| R3 审核上游更新 | 怎样让新内容先在 UAT 显示，保留 Prod 的版本？ |
| R4 上线 | 怎样接入发布流程，并按整本手册提升？ |

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
  lock.yaml            # current / next 的上游 commit，由工具写入
  content/             # Cloud 独有页面与页内片段，见 R2
```

| 文件 | 文档工程师写什么 |
|---|---|
| `source.yaml` | 从哪个仓库、哪个分支发现更新 |
| `manual.yaml` | 仓库中的手册目录、发布到哪本手册，以及 Cloud 的差异 |
| `Variables.json` | 连接地址、token 等示例值在 Cloud 中写成什么 |
| `product-names.yaml` | 哪些残留使生成失败，哪些措辞只提示复核 |
| `lock.yaml` | 不手写；bot 在接入 PR 中记录实际采用的 commit |
| `content/` | Cloud 独有页面与补充片段，和配置一起在 zdoc master 审核维护 |

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
cloud_pages: {}                # zdoc 本地完整页面，见 R2
transforms: {}                 # 页内增删与替换，见 R2
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

1. 提交配置与 Cloud 文件的 PR，不手写 `lock.yaml`。bot 取跟踪分支的 commit，初始 `current = next`，生成全部未排除的上游页面及本地页面。
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
| 在现有页面补充 Cloud 内容 | `transforms` 中的 `add` | 按 Guides 的定位规则插入本地片段；块或代码行用 `position: before / after` |
| 上游没有的完整页面 | `cloud_pages` | 声明手册内路径与 zdoc 本地文件，不需要虚构上游目标；参与导航、链接和通道管理 |
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

标题取 H1 并加 `| Rust`；描述默认取 H1 下第一段并加相同后缀。接口的引入、变更与废弃信息以上游明确记录为主，本地只补充经过核实的信息；未知版本不填，不通过目录或文件是否存在推算。具体变更内容保留在接口正文中，不压缩成一个版本标签。`last_modified` 为 `FALSE`；`beta`、`deprecate_since` 默认 `false`。SDK 接口生命周期与 Cloud 是否已上线分别管理，后者见 R3。完整规则见[技术设计 10](./design/10-sdk-reference.md#地址路径与-front-matter)。

Rust 页面的“最低 SDK 版本”只使用已确认的引入版本，废弃版本单独提示。例如 v3.0.0 引入、v3.1.0 废弃，最低版本仍为 v3.0.0；仅知道废弃时间时不显示最低版本。此展示需要 WP-R2 适配现有组件，不能仅靠写入元数据实现。

</details>

### 页面内新增、删除与替换

`transforms` 的键是相对于 `source.dir` 的上游页面路径，每页下面是一组规则。每条规则与 [Guides 的变换](./prd.md#场景-4写-cloud-的差异)一致，使用 `operation / target / content`，支持 `add / remove / replace`。

| 要改的范围 | `target` | `replace` 的新内容 |
|---|---|---|
| 整个命名块 | `block` | `content.file` |
| 代码组中的一种语言 | `block` + `language` | `content.file`，只含该语言的一个代码块 |
| 一种语言中的连续几行 | `block` + `language` + `lines` | `content.lines` |

`remove` 不写 `content`；`remove / replace` 不写 `position`。`add` 必须提供内容：在命名块或代码行前后插入时写 `position`，向代码组添加一种新语言时不写 `position`。规则默认两边生效，`channel: current / next` 限定通道，见 R3。命名块需先在 web-content 中标出；上游生成 skill 必须保留标记，并在提交前检查配对，不能用配置替代上游标记。

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

<details>
<summary>新增示例：页内片段与 Cloud 独有整页</summary>

以下路径和命名块仅说明配置格式，实际页面清单和接口用法需核实。

```yaml
transforms:
  SomeModule/example.md:
    - operation: add
      channel: next
      target:
        block: usage-notes
      position: after
      content:
        file: content/cloud-usage-notes.md

cloud_pages:
  CloudOnly/example.md:
    file: content/pages/cloud-example.md
    channel: next
```

`cloud_pages` 的键是手册内的逻辑路径，用于地址、导航和链接；`file` 相对于 `manual.yaml`，必须位于组内 `content/`。完整页面写 H1 和正文，不需要上游命名块，也不再套 Transform。逻辑路径不能与任一通道的上游页面或其他本地页面冲突，不能靠排除上游页隐式覆盖。

整页 `channel` 省略或为 `current` 时两边显示，`next` 时仅 UAT 显示，`retire-in-next` 时仅 Prod 显示。这与 Transform 中 `channel: current` 仅在 Prod 执行不同，分别沿用 Guides 的整页与规则约定。本地页面不依赖飞书的 Release Channel 字段。

整页设为 `next / retire-in-next` 时，页内不再写 `NextChannel`；需要块级分期的页面应两边都存在，再按段落控制。

</details>

**检查与维护：** 目标缺失、代码行匹配不唯一、规则重叠、本地文件缺失或越界，都会阻止这次生成。连接值残留使生成失败；SDK 名称与版本可以保留，指代服务端的 Milvus 措辞只警告。Cloud 文件由文档工程师维护，上游对应内容变动时需要复核，见 R3。

## 场景 R3：审核上游更新

**用户故事**：作为文档工程师，我在一个 PR 中查看整本手册的变化，决定是否采用。

- 每本手册一个滚动更新 PR，只更新 lock 的 `next`，保留 `current`。下一次 Fetch 将两版生成到同一份产物，UAT 显示新版本，Prod 继续显示已采用版本。
- PR 列出页面及生成结果的变化、新增模块、页面新增／删除／改名、地址变化和产品名警告。
- **被 `replace` 覆盖的上游内容有变化，即使 Cloud 输出没变，也列为需复核。** 审核人检查 Cloud 替换文件或代码行是否仍正确；工具不自动合并两份内容，也不能判断接口语义。
- 生成失败时仍开 PR 并标明原因，dev 保留已采用版本；修正配置或内容后再合并。

**只有上游原文锁定两个 commit。** `manual.yaml`、`Variables.json` 和 Cloud 文件各保留一份，配置合并后会影响两边；需要延后上线的改动必须明确通道。

| 内容 | 先在 UAT 显示的方式 |
|---|---|
| 上游原文变化 | 工具分别生成 `current / next`，用 `NextChannel` 合并差异；上游不手写通道标记 |
| 页内增删与替换 | Transform 写 `channel: next`；若两版需要不同规则，分别写 `current / next` |
| Cloud 文件中的独立新段落 | 用 `<NextChannel action="include">` 包住；旧段落仅 Prod 可见用 `exclude` |
| Cloud 独有整页 | `cloud_pages` 中设 `channel: next`，UAT 导航及直接地址可见；搜索范围见下方说明 |

不带通道的规则必须在两边都成立；只存在于一边的上游页面，需要只在该边执行的规则。Cloud 手写标记若落入工具生成的差异包裹内，校验失败，应改用规则级 `channel`。即使两边上游 commit 相同，通道规则也可能使输出不同。SDK 版本标签不控制 Cloud 的发布可见性。

**预览范围。** 已有页的 UAT 正文采用 next，但标题、描述等 front matter 沿用 current；next 独有页使用自己的元数据。Phase 1 的 Rust 中英文搜索统一索引 current 内容，UAT 搜索也不包含 next 专有内容；审阅 next 使用 UAT 导航和直接链接。Prod 的搜索结果标题、摘要和匹配文本不得出现 next 专有内容，静态 Markdown、llms、sitemap 同样采用 current。WP-R2 分别验证这些产物，不能用页面隐藏代替搜索验证。

## 场景 R4：上线

**用户故事**：作为文档工程师，我知道配置通过后，还要完成哪些工程步骤才能上线。

| 步骤 | 做什么 | 负责方 |
|---|---|---|
| 工程接入（WP-R2） | 登记 `rust` 与 `shared` 来源，接入 Fetch、翻译及手册记录的发布／恢复；补齐生命周期展示与 current 搜索；将着陆页登记为 master 维护 | 实现者，文档负责人评审 |
| 准备 dev 初始内容 | 从 dev 建 `seed/rust-reference` 分支，准备生成的英文页面、`generated/en/sidebars/rust.sidebar.js` 和重新生成的 `deploy/contracts/localization-inputs.inventory.json` | 我们准备，文档负责人检查后放入 dev |
| 第一次 Fetch | 按配置和 lock 生成并写入 dev，之后由 Fetch 正常维护 | 现有发布流程 |
| 同步工具链 | 通过验证过的 master→dev 同步 PR 带入手册登记和站点配置；与首次 Fetch 的先后顺序需按新手册流程验证，见下方说明 | 实现者，文档负责人确认 |
| UAT 与 Prod 验收 | 核对 Cloud 独有内容、导航、链接、连接值与三种变换；确认待发布内容在 UAT 可见、Prod 不可见，再按整本手册提升并发版 | 文档工程师 |

表中列出所需环节，首次 Fetch 与工具链同步的先后顺序尚待验证：当前根 README 要求发布前同步工具链，新手册运行手册却要求首次 Fetch 在同步之前（来源与验证要求见技术设计 10）。

登记合并后的第一次正式 Fetch 前，必须先准备好 dev 初始内容。现有新手册流程要求侧边栏已存在，否则首次 Fetch 无法通过；不另设激活开关。配置、变量表、Cloud 源文件和着陆页在 master，生成页面、侧边栏由 dev 管理。UAT 与 Prod 使用同一份产物，按运行时通道显示；写入 dev 不等于提升。

生成工具还需写出独立的手册级记录，逐页记录身份、来源、通道和输出摘要，并绑定整本页面集合及侧边栏。发布与恢复要携带同一份完整结果，缺页或记录不符就失败；不能直接把 Guides 单页记录的输出列表扩成整本手册。契约见[技术设计 10](./design/10-sdk-reference.md#手册级记录与恢复)。

**提升按整本手册开一个 PR**：`current` 改为已验收的 `next`，删除 `channel: current` 的临时 Transform、去掉 `channel: next` 的规则限定；Cloud 独有页的 NEXT 转为 CURRENT，RETIRE-IN-NEXT 的页移除，并检查引用。PR 同时列出仍有手写 `NextChannel` 的 Cloud 文件，由审核人确认哪些段落随本次上线处理；不自动清除所有标记。整本校验通过后合并，下一次 Fetch 与发版使 Prod 跟上。具体契约见[技术设计 10](./design/10-sdk-reference.md#上游更新与提升)。

页面或模块在提升后彻底消失时，PR 还要列出并清理遗留的 `metadata / exclude / transforms` 及导航、正文引用；无效配置仍会阻止提升。验收之后若 next 或相关配置、内容变化，需要重新生成并确认新内容，不能沿用旧验收。单独维护的 Cloud 着陆页不受上游 lock 控制，但其改动也参与验收，延后上线段落须写通道标记。

## 接入前待验证的事

设计方向已对齐；以下工程集成与真实内容仍需验证，不以讨论结论代替实现证据。

| 事项 | 我们的方案 | 结论 |
|---|---|---|
| 来源类型与 workflow | 新增 `shared`；无飞书来源的分组不要求飞书快照，不在 workflow 中继续列举 REST 等例外 | |
| 地址与标题 | `/reference/rust/rust/<模块>-<文件名>`，不加 `v2-`；标题后缀 `\| Rust`。改名导致地址变化时列出旧／新地址及引用，处理旧链接并验证后才能提升 | |
| 排除范围 | 先排除 ResourceGroup；CDC、Snapshots 逐页核对 | |
| 页面身份 | 建议 `token: shared-rust-<模块>-<文件名>`、`type: origin`；确认翻译、修订记录、侧边栏不要求真实飞书 ID | |
| dev 初始内容与同步顺序 | 按 R4 准备英文页面、侧边栏、清单；确认是否还需中文侧边栏，并通过隔离验证确定首次 Fetch 与同步的顺序，消除两份运行指引的冲突 | |
| 上游命名块 | 为变换目标加标记；上游 skill 保留标记并检查配对，具体目标和实际接线需与维护者核对 | |
| Cloud 内容完整性 | 首版覆盖经核实的 Cloud 专有方法、属性和对象；参考能力差异清单与 SDK 源码，由人审阅后提交 zdoc | |
| current / next | 复用 Guides 生成能力；验证真实双版本、Cloud 独有页和整本提升闭环 | |
| 记录与恢复 | 验证手册级新记录、完整页面集合、checkpoint 携带与恢复，不沿用 Guides 单页身份假设 | |
| 展示与搜索 | 验证最低版本与废弃提示分开；中英文 Rust 搜索只含 current，英文抓取与缓存需实际核验 | |
| 后续 SDK | 每个 SDK 各有组目录、来源、变量表和 lock，与 Fetch 分组对应 | |

## 分工与验收

| 工作包 | 范围与完成标准 |
|---|---|
| WP-R1：shared-docs | 手册展开、连接值、三种 Transform、本地页、检查、排除、链接与生命周期元数据；提供独立手册记录模型与纯校验。复用 WP10/11，隔离验证两通道，包括相同 commit 下仅本地规则不同的情况 |
| WP-R2：站点、Fetch 与上线 | 登记与分组、着陆页、侧边栏、记录认证及 checkpoint／恢复、Rust 生命周期 UI 与 current 搜索、正式 PR 校验；文档负责人评审，提供只生成不发布的 Fetch、隔离恢复回放和展示／搜索验证证据 |
| WP12：上游更新 | 整本手册一个 PR，只更新 `next`，包含被替换原文的变化提示 |
| WP13：提升 | 整本手册一个 PR，处理锁定版本、通道规则、独有页与消失页的配置引用，列出手写标记供审核；验收输入变化后重新确认 |

WP-R1 完成后用生成结果讨论 WP-R2；上线按 R4 执行。实现状态与证据记录在实现指南，不以本文中的示例代替验证。
