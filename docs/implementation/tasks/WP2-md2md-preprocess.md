# WP2 只做预处理的入口与发版

**仓库**：[md2md](https://github.com/zilliztech/md2md)（随后一个 [milvus-docs](https://github.com/milvus-io/milvus-docs) 的 PR）　**阶段**：Phase 1a　**依赖**：WP1 已合并（[zilliztech/md2md#3](https://github.com/zilliztech/md2md/pull/3)，commit [`07855e4`](https://github.com/zilliztech/md2md/commit/07855e4b4fc29ddb1907af111f7630d25b20621b)）；[R1](../README.md#4-工作包) ① ② 已完成（milvus-docs [#3691](https://github.com/milvus-io/milvus-docs/pull/3691)–[#3694](https://github.com/milvus-io/milvus-docs/pull/3694)；npm 可信发布者）　**状态**：已合并（[zilliztech/md2md#4](https://github.com/zilliztech/md2md/pull/4)，commit [`a143b27`](https://github.com/zilliztech/md2md/commit/a143b27c475059f1fe22e84e074953b05bd9cd37)），1.3.0 已发布；合并之后的第 3、4 步待做

## 目标

做完后：

- zdoc 可以调用 md2md 的 `preprocess`，用 Cloud 的变量展开变量与片段，拿到依赖清单；
- md2md 发布 1.3.0，WP1 的命名块与本工作包的预处理一起上线；
- milvus-docs 升级到 1.3.0，PR 检查开始校验命名块标记。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 1：规则、系统行为 1-1 至 1-5、出错时 | 变量与片段的行为 |
| [技术设计 03](../../design/03-md2md-interfaces.md) | 预处理、出错时、例子、设计理由 | 函数签名、处理规则、返回结构、错误码 |
| [实现指南](../README.md) | 2.7、2.8、第 4 节的 R1、第 5 节 | 契约用例、回归脚本、发版顺序、规则 |
| [WP1 走读](../walkthroughs/WP1.md) | 全文 | 已有的代码结构，`src/blocks/` 的写法照着来 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新建 `src/preprocess/`、`test/preprocess/`、`test/contract/cases/preprocess/` | `goover` 的输出：处理 milvus-docs 时必须逐字不变 |
| `package.json`：`exports` 加 `./preprocess.js`；`version` 改为 `1.3.0` | `src/blocks/` 的行为 |
| `yarn.lock`：提交锁文件，`.gitignore` 中去掉它 | |
| `.github/workflows/`：删除 `ci.yml`（旧的 semantic-release 发版）；新建 `release.yml`；`test.yml` 改为按锁文件安装 | |
| `test/spec/pending.json`：删掉本工作包的编号 | `test/spec/requirements.json` |
| `test/blocks/regression.js`：只加一个参数，可以指定期望的 milvus-docs 提交，默认值不变（计划审阅时批准） | |
| `AGENTS.md`：PR 说明改为六个部分（计划审阅时批准） | |

## 接口

照[技术设计 03](../../design/03-md2md-interfaces.md#预处理)实现，保持 CommonJS：

```js
// src/preprocess/index.js，经 exports 暴露为 "@zilliz/mdtomd/preprocess.js"
preprocess({ content, fragmentRoot, variables, sourceName, limits })
// → { ok, content | null, dependencies: { fragments, variables }, errors, engine: { name, version } }
```

- 规则可以参考 [`src/helpers/File.js`](https://github.com/zilliztech/md2md/blob/07855e4b4fc29ddb1907af111f7630d25b20621b/src/helpers/File.js) 中现有的 `_replaceFragment`、`_replaceVariable`，但不要改动它们；`goover` 继续走原来的路径。
- `variables` 只用调用方传入的这一份，不按目录查找、不合并其他来源（产品需求 1-1）。
- 参数类型错误直接抛 `TypeError`，不放进 `errors`。
- `engine.version` 读自 `package.json`，不写死。

## 发版（`release.yml`）

| 项 | 要求 |
|---|---|
| 触发 | 只用 `workflow_dispatch` 手动触发，不在合并时自动发版 |
| 权限 | `contents: write`（打 tag）、`id-token: write`（Trusted Publishing） |
| 环境 | Node 22.14 及以上；先 `npm install -g npm@^11.15` |
| 步骤 | 按锁文件安装 → `yarn test` → 确认 `v<版本>` 的 tag 还不存在 → `npm stage publish` → 打 tag `v<版本>`、建 GitHub Release |
| 版本 | 取 `package.json` 中的 `version`，不在工作流中计算 |
| 不需要 | `NPM_TOKEN`、semantic-release |

npm 上的可信发布者已配置为 `zilliztech` / `md2md` / `release.yml`、只允许暂存发布（[实现指南第 4 节 R1 ②](../README.md#4-工作包)）。`npm stage publish` 之后，由推动者在 npmjs.com 上用双因素认证批准，版本才公开。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `1-2` | 正文、片段、代码块中的变量都替换；嵌套键 `{{var.a.b}}`、不区分大小写 |
| `1-3` | 变量值中含 `{{var.x}}` 或 `{{fragments/…}}` 时原样插入，不再展开 |
| `1-4` | `{{ doc.content }}` 等其他 `{{…}}` 原样保留 |
| `1-5` | 片段只能在 `<fragmentRoot>/fragments/` 之内；同一片段多次引用只读一次 |
| `T02` | 显式传入变量表；与 `goover` 现有的展开结果一致；缺少变量报错；两份不同的变量表并行调用互不串值；不运行 Milvus 站点插件（`{{tab}}` 等报 `UNSUPPORTED_MARK`） |
| `T03` | 嵌套与重复引用都记录在依赖中；循环、越界、符号链接、深度或体积超限都失败 |
| `T11` | 用 npm 上的 1.2.3 与本分支处理 milvus-docs [`v3.0.x`](https://github.com/milvus-io/milvus-docs/tree/v3.0.x) 最新提交的全部文档，输出逐字节相同；沿用 WP1 的 [`test/blocks/regression.js`](https://github.com/zilliztech/md2md/blob/07855e4b4fc29ddb1907af111f7630d25b20621b/test/blocks/regression.js) |
| 变量与片段的 8 个错误码 | 每个错误码一个契约用例，断言 `code`、`line`，循环引用断言 `detail` 中的引用链 |

做完后 `test/spec/pending.json` 应为空。

## 完成的定义

- [ ] `yarn test` 全绿，含编号覆盖检查；`pending.json` 为空
- [ ] 锁文件已提交，`test.yml` 用 `yarn install --frozen-lockfile`
- [ ] T11 回归：命令、milvus-docs 的提交、文件数与比较结果写在 PR 说明中
- [ ] `release.yml` 用 `actionlint` 检查通过；PR 中不触发发版
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写，包括 “How to try it”：用一个临时的 `fragments/` 目录和变量表调用 `preprocess`，展示成功与 `VAR_MISSING` 两种结果

**合并之后**（由推动者发起，Agent 协助）：

1. 推动者在 GitHub Actions 中手动运行 `release.yml`，再在 npmjs.com 上批准暂存的 1.3.0。
2. 发布后，用 npm 上的 1.3.0 再跑一次 T11 回归。
3. 给 milvus-docs 的 [`v3.0.x`](https://github.com/milvus-io/milvus-docs/tree/v3.0.x) 开 PR：三个工作流中的 `@zilliz/mdtomd@1.2.3` 升级为 `@1.3.0`；[`check.yml`](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/.github/workflows/check.yml) 中加一步 `md2md-blocks check site/en`（产品需求 2-3）。其他分支保持 1.2.3。
4. 第一次发版成功后，推动者把 npm 上的 Publishing access 改为禁止 bypass 令牌。

## 不做

- zdoc 侧的调用：由 WP3 接入。
- 产品过滤、站点适配：zdoc 的事。
- 改动 `goover` 的变量或片段规则。

## 已知的坑

- 现有的片段展开按目录查找变量、出错时只记日志不失败；`preprocess` 要全部收集错误并返回 `ok: false`，两套行为不能互相影响。
- 符号链接要逐段检查路径，不只检查最后的文件。
- 同一进程中并行调用：不要用模块级的可变状态保存变量表或已读片段。
- `npm stage publish` 需要 npm CLI 11.15.0 以上；`setup-node` 自带的 npm 版本可能不够，要显式升级。
