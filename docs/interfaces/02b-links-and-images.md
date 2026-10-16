# 02b 链接与图片

Milvus 原文中的链接和图片地址是按 milvus.io 写的，原样放进 Cloud 页面，有的会指错，有的会在未经审核的情况下改变。本篇定义生成时怎样把它们变成 Cloud 可用的地址，以及作者在什么情况下需要补充配置。

**参与方**：zdoc 生成（解析与改写）、文档工程师（维护链接映射表）、zdoc 发布（上传图片，见 [05](./05-publish-handoff.md)）。

**状态**：已定义，待文档负责人确认。

## 约定

### 链接

只处理 Cloud 最终页面中留下的链接，被替换或删除的部分不处理。

| 链接类型 | 例子 | 处理 |
|---|---|---|
| 指向标题的锚点 | `#Delete-Entities-by-Primary-Keys` | 换成 Cloud 的锚点写法，见下文 |
| 外部网站 | `https://platform.openai.com/...` | 原样保留 |
| milvus.io 的完整地址 | `https://milvus.io/docs/release_notes.md` | 原样保留：作者写完整地址，就是有意指向 Milvus 站点 |
| Milvus 站内页面 | `boolean.md`、`boolean.md#xxx` | 换成 Cloud 页面地址，见下表 |
| 以 `/` 开头的站内路径 | `/api-reference/...`、`/bootcamp` | 该页生成失败：在 Cloud 站点上一定指错 |
| 不属于以上任何一类 | `filtering`（漏写 `.md`） | 该页生成失败 |

Milvus 站内页面按顺序查找，查到即停：

| 顺序 | 查什么 | 结果 |
|---|---|---|
| 1 | 目标页也是共享页（某个页面配置的 `source.file` 就是它） | 用那一页的页面标识，如 `./primary-key-search` |
| 2 | 映射表中有这一页 | 用映射表中的地址 |
| 3 | Cloud 有同名页面 | 用同名页面 |
| 4 | 以上都没有 | 该页生成失败，提示在映射表中补一行 |

映射表全站一份，只登记查不到同名页、也还不是共享页的 Milvus 页面，每页登记一次，所有共享页共用：

```yaml
# shared-docs/links.yaml
boolean.md: filtering-overview                    # Cloud 中对应的页面
ivf-flat.md: https://milvus.io/docs/ivf-flat.md   # Cloud 没有对应页时，明确指向 Milvus 站点
```

