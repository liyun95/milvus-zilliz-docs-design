# WP7 生成初始链接映射表

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP5](./WP5-zdoc-links-images.md) 已合并（[zilliztech/zdoc#815](https://github.com/zilliztech/zdoc/pull/815)，commit [`ca1cbd5`](https://github.com/zilliztech/zdoc/commit/ca1cbd57c3179a202f625391fa4d7b4b84054296)），可以开工。与 [WP8](./WP8-zdoc-build-and-validate.md) 都要在 `cli-main.ts` 中注册子命令、都要读 zdoc dev 的内容，所以先做 WP7，WP8 在它合并后开工　**状态**：未开始

## 目标

做完后，文档工程师运行一条一次性的命令，就能得到一份 `shared-docs/links.yaml` 的候选：

- 列出 User Guide 中被链接的每个 Milvus 页面在 Cloud 中对应哪一页；
- 每行用注释写明候选的来源；
- 找不到的写成注释掉的一行，附上相近的 Cloud 页面，由人判断。

文档工程师审一遍、补全后用 PR 提交（[产品需求场景 5](../../prd.md#场景-5链接与图片) 的“初始内容由工具一次生成，人审一遍”）。这份候选要在飞书版页面还在的时候生成：其中一种来源是从 Cloud 现有页面中的链接反推，页面迁出飞书后就不能再用了。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 5：怎样操作中的“链接”、取舍中的“为什么初始映射表由工具生成” | 目的 |
| [技术设计 02b](../../design/02b-links-and-images.md) | 链接；初始映射表的生成 | 输入、五种来源的顺序、输出格式 |
| [链接映射表的维护方式调研](../../../research/link-mapping-maintenance.md) | 第 1、2、3、7 节；`evidence/links-and-anchors/linkmap.py` | 方法与验收用的数字 |
| [WP5 走读](../walkthroughs/WP5.md) | 全文 | 可以复用的函数：链接分类、候选、读 Git 的适配器 |
| [实现指南](../README.md) | 第 5 节 | 规则 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新建 `core/links/seed.ts`：由输入算出候选表，纯计算；复用 `core/links/` 中已有的分类、标题处理与候选函数，不另写一份 | `core/links/` 中已有函数的行为；要改先在 PR 中提出 |
| 新建 `adapters/zdoc-content.ts`：从一份 zdoc dev 检出中读出某个手册的页面清单（slug、标题）与页面中的站内链接；WP8 之后复用它 | `lark/` 与 dev 上的任何文件：只读 |
| 新建 `commands/links-seed.ts`；在 `packages/docs-tooling/src/cli-main.ts` 中注册 `shared-docs links-seed` | `shared-docs/links.yaml`：命令只生成候选文件，正式的表由文档工程师审核后另开 PR |
| 新建 `fixtures/links-seed/`、`testing/links-seed/` | `spec/requirements.json`、`spec/pending.json`：本工作包不覆盖编号 |

## 接口

```ts
// core/links/seed.ts：纯计算
seedLinkMap(input: {
  milvusPages: readonly { path: string; id: string; title: string; markdown: string }[]   // 跟踪分支某个提交中 site/en/ 的页面
  cloudPages: readonly { slug: string; title: string; links: readonly { text: string; target: string }[] }[]  // dev 中这个手册的页面
}): SeedResult   // 每个被链接的目标一行：结果、来源、备注、待判断时的前三个相近页面

formatSeed(result: SeedResult): string   // 输出 YAML 文本，带注释

// commands
pnpm docs-tooling shared-docs links-seed --repo <milvus-docs 检出> --commit <提交> --dev <zdoc dev 检出> --out <输出文件>
// --commit 不写时取 shared-docs/source.yaml 中跟踪分支的最新提交；只读，不写 milvus-docs 与 dev
```

- **被链接的目标**：`site/en/userGuide/` 下全部页面中、正文里的 Milvus 站内链接（`<文件名>.md`，可带锚点），按文件名去重。代码块中的不算；分类用 WP5 的 `classifyLink`。
- **Milvus 页面**：按 front matter 的 `id` 找，规则与 WP5 相同（`schema.md` 取 `reference/schema.md`）；标题取 front matter 的 `title`。
- **Cloud 页面**：`content/en/guides/` 下的 `.md` 与 `.mdx`。slug 与标题取 front matter，标题去掉 `| Cloud`、`| BYOC` 这类后缀；链接只取以 `./` 开头的站内链接。只读英文 Guides。

对每个目标依次取候选，取到即停（技术设计 02b 的五种来源）：

| 顺序 | 来源 | 写进表吗 |
|---|---|---|
| 1 | 同名页面：去掉 `.md` 后 Cloud 有这个 slug | 不写：构建时第 3 步本来就能查到；在文件末尾的统计中列出数目 |
| 2 | 标题相同：转小写、非字母数字换成空格后相同，且 Cloud 只有一页是这个标题 | 写，注释 `# 标题相同` |
| 3 | 从 Cloud 现有页面反推：Milvus 源页面对应的 Cloud 页面（同名或同标题）中，链接文字相同的链接指向哪一页；多个时取票数最多的，注释中列出其余的 | 写，注释 `# 反推` |
| 4 | 按类别指向 milvus.io：目标在 `adminGuide/`、`getstarted/`、`reference/` 下，或在 `userGuide/indexes/` 下（索引类型页，如 `userGuide/indexes/floating-vector/ivf-flat.md`） | 写成 `https://milvus.io/docs/<文件名>`，注释 `# 按类别` |
| 5 | 其余 | 写成注释掉的一行，附上 WP5 候选函数给出的前三个 Cloud 页面 |

- 2、3 两步都给出结果时必须相同；不同时写成待判断，注释中列出两个结果。
- 输出按 Milvus 文件名排序，可以直接用 WP5 的 `parseLinkMap` 读入（注释行除外），不报错。
- 文件开头写明生成时的 milvus-docs 提交、zdoc dev 提交与生成日期；末尾写各来源的数目。

## 要覆盖的编号

本工作包不覆盖需求编号（`5-7` 已由 WP5 覆盖：候选只供人确认，不在生成时采用）。测试与验收：

| 检查 | 怎样测 |
|---|---|
| 五种来源各自的规则 | 合成的小样例：同名、标题相同、标题在 Cloud 有两页、反推的票数、2 与 3 不一致、四个类别目录、其余 |
| 输出能被读回 | `formatSeed` 的输出经 `parseLinkMap` 读入不报错，条目与结果一致 |
| 与调研的数字一致 | 用调研时的两个提交运行（milvus-docs [`9acdc99`](https://github.com/milvus-io/milvus-docs/tree/9acdc99959e188a54be1df512ea3806c3110ef59)、zdoc dev [`10d6bd8`](https://github.com/zilliztech/zdoc/tree/10d6bd8)），见下文 |

调研在这两个提交上的结果：

- 181 个被链接的目标；
- 同名 60 个，标题相同 107 个，反推 105 个；
- 三种合计 116 个，剩下 65 个。

命令在同样的输入上，这几个数要相同；不同时，在 PR 中逐个列出差在哪个目标、为什么。按类别写成 milvus.io 的数目，与调研第 3 节按人工分类的 27 + 16 不必相同（规则不同），在 PR 中报告即可。这一项是手动验收，不写进自动测试，因为要两份大的检出。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；`pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] 在上面两个提交上运行，PR 说明中贴出各来源的数目，与调研的数字对照
- [ ] 再在 milvus-docs `v3.0.x` 的最新提交与 zdoc dev 的最新提交上运行一次，把生成的候选文件附在 PR 中（作为 PR 评论或说明中折叠的一段），供文档工程师审核
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写。“How to try it”从 `gh pr checkout` 开始，不写本机路径，演示在一个合成的小例子上运行，看到每种来源各一行

## 不做

- 提交正式的 `shared-docs/links.yaml`：文档工程师审核后另开 PR。
- 按标题或相似度在生成页面时自动匹配：只在这里给候选（产品需求 5-7）。
- 读中文页面、BYOC 手册：Phase 1 的初始表只按英文 Guides 生成。
- 接入任何工作流：这是一次性的本地命令。

## 已知的坑

- 反推只在“Milvus 源页面在 Cloud 有对应页”时可用：调研中有链接的 167 篇里只有 109 篇找得到。
- 链接文字两边要相同才能反推；文字中有 Markdown 标记时，先用 `headingText` 那样的方式取可见文字再比较。
- 读 dev 检出：用户会给一份只取了 `content/en/guides/` 的稀疏检出（调研中的做法），`adapters/zdoc-content.ts` 不能假设整个仓库都在。
- 页面的读取量大（Milvus 约 500 篇、Cloud 约 400 篇），用一次 `git cat-file --batch` 或直接读检出的文件，不要每篇起一个进程。
