# WP8 生成命令与 PR 校验

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：WP4、WP5、WP6 已合并（[zilliztech/zdoc#804](https://github.com/zilliztech/zdoc/pull/804)、[#815](https://github.com/zilliztech/zdoc/pull/815)、[#812](https://github.com/zilliztech/zdoc/pull/812)）；WP8a 在 [WP7](./WP7-zdoc-links-seed.md) 合并后开工；WP8b 要等 zdoc 维护者回答下文“待确认”的问题　**状态**：未开始

## 目标

做完后：

- **WP8a**：一条命令 `shared-docs build` 把已有的各步接起来，为每一页、每个手册生成 Cloud 的 MDX：
  1. 读取（WP3）；
  2. 链接与图片（WP5）；
  3. 站点适配（WP4）；
  4. 产品名检查（WP6）。

  有错误时一次全部报出，不写半成品。
- **WP8b**：zdoc 中新增两个工作流：
  - 接入一页时，自动给 PR 写入 `lock.yaml`；
  - 每个改 `shared-docs/` 的 PR 都跑一遍 `shared-docs build`，不通过不能合并。

WP8 不写 dev、不上传图片：合并后进入 Fetch、真正发布是 WP9 的事。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 3：系统行为 3-2 至 3-6、出错时 | 接入一页的行为 |
| [技术设计 README](../../design/README.md) | 生成流水线、数据文件 | 各步的顺序、数据文件放在哪里 |
| [技术设计 04](../../design/04-channels-and-lock.md) | 每页一份 `lock.yaml`、只在一个通道存在的页面、接入一页 | lock 的写入；飞书表格快照 |
| [技术设计 05](../../design/05-publish-handoff.md) | 交接发生在哪里、PR 校验 | 校验做什么、不做什么 |
| [技术设计 08](../../design/08-workflows-and-permissions.md) | 全文（WP8b） | 两个工作流的触发、权限、并发与失败通知 |
| [WP3](../walkthroughs/WP3.md)、[WP4](../walkthroughs/WP4.md)、[WP5](../walkthroughs/WP5.md)、[WP6](../walkthroughs/WP6.md) 走读 | 全文 | 要接起来的各步 |
| [实现指南](../README.md) | 第 5 节 | 规则 |

## 范围

| 可以改 | 不能改 |
|---|---|
| WP8a：新建 `adapters/build-page.ts`（一页的整条流水线）、`adapters/guides-snapshot.ts`（`GuidesBase` 的真实实现，读 dev 检出中的飞书表格快照）、`commands/build.ts`；在 `cli-main.ts` 中注册 `shared-docs build` | 各步已有函数的行为：WP3–WP7 的代码只调用；要改先在 PR 中提出 |
| WP8a：复用 WP7 的 `adapters/zdoc-content.ts`，可以给它加读 front matter 的方法 | `lark/`、`mdx/` 与 dev 上的任何文件：只读 |
| WP8a：新建 `fixtures/build/`、`testing/build/` | 仓库根目录的 `shared-docs/`：第一篇页面正式接入时再建 |
| WP8b：新建 `.github/workflows/shared-docs-lock.yml`、`shared-docs-validate.yml`；在 `scripts/docs-workflow/test-matrix.json` 中登记；按 zdoc 现有的工作流测试补用例 | 现有工作流，包括 `fetch-docs.yml` 与 `sync-master-tooling-to-dev.yml` |
| `spec/pending.json`：删掉本工作包的编号；`3-6` 改为 `"WP14"` | 分支保护、`CODEOWNERS`、仓库设置：由 zdoc 维护者在 GitHub 上配置，不在 PR 中改 |

## WP8a：生成命令

```ts
// adapters/build-page.ts
buildPage(input: {
  pageId: string
  sharedDocs: SharedDocsInputs        // source.yaml、page.yaml、lock.yaml、Variables.json、links.yaml、product-names.yaml、Tabs 规则，以及全部页面的 source.file → 页面标识
  reader: LinkInputReader             // WP5：读 milvus-docs
  md2md: Md2md
  fetcher: ImageFetcher
  zdoc: ZdocContent                   // WP7：dev 中各手册的页面清单，以及这一页现有的 front matter
  guides: GuidesBase                  // 飞书表格快照
}): Promise<{ pages: { manual: string; path: string; mdx: string; images: ImageRecord[]; notices: Notice[] }[] } | { errors }>

// commands
pnpm docs-tooling shared-docs build --shared-docs <目录> --repo <milvus-docs 检出> --dev <zdoc dev 检出> --out <输出目录> [--page <页面标识>]
// 不写 --page 时生成全部页面；输出 <输出目录>/<手册>/<publish.path>.mdx 与一份 images.json；有错误时以 1 结束、不写任何 MDX
```

一页、一个版本、一个手册的顺序，与[技术设计的生成流水线](../../design/README.md#生成流水线)相同：

1. **读取**（WP3 的 `inspectPage`）：配置、lock、原文、命名块、删标记、展开变量与片段。没有 `lock.yaml` 时按计划值生成（产品需求 3-1）。
2. **链接与图片**（WP5 的 `prepareLinkInputs` 与 `rewriteLinksAndImages`）：
   - Cloud 页面清单取 dev 中这个手册的页面（待确认 1）；
   - 共享页清单取全部 `page.yaml` 的 `source.file`。
3. **站点适配**（WP4 的 `adaptPage` 与 `toMdx`）：
   - 标题锚点传入 `text => cloudAnchor(headingText(text))`，即 WP5 的算法；
   - `sidebar_label`、`sidebar_position` 取 dev 上这一页现有 MDX 的 front matter（待确认 2）。
4. **产品名检查**（WP6 的 `checkProductNames`）：`sources` 依次放这一版本的原文、用到的片段、用到的变量的值。

- **两个版本**：`current` 与 `next` 各走一遍。两版生成的 MDX 相同时输出一份；不同时，命令以明确的消息拒绝这一页，说明两版合并要等 WP11。Phase 1a 中，接入时两个版本是同一个提交，不会出现不同。
- **变换**：`page.yaml` 中的 `transforms` 不为空时，报 `CONFIG_FIELD_UNKNOWN`（位置是 `transforms` 那一行），说明变换要等 WP10。不能跳过：跳过会生成一页内容不对的页面。
- **飞书表格快照**：
  - 从 dev 检出中读 `packages/docs-tooling/src/lark/meta/snapshots/guides-uat-last-success.json`；
  - 每条记录有 `slug`、`title`、`placement_type`、`release_channel`；
  - WP8a 只用它确认 `publish[].path` 对应的页面在飞书目录中存在（技术设计 04：“只能接入在飞书目录中已有节点的页面”），不存在时报错。
  - 整页通道（`release_channel`）归 WP13，这里不输出。
- **输出路径**：用 `page.yaml` 的 `publish[].path`，不读快照中的 `output_paths`（2026-10-23 dev 上的快照中，402 条记录的这个字段都是空的）。

## WP8b：两个工作流（待 zdoc 维护者确认后开工）

按技术设计 08 的“工作流一览”实现 `shared-docs-lock` 与 `shared-docs-validate`：

| 工作流 | 触发 | 权限 | 做什么 |
|---|---|---|---|
| `shared-docs-lock` | `pull_request`：`shared-docs/pages/**` 变化 | `contents: write`、`actions: write` | 新页面没有 `lock.yaml` 时，取跟踪分支的最新提交写入，提交到 PR 分支，再用 `gh workflow run` 触发校验；来自 fork 的 PR 不写入，在 PR 中提示 |
| `shared-docs-validate` | `pull_request`；`workflow_dispatch` | `contents: read`，不读任何 secret | 只读地检出 milvus-docs 与 zdoc dev，运行 `shared-docs build`；没有改 `shared-docs/` 的 PR 立即通过 |

- 照搬 `sync-master-tooling-to-dev.yml` 的做法：用 `GITHUB_TOKEN` 推送后显式触发校验并等待结果。
- 准备 milvus-docs 检出时要有跟踪分支的本地分支与完整历史，WP3 的读取要求如此（见 [WP3 走读](../walkthroughs/WP3.md)）。
- 工作流本身出错时用飞书卡片通知，沿用 `report-card`；校验不通过只作为 PR 的检查项失败。

## 要覆盖的编号

| 编号 | 工作包 | 怎样测 |
|---|---|---|
| `3-4` | WP8a | 一篇合成的页面走完整条流水线：多语言代码组变成完整的 `<Tabs>`、变量换成 Cloud 的值、链接换成 `./<页面标识>`、锚点换算、图片换成 `shared/<摘要>` 地址，产品名检查通过，MDX 能编译 |
| `3-2` | WP8b | `Release Channel` 为 `NEXT` 的页面，接入时 `lock.yaml` 照常写入 |
| `3-3` | WP8b | 改 `shared-docs/` 的 PR 运行完整生成；生成失败时检查项失败 |
| `T12`（候选部分） | WP8b | `shared-docs-validate` 只有 `contents: read`，不引用任何 secret；用 zdoc 现有的工作流策略测试断言 |

- 三篇试点页也各跑一次 `shared-docs build`，把结果写进 PR 说明，测试不断言。内容对齐之前，预期会有产品名与链接的错误，例如 OpenAI 的 `LINK_UNRESOLVED`。
- `3-6`（接入不等于上线）改归 WP14：要等激活实现后才能验收。

## 待确认（问 zdoc 维护者）

1–3 也影响 WP8a：WP8a 可以先按下面的提议实现，由维护者在上游 PR 中确认；4 是 WP8b 开工的前提。

1. **Cloud 页面清单**：链接查找第 3 步与 WP7 的候选，从 dev 的 `content/en/<手册>/` 读 front matter 中的 slug 与标题，是否合适（技术设计 02b 留给维护者确定）？
2. **导航**：飞书表格快照中没有 `sidebar_label`、`sidebar_position`。Phase 1 共享页的这两项，从 dev 上这一页现有的 MDX 中取，是否合适？
3. **站点校验**：技术设计 05 要求生成的 MDX “通过 zdoc 现有的站点校验”。PR 校验中该跑哪一条命令？
4. **工作流与仓库配置**：
   - 两个新工作流（`shared-docs-lock` 会向 PR 分支推送 `lock.yaml`）是否可以按上表实现？
   - `shared-docs-validate` 设为 master 的必需检查项：不能按路径区分，所以所有 PR 都要跑它，没改 `shared-docs/` 的立即通过。
   - `CODEOWNERS` 与分支保护由维护者配置。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；上表中各自的编号不在 `pending.json` 中，`3-6` 归 WP14
- [ ] `pnpm test:for-change` 给出的命令全部跑过，包括 WP8b 的工作流策略测试；`pnpm typecheck` 通过
- [ ] WP8a：三篇试点页的生成结果写进 PR 说明
- [ ] WP8b：在 fork 中开一个改 `shared-docs/` 的 PR 演示两个工作流，链接写进 PR 说明
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写。“How to try it”从 `gh pr checkout` 开始，不写本机路径：WP8a 演示用合成的页面生成一份 MDX，再改坏一处看到报错；WP8b 演示 fork 中的 PR

## 不做

- 写 dev、上传图片、记录文件、接入 Fetch：WP9。
- 两版合并：WP11；变换：WP10；整页通道 `channel`：WP13。
- 上游更新、提升、比较三个工作流：WP12、WP13、WP14。
- 仓库根目录的 `shared-docs/`：第一篇页面接入时由文档工程师建。

## 已知的坑

- 一页要生成 2 个版本 × 每个手册一遍。Delete Entities 发布到 Guides 与 BYOC 两个手册，就是 4 遍。WP5 每次换算锚点都要读一遍 `site/en` 下的约 500 篇页面，同一个提交的读取结果要在一次运行中共用，不要重复读。
- 同一个外部图片在多个版本、多个手册中出现时，只下载一次（每次下载两遍做比较），结果共用。
- 校验在 `pull_request` 上下文中运行，来自 fork 的 PR 也要能跑：不能用任何 secret，也不能假设有写权限。
