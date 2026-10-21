# 01 命名块的解析

命名块的写法、两种类型、写法规则与网站上的表现见[产品需求场景 2](../prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段)。本篇定义工具怎样识别命名块与它的类型，以及各种写法错误对应的错误码。

**参与方**：md2md（解析、校验与清除，接口见 [03](./03-md2md-interfaces.md#命名块的解析与清除)）、zdoc 生成（识别命名块并按页面配置处理）、Milvus CI（PR 检查与发布）。

**状态**：由原接口设计迁入，待工程维护者完善。

## 约定

### 识别规则

- 标记是独占一行的 `<!-- doc:block:start id="<ID>" -->` 与 `<!-- doc:block:end id="<ID>" -->`。“独占一行”指：去掉行首、行尾的 ASCII 空格与 Tab 后，整行与标记完全相同；缩进四个空格或一个 Tab 的标记仍算标记，标记本身的写法（引号、ID）不放宽。
- 代码块中的标记不当作命名块，不报错，也不清除。代码块的边界按 CommonMark 判断：以三个及以上反引号或波浪线开头的行开始，以同类、长度不短于开始符的行结束；没有结束的代码块延续到文件末尾。zdoc 侧用同一个规则。
- 已知局限：识别不感知列表。列表项中缩进 4 个以上空格的代码块不当作代码块（milvus-docs `9acdc99` 中有 49 篇页面这样写），其中若写了标记，会被当作真标记。目前这些代码块中都没有标记；zdoc 判断代码组的类型与语言时（WP3）要考虑列表中的代码块。
- 类型由块内的结构决定，作者不声明：
  - 块内恰好是一个代码块，没有其他内容：**代码组**，单一语言。
  - 块内恰好是语言切换栏 `<div class="multipleCode">` 加紧跟其后的全部代码块，没有其他内容：**代码组**，多种语言。
  - 其他：**Markdown 块**。
- 代码组中每个代码块的语言取开头三个反引号后的语言名；同一个代码组中每种语言只有一个代码块。
- 切换栏与紧跟其后的代码块没有全部在同一个块内时报错（`BLOCK_PARTIAL_CODE_GROUP`），不往块外查找。
- 每次生成时重新扫描，得到**命名块清单**（ID、类型、语言、位置与摘要），不提交到仓库。

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

成对注释、不按标题定位、清除标记的产品取舍见[产品需求场景 2](../prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段)；不按标题或文档结构定位的依据见[差异定位调研](../../research/diff-locating-and-product-names.md)。

**为什么取消注册文件。** 本地样例的 `shared/modules.yaml` 为每篇原文起一个模块 ID，是为“一篇原文被多个 Cloud 页面引用”准备的：文件改名时只改一处。Phase 1 一篇原文只对应一个 Cloud 页面，改注册文件和改这一页的页面配置都只是改一处，这一层名字带不来好处，反而多一个共用文件。以后出现多页引用同一篇原文时，再加回注册层，已有页面不受影响。

</details>

## 验收

- **T01**：无命名块的整页可以正常扫描和生成；重复、空块、交叉、伪标记、嵌套和只包住代码组的一部分都报错。
- 加命名块前后 Milvus 侧输出逐字相同，见 [03](./03-md2md-interfaces.md#验收) 的 T11。
