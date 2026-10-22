# WP3 读取：页面配置、lock、原文与命名块

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：WP0 已合并（[zilliztech/zdoc#792](https://github.com/zilliztech/zdoc/pull/792)，commit [`5dd0e56`](https://github.com/zilliztech/zdoc/commit/5dd0e56a58054864eda231deeb76f1945be80fb0)）；[WP2](./WP2-md2md-preprocess.md) 不阻塞，发版前用替身　**状态**：WP3a 已合并（[zilliztech/zdoc#796](https://github.com/zilliztech/zdoc/pull/796)，commit [`5844587`](https://github.com/zilliztech/zdoc/commit/5844587037d5397e8ebd1510235db5d8592584d7)）；WP3b 未开始

## 目标

做完后，给定一个页面目录，zdoc 能：读出并校验 `page.yaml` 与 `lock.yaml`；按 lock 中的 commit 取到 Milvus 原文；找出原文中的命名块并判断类型与语言；删除标记、用 Cloud 的变量展开，得到交给站点适配（WP4）的 Markdown。整个过程的错误一次全部报出。

本工作包不做变换（WP10）、站点适配（WP4）、链接与图片（WP5），也不接任何工作流（WP8）。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 1（1-1）、场景 2（2-4、2-5）、场景 3：怎样操作、`page.yaml` 的字段、规则、系统行为、出错时 | 配置写法与报错 |
| [技术设计 01](../../design/01-named-blocks.md) | 识别规则、已知局限 | 类型与语言的判断规则；列表中的代码块 |
| [技术设计 02](../../design/02-page-config.md) | `shared-docs/` 的位置、出错时 | 目录与校验 |
| [技术设计 04](../../design/04-channels-and-lock.md) | 共享来源配置与跟踪分支、每页一份 `lock.yaml`、接入一页、出错时 | lock 的格式与校验 |
| [技术设计 03](../../design/03-md2md-interfaces.md) | 两组接口的签名 | `Md2md` 适配器 |
| [技术设计 07](../../design/07-site-adaptation.md) | front matter 中 `beta` 一行 | `beta` 的可选值从哪里来 |
| [实现指南](../README.md) | 2.3、2.6、2.7、第 5 节 | 合成仓库、适配器、契约用例、规则 |
| [WP0 走读](../walkthroughs/WP0.md) | 全文 | 已有的目录、替身与测试工具 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/shared-docs/` 下：`core/` 新增读取逻辑；`adapters/` 新增真实的 milvus-docs 读取，扩展接口；`commands/` 新增 `inspect` 命令；测试与测试素材 | 仓库根目录的 `shared-docs/`：不建，试点页只在测试素材中 |
| `packages/docs-tooling/src/cli-main.ts`：注册 `shared-docs inspect` 子命令 | `lark/`、`manuals/` 等现有模块 |
| `spec/pending.json`：删掉本工作包的编号；`requirements.json` 更新后重新复制 | 自行修改 `spec/requirements.json`、基准输出 |
| WP3b：`packages/docs-ui/src/shared/utils/docHeadingTags.ts` 只加一个 `export`，供 `commands/` 引用（计划审阅时批准） | 读取 dev 上的飞书表格快照：归 WP8 |
| WP3b：`packages/docs-tooling/package.json` 加依赖 `@zilliz/mdtomd`，版本写死为 `1.3.0`（不用 `^`）；`pnpm-lock.yaml` 随之更新；`adapters/` 新增真实的 `Md2md` 实现 | 其他依赖的版本 |

本工作包是共用类型的主人（实现指南第 5 节“协作规则”）：`core/types.ts` 与 `adapters/types.ts` 中的类型由本工作包扩展。

改动较大，建议分两个 PR：

| PR | 内容 |
|---|---|
| WP3a | `source.yaml`、`page.yaml`、`lock.yaml` 的读取与校验；真实的 milvus-docs 读取（按 commit 读文件、判断 commit 是否在跟踪分支上、是否为祖先）；接入时写 lock 的计算 |
| WP3b | 命名块清单（经 `Md2md.parseBlocks` 校验，再判断类型与语言）；删除标记；经 `Md2md.preprocess` 展开变量；`inspect` 命令 |

## 接口

```ts
// core：纯计算，输入都由调用方读好传入
parsePageConfig(pageId, yamlText, context): { config } | { errors }   // context 含已有手册、beta 可选值
parseLock(yamlText): { lock } | { errors }
planLock({ existing, trackedHead, fromFork }): { lock } | { errors }  // 产品需求 3-1；fork 时报 LOCK_FORK_PR
inventoryBlocks(markdown, parseResult): NamedBlockInventory[]          // 类型、语言、行号、内容摘要

// adapters
MilvusDocsReader: readFile(commit, path)；isOnBranch(commit, branch)；isAncestor(a, b)
// 真实实现读 Git，测试中读实现指南 2.3 的合成仓库；替身与真实实现跑同一组契约测试

// commands
pnpm docs-tooling shared-docs inspect --pages <目录> --page <页面标识> --repo <milvus-docs 检出>
// 打印：配置与 lock 的校验结果、命名块清单、展开后的 Markdown（每个版本一份）
// 页面还没有 lock.yaml 时，按产品需求 3-1 用 planLock 的结果（两个版本都取跟踪分支的最新提交），并标明这是计划值；不写文件
```

- 已有手册的列表取自 [`manuals/registry.ts`](https://github.com/zilliztech/zdoc/blob/master/packages/docs-tooling/src/manuals/registry.ts)；`beta` 的可选值取自 [`packages/docs-ui/src/shared/utils/docHeadingTags.ts`](https://github.com/zilliztech/zdoc/blob/master/packages/docs-ui/src/shared/utils/docHeadingTags.ts) 的 `DOC_HEADING_TAGS`，去掉 `BYOC`。两者都在 `commands/` 中读出后传给 `core/`，`core/` 不直接引用。
- 变量表只来自 `shared-docs/Variables.json`，原样传给 `preprocess`（产品需求 1-1）。
- md2md 1.3.0 已于 2026-10-22 发布。WP3a 合并时 `Md2md` 用的是替身；WP3b 接入真实的包 `@zilliz/mdtomd@1.3.0`（`@zilliz/mdtomd/blocks.js`、`@zilliz/mdtomd/preprocess.js`），替身保留给不需要真实包的测试。从 md2md 复制的契约用例只用来测真实的包；替身仍按预设返回结果，与真实的包一起跑 WP0 的形状契约（`adapters/contract/`），不重新实现 md2md 的规则。用例从 md2md 复制：[`a143b27` 的 `test/contract/cases/blocks/`](https://github.com/zilliztech/md2md/tree/a143b27c475059f1fe22e84e074953b05bd9cd37/test/contract/cases/blocks) 与 [`preprocess/`](https://github.com/zilliztech/md2md/tree/a143b27c475059f1fe22e84e074953b05bd9cd37/test/contract/cases/preprocess)；`preprocess/README.md` 说明了怎样运行这些用例。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `1-1` | 传给 `preprocess` 的变量表与 `Variables.json` 完全相同；缺少变量时页面失败，不回退到 Milvus 的值 |
| `2-4` | 原文中写错的标记让这一页失败，错误带文件与行号 |
| `2-5` | Markdown 块、单语言代码组、多语言代码组各一个；语言取自代码块；列表中缩进的代码块也能识别为代码组 |
| `3-1` | 没有 lock 时，`current` 与 `next` 都取跟踪分支的最新提交 |
| `3-7` | 输出位置由页面标识与 `publish[].path` 决定，三篇试点页与 zdoc [dev 上的现有路径](https://github.com/zilliztech/zdoc/tree/dev/content/en/guides/tutorials/development)一致 |
| 页面配置的 7 个错误码（含 `CONFIG_SYNTAX_INVALID`） | 每个一个错误样例（实现指南 2.5），断言 `code`、`file`、`line`、`page` |
| `CONFIG_VARIABLES_INVALID`；`Variables.json` 的 `CONFIG_SYNTAX_INVALID`（WP3b） | `Variables.json` 不是 JSON、顶层不是对象、同一层有只差大小写的键各一个样例；在调用 md2md 之前报出 |
| lock 的 5 个错误码 | 同上；`LOCK_COMMIT_NOT_FOUND`、`LOCK_ORDER` 用合成仓库构造 |

做完后把这些编号从 `spec/pending.json` 中删掉。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；本工作包的编号不在 `pending.json` 中
- [ ] `pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] 真实的 milvus-docs 读取与替身通过同一组契约测试
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写，包括 “How to try it”：对 Delete Entities 运行 `inspect`，以及把 `page.yaml` 改错一处后再运行，看到的报错

## 不做

- 变换、两版合并、站点适配、链接与图片、产品名检查。
- 读写 GitHub、飞书：接入时写 lock 只做计算，提交到 PR 由 WP8 做。
- 仓库根目录的 `shared-docs/`：等第一篇页面正式接入时再建。

## 已知的坑

- 判断代码组时要处理列表中缩进 4 个以上空格的代码块：md2md 的标记识别不认它们，但 zdoc 判断类型时要认（技术设计 01 的已知局限）。
- 行号一律从 1 开始，与 md2md 的报错一致。
- 合成仓库的 commit 号是固定的，测试中可以直接写在期望里，但要从构建器返回的映射中取，不要手抄。
- 试点页还没做内容对齐，原文中没有变量与命名块；命名块与变量的测试用合成的小样例。
