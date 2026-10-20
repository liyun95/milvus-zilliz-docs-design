# 共享页写法速查

**状态**：草稿，待确认。

本文是[Phase 1 产品需求](./prd.md)的附录，把文档工程师要写的文件、字段和可能遇到的错误汇总成速查表，供写作时查找。各项规则、例子与理由以产品需求中的对应场景为准；两处不一致时，以产品需求为准。

`examples/` 中的两篇样例仍是接口定义之前的草案写法，待确认后更新。

## 1. 文件

| 文件 | 位置 | 谁写 | 规则见 |
|---|---|---|---|
| 共享原文 | milvus-docs | 文档工程师、社区贡献者 | [场景 1](./prd.md#场景-1把产品名和连接值写成变量)、[2](./prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段) |
| Milvus 变量 | milvus-docs `site/en/Variables.json` | 文档工程师 | [场景 1](./prd.md#场景-1把产品名和连接值写成变量) |
| 页面配置 | zdoc `shared-docs/pages/<页面标识>/page.yaml` | 文档工程师 | [场景 3](./prd.md#场景-3接入一页)、[4](./prd.md#场景-4写-cloud-的差异) |
| Cloud 内容文件 | zdoc `shared-docs/pages/<页面标识>/` 下，按需 | 文档工程师 | [场景 4](./prd.md#场景-4写-cloud-的差异) |
| Cloud 变量 | zdoc `shared-docs/Variables.json` | 文档工程师 | [场景 1](./prd.md#场景-1把产品名和连接值写成变量) |
| 链接映射表 | zdoc `shared-docs/links.yaml` | 文档工程师 | [场景 5](./prd.md#场景-5链接与图片) |
| 版本记录 | zdoc `shared-docs/pages/<页面标识>/lock.yaml` | 只由工具写入 | [第 4 节](./prd.md#4-一页的生命周期) |
| 代码 Tabs 规则 | zdoc `shared-docs/presentation/cloud-sdk-tabs.yaml` | zdoc 维护者 | — |
| 共享来源配置 | zdoc `shared-docs/source.yaml` | zdoc 维护者 | — |

每个文件影响生成页面的哪一部分：

![一个共享页的文件，以 OpenAI 页为例。milvus-docs 中有共享原文（每页一份）和 Milvus 默认变量（共用）。zdoc 的 shared-docs 目录中，决定页面内容的有页面配置（每页一份）、Cloud 内容文件（按需）、Cloud 变量（共用）、链接映射表（共用）和代码 Tabs 规则（工程维护）；决定用哪个版本、不提供内容的有 lock.yaml（每页一份，工具写入）和 source.yaml（工程维护）。生成的页面中，标题、描述、标签与路由来自页面配置，导航来自飞书目录；正文来自共享原文，绑定 Cloud 变量，链接按映射表对应；替换的一节来自 Cloud 内容文件；代码 Tabs 来自共享原文的代码，凭证参数行按页面配置中的规则替换，再按 Tabs 规则生成，原文有哪些语言就显示哪些；Prod 与 UAT 各用 lock.yaml 中记录的版本。](./assets/file-relationships.png)

图 1 · 一个共享页由哪些文件组成、各影响页面的哪一部分（以 OpenAI 页为例）

## 2. 原文中的写法

| 写法 | 例子 | 规则见 |
|---|---|---|
| 变量 | `{{var.product_name}}` | [场景 1](./prd.md#场景-1把产品名和连接值写成变量) |
| 片段 | `{{fragments/xxx.md}}` | [场景 1](./prd.md#场景-1把产品名和连接值写成变量) |
| 命名块 | `<!-- doc:block:start id="before-you-start" -->` … `<!-- doc:block:end id="before-you-start" -->` | [场景 2](./prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段) |

## 3. `page.yaml` 的全部字段

| 字段 | 必填 | 取值 | 规则见 |
|---|---|---|---|
| `schema_version` | 是 | `1` | [场景 3](./prd.md#场景-3接入一页) |
| `source.file` | 是 | 原文路径，相对于 milvus-docs 仓库根目录 | 同上 |
| `publish[].manual` | 是 | zdoc 现有的手册，如 `guides`、`guides-byoc` | 同上 |
| `publish[].path` | 是 | 页面在手册中的路径；Phase 1 与飞书节点一致 | 同上 |
| `metadata.title` | 否 | 默认取原文的 `title` | 同上 |
| `metadata.description` | 否 | 默认取原文的 `summary` | 同上 |
| `metadata.beta` | 否 | `FALSE`（默认）、`PUBLIC`、`PRIVATE`、`NEAR DEPRECATE` | 同上 |
| `transforms[].operation` | 是 | `add`、`replace`、`remove` | [场景 4](./prd.md#场景-4写-cloud-的差异) |
| `transforms[].target.block` | 是 | 命名块 ID | 同上 |
| `transforms[].target.language` | 否 | 代码块的语言名，如 `python`、`javascript`、`bash`、`shell`；只用于代码组 | 同上 |
| `transforms[].target.lines` | 否 | 原文中连续的 1–5 行；需要同时写 `language` | 同上 |
| `transforms[].position` | 视情况 | `before`、`after`；只在块旁或代码行旁 `add` 时写 | 同上 |
| `transforms[].content.file` | 视情况 | Cloud 内容文件，相对于页面目录 | 同上 |
| `transforms[].content.lines` | 视情况 | 新的几行代码，不写缩进 | 同上 |
| `transforms[].channel` | 否 | `current`（只影响 Prod）、`next`（只影响 UAT） | [场景 6](./prd.md#场景-6让内容先只在-uat-显示) |

**变换的目标与操作**

| 目标 | `add` | `replace` | `remove` |
|---|---|---|---|
| `block` | `content.file` + `position` | `content.file` | 只写目标 |
| `block` + `language` | `content.file`，不写 `position` | `content.file` | 只写目标 |
| `block` + `language` + `lines` | `content.lines` + `position` | `content.lines` | 只写目标 |

## 4. 工具生成的 front matter

作者不写以下字段：

| 字段 | 生成方式 |
|---|---|
| `slug` | `/` 加页面标识 |
| `sidebar_label`、`sidebar_position` | Phase 1 按飞书节点填写 |
| `title`、`description` 的后缀 | 按手册，如 `\| Cloud`、`\| BYOC` |
| `notebook`、`added_since`、`last_modified`、`deprecate_since` | 固定为 `FALSE` |
| `type` | `origin` |
| `displayed_sidebar` | `default` |
| `token` | `shared-<页面标识>` |
| `channel` | 整页只在一边存在时，由 `lock.yaml` 决定 |

Phase 1 不开放：`keywords`、`hide_title`、`hide_table_of_contents`，以及 `beta` 的 `DEPRECATED`。

## 5. Cloud 内容文件

| 可以用 | 不可以用 |
|---|---|
| 与 Milvus 原文相同的 Markdown 写法，如 `<div class="alert note">`、`<div class="multipleCode">` | 命名块标记 |
| 变量、片段 | 手写的 `<Tabs>`、`<Admonition>` 等 Cloud 组件 |
| zdoc 现有的产品过滤写法 | |
| `<NextChannel>` | |
| 页面目录下的图片，或外部图片地址 | |

规则见[场景 4](./prd.md#场景-4写-cloud-的差异)。

## 6. 链接映射表

```yaml
# shared-docs/links.yaml
boolean.md: filtering-overview                    # Cloud 中对应的页面
ivf-flat.md: https://milvus.io/docs/ivf-flat.md   # Cloud 没有对应页时，明确指向 Milvus 站点
```

只在工具报错“找不到 Cloud 对应页面”时补；每个 Milvus 页面全站登记一次。规则见[场景 5](./prd.md#场景-5链接与图片)。

## 7. 让内容只在 UAT 显示

| 内容 | 写法 |
|---|---|
| Milvus 原文在两个版本之间的变化 | 不用写 |
| Cloud 新写的一段 | Cloud 内容文件中用 `<NextChannel action="include">` 包住 |
| 替换或删除原文的一段，下次发布时才生效 | 变换加 `channel: next` |
| 整个新页面 | 接入 PR 加标签 `shared-docs: not-launched` |

规则见[场景 6](./prd.md#场景-6让内容先只在-uat-显示)。

## 8. PR 标签与手动操作

| 操作 | 在哪里 | 谁 | 规则见 |
|---|---|---|---|
| 标签 `shared-docs: not-launched` | 接入 PR | 文档工程师 | [场景 3](./prd.md#场景-3接入一页) |
| 手动触发上游更新，可指定页面与提交 | zdoc GitHub Actions | 文档工程师 | [场景 7](./prd.md#场景-7审核上游更新) |
| 提升 | zdoc GitHub Actions，“提升与下线”工作流 | 文档工程师 | [场景 8](./prd.md#场景-8功能上线时提升) |
| 下线 | 同上 | 文档工程师 | [场景 10](./prd.md#场景-10下线一页) |
| 比较、激活 | zdoc，入口形式待定 | 文档负责人 | [场景 9](./prd.md#场景-9从飞书切换到-git激活) |
| 删除飞书节点 | 飞书知识库目录 | 发起提升的文档工程师 | [场景 10](./prd.md#场景-10下线一页) |

## 9. 出错时查哪里

工具先校验全部配置，再生成页面；出错时直接失败，不会静默跳过。

| 错误与什么有关 | 在哪里发现 | 见 |
|---|---|---|
| 变量缺少 Cloud 的值；片段 | zdoc 的 PR 校验 | [场景 1](./prd.md#场景-1把产品名和连接值写成变量) |
| 命名块标记的写法 | milvus-docs 的 PR 检查 | [场景 2](./prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段) |
| 页面目录、`page.yaml` 的字段 | zdoc 的 PR 校验 | [场景 3](./prd.md#场景-3接入一页) |
| 变换的目标、冲突、代码行、内容文件 | zdoc 的 PR 校验 | [场景 4](./prd.md#场景-4写-cloud-的差异) |
| 链接、锚点、图片 | zdoc 的 PR 校验 | [场景 5](./prd.md#场景-5链接与图片) |
| `channel`，规则只在一个版本上失效 | zdoc 的 PR 校验 | [场景 6](./prd.md#场景-6让内容先只在-uat-显示) |
| 上游改名、删除了 Cloud 引用的内容 | 上游更新 PR 的校验 | [场景 7](./prd.md#场景-7审核上游更新) |
| 激活前的检查 | 激活运行 | [场景 9](./prd.md#场景-9从飞书切换到-git激活) |
