# 技术设计

本目录面向 [zdoc](https://github.com/zilliztech/zdoc) 与 [md2md](https://github.com/zilliztech/md2md) 的维护者，定义 Phase 1 的工具怎样实现。要交付什么行为、作者怎么写，以[Phase 1 产品需求](../prd.md)为准；本目录的设计必须满足它，两处不一致时先改本目录。为什么改见[方案总览](../proposal.md)；实施顺序、验收与各项状态见[Phase 1 实施计划第 6.1 节](../phase-1.md#61-待确认的接口)。

**状态**：01–06 由原“接口设计”迁入，待工程维护者完善；07–09 是新写的草稿，依据 zdoc 现有工作流与 milvus-docs 的统计，待工程维护者确认。生产实现与集成验收尚未完成。术语见[术语表](../glossary.md)。

## 架构总览

### 组件与仓库

| 组件 | 仓库 | 本期改动 | 见 |
|---|---|---|---|
| 共享原文与 Milvus CI | [milvus-docs](https://github.com/milvus-io/milvus-docs) | PR 检查中加入命名块校验；固定 md2md 版本 | [01](./01-named-blocks.md)、[03](./03-md2md-interfaces.md) |
| md2md | [md2md](https://github.com/zilliztech/md2md) | 新增命名块的解析与清除、只做预处理的入口；一次发版 | [03](./03-md2md-interfaces.md) |
| zdoc 生成 | [zdoc](https://github.com/zilliztech/zdoc) | 按 lock 获取原文、定位命名块、执行变换、调用预处理、站点适配、两版合并、产品名检查；代码在 `packages/docs-tooling`（见下文“代码位置”） | [01](./01-named-blocks.md)–[04](./04-channels-and-lock.md)、[07](./07-site-adaptation.md) |
| zdoc 发布（Fetch） | zdoc | 接入生成结果；混源与激活；归属检查；翻译与恢复接入 | [05](./05-publish-handoff.md)、[05b](./05b-cutover-and-ownership.md) |
| zdoc 新增工作流 | zdoc | 接入时写 lock、PR 校验、上游更新、提升、激活前的比较 | [04](./04-channels-and-lock.md)、[06](./06-upstream-changes.md)、[08](./08-workflows-and-permissions.md) |

各仓库的分阶段改动见[Phase 1 实施计划第 3 节](../phase-1.md#3-各仓库改动)。

### 代码位置

zdoc 侧的代码放在 `packages/docs-tooling` 中。zdoc 的约定是发布与工作流工具都放在这里（`AGENTS.md`），它按来源组织：`lark/` 是飞书来源，`reference/` 是 SDK 与 REST 参考来源；共享页是第三种来源，与 `lark/` 并列。发布、校验、通知、图片上传、飞书表格的读取都在同一个包中，可以直接复用。

```
shared-docs/                              # 数据，master（见下文“数据文件”）
packages/docs-tooling/src/shared-docs/
  core/        页面配置 schema、命名块、变换、两版合并、链接换算、产品名检查；纯计算，不读写外部
  adapters/    按 commit 读 milvus-docs、调 md2md、图片、GitHub；飞书表格复用 lark/ 的读取
  commands/    build、check、lock、compare、upstream-plan、promote-plan，注册到 cli-main.ts
  fixtures/    测试用的合成 milvus-docs 仓库、试点页输入与基准输出
packages/docs-tooling/src/lark/                                # 认得 Docs 指向页面目录的记录；链接按 active.json 换算
.github/workflows/shared-docs-*.yml       # 只负责触发与权限，调用 pnpm docs-tooling shared-docs …
```

- `core/` 不依赖 `lark/`，与飞书有关的只经过适配器。飞书退出、删掉 `lark/` 时，共享页不受影响。
- 新路径登记到 zdoc 的代码与测试对照表（`scripts/docs-workflow/test-matrix.json`，`pnpm test:for-change`）；`shared-docs/` 不在 `deploy/contracts/master-tooling-sync.json` 的 `devOwnedPaths` 中，默认归 master，不用改这个文件。

### 生成流水线

![Cloud 页面生成流水线：①按 lock 中 current / next 两个 commit 获取 milvus-docs 原文；②定位命名块与代码组并生成命名块清单；③按页面配置对命名块、语言示例或连续的代码行执行 add、replace、remove；④调用 md2md 预处理入口展开变量与片段；⑤沿用 zdoc 现有的产品过滤，只处理 Cloud 内容中的指令；⑥站点适配。两个版本各走一遍，按块比较后把不同的块成对包进 NextChannel，输出一份 MDX。下方对照 Milvus 侧：md2md 用 Milvus 变量展开并清除命名块标记。](../assets/generation-pipeline.png)

图 1 · Cloud 页面生成流水线

| 流水线中的位置 | 见 |
|---|---|
| ① 按 lock 中的 commit 获取 milvus-docs 原文 | [04 通道与 commit 记录](./04-channels-and-lock.md) |
| ② 定位命名块，生成命名块清单 | [01 命名块的解析](./01-named-blocks.md) |
| ③ 按页面配置执行 add、replace、remove | [02 页面配置的读取与变换](./02-page-config.md) |
| ④ 展开变量与片段 | [03 md2md 提供的接口](./03-md2md-interfaces.md) |
| ⑤ 产品过滤 | 沿用 zdoc 现有能力，见 [02](./02-page-config.md#设计理由) |
| ⑥ 站点适配 | [07 站点适配](./07-site-adaptation.md)；其中的链接与图片见 [02b](./02b-links-and-images.md) |
| 两个版本合并为一份页面 | [04 通道与 commit 记录](./04-channels-and-lock.md#两个版本怎样合并成一页) |
| PR 校验，以及生成结果进入 zdoc 发布 | [05 生成结果交给发布](./05-publish-handoff.md) |
| 页面从飞书切换到 Git，或从 Git 下线 | [05b 页面切换与归属](./05b-cutover-and-ownership.md) |
| milvus-docs 有新提交时，触发整条流程 | [06 上游变化的发现与影响报告](./06-upstream-changes.md) |

两条横跨多篇的规则：

- **顺序是约束，不是实现细节。** 命名块必须在变量展开之前定位，因为标记只存在于原文中；Cloud 内容文件在变换中插入后，与原文一起在展开变量与片段时展开。本地原型也按这个顺序实现。
- **站点适配不承担业务差异。** 它只负责 Tabs、提示组件、链接、图片和元数据，不为某种业务差异增加专门的处理。

一个共享页从接入到下线的生命周期见[产品需求第 4 节](../prd.md#4-一页的生命周期)。

### 数据文件

| 文件 | 位置 | 谁写 | 格式见 |
|---|---|---|---|
| 共享来源配置 `source.yaml` | zdoc master `shared-docs/guides/` | zdoc 维护者 | [04](./04-channels-and-lock.md#共享来源配置与跟踪分支) |
| Cloud 变量 `Variables.json` | zdoc master `shared-docs/guides/` | 文档工程师 | [03](./03-md2md-interfaces.md#预处理) |
| 链接映射表 `links.yaml` | zdoc master `shared-docs/guides/` | 文档工程师 | [02b](./02b-links-and-images.md#链接) |
| 产品名检查规则 `product-names.yaml` | zdoc master `shared-docs/guides/` | 文档工程师 | [07](./07-site-adaptation.md#产品名检查) |
| 代码 Tabs 规则 `cloud-sdk-tabs.yaml` | zdoc master `shared-docs/guides/presentation/` | zdoc 维护者 | [07](./07-site-adaptation.md#代码-tabs) |
| 页面配置 `page.yaml`、Cloud 内容文件 | zdoc master `shared-docs/guides/pages/<页面标识>/` | 文档工程师 | [产品需求场景 3、4](../prd.md#场景-3接入一页)、[02](./02-page-config.md) |
| 版本记录 `lock.yaml` | zdoc master `shared-docs/guides/pages/<页面标识>/` | 工具 | [04](./04-channels-and-lock.md#每页一份-lockyaml) |
| 生效配置 `active.json` | zdoc dev `generated/en/manifests/shared-pages/<组>/` | Fetch，按飞书表格生成 | [05b](./05b-cutover-and-ownership.md#生效配置activejson) |
| `Docs` 链接、`Release Channel` | 飞书表格（DocsList）中每页的记录 | 文档负责人、文档工程师 | [05b](./05b-cutover-and-ownership.md#切换与激活) |
| 记录文件 `<页面标识>.json` | zdoc dev `generated/en/manifests/shared-pages/<组>/` | Fetch | [05](./05-publish-handoff.md#记录文件) |
| 页面 MDX | zdoc dev 各手册的内容目录 | Fetch | [05](./05-publish-handoff.md#页面-mdx) |
| 图片 | zdoc 现有的图片存储，按内容摘要命名 | Fetch | [02b](./02b-links-and-images.md#图片)、[05](./05-publish-handoff.md#图片上传) |

## 篇目

| 编号 | 文章 | 定义什么 | 对应的产品需求 | 所属阶段 |
|---|---|---|---|---|
| 01 | [命名块的解析](./01-named-blocks.md) | 命名块的识别、错误码 | 场景 2 | Phase 1a |
| 02 | [页面配置的读取与变换](./02-page-config.md) | `shared-docs/` 的位置、变换的匹配与校验 | 场景 3、4 | 目录在 Phase 1a，变换在 Phase 1b |
| 02b | [链接与图片](./02b-links-and-images.md) | 链接与锚点的换算、图片的转存地址 | 场景 5 | Phase 1a |
| 03 | [md2md 提供的接口](./03-md2md-interfaces.md) | 命名块的解析与清除、预处理入口的调用与返回 | 场景 1、2 | Phase 1a |
| 04 | [通道与 commit 记录](./04-channels-and-lock.md) | `lock.yaml` 的格式与写入、两版合并 | 场景 3、6、8、10 | 记录格式与接入在 Phase 1a，提升在 Phase 1b |
| 05 | [生成结果交给发布](./05-publish-handoff.md) | 交接物、记录文件、发布保护、翻译与恢复 | 第 6 节 | Phase 1a 设计，Phase 1b 接入 |
| 05b | [页面切换与归属](./05b-cutover-and-ownership.md) | `active.json`、激活与归属规则 | 场景 9、10 | Phase 1b |
| 06 | [上游变化的发现与影响报告](./06-upstream-changes.md) | 上游更新工作流、PR 与报告 | 场景 7 | Phase 1b |
| 07 | [站点适配](./07-site-adaptation.md) | Milvus Markdown 怎样变成 Cloud MDX；Tabs 规则文件的格式 | 场景 3、4 | Phase 1a |
| 08 | [工作流与权限](./08-workflows-and-permissions.md) | 各工作流的触发、身份、权限与失败通知 | 场景 3、7、8、9、10 | Phase 1a 起 |
| 09 | [错误目录](./09-error-catalog.md) | 统一的错误码、提示与应改的文件 | 各场景的“出错时” | Phase 1a 起 |
| 10 | [SDK Reference：从 web-content 生成（Rust 试点）](./10-sdk-reference.md) | 手册配置、整本手册的生成与 lock、Cloud 差异、接入 Fetch 与上线；草稿，待与文档负责人确认 | 待写入产品需求 | 待定 |

## 每篇的结构

| 小节 | 内容 |
|---|---|
| 开头 | 这一篇定义什么，对应哪些产品需求，参与方，当前状态 |
| 约定 | 格式、字段与实现规则 |
| 出错时 | 错误情形与结果 |
| 例子 | Delete Entities 或 OpenAI，折叠 |
| 设计理由 | 工程上为什么这样定、不采用哪些做法、依据的数据，折叠；产品上的取舍见产品需求 |
| 验收 | 对应[Phase 1 实施计划](../phase-1.md)中的 T 编号 |
