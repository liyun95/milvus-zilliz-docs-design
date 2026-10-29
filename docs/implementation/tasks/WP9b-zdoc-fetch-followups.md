# WP9b Fetch 收尾：写 dev 前的保护与真实运行的遗留问题

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP9a](./WP9-zdoc-fetch-handoff.md) 已合并（[zilliztech/zdoc#863](https://github.com/zilliztech/zdoc/pull/863)），[WP11](./WP11-zdoc-two-version-merge.md) 合并后开始（要用它的 `BuiltPage.notes`）。改动 Fetch，计划与上游 PR 都要 zdoc 维护者 review　**状态**：未开始

## 目标

WP9a 上线后，共享页已经分三批在生产上由 Git 生成（2026-10-29 共 15 篇接入，前 12 篇已上 Prod）。WP9b 补上 WP9 任务卡中留到第二个 PR 的两项保护，并收拢审阅与真实运行中记下的遗留问题。做完后：

- 写 dev 前，每一页按记录文件重新生成一遍并比对，不一致的页面保留 dev 中现有的版本（`PUBLISH_REGEN_MISMATCH`）；
- 已经采用的图片不随原地址的内容变化（`IMAGE_SOURCE_CHANGED`）；
- 同一篇飞书文档用任何一种链接格式引用，激活后都能换算到共享页；
- 记录文件中有两版 front matter 不同的备注；
- 失效链接报告不再误报指向已激活页面的链接；
- 删除命名块后不留多余的空行（4-3）；
- Fetch 侧已有的测试计入编号覆盖检查，`pending.json` 与实际覆盖一致。

不换任何 `Docs` 链接时，Fetch 写入 dev 的内容与改动前逐字节相同；已激活的页面，生成结果除了删除块后的空行，也与改动前相同。

分两个 PR 交付：

| PR | 内容 | 审阅 |
|---|---|---|
| **WP9b-1** | 只改 `packages/docs-tooling/src/shared-docs/`：删除后的空行、`failures` 死代码、同步需求清单 | 发 FYI 给 zdoc 维护者，校验通过后合并 |
| **WP9b-2** | Fetch：重新生成比对、已采用的图片、别名、旧文档的抓取条件、记录文件的 `notes`、失效链接报告、编号覆盖 | zdoc 维护者 review |

WP9b-1 改变已激活页面的生成结果（只少了空行），要单独合并、单独经过一次 Fetch，再开始 WP9b-2 的比对。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [WP9 任务卡](./WP9-zdoc-fetch-handoff.md) | 写 dev 前的保护（WP9b）；计划中要回答的事第 6 条 | 两项保护的原定方案 |
| [WP9 走读](../walkthroughs/WP9.md) | 已知的问题；审阅与真实运行中发现的问题 | 遗留问题的来历 |
| [技术设计 05](../../design/05-publish-handoff.md) | 记录文件；发布保护 | `inputs`、`outputs`、`notes` 的格式 |
| [技术设计 05b](../../design/05b-cutover-and-ownership.md) | `active.json`；指向已激活页面的链接 | 别名要改的格式 |
| [技术设计 02b](../../design/02b-links-and-images.md) | 图片 | 已采用版本的图片以第一次转存为准 |
| [技术设计 09](../../design/09-error-catalog.md) | 发布与切换 | `PUBLISH_REGEN_MISMATCH`、`IMAGE_SOURCE_CHANGED` |
| [产品需求](../../prd.md) | 场景 4 的 4-3；场景 9；第 6 节“发布保护” | 行为 |
| [实现指南](../README.md) | 第 2.1、3 节 L4、第 5 节 | 需求清单、回放测试、规则 |

## 范围

| 可以改 | 不能改 |
|---|---|
| WP9b-1：`packages/docs-tooling/src/shared-docs/` 下的代码、测试、README；`spec/requirements.json` 按本仓库的 [`requirements.json`](../requirements.json) 同步 | `apps/docs/`、`packages/docs-ui/` |
| WP9b-2：`packages/docs-tooling/src/lark/`、`scripts/docs-workflow/` 中共享页相关的模块与测试；`spec/coverage.ts`、`spec/pending.json` | 与共享页无关的 Fetch 逻辑；`.github/workflows/` 中的触发、并发与权限 |
| 两个 PR：回放测试的 fixture | `shared-docs/` 下的真实页面配置；真实的 dev 分支、图片存储、飞书表格 |

## 怎样实现

### WP9b-1：shared-docs

1. **删除后的空行（4-3）。** 现在删除一个命名块，会连同标记行一起去掉块的内容，块前和块后各留下一个空行，MDX 中出现两个连续的空行。第三批的 Stop 删掉两个块，就多了两个空行。改为删除后只留一个空行，和 `add` 现在的处理（`core/transforms/spacing.ts`）一致。补一个用例：命名块两侧各有一个空行，删除后前后的块之间只剩一个空行；删除位于文件开头和结尾的块时，不留空行。
2. **`failures` 死代码。** WP11 之后 `buildPage` 不再产生 `BuildFailure`，删掉这个类型和返回值中的 `failures`，以及调用处的处理。行为不变。
3. **同步需求清单。** 把本仓库的 `requirements.json` 复制为 `spec/requirements.json`。两份清单的 `9-3`、`OWNERSHIP_REVERTED` 的文字与 `source.prd_commit` 不同，逐字节复制。

### WP9b-2：Fetch

4. **重新生成比对。** 按 WP9 任务卡“写 dev 前的保护”第 1 条做：在抓取原文的任务中，按记录文件中的输入（`inputs.dev`、`inputs.fetch`）在干净的目录中重新生成，与 `outputs` 的摘要逐个比对；记录文件与输出的核对加进检查点事务的 `validationCommands`。不一致时这一页保留 dev 中现有的版本，报 `PUBLISH_REGEN_MISMATCH`，指出不一致的文件。
   - 同时检查：图片地址的改写是整页的字符串替换（`guides-shared-sources.js` 把 MDX 中的 `shared/<sha>.<ext>` 一律换成完整地址），代码块中出现同样的字符串时也会被替换。比对要能发现这种情况。
   - 生产环境中没有设置 `IMAGE_BED_URL` 时，现在会悄悄用默认的存储桶。改为必须设置，没有设置时 Guides 失败。
5. **已采用的图片不变。** 按 WP9 任务卡第 2 条做：上一次的记录文件中记过的图片，把“原地址 → 摘要”作为 `recorded` 传给 WP5（`core/links/rewrite.ts` 已经支持）。原地址的内容变了时沿用记录的摘要，发飞书卡片通知文档工程师（`IMAGE_SOURCE_CHANGED`，不算错误）。
6. **`active.json` 记录全部别名。** 现在 `feishu_token` 只记一个文档 ID（`doc_token` 或 `node_token`）。同一篇文档用 `docx/<obj_token>` 等另一种格式引用时，激活时登记不到，之后也不会被换算。改为记录这条记录的全部别名（`doc_token`、`node_token`、`origin_node_token`、`obj_token`，与 `incrementalFetchPlanner.js`、[zilliztech/zdoc#907](https://github.com/zilliztech/zdoc/pull/907) 中 `validate-guides-source-contract.js` 认的一组相同），激活时的扫描与之后的换算都按任一别名匹配。格式见下文“决定”第 1 条；已有的记录在下一次 Fetch 中补齐别名，不要求重新激活。
7. **只在需要锚点时抓取旧文档。** 现在激活时总是重新抓取原来的飞书文档。改为只在有带锚点的链接指向它时才抓取；没有这种链接时，旧文档已经删掉也能激活。WP9a 中有 5 个测试的 fixture 假定总是抓取，按新的条件更新。
8. **记录文件的 `notes`。** WP11 的 `BuiltPage.notes`（两版 front matter 不同、已沿用 `current`）写进记录文件的 `notes[]`，格式见技术设计 05。
9. **失效链接报告。** `guides-broken-content-links.json` 把指向已激活页面的飞书链接列为 “missing canonical”。页面中的链接是对的，报告不知道旧的飞书文档 ID 已由共享页接管。改为按 `active.json` 的别名识别这些链接，不再列出。
10. **编号覆盖。** zdoc 的编号覆盖检查（`spec/coverage.ts`）只扫描 shared-docs 下的 `*.test.ts(x)`。WP9a 的测试在 `scripts/docs-workflow/` 与 `lark/` 中，是 `.js` 文件，所以 `pending.json` 中 `9-1`、`9-2`、`9-3`、`9-6`、`ACTIVATE_CHECK_FAILED`、`OWNERSHIP_PATH_MISMATCH`、`OWNERSHIP_CONFIG_MISSING`、`OWNERSHIP_REVERTED`、`PUBLISH_IMAGE_UPLOAD_FAILED` 仍记在 WP14 名下（`T06` 记在 WP9 名下）。做法见“决定”第 2 条。

## 决定

推动者在写卡后确定（2026-10-29）：

1. **别名的格式。** 在 `pages[]` 中增加 `feishu_aliases`（字符串数组），包括 `feishu_token` 本身；`feishu_token` 保留不变，旧的读取代码不受影响。格式已写入[技术设计 05b](../../design/05b-cutover-and-ownership.md)。不把 `feishu_token` 改成数组：那样所有读取 `active.json` 的地方都要同时改。
2. **Fetch 侧测试怎样计入覆盖。** 扩展 `spec/coverage.ts`，同时扫描共享页相关的 `.js` 测试（`scripts/docs-workflow/` 与 `lark/` 中的），在这些测试的标题中写上编号，再把上面的编号从 `pending.json` 中删掉。扫描哪些文件在计划中列出。不只把归属从 WP14 改成 WP9：那样检查看不到它们是否真的有测试。
3. **只剩一个三级标题时的警告：这次不做。** [产品需求场景 4](../../prd.md#场景-4写-cloud-的差异)已规定作者在删除时一起删掉单独剩下的三级标题，工具不自动删；等出现漏删再加提示。

## 计划审阅的决定

在 [liyun95/zdoc#15](https://github.com/liyun95/zdoc/pull/15) 中审定，以 PR 中的[裁决评论](https://github.com/liyun95/zdoc/pull/15#issuecomment-6489562573)为准。要点：

| 问题 | 决定 |
|---|---|
| WP9b-2 改到 shared-docs 与飞书卡片 | 允许小范围修改 `build-page.ts`、`core/handoff/` 中的状态与别名索引，以及 `collect-build-card-notes.js`（让 `IMAGE_SOURCE_CHANGED` 走现有的卡片） |
| 已有的 `active.json` 补别名 | 允许，只补 `feishu_aliases`，其他字段不变；技术设计 05b 已同步 |
| 找不到的别名 | 只警告，不冻结页面。只在 `active.json`、同一记录的旧源缓存、dev 上快照文件的历史中查找，不为此调用飞书 |
| 真实运行 | WP9b-2 合并前，zdoc 维护者跑两次只生成不发布的 Fetch：`guides` 与一个 SDK 分组，因为链接换算是各分组共用的代码 |
| 重新生成比对 | 用新记录文件中的输入重放并比对；旧记录文件在新工具下的结果只作升级对照，不拦发布 |
| 图片地址的整页替换 | 由比对发现，不改生成端 |
| `IMAGE_BED_URL` | 只在本次运行有共享页时检查；workflow 已经传入，不改 workflow；合并前由 zdoc 维护者确认仓库变量已设置 |
| 记录文件的 `notes` | 仍是字符串数组 |
| 计划文件 | 同 WP10、WP11：WP9b-1 从 master 开分支，不含计划；WP9b-2 标为 ready 前删除 `.claude/plans/` |

## 要覆盖的编号

| 编号 | PR | 怎样测 |
|---|---|---|
| `4-3` | 9b-1 | 命名块两侧各一个空行，删除后只剩一个；删除文件开头或结尾的块不留空行 |
| `9-3` | 9b-1 | 同步后的文字与需求清单一致，原有测试照常通过 |
| `PUBLISH_REGEN_MISMATCH` | 9b-2 | 记录文件的一项输出被改动、代码块中出现图片原地址：这一页保留 dev 中现有的版本，指出不一致的文件；其他页面照常发布。PR 修改 dev 的情况由 WP14 补测试 |
| `IMAGE_SOURCE_CHANGED` | 9b-2 | 记录中的图片在原地址被同名覆盖：沿用记录的摘要，发出通知，不失败 |
| 9b-2 第 10 条列出的编号 | 9b-2 | 现有测试的标题中写上编号，覆盖检查认到它们；`pending.json` 中不再有 |

另外几条不对应编号，也要有测试：

- 一篇飞书页面用 `docx/<obj_token>` 链接指向一篇已激活的页面：渲染为 `./<页面标识>`；激活时登记了全部别名。
- 激活一篇没有带锚点链接指向的页面，原来的飞书文档已删除：激活成功。
- 两版 front matter 不同的合成页面：记录文件的 `notes` 中有一条备注。
- 一篇飞书页面链接到已激活的页面：失效链接报告中不再出现。
- 生产环境没有设置 `IMAGE_BED_URL`：Guides 失败，并说明原因。

## 完成的定义

- [ ] `pnpm test:shared-docs`、`pnpm test:workflow-policy`、`pnpm test:replay:all`，以及 `pnpm test:for-change` 给出的全部命令都通过；`pnpm typecheck` 通过
- [ ] 编号覆盖检查通过，上表的编号不在 `pending.json` 中
- [ ] **WP9b-1**：用 master 上的 `shared-docs/guides/`（15 篇）与 milvus-docs `v3.0.x`，改动前后各生成一遍：12 篇没有变换的页面逐字节相同；3 篇带删除的页面只少了多余的空行。在 PR 说明中贴出比较方法与结果
- [ ] **WP9b-2**：表格中没有页面目录地址时，Fetch 写入 dev 的内容与合并前逐字节相同；用保留的真实 Fetch 记录回放，已激活的页面生成结果不变，比对全部一致
- [ ] **WP9b-2**：合并前，zdoc 维护者对 Guides 跑一次只生成不发布的真实 Fetch（[实现指南](../README.md)第 3 节 L4 的规则）
- [ ] 两个 PR 的说明都按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写

## 不做

- 激活前的“比较”运行、旧任务遵守归属、同一路径两个来源、下线、拦截修改 dev 中生成结果的 PR：WP14。
- 每次运行都完整克隆 milvus-docs：激活的页面多起来之前再加缓存，单独做。
- 可复用模块中写死的 Guides 路径（`sharedPageBundle.js`、`sharedPagePublication.js`）：在接入第二个组（Rust SDK Reference）之前做，放进那张卡。
- 翻译读记录文件、恢复脚本：WP15。
- 句子级的变换：见[技术设计 02 的设计理由](../../design/02-page-config.md#设计理由)。

## 已知的坑

- **WP9b-1 会改变已激活页面的生成结果。** 合并后的下一次 Fetch 会重新生成 3 篇带删除的页面，只少了空行。WP9b-2 的重新生成比对要在这次 Fetch 之后开始比，否则旧记录文件与新代码的结果不同。
- **回放测试覆盖不到真实状态。** WP9a 的三个问题都是真实运行中才发现的（见 WP9 走读）。别名与旧文档的改动都涉及飞书记录的格式，合并前必须跑一次只生成不发布的真实 Fetch。
- **别名来自快照。** 已激活的记录，`Docs` 已经换成页面目录地址，快照中可能不再有旧文档的全部 ID。计划中说明补齐别名时从哪里取（上一次飞书版的快照、Fetch 的源缓存），取不到时怎样处理。
- **不要在 dev 上补数据。** 已有的 `active.json` 由 Fetch 自己补齐别名，不手工改 dev。