映射值写成 milvus.io 地址时，Cloud 页面会链接到 Milvus 站点。是否允许这样做列为[待确认事项](../phase-1.md#61-待确认的接口)，暂按允许、且只能在映射表中明确写出处理。

### 锚点

milvus.io 的标题锚点保留大小写（如 `#Delete-Entities-by-Filtering-Conditions`），zdoc 的锚点全部小写（如 `#delete-entities-by-filtering-conditions`），两边对标点的处理也不同。浏览器按大小写匹配锚点，所以原样照搬会失效。

- **目标是本页或另一个共享页**：工具按 Milvus 的规则算出目标页每个标题的锚点，找到链接指向的标题，输出该标题在 Cloud 中的锚点；找不到对应标题时该页生成失败。
- **两个版本分别计算**：`current` 版本中的链接按目标页 `current` 版本的标题计算，`next` 版本中的链接按目标页 `next` 版本的标题计算。目标页在该版本中不存在（lock 中为 `none`）时，该页生成失败。这条规则同样适用于不带锚点、指向另一个共享页的链接。
- **目标是 Cloud 自己维护的页面**：按 Cloud 的规则转成小写写法，是否存在由 zdoc 现有的链接检查发现。
- 多语言代码组中切换语言用的 `#python`、`#java` 等不是链接，由站点适配处理。

标题改名后锚点变化的处理见 [04](./04-channels-and-lock.md#标题改名与锚点)。

### 图片

**Cloud 页面用到的每一张图片，都转存到 zdoc 现有的图片存储，页面中的地址改为按内容命名的新地址。** 不再直接引用 Milvus 或其他外部地址，原因见[设计理由](#设计理由)中的“为什么转存图片”。作者不为图片写任何配置。

| 图片来源 | 例子 | 怎样取到 |
|---|---|---|
| Milvus 的存储 | `https://milvus-docs.s3.../assets/filtered-search.png` | 下载 |
| 其他外部地址 | `https://assets.zilliz.com/...png` | 下载 |
| milvus-docs 仓库内的文件 | `../../../assets/xxx.png` | 从 lock 记录的同一 commit 读取 |
| Cloud 内容文件中的图片 | 页面目录下的文件，或外部地址 | 从 zdoc 读取，或下载 |

**新地址由摘要决定。** 工具按图片内容计算摘要，用它作文件名，如 `shared/3f9a…c1.png`。摘要是用 SHA-256 这类标准算法、按文件全部内容算出的一串字符，相当于内容的指纹：内容相同摘要就相同，内容一变摘要就变（见[术语表](./glossary.md#发布)）。Markdown 的 `![](...)` 与 HTML 的 `<img src>` 都改为新地址；原地址与摘要写入记录文件（见 [05](./05-publish-handoff.md#记录文件)）。

**同样的图只存一份，换过的图另存一份。**

| 情况 | 存储中 | 页面引用 |
|---|---|---|
| 同一张图出现在 Prod 与 UAT 两个版本中，或出现在多个页面中 | 摘要相同，只存一份 | 都引用同一个地址 |
| Milvus 换了这张图，`current` 与 `next` 两个版本中的内容不同 | 摘要不同，存两份 | Prod 引用旧图，UAT 引用新图 |

- **已存的图片不会被覆盖。** 提升后 Prod 改用新图，旧图仍留在存储中；按记录文件恢复旧版本时，旧图还在。
- **换图要经过审核。** Milvus 换图会让地址变化，出现在上游更新 PR 的差异中，审核后才进入 Prod。

**生成时算地址，发布时才上传。** 地址只由内容决定，生成时就能算出，不需要图片存储的写权限；正式发布时只上传存储中还没有的图片。所以 PR 预览中，新出现的图片暂时显示不出来，合并后才上传（见 [05](./05-publish-handoff.md#图片上传)）。

## 出错时

| 情况 | 结果 |
|---|---|
| Milvus 站内页面在四步中都没有找到对应地址 | 该页生成失败，提示补映射表 |
| 出现以 `/` 开头的站内路径 | 该页生成失败，提示在映射表中处理，或回上游改成完整地址 |
| 链接不属于任何一类 | 该页生成失败，提示回上游修正 |
| 链接指向的共享页在同一版本中不存在 | 该页生成失败 |
| 指向共享页标题的锚点找不到对应标题 | 该页生成失败 |
| 指向 Cloud 自有页面的锚点不存在 | 由 zdoc 现有的链接检查发现 |
| 外部图片下载失败或不存在 | 该页生成失败 |
| 仓库内的图片在 lock 记录的 commit 中不存在 | 该页生成失败 |
| 同一图片两次读取内容不同（读取过程中被覆盖） | 该页生成失败，重试 |

## 例子

<details>
<summary>三个试点页</summary>

| 页面 | 链接 | 图片 |
|---|---|---|
| Delete Entities | `boolean.md`：第 2 步，映射表中为 `filtering-overview` | 无 |
| Filtered Search | `primary-key-search.md`：第 3 步，同名页；`filtering`（漏写 `.md`）：不符合任何类型，生成失败，在内容对齐时于上游修正 | 两张 Milvus 存储中的图片，转存后地址改为按内容生成 |
| OpenAI | `configure-docker.md`：在被替换的一节中，不处理；`embedding-function-overview.md`：Cloud 没有同名页，需要在映射表中补一行；两个 OpenAI 官网链接：原样保留 | 无 |

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么需要映射表。** milvus-docs `v3.0.x` 中有 2074 个站内页面链接；User Guide 与 Embeddings 中的 837 个，只有 32% 的目标在 Cloud 有同名页面。两边页面名字不同是历史原因：Cloud 文档在飞书中按自己的结构命名（如 Milvus 的 `boolean.md` 在 Cloud 是 `filtering-overview`）。两边的地址都已公开，被搜索引擎收录、被站外引用，改名要在两站都做跳转，Phase 1 不做。

**为什么全站一份。** 同一个目标页会被很多共享页引用，登记一次即可；每页各写一份，成本随页数增长。随着更多页面迁移为共享页，查找的第 1 步覆盖的目标越来越多，映射表随之缩短。

**为什么换算锚点。** 在两站同一页面上核实过：milvus.io 的锚点为 `Delete-Entities-by-Filtering-Conditions`，docs.zilliz.com 为全小写。milvus-docs 中跨页带锚点的链接有 284 个，其中 274 个含大写字母。

**为什么转存图片。** zdoc 现有的 397 张英文 Guides 图片都存在 zdoc 自己的图片存储中。[恢复能力核验](../../research/recovery-capability-audit.md)发现，现有上传逻辑在内容变化时会上传到同一地址，旧页面不能保证显示旧图片；核验建议为迁移页用到的图片固定内容摘要，存成不会被覆盖的地址。直接引用 Milvus 的地址也有同样的问题，还会让 Milvus 换图绕过上游更新 PR 的审核。

依据的统计见 [zdoc 代码变体与发布通道核验第 2.1 节](../../research/zdoc-variants-and-channels-audit.md#21-补充核验2026-10-14)。

</details>

## 验收

- **T06**：链接、锚点与图片正确；缺图或图片字节变化时失败。
- **T10**：图片可以从固定的摘要恢复。
