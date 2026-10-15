# 共享页面的写法与配置

本文面向 Cloud 文档工程师，按常见任务说明一个共享页面要写哪些文件、怎么写。

**状态：随接口定义更新，待文档负责人确认。** 本文是作者手册，按任务说明写法；字段的正式定义、出错情形和首期不支持的写法见[接口设计 02《共享页配置》](./interfaces/02-page-config.md)。`examples/` 中的两篇样例仍是接口定义之前的草案写法，待接口确认后更新。

## 1. 写作原则

- **按身份定位。** 先按整页、命名块和语言定位；只有代码行可以在已定位的语言示例内按连续整行的原文定位。不使用行号、正则、全文搜索或标题选择器。
- **差异只有三种动作**：add、replace、remove；不按业务类型增加专门的操作。
- **变量沿用 md2md**：`Variables.json` 与 `{{var.xxx}}`；缺少 Cloud 绑定时报错，不静默使用 Milvus 的值。
- **原文不写 Cloud 的内容**：段落、章节和代码行的差异都写在 zdoc，原文只加中性的命名块，不写产品指令或条件。
- **生成文件不能手改**：发现问题回到对应的源文件。
- **作者成本**：每个共享页一份页面配置，Cloud 内容文件按需提供，共用文件在站点范围维护一次。
- **先消除漂移，再表达差异**：标题相同时随正文引用。先消除可以合并的历史漂移，再编码必须保留的产品差异；缺少语言、旧 SDK 写法或错误示例不能当作长期差异。

## 2. 一个页面涉及哪些文件

![一个共享页面涉及的文件：milvus-docs 中的共享原文（每页一份）和 Milvus 默认变量（共用）；zdoc 的 shared-docs 目录中的页面配置（每页一份）、Cloud 内容文件（按需，与页面配置放在同一目录）、Cloud 变量（共用）、链接映射表（共用）和 Tabs 规则（工程维护）。生成页面的 front matter 来自页面配置，正文来自共享原文，绑定 Cloud 变量，链接按映射表对应；替换的一节来自 Cloud 内容文件；代码 Tabs 来自共享原文的代码，凭证参数行按页面配置中的规则替换，再按 Tabs 规则生成。](./assets/file-relationships.png)

图 1 · 一个共享页面涉及哪些文件（以 OpenAI 页为例）
- **日常只改三类文件**：共同内容改共享原文 ①；Cloud 的差异改页面配置 ③ 和 Cloud 内容文件 ④。
- **共用文件很少动**：变量 ② ⑤ 只在新增变量时改；链接映射表 ⑥ 在链接无法自动对应时补一行；Tabs 规则 ⑦ 由工程维护者统一调整。
- **lock 由工具写入**：每页目录下的 `lock.yaml` 记录 Prod 与 UAT 各用 milvus-docs 的哪个 commit，作者不手改（[接口设计 04《通道与 commit 记录》](./interfaces/04-channels-and-lock.md)）。
- **“片段”只指 milvus-docs 的片段。** milvus-docs 现有的 `site/en/fragments/` 由正文用 `{{fragments/xxx.md}}` 引用、md2md 展开，与 Cloud 内容文件是两回事。Cloud 内容文件中也可以写 `{{fragments/xxx.md}}`，路径同样指 milvus-docs 的片段。

这些文件都在 zdoc 根目录的 `shared-docs/` 中：

```
shared-docs/
  source.yaml                        # 读哪个仓库、跟踪哪个分支（工程维护）
  Variables.json                     # Cloud 变量
  links.yaml                         # 链接映射表
  presentation/cloud-sdk-tabs.yaml   # 代码 Tabs 规则（工程维护）
  pages/
    delete-entities/                 # 目录名就是页面标识，等于这一页现有的 slug
      page.yaml                      # 页面配置
      lock.yaml                      # 工具写入
    openai/
      page.yaml
      lock.yaml
      before-you-start.md            # Cloud 内容文件
```

## 3. 按任务写

### 3.1 接入一篇共享文章

