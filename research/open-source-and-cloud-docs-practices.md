# 开源与商业云产品文档工程实践调研

调研日期：2026-10-10。对象：Milvus 与 Zilliz Cloud 的共享内容、产品与版本差异、社区贡献、翻译和发布流程。

本文依据官方文档和公开源码。下文的“观察”表示有公开证据的实践；“建议”表示结合你们场景作出的判断。公开仓库无法完整反映私有编辑系统和生产部署配置；本文没有审计 milvus-docs、web-content、milvus.io 或 zdoc 的内部实现，你们的现状以本次描述为准。

## 1. 调研结论

最值得借鉴的是：**共享内容有明确的权威源，产品差异用元数据与条件内容表达，社区修改回到这个源，翻译追踪源内容的变化，网站作为发布目标消费内容。**

这不要求把所有文档和网站迁到一个仓库。TiDB 展示了同仓库的产品复用；OpenShift 展示了单行与模块级条件内容；GitLab 展示了多源码仓库由独立网站工程聚合。它们提供的是几种可组合的模式，不能据此宣布整个行业只采用一种架构。来源见各案例。

对你们而言，最需要先解决的是共享内容在 Git 与飞书之间的权威关系。只替换站点生成器，或者只增加反向同步脚本，都不会自动解决两边同时编辑、产品适用范围和译文失效的问题。这是基于现有流程的判断。

## 2. 最贴近的公开案例

