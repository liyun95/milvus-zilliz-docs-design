# 02 共享页配置

本篇定义文档工程师在 zdoc 中为一个共享页写什么：文件放在哪里、页面怎样标识、`page.yaml` 有哪些字段，以及怎样用 add、replace、remove 表达 Cloud 的差异。链接与图片由工具处理，见 [02b](./02b-links-and-images.md)。按任务的写法见[共享页面的写法与配置](../consumption-schema.md)。

**参与方**：文档工程师（编写）、zdoc 生成（读取与校验）。

**状态**：已定义，待文档负责人确认。

## 约定

### 一个共享页由哪些文件组成

`shared-docs/` 位于 zdoc 仓库根目录，在 master 分支上维护：所有修改都向 master 开 PR，合并后发布流程直接从 master 读取（见 [05](./05-publish-handoff.md#运行位置与触发)）。

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

**页面标识**就是 `pages/` 下的目录名，必须等于这一页现有的 slug（如 `delete-entities` 对应 `/delete-entities`）。目录名只能用小写字母、数字和连字符。它怎样替代飞书 `token`、供翻译清单与路由插件使用，见 [05](./05-publish-handoff.md#页面身份token)。

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
#   beta:        标题下的标签，不写就是 FALSE；可写 PUBLIC / PRIVATE / NEAR DEPRECATE
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
| `metadata.beta` | 否 | 页面标题下的标签，只影响 Guides；BYOC 的页面一律显示 “Contact Sales”。可选值：`FALSE`（默认，不显示）、`PUBLIC`（Public Beta）、`PRIVATE`（Private Beta）、`NEAR DEPRECATE`（Near Deprecation）。不沿用 Milvus 原文的 `beta` |
| `transforms` | 否 | Cloud 的差异，见下文“变换” |

其余 front matter 由工具生成，作者不写：

<details>
<summary>工具生成的 front matter</summary>

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

</details>

### 变换

`transforms` 是 `page.yaml` 中的一个列表，每一项是一条变换，表达 Cloud 与 Milvus 原文的一处差异。一条变换回答三个问题：改哪里（`target`）、怎么改（`operation`）、改成什么（`content`）；需要时再写加在前面还是后面（`position`），以及只对哪个通道生效（`channel`，见下文）。

#### 目标与操作

目标分三级，越往下越细：

| 级别 | `target` 写什么 | 适用于 |
|---|---|---|
| 整个命名块 | `block`：命名块 ID | 两种命名块（见 [01](./01-named-blocks.md#两种命名块)） |
| 代码组中的一种语言 | `block` 加 `language` | 只限代码组 |
| 一种语言中连续的几行 | `block`、`language` 加 `lines` | 只限代码组 |

- **`language`** 是代码块开头三个反引号后面的语言名，如 ```` ```python ```` 中的 `python`。它不一定等于标签页上显示的名字：NodeJS 写 `javascript`，cURL 写 `bash`，Zilliz CLI 写 `shell`。可用的值以 Tabs 规则文件 `presentation/cloud-sdk-tabs.yaml` 为准。同一个代码组中，每种语言只有一个代码块。
- **`lines`** 是从原文复制的一行或连续几行，最多 5 行，怎样匹配见下文。

每级目标都能做三种操作：

| 目标 | `add` | `replace` | `remove` | 新内容写在哪 |
|---|---|---|---|---|
| 整个命名块 | 在块前或块后插入，必须写 `position` | 换掉整块 | 删掉整块 | `content.file`：Cloud 内容文件（见下文）。替换代码组时写完整的代码组，多语言时是切换栏加各语言代码块 |
| 一种语言 | 给代码组加一种原来没有的语言；不写 `position`，顺序由 Tabs 规则决定 | 换掉这种语言的代码 | 删掉这种语言 | `content.file`：只写一个该语言的代码块，不加切换栏 |
| 几行 | 在这几行前或后插入，必须写 `position` | 换掉这几行 | 删掉这几行 | `content.lines`：直接写在配置中，不用写缩进 |

`position` 取 `before` 或 `after`，只在上表注明的两种 `add` 中写。`remove` 不写内容。

#### 写法示例

每一级各举一两例（取自不同页面，仅示意写法）：

```yaml
transforms:
  # 整个命名块：替换（OpenAI）
  - operation: replace
    target:
      block: before-you-start
    content:
      file: before-you-start.md

  # 整个命名块：在块后增加
  - operation: add
    target:
      block: choose-model
    position: after
    content:
      file: cloud-regions.md

  # 整个命名块：删除，只写目标
  - operation: remove
    target:
      block: product-notes

  # 一种语言：增加（Filtered Search 加 Zilliz CLI）
  - operation: add
    target:
      block: standard-filtering-code
      language: shell                    # 原来没有这个语言
    content:
      file: standard-filtering-cli.md    # 文件中是一个 shell 代码块

  # 几行：在后面增加一行（OpenAI 的 Java 示例）
  - operation: add
    target:
      block: define-function-code
      language: java
      lines: |                           # 从原文复制的定位行
        .param("model_name", "text-embedding-3-small")
    position: after
    content:
      lines: |
        .param("integration_id", "YOUR_INTEGRATION_ID")
```

其余组合照上表换 `operation` 即可。完整的页面示例见下文“例子”。

<details>
<summary>代码行怎样匹配（<code>lines</code>）</summary>

- **定位。** 只在目标代码组的目标语言中查找；`lines` 是一行或连续的几行，每行去掉行首缩进和行尾空格后比较，其余（包括行尾注释前的空格）必须完全一致，并且恰好出现一次。最多 5 行。
- **缩进。** 先去掉 `content.lines` 各行共同的行首空白，再在每行前加上原文中被替换或被定位的第一行的缩进，原样复制空格或 Tab；各行之间的相对缩进保留。新内容整体对齐到定位行，所以要选与新内容同一层级的行作定位。
- **不能有空行。** `lines` 与 `content.lines` 中都不能有空行，也不能有代码块的三个反引号或命名块标记。
- **超出范围就替换整种语言。** 一段代码中有多处不同，或连续超过 5 行，改为替换这种语言的代码。

</details>

#### 只对一个通道生效的规则

**lock 管原文的版本，`page.yaml` 管怎样加工。** 生成一页 Cloud 页面分两段：先按 lock 取 Milvus 原文（见 [04](./04-channels-and-lock.md)），再按 `page.yaml` 中的变换和 Cloud 内容文件加工。Prod 与 UAT 可能要显示不同版本的原文，所以每次生成跑两遍：

| | 原文 | 修改清单 | 结果 |
|---|---|---|---|
| 第一遍 | lock 中 `current` 的版本 | `page.yaml` | Prod 显示的版本 |
| 第二遍 | lock 中 `next` 的版本 | 同一份 `page.yaml` | UAT 显示的版本 |

原文有两个版本，原文本身在两版之间的变化由此自动区分，不需要在变换中声明（见 [04](./04-channels-and-lock.md#两个版本怎样合并成一页)）。但加工用的 `page.yaml`、Cloud 内容文件和 `Variables.json` 却只有一份，不受 lock 控制，合并后两遍立刻都用上（见 [04](./04-channels-and-lock.md#设计理由)）。默认每条变换两遍都执行，在两版原文上都必须成立；大多数时候这没有问题。

**`channel` 让某一条只在其中一遍执行。**

| 写法 | 在哪一遍执行 | 影响 |
|---|---|---|
| 不写 | 两遍都执行 | Prod 与 UAT |
| `channel: current` | 只在第一遍 | 只影响 Prod |
| `channel: next` | 只在第二遍 | 只影响 UAT |

**什么时候用。**

| 场景 | 默认写法为什么不行 | 写法 |
|---|---|---|
| Milvus 改了 Cloud 正在修改的那一行，上游更新 PR 把 `next` 指向了新原文 | 旧原文中有这一行，新原文中没有；同一条变换在第二遍找不到目标，上游更新 PR 无法合并 | 原来那条加 `channel: current`；按新原文另写一条，加 `channel: next` |
| 原文现在对 Cloud 也成立，Cloud 下次发布后才不同。示意：原文写每个 collection 最多 4 个向量字段，Cloud 下次发布提到 10 | 即使 lock 不变，替换规则一合并，第一遍也会执行，Prod 就提前换成了还没上线的说法 | 替换规则加 `channel: next`：UAT 先显示新说法，Prod 照常显示原文 |

以第一种场景为例：

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

<details>
<summary>第二种场景按时间走一遍</summary>

lock 一直是 `current: A`、`next: A`，两遍读同一版原文，原文写“最多 4 个”：

| 时间点 | `page.yaml` | 第一遍（Prod） | 第二遍（UAT） |
|---|---|---|---|
| 一开始 | 没有关于 Limits 的规则 | 4 个 | 4 个 |
| 合并替换规则，不加 `channel` | 多了“Limits 换成 10 个” | 10 个，功能还没上线 ❌ | 10 个 |
| 合并替换规则，加 `channel: next` | 同上，但只在第二遍执行 | 4 个 ✅ | 10 个 ✅ |
| 功能上线，提升 | 工具去掉 `channel` 标记 | 10 个 | 10 个 |

两遍结果不同，完全来自这条规则只在第二遍执行；原文一字未变。

</details>

**提升后自动收尾。** 功能上线时提升，lock 的 `current` 改成 `next` 的值，两遍从此用同一版原文。提升 PR 删除标 `channel: current` 的变换（它对准的旧原文已经用不上），去掉 `channel: next` 的标记（之后两遍都执行），见 [04](./04-channels-and-lock.md#提升)。所以 `channel` 只是过渡期的临时标记，作者不用回头清理。上游更新 PR 因上游修改而失败时，报告会直接给出按上面写法修改的建议（见 [06](./06-upstream-changes.md#出错时)）。

**与 `<NextChannel>` 的分工。** `<NextChannel>` 写在 Cloud 内容文件中，只能让 Cloud 新写的一段只在 UAT 显示（见下文“Cloud 内容文件”）；要替换或删除 Milvus 原文、并且只在一边生效，就用 `channel`。第二种场景在飞书中的写法，是用 `<NextChannel action="exclude">` 包住旧说法、`action="include"` 包住新说法；共享页的旧说法在两边共用的 Milvus 原文中，Cloud 不能在原文里加标签，所以改用 `channel: next`。

#### 其他规则

- 变换对 `publish` 中的所有手册都生效。SaaS 与 BYOC 之间的差异，用 Cloud 内容文件中 zdoc 现有的产品过滤写法表达。
- 同一位置有多条 `add` 时，按列表顺序输出。
- 目标的类型由原文结构决定，不由文件名决定；动作只由配置决定。

### Cloud 内容文件

Cloud 内容文件是 `add`、`replace` 要放进页面的新内容，放在这一页的目录中，由 `content.file` 指定。

**写法与 Milvus 原文相同。** 例如提示框写成 `<div class="alert note">`，多语言代码组写成切换栏加代码块。内容文件插入原文后，和原文一起往下处理：展开变量与片段、产品过滤，最后在站点适配中转换为 Cloud 组件（见[接口地图](./README.md#接口地图)）；用到的变量和片段一并记入依赖。所以作者只需要会一种写法。

| 写法 | 能否使用 | 说明 |
|---|---|---|
| 变量 `{{var.xxx}}`、片段 `{{fragments/xxx.md}}` | 可以 | 与原文一起展开，变量取 Cloud 的值 |
| zdoc 现有的产品过滤写法 | 可以 | 表达 SaaS 与 BYOC 之间的差异 |
| `<NextChannel>` | 可以 | 让一段内容只在 UAT 显示，见下文 |
| 页面目录下的图片文件，或外部图片地址 | 可以 | 见 [02b](./02b-links-and-images.md) |
| 命名块标记 | 不可以 | 命名块只用来定位 Milvus 原文 |
| 手写的 `<Tabs>`、`<Admonition>` 等 Cloud 组件 | 不可以 | 由工具在站点适配中生成；Tabs 的语言顺序与必选语言由工程维护的 Tabs 规则文件 `presentation/cloud-sdk-tabs.yaml` 决定 |

代码相关的内容文件怎样写（完整的代码组，或单种语言的一个代码块），见上文“目标与操作”。

### 首期不支持

<details>
<summary>首期不支持的写法</summary>

- 行号、正则、全文搜索、标题选择器，以及任意语法树路径或下标定位。
- 代码中的区域标记、超过 5 行或跨多处的行级修改：改为替换整个语言示例。
- 在共享原文中写产品指令或条件。
- move、copy、嵌套变换，以及对本轮插入内容的再次变换。
- 变量表达式、循环、条件模板，或把整段代码放进变量。
- 用脚本动态生成内容、插件式的自定义操作、自动判断不同语言示例是否等价。
- 独立编排多个共享命名块的页面：保留为扩展路径。
- front matter 中的 `keywords`、`hide_title`、`hide_table_of_contents`。
- `metadata.beta` 的 `DEPRECATED`：zdoc 支持，但目前没有页面使用，需要时再开放。

</details>

## 出错时

工具先校验全部配置，再生成页面。以下情况该页生成失败，不会静默跳过：

| 类别 | 生成失败的情况 |
|---|---|
| 页面与字段 | 页面目录名不符合 slug 规则；缺少必填字段；未知的字段、动作或 `schema_version`；`source.file` 在 lock 记录的 commit 中不存在；`publish[].manual` 不是 zdoc 已有的手册；`metadata.beta` 不是上述可选值（zdoc 遇到不认识的值会不显示标签、也不报错，所以在生成前拦下） |
| 目标 | 目标命名块、语言或内容文件不存在；内容文件路径指向页面目录之外 |
| `position` 与内容 | 在块旁或代码行旁 `add` 时没写 `position`；给代码组增加语言、`replace` 或 `remove` 时写了；`remove` 提供了内容 |
| 冲突（同一个通道中） | 同一个目标被多次变换；整块的 `replace` 或 `remove` 与该块的语言项变换、前后增加同时出现；语言项的 `replace` 或 `remove` 与该语言内的行级变换同时出现；同一语言内两条行级规则定位的行有重叠。不带 `channel` 的规则同时计入两个通道 |
| `channel` | 不是 `current` 或 `next`；页面在该通道中不存在（lock 中为 `none`） |
| 代码行 | `lines` 在目标语言中找不到、出现多次或超过 5 行；`lines` 用在没有 `language` 的目标上；`lines` 或 `content.lines` 中有空行 |
| 内容文件与 Tabs | 内容文件中出现命名块标记或手写的 Tabs；试图对本轮刚插入的内容再做变换；删除了 Tabs 规则要求必须存在的语言或默认语言 |

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
