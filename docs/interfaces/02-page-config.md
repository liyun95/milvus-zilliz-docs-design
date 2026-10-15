# 02 共享页配置

本篇定义 Cloud 文档工程师在 zdoc 中为一个共享页写什么：文件放在哪里、页面怎样标识、`page.yaml` 有哪些字段，以及怎样用 add、replace、remove 表达 Cloud 的差异。链接与图片由工具处理，见 [02b](./02b-links-and-images.md)。按任务的写法见[共享页面的写法与配置](../consumption-schema.md)。

**参与方**：Cloud 文档工程师（编写）、zdoc 生成（读取与校验）。

**状态**：已定义，待文档负责人确认。

## 约定

### 目录

```
shared-docs/
  source.yaml                        # 共享来源配置：仓库与跟踪分支（见 04）
  Variables.json                     # Cloud 变量（见 03）
  links.yaml                         # 链接映射表（见 02b）
  presentation/cloud-sdk-tabs.yaml   # 代码 Tabs 规则，工程维护
  pages/
    delete-entities/                 # 目录名即页面标识
      page.yaml                      # 页面配置，作者编写
      lock.yaml                      # 版本记录，工具写入（见 04）
    openai/
      page.yaml
      lock.yaml
      before-you-start.md            # Cloud 内容文件，按需提供
```

### 页面标识

