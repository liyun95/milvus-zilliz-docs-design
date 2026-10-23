# 07 站点适配

对应的产品需求见[产品需求场景 1](../prd.md#场景-1把产品名和连接值写成变量)（系统行为 1-6）、[场景 3](../prd.md#场景-3接入一页)（系统行为 3-4、3-5）与[场景 4](../prd.md#场景-4写-cloud-的差异)（系统行为 4-4、4-5）。本篇定义生成的最后一步：把完成变换、变量展开和产品过滤之后的 Milvus Markdown，转换成 Cloud 站点使用的 MDX（见[生成流水线](./README.md#生成流水线)），再检查其中有没有漏换的产品名。

**参与方**：zdoc 生成（转换）、zdoc 维护者（维护 Tabs 规则）。

**状态**：草稿，待工程维护者确认。依据 milvus-docs `v3.0.x` 的 [`1997ce9`](https://github.com/milvus-io/milvus-docs/tree/1997ce96782b31f8628f22d31fad11007e4b924b)、zdoc 现有的飞书转换代码和本地原型（[Filtered Search](../../examples/filtered-search/build_example.py)）。

## 约定

### 输入与输出

- **输入**：一个版本、一个手册的页面 Markdown，已经完成变换（[02](./02-page-config.md)）、变量与片段展开（[03](./03-md2md-interfaces.md#预处理)）、产品过滤；Cloud 内容文件已插入其中，写法与 Milvus 原文相同；链接与图片已按 [02b](./02b-links-and-images.md) 改写。
- **输出**：一份 MDX，再按 [04](./04-channels-and-lock.md#两个版本怎样合并成一页) 与另一个版本合并。
- 站点适配只负责 Tabs、提示组件、front matter 和 MDX 兼容，不为某种业务差异增加专门的处理。
- 只转换下文列出的写法；其余照原样输出，由 zdoc 现有的 MDX 校验与试构建检查（见 [05](./05-publish-handoff.md#发布保护)）。

### 代码 Tabs

每个多语言代码组（[01](./01-named-blocks.md#识别规则)）按 Tabs 规则重新生成一组 `<Tabs>`，不使用语言切换栏 `<div class="multipleCode">` 的内容；不在代码组中的代码块照原样输出。

````mdx
<Tabs groupId="code" defaultValue="python" values={[{"label":"Python","value":"python"},{"label":"Java","value":"java"}]}>
<TabItem value="python">

```python
client.delete(collection_name="quick_setup", ids=[0, 1, 2])
```

</TabItem>
<TabItem value="java">
……
</TabItem>
</Tabs>
````

- 标签页的顺序按 Tabs 规则中 `languages` 的顺序，只输出代码组中实际有的语言。
- `defaultValue` 取规则中的 `default`；代码组中没有这种语言时，取规则顺序中的第一种。
- 代码块的语言名先按规则中的 `aliases` 换成 Cloud 的值，再输出到 `<TabItem value>` 与代码块的语言名。
- 只有一种语言的代码组输出普通代码块，不加 `<Tabs>`，与 zdoc 现有页面一致；Cloud 给它增加语言后，按多种语言输出。

**Tabs 规则文件** `shared-docs/presentation/cloud-sdk-tabs.yaml`，全站一份，由 zdoc 维护者修改：

```yaml
schema_version: 1
group_id: code              # <Tabs groupId>，同一页的代码组同步切换
default: python             # 默认显示的语言
languages:                  # 顺序即标签页顺序
  - value: python           # Cloud 的语言值，用于 <TabItem value> 和代码块语言名
    label: Python           # 标签页上显示的名字
    required: true          # 每个多语言代码组都必须有
  - value: java             # 不写 required：原文有就显示，没有就不显示
    label: Java
  - value: go
    label: Go
  - value: rust
    label: Rust
  - value: c++
    label: C++
    aliases: [cpp]          # Milvus 原文中的语言名
  - value: javascript
    label: NodeJS
  - value: bash
    label: cURL
    aliases: [curl]
  - value: shell
    label: Zilliz CLI
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `schema_version` | 是 | 固定为 `1` |
| `group_id` | 是 | 输出到 `<Tabs groupId>` |
| `default` | 是 | 默认显示的语言，必须是 `languages` 中的一个 `value` |
| `languages[].value` | 是 | Cloud 的语言值，不能重复 |
| `languages[].label` | 是 | 标签页上显示的名字 |
| `languages[].aliases` | 否 | Milvus 原文中对应的语言名；变换中的 `language` 写原文的语言名，也可以写 `value` |
| `languages[].required` | 否 | 默认 `false`；为 `true` 时，每个多语言代码组都必须有这种语言 |

Phase 1 的取值是推动者的建议，待文档负责人确认（见[Phase 1 实施计划第 6.1 节](../phase-1.md#61-待确认的接口)）：只有 Python 必须有；其他语言原文有就显示、没有就不显示，包括 C++。语言顺序与显示名沿用本地原型，加上 `aliases`。

### 提示框

milvus-docs 中提示框的写法与数量（`1997ce9`）：

| Milvus 写法 | 次数 | 转换为 |
|---|---|---|
| `<div class="alert note">` | 463 | `<Admonition type="info" icon="📘" title="Notes">`，与 zdoc 现有的飞书提示框一致 |
| `<div class="alert warning">` | 18 | `<Admonition type="warning" icon="🚧" title="Warning">`，与 zdoc 现有页面一致 |
| `alert notes`、`alert alert-info`、`admonition note` | 各 1 | 不转换，该页生成失败，回上游改成 `alert note` |

- 提示框内的 Markdown 照常转换；结束标记 `</div>` 换成 `</Admonition>`。
- 提示框中嵌套代码组或另一个提示框时，照同样规则转换。
- 输出 MDX 的开头按用到的组件加入 `import`：`Admonition`、`Tabs`、`TabItem`。

### MDX 兼容

Milvus 原文按 Markdown 写，直接作为 MDX 编译可能出错。站点适配沿用 zdoc 现有的 MDX 修补模块（`mdx-parse`），至少处理：

- 未闭合的空元素，如 `<br>`、`<img ...>`，改为自闭合；
- 正文中会被 MDX 当作表达式的 `{`、`}` 与 `<`，在代码块之外转义；
- HTML 的 `class` 属性按 zdoc 现有页面的写法处理。

修补后仍不能编译的，该页生成失败，不静默删除内容。

### front matter

作者只写 `page.yaml` 中的 `metadata`（见[产品需求场景 3](../prd.md#场景-3接入一页)），其余由工具生成：

| front matter | 生成方式 |
|---|---|
| `title`、`description` | 默认取原文的 `title`、`summary`，`metadata` 中写了就用它；按手册加后缀：`guides` 加 `\| Cloud`，`guides-byoc` 加 `\| BYOC`。规则与 zdoc 飞书转换器中的 `__title_suffix`（`packages/docs-tooling/src/lark/larkDocWriter.js`）相同，生成结果与现有页面一致 |
| `beta` | 取 `metadata.beta`，默认 `FALSE`。可选的值读 zdoc 的标签定义（`packages/docs-ui/src/shared/utils/docHeadingTags.ts` 中的 `DOC_HEADING_TAGS`），去掉标手册的 `BYOC`，不在工具中另写一份 |
| `slug` | `/` 加页面标识 |
| `sidebar_label`、`sidebar_position` | Phase 1 按飞书节点填写，见 [05b](./05b-cutover-and-ownership.md#导航phase-1) |
| `notebook`、`added_since`、`last_modified`、`deprecate_since` | 固定为 `FALSE` |
| `type` | `origin` |
| `displayed_sidebar` | `default` |
| `token` | `shared-<页面标识>`，见 [05](./05-publish-handoff.md#页面身份token) |
| `channel` | 整页只在一边存在时，由飞书表格的 `Release Channel` 决定，见 [04](./04-channels-and-lock.md#只在一个通道存在的页面) |

原文 front matter 中的其他字段（如 Milvus 的 `beta`、`id`）不输出。

### 标题锚点

每个标题都输出显式的锚点 `{#id}`，`id` 用 zdoc 飞书转换器相同的算法：`slugify(标题文字, { lower: true, strict: true })`（`packages/docs-tooling/src/lark/larkDocWriter.js` 的 `__heading_slug`，复用同一个函数，不另写一份）。这样迁移后与飞书版相同的标题锚点不变，链接换算（[02b](./02b-links-and-images.md#锚点)）也能算出确定的结果。

- 计算前去掉标题中的 Markdown 标记与 HTML，与飞书转换器的 `__clean_headings` 相同。
- 同一页中有几个标题算出相同的锚点时，第一个不变，之后的依次加 `-1`、`-2`，与 Docusaurus 自动生成锚点的做法相同。User Guide 的 201 篇中有 4 篇有重复的标题，如 `set-collection-ttl.md`。链接换算时，Milvus 的锚点对应到几个标题的，取第一个，与浏览器的行为一致。

### 其他 Milvus 语法

需要 Milvus 站点插件的标记（如 `{{tab}}`、`::glossary.`）在预处理时就报错（`UNSUPPORTED_MARK`，见 [03](./03-md2md-interfaces.md#出错时)）。Milvus 站点专用的版式 `div`，如 `start_card_container`、`card-wrapper`、`filter`，只出现在首页、安装选择页等非 User Guide 页面，Phase 1 不转换；共享页中出现时，该页生成失败。

### 产品名检查

每个版本、每个手册的 MDX 生成后、两版合并前，按 `shared-docs/product-names.yaml` 检查一遍：

- **检查什么**：`check` 中的每一项，在正文与代码块中按整词匹配，区分大小写。`MilvusClient`、`pymilvus`、`milvus.yaml` 这类更长的词中出现的 Milvus 不算命中；链接与图片地址、front matter 不检查。
- **放过什么**：命中的位置落在 `allow` 中某个短语之内时放过。`allow` 只接受包含空格的短语，不接受单个词。
- **报在哪里**：报错指出页面、版本和手册，并按变换前的位置映射回原文的文件与行号；命中在 Cloud 内容文件中时，指向内容文件。
- **怎样找回位置**：是否失败只看生成的 MDX。对 MDX 中命中的每种写法，再到这一版本用到的输入中按同样的规则查找：Cloud 内容文件、原文、用到的片段、用到的变量的值；每处没被放过的位置报一条错，MDX 中的行号放在 `detail` 中。输入中都找不到时（写法来自站点适配），报在页面原文上，不给行号。变换接入后，原文中被替换或删除的范围不再查找。
- **milvus-docs 侧**：milvus-docs 的 PR 检查用同一套规则只给提示、不拦截，因为它不知道哪些页面是共享页。规则文件从 zdoc 读取还是在 milvus-docs 中另放一份，由实现决定。

## 出错时

| 情况 | 结果 |
|---|---|
| 代码组中有规则中没有的语言（换算 `aliases` 之后），包括多语言代码组中没写语言名的代码块 | 该页生成失败，提示在 Tabs 规则中补充，或用变换删除这种语言 |
| 同一个多语言代码组中一种语言出现两次 | 该页生成失败（`ADAPT_UNSUPPORTED_MARKUP`），回上游合并或删除重复的代码块 |
| 多语言代码组缺少 `required` 的语言 | 该页生成失败，提示用变换补上，或回上游补齐 |
| Tabs 规则文件格式不对：`value` 重复，`default` 不在 `languages` 中 | 所有共享页生成失败 |
| 提示框写法不在上表中；出现 Milvus 站点专用的版式 `div` | 该页生成失败 |
| MDX 修补后仍不能编译 | 该页生成失败 |
| Cloud 内容文件中手写了 `<Tabs>`、`<Admonition>` 等 Cloud 组件 | 该页生成失败，见 [02](./02-page-config.md#出错时) |
| 生成的页面中出现 `check` 中的写法，且不在 `allow` 中 | 该页生成失败，提示回 milvus-docs 改成变量，或在 `allow` 中补一行 |
| `product-names.yaml` 格式不对，或 `allow` 中有单个词 | 所有共享页生成失败 |

## 例子

<details>
<summary>Filtered Search 的一个代码组（本地原型）</summary>

原文的标准过滤代码组有 Python、Java、Go、NodeJS、cURL 等语言；页面配置给它加了 `shell`（Zilliz CLI）。生成结果中，`<Tabs>` 按规则顺序列出八种语言，`shell` 排在最后；原文中的 `<div class="alert note">` 转为 `<Admonition type="info" ...>`。完整输出见 [filtered-search.mdx](../../examples/filtered-search/generated/filtered-search.mdx)。

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么重新生成 Tabs，不转换切换栏。** 切换栏只是链接列表，内容和顺序都由 Milvus 维护；Cloud 的标签页顺序、显示名和必选语言是 Cloud 自己的站点规则。从代码块重新生成，Cloud 增删语言（[02](./02-page-config.md)）后也不用维护切换栏。

**为什么要 `aliases`。** milvus-docs 中 C++ 的代码块写 `cpp`（68 处），zdoc 页面中写 `c++`；cURL 多数写 `bash`，也有 8 处写 `curl`。作者在变换中按原文写语言名，输出时统一换成 Cloud 的值。

**为什么提示框沿用 zdoc 现有样式。** zdoc 现有页面的提示框写作 `<Admonition type="info" icon="📘" title="Notes">` 与 `<Admonition type="warning" icon="🚧" title="Warning">`（zdoc master `b832f16` 的 Guides 中，后者有 15 处）。共享页沿用同样的输出，两种来源的页面看起来一致。

**为什么不认识的写法直接失败。** 原样输出可能编译通过，却在页面上显示成乱码或空白，审核时容易漏掉。

</details>

## 验收

- **T06**：Tabs 可切换、语言完整；锚点、导航、链接、图片和编辑入口正确；未知语法失败。
- **T14**：漏换的产品名与连接值在两个版本中都能查出；`allow` 中的短语与更长的词不误报；报错位置指回原文或内容文件。
