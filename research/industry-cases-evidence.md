# 多产品文档工程案例：GitLab、Elastic、CockroachDB

调研日期：2026-10-10（Asia/Shanghai）。仅采用官方文档、官方公开源码。下文将“公开文件中存在的实现”“官方描述的工作流”与“对 Milvus / Zilliz 的推论”分开。读取了公开仓库具体文件与 CI 配置，没有访问企业内部发布系统，不能据此证明每个生产构建均成功执行。

## 1. GitLab：共享源码，多 offering，同站发布；英语源码驱动自动翻译

### 1.1 内容仓库和网站构建仓库分离

官方目前说明：文档源码随产品代码存放，例如主 GitLab 的 `/doc`、Runner 的 `/docs`、Omnibus 的 `/doc`；网站由独立 `docs-gitlab-com` 仓库通过 Hugo 聚合构建。文档 MR 提交到对应内容仓库；同一源码也进入 GitLab 产品内 `/help`。这不是“把所有文档强制合并到一个仓库”。[官方架构](https://docs.gitlab.com/development/documentation/site_architecture/)

直接仓库证据：`docs-gitlab-com/.gitlab/ci/build.gitlab-ci.yml` 中的 `build:compile_site` 使用 `$HUGO_IMAGE`，执行 `make clone-docs-projects` 拉取内容，随后执行 Hugo 构建，输出 `public` artifact。[构建 CI 源码](https://gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/blob/main/.gitlab/ci/build.gitlab-ci.yml)

发布 CI 配置另设 `pages-production`、`pages-review-apps`、`pages-archives`，均消费相应构建输出。Review app 有独立 URL 前缀和有效期；生产 job 带项目路径判断，排除 fork。[发布 CI 源码](https://gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/blob/main/.gitlab/ci/deploy.gitlab-ci.yml)

官方发布指南还说明版本网站从各产品对应 stable branches 取内容；主站默认分支展示 upcoming 文档，历史版本归档。这说明“多产品源码→独立构建项目→站点”的拓扑本身不是反模式，关键是内容修改入口与版本选择清楚。[发布指南](https://docs.gitlab.com/development/documentation/site_architecture/deployment_process/)

### 1.2 offering / tier 差异表达在页级、章节级

GitLab 区分 GitLab.com、Self-Managed、Dedicated 等 offering，以及 Free、Premium、Ultimate 等 tier。在页首或章节标题下标注适用范围，章节只需补充与父级不同的范围。官方语法是 Hugo shortcode。[适用性写作规范](https://docs.gitlab.com/development/documentation/styleguide/availability_details/)

以下是保持真实语法、用中文内容简化的示意：

```markdown
{{< details >}}
- Tier: Premium, Ultimate
- Offering: GitLab.com
{{< /details >}}

云版订阅相关步骤。
```

实际源码 `gitlab/doc/subscriptions/manage_subscription.md` 在同一文件中维护 GitLab.com 与 Self-Managed 的独立章节，分别标注 offering。[真实内容源码](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/subscriptions/manage_subscription.md) / [可直接读取的 raw 源码](https://gitlab.com/gitlab-org/gitlab/-/raw/master/doc/subscriptions/manage_subscription.md)

**边界：**这里已经验证的是共享页面和章节适用性标识。不能把这些 shortcode 等同于“构建时完全删除另一产品的块”，也不能声称 GitLab 为每个 offering 自动生成一套独立品牌网站。它适合共享站点中帮助用户辨别差异；Milvus 与 Zilliz 若要分别输出纯净页面，还需另加构建过滤。

### 1.3 社区修改进入权威源码

官方 workflow 让社区贡献者提交 MR；开发者是新功能文档的主要作者，尽可能把文档与代码置于同一 MR，技术写作团队和领域专家参与评审。文档独立 MR 也允许，发布节奏要与功能对应。[官方贡献与评审流程](https://docs.gitlab.com/development/documentation/workflow/)

**对当前问题的推论：**在共享内容直接由公共 Git 仓库维护的范围内，社区 MR 合并就是权威源更新，省去了把导出的 Milvus 页面再回写另一套 authoring source 的步骤。这个推论不能扩展成“GitLab 有 Git↔企业 Wiki 双向同步”，未发现这类证据。

### 1.4 翻译是派生内容，贡献者只改英文

GitLab 当前架构文档明确规定：英语为 canonical source；译文置于 `doc-locale` 等语言目录，日本语示例为 `/doc-locale/ja-jp/`；译文由 automation 更新，贡献者只贡献英文；development 文档不翻译。这是官方描述的 semi-autonomous 流程。[翻译章节](https://docs.gitlab.com/development/documentation/site_architecture/#documentation-in-other-languages)

网站另将导航、短 UI 字符串、较长页面模板分开本地化，以英语配置为源。[网站仓库的 Localization Architecture](https://gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/blob/main/doc/architecture.md#localization-architecture)

**未验证：**官方这里没有披露足以复刻的翻译服务选择、段落 hash、翻译记忆库、自动触发阈值或人工审核覆盖率，不应补写成已证实的具体产品流程。

### 1.5 时效和文档内部不一致

当前官方架构和实际 CI 均指向 Hugo；但构建仓库 `doc/architecture.md` 的旧“Deploy the docs site”段落仍写 Nanoc。调研采用真实 CI 作为现状证据，不采用这一残留描述。[仓库架构文件](https://gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/blob/main/doc/architecture.md) / [真实 Hugo 构建配置](https://gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/blob/main/.gitlab/ci/build.gitlab-ci.yml)

## 2. Elastic：必须区分 2025 年以前 AsciiDoc 与当前 Markdown cumulative docs

### 2.1 当前系统：2025-04 迁移，跨部署模式共同维护

官方明确：2025 年 4 月迁到 `elastic.co/docs`，使用 Markdown 和 `docs-builder`，覆盖 Stack 9.x、Cloud Hosted、Cloud Serverless、ECE、ECK。9.x 文档采用 cumulative 模式，不为每个 minor release 复制整套页面，而是在页内表达版本变化。8.x 及更早版本仍属于 `elastic.co/guide` 的 AsciiDoc 系统。[系统分界说明](https://www.elastic.co/docs/contribute-docs/)

多数叙述性文档来自公开 `elastic/docs-content`；大量 reference 文档仍位于相应产品仓库。用户从“Edit this page”进入 GitHub 编辑并提交 PR，由 Elastic 成员评审、合并、向发布分支传播；某些仓库须将修改从 main/master backport 到发布分支。[官方网页贡献流程](https://www.elastic.co/docs/contribute-docs/on-the-web)

公开 `docs-builder/config/assembler.yml` 列出 narrative 与 references 来源，并为环境选择 current / next / edge。不同来源可以选择不同分支；配置中也存在 private 来源。这是“共同发布平台，分布式内容所有权”，不能简化成只有一个公开仓库。[真实聚合配置](https://github.com/elastic/docs-builder/blob/main/config/assembler.yml)

### 2.2 实际页级、节级、块级差异和共享 include

直接读取 `elastic/docs-content/deploy-manage/security.md`：页首有 `applies_to`，部分章节给出部署模式适用信息；该页用 `include` 引入多个 `_snippets/*.md`。同一源页覆盖多种部署，局部差异有明确标签。[真实安全概览源码](https://github.com/elastic/docs-content/blob/90f6e6299a916300389b3faa58f43eb229c7c78a/deploy-manage/security.md)

```markdown
:::{include} /deploy-manage/security/_snippets/complete-security.md
:::
```

`deploy-manage/security/secure-settings.md` 的实际源文件使用 `applies-switch` / `applies-item`：ECH 与 ECE 共享一组步骤，ECK 单独链接 Kubernetes 操作，Self-Managed 使用本机工具。这是企业正在使用的内容实例，不是仅有工具示例。[真实 secure-settings 源码](https://github.com/elastic/docs-content/blob/90f6e6299a916300389b3faa58f43eb229c7c78a/deploy-manage/security/secure-settings.md)

以下保留原指令结构，用中文代替正文：

```markdown
:::::{applies-switch}
::::{applies-item} { ess:, ece: }
云控制台步骤。
::::
::::{applies-item} eck:
Kubernetes 步骤。
::::
::::{applies-item} self:
自行部署步骤。
::::
:::::
```

工具说明确认这些是同一页面的适用性标签 tab，并支持版本、部署模式等条件；同页多个 switch 会同步选择。[applies-switch 工具语义](https://elastic.github.io/docs-builder/syntax/applies-switch/)

**边界：**`applies_to` 是适用性元数据，`applies-switch` 是读者可选择的展示。已验证源码中的块级分支，不应自动推断它能生成分别面向 Milvus 和 Zilliz、物理删除另一产品内容的两套 artifact。该能力需要单独验证或实现。

### 2.3 不把所有差异塞进 if：官方明确给出内容拆分准则

Elastic 的部署模式写作指南给出真实团队规则：通用小任务单独维护并被链接；相同概念但配置入口不同，先共享概念再分支步骤；差异较小用限定章节；差异改变用户操作模型时可拆 sibling pages；复杂流程在 tab 与拆页间权衡。对不可用功能也要解释或提供替代路径。[官方跨部署写作策略](https://www.elastic.co/docs/contribute-docs/how-to/deployment-types/strategies)

**对 Milvus / Zilliz 的推论：**向量检索语义、表达式、索引原理很适合共享；账户、云控制台、账单、部署、运维等可能需要独立页面。行级判断适合很小的差异，复杂操作路径应保留产品所有权，避免把单一大文档写成难以评审的条件程序。

### 2.4 CI、预览与发布配置已经独立化

公开 `docs-content/.github/workflows/docs-build.yml` 在 PR、main push、merge group 上触发，调用 `elastic/docs-actions` 共享构建 workflow，并启用 Vale。[真实构建 workflow](https://github.com/elastic/docs-content/blob/90f6e6299a916300389b3faa58f43eb229c7c78a/.github/workflows/docs-build.yml)

`docs-deploy.yml` 则在 docs-build 完成后调用共享 deploy workflow。[真实发布入口](https://github.com/elastic/docs-content/blob/90f6e6299a916300389b3faa58f43eb229c7c78a/.github/workflows/docs-deploy.yml)

官方本地流程支持 `docs-builder` 做完整构建检查，以及 `docs-builder serve` 预览。[本地构建与预览](https://www.elastic.co/docs/contribute-docs/locally)

**未验证：**这里只验证了公开触发器和调用关系；尚未逐层追踪被调用 workflow 到生产基础设施，不应声称每个 PR 的具体部署权限、发布成功率或服务等级。

### 2.5 历史系统仍有可借鉴点，但不能当作 9.x 当前架构

`elastic/docs/README.asciidoc` 当前开头直接说明它属于 pre-9.0 系统。历史方式用集中 `conf.yaml` 定义仓库、books、branches，聚合产品文档并做跨文档链接检查；共享 attributes 文件维护统一词汇和 URL。这里可借鉴发布清单与共享变量，但不应将其描述为 Elastic 当前全部文档技术栈。[历史构建仓库 README](https://github.com/elastic/docs/blob/master/README.asciidoc)

**未验证：**此次没有追踪 Elastic 当前翻译系统；不要用 Elasticsearch API examples 的多语言客户端代码选项来替代自然语言文档翻译证据。

## 3. CockroachDB：有力的历史“共享模块＋上下文条件”实现，2026-10-06 已归档

### 3.1 必须标明历史状态

2026-10-10 直接打开官方 GitHub `cockroachdb/docs`，页面显示仓库在 **2026-10-06** 被归档并设为只读。因此以下 Jekyll / Liquid 资料是公开历史实现，不能再称为当前活跃的发布仓库。[归档状态](https://github.com/cockroachdb/docs)

目前旧 `www.cockroachlabs.com/docs/...` URL 会重定向到 `docs.cockroachlabs.com/docs/...`，页面出现 Mintlify 托管资产。可判断前端已发生变化，但没有当前公开源码及迁移说明来确认完整新架构；不推断新平台继承原 include 机制。[当前站点观察](https://docs.cockroachlabs.com/docs/stable/architecture/overview)

### 3.2 具体可复现历史源码

读取时历史仓库 HEAD 为 `27e64c5d4481a3c888f8f1f61c540fcba37e0594`，以固定 commit 引用：

- 云版页面：`src/current/cockroachcloud/upgrade-cockroach-version.md`。[源码](https://github.com/cockroachdb/docs/blob/27e64c5d4481a3c888f8f1f61c540fcba37e0594/src/current/cockroachcloud/upgrade-cockroach-version.md)
- 自托管 v26.2 页面：`src/current/v26.2/upgrade-cockroach-version.md`。[源码](https://github.com/cockroachdb/docs/blob/27e64c5d4481a3c888f8f1f61c540fcba37e0594/src/current/v26.2/upgrade-cockroach-version.md)
- 两页共同引用 `common/upgrade/overview.md`；随后各自拼装 Cloud / Self-Hosted 专用步骤。

共同模块 `src/current/_includes/common/upgrade/overview.md` 根据调用页面路径判断是否为 cloud，控制段落、表格、链接、句内短语，已经具有实际的块级及行内差异处理。[共同模块真实源码](https://github.com/cockroachdb/docs/blob/27e64c5d4481a3c888f8f1f61c540fcba37e0594/src/current/_includes/common/upgrade/overview.md)

简化示意：

```liquid
{% if page.path contains "cockroachcloud" %}
云版升级规则。
{% else %}
自行部署升级规则。
{% endif %}
```

官方历史 `MarkdownGuide.md` 说明按版本、产品设置 `_includes`，与产品和版本无关的共享块放 `common`；也说明 include 的渲染限制，以及从其他仓库拉代码片段的 remote include。这些是已采用的写作约定。[历史 MarkdownGuide](https://github.com/cockroachdb/docs/blob/27e64c5d4481a3c888f8f1f61c540fcba37e0594/MarkdownGuide.md#include-files)

**对 Milvus / Zilliz 的推论：**“共同原理模块＋产品专用步骤模块＋少量条件”能得到独立页面而不用复制整个内容。实际 CockroachDB 例子将产品条件绑定到页面路径，可工作，但重命名路径可能改变行为；若重新设计，更适合显式 product/version metadata，而不是隐式字符串判断。这是架构建议，不是 CockroachDB 已采用的改进。

**未验证：**其当前社区编辑流程、新站 CI、翻译系统没有得到足够公开证据。此案例用来说明可验证的历史模块化实践，不适合作为当前平台采购或具体新框架选型依据。

## 4. 三个案例对当前调研的共同启示

以下为基于上述事实的分析，不是厂商原话：

| 当前问题 | 公开实践支持的方向 | 不应推出的结论 |
| --- | --- | --- |
| 两产品大量共享但有局部差异 | 权威公共内容模块；显式产品/版本适用元数据；短差异用块，长操作流程拆页 | 每个功能都该做行级 if，或所有页面必须合并 |
| 社区 PR 需要回流到 Wiki | 让社区 PR 直接修改共享权威源；将生成输出从编辑入口移出 | 企业普遍实现可靠 Git↔Wiki 无损自动双向同步 |
| 网站链路较长 | 内容所有权与构建部署分离；多源码仓库仍可以统一质量与发布平台 | 多仓库、多阶段流水线天然错误，重构必须先合仓 |
| 自动翻译 | 英文 canonical source；译文作为自动派生产物；明确哪些内容不译 | 机器翻译无需任何人工审核，或以上厂商均使用同一翻译工具 |

对 Milvus / Zilliz 可优先做小范围验证：选择有真实差异、社区贡献和多语言需求的一个功能，试验共享源内容能否直接贡献、分别构建两产品页面，并能从一次源修改追踪到两种产品和多语言发布。先验证编辑与发布闭环，再决定是否迁走飞书全部内容。