页面标识就是 `pages/` 下的目录名，必须等于这一页现有的 slug（如 `delete-entities` 对应 `/delete-entities`）。目录名只能用小写字母、数字和连字符。它怎样替代飞书 `token`、供翻译清单与路由插件使用，见 [05](./05-publish-handoff.md#页面身份token)。

### 页面配置 `page.yaml`

```yaml
schema_version: 1                       # 配置格式版本，固定写 1

source:
  # 这一页引用的 Milvus 原文，路径相对于 milvus-docs 仓库根目录
  file: site/en/userGuide/insert-and-delete/delete-entities.md

publish:
  # 发布到哪些手册；每个手册各生成一份
  - manual: guides                      # Guides（SaaS），标题自动加 “| Cloud”
    path: tutorials/development/insert-and-delete/delete-entities   # 在手册中的位置，决定导航层级
  - manual: guides-byoc                 # BYOC，标题自动加 “| BYOC”
    path: tutorials/development/insert-and-delete/delete-entities

# metadata:                             # 都可以不写
#   title:       不写就用 Milvus 原文的 title
#   description: 不写就用 Milvus 原文的 summary
#   beta:        不写就是 FALSE；可写 PUBLIC / PRIVATE / NEAR DEPRECATE
# 导航中的位置、顺序和标签首期由飞书目录决定（见 05b）

# transforms:                           # Cloud 的差异，见下文“变换”；Delete Entities 没有
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `schema_version` | 是 | 固定为 `1` |
| `source.file` | 是 | 共享原文路径 |
| `publish[].manual` | 是 | zdoc 现有的手册 ID，如 `guides`、`guides-byoc`。每个手册各生成一份，产品过滤与标题、描述的后缀按手册处理 |
| `publish[].path` | 是 | 页面在该手册中的路径，决定输出位置。首期必须与飞书节点生成的路径一致，不一致时生成失败（见 [05b](./05b-cutover-and-ownership.md#导航首期)） |
| `metadata.title` | 否 | 默认取 Milvus 原文的 `title` |
| `metadata.description` | 否 | 默认取 Milvus 原文的 `summary`（变量展开后）；两边不同时在这里改写 |
| `metadata.beta` | 否 | Cloud 的预览标签，默认 `FALSE`，不沿用 Milvus 原文的 `beta` |
| `transforms` | 否 | Cloud 的差异，见下文 |

其余 front matter 由工具生成，作者不写：

| front matter | 生成方式 |
|---|---|
| `slug` | `/` 加页面标识 |
| `sidebar_label`、`sidebar_position` | 首期按飞书节点填写，见 [05b](./05b-cutover-and-ownership.md#导航首期) |
| `title`、`description` 的后缀 | 按手册，如 `\| Cloud`、`\| BYOC` |
| `notebook`、`added_since`、`last_modified`、`deprecate_since` | 固定为 `FALSE` |
| `type` | `origin` |
| `displayed_sidebar` | `default` |
| `token` | 由页面标识代替，见 [05](./05-publish-handoff.md#页面身份token) |
| `channel` | 整页通道，由 lock 决定，见 [04](./04-channels-and-lock.md#只在一个通道存在的页面) |

### 变换

`transforms` 是 `page.yaml` 中的一个列表，每一项是一条变换。目标分三级：整个命名块、代码组中的一个语言、语言中连续的几行。下面列出常见写法（取自不同页面，仅示意写法）：

```yaml
transforms:
  # ① 替换一个命名块（OpenAI）
  - operation: replace
    target:
      block: before-you-start
    content:
      file: before-you-start.md          # 同一页面目录下的 Cloud 内容文件

  # ② 在一个命名块后面增加内容
  - operation: add
    target:
      block: choose-model
    position: after                      # 加在块后；before 加在块前
    content:
      file: cloud-regions.md

  # ③ 删除一个命名块：只写目标，不提供内容
  - operation: remove
    target:
      block: product-notes

  # ④ 给代码组增加一个语言（Filtered Search 加 Zilliz CLI）
  - operation: add
    target:
      block: standard-filtering-code
      language: shell                    # 原来没有这个语言
    content:
      file: standard-filtering-cli.md    # 文件中是一个 shell 代码块
    # 不写 position：语言顺序由 Tabs 规则决定

  # ⑤ 在代码行后面增加一行（OpenAI 的 Java 示例）
  - operation: add
    target:
      block: define-function-code
      language: java
      lines: |                           # 从原文复制的定位行
        .param("model_name", "text-embedding-3-small")
    position: after
    content:
      lines: |                           # 新的代码行，不用写缩进
        .param("integration_id", "YOUR_INTEGRATION_ID")
```

替换或删除一个语言、替换或删除几行代码，写法分别同 ④、⑤，把 `operation` 换成 `replace` 或 `remove`；`remove` 不写 `content`，`replace` 不写 `position`。完整的页面示例见下文“例子”。

| 字段 | 必填 | 说明 |
|---|---|---|
| `operation` | 是 | `add`、`replace` 或 `remove` |
| `target.block` | 是 | 命名块 ID |
| `target.language` | 否 | 只处理代码组中的这个语言；块的内容恰好是一个代码组时才能使用 |
| `target.lines` | 否 | 只处理这个语言中连续的几行，必须同时写 `language` |
| `position` | 视情况 | 在命名块或代码行旁 `add` 时必填，取 `before` 或 `after`；给代码组增加语言时不写，顺序由 Tabs 规则决定；`replace`、`remove` 不写 |
| `content.file` | `add` / `replace` 时 | Cloud 内容文件，相对于页面目录，不能指向目录之外 |
| `content.lines` | 目标有 `lines` 时 | 新的代码行，直接写在配置中，代替 `content.file` |
| `channel` | 否 | `current` 或 `next`：这条规则只对 Prod 或只对 UAT 的版本生效；不写则两个版本都生效。见下文“只对一个通道生效的规则” |

- 变换对 `publish` 中的所有手册都生效。SaaS 与 BYOC 之间的差异，用 Cloud 内容文件中 zdoc 现有的产品过滤写法表达。
- 同一位置有多条 `add` 时，按列表顺序输出。
- 块 ID 在源文件内唯一，语言在代码组内唯一。目标的类型由原文结构决定（见 [01](./01-named-blocks.md#命名块清单与块的类型)）；文件名不决定动作，配置才决定。
- 共享原文在 Prod 与 UAT 两个版本之间的变化不需要在变换中声明，由 lock 的两个版本自动区分（见 [04](./04-channels-and-lock.md#两个版本怎样合并)）。

### 代码行定位（`lines`）

- **定位。** 只在已经定位的代码组和语言示例内查找；`lines` 是一行或连续的几行，每行去掉行首缩进和行尾空格后比较，其余（包括行尾注释前的空格）必须完全一致，并且恰好出现一次。最多 5 行。
- **三种动作。** `replace` 换掉这几行，`remove` 删掉，`add` 配合 `position: before | after` 在这几行前后插入。
- **缩进。** 先去掉 `content.lines` 各行共同的行首空白，再在每行前加上原文中被替换或被定位的第一行的缩进，原样复制空格或 Tab；各行之间的相对缩进保留。新内容整体对齐到定位行，所以要选与新内容同一层级的行作定位。
- **不能有空行。** `lines` 与 `content.lines` 中都不能有空行，也不能有代码块的三个反引号或命名块标记。
- **超出范围就替换整个语言示例。** 一段代码中有多处不同，或连续超过 5 行，改为替换该语言示例。

### Cloud 内容文件

Cloud 内容文件与 Milvus 原文使用同一种 Markdown 写法（如提示框写成 `<div class="alert note">`，多语言代码组写成 `<div class="multipleCode">` 加代码块），与原文一起在流水线第 ⑥ 步转换为 Cloud 组件。

| 可以使用 | 不可以使用 |
|---|---|
| 变量 `{{var.xxx}}`、片段 `{{fragments/xxx.md}}` | 命名块标记 |
| `<NextChannel>` | 手写的 `<Tabs>`、`<Admonition>` 等 Cloud 站点组件 |
| zdoc 现有的产品过滤写法 | |
| 页面目录下的图片文件，或外部图片地址 | |

代码相关的内容文件按变换目标写：

| 变换目标 | 内容文件里写什么 |
|---|---|
| 整个代码组（目标只写 `block`） | 与 Milvus 原文相同：`<div class="multipleCode">` 加各语言的代码块 |
| 代码组中的一个语言（目标写了 `language`） | 只写一个该语言的代码块，不加 `multipleCode` 外壳，工具把它放进对应的代码组 |

转换为 Cloud 组件的规则（如多语言代码组的语言顺序与必选语言）由工程维护的 Tabs 规则文件 `presentation/cloud-sdk-tabs.yaml` 与工具共同决定，作者写配置和内容文件时不用考虑。

新增和替换的内容与原文一起展开变量与片段，并记入依赖。

**内容文件、`Variables.json` 与页面配置都只有一份，不按 lock 分两个版本。** Prod 与 UAT 由同一个 dev 提交构建，这些文件的修改合并后两边都会变（见 [04](./04-channels-and-lock.md#设计理由)）。还不能在 Prod 显示的内容，在内容文件中用 `<NextChannel>` 包住；Prod 要继续显示 Milvus 原文时，给规则加 `channel: next`（见下文）。

### 只对一个通道生效的规则

变换默认对 `current`（Prod）与 `next`（UAT）两个版本都生效，在两个版本上都必须成立。有两种情况需要一条规则只对一个通道生效，这时写 `channel`：

| 情况 | 写法 |
|---|---|
| 上游修改了 Cloud 定位的内容（如 `lines` 指定的代码行），过渡期内旧写法只在 `current` 中存在，新写法只在 `next` 中存在 | 原规则加 `channel: current`，另加一条按新原文写的规则，标 `channel: next` |
| Cloud 要在下次发布时才用自己的内容替换 Milvus 的某一节，Prod 继续显示 Milvus 原文 | 这条规则标 `channel: next` |

```yaml
transforms:
  # 旧原文的行：只对 Prod 生效
  - operation: replace
    channel: current
    target:
      block: define-function-code
      language: python
      lines: |
        # "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
    content:
      lines: |
        "integration_id": "YOUR_INTEGRATION_ID",

  # 上游修改后的行：只对 UAT 生效
  - operation: replace
    channel: next
    target:
      block: define-function-code
      language: python
      lines: |
        <上游修改后的那一行>
    content:
      lines: |
        "integration_id": "YOUR_INTEGRATION_ID",
```

- 带 `channel` 的规则只在对应版本上校验与生效；不带 `channel` 的规则在两个版本上都必须成立。
- **提升时由工具清理**：提升 PR 删除 `channel: current` 的规则，去掉 `channel: next` 规则上的标记（见 [04](./04-channels-and-lock.md#写入与提升)）。作者不用回头清理。
- 上游更新 PR 因上游修改而失败时，报告直接给出按上述写法修改的建议（见 [06](./06-upstream-changes.md#出错时)）。

### 首期不支持

- 行号、正则、全文搜索、标题选择器，以及任意语法树路径或下标定位。
- 代码中的区域标记、超过 5 行或跨多处的行级修改：改为替换整个语言示例。
- 在共享原文中写产品指令或条件。
- move、copy、嵌套变换，以及对本轮插入内容的再次变换。
- 变量表达式、循环、条件模板，或把整段代码放进变量。
- 用脚本动态生成内容、插件式的自定义操作、自动判断不同语言示例是否等价。
- 独立编排多个共享命名块的页面：保留为扩展路径。
- front matter 中的 `keywords`、`hide_title`、`hide_table_of_contents`。

## 出错时

工具先校验全部配置，再生成页面。以下情况该页生成失败，不会静默跳过：

- 页面目录名不符合 slug 规则；缺少必填字段；未知的字段、动作或 `schema_version`。
- `source.file` 在 lock 记录的 commit 中不存在；`publish[].manual` 不是 zdoc 已有的手册。
- 目标命名块、语言或内容文件不存在；内容文件路径指向页面目录之外。
- `position` 缺失或多余：在块旁或代码行旁 `add` 时没写，给代码组增加语言、`replace` 或 `remove` 时写了；`remove` 提供了内容。
- 在同一个通道中：同一个目标被多次变换；整块的 replace 或 remove 与该块的语言项变换、前后增加同时出现；语言项的 replace 或 remove 与该语言内的行级变换同时出现；同一语言内两条行级规则定位的行有重叠。不带 `channel` 的规则同时计入两个通道。
- `channel` 不是 `current` 或 `next`；页面在该通道中不存在（lock 中为 `none`）。
- `lines` 在目标语言示例中找不到、出现多次或超过 5 行；`lines` 用在没有 `language` 的目标上；`lines` 或 `content.lines` 中有空行。
- 内容文件中出现命名块标记或手写的 Tabs；试图对本轮刚插入的内容再做变换。
- 删除了 Tabs 规则要求必须存在的语言或默认语言。

链接与图片的错误见 [02b](./02b-links-and-images.md#出错时)，变量与片段的错误见 [03](./03-md2md-interfaces.md#出错时)，生成结果被手动修改见 [05](./05-publish-handoff.md#发布保护)。

## 例子

<details>
<summary>OpenAI 的完整 page.yaml（1b）</summary>

```yaml
schema_version: 1

source:
  file: site/en/userGuide/embeddings-reranking/embedding-function/openai.md

publish:
  - manual: guides                       # OpenAI 只发布到 Guides
    path: tutorials/development/function/text-embedding-functions/openai

metadata:
  # 两边描述不同，在这里改写
  description: Use an OpenAI embedding model with Zilliz Cloud by choosing an embedding model and creating a collection with a text embedding function.

transforms:
  # 整节替换：Milvus 讲怎样在 milvus.yaml 中配置密钥，Cloud 讲在控制台创建集成
  - operation: replace
    target:
      block: before-you-start
    content:
      file: before-you-start.md

  # 代码行替换：把可选的 credential 注释换成 Cloud 必填的 integration_id
  - operation: replace
    target:
      block: define-function-code
      language: python
      lines: |                           # 从原文整行复制，行尾的注释也要带上
        # Optional parameters:
        # "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
    content:
      lines: |                           # 不用写缩进
        "integration_id": "YOUR_INTEGRATION_ID",
        # Optional parameters:
```

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么放在 `shared-docs/`。** zdoc 规定 `content/`、`generated/` 等目录归 dev 分支，只由发布工作流写入；人编写的文件走 master，经同步 PR 进入 dev。共享页的配置由人编写，所以放在 `content/` 之外、归 master 管理的新目录中。

**为什么页面标识等于现有 slug。** 不另起一套 ID；目录名本来就必须唯一，zdoc 也用 slug 作路由。等于现有 slug 能让迁移后的 URL 保持不变，搜索收录和站外链接不受影响。

**为什么按手册发布。** Delete Entities 和 Filtered Search 在 zdoc 中各发布两份：Guides（SaaS，标题后缀 `| Cloud`）和 BYOC（标题后缀 `| BYOC`），来源是同一条飞书记录，由 `Publish Targets` 控制，两份只差标题和描述的后缀；OpenAI 只发布到 Guides。所以页面配置要列出手册，后缀由工具按手册添加，作者不手写。

**为什么作者只写 3 项元数据。** zdoc 现有 366 个英文 Guides 页面中，`notebook`、`added_since`、`last_modified`、`deprecate_since` 全部是 `FALSE`；`type` 有 365 页是 `origin`；`displayed_sidebar` 只有发布说明使用非默认值；`beta` 有 34 页不是 `FALSE`。所以只开放确实因页而异的项。导航标签与排序首期由飞书目录决定（见 05b），不在页面配置中重复。Milvus 原文的 `beta`（如 `Milvus 2.6.x`）是 Milvus 自己的版本说明，不沿用。

**为什么代码行差异写在 zdoc。** 同一段代码中只有个别行因产品而不同时，例如 Milvus 的可选 `credential` 注释与 Cloud 必填的 `integration_id`，原文的代码不改，只给代码组加命名块，由 zdoc 按原文中连续的整行定位并修改。不采用以下做法：

- **在原文中写 zdoc 产品行指令**（`include-next-line zilliz|milvus`）：Cloud 的代码会进入 Milvus 原文，Milvus 作者修改代码时要同时照顾 Cloud 的行，Milvus 发布链还要新增一套与 zdoc 理解一致的过滤。
- **在代码中加区域标记再替换**：标记要按每种语言写成注释，在代码内部清除，替换时还要按标记位置处理缩进。

**产品过滤沿用现有能力。** zdoc 的产品过滤（zilliz、saas、paas、milvus 等目标）在 Fetch 阶段执行。共享原文不写产品指令；Cloud 内容文件迁入 Git 后仍可使用现有写法，处理对象从飞书输入扩展到 Git 输入。

**为什么允许规则只对一个通道生效。** 规则默认对两个版本都要成立，但上游修改 Cloud 定位的代码行或命名块后，过渡期内旧写法只在 `current` 中存在、新写法只在 `next` 中存在，同一条规则无论怎样写都有一个版本失败，上游更新 PR 就无法合并。允许规则只对一个通道生效，过渡期可以新旧两条并存，提升时由工具合并回一条。同一机制也能表达“只在下次发布时用 Cloud 内容替换某一节”。

**为什么 Cloud 内容文件用 Milvus 的写法。** 这样工具对内容文件和原文做同一套转换，作者不用学第二种写法；本地样例也是这样实现的。

</details>

## 验收

- **T04**：内容变换的目标存在性、类型、语言和冲突检查；以 OpenAI 的凭证参数为真实用例验证代码行的 replace 与 add。
- **T06**：MDX、路由与 front matter 正确。
- **T13**：不适用的内容被过滤；通道相关部分见 04。
