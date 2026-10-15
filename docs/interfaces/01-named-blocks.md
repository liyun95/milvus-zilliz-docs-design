# 01 命名块的定义与解析

Cloud 要替换、删除或补充 Milvus 原文中的某一段时，需要一个稳定的定位点。本篇定义这个定位点（命名块）在原文中怎样写、分哪两类、什么算写错。

**参与方**：milvus-docs 原文（写标记）、md2md（解析、校验与清除，接口见 [03](./03-md2md-interfaces.md#命名块的解析与清除)）、zdoc 生成（识别命名块并按页面配置处理）、Milvus CI（PR 检查与发布）。

**状态**：已定义，待文档负责人确认。

## 约定

### 两种命名块

用一对 HTML 注释把原文中的一段包起来，就是一个命名块。命名块按包住的内容分两种，类型决定 Cloud 能把这一块改得多细（变换写法见 [02](./02-page-config.md#变换)）。

#### Markdown 块

包住任意一段 Markdown，例如一节标题和正文、几个段落、一个列表：

```markdown
<!-- doc:block:start id="before-you-start" -->
## Configure credentials
……
<!-- doc:block:end id="before-you-start" -->
```

Cloud 只能整块替换、删除，或在块的前后添加内容。

#### 代码组

只包住示例代码，不包说明文字。按原文中代码的样子分两种情况：

**情况一：只有一种语言。** 原文中就是一个单独的代码块，没有切换栏。直接包住这个代码块：

````markdown
<!-- doc:block:start id="install-cmd" -->
```shell
pip install pymilvus
```
<!-- doc:block:end id="install-cmd" -->
````

**情况二：多种语言。** milvus-docs 中的多语言代码由语言切换栏 `<div class="multipleCode">` 和紧跟其后的各语言代码块组成，milvus.io 上显示为可以切换的标签页。标记要把**切换栏和全部代码块**一起包住：

````markdown
<!-- doc:block:start id="delete-code" -->
<div class="multipleCode">
    <a href="#python">Python</a>
    <a href="#java">Java</a>
</div>

```python
client.delete(collection_name="quick_setup", ids=[0, 1, 2])
```

```java
// ……
```
<!-- doc:block:end id="delete-code" -->
````

两种情况下，Cloud 除了整块替换、删除或在前后添加，还可以只改其中某种语言（包括增删语言），或某种语言中的某几行。包的时候注意：

- **多种语言时，切换栏必须在块内。** 切换栏和后面的代码块是一个整体，块的边界要与它一致：工具不用往块外查找，整块删除或替换时也不会在块外留下孤立的切换栏。Cloud 的标签页由工具按代码块和 Tabs 规则重新生成，不使用切换栏的内容。
- **只包代码，不包说明文字。** 把前后的说明文字也包进去，这一块就成了 Markdown 块，只能整块处理。
- **不能只包一部分。** 只包了其中几个代码块，或包了代码块却漏了切换栏，都报错（`BLOCK_PARTIAL_CODE_GROUP`）：否则整块删除或替换后，会留下没有代码的切换栏，或没有切换栏的代码。

<details>
<summary>报错的包法</summary>

只包了 Python 代码块，切换栏和 Java 代码块在块外：

````markdown
<div class="multipleCode">
……
</div>

<!-- doc:block:start id="delete-python" -->
```python
……
```
<!-- doc:block:end id="delete-python" -->

```java
……
```
````

</details>

### 标记的写法规则

两种命名块都遵守：

- 标记必须独占一行。ID 由小写字母、数字和连字符组成，以字母或数字开头，在同一文件内唯一。
- 写在代码块（三个反引号围起的示例代码）中的标记不算数：工具不把它当作命名块，不报错，也不清除，页面上原样显示。这样文档才能展示标记本身的写法，例如 Milvus 贡献说明中教人写命名块的示例。
- 首期不允许嵌套。
- 标记只能写在页面文件中，不能写在片段文件（`fragments/`）中。
- 只在需要差异处理的位置命名；无差异的页面整篇复用，不需要任何命名块。

### 写错时与网站上的表现

| 写原文的人关心的 | 结果 |
|---|---|
| 写错了在哪里发现 | milvus-docs 的 PR 检查失败，PR 不能合并；万一漏过，Cloud 这一页生成失败（见[出错时](#出错时)） |
| 标记会不会出现在网站上 | 不会。Milvus 发布和 Cloud 生成时都会清除标记；同一篇原文加命名块前后，Milvus 侧的输出逐字相同 |

标记的解析、检查与清除都由 md2md 提供，Milvus 与 Cloud 两端用同一套规则；milvus-docs 的 CI 与 zdoc 在哪一步调用，见 [03](./03-md2md-interfaces.md#命名块的解析与清除)。

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
| `BLOCK_PARTIAL_CODE_GROUP` | 只包住多语言代码组的一部分：切换栏与紧跟其后的代码块没有全部在同一个块内 |

在 Milvus 侧，这些错误让 PR 检查失败，漏过时构建也会失败；在 zdoc 侧，让该页生成失败。命名块被改名或删除后，引用它的页面怎样处理见 [06](./06-upstream-changes.md)。

## 例子

<details>
<summary>Delete Entities（1a）与 OpenAI（1b）</summary>

Delete Entities 没有命名块，扫描结果为整页、无块，可以正常生成。

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

工具识别出 `before-you-start` 是 Markdown 块，`define-function-code` 是代码组，语言为 python。Milvus 侧的输出与不加标记时逐字相同。

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么用成对的注释。** 成对的开始、结束标记加名字，是 AsciiDoc（`tag::名字[]` / `end::名字[]`）和 MkDocs Snippets（`[start:名字]` / `[end:名字]`）的通行做法；用 HTML 注释，是因为 Markdown 中只有注释在 milvus.io 上不显示。这里比两者更严格：

- **必须独占一行**：Markdown 靠空行和行首符号划分段落与表格，标记夹在一行中间可能切断它们。
- **不允许嵌套**：让 [02](./02-page-config.md) 中的冲突规则保持简单。
- **写错一律报错**：Cloud 页面依赖这些标记生成，问题要尽早暴露。

不按标题或文档结构定位，原因见[差异定位调研](../../research/diff-locating-and-product-names.md)：标题会改名（milvus-docs 一年内有 17% 的候选页改过或删过标题），按结构定位可能找到错误的位置而不报错。

**为什么仍要清除标记。** milvus.io 会把 HTML 注释原样留在页面源码中，读者看不到。但不清除的话，web-content 的 Markdown 和提供给大模型读取的内容中都会出现这些注释；清除后还能用“加标记前后输出逐字相同”作为可自动检查的验收标准。

**为什么取消注册文件。** 本地样例的 `shared/modules.yaml` 为每篇原文起一个模块 ID，是为“一篇原文被多个 Cloud 页面引用”准备的：文件改名时只改一处。首期一篇原文只对应一个 Cloud 页面，改注册文件和改这一页的页面配置都只是改一处，这一层名字带不来好处，反而多一个共用文件。以后出现多页引用同一篇原文时，再加回注册层，已有页面不受影响。

</details>

## 验收

- **T01**：无命名块的整页可以正常扫描和生成；重复、空块、交叉、伪标记、嵌套和只包住代码组的一部分都报错。
- 加命名块前后 Milvus 侧输出逐字相同，见 [03](./03-md2md-interfaces.md#验收) 的 T11。
