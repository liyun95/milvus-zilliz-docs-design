# WP1 走读：命名块的解析、校验与清除

**仓库**：md2md　**上游 PR**：[zilliztech/md2md#3](https://github.com/zilliztech/md2md/pull/3)　**任务卡**：[WP1](../tasks/WP1-md2md-named-blocks.md)

## 解决什么问题

Milvus 作者会在原文中加这样的标记，让 Cloud 能说“替换这一节”（[产品需求场景 2](../../prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段)）：

```markdown
<!-- doc:block:start id="before-you-start" -->
## Configure credentials
…
<!-- doc:block:end id="before-you-start" -->
```

md2md 要对它们做两件事：**检查写得对不对**；在 milvus.io 发布之前**把它们删掉**，网站上不留痕迹。

## 文件地图

| 文件 | 做什么 |
|---|---|
| `src/blocks/scan.js` | 逐行读，标出哪些行在代码示例中、哪些行像标记；找出多语言代码组 |
| `src/blocks/index.js` | `parseBlocks`：配对开始与结束标记，收集全部错误；`stripBlockMarkers`：删掉标记行 |
| `src/blocks/files.js` | 读整个目录、判断哪些文件是片段；只有这里读文件，上面两个文件是纯计算 |
| `bin/md2md-blocks.js` | 命令行 `md2md-blocks check <目录>`，供 milvus-docs 的 PR 检查使用 |
| `index.js` | 接进现有的 `goover`：转换前先检查整个目录，写文件前删掉标记 |
| `test/blocks/`、`test/contract/cases/blocks/` | 测试与 15 个契约用例（zdoc 以后会复用这些用例） |

## 代码怎样工作

1. **逐行读**（`scan.js`）。每一行记下两件事：
   - 是否在代码示例中（三个以上反引号或波浪线围起的部分）。代码示例中的标记只是示例文字，不检查也不删。
   - 是否像标记。先宽松地找含 `<!-- doc:block` 的行，再判断去掉行首行尾的空格和 Tab 后，是不是**一字不差**的标记。
2. **配对**（`parseBlocks`）。按顺序处理每个标记，记下当前打开的块：

   | 遇到 | 情况 | 结果 |
   |---|---|---|
   | 开始标记 | 已有打开的块 | `BLOCK_NESTED` |
   | 开始标记 | ID 用过了 | `BLOCK_DUPLICATE_ID` |
   | 结束标记 | 没有打开的块 | `BLOCK_UNMATCHED_END` |
   | 结束标记 | ID 与打开的块不同 | `BLOCK_CROSSED` |
   | 文件结束 | 还有块没关 | `BLOCK_UNCLOSED` |
   | 块关闭时 | 块内没有内容 | `BLOCK_EMPTY` |
   | 像标记的行 | 写法不对，如与标题写在同一行、ID 有大写 | `BLOCK_MALFORMED` |
   | 任何标记 | 文件在 `fragments/` 下 | `BLOCK_IN_FRAGMENT` |

3. **检查代码组**（`codeGroups`）。找出每个多语言代码组（切换栏 `<div class="multipleCode">` 加紧跟的代码块），命名块只包住其中一部分时报 `BLOCK_PARTIAL_CODE_GROUP`。
4. **返回结果**：要么“没问题，这是各个块和它们的行号”，要么一次列出全部错误，每个都有文件、行号和原因。有错误时不返回部分结果。
5. **删除标记**（`stripBlockMarkers`）。只删标记所在的整行，其余每个字节都不动，所以 Milvus 的输出逐字不变。
6. **接进构建**（`index.js`）。`goover` 转换之前先检查整个文档目录，有错误就让 Milvus 的构建失败；没有错误时，写每个页面之前删掉标记。

## 一个例子走一遍

两篇页面和一个片段，一好两坏：

<details>
<summary>输入文件</summary>

`site/en/good.md`：

```markdown
# Good page

<!-- doc:block:start id="before-you-start" -->
## Configure credentials
Set your API key.
<!-- doc:block:end id="before-you-start" -->

Shared text.
```

`site/en/bad.md`：

```markdown
# Bad page

<!-- doc:block:start id="setup" -->
## Setup
<!-- doc:block:start id="inner" -->
Text.
<!-- doc:block:end id="inner" -->
<!-- doc:block:end id="setup" -->

## Another <!-- doc:block:start id="Wrong" -->

<!-- doc:block:start id="setup" -->
Duplicate ID, never closed.
```

`site/en/fragments/shared.md`：

```markdown
<!-- doc:block:start id="x" -->
```

</details>

检查整个目录：

```
site/en/bad.md:5 BLOCK_NESTED Block "inner" starts inside block "setup".
site/en/bad.md:10 BLOCK_MALFORMED Expected a standalone <!-- doc:block:start|end id="lowercase-id" --> marker.
site/en/bad.md:12 BLOCK_DUPLICATE_ID Duplicate block ID "setup".
site/en/bad.md:12 BLOCK_UNCLOSED Block "setup" has no end marker.
site/en/fragments/shared.md:1 BLOCK_IN_FRAGMENT Named block markers are not allowed in fragments.
```

五处错误一次报出，命令以退出码 1 结束；在 milvus-docs 中，这会让 PR 检查或构建失败。

解析好的那篇，结果是 `{"ok":true,"blocks":[{"id":"before-you-start","startLine":3,"endLine":6}],"errors":[]}`。删除标记后，两行标记消失，其余各行与原文一致：

```markdown
# Good page

## Configure credentials
Set your API key.

Shared text.
```

## 自己试一试

需要 Node 22 以上。WP1 合并到上游之前，在 Agent 的工作树中运行；合并之后，在 `~/md2md` 中 `git pull` 后运行。

```bash
cd ~/worktrees/md2md/wp1-named-blocks
```

1. 跑全部测试，应看到 83 个通过：

   ```bash
   yarn test
   ```

2. 把上面的三个输入文件放进一个临时目录（如 `/tmp/demo/site/en/`），然后检查它：

   ```bash
   node bin/md2md-blocks.js check /tmp/demo/site
   ```

3. 改动一个文件，例如把 `bad.md` 中的 `id="Wrong"` 改成小写，并单独放一行，再检查一次，看错误怎样变少。

## 值得读的测试

测试名中方括号里的是需求编号；读测试名就能知道代码承诺了什么。

| 文件 | 看什么 |
|---|---|
| `test/blocks/parser.test.js` | 每种错误、代码示例中的标记、代码组的边界 |
| `test/blocks/integration.test.js` | 命令行与 `goover` 的行为：失败时报原始行号、只删标记 |
| `test/contract/cases/blocks/*.json` | 15 个“输入 → 期望结果”的样例，最容易读 |

## 刻意没做的

- **判断命名块的类型和语言**：由 zdoc 做（WP3）。md2md 只认得出代码组的边界，用来报 `BLOCK_PARTIAL_CODE_GROUP`。
- **列表中的代码块**：缩进 4 个以上空格的代码块不当作代码示例，是已知局限，见[技术设计 01](../../design/01-named-blocks.md#识别规则)。
- **发新版本**：WP2 与 R1 负责。在那之前，milvus-docs 固定使用 1.2.3，WP1 不会进入 Milvus 的构建。

## 证据

用 npm 上的 1.2.3 与本分支分别处理 milvus-docs `9acdc99` 的全部文档，两份输出都是 506 个文件，逐字节相同；给三篇试点页加上标记后再处理，输出仍然相同（产品需求 2-2，验收 T11 的一部分）。
