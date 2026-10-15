# 接口设计

本目录面向 [zdoc](https://github.com/zilliztech/zdoc) 与 [md2md](https://github.com/zilliztech/md2md) 的维护者，是首期各接口的唯一定义，也是接口评审的议程。为什么改、整体怎么做见[方案总览](../proposal.md)；文档作者怎么写见[共享页面的写法与配置](../consumption-schema.md)；实施顺序、验收与各接口的状态见[首期实施计划第 6.1 节](../phase-1.md#61-待确认的接口)。

生产实现与集成验收尚未完成。1a 的例子用 Delete Entities，1b 的例子用 OpenAI。术语见[术语表](./glossary.md)。

## 接口地图

![Cloud 页面生成流水线：①按 lock 中 current / next 两个 commit 获取 milvus-docs 原文；②定位命名块与代码组并生成命名块清单；③按页面配置对命名块、语言示例或连续的代码行执行 add、replace、remove；④调用 md2md 预处理入口展开变量与片段；⑤沿用 zdoc 现有的产品过滤，只处理 Cloud 内容中的指令；⑥站点适配。两个版本各走一遍，按块比较后把不同的块成对包进 NextChannel，输出一份 MDX。下方对照 Milvus 侧：md2md 用 Milvus 变量展开并清除命名块标记。](../assets/generation-pipeline.png)

图 1 · Cloud 页面生成流水线

| 流水线中的位置 | 接口 |
|---|---|
| ① 按 lock 中的 commit 获取 milvus-docs 原文 | [04 通道与 commit 记录](./04-channels-and-lock.md) |
| ② 定位命名块，生成命名块清单 | [01 命名块的定义与解析](./01-named-blocks.md) |
| ③ 按页面配置执行 add、replace、remove | [02 共享页配置](./02-page-config.md) |
| ④ 展开变量与片段 | [03 md2md 提供的接口](./03-md2md-interfaces.md) |
| ⑤ 产品过滤 | 沿用 zdoc 现有能力，见 [02 共享页配置](./02-page-config.md#变换) |
| ⑥ 站点适配，其中的链接与图片 | [02b 链接与图片](./02b-links-and-images.md) |
| 两个版本合并为一份页面 | [04 通道与 commit 记录](./04-channels-and-lock.md) |
| PR 校验，以及生成结果进入 zdoc 发布 | [05 生成结果交给发布](./05-publish-handoff.md) |
| 页面从飞书切换到 Git，或从 Git 下线 | [05b 页面切换与归属](./05b-cutover-and-ownership.md) |
| milvus-docs 有新提交时，触发整条流程 | [06 上游变化的发现与影响报告](./06-upstream-changes.md) |

两条横跨多个接口的规则：

- **顺序是约束，不是实现细节。** 命名块必须在变量展开之前定位，因为标记只存在于原文中；Cloud 内容文件在第 ③ 步插入后，与原文一起在第 ④ 步展开变量。本地原型也按这个顺序实现。
- **站点适配不承担业务差异。** 第 ⑥ 步只负责 Tabs、提示组件、链接、图片和元数据，不为某种业务差异增加专门的处理。

## 一页的生命周期

流水线讲的是一次生成怎样进行；下表讲一个共享页从接入到下线要经过哪些步骤。lock 决定 Prod 与 UAT 各用哪个版本，`active.json` 决定这一页由飞书还是 Git 生成。

| 步骤 | 谁做 | lock | `active.json` | 网站上的变化 | 详见 |
|---|---|---|---|---|---|
| 接入 | 作者开 PR，工具写入 lock | `current` 与 `next` 都是跟踪分支的最新提交；功能未上线时 `current: none` | 不在清单中 | 无，只生成候选结果 | [04](./04-channels-and-lock.md#接入一页) |
| 激活 | 文档负责人触发 Fetch，先比较、再激活 | 不变 | 加入 | 从这次起由 Git 生成 | [05b](./05b-cutover-and-ownership.md#切换与激活) |
| 上游更新 | 工具每天发起，Cloud 审核合并 | `next` 改为新提交 | 不变 | UAT 显示新版本，Prod 不变 | [06](./06-upstream-changes.md) |
| 提升 | Cloud 文档工程师在功能上线时发起 | `current` 的 commit 值改成 `next` 的 commit 值 | 不变 | Prod 跟上 UAT | [04](./04-channels-and-lock.md#下线一页与提升) |
| 下线 | Cloud 文档工程师发起，只限已激活的页面 | `next` 改为 `none` | 不变 | UAT 不再显示，Prod 照常 | [04](./04-channels-and-lock.md#下线一页与提升) |
| 下线后提升 | 同提升；合并后删除飞书节点 | 页面目录删除 | 飞书节点删除后由 Fetch 移除 | 两边都不再显示 | [04](./04-channels-and-lock.md#下线一页与提升)、[05b](./05b-cutover-and-ownership.md#下线完成) |

**激活与提升是两件事。** 激活决定这一页由谁生成，一页只做一次；提升决定 Prod 用哪个版本，每次上线都做。功能未上线的新页面两件事都要做：接入时 `current: none`，激活后由 Git 生成、只在 UAT 显示，功能上线时提升，Prod 才显示。

## 阅读顺序

按下表顺序阅读：先看一个版本的页面怎样生成（01、02、03、02b，与流水线的顺序一致），再看两个版本怎样共存（04），然后是交给发布与页面切换（05、05b），最后是上游变化时怎样再走一遍（06）。

| 编号 | 文章 | 解决什么 | 主要用于 |
|---|---|---|---|
| 01 | [命名块的定义与解析](./01-named-blocks.md) | 原文中怎样标出可处理的一段，什么算写错，流水线中由谁处理 | 1a |
| 02 | [共享页配置](./02-page-config.md) | 作者在 zdoc 中为一个共享页写什么：目录、`page.yaml`、变换 | 目录在 1a，变换在 1b |
| 03 | [md2md 提供的接口](./03-md2md-interfaces.md) | md2md 为命名块的解析与清除、变量与片段的展开提供哪些接口 | 1a |
| 02b | [链接与图片](./02b-links-and-images.md) | 原文中的链接与图片怎样变成 Cloud 可用的地址 | 1a |
| 04 | [通道与 commit 记录](./04-channels-and-lock.md) | Prod 与 UAT 各读哪个版本，lock 由哪些 PR 写入，两个版本怎样合并 | 记录格式与接入在 1a，提升在 1b |
| 05 | [生成结果交给发布](./05-publish-handoff.md) | 生成结果怎样经过 PR 校验、进入 zdoc 现有的发布流程 | 1a 设计，1b 接入 |
| 05b | [页面切换与归属](./05b-cutover-and-ownership.md) | 一页怎样从飞书交给 Git、怎样下线，导航首期怎样处理 | 1b |
| 06 | [上游变化的发现与影响报告](./06-upstream-changes.md) | milvus-docs 有新提交后，怎样发起上游更新 PR | 1b |

## 每篇的结构

| 小节 | 内容 | 谁读 |
|---|---|---|
| 开头 | 这个接口解决什么，参与方有哪些，当前状态 | 所有人 |
| 约定 | 格式、字段与规则 | 实现者 |
| 出错时 | 错误情形与结果 | 实现者 |
| 例子 | Delete Entities 或 OpenAI，折叠 | 按需 |
| 设计理由 | 为什么这样定、不采用哪些做法、依据的数据 | 想了解原因时 |
| 验收 | 对应[首期实施计划](../phase-1.md)中的 T 编号 | 实现者与评审人 |
