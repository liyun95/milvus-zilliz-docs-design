# Phase 1 产品需求

**状态**：草稿，待确认。

## 概述

Milvus 与 Zilliz Cloud 的功能文档有大量相同的内容，但现在各维护一份正文：Cloud 在飞书中编写，Milvus 在 milvus-docs 中编写，两边的修改靠文档工程师人工同步。社区对 Milvus 的修改容易漏抄回 Cloud；从飞书导出时，又可能把旧内容带回 Milvus、覆盖社区的修改。时间一长，两边越差越远。

改造后，共同的正文只在 milvus-docs 维护一份。Cloud 直接读取它，只在 zdoc 中维护与 Milvus 不同的部分，并且自己决定上游的修改是否采用、何时上线。飞书按页退出。

本文定义 Phase 1 交付后，文档工程师和文档负责人怎样完成日常工作：怎样写共享原文和 Cloud 的差异，怎样接入一页，怎样审核上游的修改，怎样上线和下线一页；每一步在网站上有什么结果，出错时怎样发现和处理。作者要写的语法，包括命名块标记、页面配置、链接映射表，也在本文中定下来。

本文是 Phase 1 评审、实现与验收的依据。工具内部怎样实现由技术设计决定，但必须满足本文。

| 相关文档 | 内容 |
|---|---|
| [方案总览](./proposal.md) | 为什么改、大方向（已冻结） |
| [写法速查](./authoring-spec.md) | 本文的附录：作者要写的文件、字段与出错情形的速查表 |
| [术语表](./glossary.md) | 本方案用到的术语 |
| [技术设计](./design/README.md) | 技术设计：工具怎样实现 |
| [Phase 1 实施计划](./phase-1.md) | 排期、任务与各项状态 |

## 1. 目标与范围

### 1.1 要满足的五条要求

