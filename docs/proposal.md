# Milvus × Zilliz Cloud 文档同源：流程与试点方案对齐

**第一次方案对齐会 · 已于 2026-10-13 讨论，结论见[第 7 节](#7-会议结论2026-10-13)**

> 本文是 2026-10-13 对齐会的材料，已冻结，正文不再随设计细化同步。之后的细化以[接口设计](./design/README.md)、[产品需求](./prd.md)和[首期实施计划](./phase-1.md)为准；再开会时，结论追加到第 7 节。

本文说明为什么改、方案怎样逐条满足改造要求，以及先从哪些页面试点。本次会议对齐方向与范围，会议结论与待调研事项见[第 7 节](#7-会议结论2026-10-13)；配置字段、接口签名等实现设计留到后续会议。

范围是 User Guide 等功能文档的共享与试点迁移。SDK Reference（原文仍在 web-content 维护）、全量迁移及飞书全面退役不属于首期。

## 1. 现状与改造要求

### 1.1 现状：两份正文都能改，靠人工同步

![现状维护关系：飞书正文与 milvus-docs 正文都可以独立编辑。文档工程师可以编辑飞书后导出到 Milvus（①），社区和文档工程师可以直接向 milvus-docs 提交 PR（②），Milvus 的修改需要文档工程师人工核对后抄回飞书（③，虚线）。](./assets/current-content-flow.png)

图 1 · 现状：共享内容的三条维护路径
- 三条路径中，只有 ③“把 Milvus 的修改抄回飞书”是虚线：它没有提醒，也没有固定检查，两边冲突时也没有约定以哪一侧为准。
- 社区修订尚未抄回飞书时，下次从飞书导出可能把旧说明带回 Milvus，覆盖社区的修改。现有流程允许这种情况发生，尚未核实是否出现过事故。
- 长期分开维护会造成漂移。例如 OpenAI embedding 页，两端的真实差异只有前提条件和凭证参数，但标题、示例语言和覆盖步骤也已经不同（见[第 4.1 节](#41-内容差异cloud-的改动写在-zdocmilvus-原文只加命名块)）。

### 1.2 改造需要满足的要求

要求分三组，共五条：

- **一处编辑**

  1. **milvus-docs 是唯一编辑源。** 共同内容只在这里修改；社区的修改提交到这里即可，不需要再人工抄回飞书。
- **Cloud 可控地复用**

  2. **Cloud 能表达差异。** 例如前提条件、凭证参数和 Cloud 独有的示例，而且不影响 Milvus 的内容。
  3. **自动得知，自己决定采用。** 上游有修改时 Cloud 能自动得知，并决定是否采用、何时采用，而不是 Milvus 一合并就跟着变。
  4. **未上线的功能不进 Prod。** Cloud 尚未上线的功能不出现在 Prod，但可以在 UAT 提前审阅。
- **现有能力不丢**

  5. **不经飞书，能力不丢。** 不再经过飞书中转，同时保留多语言代码、内容过滤、翻译、UAT / Prod 审核和恢复能力。

这些要求在方案中的对应见[第 2 节](#2-方案总览共享正文只改一处cloud-差异在-zdoc-维护)的对应表。

## 2. 方案总览：共享正文只改一处，Cloud 差异在 zdoc 维护

共享正文在 milvus-docs 维护一份，以 Git 为准；Cloud 的差异在 zdoc 中维护，飞书按页退出文档生产链。

下图是改造后的全貌，可与图 1 对照：两份正文合并为一份，靠人工抄回飞书的路径 ③ 不再需要。

![目标协作方式：社区贡献者和文档工程师向 milvus-docs 提交共享内容，Milvus 沿用既有发布；文档工程师在 zdoc 维护 Cloud 差异与配置。上游变化后，工具在 zdoc 自动发起上游更新 PR，附生成结果与影响提示；Cloud 审核后合并，新版本先在 UAT 可见，Cloud 发布时进入 Prod；暂不合并则保持已批准版本；需要修改时回到对应源文件。](./assets/collaboration-overview.png)

图 2 · 目标协作方式
- **谁改哪里。** Cloud 文档工程师不再在飞书编辑迁移后的页面，改为在 Git 中提交 PR：共同内容改 milvus-docs，Cloud 差异和配置改 zdoc。同一位文档工程师可以两边都改；审核在 GitHub PR 中进行，结果在 PR 预览和 UAT 中查看。
- **上游更新 PR 是 Cloud 的关口。** 上游修改不会直接进入 Cloud，要经 zdoc 中的上游更新 PR 审核后才采用（[第 4.2 节](#42-是否采用上游修改经更新-pr-审核)）。
- **生成文件不能手改。** CI 按固定输入重新生成并比对；发现问题时，回到图中对应的源文件修改。

第 1.2 节的各项要求在方案中的对应如下，后文按这张表的顺序展开。

| 要求（[第 1.2 节](#12-改造需要满足的要求)） | 方案怎样满足 | 详见 |
|---|---|---|
| 1 milvus-docs 是唯一编辑源 | 共同内容只改 milvus-docs；Cloud 直接读取它的固定 commit，不再从飞书导出 | [第 3 节](#3-一处编辑cloud-直接读取-milvus-docs) |
| 2 Cloud 能表达差异 | 差异写在 zdoc 的页面配置和 Cloud 内容文件中，原文只加命名块 | [4.1](#41-内容差异cloud-的改动写在-zdocmilvus-原文只加命名块) |
| 3 自动得知，自己决定采用 | milvus-docs 合并后，工具自动发起上游更新 PR，Cloud 审核后合并 | [4.2](#42-是否采用上游修改经更新-pr-审核) |
| 4 未上线的功能不进 Prod | Prod 与 UAT 各固定一个 commit，差异自动包进 `<NextChannel>` | [4.3](#43-何时上线prod-与-uat-各固定一个-commit) |
| 5 不经飞书，能力不丢 | 校验、过滤、翻译、发布沿用 zdoc 现有流程；按页切换 | [第 5 节](#5-现有能力不丢沿用-zdoc-流程飞书按页退出) |

## 3. 一处编辑：Cloud 直接读取 milvus-docs

![目标工具链：Milvus 侧沿用 milvus-docs → md2md → web-content → milvus.io，md2md 新增两项能力：发布时清除命名块标记，以及供 zdoc 调用的预处理入口。zdoc 在 md2md 处理之前，按 commit 直接读取 milvus-docs 原文，结合页面配置（YAML）、Variables.json 和 Cloud 内容文件（Markdown）生成 Cloud 页面（MDX），生成时调用 md2md 的预处理，用 Cloud 的值展开变量与片段。生成结果在 zdoc 中经 PR 审核合并后，进入 zdoc 既有的校验、过滤、Current / Next、翻译与发布流程。过渡期未迁移的飞书页和后续迁入的 Cloud 独有页也进入同一流程。虚线框标出新增工作的范围。](./assets/target-publication-chains.png)

图 3 · 目标工具链（待实施）

图 3 按 ①–④ 的顺序读：

- **① Milvus 侧流程不变。** milvus-docs 存放原文；[md2md](https://github.com/zilliztech/md2md) 展开变量与片段，并转换为 Milvus 站点格式；结果存入 web-content，再由 milvus.io 构建发布。md2md 只新增两项能力：发布时清除命名块标记，以及一个供 zdoc 调用的预处理入口。
- **② Cloud 按 commit 读取 md2md 处理之前的原文。** web-content 里的变量已经按 Milvus 的值展开，命名块标记也已清除。Cloud 如果从那里读，就无法绑定自己的值，也找不到需要差异处理的位置。
- **③ zdoc 生成 Cloud 页面。** 这是首期新增的部分，即图中的虚线框。输入是共享原文、页面配置（YAML）、Variables.json，以及按需提供的 Cloud 内容文件（Markdown）；生成时调用 md2md 的预处理，用 Cloud 的值展开变量与片段，两端共用同一套展开规则；输出是 Cloud 页面的 MDX。
- **④ 在 zdoc 中经 PR 审核后发布。** 上游有变化时，由工具发起上游更新 PR（[第 4.2 节](#42-是否采用上游修改经更新-pr-审核)）；Cloud 自己的修改，由文档工程师提 PR。合并后进入 zdoc 既有的校验、过滤、翻译与发布流程（[第 5 节](#5-现有能力不丢沿用-zdoc-流程飞书按页退出)）。milvus-docs 的 PR 仍按 Milvus 既有流程审核，Cloud 不参与，而是在这一步把关；Milvus 贡献说明届时补充共享页的写法。

现有工具链的对照见[附录 A](#附录-a现有发布工具链)。

## 4. Cloud 可控地复用

Cloud 复用共享内容时要回答三个问题：哪里和 Milvus 不同（[4.1](#41-内容差异cloud-的改动写在-zdocmilvus-原文只加命名块)），上游的修改要不要采用（[4.2](#42-是否采用上游修改经更新-pr-审核)），采用之后什么时候进入 Prod（[4.3](#43-何时上线prod-与-uat-各固定一个-commit)）。

三个问题中，人和工具的分工如下：

- **文档工程师手写**：milvus-docs 中的共享原文和命名块；zdoc 中的页面配置（YAML）、Cloud 内容文件，以及 Variables.json 中 Cloud 的值。4.1 讲的都是这一部分。
- **zdoc 新增的共享接入自动完成**：发现 milvus-docs 的新提交，发起上游更新 PR；记录 Prod 与 UAT 各用 milvus-docs 的哪个 commit；生成 Cloud 页面，包括其中的 `<NextChannel>` 标记，即图 3 的 ③。
- **人做决定**：是否合并上游更新 PR，也就是 UAT 是否采用；Cloud 发布时让 Prod 跟上 UAT。

### 4.1 内容差异：Cloud 的改动写在 zdoc，Milvus 原文只加命名块

按 Cloud 与 Milvus 的差异多少，页面分三类：

![三类页面：无差异的页面整篇复用，如 Delete Entities，原文把产品值写成变量，zdoc 只需一份页面配置；有差异的页面在共享正文上叠加 Cloud 差异，如 OpenAI 与 Filtered Search，原文只加命名块，zdoc 维护页面配置与 Cloud 内容文件；Cloud 独有页在 zdoc 维护完整原文，首期不迁移。](./assets/page-types.png)

图 4 · 三类页面
- **无差异：整篇复用。** 例如 [Delete Entities](https://milvus.io/docs/delete-entities.md)。两端只有产品名、连接地址等值不同：Milvus 原文把它们写成变量，zdoc 写一份页面配置（YAML）引用整篇。首期 1a 先做这一类。
- **有差异：以共享为主，局部由 Cloud 修改。** 例如 [OpenAI](https://milvus.io/docs/openai.md) 和 [Filtered Search](https://milvus.io/docs/filtered-search.md)。Milvus 原文只在 Cloud 要改动的位置加命名块，Cloud 的改动写在 zdoc，写法见图 5。首期 1b 处理这一类。
- **Cloud 独有：不涉及共享。** 整页在 zdoc 中以 Markdown / MDX 维护，首期不迁移。

有差异的页面具体怎样写，以 OpenAI 页（[Milvus 原文](https://milvus.io/docs/openai.md) / [Cloud 页面](https://docs.zilliz.com/docs/openai)）为例：

![OpenAI 页的差异：①共享正文整篇复用，产品名写成变量；②“Before you start”一节两端不同，milvus-docs 为这一节加命名块，zdoc 用 Cloud 内容文件替换；③代码中的凭证参数，milvus-docs 的代码不改，只给代码组加命名块；zdoc 页面配置中的一条 replace 规则按原文中连续的两行定位，把可选的 credential 注释换成 Cloud 必填的 integration_id。Milvus 站点与原文相同，只去掉命名块标记。](./assets/page-anatomy.png)

图 5 · OpenAI 页的差异怎样表达
- **Milvus 原文只加中性的命名块。** Cloud 的内容和规则都在 zdoc，Milvus 作者不需要照顾 Cloud 的写法。原文也不写 `include-next-line` 这类产品指令，否则 Milvus 发布链也要跟着过滤。命名块是一对 HTML 注释，只用来定位：zdoc 生成 Cloud 页面时按页面配置处理它，Milvus 发布时 md2md 把它清掉。
- **按差异的粒度选写法。**
  - ① 只有产品名不同：写成变量，例如把 "Milvus" 写成 `{{var.product_name}}`，两端各自给值。
  - ② 整节不同：例如 Before you start，Milvus 讲配置 `milvus.yaml`，Cloud 讲在控制台创建集成。用一对 HTML 注释把这一节标成命名块，在页面配置中声明用 Cloud 内容文件（Markdown）替换它。
  - ③ 代码只差一两行：例如 Python 示例中，Milvus 用两行注释说明 `credential` 是可选参数，Cloud 则必须填 `integration_id`。命名块加在整个代码组上，代码本身不改；页面配置用 `lines` 匹配这两行，只改这两行。
  - Cloud 独有的示例，如 Filtered Search 的 CLI，也写成 Cloud 内容文件，加进对应的代码组。
- **匹配失败时直接报错。** 上游改了 `lines` 匹配的那几行，上游更新 PR 会被拦下（[第 4.2 节](#42-是否采用上游修改经更新-pr-审核)）；差异更大时，替换整个语言示例。

### 4.2 是否采用：上游修改经更新 PR 审核

上游的修改不会直接进入 Cloud，要经过 Cloud 审核上游更新 PR。

- **谁发起：** zdoc 新增的自动任务。它跟踪 milvus-docs 的新提交，只为改动涉及的已接入页面发起 PR。
- **PR 改什么：** 把 UAT 使用的 milvus-docs commit 更新为新提交。zdoc 记录的是具体的提交编号，由工具维护；上游合并新提交不会让它变。
- **审核看什么：** 新生成的 Cloud 页面和差异。有两种变化在差异中看不出来或容易漏，工具会单独提示：
  - 一是 Cloud 替换过的一节在上游有修改。例如上游在 Before you start 中补充了一条要求，Cloud 页面因为整节替换而没有变化，需要确认 Cloud 内容文件是否同步。
  - 二是正文中残留只属于 Milvus 的说法，例如没写成变量的 "In Milvus"。
- **出错时不放过：** 命名块被删除或改名，或 `lines` 匹配的代码行被改动时，PR 直接报错，Cloud 继续使用已批准的内容。

合不合并由 Cloud 决定：

| 这次上游修改 | 怎么处理 |
|---|---|
| 适用于 Cloud，包括还没上线的功能。例如新增参数 X，Cloud 下月支持 | 合并。UAT 先看到，何时进入 Prod 见[第 4.3 节](#43-何时上线prod-与-uat-各固定一个-commit) |
| 内容 Cloud 也需要，只是写法只适合 Milvus。例如新增一句 "In Milvus, you can …" | 在 milvus-docs 把 "Milvus" 改成变量。修正合并后，下一个上游更新 PR 自然带上，zdoc 不用改 |
| 内容只属于 Milvus。例如新增一段 `milvus.yaml` 配置说明 | 在 milvus-docs 用一对 HTML 注释把这段标成命名块，在 zdoc 页面配置中加一条 `remove`（[第 4.1 节](#41-内容差异cloud-的改动写在-zdocmilvus-原文只加命名块)）。这条规则加进包含命名块的新上游更新 PR，一起合并 |
| 暂时判断不了 | 先不合并，UAT 和 Prod 保持原样。但后来的 commit 包含这次修改，之后的上游修改也会一起等待，所以要尽快按上面几行做出决定 |

### 4.3 何时上线：Prod 与 UAT 各固定一个 commit

Prod 用上次 Cloud 发布时的 commit，UAT 用最新批准的 commit；两者不同的段落，由工具自动包进 `<NextChannel>`。这两个 commit 由工具记录在 zdoc 中，不写在页面配置里，文档工程师不用手填。

**为什么需要。** 例如 Milvus 发布小版本时，文档工程师改写了共享页 A 中 Introduction 的措辞，又新增一段介绍新参数 X，而 Cloud 下个月才支持 X。在此之前，Prod 应继续显示旧的 Introduction、不出现 X，UAT 则要能提前看到新内容。只给改动的段落打标记做不到：原文里已经只剩新文，包进 `<NextChannel>` 后，Prod 上这一段会直接消失；改动零碎时，逐处加标记也难以维护。

**怎样做。** 工具用两个 commit 各生成一遍页面，相同的段落只保留一份，不同的段落写成一对：

```mdx
<NextChannel action="exclude">

旧的 Introduction

</NextChannel>

<NextChannel action="include">

新的 Introduction

介绍 X 的新段落

</NextChannel>
```

`exclude` 中的内容只在 Prod 显示，`include` 中的内容只在 UAT 显示，这是 zdoc 现有的用法；这些标记由工具生成，不需要手写。

| 时间点 | Prod 用的 commit | UAT 用的 commit | 页面上 |
|---|---|---|---|
| 起始 | a1 | a1 | 两者相同，没有 `<NextChannel>` |
| 合并上游更新 PR（b2：改写 Introduction，新增 X） | a1 | b2 | Prod 显示旧的 Introduction；UAT 显示新的 Introduction 和 X |
| 再合并一个上游更新 PR（c3：修正一处错字） | a1 | c3 | Prod 不变；UAT 也带上这处修正 |
| Cloud 发布 | c3 | c3 | 两者又相同，成对的标记自动消失 |

**两种例外：**

- **急需上线的修正**：如果这一页在 UAT 上没有等待发布的内容，合并后可以立即让 Prod 也改用新的 commit；如果有，直接推进会把未上线的内容一起带进 Prod，这时在 zdoc 页面配置中加一条临时规则修正，用注释标明是临时的，发布后删除。
- **Cloud 自己写的内容**：仍按现在的做法，要等下次发布才上线的部分手写 `<NextChannel>`，发布时去掉。双 commit 只处理 Milvus 原文的变化。

这一做法的两个前提列在[第 7 节](#7-会议结论2026-10-13)第 5 项。

## 5. 现有能力不丢：沿用 zdoc 流程，飞书按页退出

- **沿用 zdoc 现有流程。** 生成的页面进入 zdoc 既有的校验、过滤、Current / Next、翻译、发布与恢复流程，只扩展 Git 输入。
- **飞书按页退出。** 过渡期两种来源并存：未迁移的页面继续从飞书进入，已迁移的页面从 Git 进入，同一页任一时刻只有一个来源。首期只迁移试点页，Cloud 独有页暂不变；终态是 Cloud 文档全部在 Git 中维护。

**切换前做好写作准备。** 为文档工程师准备 Markdown、配置写法和 PR 流程的说明，预览页提供跳转到源文件的编辑入口。

## 6. 试点与路线

![项目路线：首期分 1a 与 1b。1a 用 Delete Entities 跑通整篇复用，从固定源生成到 UAT 预览，建议年底前完成；1b 用 Filtered Search 与 OpenAI 验证差异与上游更新 PR，接入正式发布、翻译与恢复，并切换试点页。后续分批迁移共享页与 Cloud 独有页，依赖清零后飞书退出。](./assets/rollout-roadmap.png)

图 6 · 项目路线
- **1a 只走最短路径**：用不需要差异的 Delete Entities 验证真实工具链能生成完整页面，生成结果只进入预览，不写生产。
- **1b 才正式切换。** 一页切换意味着：从 Git 输入生成并上线，旧飞书任务不能再写入或删除这一页；切换前核对最新的飞书修订。部署失败按既有机制重试或回滚，编辑来源仍是 Git。
- **未迁移页面照常走飞书。** 范围内的页面和导航、媒体等依赖迁完后，再停用相应的飞书抓取与调度。

| 候选 | 验证什么 | 状态 |
|---|---|---|
| [Delete Entities](../examples/delete-entities/walkthrough.md) | 整篇复用：变量绑定连接值，生成多语言代码 Tabs | 本地样例已验证 |
| [Filtered Search](../examples/filtered-search/walkthrough.md) | 产品名变量；在共享代码组中加入 Cloud CLI | 本地样例已验证 |
| OpenAI（[Milvus](https://milvus.io/docs/openai.md) / [Cloud](https://docs.zilliz.com/docs/openai)） | 前提条件整节替换；凭证参数的代码行替换；先对齐历史漂移 | 候选，未制作样例 |

两篇样例的共享原文含有尚未合入 Milvus 的共同修订和语言补齐，内容与 SDK 适用性仍需审核。OpenAI 跑通后，Cohere、Voyage AI 等同类页面可以照搬。实施细节与验收见 [phase-1](./phase-1.md)。

## 7. 会议结论（2026-10-13）

第一次对齐会由推动者、文档负责人和工程顾问参加。整体方向通过；差异的定位方式和产品名的写法需要先调研，配置字段等工程细节由推动者定义后再约评审。

| # | 事项 | 结论 | 详见 |
|---|---|---|---|
| 1 | 共享原文来源 | 通过：读取 md2md 处理之前的 milvus-docs 原文 | [第 3 节](#3-一处编辑cloud-直接读取-milvus-docs) |
| 2 | 飞书退出方式与终态 | 通过：按页分批迁移，已迁移的页面只在仓库中修改；终态只维护 milvus-docs 与 zdoc 两个仓库，飞书下线。迁移开始后维护一份已迁移页面清单，供仍在飞书修改的同事避开；迁移时长在方案细化后评估 | [第 5 节](#5-现有能力不丢沿用-zdoc-流程飞书按页退出) |
| 3 | 差异表达原则 | Cloud 的改动写在 zdoc：通过。Milvus 原文中怎样定位要替换的内容（命名块，或按标题层级、代码语言等结构定位）待调研，希望 Milvus 原文中尽量不出现可见标记 | [4.1](#41-内容差异cloud-的改动写在-zdocmilvus-原文只加命名块) |
| 4 | 共享内容把关 | 通过：Cloud 不审核 milvus-docs PR，在上游更新 PR 中把关。产品名是否写成变量待调研：贡献说明只能提要求，不能保证社区遵守；但社区贡献不是文档的主要来源，找不到更好的办法时沿用变量 | [4.2](#42-是否采用上游修改经更新-pr-审核) |
| 5 | Current / Next | 通过：`<NextChannel>` 由工具生成，不再手工插入；`include` 只在 UAT 显示，`exclude` 只在 Prod 显示。两个 commit 指 milvus-docs 的 commit，zdoc 的 Prod 与 UAT 仍发布同一个 commit。急需上线的修正用 zdoc 中的临时规则。两个前提未单独讨论，暂按建议执行 | [4.3](#43-何时上线prod-与-uat-各固定一个-commit) |
| 6 | 试点候选 | 未提出异议，按建议执行 | [第 6 节](#6-试点与路线) |
| 7 | 首期范围与年底目标 | 首期按 1a、1b 推进，未提出异议；年底前完成 1a，并启动 1b | [第 6 节](#6-试点与路线) |
| 8 | 分工 | 未单独讨论；推动者定义工程细节后，与文档负责人、工程顾问再约评审 | — |

**会上补充的范围说明：**

- **Cloud 独有页面**（如集群、控制面）继续在 zdoc 中以 Markdown 单独维护，不经过共享流程。
- **SDK Reference** 不在本期范围。文档负责人计划采用类似做法：以 web-content 为源，在 zdoc 中用配置替换产品名、连接地址和示例参数，并由 agent 自动维护。
- **AI 维护。** 修改共享页时可以先在本地生成单页（秒级）再判断改哪里；YAML、JSON 这类配置便于大模型读写。

**后续事项：**

| 负责人 | 事项 |
|---|---|
| 推动者 | 调研差异的定位方式，形成调研报告和方案 |
| 推动者 | 调研产品名的处理方式，形成调研报告和方案 |
| 推动者 | 定义配置字段等工程细节，与文档负责人、工程顾问再约评审 |
| 推动者 | 迁移开始后：维护已迁移页面清单；工程顾问近期在飞书中的修改随迁移并入 milvus-docs |
| 工程顾问 | 开放生成 SDK 文档与示例代码的 skill 仓库权限，便于共建 |

配置字段的[草案](./authoring-spec.md)会随上述调研结果修订。

## 附录 A：现有发布工具链

<details>
<summary>展开查看现有工具链与各阶段对照</summary>

![现有工具链：Milvus 从 milvus-docs 经 md2md、web-content、milvus.io 发布；Cloud 从飞书经 zdoc Fetch、zdoc dev 分支、Docusaurus 站点与外部 Jenkins 发布。两侧各有翻译支路。](./assets/current-publication-chains.png)

图 A · 现有发布工具链。实线表示内容处理顺序，点线表示工作流触发
| 阶段 | Milvus | Cloud |
|---|---|---|
| 发布输入 | milvus-docs 的 `site/` 目录存放原始 Markdown | 飞书提供正文和媒体 |
| 正文处理 | [md2md](https://github.com/zilliztech/md2md) 展开变量、引用片段并转换 Milvus 格式 | [zdoc](https://github.com/zilliztech/zdoc) 的 Fetch 工作流抓取飞书正文和媒体，完成渲染、组装与校验 |
| 中间内容 | [web-content](https://github.com/milvus-io/web-content) 保存站点正文和导航数据 | 生成的正文、导航和译文保存到 zdoc 的 `dev` 分支 |
| 站点构建与发布 | [milvus.io](https://github.com/milvus-io/milvus.io) 构建并部署 | zdoc 的 `apps/docs`（Docusaurus）；外部 Jenkins 负责 UAT / Prod |
| 翻译 | 新文件、每周定时或手动触发，译文保存到 web-content | Fetch 写入 dev 后触发，译文写回 dev |

当前 Cloud Guides 链没有调用 md2md。仓库实现已按固定修订核对，Jenkins 的外部配置和线上运行版本未核验。

</details>
