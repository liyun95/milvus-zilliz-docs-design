# milvus-zilliz-docs-design

Milvus × Zilliz Cloud 文档同源设计仓库，维护方案、架构、实施约定与设计样例，供文档团队和工程团队共同评审、演进和参考。

目标是让共享正文在 **milvus-docs** 维护一份，由 **zdoc** 消费并结合 Cloud 产品差异生成页面，逐步让飞书退出文档生产链。Milvus 继续使用既有发布流程。

当前处于设计与工程评估阶段。样例用于解释和验证设计，不代表生产能力已实现；实施范围与验证状态见[Phase 1 实施计划](docs/phase-1.md)。

## 设计文档

| 文档 | 回答的问题 |
|---|---|
| [方案总览](docs/proposal.md) | 为什么改、目标工作方式是什么、怎样逐步演进？（2026-10-13 对齐会材料，已冻结） |
| [Phase 1 产品需求](docs/prd.md) | Phase 1 交付后，文档工程师和文档负责人怎样工作、网站上看到什么、出错时怎样处理？作者的写法也在这里定下（评审与验收的依据） |
| [共享页写法速查](docs/authoring-spec.md) | 产品需求的附录：作者要写的文件、字段与出错情形的速查表 |
| [术语表](docs/glossary.md) | 本方案用到的术语分别指什么？ |
| [技术设计](docs/design/README.md) | 工具怎样实现产品需求：架构、数据文件、各环节的实现规则？（面向 zdoc 与 md2md 维护者） |
| [Phase 1 实施计划](docs/phase-1.md) | Phase 1 做什么、按什么顺序、怎样算完成？含待确认事项的唯一清单（面向实施者与评审人） |
| [Phase 1 实现指南](docs/implementation/README.md) | 实现怎样切分成工作包、每一步怎样验证、怎样审阅？含交给实现 Agent 的任务卡（面向实现 Agent 与审阅人） |

## 设计样例

- [Delete Entities](examples/delete-entities/walkthrough.md)：整篇复用，仅通过变量处理连接值差异。
- [Filtered Search](examples/filtered-search/walkthrough.md)：产品名与连接变量、共享多语言代码，以及 Cloud CLI 的补充。
- [双 commit 通道](examples/filtered-search/two-commit/walkthrough.md)（原型，规则见技术设计 04）：Prod 与 UAT 各读一个 milvus-docs 版本，不同的块自动包进 NextChannel。

OpenAI embedding 页是第三个试点候选，用于验证前提条件整节替换和凭证参数的代码行替换，尚未制作样例；差异分析见 [zdoc 代码变体与发布通道核验](research/zdoc-variants-and-channels-audit.md#3-openai-页对照)。

每篇样例包含作者输入、生成结果及适用边界，具体说明随样例维护。样例仍是接口定义之前的草案写法，与[产品需求](docs/prd.md)、[技术设计](docs/design/README.md)不一致处以它们为准，待接口确认后更新。

## 目录与维护

- `docs/`：当前方案、架构与工程约定。
- `examples/`：用于验证约定的独立样例。
- `research/`：行业调研与现有工程能力的核验依据。

调研入口：[行业实践](research/open-source-and-cloud-docs-practices.md)、[现有工具链](research/current-publication-chains-audit.md)、[能力复用](research/md2md-zdoc-reuse-audit.md)、[恢复能力](research/recovery-capability-audit.md)、[代码变体与发布通道](research/zdoc-variants-and-channels-audit.md)。事实核验以各文档记录的日期和固定修订为准。

设计结论更新到对应文档，接口变更同步检查受影响样例，会议安排和评审问题留在具体提案中。生产原文与工具实现仍在各产品仓库维护，本仓库保留设计及其验证材料。
