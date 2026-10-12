# 下游消费共享文档：公开代码证据

核查日期：2026-10-10。仅修改本文件。以下明确区分实际厂商实例、框架能力和对 Milvus/Zilliz 的设计推论。

## 1. Couchbase：实际存在消费侧选择共享片段，Cloud 细节不完全公开

官方站点构建仓库将 `docs-devex` 标为 Server 与 Capella 的共享内容，分别获取 release/8.0、release/7.6、release/7.2、capella 分支；同一 playbook 聚合私有 `docs-capella`，以及公开 `docs-server`、`docs-sdk-common` 和各 SDK 仓库。这是可核对的多源组装实践，但共享源使用 capella 分支意味着不能据此声称“全部产品差异都在消费者仓库”。[固定修订的 playbook](https://github.com/couchbase/docs-site/blob/6dc97eae61b41d33907e730ccb43dc7bdd11e118/antora-playbook.yml#L139)

更直接的消费侧块级选择例子来自 Java SDK 文档：transactions.adoc 从 common SDK 引入 intro、mechanics、query 等有名字的区域，且消费者显式排除 `library-cleanup-process`、`library-begin-transaction`。同时页面在共享片段之间加入 Java 专属代码示例和说明。这里的差异由消费页面的选择与组装表达，不需要共享源知道每个消费者的页面布局。[消费页面源码](https://github.com/couchbase/docs-sdk-java/blob/ee3255a8519ade4471d75bf1056418b347b177e9/modules/concept-docs/pages/transactions.adoc#L16)

Java 的 component descriptor 指定 `version-common`，页面通过该属性绑定共享 component 版本。这个例子证明消费者能够选择共享文档版本，尚不能证明其线上构建锁定每个仓库 commit SHA。[Java component 配置](https://github.com/couchbase/docs-sdk-java/blob/ee3255a8519ade4471d75bf1056418b347b177e9/antora.yml)

**证据边界：** Capella 正文仓库私有，未核实 Capella 实际怎样做局部覆盖或过滤；上面 block include/exclude 是官方 SDK 实际源码，不是“开源 Server 到商业 Cloud 的全部差异都在下游”的证明。不得把“站点配置包含私有 Cloud 仓库”推断成已查到它的正文消费策略。

## 2. Antora：框架能力非常接近 registry/consumption，但并非自动 patch 系统

Antora 的 partial 有资源身份，可跨 component 引入；完整引用包含 version、component、module、family、path。include 支持 `tag`、`tags` 和 `lines`，且片段插入后在消费页面上下文中解析。这支持命名块选择、行级提取和消费方参数绑定。partial 本身不生成独立页面。[Partials](https://docs.antora.org/antora/latest/page/partials/)、[Include a Partial](https://docs.antora.org/antora/latest/page/include-a-partial/)

playbook 控制输入仓库、分支和站点配置。由此可以把“内容源”与“发布组装项目”分开。[Playbook 说明](https://docs.antora.org/antora/latest/playbook/)

**能力边界：** include/exclude 并不等于任意 AST block 替换、冲突复核或兼容性验证。这些如果采用 Markdown registry + zdoc overlay，需要自建。Antora supplemental UI 的 override 仅替换 UI 资源，不能作为正文 overlay 的证据。

## 3. Foreman / Red Hat Satellite：有结构化模块和产品属性覆盖，但不是差异全放消费侧

公开 Foreman 文档按 modular documentation framework 组织。common/attributes.adoc 先加载 base、再加载 `attributes-{build}.adoc`，构建产品包括 Satellite；这证明产品属性覆盖与共享正文可分离。[公共属性入口](https://github.com/theforeman/foreman-documentation/blob/a4168b597a026c84ccd06f58a6e9bbd909ae047a/guides/common/attributes.adoc#L64)、[构建说明](https://github.com/theforeman/foreman-documentation/blob/a4168b597a026c84ccd06f58a6e9bbd909ae047a/guides/README.md)

但共享模块包含 `ifdef::satellite[]` 等产品条件，因此产品逻辑实际仍进入公开上游正文。它可以参考模块类型和 assembly/include 组织方式，不能作为用户希望的“Milvus 上游不承担 Cloud diff”直接案例。[条件块实例](https://github.com/theforeman/foreman-documentation/blob/a4168b597a026c84ccd06f58a6e9bbd909ae047a/guides/common/modules/proc_importing-a-repository.adoc)

## 对当前方案的推论

基于 Couchbase 的实际共享片段消费实践，可行的第一阶段是：Milvus 正文仅增加中性的稳定块身份（不增加 Cloud 条件），zdoc 固定源修订、选择 include/exclude blocks，在明确位置插入或替换 Cloud 专属模块。共享源需要承担“可引用”的结构契约，但不需要承担“商业产品差异”的逻辑。

推荐优先采用有名字的语义块；行号选择保留为迁移时的受控机制。若必须行级过滤，应同时锁定源 SHA 与被选内容 hash，上游变动后要求显式复核，避免行号漂移静默删错内容。这属于设计建议，不是上述厂商的已核实实现。

重要区别：排除共享块与用 Cloud 模块替换共享块，是消费策略；直接在中间层复制并修改共同正文，会重新制造第二权威源。替换必须是独立 Cloud 变体，保留被替换块 ID、基线 hash、适用原因和审核状态。
