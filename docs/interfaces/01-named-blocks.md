# 01 命名块的定义与解析

Cloud 要替换、删除或补充 Milvus 原文中的某一段时，需要一个稳定的定位点。本篇定义这个定位点（命名块）在原文中怎样写，以及由谁解析、校验和清除。

**参与方**：milvus-docs 原文（写标记）、md2md（解析、校验与清除）、zdoc 生成（扫描并生成命名块清单）、Milvus CI（PR 检查与发布）。

**状态**：已定义，待文档负责人确认。

## 约定

### 标记写法

```markdown
<!-- doc:block:start id="before-you-start" -->
## Configure credentials
……
<!-- doc:block:end id="before-you-start" -->
```

- 标记必须独占一行。ID 由小写字母、数字和连字符组成，以字母或数字开头，在同一文件内唯一。
- 代码块（三个反引号围起的部分）中出现的标记只是普通文字，不识别也不清除，例如贡献说明中给出的写法示例。
- 首期不允许嵌套。
- 标记只能写在页面文件中，不能写在片段文件（`fragments/`）中。
- 只在需要差异处理的位置命名；无差异的页面整篇复用，不需要任何命名块。

### md2md 提供的能力

```js
import { parseBlocks, stripBlockMarkers } from "@zilliz/mdtomd/blocks.js";

const result = parseBlocks(content, { sourceName });
// { ok, blocks: [{ id, startLine, endLine }], errors: [{ code, message, file, line }] }

const output = stripBlockMarkers(content);   // 只删除标记所在的整行，其余不变
```

| 能力 | 使用方 | 行为 |
|---|---|---|
| `parseBlocks` | zdoc | 返回块的 ID 与起止行；错误一次收集全部 |
| `stripBlockMarkers` | zdoc、`goover` | 只删除代码块之外的标记行；`goover` 在写文件前对每篇文档执行，遇到错误时构建失败 |
| 命令行检查（如 `md2md-blocks check site/en`） | Milvus PR 检查（`check.yml`） | 检查全部页面与片段文件，有错误时以非零状态退出 |

这些能力随 1a 的 md2md 发版上线。同一篇原文加命名块前后，Milvus 侧的转换结果必须逐字相同。zdoc 在流水线第 ③ 步完成变换后清除标记，再调用 [03 md2md 预处理](./03-md2md-preprocess.md)。

### 共享来源配置

站点级一份，与页面目录同在 `shared-docs/` 中（见 [02 共享页配置](./02-page-config.md)）：

```yaml
# shared-docs/source.yaml
schema_version: 1
repository: https://github.com/milvus-io/milvus-docs
track: v3.0.x          # 跟踪分支，见 04
```

### 命名块清单与块的类型

zdoc 扫描源文件后，在内部得到每页的命名块清单：块 ID、类型、语言、所在行和内容摘要。它供 [02](./02-page-config.md) 校验变换目标、[05](./05-publish-handoff.md) 写入记录文件、[06](./06-upstream-changes.md) 比较上游变化。清单的具体结构在实现时确定；写入记录文件 与影响报告的部分在 05、06 中定义。

块的类型由内容决定：块的内容恰好是一个代码组（`<div class="multipleCode">` 加连续的代码块，或单个代码块）时为**代码组**，可以按语言或代码行做变换；否则为 **Markdown 块**，只能整块变换。

## 出错时

| 错误码 | 何时出现 |
|---|---|
| `BLOCK_DUPLICATE_ID` | 同一文件中 ID 重复 |
| `BLOCK_UNCLOSED` / `BLOCK_UNMATCHED_END` | 有开始没有结束，或有结束没有开始 |
| `BLOCK_CROSSED` | 结束标记的 ID 与当前打开的块不一致 |
| `BLOCK_NESTED` | 块内又出现开始标记 |
| `BLOCK_EMPTY` | 块内没有内容 |
| `BLOCK_MALFORMED` | 代码块之外出现格式不对的标记，例如 ID 没加引号、含大写字母，或与正文写在同一行 |
| `BLOCK_IN_FRAGMENT` | 片段文件中出现标记 |

在 Milvus 侧，这些错误让 PR 检查失败；在 zdoc 侧，让该页生成失败。命名块被改名或删除后，引用它的页面怎样处理见 [06](./06-upstream-changes.md)。

## 例子

<details>
<summary>Delete Entities（1a）与 OpenAI（1b）</summary>

Delete Entities 没有命名块，扫描结果为整页、无块，可以正常接入。

OpenAI 在内容对齐时加两个命名块：

````markdown
<!-- doc:block:start id="before-you-start" -->
## Configure credentials
……
<!-- doc:block:end id="before-you-start" -->
……
<!-- doc:block:start id="define-function-code" -->
```python
……
```
<!-- doc:block:end id="define-function-code" -->
````

命名块清单中，`before-you-start` 是 Markdown 块，`define-function-code` 是代码组，语言为 python。Milvus 侧的输出与不加标记时逐字相同。

</details>

## 设计理由

**为什么用成对的注释。** 成对的开始、结束标记加名字，是 AsciiDoc（`tag::名字[]` / `end::名字[]`）和 MkDocs Snippets（`[start:名字]` / `[end:名字]`）的通行做法；用 HTML 注释，是因为 Markdown 中只有注释在 milvus.io 上不显示。这里比两者更严格：

- **必须独占一行**：Markdown 靠空行和行首符号划分段落与表格，标记夹在一行中间可能切断它们。
- **不允许嵌套**：让 [02](./02-page-config.md) 中的冲突规则保持简单。
- **写错一律报错**：Cloud 页面依赖这些标记生成，问题要尽早暴露。

不按标题或文档结构定位，原因见[差异定位调研](../../research/diff-locating-and-product-names.md)：标题会改名（milvus-docs 一年内有 17% 的候选页改过或删过标题），按结构定位可能找到错误的位置而不报错。

**为什么放在 md2md。** md2md 与 zdoc 都是公开仓库，但 zdoc 是大型 monorepo，不适合让 Milvus CI 依赖。规则只实现一次，zdoc 与 Milvus 对“标记是否写对”的判断不会出现分歧。

**为什么在 1a 上线。** T01“注册与扫描”属于 1a，解析代码 1a 就要可用；清除能力随同一版本进入 Milvus CI，带命名块的原文就不必等 1b。milvus-docs 目前没有命名块，加入校验不会牵出历史问题。

**为什么仍要清除标记。** milvus.io 会把 HTML 注释原样留在页面源码中，读者看不到。但不清除的话，web-content 的 Markdown 和提供给大模型读取的内容中都会出现这些注释；清除后还能用“加标记前后输出逐字相同”作为可自动检查的验收标准。

**为什么取消注册文件。** 本地样例的 `shared/modules.yaml` 为每篇原文起一个模块 ID，是为“一篇原文被多个 Cloud 页面引用”准备的：文件改名时只改一处。首期一篇原文只对应一个 Cloud 页面，改注册文件和改这一页的页面配置都只是改一处，这一层名字带不来好处，反而多一个共用文件。以后出现多页引用同一篇原文时，再加回注册层，已有页面不受影响。

## 验收

- **T01**：无命名块的整页可以接入；重复、空块、交叉、伪标记和嵌套都报错。
- **T11**：加命名块前后 Milvus 侧输出逐字相同，没有标记残留。
