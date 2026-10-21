# WP1 命名块的解析、校验与清除

**仓库**：md2md　**阶段**：Phase 1a　**依赖**：开工不依赖；合并前要完成 R1 ①（milvus-docs 固定 md2md 的版本，见[实现指南第 4 节](../README.md#4-工作包)）　**状态**：未开始

## 目标

md2md 能找出 Milvus 原文中的命名块、检查标记写法、在发布前把标记删掉。做完后：milvus-docs 的 PR 检查可以拦下写错的标记；`goover` 输出的 Milvus 页面中不再有标记；zdoc 可以调用同一套解析。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 2：规则、系统行为、出错时 | 标记的写法与报错 |
| [技术设计 01](../../design/01-named-blocks.md) | 全文 | 识别规则与错误码 |
| [技术设计 03](../../design/03-md2md-interfaces.md) | 命名块的解析与清除 | 函数签名、返回结构、命令行 |
| [实现指南](../README.md) | 2.1、2.2、2.7、2.8 节 | 需求清单、覆盖检查、契约用例、回归脚本 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新建 `src/blocks/`、`bin/md2md-blocks.js`、`test/blocks/`、`test/contract/cases/blocks/`、`test/spec/` | 变量、片段、Tab、Glossary 等现有插件的行为 |
| `index.js` 中 `goOver` 写文件前的一步：先检查、再清除 | `goover` 的其他默认行为 |
| `package.json`：`exports`、`bin`、Jest 与 Node 版本 | 发版流程（WP2 处理） |
| `.github/workflows/`：新增在 PR 上运行 `yarn test` 的工作流 | 现有的 `ci.yml` 发版步骤 |
| 根目录新建 `AGENTS.md`（实现指南第 5 节“Agent 的规则”） | |

## 接口

照[技术设计 03](../../design/03-md2md-interfaces.md#命名块的解析与清除)实现，保持 CommonJS：

```js
// src/blocks/index.js，经 package.json 的 exports 暴露为 "@zilliz/mdtomd/blocks.js"
parseBlocks(content, { sourceName, isFragment = false })
// → { ok, blocks: [{ id, startLine, endLine }], errors: [{ code, message, file, line }] }
stripBlockMarkers(content)   // → 删掉标记所在整行后的字符串
```

- `isFragment` 是本工作包新增的参数：为 `true` 时，任何标记都报 `BLOCK_IN_FRAGMENT`。命令行与 `goOver` 按路径是否在 `fragments/` 下传入。技术设计 03 要同步补上这个参数，在 PR 中提出即可，不要改设计仓库。
- 命令行：`md2md-blocks check <目录>`，检查目录下全部 `.md`，逐条输出 `文件:行号 错误码 说明`，有错误时退出码为 1。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| 命名块的 9 个错误码 | 每个错误码一个最小输入，断言 `code` 与 `line`；同一文件中的多个错误一次全部报出 |
| `2-1` | `goOver` 处理带标记的原文后，输出中没有 `doc:block`；代码块中的标记原样保留 |
| `2-2` | 同一篇原文加标记前后，`goOver` 的输出逐字相同；至少用三篇 milvus-docs 的真实页面（取 `9acdc99` 的试点页） |
| `2-3` | `md2md-blocks check` 遇到错误时退出码为 1，输出包含文件、行号、错误码 |
| `T01` | 无命名块的整页正常通过；重复、空块、交叉、伪标记、非法嵌套、只包住代码组的一部分都报错 |

另外：`test/contract/cases/blocks/` 中至少放 12 个契约用例（每个错误码一个，再加正常的单语言代码组、多语言代码组、Markdown 块各一个），格式见 实现指南 2.7 节。

做完后把 `2-1`–`2-3`、命名块错误码与 `T01` 从 `test/spec/pending.json` 中删掉；`1-2`–`1-5` 等留给 WP2。

## 完成的定义

- [ ] `yarn test` 全绿，含 `test/spec/coverage.test.js`
- [ ] 现有测试全部照常通过，没有改动现有测试的期望
- [ ] 在一份 milvus-docs `9acdc99` 的检出上，用 npm 上当前发布的 md2md 版本和本分支各运行一次 `goover`，输出逐字相同（实现指南 2.8 节的回归，此时原文中还没有标记）；PR 中写明运行的命令与比较结果
- [ ] 合并前确认 milvus-docs 已经固定了 md2md 的版本：md2md 合并到 master 会自动发版
- [ ] PR 说明按 [实现指南第 5 节](../README.md#pr-说明的格式)的格式写

## 不做

- 判断命名块的类型和语言（产品需求 2-5）：由 zdoc 在 WP3 中做。md2md 只需识别 `BLOCK_PARTIAL_CODE_GROUP` 所需的切换栏结构。
- 预处理入口、发版、Trusted Publishing：WP2 与 R1。
- 修改 milvus-docs 的 `check.yml`：md2md 发版并固定版本后，另开 milvus-docs 的 PR。

## 已知的坑

- md2md 最后一次提交在 2022 年，`ci.yml` 用 Node 14。新的测试工作流用 Node 22；Jest 26 在 Node 22 上能否运行要先确认，不行就升级 Jest，并在 PR 中说明。
- 加 `exports` 后，包内的其他路径不能再被深层引用。保留 `"."`，并在 PR 中确认 milvus-docs 与 web-content 只使用命令行（`goover`），没有深层引用。
- 标记必须独占一行，但技术设计 01 没有规定行首、行尾的空白算不算。开始实现前，在 PR 草稿中列出你的处理方式，等推动者确认。
- 代码块的边界按 CommonMark 判断：三个及以上反引号或波浪线开头的行都算，结束符要与开始符同类且不短于它。技术设计只写了“三个反引号”，按 CommonMark 实现，并在 PR 中注明；zdoc 侧以后用同一个规则。
