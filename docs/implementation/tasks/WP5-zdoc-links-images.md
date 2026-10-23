# WP5 链接与图片

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP3](./WP3-zdoc-read.md)：WP3a 已合并（[zilliztech/zdoc#796](https://github.com/zilliztech/zdoc/pull/796)，commit [`5844587`](https://github.com/zilliztech/zdoc/commit/5844587037d5397e8ebd1510235db5d8592584d7)）；WP3b 已合并（[zilliztech/zdoc#800](https://github.com/zilliztech/zdoc/pull/800)，commit [`31a9b54`](https://github.com/zilliztech/zdoc/commit/31a9b54176c9adc50515f84a559b4082700b6620)），可以开工。可与 [WP4](./WP4-zdoc-site-adaptation.md)、[WP6](./WP6-zdoc-product-names.md) 同时进行　**状态**：未开始

## 目标

做完后，给定一个版本的页面 Markdown（WP3 已展开变量与片段），zdoc 能：

- 把其中的链接改成 Cloud 可用的地址：Milvus 站内页面按四步查找，锚点按两个站点的算法换算；
- 算出每张图片转存后的地址（按内容摘要命名），只算不传；
- 处理不了的链接和取不到的图片一律报错，一次全部报出。

本工作包还提供两个站点的标题锚点算法。WP4 输出标题锚点时经参数使用 Cloud 的算法，由 WP8 接入。

本工作包只提供函数和测试，不接入任何命令（WP8）。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 5 全部 | 链接类型、四步查找、锚点、图片的行为 |
| [技术设计 02b](../../design/02b-links-and-images.md) | 链接、锚点、图片、出错时 | 实现规则；“初始映射表的生成”只读“查不到时的报错”一段 |
| [技术设计 07](../../design/07-site-adaptation.md) | 标题锚点 | Cloud 锚点与重复标题 |
| [技术设计 09](../../design/09-error-catalog.md) | 错误的结构、链接与图片 | 错误码 |
| [实现指南](../README.md) | 2.3、2.5、2.6、第 5 节 | 合成仓库、错误样例表、适配器、规则 |
| [WP0 走读](../walkthroughs/WP0.md) | 全文 | 目录、替身与测试工具 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新建 `core/links/`：链接分类、四步查找、`links.yaml` 的读取、两个站点的锚点算法、图片地址的计算，都是纯计算 | `core/types.ts`、`adapters/types.ts`：WP3 是主人，要加共用类型先在 PR 中提出；本工作包的类型放在 `core/links/` 与下面的新适配器文件中 |
| 新建 `adapters/images.ts`：下载外部图片的接口、真实实现与假实现；读仓库内图片用已有的 `MilvusDocsReader` | `lark/`：只在测试中调用，用来比对锚点算法 |
| 新建 `adapters/links-input.ts`：为一页准备查找所需的输入（目标页原文、图片内容），用 `MilvusDocsReader` 按同一 commit 读取 | `commands/`、`cli-main.ts`：接入命令归 WP8 |
| `fixtures/milvus-docs/commits/`：在 `01-base` 中新增一张图片和一篇只供本工作包测试的小页面，新增 `10-image-changed` 换掉这张图（实现指南 2.3）；不改已有文件 | Tabs、提示框、front matter（WP4）；产品名检查（WP6） |
| 新建 `fixtures/links/`、`fixtures/links-errors/<样例>/`、`testing/links/` | `fixtures/golden/` |
| `spec/pending.json`：删掉本工作包的编号；`5-3`、`T06` 改为 `"WP9"` | |
| `spec/requirements.json`：从设计仓库原样重新复制一次，新增 `LINK_MAP_INVALID`（共 76 个错误码）；三个同时进行的工作包中只有本工作包复制它 | 自行修改其中的内容 |

## 接口

```ts
// core/links/：纯计算
parseLinkMap(yamlText, context): { map: LinkMap } | { errors }        // LINK_MAP_INVALID
headingText(headingMarkdown: string): string    // 去掉 Markdown 标记与 HTML，两种算法共用
milvusAnchor(text: string): string              // milvus.io：\s+ → '-'，再删去 [^A-Za-z0-9-]，保留大小写
cloudAnchor(text: string): string               // zdoc：slugify(text, { lower: true, strict: true })
collectReferences(markdown): { links: LinkRef[]; images: ImageRef[] }  // 带行号
rewriteLinksAndImages(input: {
  markdown: string
  sourceFile: string                            // 这一页在 milvus-docs 中的路径
  sharedPages: ReadonlyMap<string, string>      // 第 1 步：Milvus 文件名 → 共享页的页面标识，来自全部 page.yaml
  linkMap: LinkMap                              // 第 2 步
  cloudPages: readonly { slug: string; title: string }[]   // 第 3 步与报错中的候选；真实来源由 zdoc 维护者确定，WP8 接入
  targets: ReadonlyMap<string, string | null>   // 链接指向的 Milvus 页面在同一 commit 的原文；null 表示不存在
  images: ReadonlyMap<string, ImageContent>     // 每个图片地址读到的内容与摘要
  recorded?: ReadonlyMap<string, string>        // 已采用版本中记录的“原地址 → 摘要”，见 5-6
  context: DiagnosticContext
}): { markdown: string; images: ImageRecord[]; notices: Notice[] } | { errors }

// adapters/
interface ImageFetcher { fetch(url: string): Promise<Uint8Array> }   // 真实实现只在 L3 跑；测试用假实现
prepareLinkInputs(markdown, sourceFile, commit, reader, fetcher): Promise<{ targets; images } | { errors }>
```

- **链接分类**按产品需求场景 5 的表：
  - 页内锚点、外部网站、milvus.io 完整地址、Milvus 站内页面（`<文件名>.md`，可带 `#锚点`）、以 `/` 开头的路径，其余都算不认识的写法；
  - `mailto:` 按外部网站处理。
  - 只处理正文中的 Markdown 链接与 HTML 的 `href`。代码块中的不处理，多语言代码组切换栏中的 `#python` 等也不处理。
- **四步查找**查到即停：
  - 得到 Cloud 页面时一律写成 `./<页面标识>`：第 1、3 步，以及第 2 步中映射表的值是页面标识时；与 dev 上现有页面的写法相同，如 `(./filtering-overview)`；
  - 映射表的值是 milvus.io 地址时，原链接的锚点原样接在后面，因为它指向的是 milvus.io 的页面；
  - 查不到时报 `LINK_UNRESOLVED`，`detail.candidates` 中附上最多三个候选：标题相同的页面，以及标题相近的页面。候选的计算写成独立的函数，WP7 生成初始映射表时复用。
- **锚点换算**：
  1. 在目标页同一 commit 的原文中，用 `milvusAnchor` 算出每个标题的锚点，找到与链接锚点完全相同的那个；
  2. 再用 `cloudAnchor` 从这个标题的文字算出 Cloud 锚点。
  - 页内锚点的目标页就是本页。
  - 找不到对应标题时报 `ANCHOR_NOT_FOUND`；只差大小写也算找不到。
  - 几个标题算出相同的 Milvus 锚点时，取第一个。
- **图片**：
  - 处理 Markdown 的 `![](...)` 与 HTML 的 `<img src>`。
  - 仓库内的相对路径相对页面文件解析，按同一 commit 读取；外部地址下载。
  - 新地址是 `shared/<sha256>.<扩展名>`，扩展名取原地址路径中的小写扩展名。
  - 结果中的 `images` 列出每张图片的原地址、摘要与新地址，供 WP9 写记录文件与上传。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `5-1` | 产品需求场景 5 表中每类链接各一个样例；处理不了的报错，输出中不留原链接 |
| `5-2` | 同一个 Milvus 页面在 `links.yaml` 中登记两次，报 `LINK_MAP_INVALID`；两篇共享页用同一份映射表得到相同结果 |
| `5-4` | 合成仓库 `01-base` 与 `10-image-changed` 中同一张仓库内图片，算出的新地址不同 |
| `5-5` | 整个过程不调用 `ImageStore.upload`：测试中传入 `FakeImageStore`，结束时它的 `uploads` 为空 |
| `5-6` | `recorded` 中有这张图的摘要、而读到的内容不同：仍用记录中的摘要算地址，`notices` 中有一条“原地址内容已变”，不报错 |
| `5-7` | Cloud 有一页标题与目标页相同、slug 不同：不自动采用，报 `LINK_UNRESOLVED`，候选中有这一页 |
| `LINK_UNRESOLVED`、`LINK_ROOT_PATH`、`LINK_UNKNOWN_FORM`、`LINK_TARGET_ABSENT`、`LINK_MAP_INVALID`、`ANCHOR_NOT_FOUND`、`IMAGE_FETCH_FAILED`、`IMAGE_NOT_IN_COMMIT`、`IMAGE_CHANGED_DURING_READ` | 每个一个错误样例（实现指南 2.5），断言 `code`、`file`、`line`、`page`、`channel` |

锚点算法另有两组测试，不对应编号：

- `cloudAnchor` 与 zdoc 飞书转换器的 [`__heading_slug`](https://github.com/zilliztech/zdoc/blob/master/packages/docs-tooling/src/lark/larkDocWriter.js) 在同一批标题上结果相同。这批标题包括三篇试点页的全部标题，以及含 `&`、`<`、`|`、`$`、`%`、表情符号、非 ASCII 字符的标题。
- `milvusAnchor` 符合技术设计 02b 中两个线上例子：`What’s next` → `Whats-next`，`Phase 1: Ingestion & key classification` → `Phase-1-Ingestion--key-classification`。

做完后把 `5-1`、`5-2`、`5-4`–`5-7` 与上表的错误码从 `spec/pending.json` 中删掉，并把两项改归 WP9：

- `5-3` 改为 `"WP9"`：已存图片不覆盖、不清理，属于上传与存储；
- `T06` 改为 `"WP9"`：它还要求导航与编辑入口正确，要在 Fetch 接入后验收。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；上表的编号不在 `pending.json` 中，`5-3`、`T06` 归 WP9
- [ ] `pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] 合成仓库改动后，已有测试的期望不需要修改；测试中的 commit 号都从构建器返回的映射中取
- [ ] `ImageFetcher` 的真实实现与假实现通过同一组契约测试；真实实现中访问网络的用例默认跳过，只在 L3 运行
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写。“How to try it”从 `gh pr checkout` 开始，不写本机路径，演示两件事：处理 Delete Entities，看到 `boolean.md` 换成 `filtering-overview`；处理 OpenAI，看到 `embedding-function-overview.md` 报 `LINK_UNRESOLVED` 并附候选。可以像 WP3b 的 `testing/demo.ts` 那样写一个小脚本，在临时目录中运行

## 不做

- 上传图片、写记录文件、已存图片的保留（WP9）。
- 生成初始映射表的命令（WP7），只把候选的计算写成可以复用的函数。
- Cloud 内容文件中的链接与图片（WP10）；Cloud 页面列表的真实来源（WP8，由 zdoc 维护者确定）。
- 标题改名后锚点的处理（WP12，见技术设计 04）。
- 在 Markdown 中输出标题锚点 `{#id}`（WP4）。

## 已知的坑

- milvus-docs `v3.0.x` `6fb1bf9` 的 User Guide 中：
  - 837 个链接直接写文件名，如 `boolean.md`，没有相对路径，也没有以 `/` 开头的路径；
  - 3 个漏写 `.md`，如 Filtered Search 中的 `filtering`；
  - 175 个外部链接，60 个 milvus.io 完整地址。
- `site/en` 中同名的 Markdown 文件只有一对：`userGuide/schema/schema.md` 与 `reference/schema.md`。读 `schema.md` 的原文来换算锚点时不能确定是哪一篇；在计划中说明 milvus.io 怎样解析它，再定规则。
- 现有 49 个带锚点的站内链接在 milvus.io 上就失效（技术设计 02b 的统计）。接入这些页面时报 `ANCHOR_NOT_FOUND` 是预期的，不要放宽规则。
- `headingText` 要先去掉 Markdown 标记再算锚点：强调、行内代码的反引号、链接只留文字、HTML 标签。两个站点的算法共用这一步，Cloud 一侧与飞书转换器的 `__clean_headings` 结果一致。
- 下载外部图片要读两次、比较摘要，不同时报 `IMAGE_CHANGED_DURING_READ`；假实现要能模拟两次返回不同内容。
- 合成仓库是测试共用的：在 `01-base` 中加文件会改变所有 commit 号，所以测试一律从构建器返回的映射中取；不改已有文件的内容，WP3 的读取测试才不受影响。
