# 共享文档模块化与 zdoc 消费侧差异调研

调研日期：2026-10-10。承接前轮调研，本轮明确约束：`milvus-docs` 是共享正文的唯一权威源；Cloud 的选择、差异与页面组装规则放在 zdoc 侧；第一阶段即支持块或行粒度。本文为调研与设计建议，没有实现解析器、修改产品仓库或运行发布构建。

## 1. 结论与使用边界

行业实践支持“上游提供稳定内容，下游选择和组装”的方向，但不证明现成工具已经提供本项目需要的所有差异处理与发布保护。以下保留可核查的厂商与标准证据；本项目的当前决策见[接口设计](../docs/interfaces/README.md)，操作语义见[产品需求](../docs/prd.md)。

## 2. 更贴近本轮方向的证据

### 2.1 Grafana：明确优先由开源项目共享，商业项目消费

Grafana 官方写作指南将共享单元定义为适合多个上下文的句子、段落或页面，并要求区分 sharing 与 consuming 项目。它明确建议优先从开源项目共享，举例为 Tempo 提供片段、Grafana Enterprise Traces 消费，以保留外部贡献入口。上游建立 `docs/sources/shared/`，下游按 source、lookup、version 引用。[共享片段指南](https://grafana.com/docs/writers-toolkit/write/reuse-content/reuse-shared-content/)

其目录复用指南说明该模式不实现页内 conditional text，理由是条件增加源文件复杂度和外部贡献者理解成本。这个限制适用于它描述的目录挂载方案，不能扩展成 Grafana 全部文档都没有任何产品条件。[复用模式与取舍](https://grafana.com/docs/writers-toolkit/write/reuse-content/)

已核对实际开源源码：`config-options-intro.md` 是一个独立段落片段；histogram 页面引用它并组合其他片段，消费引用带版本参数。源码证明片段复用实际存在；Enterprise/Cloud 网站内部 shortcode 实现未公开，本轮没有验证其任意正文 overlay 或完整生产发布逻辑。[真实共享段落](https://github.com/grafana/grafana/blob/main/docs/sources/shared/visualizations/config-options-intro.md)、[真实消费页面](https://github.com/grafana/grafana/blob/main/docs/sources/visualizations/panels-visualizations/visualizations/histogram/index.md)

它还区分通用跨项目 `docs/shared` 与供 learning journeys 使用的 `shared-snippet` 命名区域，不应把后者描述为通用商业文档消费接口。指南承认列表嵌入与标题锚点需要额外处理，说明“能 include”不等于“任意片段组装后都正确”。[shortcode 语义与限制](https://grafana.com/docs/writers-toolkit/write/shortcodes/#docsshared)、[实际片段格式说明](https://github.com/grafana/grafana/blob/main/docs/sources/shared/example.md)

**对你们的参考：** shared source 保留在开源仓库；下游决定消费哪些片段；片段有来源和版本。无需照搬 Hugo，也不能据此认定 Grafana 已提供你们需要的全部块替换能力。

### 2.2 Couchbase：消费方实际按命名块 include/exclude，再补专属内容

Java SDK 的真实 `transactions.adoc` 从 common SDK 文档引用 intro、mechanics、query 等命名区域。消费页使用 `tags=mechanics;!library-cleanup-process`、`tags=query;!library-begin-transaction` 排除子区域，再加入 Java 专属说明和示例。这是实际厂商源码中的块级消费选择，不只是框架演示。[固定修订的消费源码](https://github.com/couchbase/docs-sdk-java/blob/ee3255a8519ade4471d75bf1056418b347b177e9/modules/concept-docs/pages/transactions.adoc)

Java 的 `antora.yml` 定义 `version-common`，页面引用它来选择共享组件版本。本轮没有据此确认构建对每个 Git 仓库锁定 commit SHA。[组件版本配置](https://github.com/couchbase/docs-sdk-java/blob/ee3255a8519ade4471d75bf1056418b347b177e9/antora.yml)

Couchbase 站点 playbook 还聚合 Server、Capella、SDK 等内容源；配置把 `docs-devex` 标为 Server 与 Capella 共享，但它存在 capella 分支，且 Capella 正文源私有。因此可以确认多源组装，不能确认全部 Cloud 差异都位于消费者仓库。[站点 playbook](https://github.com/couchbase/docs-site/blob/6dc97eae61b41d33907e730ccb43dc7bdd11e118/antora-playbook.yml)

**对你们的参考：** 源提供名字与边界，下游表达选择与排除，并在片段间写产品专属内容。它直接支持“zdoc 消费级差异”的局部机制，但不是完全相同的 Milvus→Cloud 系统实例。

### 2.3 DITA：成熟的命名引用与外部块替换机制

OASIS DITA 标准通过 `conkeyref` 将正文引用与产品 map 中的绑定分离。标准的 OEM 示例让不同 map 将同一个 key 绑定到不同产品名与提示内容。因此，消费者配置可以改变输出，而不把各产品的分支条件全部写入共同正文。[正式标准中的产品绑定示例](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/base/example-keys-conref-redirection.html)

DITA `conaction` 还支持按元素 ID 进行 `pushbefore`、`pushafter`、`pushreplace`，替换内容在其独立源中维护；它要求结构类型兼容，并将多个源替换同一目标视为错误。[正式标准中的外部元素替换](https://docs.oasis-open.org/dita/dita/v1.3/os/part1-base/langRef/attributes/theconactionattribute.html)

**证据性质：** 这是标准能力，本文没有把它说成某家厂商已经采用的特定生产架构。值得借鉴其稳定身份、消费绑定、插入/替换和结构校验，不必因此将现有 Markdown 全量迁到 DITA。

### 2.4 其他案例的边界

前轮 TiDB 和 OpenShift 把产品条件写入共同源。Foreman/Satellite 同样有模块化和产品属性覆盖，但共享正文中仍存在 `ifdef::satellite[]`，所以它们不是“全部 Cloud diff 放在 zdoc”这条路线的直接证明。[Foreman 条件实例](https://github.com/theforeman/foreman-documentation/blob/a4168b597a026c84ccd06f58a6e9bbd909ae047a/guides/common/modules/proc_importing-a-repository.adoc)

更完整的 Couchbase、Antora、Foreman 原始路径与证据边界见 [消费侧案例附录](./downstream-composition-evidence.md)。

## 3. 对本项目的含义

采用少量中性命名边界，由消费方维护产品差异，可以减少开源作者理解商业条件的负担。独立文件共享、命名区域和产品变量各有适用范围，不能把“支持行粒度”理解为按物理行号定位，也不能把厂商的 include 能力等同于任意代码替换。

本项目的当前选择是 milvus-docs 维护共享原文，zdoc 内生成 registry 并消费，Cloud 产品差异进入 Git，飞书按页退出。历史调研中的候选定位方式和飞书权威方案不作为当前设计接口。
