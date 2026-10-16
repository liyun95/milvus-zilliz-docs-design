# 07 站点适配

对应的产品需求见[产品需求场景 3](../prd.md#场景-3接入一页)（系统行为 3-4、3-5）与[场景 4](../prd.md#场景-4写-cloud-的差异)（系统行为 4-4、4-5）。本篇定义生成的最后一步：把完成变换、变量展开和产品过滤之后的 Milvus Markdown，转换成 Cloud 站点使用的 MDX（见[生成流水线](./README.md#生成流水线)）。

**参与方**：zdoc 生成（转换）、zdoc 维护者（维护 Tabs 规则）。

**状态**：骨架，待工程维护者补充。下文只汇总其他篇中已经确定的约束，标“待补”的部分尚未设计。

## 约定

### 输入与输出

- **输入**：一个版本的页面 Markdown，已经完成变换（[02](./02-page-config.md)）、变量与片段展开（[03](./03-md2md-interfaces.md#预处理)）、产品过滤；Cloud 内容文件已插入其中，写法与 Milvus 原文相同。
- **输出**：每个手册一份 MDX，再按 [04](./04-channels-and-lock.md#两个版本怎样合并成一页) 与另一个版本合并。
- 站点适配只负责 Tabs、提示组件、链接、图片和元数据，不为某种业务差异增加专门的处理。

### 代码 Tabs

- 由代码组中的代码块和 Tabs 规则重新生成，不使用语言切换栏 `<div class="multipleCode">` 的内容。
- 语言顺序、必选语言、默认语言，以及语言名与标签页显示名的对应（如 `javascript` 显示为 NodeJS、`bash` 显示为 cURL、`shell` 显示为 Zilliz CLI），由 Tabs 规则文件决定。
- 多语言代码组中切换语言用的 `#python`、`#java` 等锚点在这里处理，不当作链接。

**Tabs 规则文件 `shared-docs/presentation/cloud-sdk-tabs.yaml` 的格式**：待补。至少要表达上面列出的几项。

### 提示框等组件

Milvus 写法的提示框（如 `<div class="alert note">`）转换为 Cloud 的提示组件。对应关系：待补。

### 链接与图片

见 [02b](./02b-links-and-images.md)。

### front matter

作者只写 `page.yaml` 中的 `metadata`（见[产品需求场景 3](../prd.md#场景-3接入一页)），其余由工具生成：

| front matter | 生成方式 |
|---|---|
| `title`、`description` | 默认取原文的 `title`、`summary`，`metadata` 中写了就用它；按手册加后缀，如 `\| Cloud`、`\| BYOC` |
| `beta` | 取 `metadata.beta`，默认 `FALSE` |
| `slug` | `/` 加页面标识 |
| `sidebar_label`、`sidebar_position` | Phase 1 按飞书节点填写，见 [05b](./05b-cutover-and-ownership.md#导航phase-1) |
| `notebook`、`added_since`、`last_modified`、`deprecate_since` | 固定为 `FALSE` |
| `type` | `origin` |
| `displayed_sidebar` | `default` |
| `token` | `shared-<页面标识>`，见 [05](./05-publish-handoff.md#页面身份token) |
| `channel` | 整页只在一边存在时，由 `lock.yaml` 决定，见 [04](./04-channels-and-lock.md#只在一个通道存在的页面) |

### 其他 Milvus 语法

需要 Milvus 站点插件的标记（如 `{{tab}}`、`::glossary.`）在预处理时就报错（`UNSUPPORTED_MARK`，见 [03](./03-md2md-interfaces.md#出错时)）。其余 Milvus 特有的 HTML 或语法怎样处理：待补。

## 出错时

| 情况 | 结果 |
|---|---|
| 遇到无法转换的语法 | 该页生成失败（T06），具体范围待补 |
| Cloud 内容文件中手写了 `<Tabs>`、`<Admonition>` 等 Cloud 组件 | 该页生成失败，见 [02](./02-page-config.md#出错时) |
| 删除了 Tabs 规则要求必须有的语言或默认语言 | 该页生成失败，见 [02](./02-page-config.md#出错时) |

## 设计理由

<details>
<summary>展开设计理由</summary>

待补。Cloud 内容文件使用 Milvus 写法的产品理由见[产品需求场景 4](../prd.md#场景-4写-cloud-的差异)。

</details>

## 验收

- **T06**：Tabs 可切换、语言完整；锚点、导航、链接、图片和编辑入口正确；未知语法失败。