| 案例 | 已查证的实践 | 对你们的参考价值 |
|---|---|---|
| TiDB / TiDB Cloud | 同文档仓库、Cloud 独立目录与目录树，复用数据库文档，段落使用 `CustomContent` | 最接近数据库内核与托管云产品复用。见 [贡献指南](https://github.com/pingcap/docs/blob/master/CONTRIBUTING.md) 与 [Cloud TOC](https://github.com/pingcap/docs/blob/release-8.1/TOC-tidb-cloud.md) |
| OKD / OpenShift / 托管发行版 | AsciiDoc 条件文本、模块引用、按发行版配置目录、发布分支 | 覆盖行、块、页及版本的差异管理。见 [贡献指南](https://github.com/openshift/openshift-docs/blob/main/contributing_to_docs/contributing.adoc) |
| GitLab SaaS / Self-Managed / Dedicated | 同一文档体系注明适用 offerings，多产品源码仓库由专门站点工程聚合；英文源与自动译文分工 | 内容、产品适用性、站点工程和语言职责可以分开。见 [站点架构](https://docs.gitlab.com/development/documentation/site_architecture/) |
| Elastic Stack / Cloud / Serverless | 当前 Markdown 系统复用 snippets，并用适用性元数据和部署类型 tabs 表达差异 | 重点借鉴共享概念与差异步骤的拆分准则。见 [官方策略](https://www.elastic.co/docs/contribute-docs/how-to/deployment-types/strategies) |
| CockroachDB，历史实现 | Cloud 与自托管页面共同 include 模块，使用 Liquid 处理块和句内差异 | 提供实际的模块组装源码；旧仓库已归档，不能视作当前发布系统。见 [仓库状态](https://github.com/cockroachdb/docs) |
| Electron，作为翻译专项案例 | 文档 Markdown 与界面 JSON 接入 Crowdin，翻译落入 Docusaurus 的语言目录 | 证明 Git 文档与外部翻译工作台可配合使用。见 [实际配置](https://github.com/electron/website/blob/main/crowdin.yml) |

### 2.1 TiDB：共用数据库文档，Cloud 保留自己的产品入口

**观察。** TiDB 的贡献指南定义了 `CustomContent platform="tidb"` 与 `platform="tidb-cloud"`：标签内的内容分别适用于对应产品，未包裹内容由两者共享。Cloud TOC 同时指向 `/tidb-cloud/` 专属页面与 `/develop/`、`/sql-statements/` 等共用页面。也就是说，页面内容可以共享，用户入口与导航仍由产品自己组织。[条件内容规则](https://github.com/pingcap/docs/blob/master/CONTRIBUTING.md#guideline-for-contributing-to-tidb-cloud-documentation)、[实际 Cloud TOC](https://github.com/pingcap/docs/blob/release-8.1/TOC-tidb-cloud.md)

下面是按其机制写的示意，正文为虚构内容，不是 TiDB 产品行为：

```markdown
这段说明由两个产品共享。

<CustomContent platform="tidb">
这里放自托管产品的配置说明。
</CustomContent>

<CustomContent platform="tidb-cloud">
这里放云产品的操作入口说明。
</CustomContent>
```

**观察。** 版本使用 `release-<version>` 分支，跨版本修订可通过标签触发 bot 创建 cherry-pick PR；有版本差异时仍需要修改和审核目标 PR。贡献指南当前文字把 Cloud 内容放在 `release-8.1` 分支，而该分支的 Cloud TOC 确实存在。不过指南的“Cloud 仅英文”等描述与网站已有中文入口不能直接等同，故这里只确认公开复用机制，不把某个分支名视作 Cloud 当前完整部署契约。[版本贡献指南](https://github.com/pingcap/docs/blob/master/CONTRIBUTING.md#learn-about-docs-versions)、[中文文档入口](https://docs.pingcap.com/zh/)

**建议。** Milvus 和 Cloud 可以共享概念、API 行为、搜索原理和通用示例，同时分别组织导航。短差异适合条件块；如果部署前提、权限或操作步骤已经不同，宜各写产品页面，再引用共同说明。

### 2.2 OpenShift：产品条件与版本分支承担不同职责

**观察。** `openshift-docs` 的贡献指南明确支持用 AsciiDoc `ifdef/endif` 跨产品复用，粒度可到单行；整页是否出现由 topic map 决定。发行版属性涵盖 origin、enterprise、dedicated、ROSA 等。当前仓库把受支持版本的 topic maps 放在 `_topic_maps/`，因此不应照搬旧资料中只有根目录 `_topic_map.yml` 的布局。[贡献指南](https://github.com/openshift/openshift-docs/blob/main/contributing_to_docs/contributing.adoc)、[topic maps](https://github.com/openshift/openshift-docs/tree/main/_topic_maps)

**观察。** 开发内容在工作分支维护，发布版本采用 release branches，修订再应用到相关发布分支。产品条件决定“给哪类产品看”，版本分支决定“对应哪个发布状态”；不是给每个产品复制一套全部正文。[发布分支规则](https://github.com/openshift/openshift-docs/blob/main/contributing_to_docs/contributing.adoc#release-branches)

**观察。** Red Hat 的模块化写作规范把内容拆成概念、步骤、参考模块，再组装为 assembly；更小的 snippet 可复用段落、步骤、表格和提示。规范规定模块不再包含另一模块，但可以包含 snippet，以控制复用层级。[模块化规范](https://redhat-documentation.github.io/modular-docs/#creating-modules)、[snippet 规范](https://redhat-documentation.github.io/modular-docs/#using-text-snippets)

**建议。** 将“行级过滤”定义成一段有稳定语义的条件文本，而非依赖文件行号。对于 Markdown，优先考虑块或结构节点；对于 AsciiDoc，原生行条件已存在。两者都需要检查过滤后列表、表格、锚点与代码示例是否仍然完整。Asciidoctor 官方明确说明其条件处理发生在结构解析前，并不理解周围文档结构，这也是需要构建验证的原因。[条件处理语义](https://docs.asciidoctor.org/asciidoc/latest/directives/conditionals/)

### 2.3 GitLab：多仓库内容源，独立网站聚合

**观察。** GitLab 文档分别位于 GitLab、Runner、Omnibus、Charts 等产品仓库；独立 `docs-gitlab-com` 工程用 Hugo 生成网站。文档修改在各自源码仓库通过 MR 处理。官网与产品内帮助共用文档，产品内帮助只包含相应 edition 和 version。官方还明确英文为 canonical source，译文由半自主自动化流程更新，贡献者只修改英文源。[站点架构及翻译职责](https://docs.gitlab.com/development/documentation/site_architecture/)

**观察。** GitLab 在页首或章节标注 tier 和 offering。已核对的是适用性标注，不能把这种标注等同于构建时删除其他产品内容。实际 CI 执行 `make clone-docs-projects` 与 Hugo，输出 `public` artifact，再由独立发布 job 消费。[适用性规范](https://docs.gitlab.com/development/documentation/styleguide/availability_details/)、[构建 CI](https://gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/blob/main/.gitlab/ci/build.gitlab-ci.yml)、[发布 CI](https://gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/blob/main/.gitlab/ci/deploy.gitlab-ci.yml)

**建议。** 你们现有“内容仓库 → 中间构建 → 网站”的层次本身并不是问题。值得检查的是它是否能独立预览、选择明确内容版本、生成可追踪的产物，以及不同站点能否消费同一套共用内容。多仓库可以保留，重复权威源需要消除。

### 2.4 Elastic：当前 Markdown 实践，共享概念与部署差异分开

**观察。** Elastic 于 2025 年 4 月迁移到 Markdown 与 `docs-builder`，当前站点覆盖 Stack 9.x、Cloud Hosted、Serverless、ECE 与 ECK；8.x 及更早属于旧 AsciiDoc 系统。新系统采用 cumulative docs，不为每个 minor release 复制一套完整页面，而是在持续维护的页面内表达版本变化。[官方系统分界与版本模式](https://www.elastic.co/docs/contribute-docs/)

**观察。** 当前真实源文件中，安全概览引用 `_snippets`，secure-settings 页面通过 `applies-switch` 为 Cloud、ECK 和 Self-Managed 提供不同步骤。后者属于同页展示分支；`applies_to` 属于适用性元数据，都不能未经验证就说成“分别导出并物理删除另一产品内容”。[实际 snippet 引用](https://github.com/elastic/docs-content/blob/90f6e6299a916300389b3faa58f43eb229c7c78a/deploy-manage/security.md)、[实际差异步骤](https://github.com/elastic/docs-content/blob/90f6e6299a916300389b3faa58f43eb229c7c78a/deploy-manage/security/secure-settings.md)、[switch 的工具语义](https://elastic.github.io/docs-builder/syntax/applies-switch/)

**观察。** 官方写作策略区分共同概念、不同配置入口、轻微增强、显著改变操作模型、不同实现机制等场景：短差异使用限定章节或 tabs，复杂差异可以拆 sibling pages；某部署不可用的功能应在容易产生误解的位置说明。[跨部署内容策略](https://www.elastic.co/docs/contribute-docs/how-to/deployment-types/strategies)

**建议。** 这对你们的内容拆分比单纯选择语法更重要。搜索语义可以共用，Cloud 权限、控制台流程和自托管运维可以有各自页面。版本管理也有两种已观察到的模式：发布分支与 cumulative docs，需结合旧版本行为差异和维护范围选择，不能认定只有一条最佳路径。

### 2.5 CockroachDB：有具体源码的历史模块化案例

**观察。** 官方 `cockroachdb/docs` 仓库显示于 2026-10-06 归档。归档前的 Cloud 与自托管 v26.2 升级页面共同引用 `common/upgrade/overview.md`，再拼装产品专属步骤；共同模块使用 Liquid，根据页面上下文调整段落、表格与句内短语。这是可查证的历史实现。[归档状态](https://github.com/cockroachdb/docs)、[Cloud 升级页](https://github.com/cockroachdb/docs/blob/27e64c5d4481a3c888f8f1f61c540fcba37e0594/src/current/cockroachcloud/upgrade-cockroach-version.md)、[自托管升级页](https://github.com/cockroachdb/docs/blob/27e64c5d4481a3c888f8f1f61c540fcba37e0594/src/current/v26.2/upgrade-cockroach-version.md)、[共同模块](https://github.com/cockroachdb/docs/blob/27e64c5d4481a3c888f8f1f61c540fcba37e0594/src/current/_includes/common/upgrade/overview.md)

**建议。** 可以借鉴“共同模块 + 专属步骤”的组装方式，但不将旧 Jekyll/Liquid 仓库当作现行平台推荐。其条件依赖页面路径字符串；重新设计时可考虑显式产品元数据，降低路径调整影响内容行为的风险。

## 3. 社区贡献：回到权威源，比同步两份最终页面更重要

从已查证的 TiDB、OpenShift、GitLab 案例看，社区修改以文档源码 PR/MR 进入维护流程。这些资料没有提供一个可以直接复用的“公开 Markdown 与企业富文本 Wiki 自动无损双向同步”方案。这里说的是本次样本的证据边界，而非声称这种方案不存在。

针对你们的第二个问题，有三种方向。以下是架构判断，不是已落地的厂商案例。

| 方向 | 如何处理 Milvus 社区 PR | 长期取舍 |
|---|---|---|
| Git 为共享内容的权威源 | 社区直接修改共享源；Cloud 构建消费审核后的相应修订 | 与公开贡献流程契合。飞书可保留草稿、评审或受控写入入口，需要调整作者流程 |
| 飞书为共享内容的权威源 | 将 Git PR 的差异映射成飞书修改建议，确认后再生成对应 Git 内容 | 保留当前编辑体验，但需要维护格式映射、版本基线、冲突处理、归属与同步状态 |
| 两边均自由编辑与发布 | Git 和飞书修改彼此覆盖或自动合并 | 操作上方便，但长期需要承担完整的双向合并系统；本次不建议作为默认方向 |

“一个权威源”是**每个内容单元只有明确的最终版本归属**，不是所有内容都必须在同一个仓库。一个现实候选是：公开仓库维护共享内容和 Milvus 文档，Cloud 专属内容保留在自己的仓库或内容系统，并固定消费某个共享内容修订。这样社区贡献仍在公开源上完成。

如果共享源隐藏在私有系统、milvus-docs 只保留生成后的页面，外部贡献仍需回流。映射机制至少应保留源文档/块标识、生成时的源修订、上下文和 PR 归属；产品组装时被过滤掉的内容，不能仅凭输出页面反推。这是对系统需求的推导，尚未验证你们现有的飞书导出器是否已有这些能力。

## 4. 翻译自动化：两类组织方式与三种工具路线

### 4.1 已有实践

**TiDB：源 PR 与翻译 PR 建立关联。** 社区使用 `translation/doing`、`done`、`from-docs` 等标签追踪跨语言修改。公开仓库新增的翻译 skill 与配套脚本进一步支持把源 PR/commit range 拆成 change units，对已有中文文件做最小修改，并创建或更新翻译 PR。这证明了公开的增量工作流设计与实现存在，不证明每次源变更都自动触发或自动通过审核。[社区翻译流程](https://pingcap.github.io/tidb-dev-guide/contribute-to-tidb/write-document.html)、[增量翻译工作流](https://github.com/pingcap/docs/blob/master/.agents/skills/create-or-update-zh-translation-pr/SKILL.md)

**Electron：Git 源文档与翻译工作台分工。** 实际 `crowdin.yml` 把 `/docs/**/*` 映射到 `i18n/<locale>/docusaurus-plugin-content-docs/current/`，并单独处理界面 JSON、博客和不参与翻译的图片等路径。Docusaurus 官方也明确国际化系统与具体翻译服务解耦。[Electron 配置](https://github.com/electron/website/blob/main/crowdin.yml)、[Docusaurus 集成说明](https://docusaurus.io/docs/i18n/crowdin)

### 4.2 工具能力与边界

| 路线 | 官方能力 | 适用判断 |
|---|---|---|
| Markdown/MDX + Crowdin | GitHub 源文件同步，译文通过服务分支和 PR 返回；提供术语库与翻译记忆 | 可作为保持 Markdown 的候选；需实测自定义标签与块的往返保真。[GitHub 集成](https://support.crowdin.com/github-integration/)、[格式支持](https://support.crowdin.com/supported-formats/) |
| Weblate + Git | 持续拉取与推送，提供翻译工作台；Markdown 支持有格式特定限制 | 适合评估集中译文编辑。官方说明 Markdown 的外部译文修改无法可靠回导，因此译文权威在 Weblate；不能默认让 Git 与工作台各自随意改译文。[持续本地化](https://docs.weblate.org/en/latest/admin/continuous.html)、[Markdown 限制](https://docs.weblate.org/en/latest/formats/markdown.html) |
| Sphinx + gettext + 翻译平台 | 从文档结构抽取 POT，维护 PO/MO，将译文应用回文档；提供交叉引用检查 | 更适合愿意采用消息目录翻译模型的团队，不是必须更换到 Sphinx。[官方国际化流程](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html) |

上述属于工具能力。除已列明的 TiDB、GitLab、Electron，不据此推断某家厂商使用某个翻译服务。

### 4.3 适用于你们的候选流程

以下是建议流程：

```text
权威源修改并合并
  → 找出变更内容单元与受影响的产品/版本
  → 复用已审核译文和术语，生成新增/变化部分的翻译建议
  → 更新翻译 PR 或翻译工作台任务
  → 语言审核、结构校验、产品预览
  → 按各产品发布策略生成产物
```

优先保留源修订或源内容 hash、目标语言、适用产品/能力上下文和审核状态。相同共享模块可复用翻译；当正文、能力含义或术语发生变化时，需要重新判断旧译文是否仍有效。hash 和状态设计是建议，不能宣称所有案例都采用完全相同的数据模型。

翻译复用应尽量发生在共享模块或翻译单元层，而不是把两个完整网站分别导出、分别全文翻译。翻译模块后再组装，或先按产品解析后抽取翻译单元，两种顺序均可；试点时要验证条件标签保留、去重效果和译者上下文，不能预设一种顺序必然最好。

## 5. 内容模型与工程选型

| 选择 | 已核对能力 | 对你们的判断 |
|---|---|---|
| Markdown/MDX + 少量条件语法与 include | TiDB 的 `CustomContent` 是真实实例；具体解析器仍由项目实现 | 最适合作为贴近现有 Git 文档的试点候选。不要把选 Docusaurus 等同于已获得产品条件和社区回流能力 |
| AsciiDoc + Asciidoctor / Antora | 条件文本、引用；Antora 可采集多个仓库、分支、tag 与内容目录 | 产品复用与版本维度复杂时值得对照评估，转换既有格式有成本。[条件能力](https://docs.asciidoctor.org/asciidoc/latest/directives/conditionals/)、[Antora 多源采集](https://docs.antora.org/antora/latest/content-source-repositories/) |
| DITA / CCMS | DITA 提供基于属性的 applicability/profiling，用 DITAVAL 在处理时过滤 | 可满足结构化复用与企业作者工作台需求；公开社区 Markdown PR 的接入要另做设计。本次仅确认标准能力，没有验证具体商业 CCMS 部署。[OASIS 条件处理标准](https://docs.oasis-open.org/dita/v1.2/os/spec/archSpec/condproc.html) |

优先级建议是先明确内容归属与贡献流程，再决定格式和站点生成器。选择另一种渲染框架不会自动修复权威源冲突。

## 6. 对三个问题的直接映射

| 你们的问题 | 可借鉴的模式 | 需要验证的具体点 |
|---|---|---|
| 内核文档重合、产品与版本不同 | TiDB 条件块 + 产品 TOC；OpenShift 模块 + 产品条件 + 发布分支 | 两套产品的支持矩阵能否显式表达；过滤后页面是否完整；重用模块是否有稳定标识 |
| Git 社区修改需要反向同步飞书 | 社区修改直接进入权威共享源；保留飞书时把其定位成受控编辑入口或维护映射流程 | Git 与飞书同时编辑的规则；PR 应用到哪个源修订；保留作者归属；如何处理结构差异 |
| 翻译自动化 | GitLab 源语言与自动译文职责；TiDB 增量翻译 PR；Electron 翻译平台集成 | 原文变化如何令译文失效；术语与代码保护；跨产品翻译复用；审核和发布状态 |

对于产品适用性，建议分别描述 `product`、`capability`、开源发布版本、Cloud 的服务/套餐等相关维度。Cloud 的某项功能即使来自 Milvus 某版本，也可能尚未在某个服务形态开放；不能用一个 Milvus 版本号自动代表所有 Cloud 能力。这是根据你们已描述的差异作出的建模建议。

对于发布，候选目标是能够用“内容修订 + 产品配置 + 语言 + 构建工具版本”解释每个产物，独立产生受影响产品的预览，并允许两个网站按自己的节奏部署。是否需要替换 web-content 或 zdoc，必须经过现有实现审计才能判断。

## 7. 下一阶段建议验证的最小范围

不建议在调研阶段直接决定全量迁移。先选一组包含共享正文和真实差异的页面，例如概念说明、搜索/API 操作、能力限制与连接前提，验证以下闭环：

1. 同一共享源能分别产出 Milvus 与 Cloud 页面，短差异和独立页面均可表达。
2. 模拟一个外部 PR，共享修订只处理一次，两个产品能正确选择是否采用。
3. 原文一个段落变化，翻译只更新相应单元，并能显示源修订与待审核状态。
4. Milvus 的旧发布分支与 Cloud 当前服务行为可以不同，不强制同步升级。
5. 两条现有网站链路可消费结果或经适配层接入，预览、导航、锚点和链接完整。

建议记录共享修订所需的人工次数、同步冲突次数、翻译重复量、从源变更到两站上线的耗时、产品适用性错误。用这些指标比较 Git 权威源、飞书权威源及不同内容格式的成本，而不是只比较页面生成效果。

## 8. 证据与调研边界

- 一手来源为官方维护指南、标准、公开源文件与实际配置；历史工程需要单独标注，不能等同当前架构。
- Elastic 的旧 AsciiDoc 工程与当前 Markdown 工程分开处理；CockroachDB 归档仓库只作为历史模块化证据。
- GitLab 仓库架构说明有残留 Nanoc 描述，当前官方站点文档和实际 CI 均指向 Hugo；本文采用后两者作为现状依据。
- TiDB 贡献指南存在可能滞后的语言/分支描述；本文实际查看了所引用 Cloud TOC，但没有验证完整线上构建配置。
- 公开资料尚未给出与你们完全相同的飞书 Wiki ↔ 社区 Git 文档自动无损双向同步案例；其可行性与成本须用你们的导出器和典型复杂页面验证。
- 本次没有跑同行的构建流水线，没有测量各方案的成本与维护效率；适用性排序为本次研究判断。
- 报告中的代码及候选流程均为说明性示例，不是可以直接投入生产的配置。

本地 `research/evidence/` 保留了本次读取的部分公开源文件快照。进一步讨论应以正文链接的原始来源和后续工程试验为准。

GitLab、Elastic 与 CockroachDB 的源码路径、CI 和额外时效性核对见 [案例证据附录](./industry-cases-evidence.md)。