[方案总览第 1.2 节](./proposal.md#12-改造需要满足的要求)提出五条改造要求，本文的场景逐条落实：

| 要求 | 具体指什么 | 落实在 |
|---|---|---|
| 1 milvus-docs 是唯一编辑源 | 共同的内容只在 milvus-docs 中改，社区的修改提交到那里即可；Cloud 不再保留一份需要人工同步的正文 | [场景 1](#场景-1把产品名和连接值写成变量)、[2](#场景-2在-milvus-原文中标出-cloud-要改的一段)、[3](#场景-3接入一页) |
| 2 Cloud 能表达差异 | Cloud 可以替换、删除或补充原文中的一节、一种语言的示例或几行代码，这些修改写在 zdoc 中，不影响 Milvus 的内容 | [场景 4](#场景-4写-cloud-的差异)、[5](#场景-5链接与图片) |
| 3 自动得知，自己决定采用 | milvus-docs 合并修改后，Cloud 不用人盯：工具每天检查，为受影响的页面开出上游更新 PR，列出哪些页面受影响、变了什么、哪些地方需要复核。Cloud 自己决定采用、暂缓还是先修改；采用后先在 UAT 显示，发版时才进入 Prod | [场景 7](#场景-7审核上游更新) |
| 4 未上线的功能不进 Prod | Cloud 还没上线的功能，可以在 UAT 提前审阅，但不出现在 Prod；功能上线时，再让 Prod 跟上 | [场景 6](#场景-6让内容先只在-uat-显示)、[8](#场景-8功能上线时提升) |
| 5 不经飞书，能力不丢 | 页面不再经过飞书中转，同时保留多语言代码、产品过滤、翻译、UAT / Prod 审核和恢复能力 | [场景 9](#场景-9从飞书切换到-git激活)、[10](#场景-10下线一页)、[第 5 节](#6-对现有能力的要求) |

### 1.2 两个阶段

| 阶段 | 试点页 | 交付的场景 | 做完的样子 |
|---|---|---|---|
| Phase 1a：整篇复用 | Delete Entities | 1、2、3、5 | 经真实的 zdoc 生成，页面内容完整；预览不具备写生产的权限；Milvus 发布不受影响 |
| Phase 1b：差异、上游更新与切换 | Filtered Search、OpenAI | 4、6、7、8、9、10 | 差异正确生成；上游修改经 PR 审核后采用；试点页切换上线，并通过后续更新、翻译与恢复的验证 |

**Phase 1 完成**，意味着批准的试点页已经从 Git 来源生成并上线，旧的飞书任务不能再覆盖或删除它们。只在本地生成页面，或只拿到预览，都只完成了一部分。

<details>
<summary>Phase 1 不做的事</summary>

- SDK Reference、全量迁移、Cloud 独有页的迁移、飞书全面退出。
- 把导航迁到 Git：Phase 1 导航仍在飞书目录中维护。
- 在 Milvus 原文中写 Cloud 的内容或产品条件。
- 按行号、正则、全文搜索或标题定位；超过 5 行或多处的代码行修改（改为替换整种语言的代码）。
- 移动、复制、条件模板等复杂写法；一页拼接多篇原文。
- 已切换的页面切回飞书。
- Milvus 侧的锚点校验。

</details>

## 2. 角色

| 角色 | 在本方案中做什么 |
|---|---|
| 文档工程师 | 同时负责 Milvus 与 Zilliz Cloud 文档。在 milvus-docs 中改共享原文、加变量与命名块；在 zdoc 中接入页面、写 Cloud 的差异、审核上游更新、提升；Phase 1 还要在飞书表格中处理整页的上线与下线 |
| 文档负责人 | 确认本文；激活页面，即在飞书表格中把一页标为由 Git 生成 |
| 社区贡献者 | 照常向 milvus-docs 提 PR，不需要了解 Cloud |
| zdoc / md2md 维护者 | 实现工具；维护代码 Tabs 规则、共享来源配置等工程文件 |
| 工具（自动） | 记录每页采用的版本、每天发起上游更新 PR、校验每个 PR、生成页面 |

## 3. 一个共享页由什么组成

**共享页**是正文引用 milvus-docs 原文、在 zdoc 中只维护差异的 Cloud 页面。

| 文件 | 在哪 | 谁写 | 多久改一次 |
|---|---|---|---|
| 共享原文 | milvus-docs | 文档工程师、社区贡献者 | 日常 |
| 页面配置 `page.yaml` | zdoc，每页一份 | 文档工程师 | 接入时写，有差异时改 |
| Cloud 内容文件 | zdoc，与页面配置同一目录，按需 | 文档工程师 | 有差异时 |
| Cloud 变量 `Variables.json` | zdoc，全站一份 | 文档工程师 | 新增变量时 |
| 链接映射表 `links.yaml` | zdoc，全站一份 | 工具生成初始内容，文档工程师审核；之后由文档工程师补 | 工具报错提示时补一行 |
| 产品名检查规则 `product-names.yaml` | zdoc，全站一份 | 文档工程师 | 检查误报、需要放行时补一行 |
| 版本记录 `lock.yaml` | zdoc，每页一份 | 只由工具写入 | 每个改变版本的 PR；样例见[第 4 节](#4-一页的生命周期) |
| 代码 Tabs 规则、共享来源配置 | zdoc，全站一份 | zdoc 维护者 | 很少 |

zdoc 中的文件都放在 master 分支根目录的 `shared-docs/` 下，所有修改都向 master 开 PR：

```
shared-docs/
  source.yaml                        # 共享来源配置：读哪个仓库、跟踪哪个分支（工程维护）
  Variables.json                     # Cloud 变量
  links.yaml                         # 链接映射表
  product-names.yaml                 # 产品名检查规则
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

**生成的页面不能手改。** 发现问题，回到上表中对应的源文件修改。

## 4. 一页的生命周期

网站分 **Prod**（正式站点）与 **UAT**（预发布站点）。每个共享页的 **`lock.yaml`** 记录 Prod 与 UAT 各用 milvus-docs 的哪个版本（commit）：

```yaml
# shared-docs/pages/delete-entities/lock.yaml
# 工具生成，不要手改
schema_version: 1
current: 1997ce96782b31f8628f22d31fad11007e4b924b   # Prod 用的 milvus-docs 版本
next: 1997ce96782b31f8628f22d31fad11007e4b924b      # UAT 用的 milvus-docs 版本
```

- 两者相同，Prod 与 UAT 显示同样的内容；不同时，UAT 先显示新版本。
- 文档工程师不手改它，但接入、上游更新、提升的 PR 都改它，审核时会看到它的变化。
- 整页只在 UAT 或只在 Prod 显示（功能还没上线的新页面、要下线的页面），Phase 1 沿用飞书表格的 `Release Channel`，不由 `lock.yaml` 表达（[场景 6](#场景-6让内容先只在-uat-显示)、[10](#场景-10下线一页)）。

![一个共享页的生命周期。上半部分是 Git 中的生命周期，由 lock 决定版本：写 page.yaml 接入，工具写入 lock；上游更新让 next 前进、提升让 current 跟上 next，每次发版重复；下线完成后用普通 PR 删除页面目录与 lock。下半部分是 Phase 1 过渡，由飞书表格决定来源与整页通道，飞书退出后不再需要：接入之后由文档负责人激活，即在表格中把 placement type 改为 Git，网站从飞书版换成 Git 版；下线时文档工程师把 Release Channel 改为 RETIRE-IN-NEXT，UAT 不再显示；发版时删除表格记录，这一页从网站和导航中移除，之后再删除页面目录。](./assets/page-lifecycle.png)

图 1 · 一个共享页的生命周期

**Git 中的生命周期**：下表每一步都是一个 zdoc PR，审核合并后生效。

| 步骤 | 谁做 | 网站上的变化 | 场景 |
|---|---|---|---|
| 接入 | 文档工程师开 PR，工具补上 `lock.yaml` | 无；Phase 1 要激活后才上网站 | [3](#场景-3接入一页) |
| 上游更新 | 工具每天自动开 PR，文档工程师审核 | UAT 显示新版本，Prod 不变 | [7](#场景-7审核上游更新) |
| 提升 | 功能上线时，文档工程师发起 | Prod 跟上 UAT | [8](#场景-8功能上线时提升) |
| 删除页面目录 | 下线完成后，文档工程师开普通 PR | 无；页面已在下线时从网站移除 | [10](#场景-10下线一页) |

**Phase 1 过渡**：飞书还不能退出，每一页原本都在飞书中编写，导航也仍由飞书表格和目录决定。所以这一页由谁生成、整页在哪一边显示，都在飞书表格中操作，与其他飞书页面相同；飞书退出后改由 Git 管理：

| 步骤 | 什么时候 | 谁做 | 在表格中做什么 | 网站上的变化 | 场景 |
|---|---|---|---|---|---|
| 激活 | 接入之后，一页只做一次 | 文档负责人 | 把 placement type 改为表示 Git 的值 | 这一页从飞书版换成 Git 版 | [9](#场景-9从飞书切换到-git激活) |
| 新页面上线 | 功能上线、提升的同一次发布 | 文档工程师 | `Release Channel` 从 `NEXT` 改为 `CURRENT` | Prod 开始显示这一页 | [6](#场景-6让内容先只在-uat-显示)、[8](#场景-8功能上线时提升) |
| 下线 | 决定下线时 | 文档工程师 | `Release Channel` 改为 `RETIRE-IN-NEXT` | UAT 不再显示，Prod 照常 | [10](#场景-10下线一页) |
| 下线完成 | 发版时 | 文档工程师 | 删除这一页的记录与飞书节点 | 这一页从网站和导航中消失 | [10](#场景-10下线一页) |

## 5. 场景

本节按文档工程师的日常工作组织，从写 Milvus 原文开始，到一页上线、更新和下线为止。每个场景开头列出阶段、谁来做和对应的技术设计；“系统行为”带编号，便于评审和验收时引用；错误码见[技术设计 09](./design/09-error-catalog.md)。

“技术设计”列出的是对应的篇目，不代表实现方案已经定稿；各篇的完成程度见[技术设计 README](./design/README.md)。

### 场景 1：把产品名和连接值写成变量

**阶段**：Phase 1a　**谁**：文档工程师

**技术设计**：[03 预处理](./design/03-md2md-interfaces.md#预处理)

**背景**：整篇复用的页面，两边常常只差产品名和示例中的连接地址、令牌。把这些值写成变量，两边各自给值，正文就能共用一份。

**用户故事**：作为文档工程师，我把原文中的产品名和连接值写成变量，Milvus 与 Cloud 各自显示自己的值，我只维护一份正文。

**怎样操作**

1. 在 milvus-docs 原文中，把产品名和连接值写成 `{{var.名字}}`，沿用 milvus-docs 现有的变量写法：

   ```markdown
   In {{var.product_name}}, filtered searches are categorized into two types.
   ```

   ```python
   client = MilvusClient(
       uri="{{var.example_endpoint}}",
       token="{{var.example_token}}"
   )
   ```

2. 新增的变量，两边都要给值：milvus-docs 的 `site/en/Variables.json` 给 Milvus 的值，zdoc 的 `shared-docs/Variables.json` 给 Cloud 的值。

   | 变量 | Milvus 的值 | Cloud 的值 |
   |---|---|---|
   | `product_name` | `Milvus` | `Zilliz Cloud` |
   | `example_endpoint` | `http://localhost:19530` | `YOUR_CLUSTER_ENDPOINT` |
   | `example_token` | `root:Milvus` | `YOUR_CLUSTER_TOKEN` |

**规则**

| 规则 | 例子 |
|---|---|
| 只放小粒度的值，不放整行或整段代码 | ✅ `uri="{{var.example_endpoint}}"`；❌ 把整个 `MilvusClient(...)` 调用放进变量 |
| 真实的名称不写成变量 | `MilvusClient`、`pymilvus` 保持原样 |
| 明确讨论 Milvus 本身的文字不写成变量 | “Milvus 的 `milvus.yaml` 配置”保持原样 |
| 产品功能或流程不同时，不能靠换名字掩盖 | 用命名块和变换处理（[场景 2](#场景-2在-milvus-原文中标出-cloud-要改的一段)、[4](#场景-4写-cloud-的差异)） |
| 同一产品的各语言共用连接变量；参数名、引号和代码结构仍写在原文中 | Python 与 Java 都用 `{{var.example_endpoint}}` |
| 变量名可以分层，不区分大小写 | `{{var.cloud.region}}` |

原文也可以照常用 `{{fragments/xxx.md}}` 引用 milvus-docs 的**片段**（`site/en/fragments/` 中多篇共用的一段内容）。片段中的变量同样取各自产品的值。

**产品名检查**

漏写变量时，Milvus 的产品名或连接值会直接出现在 Cloud 页面上。所以工具在合并前检查**生成后的 Cloud 页面**：出现检查规则中的写法，又不在放行清单中，这一页生成失败。规则写在 zdoc 的 `shared-docs/product-names.yaml`：

```yaml
# shared-docs/product-names.yaml
check:                                  # 出现就报错的写法
  - Milvus
  - localhost:19530
  - root:Milvus
allow:                                  # 确实要保留的写法，报错时由文档工程师补
  - Zilliz Cloud is built on Milvus
```

- 按整词匹配：`MilvusClient`、`pymilvus`、`milvus.yaml` 中的 Milvus 不算；链接地址不检查。
- 放行清单写完整的短语，不写单个词，避免把 `Milvus` 整个放过。
- milvus-docs 的 PR 检查只给提示，不拦截：它不知道哪些页面是共享页，Milvus 页面中也大量合法地写着 Milvus。

**系统行为**

| 编号 | 要求 |
|---|---|
| 1-1 | Cloud 只读 zdoc 的 `Variables.json`，不合并、不回退到 Milvus 的值 |
| 1-2 | 正文、片段、代码块和 Cloud 内容文件中的变量都按 Cloud 的值替换 |
| 1-3 | 变量值原样插入，不再当作变量或片段展开 |
| 1-4 | `{{var.…}}`、`{{fragments/…}}` 之外的 `{{…}}`（如代码中的模板语法 `{{ doc.content }}`）原样保留 |
| 1-5 | 原文和 Cloud 内容文件中的 `{{fragments/xxx.md}}`，只能引用同一版本 milvus-docs 中 `site/en/fragments/` 里的文件；zdoc 中没有 Cloud 自己的片段目录 |
| 1-6 | 生成后的 Cloud 页面中，出现检查规则中的写法、又不在放行清单中时，这一页生成失败，报错指出页面、版本和所在的原文位置；Prod 与 UAT 的版本分别检查 |

<details>
<summary>出错时</summary>

| 情况 | 在哪里发现 | 怎样改 |
|---|---|---|
| 变量在 Cloud 中没有值 | zdoc 的 PR 校验，或上游更新 PR 的校验 | 在 `shared-docs/Variables.json` 中补上 |
| 片段不存在、循环引用、嵌套太深或太大 | 同上 | 回 milvus-docs 修正 |
| Cloud 页面中出现没换成变量的产品名或连接值 | 同上 | 回 milvus-docs 改成变量；确实要保留的写法，在 `product-names.yaml` 的 `allow` 中补一行 |

</details>

**验收**：T02、T03、T14。

<details>
<summary>取舍</summary>

**为什么缺值就报错，不用 Milvus 的值。** 静默使用会把 `localhost:19530` 这类 Milvus 的值带到 Cloud 页面上，页面能生成，却没人发现。

**为什么不放整行代码。** 变量中的代码在原文里看不到，Milvus 作者改代码时会漏改；参数名和结构也因语言而异。

**为什么检查生成后的页面。** 写变量的规则只靠人记，迟早会漏。生成后的页面就是 Cloud 读者看到的内容，在这里检查最可靠，Milvus 原文中合法的 Milvus 字样不会被误报。

</details>


### 场景 2：在 Milvus 原文中标出 Cloud 要改的一段

**阶段**：Phase 1a 提供能力，Phase 1b 的试点页开始使用　**谁**：文档工程师

**技术设计**：[01 命名块的解析](./design/01-named-blocks.md)、[03 解析与清除](./design/03-md2md-interfaces.md#命名块的解析与清除)

**背景**：Cloud 要替换、删除或补充原文中的某一段，就要能稳定地指到这一段。按行号、标题或文档结构定位，上游一改就会失效，甚至悄悄指到错误的位置。所以在原文中给这一段起个名字，Cloud 按名字引用。这个有名字的一段叫**命名块**。

**用户故事**：作为文档工程师，我在 milvus-docs 中给 Cloud 要改的一段加上标记，Milvus 站点不受任何影响；之后上游移动或修改这段内容，Cloud 的引用也不会断。

**怎样操作**

1. 在 milvus-docs 中开 PR，在要改的一段前后各加一行标记，起一个 ID。标记是 HTML 注释，网站上不显示：

   ```markdown
   <!-- doc:block:start id="before-you-start" -->
   ## Configure credentials
   ……
   <!-- doc:block:end id="before-you-start" -->
   ```

2. PR 检查校验标记的写法，通过后合并。
3. 在 zdoc 的页面配置中按 ID 引用这一段（[场景 4](#场景-4写-cloud-的差异)）。

只在 Cloud 有差异的地方加命名块。整篇复用的页面不需要任何标记。

**两种命名块**：按包住的内容区分，类型决定 Cloud 能改多细。

| 类型 | 包住什么 | Cloud 能做什么 |
|---|---|---|
| Markdown 块 | 任意一段 Markdown：一节标题和正文、几个段落、一个列表 | 整块替换、删除，或在块的前后增加 |
| 代码组 | 恰好一组示例代码，不含说明文字 | 以上全部，还能只改其中某种语言（包括增删语言），或某种语言中的某几行 |

代码组按原文中代码的样子分两种情况：

**情况一：只有一种语言。** 原文中就是一个单独的代码块，直接包住它：

````markdown
<!-- doc:block:start id="install-cmd" -->
```shell
pip install pymilvus
```
<!-- doc:block:end id="install-cmd" -->
````

**情况二：多种语言。** milvus-docs 的多语言代码由语言切换栏 `<div class="multipleCode">` 和紧跟其后的各语言代码块组成，在 milvus.io 上显示为可以切换的标签页。标记要把**切换栏和全部代码块**一起包住：

````markdown
<!-- doc:block:start id="delete-code" -->
<div class="multipleCode">
    <a href="#python">Python</a>
    <a href="#java">Java</a>
</div>

```python
client.delete(collection_name="quick_setup", ids=[0, 1, 2])
```

```java
// ……
```
<!-- doc:block:end id="delete-code" -->
````

**规则**

| 规则 | 例子 |
|---|---|
| 标记必须独占一行 | ❌ `## Configure credentials <!-- doc:block:start id="x" -->` |
| ID 由小写字母、数字和连字符组成，以字母或数字开头，ID 加双引号 | ✅ `id="before-you-start"`；❌ `id="BeforeYouStart"`、`id=before-you-start` |
| ID 在同一个文件内唯一；开始与结束标记的 ID 一致 | 两个 `id="code"` 报错 |
| 代码组只包代码，不包说明文字 | 把代码前的一句说明也包进去，这一块就成了 Markdown 块，只能整块处理 |
| 多语言代码组必须连同切换栏一起包住，而且包住全部代码块 | ❌ 只包住其中的 Python 代码块，切换栏和 Java 代码块在块外 |
| 块内不能是空的 | — |
| 不能嵌套：块内不能再出现开始标记 | — |
| 只能写在页面文件中，不能写在片段中 | `site/en/fragments/` 中出现标记报错 |
| 写在示例代码中的标记只是普通文字，不算命名块，也不报错 | 贡献说明中教人写命名块的示例代码可以照常显示 |

<details>
<summary>报错的代码组包法</summary>

只包了 Python 代码块，切换栏和 Java 代码块在块外：

````markdown
<div class="multipleCode">
……
</div>

<!-- doc:block:start id="delete-python" -->
```python
……
```
<!-- doc:block:end id="delete-python" -->

```java
……
```
````

整块删除或替换后，会留下没有代码的切换栏，或没有切换栏的代码。

</details>

**系统行为**

| 编号 | 要求 |
|---|---|
| 2-1 | 标记不出现在任何网站上，也不出现在 web-content 的 Markdown 和提供给大模型读取的内容中 |
| 2-2 | 同一篇原文加标记前后，Milvus 站点的输出逐字相同 |
| 2-3 | milvus-docs 的 PR 检查校验标记，写错时检查失败、不能合并；报错指出文件、行号、原因 |
| 2-4 | Cloud 生成时用同一套规则再校验一次；漏过的错误让这一页生成失败，不带着错误上线 |
| 2-5 | 工具按原文结构判断命名块的类型和其中的语言，作者不用声明 |
| 2-6 | Cloud 的标签页由工具按代码块和 Tabs 规则重新生成，不使用切换栏的内容 |

<details>
<summary>出错时</summary>

| 情况 | 在哪里发现 | 怎样改 |
|---|---|---|
| 上表任何一条写法错误 | milvus-docs 的 PR 检查；万一漏过，zdoc 中这一页生成失败 | 回 milvus-docs 修正 |
| 命名块被上游改名或删除，Cloud 还在引用 | 上游更新 PR 的校验（[场景 7](#场景-7审核上游更新)） | 在同一个 PR 中修改 Cloud 的规则 |

</details>

**不做与已知局限**：不能嵌套；不能写在片段中。

**验收**：T01、T11。

<details>
<summary>取舍</summary>

**为什么用成对的注释。** 成对的开始、结束标记加名字，是 AsciiDoc 和 MkDocs Snippets 的通行做法；用 HTML 注释，是因为 Markdown 中只有注释在 milvus.io 上不显示。比它们更严格的地方：必须独占一行，避免切断段落和表格；不允许嵌套，让冲突规则保持简单；写错一律报错，问题尽早暴露。

**为什么不按标题定位。** milvus-docs 一年内有 17% 的候选页改过或删过标题；按结构定位可能找到错误的位置而不报错。

**为什么还要清除标记。** milvus.io 页面上虽然看不到注释，但 web-content 的 Markdown 和给大模型的内容里会有；清除后还能用“加标记前后输出逐字相同”作为可以自动检查的验收标准。

**为什么代码组要连同切换栏一起包。** 切换栏和后面的代码块是一个整体。块的边界与它一致，工具不用往块外查找，整块删除或替换时也不会留下孤立的切换栏。

</details>


### 场景 3：接入一页

**阶段**：Phase 1a　**谁**：文档工程师

**技术设计**：[02 页面配置](./design/02-page-config.md)、[04 接入一页](./design/04-channels-and-lock.md#接入一页)、[07 front matter](./design/07-site-adaptation.md#front-matter)、[08 工作流](./design/08-workflows-and-permissions.md)

**背景**：一页 Cloud 页面要从 Git 生成，先要告诉工具：它引用哪篇 Milvus 原文、发布到哪些手册、标题和描述是否要改写。

**用户故事**：作为文档工程师，我在 zdoc 中为一页写一份简短的配置，就能让工具从 Milvus 原文生成这一页的 Cloud 版本，不用复制正文，也不用查 commit。

**怎样操作**

1. 在 zdoc 中从仓库内的分支向 master 开 PR，在 `shared-docs/pages/` 下新建一个目录，目录名用这一页现有的 slug，如 `delete-entities`。
2. 在目录中写 `page.yaml`。整篇复用的 Delete Entities：

   ```yaml
   schema_version: 1                       # 配置格式版本，固定写 1

   source:
     # 这一页引用的 Milvus 原文，路径相对于 milvus-docs 仓库根目录
     file: site/en/userGuide/insert-and-delete/delete-entities.md

   publish:
     # 发布到哪些手册；每个手册各生成一份
     - manual: guides                      # Guides（SaaS），标题自动加 “| Cloud”
       path: tutorials/development/insert-and-delete/delete-entities
     - manual: guides-byoc                 # BYOC，标题自动加 “| BYOC”
       path: tutorials/development/insert-and-delete/delete-entities

   # metadata:                             # 都可以不写
   #   title:       不写就用 Milvus 原文的 title
   #   description: 不写就用 Milvus 原文的 summary
   #   beta:        标题下的标签，不写就是 FALSE
   ```

3. 提交 PR 后，工具在同一个 PR 中写入 `lock.yaml`：`current` 与 `next` 都取跟踪分支的最新提交，再运行校验。
4. 校验通过、审核后合并。合并后网站不变，激活后才上线（[场景 9](#场景-9从飞书切换到-git激活)）。

这一页对应的功能还没上线时，zdoc 中不用做任何标记：整页只在 UAT 显示，沿用飞书表格的 `Release Channel`（[场景 6](#场景-6让内容先只在-uat-显示)）。

**`page.yaml` 的字段**

| 字段 | 必填 | 写什么 |
|---|---|---|
| `schema_version` | 是 | 固定为 `1` |
| `source.file` | 是 | 共享原文的路径，相对于 milvus-docs 仓库根目录 |
| `publish[].manual` | 是 | zdoc 现有的手册，如 `guides`、`guides-byoc`；每个手册各生成一份 |
| `publish[].path` | 是 | 页面在该手册中的路径，决定输出位置。Phase 1 必须与飞书节点生成的路径一致 |
| `metadata.title` | 否 | 默认取原文的 `title` |
| `metadata.description` | 否 | 默认取原文的 `summary`；两边不同时在这里改写 |
| `metadata.beta` | 否 | 页面标题旁的标签，见下表；只影响 Guides。BYOC 的页面不显示这个标签，统一在右侧显示 Contact Sales 按钮 |
| `transforms` | 否 | Cloud 的差异，见[场景 4](#场景-4写-cloud-的差异) |

| `beta` 的值 | 英文站显示 | 中文站显示 |
|---|---|---|
| `FALSE`（默认） | 不显示 | 不显示 |
| `PUBLIC` | Public Preview | 公测版 |
| `PRIVATE` | Private Preview | 内测版 |
| `ON REQUEST` | On Request | 申请开通 |
| `NEAR DEPRECATE` | Near Deprecation | Near Deprecation |
| `DEPRECATED` | Deprecated | Deprecated |
| `CONTACT SALES` | 不显示在标题旁，显示为单独的 Contact Sales 按钮 | 同英文站 |

上表是 zdoc 现有的标签。可选的值以 zdoc 的标签定义为准，zdoc 增加新的值后随之可用；其中的 `BYOC` 标的是手册，不作为 `beta` 的值。

`slug`、标题后缀、导航标签与排序等其余 front matter 由工具生成，作者不写；完整列表见[写法速查](./authoring-spec.md)。

**规则**

| 规则 | 例子 |
|---|---|
| 目录名等于这一页现有的 slug，只用小写字母、数字和连字符 | `/delete-entities` 对应目录 `delete-entities` |
| 不写 `lock.yaml` | 工具写入；要重新取最新提交，删掉 PR 中的 `lock.yaml` 即可 |
| 正文的标题和章节结构随原文，不在配置中重复 | — |
| Phase 1 只能接入飞书目录中已有节点的页面；全新的页面先在飞书表格和目录中建好记录与节点。导航位置、顺序、标签在飞书目录中调整。导航迁到 Git 后取消这条限制 | 要移动这一页，在飞书目录中操作，并同步修改 `publish[].path` |
| PR 要从 zdoc 仓库内的分支提交 | 来自 fork 的 PR，工具无权写入 `lock.yaml` |

**系统行为**

| 编号 | 要求 |
|---|---|
| 3-1 | 新页面没有 `lock.yaml` 时，工具取 milvus-docs 跟踪分支（目前是 `v3.0.x`）的最新提交写入，`current` 与 `next` 相同，并提交到同一个 PR |
| 3-2 | 功能还没上线的页面，`lock.yaml` 照常写入；整页只在 UAT 显示，由飞书表格的 `Release Channel` 决定（[场景 6](#场景-6让内容先只在-uat-显示)） |
| 3-3 | 每个修改 `shared-docs/` 的 PR 都完整生成一遍页面来校验，不通过不能合并 |
| 3-4 | 生成的页面中，多语言代码 Tabs 完整、可以切换，语言顺序与必选语言按 Tabs 规则；变量换成 Cloud 的值；链接、锚点与图片可用（[场景 5](#场景-5链接与图片)） |
| 3-5 | 标题、描述按手册加后缀，如 `\| Cloud`、`\| BYOC` |
| 3-6 | **接入不等于上线**：合并后网站上仍是飞书版，激活后才换成 Git 版（[场景 9](#场景-9从飞书切换到-git激活)） |
| 3-7 | 迁移后页面的 URL 不变 |

<details>
<summary>出错时</summary>

| 情况 | 在哪里发现 | 怎样改 |
|---|---|---|
| 目录名不符合规则；缺少必填字段；有不认识的字段或值；`beta` 不是上表的值 | PR 校验 | 改 `page.yaml` |
| `source.file` 在 milvus-docs 中不存在 | PR 校验 | 改路径 |
| `publish[].manual` 不是已有的手册；`path` 与飞书节点不一致 | PR 校验 | 改 `page.yaml`，或在飞书目录中调整 |
| PR 来自 fork | PR 中提示 | 改从 zdoc 仓库内的分支提交 |

</details>

**不做与已知局限**：front matter 中的 `keywords`、`hide_title`、`hide_table_of_contents` 不开放。接入后、激活前在哪里看到生成的页面，见[第 7 节](#7-待确认的问题)。

**验收**：T06、T12（预览部分）。

<details>
<summary>取舍</summary>

**为什么目录名等于现有 slug。** 不另起一套 ID；迁移后 URL 不变，搜索收录和站外链接不受影响。

**为什么按手册列出发布目标。** Delete Entities 和 Filtered Search 现在各发布 Guides 与 BYOC 两份，只差标题后缀；OpenAI 只发布到 Guides。后缀由工具按手册加，作者不手写。

**为什么作者只写三项元数据。** zdoc 现有 366 个英文 Guides 页面中，其余 front matter 几乎全是同一个值；只有 `beta` 确实因页而异（34 页）。Milvus 原文的 `beta`（如 `Milvus 2.6.x`）是 Milvus 自己的版本说明，不沿用。`beta` 的值会被检查，因为 zdoc 遇到不认识的值时既不显示标签、也不报错。

**为什么 `lock.yaml` 由工具写。** 作者不用查 commit，也不会抄错。

**为什么功能未上线不在 zdoc 中标记。** Phase 1 每一页都要在飞书表格中有一条记录来决定导航，这条记录的 `Release Channel` 已经控制整页在哪一边显示，Fetch 也按它处理导航和搜索。zdoc 中再标一次，就有两处来源要保持一致。导航迁到 Git 后，再由 `lock.yaml` 表达（[第 4 节](#4-一页的生命周期)）。

</details>


### 场景 4：写 Cloud 的差异

**阶段**：Phase 1b　**谁**：文档工程师

**技术设计**：[02 变换的执行](./design/02-page-config.md#变换的执行)、[07 代码 Tabs](./design/07-site-adaptation.md#代码-tabs)

**背景**：有的页面，Cloud 与 Milvus 不只差几个值。例如 OpenAI 页，Milvus 讲怎样在 `milvus.yaml` 中配置密钥，Cloud 讲在控制台创建集成；代码中 Milvus 用可选的 `credential`，Cloud 必须填 `integration_id`。这些差异写在 zdoc 中，原文不动，Milvus 作者也不需要照顾 Cloud 的写法。

**用户故事**：作为文档工程师，我在 zdoc 中声明 Cloud 要替换、删除或补充原文的哪一段，Cloud 页面体现这些差异，Milvus 页面完全不受影响。

**先消除漂移，再写差异。** 两边标题相同的部分随原文引用。先把可以合并的历史漂移在 milvus-docs 中改掉，再为必须保留的产品差异写变换；缺少某种语言、旧的 SDK 写法或错误的示例，不能当作长期差异保留。

**按差异的大小选写法**

| 差异 | 写法 | 例子 |
|---|---|---|
| 只差产品名、连接值 | 变量 | [场景 1](#场景-1把产品名和连接值写成变量) |
| 整节不同 | 替换整个命名块 | 例 1 |
| Cloud 要在某一节前后多一段 | 在命名块前或后增加 | 例 1 后的说明 |
| 某一节只属于 Milvus | 删除整个命名块 | 例 1 后的说明 |
| Cloud 独有一种语言的示例，如 Zilliz CLI | 给代码组增加一种语言 | 例 2 |
| 某种语言的示例整个不同 | 替换或删除这种语言 | 例 2 后的说明 |
| 代码只差一两行 | 替换、增加或删除这几行 | 例 3 |

**怎样操作**

1. 在 milvus-docs 中给要改的一段加命名块（[场景 2](#场景-2在-milvus-原文中标出-cloud-要改的一段)）。
2. 在这一页的 `page.yaml` 中加一条**变换**（`transforms` 列表中的一项），说明改哪里、怎么改、改成什么。
3. 需要新内容时，在同一目录中写 **Cloud 内容文件**。
4. 提交 PR，校验通过后合并。

**例 1：替换整个命名块**（OpenAI）

Milvus 原文的 “Configure credentials” 一节已经包成命名块 `before-you-start`。在 `page.yaml` 中写：

```yaml
transforms:                        # 这一页的全部变换，每一项是一条
  - operation: replace             # 怎么改：add（增加）、replace（替换）、remove（删除）
    target:
      block: before-you-start      # 改哪个命名块
    content:
      file: before-you-start.md    # 新内容所在的 Cloud 内容文件，与 page.yaml 同一目录
```

Cloud 内容文件 `shared-docs/pages/openai/before-you-start.md` 写完整的一节，包括标题，写法与 Milvus 原文相同：

```markdown
## Before you start

……Cloud 的内容：在控制台创建集成……

<div class="alert note">
……
</div>
```

生成后，Cloud 页面中这一节换成内容文件的内容；Milvus 页面不变。

- 在这一节前后增加一段：`operation` 写 `add`，再加一行 `position: before` 或 `position: after`。
- 删除这一节：`operation` 写 `remove`，只写 `target`，不写 `content`。

**例 2：给代码组增加一种语言**（Filtered Search）

```yaml
  - operation: add
    target:
      block: standard-filtering-code   # 一个代码组
      language: shell                  # 只改这种语言；原来没有这种语言
    content:
      file: standard-filtering-cli.md  # 文件中只有一个 shell 代码块
```

`standard-filtering-cli.md` 中只写一个代码块，不加语言切换栏：

````markdown
```shell
zilliz ……
```
````

生成后，这个代码组的标签页多出 “Zilliz CLI”，位置由 Tabs 规则决定，所以不写 `position`。

- 替换或删除一种语言：`operation` 换成 `replace` 或 `remove`；删除时不写 `content`。
- `language` 写代码块开头三个反引号后的语言名，不一定等于标签页上显示的名字：NodeJS 写 `javascript`，cURL 写 `bash`，Zilliz CLI 写 `shell`。

**例 3：改代码中的几行**（OpenAI 的 Java 示例）

```yaml
  - operation: add
    target:
      block: define-function-code
      language: java
      lines: |                         # 定位：从原文整行复制的一行或连续几行，最多 5 行
        .param("model_name", "text-embedding-3-small")
    position: after                    # 加在定位行之后；before 为之前
    content:
      lines: |                         # 新的代码行，直接写在配置中，不用写缩进
        .param("integration_id", "YOUR_INTEGRATION_ID")
```

生成后，新的一行自动对齐定位行的缩进：

```java
    .param("provider", "openai")
    .param("model_name", "text-embedding-3-small")
    .param("integration_id", "YOUR_INTEGRATION_ID")    // 新增
    .build();
```

- 删除几行：`operation` 写 `remove`，只写 `lines`，不写 `content` 与 `position`。
- 替换几行：`operation` 写 `replace`，不写 `position`，见下面的例子。

<details>
<summary>替换几行的例子（OpenAI 的 Python 示例）</summary>

```yaml
  - operation: replace
    target:
      block: define-function-code
      language: python
      lines: |                           # 从原文整行复制，行尾的注释也要带上
        # Optional parameters:
        # "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
    content:
      lines: |
        "integration_id": "YOUR_INTEGRATION_ID",
        # Optional parameters:
```

两行一起替换，`integration_id` 放在前面，原来的 “Optional parameters” 注释保留在后面，避免必填参数出现在“可选参数”下面。

</details>

**字段与组合**

<details>
<summary>一条变换的全部字段</summary>

| 字段 | 写什么 |
|---|---|
| `operation` | 怎么改：`add`（增加）、`replace`（替换）、`remove`（删除） |
| `target.block` | 改哪个命名块 |
| `target.language` | 只改代码组中的这种语言；值是代码块开头三个反引号后的语言名 |
| `target.lines` | 只改这种语言中连续的几行；从原文复制，最多 5 行 |
| `position` | 加在前面还是后面：`before` 或 `after`，只在下面的对照表注明的两种 `add` 中写 |
| `content.file` | 新内容所在的 Cloud 内容文件 |
| `content.lines` | 新的几行代码，直接写在配置中 |
| `channel` | 只对 Prod 或只对 UAT 生效，见[场景 6](#场景-6让内容先只在-uat-显示) |

</details>

目标分三级，每级都能做三种操作：

| 目标 | `add` | `replace` | `remove` | 新内容写在哪 |
|---|---|---|---|---|
| 整个命名块（`block`） | 在块前或块后插入，必须写 `position` | 换掉整块 | 删掉整块 | `content.file`；替换代码组时写完整的代码组，多语言时含切换栏 |
| 代码组中的一种语言（`block` + `language`） | 加一种原来没有的语言；不写 `position`，顺序由 Tabs 规则决定 | 换掉这种语言的代码 | 删掉这种语言 | `content.file`；只写一个该语言的代码块，不加切换栏 |
| 一种语言中连续的几行（`block` + `language` + `lines`） | 在这几行前或后插入，必须写 `position` | 换掉这几行 | 删掉这几行 | `content.lines`，不用写缩进 |

**代码行的规则**

| 规则 | 例子 |
|---|---|
| `lines` 是原文中连续的一行或几行，最多 5 行，在这种语言的代码中恰好出现一次 | 出现两次的 `)` 不能单独作定位 |
| 匹配时忽略每行行首的缩进和行尾的空格，其余必须一字不差，包括行尾的注释 | 少复制了行尾的 `# Optional: …` 注释就找不到 |
| `lines` 与 `content.lines` 中都不能有空行、三个反引号或命名块标记 | — |
| 写入时自动补上缩进：新内容整体对齐到被替换或被定位的第一行，各行之间的相对缩进保留，原文用空格就是空格、用 Tab 就是 Tab | 定位行缩进 8 个空格，新内容的第二行比第一行多缩进 4 格，写入后就是 12 个空格 |
| 选与新内容同一层级的行作定位 | 想在 `params={` 里面加参数，用它里面的 `"provider": "openai",` 定位，不用 `params={` |
| 一段代码中有多处不同，或连续超过 5 行，改为替换整种语言 | — |
| 定位行尽量选上游不常改的行 | 上游改了定位行，上游更新 PR 会被拦下（[场景 7](#场景-7审核上游更新)） |

**Cloud 内容文件**

Cloud 内容文件放 `add` 与 `replace` 的新内容，与 `page.yaml` 在同一目录。**写法与 Milvus 原文相同**：提示框写成 `<div class="alert note">`，多语言代码组写成切换栏加代码块。工具把它和原文一起转换成 Cloud 的组件，作者只需要会一种写法。

| 可以用 | 不可以用 |
|---|---|
| 变量 `{{var.xxx}}`、片段 `{{fragments/xxx.md}}`，取 Cloud 的值 | 命名块标记：命名块只用来定位 Milvus 原文 |
| zdoc 现有的产品过滤写法，区分 SaaS 与 BYOC | 手写的 `<Tabs>`、`<Admonition>` 等 Cloud 组件：由工具生成 |
| `<NextChannel>`，让一段只在 UAT 显示（[场景 6](#场景-6让内容先只在-uat-显示)） | |
| 页面目录下的图片文件，或外部图片地址 | |

替换一节时，内容文件要提供完整的内容，包括这一节的标题。

**其他规则**

| 规则 | 例子 |
|---|---|
| 变换对 `publish` 中的所有手册都生效；SaaS 与 BYOC 之间的差异用产品过滤写法 | OpenAI 只发布到 Guides，不受影响 |
| `remove` 不写内容，也不用空文件表达删除 | — |
| 给代码组加语言时，这种语言原来必须没有；替换或删除语言时必须已有 | — |
| 不再需要 Cloud 自己加的语言，直接删掉那条 `add`，不要再加一条 `remove` | — |
| 删除代码组不会删掉它外面的标题或说明，命名块要覆盖完整的语义范围 | 删掉一个示例后，检查是否留下“下面的代码……”这类悬空的说明 |
| 同一位置有多条 `add` 时，按列表顺序输出 | — |
| 同一个目标在同一个通道中只能有一条变换，不同级别的变换不能重叠 | 整块替换后，不能再改这一块中的某种语言 |

**系统行为**

| 编号 | 要求 |
|---|---|
| 4-1 | 先校验全部变换，再生成页面；任何一条不成立，这一页生成失败，不跳过 |
| 4-2 | 命名块的类型和语言按原文结构判断；Markdown 块上只能做整块操作 |
| 4-3 | 代码行的缩进按上述规则自动处理，生成结果中不留多余空行 |
| 4-4 | 代码 Tabs 按 Tabs 规则重新生成，语言顺序、显示名和默认语言全站统一。多语言代码组必须有 Python；其他语言原文或变换中有就显示，没有就不显示，不加占位 |
| 4-5 | Cloud 内容文件与原文经过同样的处理：变量、片段、产品过滤、组件转换 |
| 4-6 | Milvus 站点的输出与原文一致，不受 zdoc 中任何变换影响 |

<details>
<summary>出错时</summary>

以下情况，PR 校验失败，这一页不能合并：

| 情况 | 怎样改 |
|---|---|
| 目标命名块、语言或内容文件不存在；内容文件在页面目录之外 | 改 `page.yaml`，或回 milvus-docs 加命名块 |
| `position` 该写没写，或不该写写了；`remove` 带了内容 | 改 `page.yaml` |
| 同一目标被多次变换，或不同级别的变换重叠 | 合并成一条，或改用更大一级的目标 |
| `lines` 找不到、出现多次、超过 5 行，或用在没有 `language` 的目标上；`lines` 或 `content.lines` 中有空行 | 重新从原文复制，或改为替换整种语言 |
| 内容文件中有命名块标记或手写的 Tabs | 去掉 |
| 删除了 Tabs 规则要求必须有的语言或默认语言 | 改为替换这种语言 |

</details>

**不做与已知局限**

- 行号、正则、全文搜索、标题选择器等定位方式。
- 代码中的区域标记；超过 5 行或跨多处的代码行修改。
- 在共享原文中写产品指令或条件。
- 移动、复制、嵌套的变换，以及对刚插入的内容再做变换。
- 变量表达式、循环、条件模板，或把整段代码放进变量。
- 一页拼接多篇原文的多个命名块。
- 工具不判断不同语言的示例是否等价。
- 原文中没有的语言不会出现在 Cloud 页面上。现有 Cloud 页面中的 Rust 示例，在 Phase 1 内容对齐时从飞书同步到 milvus-docs。

**验收**：T04、T13（过滤部分）。

<details>
<summary>例子：OpenAI 的完整 page.yaml</summary>

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
      lines: |
        # Optional parameters:
        # "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml
    content:
      lines: |
        "integration_id": "YOUR_INTEGRATION_ID",
        # Optional parameters:
```

</details>

<details>
<summary>取舍</summary>

**为什么只有三种操作。** 增加、替换、删除足以表达试点页中的全部差异；按业务类型增加专门的操作，规则会越来越多，作者也要学更多写法。

**为什么代码行的差异写在 zdoc。** 另两种做法都会把 Cloud 的负担带给 Milvus：在原文中写产品行指令，Milvus 作者改代码时要同时照顾 Cloud 的行，Milvus 发布链还要新增一套过滤；在代码中加区域标记，标记要按每种语言写成注释，还要在代码内部清除。

**为什么 Cloud 内容文件用 Milvus 的写法。** 工具对内容文件和原文做同一套转换，作者不用学第二种写法。

</details>


### 场景 5：链接与图片

**阶段**：Phase 1a　**谁**：工具自动处理，文档工程师按提示补充

**技术设计**：[02b 链接与图片](./design/02b-links-and-images.md)、[05 图片上传](./design/05-publish-handoff.md#图片上传)

**背景**：Milvus 原文中的链接和图片是按 milvus.io 写的。原样放进 Cloud 页面，站内链接会指向 Cloud 不存在的页面，锚点会因为大小写规则不同而失效，图片可能在没人审核的情况下被换掉。

**用户故事**：作为文档工程师，我不用逐个检查原文中的链接和图片：工具自动换成 Cloud 可用的地址，只在找不到对应页面时告诉我补一行配置。

**怎样操作**

- **链接**：多数不用管。全站共用的链接映射表 `shared-docs/links.yaml` 登记 Milvus 页面在 Cloud 中对应哪一页：

  ```yaml
  boolean.md: filtering-overview                    # Cloud 中对应的页面
  ivf-flat.md: https://milvus.io/docs/ivf-flat.md   # Cloud 没有对应页时，明确指向 Milvus 站点
  ```

  1. **初始内容由工具一次生成，人审一遍。** Phase 1 开始时，工具为 User Guide 中所有被链接的 Milvus 页面找 Cloud 对应页：同名页面、标题相同的页面、Cloud 现有页面中同一处链接指向的页面。找到的写成候选，Cloud 没有对应页的索引类型、自部署与配置页写成指向 milvus.io 的候选，其余列出待人判断。文档工程师审核、补全后，用一个 PR 提交。
  2. **之后只补新出现的页面。** 工具报错“找不到 Cloud 对应页面”时，报错中附上候选（标题相同或相近的 Cloud 页面），文档工程师确认后补一行。

- **图片**：不用写任何配置。在 milvus-docs 中换图时，用新的文件名，不要覆盖已上传的图片（见下文）。

链接和图片的错误都在 PR 校验中发现：校验只生成共享页，不需要等一两个小时的整站构建。

**链接怎样处理**

只处理 Cloud 最终页面中留下的链接；被替换或删除的部分不处理。

| 链接类型 | 例子 | 处理 |
|---|---|---|
| 指向标题的锚点 | `#Delete-Entities-by-Primary-Keys` | 换成 Cloud 的锚点写法，见下文 |
| 外部网站 | `https://platform.openai.com/...` | 原样保留 |
| milvus.io 的完整地址 | `https://milvus.io/docs/release_notes.md` | 原样保留：作者写完整地址，就是有意指向 Milvus 站点 |
| Milvus 站内页面 | `boolean.md`、`boolean.md#xxx` | 换成 Cloud 页面地址，按下表查找 |
| 以 `/` 开头的站内路径 | `/api-reference/...` | 这一页生成失败：在 Cloud 站点上一定指错 |
| 不属于以上任何一类 | `filtering`（漏写 `.md`） | 这一页生成失败 |

Milvus 站内页面按顺序查找，查到即停：

| 顺序 | 查什么 | 怎样判断 | 例子 |
|---|---|---|---|
| 1 | 目标页也是共享页 | 某个共享页的 `page.yaml` 中，`source.file` 就是这个 Milvus 页面 | 目标 `delete-entities.md` 已接入，链接换成 Cloud 的 `delete-entities`（示意） |
| 2 | 链接映射表中有这一页 | `links.yaml` 中登记了这个 Milvus 文件名 | `boolean.md` 换成 `filtering-overview` |
| 3 | Cloud 有同名页面 | 去掉 `.md` 后，Cloud 上有同样 slug 的页面 | `primary-key-search.md` 换成 Cloud 的 `primary-key-search` |
| 4 | 都没有 | — | OpenAI 页中的 `embedding-function-overview.md`：这一页生成失败，提示在映射表中补一行，并附上候选 |

- **名字不同的共享页不用登记**：工具用它的目录名，也就是 Cloud 现有的 slug；两边名字的对应关系已经记在它的 `page.yaml` 中。例如 `boolean.md` 以后迁成共享页，目录名仍是 `filtering-overview`，链接照样换成 `filtering-overview`，`links.yaml` 中原来那一行可以删掉。
- **人工登记排在同名查找之前**：登记的结果比自动猜测可靠；同名页面在 Cloud 上讲的其实是别的内容时，登记一行就能纠正。
- **链接映射表是一张补丁表**，只补自动查找查不到的部分：

  | 登记的这一行 | 以后 |
  |---|---|
  | 目标页以后也迁成共享页 | 第 1 步就能查到，这一行不再起作用，可以删 |
  | 目标页 Cloud 不迁移，只是两边名字不同 | 一直需要 |
  | Cloud 上没有对应页，只能指向 milvus.io | 一直需要 |

  迁移的页面越多，这张表越短。

**锚点**：共享页中带锚点的链接，页面部分按上表换算，锚点部分再换成 Cloud 的写法。两边的锚点都由标题文字生成，但规则不同；浏览器按大小写匹配锚点，原样照搬会失效：

| 站点 | 规则 | `Phase 1: Ingestion & key classification` 的锚点 |
|---|---|---|
| milvus.io | 保留大小写，空格换成 `-`，去掉其余符号 | `Phase-1-Ingestion--key-classification` |
| Cloud | 全部小写，空格换成 `-`，`&`、`<`、`\|` 等换成单词，去掉其余符号；与 zdoc 现有页面相同 | `phase-1-ingestion-and-key-classification` |

工具在链接指向的那篇 Milvus 原文（同一版本）中找到锚点对应的标题，再按 Cloud 的规则从标题文字算出锚点；找不到对应的标题时，这一页生成失败。Prod 与 UAT 分别计算。

- 目标是共享页时，算出的锚点一定存在。
- 目标是仍由飞书维护的页面（经链接映射表或同名页面找到）时，飞书版的标题可能与 Milvus 原文不同；锚点是否存在，由 zdoc 现有的链接检查发现。
- 共享页自己的标题也按 Cloud 的规则生成锚点，所以迁移后，与飞书版相同的标题，锚点也不变。

Cloud 独有页面自己内部的链接不经过这套处理。

**图片怎样处理**

Milvus 原文中的图片有两种来源，都能确定某个版本用的是哪一张：

| 来源 | 例子 | 怎样确定版本 |
|---|---|---|
| Milvus 的图片存储 | `https://milvus-docs.s3.us-west-2.amazonaws.com/assets/filtered-search.png` | 已上传的图片不覆盖，换图用新文件名，所以同一个地址始终是同一张图 |
| milvus-docs 仓库内的文件 | `../../../assets/xxx.png` | 按 `lock.yaml` 记录的 commit 读取 |

Cloud 页面用到的每一张图片，都转存到 zdoc 现有的图片存储，页面中的地址改为新地址。新地址由图片内容决定：内容相同，地址就相同；内容一变，地址就变。

| 情况 | 结果 |
|---|---|
| 同一张图出现在 Prod 与 UAT 两个版本中，或出现在多个页面中 | 只存一份，都引用同一个地址 |
| Milvus 换了这张图 | 新图另存一份：Prod 显示旧图，UAT 显示新图，互不影响 |
| 提升后 Prod 改用新图 | 旧图仍留在存储中，恢复旧版本时还在 |
| Milvus 存储中的图片被同名覆盖（违反上面的规则） | 已采用的版本仍显示转存时的图片；工具发现后通知文档工程师 |

图片还可以来自其他外部地址，或 Cloud 内容文件所在的目录。

**系统行为**

| 编号 | 要求 |
|---|---|
| 5-1 | 链接按上述规则处理，处理不了的一律报错，不原样放过 |
| 5-2 | 映射表全站一份，每个 Milvus 页面只登记一次，所有共享页共用 |
| 5-7 | 生成时不按标题或相似度自动猜测对应页；它们只用来生成初始映射表的候选，以及查不到时报错中附带的候选，采用前都经人确认 |
| 5-3 | 已存的图片不会被覆盖或自动清理，只要还有已发布或可以恢复的页面引用它 |
| 5-4 | Milvus 换图会让图片地址变化，出现在上游更新 PR 中，审核后才进入 Cloud |
| 5-5 | 校验时只算出地址、不上传；合并后的正式发布才上传还没有的图片 |
| 5-6 | 已采用的版本中，每张图片以第一次转存的内容为准，重新生成或恢复时不因原地址的内容变化而改变 |

<details>
<summary>出错时</summary>

| 情况 | 在哪里发现 | 怎样改 |
|---|---|---|
| Milvus 站内页面找不到对应地址 | PR 校验 | 在映射表中补一行 |
| 以 `/` 开头的站内路径 | PR 校验 | 在映射表中处理，或回 milvus-docs 改成完整地址 |
| 链接不属于任何一类 | PR 校验 | 回 milvus-docs 修正 |
| 链接指向的共享页在这个版本中不存在；锚点找不到对应标题 | PR 校验 | 回 milvus-docs 修正，或调整采用的版本 |
| 图片下载失败或不存在 | PR 校验 | 回源头修正 |

</details>

**不做与已知局限**

- milvus-docs 中已有失效的锚点：User Guide 中带锚点的站内链接有 233 个，其中 49 个在 milvus.io 上就找不到对应的标题，多为从飞书导入时留下的块 ID、已改名的标题或大小写写错。接入这些页面时会报错，在内容对齐时回 milvus-docs 修正。
- PR 预览中，新出现的图片暂时显示不出来，合并后才上传。上游更新 PR 的报告会列出新增或变化的图片及其原地址，供审核人查看。
- Cloud 页面可以链接到 Milvus 站点，但只能在映射表中明确写出；工具不会自动把查不到的链接指向 milvus.io。

**验收**：T06、T10。

<details>
<summary>例子：三个试点页</summary>

| 页面 | 链接 | 图片 |
|---|---|---|
| Delete Entities | `boolean.md`：查找第 2 步，映射表中为 `filtering-overview` | 无 |
| Filtered Search | `primary-key-search.md`：第 3 步，同名页；`filtering`（漏写 `.md`）：报错，在内容对齐时回上游修正 | 两张 Milvus 存储中的图片，转存后地址改变 |
| OpenAI | `configure-docker.md`：在被替换的一节中，不处理；`embedding-function-overview.md`：Cloud 没有同名页，需要在映射表中补一行；两个 OpenAI 官网链接：原样保留 | 无 |

</details>

<details>
<summary>取舍</summary>

**为什么需要映射表。** milvus-docs 中 User Guide 与 Embeddings 的 837 个站内链接，只有 32% 的目标在 Cloud 有同名页面。两边的页面名字因历史原因不同，而且都已公开，改名要两站都做跳转，Phase 1 不做。

**为什么全站一份。** 同一个目标页会被很多共享页引用，登记一次即可。随着更多页面成为共享页，查找第 1 步覆盖得越来越多，映射表会越来越短。

**为什么初始映射表由工具生成。** 只靠同名页面，User Guide 中 181 个被链接的页面要人登记 121 个。加上标题相同与 Cloud 现有页面中的链接，工具能给出 116 个的候选，三种来源两两比较没有一个不一致；剩下 65 个中，43 个是 Cloud 没有对应页的索引类型、自部署与配置页，可以按类别批量写成指向 milvus.io。人要做的变成审一遍候选、判断二十多个。从 Cloud 现有页面反推只能在飞书退出之前做，所以放在 Phase 1 开始时一次做完。数据见[链接映射表的维护方式调研](../research/link-mapping-maintenance.md)。

**为什么生成时不按标题自动匹配。** 任一边改了标题，映射就可能悄悄变成另一页；写进映射表，改动都经过 PR。

**为什么查不到仍然失败，不自动指向 milvus.io。** 查不到的链接中，有的在 Cloud 上有名字不同的对应页，例如 `limitations.md` 对应 `limits`；自动指向 milvus.io，读者会被悄悄带到 Milvus 站点。之后每月新出现的链接目标约 4 个，报错附有候选，补一行的成本不高。

**为什么换算锚点。** milvus-docs 中跨页带锚点的链接有 284 个，其中 274 个含大写字母，原样照搬会失效。docs.zilliz.com 上实测：`filtered-search#Iterative-filtering` 停在页面顶部，`#iterative-filtering` 才跳到对应的一节。

**为什么从标题文字算，不直接转小写。** 直接转小写，在 User Guide 中能找到标题的 184 个锚点链接里只有 1 个对不上；但标题中有 `&`、`<`、`|`、表情符号等时，两边的规则不同，全站 4457 个标题中有 136 个。工具本来就要读目标页的标题来确认锚点存在，从标题文字算不多花工夫，结果也与 zdoc 现有页面的锚点一致。

**为什么转存图片。** 直接引用 Milvus 的地址，Milvus 换图会绕过上游更新 PR 的审核，Prod 也会跟着变；转存后，Cloud 页面的图片沿用 zdoc 现有的存储与分发。按内容命名，是因为 zdoc 现有的图片上传在内容变化时会写到同一个地址，旧页面不能保证显示旧图。

**为什么不用找回 Milvus 的旧图。** milvus-docs 中没有上传图片的代码，存储中的图片由维护者手动上传：可访问的 269 张都是 2025 年 12 月一次性上传的，此后没有被覆盖；存储也没有开启版本保留，一旦覆盖就找不回旧图。之后新加的图片放在仓库的 `assets/` 中，按 commit 就能取到。所以只要守住“换图用新文件名”这一条，工具在第一次采用时转存即可，不需要回头找旧图。

</details>


### 场景 6：让内容先只在 UAT 显示

**阶段**：Phase 1b　**谁**：文档工程师；原文的版本差异由工具处理

**技术设计**：[04 两版合并](./design/04-channels-and-lock.md#两个版本怎样合并成一页)、[02 两遍生成](./design/02-page-config.md#两遍生成与-channel)

**背景**：Cloud 的功能往往晚于 Milvus 上线。Milvus 文档已经写了新参数，Cloud 下个月才支持；在此之前，Prod 要继续显示旧的内容，UAT 则要能提前审阅新内容。

**用户故事**：作为文档工程师，我可以先让还没上线的内容只在 UAT 显示，功能上线时再让 Prod 跟上，不用担心未上线的内容提前出现在 Prod。

**前提：只有 Milvus 原文分两个版本**

| 内容 | 有没有两个版本 | 合并后 |
|---|---|---|
| Milvus 原文 | 有：`lock.yaml` 中，`current` 给 Prod，`next` 给 UAT | 上游更新只改 `next`，Prod 要等提升 |
| `page.yaml`、Cloud 内容文件、`Variables.json` | 没有，只有一份 | Prod 与 UAT 同时用上 |

提升只把 `lock.yaml` 中的 `current` 改成 `next`，管不到页面配置。所以 Cloud 自己写的内容和规则，合并后会在 Prod 下一次部署时一起出现；还不能在 Prod 显示的，要用下表的写法。PR 校验只生成候选结果，不发布到任何站点。

**四种情况，四种做法**

| 想先只在 UAT 显示的内容 | 怎样做 |
|---|---|
| Milvus 原文在两个版本之间的变化 | 不用做。工具按 `lock.yaml` 为 Prod 与 UAT 各生成一版 |
| Cloud 新写的一段 | 在 Cloud 内容文件中用 `<NextChannel action="include">` 包住，沿用 zdoc 现有写法；功能上线时去掉包裹 |
| 用 Cloud 内容替换或删除原文的某一段，但下次发布时才生效 | 给这条变换加 `channel: next` |
| 整个新页面 | 在飞书表格中把这一页的 `Release Channel` 设为 `NEXT`（新记录的默认值），与其他页面相同；功能上线时改为 `CURRENT`（[场景 8](#场景-8功能上线时提升)） |

**原文的版本差异怎样体现**

Prod 与 UAT 由同一次构建产生，所以一页中同时放着两个版本：相同的部分只出现一次，不同的部分成对出现，`exclude` 中的只在 Prod 显示，`include` 中的只在 UAT 显示。这些标记由工具生成：

```mdx
## Delete entities by filter        ← 两版相同，不加标记

<NextChannel action="exclude">
旧的 Introduction                   ← 只在 Prod 显示
</NextChannel>
<NextChannel action="include">
新的 Introduction                   ← 只在 UAT 显示

介绍参数 X 的新段落
</NextChannel>
```

| 时间点 | Prod 用的版本 | UAT 用的版本 | 页面上 |
|---|---|---|---|
| 起始 | a1 | a1 | 两者相同，没有 `<NextChannel>` |
| 合并上游更新 PR（b2：改写 Introduction，新增参数 X） | a1 | b2 | Prod 显示旧的 Introduction；UAT 显示新的 Introduction 和 X |
| 再合并一个上游更新 PR（c3：修正一处错字） | a1 | c3 | Prod 不变；UAT 也带上这处修正 |
| 功能上线，提升 | c3 | c3 | 两者又相同，成对的标记消失 |

**只对一个通道生效的变换**

如本场景开头所说，页面配置合并后两边立刻都生效。默认每条变换在两个版本上都执行，也都必须成立。`channel` 让一条变换只在一边执行：

| 写法 | 影响 |
|---|---|
| 不写 | Prod 与 UAT |
| `channel: current` | 只影响 Prod |
| `channel: next` | 只影响 UAT |

两种情况需要它：

| 情况 | 不写 `channel` 会怎样 | 写法 |
|---|---|---|
| Milvus 改了 Cloud 正在修改的那一行，上游更新 PR 让 UAT 改用新原文 | 旧原文中有这一行，新原文中没有：同一条变换在 UAT 的版本上找不到目标，上游更新 PR 无法合并 | 原来那条加 `channel: current`；按新原文另写一条，加 `channel: next` |
| 原文现在对 Cloud 也成立，Cloud 下次发布后才不同。示意：原文写每个 collection 最多 4 个向量字段，Cloud 下次发布提到 10 | 替换规则一合并，Prod 就提前换成了还没上线的说法 | 替换规则加 `channel: next`：UAT 先显示新说法，Prod 照常显示原文 |

<details>
<summary>第一种情况的写法</summary>

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

</details>

<details>
<summary>第二种情况按时间走一遍</summary>

`lock.yaml` 一直是 Prod 与 UAT 都用 a1，原文写“最多 4 个”：

| 时间点 | `page.yaml` | Prod | UAT |
|---|---|---|---|
| 一开始 | 没有关于 Limits 的规则 | 4 个 | 4 个 |
| 合并替换规则，不加 `channel` | 多了“Limits 换成 10 个” | 10 个，功能还没上线 ❌ | 10 个 |
| 合并替换规则，加 `channel: next` | 同上，但只对 UAT 生效 | 4 个 ✅ | 10 个 ✅ |
| 功能上线，提升 | 工具去掉 `channel` 标记 | 10 个 | 10 个 |

两边结果不同，完全来自这条规则只对 UAT 生效；原文一字未变。在飞书中，这种情况用 `<NextChannel action="exclude">` 包住旧说法、`action="include"` 包住新说法；共享页的旧说法在两边共用的 Milvus 原文中，Cloud 不能在原文里加标签，所以改用 `channel: next`。

</details>

**规则**

| 规则 | 说明 |
|---|---|
| Milvus 原文中不写任何通道标记，也不为通道加命名块 | 原文的版本差异由工具处理 |
| `<NextChannel>` 只写在 Cloud 内容文件中，只用于 Cloud 新写的内容 | 要替换或删除原文、并且只在一边生效，用 `channel` |
| `channel` 是过渡期的临时标记，提升时由工具清理 | 作者不用回头删（[场景 8](#场景-8功能上线时提升)） |
| 页面在某一边不存在时，不能写只对那一边生效的变换 | 飞书表格中为 `NEXT` 的新页面 Prod 上没有，不能写 `channel: current` |

**系统行为**

| 编号 | 要求 |
|---|---|
| 6-1 | 两个版本相同时，生成的页面与只有一个版本时逐字相同 |
| 6-2 | 不同的部分按段落、整个列表、表格、提示框、整个代码组为单位成对输出，不在句子中间切分 |
| 6-3 | Cloud 的规则在两个版本上分别校验；失败时指出是哪个版本 |
| 6-4 | 未上线的内容不出现在 Prod，也不出现在搜索、`llms.txt` 等产物中 |
| 6-5 | 整页只在 UAT 存在、或只在 Prod 存在时，沿用 zdoc 现有的整页通道，即飞书表格的 `Release Channel`，导航与搜索随之处理 |
| 6-6 | front matter 不能按通道区分；两个版本不同时用 Prod 的版本，并在记录中注明 |
| 6-7 | `<NextChannel>` 包住列表、提示框和代码 Tabs 时都能正确显示；整页通道在各语言译文中同样生效 |

<details>
<summary>出错时</summary>

| 情况 | 在哪里发现 | 怎样改 |
|---|---|---|
| Cloud 的规则只在 UAT 的版本上失效 | 上游更新 PR 的校验，指出是 UAT 的版本 | 按上面第一种情况加一对 `channel` 规则；报告会给出建议 |
| `channel` 不是 `current` 或 `next`；页面在该通道中不存在 | PR 校验 | 改 `page.yaml` |
| Cloud 内容文件中手写的 `<NextChannel>` 落在工具生成的成对区域内 | PR 校验 | 改用 `channel` |

</details>

**验收**：T13。

<details>
<summary>取舍</summary>

**为什么两个版本放进同一页。** zdoc 的 Prod 与 UAT 用同一次构建，部署时才区分，不能各读一份文件。只给改动的段落打标记也做不到：原文中已经只剩新文，Prod 无法保留旧文。

**为什么允许规则只对一个通道生效。** 否则上游修改了 Cloud 定位的那一行后，同一条规则总有一个版本失败，上游更新 PR 无法合并；它也能表达“下次发布时才用 Cloud 内容替换某一节”。

**为什么整页上线、下线沿用飞书表格。** 理由见[场景 3 的取舍](#场景-3接入一页)：表格已经控制整页的通道，zdoc 中再表达一次会出现两处来源。

</details>


### 场景 7：审核上游更新

**阶段**：Phase 1b　**谁**：工具发起，文档工程师审核

**技术设计**：[06 上游更新](./design/06-upstream-changes.md)、[08 工作流](./design/08-workflows-and-permissions.md)

**背景**：milvus-docs 每天都可能有新的修改。Cloud 要能及时知道，又不能一合并就跟着变：有的修改 Cloud 也适用，有的写法只适合 Milvus，有的涉及 Cloud 还没上线的功能。

完整的链路是：社区或文档工程师在 milvus-docs 合并修改后，工具每天发现新提交，开出上游更新 PR；文档工程师审核合并后，新内容先在 UAT 显示，功能上线提升后才进入 Prod。

**用户故事**：作为文档工程师，我不用盯着 milvus-docs：上游有修改时，我会收到一个 PR，告诉我哪些页面变了、变了什么、哪些地方需要复核；我决定采用、暂缓还是先修改。

**怎样操作**

1. 收到工具开出的上游更新 PR，例如标题 `shared-docs: update openai to milvus-docs b2c3d4e`。
2. 读 PR 中的影响报告和生成结果的差异。
3. 按下表决定。

| 这次上游修改 | 怎样处理 |
|---|---|
| 适用于 Cloud，包括还没上线的功能 | 合并。UAT 先显示，功能上线时再提升（[场景 8](#场景-8功能上线时提升)） |
| Cloud 也需要，只是写法只适合 Milvus，例如新增一句 “In Milvus, you can …” | 回 milvus-docs 把 “Milvus” 改成变量；修正合并后，这个 PR 会自动带上 |
| 只属于 Milvus，例如新增一段 `milvus.yaml` 配置说明 | 回 milvus-docs 把这段标成命名块，在这个 PR 中加一条 `remove`，一起合并 |
| 暂时判断不了 | 先不合并。之后的上游修改会继续累积到这个 PR 中，所以要尽快决定 |
| 校验失败 | 按报告的建议，在同一个 PR 中修改页面配置或 Cloud 内容文件，校验通过后合并 |

**PR 中有什么**

| 部分 | 内容 |
|---|---|
| 改动 | 工具只改对应页面 `lock.yaml` 中的 `next`；校验失败时，文档工程师可以在同一个 PR 中修改页面配置或 Cloud 内容文件 |
| 上游范围 | milvus-docs 从旧版本到新版本的对比链接 |
| 影响报告 | 每页一节，见下表 |
| 校验 | 必须通过才能合并 |

| 影响报告的内容 | 说明 |
|---|---|
| UAT 将看到的变化 | 新旧两个版本的生成结果差异，折叠显示；代码组的变化附整个代码组，Markdown 块的变化附前后文 |
| 需要复核 | 被 Cloud 替换掉的原文有变化；标题改名与受影响的链接；新增或变化的图片，附原地址 |
| 失败 | 哪条规则、哪个版本失败，应改哪个文件，怎样改 |
| 一起采用的原因 | 合并了多页时，说明它们之间的依赖 |
| 翻译 | Cloud 页面是否变化，即合并后是否会触发重新翻译 |

**不同的上游变化在 PR 中的表现**

| 上游变化 | 在 PR 中的表现 |
|---|---|
| 普通的正文修改 | 报告列出 UAT 将看到的变化 |
| 被 Cloud 替换掉的那段原文变了 | 即使 Cloud 页面不变，也提示复核：Cloud 的替换内容是否要跟着改 |
| 标题改名 | 报告列出改名与受影响的链接；链接在提升时处理 |
| 新增命名块 | 报告列出，不改变 Cloud 页面 |
| 命名块移动位置，或块内标题改了，ID 不变 | 仍是同一个块，规则照常生效；报告列出变化 |
| 命名块的类型或语言变了，例如少了一种语言 | 按新原文重新检查 Cloud 的规则，不再成立时校验失败 |
| 只新增了命名块标记，正文没变 | Cloud 页面不变，不触发重新翻译 |
| 命名块被改名或删除；Cloud 定位的代码行被改了；原文被改名或删除 | 校验失败，见“出错时” |

**系统行为**

| 编号 | 要求 |
|---|---|
| 7-1 | 每天检查一次 milvus-docs 跟踪分支，一天内的多个提交一并处理；也可以手动触发，并指定页面与提交 |
| 7-2 | 上游修改只开 PR，不自动采用；PR 合并前，生成结果不进入正式发布 |
| 7-3 | 合并后新版本先在 UAT 显示，Prod 要等提升 |
| 7-4 | 每页一个 PR：这一页已有未合并的上游更新 PR 时，更新它，不另开 |
| 7-5 | 同一批提交中互相依赖的几页（例如一页改了标题，另一页的链接指向它）合进同一个 PR |
| 7-6 | 一页暂缓不影响其他页面 |
| 7-7 | 内容没有变化的页面不开 PR；同样的输入得到同样的结果 |
| 7-8 | 这一页提升后，还开着的上游更新 PR 在下一次运行时按新的版本重建 |
| 7-9 | 飞书表格中为 `RETIRE-IN-NEXT` 或已删除记录的页面不再检查；还开着的上游更新 PR 被关闭并写明原因 |
| 7-10 | 社区在 milvus-docs 中的 PR 不运行 zdoc 的任何代码，也拿不到 Cloud 的凭据 |

<details>
<summary>出错时</summary>

| 情况 | 结果 | 怎样改 |
|---|---|---|
| 命名块被改名或删除；Cloud 定位的代码行被改了；Cloud 的规则只在 UAT 的版本上失效 | PR 照样开，校验标为失败，报告写明原因与建议；修好之前网站继续用旧版本 | 在同一个 PR 中修改：通常是把原规则标为 `channel: current`，再按新原文加一条 `channel: next`（[场景 6](#场景-6让内容先只在-uat-显示)）；命名块改名时改规则中的 ID |
| 原文被改名 | 同上 | 在同一个 PR 中改 `source.file` |
| 原文被删除 | 同上 | 考虑下线这一页（[场景 10](#场景-10下线一页)） |
| 检查本身出错，例如网络问题 | 下一次定时运行自动重试；失败沿用 zdoc 现有的飞书通知 | — |
| milvus-docs 的分支历史被改写，记录的版本不在分支上 | 失败并通知 | 人工处理 |

</details>

**不做与已知局限**

- 工具只能发现内容“变了”，不能判断改动后意思是否还一样，所以宁可多提示，由审核人判断。
- 原文改名或删除没有专门的写法，人工处理。

**验收**：T05、T12。

<details>
<summary>例子：OpenAI 的上游更新 PR</summary>

milvus-docs 在 `b2c3d4e` 中给 OpenAI 页 “Choose an embedding model” 一节的模型表加了一行，并在被 Cloud 整节替换的 “Configure credentials” 中补充了一条要求。

- **标题**：`shared-docs: update openai to milvus-docs b2c3d4e`
- **改动**：`shared-docs/pages/openai/lock.yaml` 中 `next` 改为 `b2c3d4e…`
- **影响报告**：
  - UAT 将看到的变化：模型表新增一行。
  - 需要复核：`before-you-start` 替换的原文有变化，Cloud 页面没有变化；请确认 `before-you-start.md` 是否也要补充这条要求。
  - 翻译：Cloud 页面有变化，合并后会触发重新翻译。
- **校验**：通过。审核人确认 Cloud 内容文件不需要修改后合并。

</details>

<details>
<summary>取舍</summary>

**为什么每天检查，不是一有提交就触发。** milvus-docs 与 zdoc 属于不同的 GitHub 组织，即时触发要在 Milvus 的公开仓库中放一个能操作 zdoc 的凭据，管理与安全成本都高。上游修改本来就要等 Cloud 审核，晚几个小时发现没有影响。`v3.0.x` 近 30 天有 33 个提交，单日最多 9 个，按天处理比每个提交开一个 PR 合理。

**为什么每页一个滚动更新的 PR。** 不同页面的上游修改，Cloud 可能在不同时间采用，一页暂缓不应拖住其他页面；同一页的新提交累积到已有的 PR 中，审核人只需看一个 PR。

**为什么失败也开 PR。** 失败多半意味着 Cloud 的配置要跟着上游调整。把失败和修改建议放进 PR，文档工程师可以直接在同一个 PR 中修好，再走正常审核。

**为什么原文改名或删除不提供专门写法。** milvus-docs 调整导航时不必移动原文，原文本身改名或删除很少：`v3.0.x` 近一年改名 2 次、删除 9 次。

</details>


### 场景 8：功能上线时提升

**阶段**：Phase 1b　**谁**：文档工程师发起，工具开 PR

**技术设计**：[04 提升](./design/04-channels-and-lock.md#提升)、[08 工作流](./design/08-workflows-and-permissions.md)

**背景**：功能上线时，Prod 要采用 UAT 已在显示的版本。现在这一步是在飞书多维表格中逐页把 `Release Channel` 从 `NEXT` 改为 `CURRENT`。共享页的正文版本由 `lock.yaml` 决定，所以迁移后，提升改的是每页 `lock.yaml` 中 Prod 用的版本；整页从 `NEXT` 改为 `CURRENT` 仍在表格中操作（[场景 6](#场景-6让内容先只在-uat-显示)）。

**用户故事**：作为文档工程师，功能上线时我点一次按钮、选好要上线的页面，工具就开出一个 PR；合并后这些页面的 Prod 跟上 UAT，过渡期留下的临时写法也一并清理。

**怎样操作**

文档工程师**不手改** `lock.yaml`：

1. 在 zdoc 的 GitHub Actions 中运行“提升”工作流。
2. 填写这次上线的页面标识，或选“全部待提升”，即所有 Prod 与 UAT 版本不同的页面。
3. 工具开一个 PR，同一次上线的页面都在里面。
4. 审核 PR，确认页面清单正确；处理 PR 说明中列出的手写 `<NextChannel>` 和整页通道（见下文）。
5. 合并。之后 Prod 采用新版本。

大版本发布时选“全部待提升”即可：没有全站共用的一份版本记录，每页各一份，工具把它们放进同一个 PR，一次审核、一次合并。

**PR 中有什么**

- 每页 `lock.yaml` 中 Prod 用的版本（`current`）改成 UAT 的版本（`next`）。
- 清理只对一个通道生效的变换：删除 `channel: current` 的规则，去掉 `channel: next` 的标记。
- Git 页面中指向改名标题的旧锚点，改为新锚点。
- PR 说明列出飞书表格中 `Release Channel` 仍为 `NEXT` 的页面，提示“这些页面如果也在这次上线，请在同一次发布中把表格改为 `CURRENT`”。只改表格、不提升，Prod 显示的会是接入时的旧版本。
- PR 说明列出这些页面的 Cloud 内容文件中还剩的手写 `<NextChannel>`，提示“对应的功能也在这次上线时，请在本 PR 中一并去掉”。工具不自动去掉，因为它不知道每段属于哪个功能。

**标题改名的链接**

标题改名后锚点随之改变。提升之前，Prod 显示旧标题、UAT 显示新标题，同一个链接无法同时对准两个锚点，所以链接在提升时改：

| 链接在哪里 | 处理 |
|---|---|
| zdoc 中 Git 来源的页面，包括 Cloud 内容文件 | 提升 PR 中由工具自动改 |
| milvus-docs 中的其他页 | 上游更新 PR 的报告提示，由文档工程师判断是否回上游修改 |
| 仍在飞书的页面 | 报告列出，由文档工程师在飞书中修改；Phase 1 不拦截提升 |
| 站外链接 | Phase 1 不处理 |

过渡期内，指向旧锚点的链接在 UAT 上落到页面顶部。

**急需上线的修正**：Milvus 已修好的错误，要马上进入 Prod，不等下次发布：

| 这一页的情况 | 做法 |
|---|---|
| Prod 与 UAT 用同一个版本 | 手动触发上游更新，指定这一页和修正所在的提交；合并后单独提升这一页 |
| UAT 上有还不能上线的内容 | 加一条 `channel: current` 的变换，替换出错的那一段；下次提升时工具自动删除 |

出错的一段不在任何命名块中时，只能等下次发布，或提前提升整页（未上线的内容会一起进入 Prod），由文档工程师判断。

**系统行为**

| 编号 | 要求 |
|---|---|
| 8-1 | 一次提升只开一个 PR；只有对 zdoc 有写权限的人能运行这个工作流，审核仍走 PR |
| 8-2 | 合并后，Prod 显示的内容与提升前 UAT 显示的一致，页面中不再有工具生成的通道标记 |
| 8-3 | 合并后，在下一次发布运行时进入网站（时延见[第 7 节](#7-待确认的问题)） |
| 8-4 | 这些页面还开着的上游更新 PR，在下一次运行时按新的版本重建 |

<details>
<summary>出错时</summary>

| 情况 | 结果 |
|---|---|
| 填写的页面不存在 | 这一页不进入 PR，运行结果中列出 |
| 这一页 Prod 与 UAT 已是同一个版本 | 同上 |

</details>

**验收**：T13。

<details>
<summary>取舍</summary>

**为什么手动发起。** 上线是 Cloud 的发布决定，工具无从判断时机。zdoc 现有的“按需抓取 Guides”工作流也是手动运行、填写页面列表，这里照搬。

**为什么按页。** zdoc 现在的上线就是按页进行的，没有全站统一发布的动作。全站共用一份版本记录，会让不同时间上线的功能被迫一起进入 Prod。

**为什么锚点跟着标题变。** 这与 zdoc 现在修改飞书标题时的行为一致。milvus-docs 一年内有 17% 的候选页改过或删过标题，所以不能只给提示，要在提升时处理链接。

</details>


### 场景 9：从飞书切换到 Git（激活）

**阶段**：Phase 1b，只在 Phase 1 过渡期存在　**谁**：文档负责人

**技术设计**：[05b 切换与归属](./design/05b-cutover-and-ownership.md)、[05 交给发布](./design/05-publish-handoff.md)、[08 工作流](./design/08-workflows-and-permissions.md)

**背景**：Phase 1 飞书还不能退出。接入一页之后，网站上仍是飞书生成的版本；飞书上也可能还有人在改它。要有一个明确的时刻，把这一页交给 Git：从此网站上的这一页由 Git 生成，飞书不能再改它。这个时刻叫**激活**。

Phase 1 导航仍由飞书表格（DocsList）决定，表格中每条记录都有 placement type，说明这一行在导航中是什么，例如 `canonical` 表示一页由飞书文档生成的页面。激活就是在这一页的记录中，把 placement type 改为新增的 `git`，表示这一页由 Git 生成。

**用户故事**：作为文档负责人，我先看到 Git 版本与网站当前版本的差异，确认无误后再把这一页切换到 Git；切换要么完整完成，要么完全不发生。

![一页从飞书切换到 Git 的三步，都由文档负责人进行。比较：在 GitHub Actions 中运行，生成 Git 版与网站当前飞书版的差异，同时检查能否生成、链接与图片能否解析、表格记录与页面配置是否一致，不改网站。确认：由人判断飞书最近的修改已在 Git 中，或飞书已暂时冻结。激活：在飞书表格中把 placement type 改为 Git。下一次 Fetch 在同一个提交中写入正文、导航与 active.json，网站上换成 Git 版，飞书不能再改这一页，导航仍由飞书表格决定；Fetch 检查不通过时保留网站现有的版本并通知。比较或确认不通过时不激活，修正后重新比较。接入之后才能激活，一页只激活一次，不提供切回飞书。](./assets/page-activation.png)

图 2 · 一页从飞书切换到 Git（激活）

**怎样操作**

1. **比较**：在 zdoc 的 GitHub Actions 中运行“比较”，填写页面标识。工具生成两份页面的差异：一份是 Git 版本，一份是网站当前的飞书版本；同时做激活前的检查（9-1）。差异中单独列出锚点的变化，例如飞书版中手写的自定义锚点在 Git 版中没有了，指向它们的链接要跟着改。差异与检查结果显示在这次运行的结果中，比较不改网站。
2. **确认**：看过差异，确认飞书最近的修改已反映到 Git 中，或这一页在飞书中已暂时冻结；确认生成结果已审核。这一步由人判断，工具不检查。
3. **激活**：比较通过、确认无误后，在飞书表格中把这一页记录的 placement type 改为 `git`。这条记录的 `Docs`（飞书文档链接）不用再填；发布目标与路径仍要填，并与页面配置一致。下一次 Fetch 起，网站上这一页由 Git 生成。

- 全新的页面没有飞书版：在飞书表格中新建记录时，直接把 placement type 设为 `git`，不用比较。
- 已激活的页面，由 Fetch 写进 dev 中的一份清单 `active.json`，作为 Git 中的记录。它由 Fetch 按表格生成，人不手改。

**规则**

| 规则 | 说明 |
|---|---|
| 只由文档负责人修改 placement type | 修改记录留在飞书表格的历史和 `active.json` 的提交历史中 |
| 接入之后才能激活 | `shared-docs/pages/` 中没有这一页的目录时，表格标为 `git` 会让这一页生成失败 |
| 一页只激活一次 | 激活后不能改回其他值（9-3） |

**系统行为**

| 编号 | 要求 |
|---|---|
| 9-1 | 比较时，以及激活后的每次 Fetch，工具都检查：能生成；图片与链接都能解析；飞书表格记录的发布目标、路径与页面配置一致。比较时不通过，就不应激活；Fetch 中不通过，这一页保留网站上现有的版本并通知，不退回飞书重新生成 |
| 9-2 | 激活后的第一次 Fetch，在同一个提交中写入这一页的正文、导航与 `active.json`，不会出现只切换了一半的状态 |
| 9-3 | 已在 `active.json` 中的页面，表格中的 placement type 被改回其他值时，Fetch 失败并通知，页面保持 Git 版 |
| 9-4 | 激活后，飞书的任何任务（全量抓取、旧缓存、删除清单、恢复）都不能改写或删除这一页的页面与译文；未迁移的页面照常从飞书更新 |
| 9-5 | 同一个地址既有飞书页面又有 Git 页面时，生成失败 |
| 9-6 | 导航位置、顺序和标签 Phase 1 仍由飞书表格和目录决定；这一页的记录与节点保留，只用来决定导航，正文和其余元数据由 Git 生成 |
| 9-7 | 激活与提升互不依赖：激活决定这一页由飞书还是 Git 生成，一页只做一次；提升决定 Prod 用哪个 Git 版本，每次发版都做。功能未上线的新页面可以先激活、只在 UAT 显示 |
| 9-8 | 网站部署在激活之后进行；部署失败时重试或回滚，编辑来源仍是 Git，不交回飞书 |

<details>
<summary>出错时</summary>

| 情况 | 结果 |
|---|---|
| 比较时检查不通过 | 不应激活；修正后重新比较 |
| 激活后的 Fetch 检查不通过 | 这一页保留网站上现有的版本，通知文档负责人 |
| 表格标为 `git`，但 zdoc 中没有这一页的目录 | 这一页生成失败，网站保留现有的版本 |
| placement type 从 `git` 改回其他值 | Fetch 失败，页面保持 Git 版 |
| 同一个地址既有飞书页面又有 Git 页面 | 生成失败 |
| 飞书任务试图改写或删除已切换的页面 | 失败，页面保持不变 |

</details>

**不做与已知局限**

- 不提供切回飞书。激活后出了问题，用现有的恢复流程或镜像回滚处理。
- 调整迁移页在导航中的位置，仍在飞书目录中操作。

**一页完成迁移的标准**

- 从批准的 Git 输入生成并上线，旧任务不能改变结果。
- 资源可以重建，翻译输入有效，编辑入口明确。
- 附件、图片、同步块（飞书中多页共用的内容块）和必要的元数据也已迁出；仍依赖飞书同步块的页面不算完全迁出。

范围内的页面和依赖迁完后，再停用相应的飞书抓取与调度。

**验收**：T07。

<details>
<summary>例子：Delete Entities 的激活</summary>

1. 接入 PR 合并后，网站上仍是飞书版本。
2. 文档负责人对 `delete-entities` 运行比较，查看 Git 版本与飞书当前版本的差异，检查全部通过，确认飞书最近的修改已反映到 Git 中。
3. 文档负责人在飞书表格中把 Delete Entities 记录的 placement type 改为 `git`。下一次 Fetch 检查通过后，Guides 与 BYOC 两份页面同时改由 Git 生成，`active.json` 中加入 `delete-entities`；它在导航中的位置仍由飞书表格和目录决定。

</details>

<details>
<summary>取舍</summary>

**为什么激活前先比较。** 接入之后，飞书上可能又有人改过这一页；先比较一次，文档负责人才有东西可审。

**为什么在飞书表格中激活。** Phase 1 导航本来就由表格决定，文档负责人在同一处操作，与其他页面的维护方式一致；不用另建激活工作流和审批。

**为什么还要 `active.json`。** 它由 Fetch 按表格生成，人不改，所以不会和表格不一致；它让 Git 中有一份可以追溯的记录。dev 上的检查不调用飞书，就能拦住改写已激活页面的提交；Fetch 也能据此发现 placement type 被误改回去。飞书退出时，它可以直接改为正式来源。

**为什么激活与提升分开。** 两者回答不同的问题，节奏也不同：激活一页只做一次，由文档负责人把关；提升每次上线都做，由文档工程师发起。

**为什么 Phase 1 导航仍由飞书管理。** Guides 的导航从飞书目录树生成，Phase 1 只迁 3 页，其余 360 多页的导航仍在飞书。把 Git 页面插进飞书导航，要新增合并规则，作者调整导航时也要面对两套规则。

**为什么不提供切回飞书。** 切回要处理期间在 Git 中做的修改。Phase 1 只有 3 页，出了问题用恢复流程或镜像回滚就能处理。

</details>


### 场景 10：下线一页

**阶段**：Phase 1b，按需　**谁**：文档工程师

**技术设计**：[05b 下线完成](./design/05b-cutover-and-ownership.md#下线完成)、[04 删除页面目录](./design/04-channels-and-lock.md#删除页面目录)

**背景**：功能下线或页面合并时，一页要从网站上移除。和上线一样，它要先从 UAT 消失，到发布时再从 Prod 消失。Phase 1 这两步都沿用飞书表格现有的做法，与其他页面相同；Git 中只需在最后删除页面目录。

**用户故事**：作为文档工程师，我照现在的做法在飞书表格中下线一页：这一页先从 UAT 消失，到发布时再从 Prod 和导航中消失，中间不会出现“页面还在、导航里却没有”的情况。

**怎样操作**

1. 在飞书表格中把这一页的 `Release Channel` 改为 `RETIRE-IN-NEXT`：UAT 不再显示，Prod 照常。
2. 发版时，在飞书表格中删除这一页的记录，并删除飞书节点，沿用现有做法。之后的 Fetch 把这一页从网站上移除。
3. 之后开一个普通 PR，删除 `shared-docs/pages/<页面标识>/`。

| 时间 | 做什么 | UAT | Prod |
|---|---|---|---|
| 平时 | — | 有 | 有 |
| 决定下线 | 表格改为 `RETIRE-IN-NEXT` | 没有 | 有 |
| 发版 | 删除表格记录与飞书节点 | 没有 | 没有，导航中也没有 |
| 之后 | 普通 PR 删除页面目录 | 没有 | 没有 |

**规则**

| 规则 | 说明 |
|---|---|
| 先删表格记录，再删页面目录 | 目录先删，表格还标着 `git`，这一页生成失败（网站保留现有的版本）；记录先删，页面干净地移除，留下的目录只会被提示删除 |
| 还没激活的页面不走这个流程 | 网站上是飞书版本，照现在的做法在飞书中处理，再用普通 PR 删除页面目录 |

**系统行为**

| 编号 | 要求 |
|---|---|
| 10-1 | 表格中为 `RETIRE-IN-NEXT` 时，沿用 zdoc 现有的整页通道：UAT 不显示，Prod 照常，导航与搜索随之处理 |
| 10-2 | 表格记录删除后，下一次 Fetch 在同一次发布中移除这一页的所有内容（页面、译文、记录），并把它从 `active.json` 中去掉 |
| 10-3 | 表格中为 `RETIRE-IN-NEXT` 或已删除记录的页面，不再检查上游更新；还开着的上游更新 PR 被关闭并写明原因 |
| 10-4 | 表格记录已删除、页面目录还在时，PR 校验与 Fetch 提示删除目录，不生成这一页 |

<details>
<summary>出错时</summary>

| 情况 | 结果 |
|---|---|
| 页面目录已删除，表格记录还在、仍标为 `git` | 这一页生成失败，网站保留现有的版本并通知 |

</details>

**验收**：T07。

<details>
<summary>取舍</summary>

**为什么沿用飞书表格下线。** Phase 1 每一页都在表格中有记录，`RETIRE-IN-NEXT` 已经能让一页先从 UAT 消失、发版时再整体移除，导航与搜索也随之处理。共享页用同一套做法，文档工程师不用为它另学一个流程。

**为什么下线手动发起。** 与提升一样，下线是 Cloud 的发布决定。

</details>


## 6. 对现有能力的要求

改造不能让现有能力倒退：

| 能力 | 要求 | 验收 |
|---|---|---|
| 多语言代码 | Tabs 可以切换、语言完整，顺序与必选语言按统一规则 | T06 |
| 产品过滤 | Guides 与 BYOC 各自得到适用的正文与代码 | T13 |
| 产品名 | Cloud 页面中不出现没换成变量的 Milvus 产品名和连接值 | T14 |
| UAT 与 Prod | 未上线的内容不出现在 Prod，也不出现在搜索、`llms.txt` 等产物中 | T13 |
| 翻译 | 以最终的 Cloud 正文为输入，代码等技术内容受保护；Cloud 正文不变就不重译，即使被替换掉的原文变了；英文站（含日文）与中文站的边界不变 | T09 |
| 恢复 | 能回到历史版本，或从固定的输入重新生成同样的结果；缺少输入时停止，不回退到最新版本 | T10 |
| 发布保护 | 生成的页面不能手改，手改会被拒绝并指出应改的源文件；社区 PR 不需要、也拿不到 Cloud 凭据；预览不具备写生产的权限；内容 PR 不能关闭这些检查 | T12 |
| 及时生效 | 只改了 Cloud 的变量或内容文件，也会重新生成，不会因飞书侧“没有变化”而跳过 | T08 |
| 时延 | 合并后，在下一次定时的发布运行时生成，最多等约 8 小时；一次运行约 70 分钟；UAT 部署目前不是自动的（见[第 7 节](#7-待确认的问题)）。Phase 1 不在合并后自动触发发布，急用时由文档工程师手动运行一次 | — |
| Milvus 侧 | Milvus 站点的输出不变，不出现命名块标记 | T11 |
| 未迁移的页面 | 飞书页面的行为不变 | T13 |
| 出错 | 一律在 PR 校验或生成时失败，说明原因与应改的文件；不静默跳过，不静默使用 Milvus 的值 | — |

实现见[技术设计 05](./design/05-publish-handoff.md)、[08](./design/08-workflows-and-permissions.md)、[09](./design/09-error-catalog.md)。各项的验收标准见[Phase 1 实施计划第 4、5 节](./phase-1.md#4-1a整篇复用跑通)；T05、T07、T08、T11、T12 是上线阻断项。

## 7. 待确认的问题

状态统一在[Phase 1 实施计划第 6.1 节](./phase-1.md#61-待确认的接口)跟踪。工程侧的待核实事项（如 Fetch 的接入点）不在此列。

| 问题 | 当前假设 | 影响的场景 |
|---|---|---|
| 变换能否只对 Prod 或只对 UAT 生效 | 可以，提升时由工具清理 | 6、7、8 |
| 接入后、激活前，文档工程师在哪里看到生成的页面 | zdoc 现在没有 PR 预览站点：PR 校验只做构建检查，激活前的比较只给差异。由推动者在实现设计中给出方案 | 3、9 |
| UAT 部署是自动还是人工启动 | 目前不是自动的，文档负责人计划改为自动；GitHub Actions 连不到内网的 Jenkins，要另找接法 | 全部 |
| 共享页对各种代码语言的要求 | 推动者建议：只有 Python 必须有，其他语言原文有就显示、没有就不显示，包括 C++（见场景 4 的 4-4） | 4 |
| 迁移页的导航由谁管 | 已定：Phase 1 仍在飞书表格和目录中维护 | 3、9、10 |