在 `shared-docs/pages/` 下建一个目录，目录名用这一页现有的 slug，在其中写 `page.yaml`。下面是整篇复用的 Delete Entities：

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
```

- 正文的标题和章节结构随原文引用，不需要在配置中重复。
- `slug`、标题后缀和其余 front matter 由工具生成，不要写。
- **导航仍在飞书中调整。** 首期，这一页在飞书知识库目录中的节点保留，导航中的位置、顺序和标签都由它决定；要移动这一页或改导航标签，和其他页面一样在飞书目录中操作（[接口设计 05《生成结果交给发布》](./interfaces/05-publish-handoff.md#导航首期)）。
- 提交 PR 后，工具在同一目录写入 `lock.yaml`，不要自己写。这一页对应的功能还没上线时，给 PR 加标签 `shared-docs: not-launched`，工具会让它先只在 UAT 显示（3.9 节）。
- PR 合并后，这一页只生成候选结果；由文档负责人激活后才正式发布。

### 3.2 把产品名或连接值写成变量

在共享原文中写变量，两端的 `Variables.json` 各自给值：

```markdown
In {{var.product_name}}, filtered searches are categorized into two types.
```

```python
client = MilvusClient(
    uri="{{var.example_endpoint}}",
    token="{{var.example_token}}"
)
```

| 变量 | Milvus | Cloud |
|---|---|---|
| `product_name` | `Milvus` | `Zilliz Cloud` |
| `example_endpoint` | `http://localhost:19530` | `YOUR_CLUSTER_ENDPOINT` |
| `example_token` | `root:Milvus` | `YOUR_CLUSTER_TOKEN` |

- 同一产品的各语言共用连接变量；各语言的参数名、引号和代码结构仍写在原文中。
- Cloud 只读 `shared-docs/Variables.json`，不合并 Milvus 的值；片段和 Cloud 内容文件中的变量同样按 Cloud 的值展开（[接口设计 03《md2md 预处理》](./interfaces/03-md2md-preprocess.md)）。
- `MilvusClient`、`pymilvus` 等真实名称，以及明确讨论 Milvus 本身的文字，不要写成变量。产品功能或流程不同时，不能靠改名掩盖，要用命名块和页面配置处理。
- 变量只放小粒度的值，不放整行代码。新增变量时，要同时在 milvus-docs 的 `site/en/Variables.json` 和 `shared-docs/Variables.json` 中给值。

### 3.3 替换一节

先在共享原文中为这一节加命名块。标记必须独占一行，ID 只用小写字母、数字和连字符：

```markdown
<!-- doc:block:start id="before-you-start" -->
## Configure credentials
……Milvus 的写法……
<!-- doc:block:end id="before-you-start" -->
```

再在页面配置中声明替换，Cloud 的内容写在同一目录的内容文件中：

```yaml
transforms:
  - operation: replace
    target:
      block: before-you-start
    content:
      file: before-you-start.md   # 即 shared-docs/pages/openai/before-you-start.md
```

内容文件提供完整的替换内容，包括这一节的标题。

**Cloud 内容文件的写法与 Milvus 原文相同**，例如提示框写成 `<div class="alert note">`，多语言代码组写成 `<div class="multipleCode">` 加代码块，工具会和原文一起转换成 Cloud 的组件。

| 可以用 | 不可以用 |
|---|---|
| 变量 `{{var.xxx}}`、片段 `{{fragments/xxx.md}}` | 命名块标记 |
| `<NextChannel>`（只在 Next 显示的内容，3.9 节） | 手写的 `<Tabs>`、`<Admonition>` 等 Cloud 站点组件 |
| zdoc 现有的产品过滤写法，用来区分 SaaS 与 BYOC | |
| 图片：页面目录下的文件，或外部地址 | |

### 3.4 在一节前后增加内容

原文中这一节必须已经是命名块，工具不会根据标题猜位置。例如在 OpenAI 页的 “Choose an embedding model” 后面加一段 Cloud 的提示：

```markdown
<!-- doc:block:start id="choose-model" -->
## Choose an embedding model
……模型表……
<!-- doc:block:end id="choose-model" -->
```

```yaml
transforms:
  - operation: add
    target:
      block: choose-model       # 加在这个命名块旁边
    position: after             # 加在后面；before 加在前面
    content:
      file: cloud-regions.md
```

