# WP9a 走读：在 Fetch 中生成已激活的共享页

**仓库**：zdoc　**上游 PR**：[zilliztech/zdoc#863](https://github.com/zilliztech/zdoc/pull/863)，2026-10-27 合并（[`8289d7451`](https://github.com/zilliztech/zdoc/commit/8289d7451)），含 zdoc 文档负责人审阅后的两处修复，见[审阅与真实运行中发现的问题](#审阅与真实运行中发现的问题)　**任务卡**：[WP9](../tasks/WP9-zdoc-fetch-handoff.md)

## 解决什么问题

WP8 之后，`shared-docs build` 已经能在本地生成共享页的 MDX，但网站上的内容只来自 zdoc 的 dev 分支，而写 dev 的只有 Fetch。WP9a 让 Fetch 认得共享页：飞书多维表格中一页记录的 `Docs` 列，换成这一页在 zdoc master 上的页面目录地址（[技术设计 05b](../../design/05b-cutover-and-ownership.md#开关docs-链接)），下一次 Fetch 就不再抓这一页的飞书正文，改用 Git 生成，并写入 dev。

```
https://github.com/zilliztech/zdoc/tree/master/shared-docs/guides/pages/delete-entities
```

表格中一条这样的地址都没有时，Fetch 写入 dev 的内容与改动前逐字节相同。

## 一次 Fetch 中，共享页经过的地方

Fetch 原有的顺序不变，WP9a 只在其中三个任务里加了步骤：

| Fetch 的任务 | 原来做什么 | WP9a 加了什么 |
|---|---|---|
| `prepare` | 固定这次运行用的 master 与 dev 提交 | 不变 |
| 抓取英文 Guides 原文（`_fetch-guides-sources.yml`） | 读飞书表格、抓飞书正文、上传飞书图片 | 认出共享页记录；每页生成一次 Guides 与 BYOC 两份 MDX；上传它的图片；第一次激活时检查锚点 |
| 渲染各张表（`_render-guides-table.yml`） | 把飞书正文转成 MDX | 遇到共享页，把已生成的 MDX 放在飞书页面原本的位置 |
| 组装 Guides（`_assemble-guides.yml`） | 合并各表、生成导航、校验、生成检查点 | 写记录文件与 `active.json`，校验它们与最终页面一致 |
| 检查点发布 | 按串行队列写 dev | 不变；共享页的文件和其他页面在同一个提交中写入 |

渲染任务不生成、不抓取、不上传任何东西，也没有 Cloud 凭据。

## 文件地图

都在 zdoc 中。新增的文件：

| 文件 | 做什么 |
|---|---|
| `packages/docs-tooling/src/shared-docs/core/handoff/source-state.ts` | 纯计算：识别 `Docs` 链接、`active.json` 与记录文件的格式和校验 |
| `packages/docs-tooling/src/shared-docs/adapters/handoff/routing.ts` | 按固定的 master 提交确认页面目录存在；读 dev 上的 `active.json` 与记录文件 |
| `packages/docs-tooling/src/lark/sharedPageRouting.js` | 把上面两个接到飞书侧代码：每条记录走飞书还是共享页 |
| `packages/docs-tooling/src/lark/sharedPageFetch.js` | 抓取原文任务中的准备：选出共享页记录、第一次激活时抓旧文档、算锚点 |
| `packages/docs-tooling/src/lark/sharedPageBundle.js` | 生成结果的打包与读取；渲染时放入已生成的页面 |
| `packages/docs-tooling/src/lark/sharedPagePublication.js` | 组装时写记录文件、`active.json`，校验与最终页面一致 |
| `packages/docs-tooling/src/lark/sharedImageUploader.js` | 新的图片上传：只在对象不存在时创建，不覆盖 |
| `scripts/docs-workflow/guides-shared-sources.js`、`guides-shared-images.js`、`guides-shared-publication.js` | 工作流调用的三个入口：生成、上传图片、组装时的定稿与校验 |
| `scripts/docs-workflow/replay-shared-pages.js` | 回放测试：在本地 Git 远端上跑一遍完整的 Fetch |

修改的地方：

- **飞书侧按飞书文档 ID 工作的模块**：`sourceSnapshot.js`、`incrementalFetchPlanner.js`、`requestedGuidesFetchPlanner.js`、`canonicalLinkAuditor.js`、`guidesBasePreflight.js`、`larkDocScraper.js`、`larkDocWriter.js` 等。共享页记录没有飞书文档 ID，这些模块都要认得它。
- **组装身份与缓存**：`guides-assembly-identity.js`、`guides-cache-save-decision.js` 等，把共享页的输入算进去。
- **`workflows/groups.ts`**：`GUIDES_CHECKPOINT_PATHS` 加上 `generated/en/manifests/shared-pages/guides/`。
- **WP4 的站点适配**：front matter 增加 `custom_edit_url`。
- **三个工作流文件**，以及 `README.md` 中的 “Selected shared Guides source generation” 一节。

## 代码怎样工作

### 1. 认出共享页记录

每条 canonical 记录按 `Docs` 链接分三种：

| `Docs` | 结果 |
|---|---|
| 飞书文档链接 | 照旧走飞书 |
| `https://github.com/zilliztech/zdoc/tree/master/shared-docs/guides/pages/<页面标识>`，且这个目录在这次运行固定的 master 提交中存在 | 共享页 |
| 其他写法，或目录不存在 | 这一页报 `OWNERSHIP_CONFIG_MISSING`，保留 dev 上现有的版本 |

地址只认这一种写法：多一段路径、换了分支或仓库、带查询参数，都不算。

激活之后，这条记录要一直是“发布状态可发布的 canonical 记录、`Docs` 指向页面目录”。改回飞书链接、删掉记录、改成别的 placement type、把 Progress 改成不发布，Fetch 都会停下并报 `OWNERSHIP_REVERTED`，网站保持 Git 版。这一条是 zdoc 文档负责人审阅时发现的：原来删掉记录时，Fetch 会在组装时反复失败，且说不清原因。下线共享页要等 WP14。

### 2. 共享页记录没有飞书文档 ID

zdoc 原有的很多代码默认每条 canonical 记录都有飞书文档 ID。WP9a 逐个处理了这些地方，其中最要紧的一处：

- **换链接不等于删除记录**。增量抓取计划原来按文档 ID 跟踪记录，换掉链接后，旧 ID 会被当成“记录删除”，接着删掉这一页的输出。现在按记录 ID 跟踪，换链接只是“来源变了”。
- **快照中的记录格式**：表格快照 `guides-uat-last-success.json` 为共享页记录加了一种写法，`source_kind: shared-page`、`doc_token: null`。WP8 的 PR 校验读这个快照，也已经认得它。
- **文件扩展名不变**：线上已有的页面是 `.md` 就仍写 `.md`，全新页面用 `.mdx`。扩展名一变，下游的翻译会把它当成删掉了一页、新增了一页。
- **只有 Guides 用新的链接分类**：SDK 参考的 Drive 表格中，记录的链接是 `/drive/folder/<ID>` 这样的文件夹地址。`larkDocScraper.js` 取文档 ID 时，Drive 表格仍用原来的写法，不经过 Guides 的分类。

### 3. 生成：每页一次，两个手册一起

在抓取原文的任务中，对每条共享页记录运行一次 `shared-docs build --page <页面标识>`，一次得到 Guides 与 BYOC 两份 MDX，成功还是保留旧版也只判断这一次。

- 原文按这一页 `lock.yaml` 锁定的 milvus-docs 提交读取，不读分支的最新提交。
- 导航用的 `sidebar_label`、`sidebar_position` 取自这次读到的飞书记录。
- front matter 写 `token: shared-<页面标识>`，以及 `custom_edit_url`（指向 milvus-docs 上原文的编辑页）。
- 表格中没有被选中的页面目录，Fetch 不读它的配置。所以某个还没激活的页面配置写错了，不会让 Fetch 失败。

### 4. 图片

在同一个任务中，与飞书图片的上传放在一起。每张图按内容摘要命名为 `shared/<摘要>.<扩展名>`：

1. 存储中已有这个对象：读回核对摘要，不重新上传，也不改它的权限。
2. 没有：用“对象不存在才创建”的方式上传，设为公开可读，再读回核对摘要。

任何一张失败，报 `PUBLISH_IMAGE_UPLOAD_FAILED`，这次运行的英文 Guides 不发布，与飞书图片上传失败时相同。原有的上传函数没有改。

### 5. 第一次激活：保住其他页面指向它的链接

其他飞书页面链接到这一页时，链接中写的是它原来的飞书文档 ID，锚点是飞书的块 ID。第一次激活时：

1. 从上一次成功的快照中取出这条记录原来的飞书文档 ID；
2. 重新抓一次原来的飞书文档，只取其中的标题块；
3. 扫描这次运行中抓到的所有页面，找出指向它的链接；
4. 把每个被链接的块 ID 换算成锚点，在两份 Git 版 MDX 中都找得到，才算通过。

结果记进 `active.json`：

```json
{
  "page": "delete-entities",
  "record": "rec…",
  "feishu_token": "<原来的飞书文档 ID>",
  "anchors": { "<被链接的块 ID>": "<Git 版的锚点>" },
  "activated_in": "<Fetch 运行编号>"
}
```

之后的运行不再抓旧文档：渲染其他飞书页面时，指向 `feishu_token` 的链接换成 `./delete-entities`，块 ID 按 `anchors` 换成锚点；块 ID 不在表中的，只指到页面顶部，并在运行摘要中列出。

### 6. 写入 dev：同一个提交

组装时，在这次 Guides 检查点中写入：

- 两个手册的页面；
- 记录文件 `generated/en/manifests/shared-pages/guides/delete-entities.json`，记下这次用到的每个输入的摘要和输出的摘要；
- `active.json`，只在第一次激活时追加，已有的项不改；
- `_publication.json`，组装时的校验依据。

它们和导航在同一个 dev 提交中，不会出现页面换了、清单还没换的情况。

### 7. 及时生效

组装身份与缓存原来只看飞书侧有没有变化。现在 `shared-docs/guides/` 的内容、各页 lock 锁定的提交也算在内：只改了 Cloud 的变量或升级了 lock，飞书没有任何变化，下一次 Fetch 也会重新生成这一页。

### 出错时，影响多大

| 情况 | 影响范围 | 错误码 |
|---|---|---|
| 这一页生成失败、链接或图片解析不了、发布目标或路径与 `page.yaml` 不一致、被链接的锚点在 Git 版中找不到、旧文档抓不到 | 只影响这一页：两个手册都保留 dev 上现有的版本，其他页面照常发布 | `ACTIVATE_CHECK_FAILED`、`OWNERSHIP_PATH_MISMATCH`、`OWNERSHIP_CONFIG_MISSING` |
| 图片上传或读回核对失败 | 这次运行的英文 Guides 不发布 | `PUBLISH_IMAGE_UPLOAD_FAILED` |
| 已激活的页面被改回飞书链接，或记录被删除、降级 | Fetch 停下，网站保持 Git 版 | `OWNERSHIP_REVERTED` |

失败的页面和原因写进 `guides-shared-publication.json`，并出现在 Fetch 的飞书卡片中。

## 一个例子：激活 Delete Entities

前提：Delete Entities 的原文已在 milvus-docs 对齐（[milvus-io/milvus-docs#3719](https://github.com/milvus-io/milvus-docs/pull/3719)、[#3722](https://github.com/milvus-io/milvus-docs/pull/3722)），页面配置已合并到 zdoc master（[zilliztech/zdoc#861](https://github.com/zilliztech/zdoc/pull/861)，lock 锁在 `3e6b749`）。WP9a 合并后：

1. **推动者**在飞书表格中，把 Delete Entities 记录的 `Docs` 换成上面的页面目录地址。其他列不动，原来的飞书文档先保留。
2. **等下一次定时 Fetch**（北京时间 10:00、18:00、02:00），或手动运行一次 `fetch-docs.yml`；只激活 Guides 页面时可以加 `-f group=guides`。
3. **Fetch 中**：
   - 认出这条记录是共享页；
   - 按 `3e6b749` 读原文，生成 Guides 与 BYOC 两份页面；
   - 这一页没有图片，所以不上传；
   - 重新抓一次旧文档，核对其他页面指向它的锚点。
4. **dev 上的一个提交中**出现：
   - 两份页面，仍是原来的 `.md` 文件；
   - `delete-entities.json` 记录文件；
   - `active.json`，其中一项是 `delete-entities`。
5. **部署 UAT**，验收页面：8 种语言的代码 Tabs、连接处显示 `YOUR_CLUSTER_ENDPOINT`、“编辑此页”指向 milvus-docs 的原文。
6. **确认 `active.json` 里有这一页、UAT 验收通过后**，再停用原来的飞书文档。之后其他页面指向它的链接只靠 `active.json` 换算。

建议激活前先跑一次不换链接的 Fetch，确认它写入 dev 的结果正常，再换链接。这样激活出了问题，不会与其他改动混在一起。

## 自己试一试

在 zdoc 检出中更新到最新的 master，然后在仓库根目录运行：

```bash
corepack enable && pnpm install --frozen-lockfile
```

```bash
pnpm test:replay:shared-pages
```

约一分多钟，10 项全部通过。它在临时目录中建本地的 Git 远端、合成的飞书表格快照与一个本地的图片存储，用正式的生成、渲染、组装、检查点代码跑完整的 Fetch。第一项会：

- 把一篇合成页面的 `Docs` 换成页面目录地址；
- 检查页面、导航、记录文件、`active.json` 都在同一个本地 dev 提交中；
- 检查另一篇飞书页面中指向它的两处链接，分别渲染成 `./<页面标识>` 和 `./<页面标识>#<锚点>`。

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `scripts/docs-workflow/replay-shared-pages.test.js` | 10 个完整场景：激活、只改 Cloud 配置时重新生成、单页失败保留旧版、图片上传失败、改回飞书链接、指定页面抓取、NEXT 与下线页面的保留 |
| `scripts/docs-workflow/guides-shared-sources.test.js` | 抓取原文任务中的生成：两个手册、扩展名、第一次激活的锚点核对、旧文档抓不到时只影响这一页、记录被删除或降级时报 `OWNERSHIP_REVERTED` |
| `packages/docs-tooling/src/lark/sharedPageRouting.test.js` | `Docs` 链接的识别规则、换链接不算删除记录、改回飞书链接时失败 |
| `packages/docs-tooling/src/lark/sharedImageUploader.test.js` | 有条件的创建、公开可读、已存在的对象不改权限、读回核对失败 |

## 刻意没做的

- **WP9b**：写 dev 前按记录文件重新生成一遍比对，已采用的图片不随原地址变化。WP9a 合并后再做。
- **WP14**：激活前的“比较”运行、下线共享页、旧的飞书任务不能改写已迁移的页面、拦截直接修改 dev 中生成结果的 PR。
- **在 Fetch 中为未激活的页面生成候选**：PR 校验（WP8b）已经能看到。
- **NEXT 内容中标题的跳转**：链接跳到 NEXT 内容里的标题时页面不滚动，这是网站原有的问题，与 WP9 无关，记为 [zilliztech/zdoc#864](https://github.com/zilliztech/zdoc/issues/864)。

## 已知的问题

- **图片存储还没在真实环境中验证**：有条件的创建是否支持、公开读取是否可用、`shared/` 会不会被生命周期规则清理，都要在第一篇带图片的页面激活前查清（zdoc 文档负责人审阅意见 P1-2）。Delete Entities 没有图片。
- **`active.json` 只记一个飞书文档 ID**：同一篇文档如果被人用另一种链接格式引用，激活后不会被换算。改为记录全部别名，放在 WP9b。
- **每次运行都完整克隆 milvus-docs**：页面少时不影响，激活的页面多起来之前要加缓存。
- **合并后的第一次 Fetch 会慢一些**：组装身份把新增的模块算了进去，第一次会重新渲染全部 Guides 表，结果应与之前相同。

## 审阅与真实运行中发现的问题

| 问题 | 怎样发现 | 处理 |
|---|---|---|
| 删掉已激活的记录时，Fetch 在组装时反复失败，说不清原因（P1-1） | zdoc 文档负责人读代码 | `dd64b581c`：抓取原文时先核对 `active.json` 中的每条记录，不在或不再是可发布的 canonical 记录，就报 `OWNERSHIP_REVERTED`，见第 1 节 |
| SDK 参考的 6 个 Drive 表格生成失败（P0） | 文档负责人的只生成不发布的真实 Fetch（运行 `40438506088`） | `cf376e013`：Drive 表格的文档 ID 恢复原来的写法，见第 2 节。新增的回归测试把真实格式的表格记录一路跑到写出文件，只模拟飞书的响应 |
| 中文 Guides 抓取报 341/342 不完整 | 同一次运行 | 不是 WP9 引起的：一条中文记录被同事有意换成了 wiki 之外的独立 docx，原有代码不支持这种文档。修复单独提交为 [zilliztech/zdoc#867](https://github.com/zilliztech/zdoc/pull/867)，先于 #863 合并 |

原有的测试没有发现 P0：Drive 的单元测试直接填好了文档 ID 映射，命令行测试把抓取和写出都换成了模拟。因此，以后改动飞书记录的解析，合并前要先对一个 SDK 分组跑一次只生成不发布的 Fetch。

## 证据

- agent 交付时：`pnpm test:shared-docs` 537 个通过、4 个跳过；`pnpm test:replay:all` 通过；用 zdoc 保留的真实 Fetch 运行记录（`40259363946`）回放，20 个本地事务成功，两种发布顺序得到同一棵树。
- 审阅人在 `35176d996` 上重跑 shared-docs、共享页回放、工作流规则检查与类型检查，结果相同；P1-1 的修复（`dd64b581c`）跑过 `pnpm test:for-change` 选出的全部检查，包括 `test:replay:all`（2026-10-27）。
- zdoc 文档负责人在 `35176d996` 上独立重跑了主要测试，并确认不换 `Docs` 链接时这些改动完全不生效。他的只生成不发布的真实 Fetch（运行 `40438506088`）发现了上表中的 P0。
- 修复后，agent 的 `pnpm test:replay:all` 65 项全部通过；文档负责人把 #863 与 #867 合在一起（`99e51b9fc`）重跑真实 Fetch（运行 `40458642814`），成功后合并。