生成结果中，`cloud-regions.md` 的内容紧跟在模型表之后、下一节标题之前。可以增加前置条件、提示、列表或带代码块的 Markdown。同一块旁可以有多条 add，同一方向按列表顺序输出。

### 3.5 删除一节

```yaml
transforms:
  - operation: remove
    target:
      block: product-notes
```

不提供内容文件，也不要用空文件表达删除。删除只影响 Cloud 输出，不改 Milvus 原文。删除代码组不会自动删除它外面的标题或说明，命名块应覆盖完整的语义范围，并检查预览中是否留下悬空的链接或锚点。

### 3.6 增加、替换或删除一个语言示例

在目标中加上 `language`。命名块的内容恰好是一个代码组时，才能按语言处理。下面是 Filtered Search 中为一个代码组增加 Cloud CLI 示例：

```yaml
transforms:
  - operation: add
    target:
      block: standard-filtering-code
      language: shell           # 要加的语言，原来必须没有
    content:
      file: standard-filtering-cli.md
```

- 给代码组加语言时**不写 `position`**：语言在 Tabs 中的顺序由全站的 Tabs 规则决定。
- add 时该语言必须还不存在；replace 和 remove 时必须已经存在。
- 内容文件包含一个语言匹配的完整代码块。
- 不再需要 Cloud 自己加的示例时，直接删掉那条 add，不要再加一条 remove。

### 3.7 代码中的个别行不同

共享原文的代码**不改**，只给整个代码组加命名块（写法同 3.3）。差异写在页面配置中：在 `target` 里加上 `language` 和 `lines`，写出原文中要处理的连续几行。

**替换几行。** OpenAI 页的 Python 示例中，Milvus 用两行注释说明 `credential` 是可选参数，Cloud 则必须填 `integration_id`：

```yaml
transforms:
  - operation: replace
    target:
      block: define-function-code
      language: python
      lines: |                  # 从原文整行复制，行尾的注释也要带上
        # Optional parameters:
        # "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
    content:
      lines: |                  # 不用写缩进
        "integration_id": "YOUR_INTEGRATION_ID",
        # Optional parameters:
```

两行一起替换，`integration_id` 放在前面，原来的 “Optional parameters” 注释保留在后面，避免必填参数出现在“可选参数”下面。

**在几行前后增加。** 内容对齐后的 Java 示例中，在 `model_name` 一行后面加一行：

```yaml
transforms:
  - operation: add
    target:
      block: define-function-code
      language: java
      lines: |
        .param("model_name", "text-embedding-3-small")
    position: after
    content:
      lines: |
        .param("integration_id", "YOUR_INTEGRATION_ID")
```

```java
    .param("provider", "openai")
    .param("model_name", "text-embedding-3-small")
    .param("integration_id", "YOUR_INTEGRATION_ID")    // 新增，自动对齐
    .build();
```

**删除几行**：写 `operation: remove` 和 `lines`，不写 `content` 与 `position`。

**缩进怎样处理：**

- **匹配时忽略缩进。** 每行去掉行首缩进和行尾空格后比较，行中间的内容（包括行尾注释前的空格）必须一字不差。YAML 中怎样缩进都不影响匹配。
- **写入时补上缩进。** 工具先去掉 `content.lines` 各行共同的行首空白，再在每行前加上原文中“被替换或被定位的第一行”的缩进（原文用空格就是空格，用 Tab 就是 Tab）。各行之间的相对缩进保留：

  ```yaml
  content:
    lines: |
      "integration": {
          "id": "YOUR_INTEGRATION_ID"
      },
  ```

  若原文那一行缩进 8 个空格，写入后第一、三行是 8 个空格，第二行是 12 个空格。
- **选和新内容同一层级的行作定位。** 新内容整体对齐到定位行。想在 `params={` 里面加参数时，不要用 `params={` 定位，要用它里面已有的一行（如 `"provider": "openai",`）定位，再写 `before` 或 `after`。

**其他规则：**

- `lines` 在这个语言示例中必须恰好出现一次，最多 5 行。`lines` 和 `content.lines` 中都不能有空行，也不能有代码块的三个反引号或命名块标记。
- 定位行尽量选不常改的行。上游改了这几行时匹配失败，这一页的上游更新 PR 被拦下。这时不要直接改原规则：在 Prod 上线新版本之前，旧原文仍要能匹配。做法是给原规则加 `channel: current`，再按新原文复制一条规则，标 `channel: next`：

  ```yaml
  - operation: replace
    channel: current            # 旧原文的行，只对 Prod 生效
    target: { block: define-function-code, language: python, lines: "<旧的那一行>" }
    content: { lines: '"integration_id": "YOUR_INTEGRATION_ID",' }
  - operation: replace
    channel: next               # 上游修改后的行，只对 UAT 生效
    target: { block: define-function-code, language: python, lines: "<新的那一行>" }
    content: { lines: '"integration_id": "YOUR_INTEGRATION_ID",' }
  ```

  上游更新 PR 的报告会给出这样的修改建议。提升时，工具自动删除 `channel: current` 的规则、去掉 `channel: next` 的标记。
- 一段代码中有多处不同，或连续超过 5 行，改为用 3.6 节替换整个语言示例。
- 共享原文中不写产品指令（如 `include-next-line`），Milvus 站点上看到的就是原文的代码。

### 3.8 链接与图片

**图片不用写任何配置。** 原文和 Cloud 内容文件中的图片，由工具按内容转存到 zdoc 的图片存储，并改写地址。

**链接大多也不用管。** 工具按类型处理 Cloud 最终页面中留下的链接：

| 链接 | 工具怎样处理 |
|---|---|
| 指向标题的锚点，如 `#Delete-Entities-by-Primary-Keys` | 换成 Cloud 的锚点写法（全部小写） |
| 外部网站、milvus.io 的完整地址 | 原样保留 |
| Milvus 站内页面，如 `primary-key-search.md` | 依次查找：目标也是共享页 → 链接映射表 → Cloud 的同名页面 |
| 以 `/` 开头的站内路径 | 报错 |

只有当工具报错“找不到 Cloud 对应页面”时，才需要在 `shared-docs/links.yaml` 中补一行。每个 Milvus 页面全站只登记一次：

```yaml
boolean.md: filtering-overview                    # Cloud 中对应的页面
ivf-flat.md: https://milvus.io/docs/ivf-flat.md   # Cloud 没有对应页时，可以明确指向 Milvus 站点
```

以 `/` 开头的站内路径（如 `/api-reference/...`），回 milvus-docs 改成完整地址，或在映射表中处理。指向 Milvus 站点的做法尚待文档负责人确认。完整规则见[接口设计 02b《链接与图片》](./interfaces/02b-links-and-images.md)。

### 3.9 让内容只在 Next 显示

| 内容 | 写法 |
|---|---|
| Cloud 内容文件中新增或替换的内容 | 在文件里直接用 `<NextChannel action="include">` 包住 |
| 共享原文中的变化 | 不需要写。lock 中 `current` 与 `next` 两个版本的差异由工具成对包进 `<NextChannel>` |
| 用 Cloud 内容替换原文的某一节，但只在下次发布时生效 | 这条变换规则标 `channel: next`，Prod 继续显示原文；提升时工具去掉标记 |
| 整个页面（新页面还没上线，或要下线的页面） | 不在页面配置中写。新页面：接入 PR 加标签 `shared-docs: not-launched`，工具把 `current` 写成 `none`；下线：Cloud 文档工程师运行下线工作流，工具开 PR 把 `next` 改为 `none`（[接口设计 04](./interfaces/04-channels-and-lock.md#写入与提升)） |

共享原文本身不写通道标记。Cloud 上线时，Cloud 内容文件去掉包裹；共享原文的差异和整页的上线、下线，都通过提升 lock 完成，规则见[接口设计 04《通道与 commit 记录》](./interfaces/04-channels-and-lock.md)。场景说明见[方案总览第 4.3 节](./proposal.md#43-何时上线prod-与-uat-各固定一个-commit)。

## 4. 什么情况会报错

工具先校验全部配置，再生成页面；出错时直接失败，不会静默跳过。完整的出错情形、字段定义和首期不支持的写法见[接口设计 02《共享页配置》](./interfaces/02-page-config.md)；链接与图片的错误见 [02b](./interfaces/02b-links-and-images.md#出错时)，变量与片段的错误见 [03](./interfaces/03-md2md-preprocess.md#出错时)。
