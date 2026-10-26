# WP9 接入 Fetch：按 `Docs` 链接分流与交接

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP8c](./WP8c-zdoc-group-layout.md) 已合并（`shared-docs/guides/` 的目录结构）。改动 Fetch，计划与上游 PR 都要 zdoc 维护者 review　**状态**：2026-10-26 按新的激活方式重写了任务卡；按旧卡写的计划（liyun95/zdoc#11）作废，要重写

## 目标

文档负责人在飞书表格中，把一页记录的 `Docs` 换成它在 zdoc master 上的页面目录地址（[技术设计 05b](../../design/05b-cutover-and-ownership.md#开关docs-链接)）：

```
https://github.com/zilliztech/zdoc/tree/master/shared-docs/guides/pages/delete-entities
```

做完 WP9 后，下一次 Fetch 就改由 Git 生成这一页，并写入 dev：

- **分流**：Fetch 照常读飞书表格。`Docs` 是页面目录地址的记录，不抓飞书正文，在渲染这一张 Guides 表时改用 `shared-docs build` 生成，结果放在飞书页面原本的位置。之后的组装、身份核对、检查点、导航都照常进行。
- **交接**：在同一个 dev 提交中写入两个手册的 MDX、每页的记录文件和 `active.json`；上传还不存在的图片。
- **保住链接**：其他飞书页面指向这一页的链接，包括带锚点的，按 `active.json` 换算，仍指向正确的位置。
- **及时生效**：只改了 milvus-docs 原文或 Cloud 配置、飞书没有变化时，下一次 Fetch 也会重新生成这一页。
- **出错只影响这一页**：检查不通过时，这一页保留 dev 上现有的版本，其他页面照常发布，并用飞书卡片通知文档负责人。

Fetch 不为还没激活的页面生成任何东西。表格中一个页面目录地址都没有时，Fetch 写入 dev 的内容与现在逐字节相同。

WP9 分两个 PR 交付：

- **WP9a**：分流、交接、链接、及时生效、图片上传，以及 Fetch 中的激活检查。合并后，第一篇试点页面就能激活。
- **WP9b**：写 dev 前的重新生成比对；已采用的图片保持不变。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [技术设计 05b](../../design/05b-cutover-and-ownership.md) | 开关；生效配置；指向已激活页面的链接；切换与激活的第 3–5 步；出错时 | 本工作包的主要行为 |
| [技术设计 05](../../design/05-publish-handoff.md) | 交接发生在哪里；交给发布的三样东西；记录文件；图片上传；缓存与运行；发布保护 | 交接物的格式 |
| [产品需求](../../prd.md) | 场景 9 的系统行为；场景 5 的 5-3；第 6 节中的“及时生效”“发布保护” | 行为 |
| [技术设计 02b](../../design/02b-links-and-images.md) | 图片 | 已采用版本的图片以第一次转存为准 |
| [技术设计 08](../../design/08-workflows-and-permissions.md) | 现有做法、失败通知 | 并发组、飞书卡片 |
| [技术设计 09](../../design/09-error-catalog.md) | 发布与切换 | 错误码 |
| [WP8 走读](../walkthroughs/WP8.md) | 全文 | 要接入的生成命令 |
| [实现指南](../README.md) | 第 3 节 L4、第 5 节 | 回放测试、规则 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/lark/` 中按飞书文档 ID 工作的模块（05b“开关”一节的表）：认得 `Docs` 是页面目录地址的记录；转换链接时先查 `active.json` | 飞书记录的其他语义：placement type 的取值、导航的生成、`Release Channel` |
| `scripts/docs-workflow/` 中渲染 Guides 表、组装身份、缓存、检查点相关的脚本：只做接入共享页所需的最小改动 | 其他工作流的行为，除非计划审阅时批准 |
| `.github/workflows/_render-guides-table.yml`、`_assemble-guides.yml`、`fetch-docs.yml`：接入所需的检出、步骤与产物 | 新开一条发布线，或新建一个并行的生成任务 |
| `packages/docs-tooling/src/shared-docs/` 下：`active.json`、记录文件、锚点、重新生成比对、图片上传的代码与测试；在 `commands/` 中新增需要的子命令 | 改写 `active.json` 中已有的页面：WP9 只在激活时加入，下线时的移除归 WP14 |
| 图片上传：在 zdoc 现有的上传代码旁新增一个“只上传、不覆盖”的函数，实现 WP0 定义的 `ImageStore` 适配器 | 现有上传函数（`larkImageDownloader.js` 的 `__uploadToS3`）的行为 |
| 回放测试：复用 zdoc 现有的回放测试工具（`pnpm test:replay`） | 真实的 dev 分支、真实的图片存储、真实的飞书表格：测试中都用隔离的替身 |
| `scripts/docs-workflow/test-matrix.json`、工作流规则检查与测试 | |
| `spec/pending.json`：删掉本工作包覆盖的编号 | `spec/requirements.json`：WP8c 已复制最新版本 |

## 怎样接

### 分流（WP9a）

- **认出共享页记录**：`Docs` 以 `https://github.com/zilliztech/zdoc/tree/master/shared-docs/` 开头，后面是 `<组>/pages/<页面标识>`，末尾可以带一个 `/`。
  - Phase 1 只认 `guides` 组。
  - 以下情况，这一行都失败（`OWNERSHIP_CONFIG_MISSING`）：
    - 页面目录在 master 上不存在、组不对，或地址写法不对；
    - canonical 记录的 `Docs` 既不是飞书文档链接，也不是页面目录地址。不能把它当成 `section` 处理，`guidesPlacementType` 现在就是这样做的。
- **按飞书文档 ID 工作的模块**：05b“开关”一节的表列出了已知的 8 个文件。计划中逐个说明怎样处理，再在全仓库搜一遍 `doc_token`，确认没有遗漏。还要在计划中写清两件事：
  - 换掉链接后，增量抓取计划会把旧 ID 看成“记录删除”。要查清这会触发什么（删除输出？删除译文？），并避免它发生。
  - 快照 `guides-uat-last-success.json` 中共享页记录的格式。WP8 的 PR 校验会读这个快照。
- **在哪里生成**：渲染这一张 Guides 表时，对共享页记录调用 `shared-docs build --page <页面标识>`，把两个手册的 MDX 放到飞书渲染这一页时本来要放的路径。
  - 渲染任务要有 milvus-docs 跟踪分支的检出，要求与 WP8 相同：本地分支、完整历史。
  - Cloud 页面清单用这次运行的组装基线，与 WP8 读 dev 的方式一致。
- **front matter**：
  - `token: shared-<页面标识>`（技术设计 05 的“页面身份”）；
  - `custom_edit_url` 指向 milvus-docs 跟踪分支上原文的编辑页：`https://github.com/milvus-io/milvus-docs/edit/<跟踪分支>/<source.file>`。WP4 的站点适配要能接受这个字段，计划中说明怎样传入。
  - `sidebar_label`、`sidebar_position` 按飞书记录填写。
- **及时生效**：组装身份（`guides-assembly-identity.js`）与缓存判断，要把 `shared-docs/guides/` 的内容和各页 lock 中的上游 commit 算进去。它们变了，增量计划就要把共享页所在的表标为需要重新渲染。

### 交接（WP9a）

1. **`active.json`**：Fetch 按表格生成，放在 `generated/en/manifests/shared-pages/guides/active.json`，格式见 05b。
   - 激活后的第一次 Fetch 加入一项：`feishu_token` 取自上一次成功的快照中这条记录的飞书文档 ID，`anchors` 的算法见下文。之后的运行照抄。
   - 已在清单中的页面，`Docs` 被改回飞书链接时，Fetch 失败（`OWNERSHIP_REVERTED`），页面保持 Git 版。
2. **记录文件**：按技术设计 05 的格式，写到 `generated/en/manifests/shared-pages/guides/<页面标识>.json`，与 MDX、`active.json` 在同一个 dev 提交中。
   - `inputs` 中的摘要都按实际读到的字节计算；
   - `outputs` 是最终写入 dev 的 MDX 的摘要。
3. **图片**：
   - 沿用 Fetch 的 `media_upload_mode`：
     - `write` 时，把存储中还没有的对象按 `shared/<摘要>.<扩展名>` 上传，上传后读回核对摘要；
     - `skip` 时只算地址。
   - 已存在的对象不覆盖。
   - 任何一张上传失败，这次运行不写 dev（`PUBLISH_IMAGE_UPLOAD_FAILED`）。
   - MDX 中的图片地址要带上 zdoc 现有的图片基地址 `IMAGE_BED_URL`，因为 WP5 返回的是相对路径 `shared/...`。
4. **Fetch 中的激活检查**（9-1 的 Fetch 部分）：
   - 能生成；
   - 图片与链接都能解析；
   - 记录的发布目标与路径与 `page.yaml` 的 `publish` 一致（`OWNERSHIP_PATH_MISMATCH`）；
   - 被其他页面链接的锚点都在 Git 版中（见下文）。

   任何一项不通过，报 `ACTIVATE_CHECK_FAILED`：这一页保留 dev 上现有的版本，用飞书卡片通知文档负责人，其他页面照常发布。

### 保住指向已激活页面的链接（WP9a）

- **转换**：渲染其他飞书页面时，链接中的文档 ID 等于 `active.json` 中某一项的 `feishu_token`，就换成 `./<页面标识>`。
  - 带块 ID 时，按 `anchors` 换成锚点；块 ID 不在 `anchors` 中时，只指到页面顶部，并在运行摘要中列出。
  - 可以复用现有的 `--linkShim`。计划中说明 `active.json` 怎样传到渲染各张表的任务中。
- **`anchors` 的计算**：在激活后的第一次 Fetch 中进行。
  1. 从上一次抓取的飞书原文中，找出被其他页面链接到的标题块；
  2. 按飞书版的标题，用 zdoc 现有的算法算出锚点；
  3. 在 Git 版中找同一个锚点。

  有找不到的，激活检查不通过，`detail` 中列出链接所在的页面。计划中要说明：上一次的飞书原文在这次运行中从哪里取（缓存、dev 还是快照）；怎样知道哪些块被链接过，因为现有的 `outgoing_tokens` 只记文档 ID，不记块 ID。

### 写 dev 前的保护（WP9b）

1. **重新生成比对**：写 dev 之前，按记录文件中的输入，在一个干净的目录中重新生成一遍，与 `outputs` 的摘要逐个比对。不一致时这一页不写，报 `PUBLISH_REGEN_MISMATCH`，指出不一致的文件。比对放在哪一步，在计划中提出。
2. **已采用的图片不变**：上一次的记录文件中记过的图片，把“原地址 → 摘要”作为 `recorded` 传给 WP5。原地址的内容变了时，沿用记录的摘要，并发飞书卡片通知文档工程师（`IMAGE_SOURCE_CHANGED`，不算错误）。

### 试点的激活

WP9a 合并后，Delete Entities 按以下步骤激活：

1. 用 `shared-docs build` 生成 Git 版，与 dev 中现有的 MDX 手工比较（比较运行由 WP14 提供）；
2. 文档负责人确认；
3. 在表格中换掉 `Docs`；
4. 等下一次 Fetch，或手动运行一次。

这一步由推动者与文档负责人在真实环境中进行，不交给 Agent。

## 要覆盖的编号

| 编号 | PR | 怎样测 |
|---|---|---|
| `3-6` | 9a | 页面目录已合并、表格中的 `Docs` 仍是飞书链接：Fetch 照常用飞书版，dev 与改动前逐字节相同 |
| `9-1`（Fetch 部分） | 9a | 生成失败、图片或链接解析失败、发布目标或路径不一致、被链接的锚点不在 Git 版中，各一个样例：这一页保留 dev 上现有的版本，其他页面照常发布 |
| `9-2` | 9a | 回放测试中激活一篇合成的页面：MDX、导航、记录文件、`active.json` 在同一个 dev 提交中 |
| `9-3` | 9a | `active.json` 中的页面，`Docs` 改回飞书链接：Fetch 失败，页面保持 Git 版 |
| `9-6` | 9a | 激活后，导航的位置、顺序、标签仍来自飞书记录；指向它的 `ref` 记录照常有效 |
| `9-9` | 9a | 一篇飞书页面中有两处链接指向被激活的页面，一处不带锚点、一处带块 ID：渲染结果分别是 `./<页面标识>` 与正确的锚点；激活之后新出现的块 ID 指到页面顶部，并在摘要中列出 |
| `5-3` | 9a | 图片存储中已有的对象不覆盖；同一张图被两个版本、两个页面引用时只上传一次；一页的图片换了之后，旧对象仍在 |
| `T06` | 9a | 回放测试中激活后，组装后的站点试构建通过：Tabs 可切换、语言完整，锚点、导航、链接、图片、编辑入口都正确；缺图、图片字节变化、不认识的写法都让这一页失败 |
| `PUBLISH_IMAGE_UPLOAD_FAILED` | 9a | 上传失败、上传后读回的摘要不一致，各一个样例；这次运行不写 dev |
| `ACTIVATE_CHECK_FAILED` | 9a | 见 `9-1` |
| `OWNERSHIP_PATH_MISMATCH` | 9a | 记录的发布路径与 `publish[].path` 不同 |
| `OWNERSHIP_CONFIG_MISSING` | 9a | 页面目录不存在；组不是 `guides`；`Docs` 既不是飞书链接也不是页面目录地址 |
| `OWNERSHIP_REVERTED` | 9a | 见 `9-3` |
| `PUBLISH_REGEN_MISMATCH` | 9b | 写 dev 前重新生成的结果不一致。PR 修改 dev 的情况由 WP14 补测试 |
| `IMAGE_SOURCE_CHANGED` | 9b | 记录中的图片在原地址被同名覆盖：沿用记录的摘要，发出通知，不失败 |

`pending.json` 中的归属：

- 上表中除 `5-3`、`T06`、`9-9` 以外的编号，现在都登记为 WP14，改为由 WP9 覆盖；
- `9-9` 是新增的编号，WP8c 复制需求清单时已经按 WP9 登记。

另外两条不对应编号，但也要有测试：

- **及时生效**：只改 Cloud 的变量、飞书没有变化时，下一次运行重新生成这一页，并更新记录文件。
- **没有共享页记录时什么都不变**：表格中没有页面目录地址时，一次 Fetch 写入 dev 的内容与改动前逐字节相同。

## 完成的定义

- [ ] `pnpm test:shared-docs`、`pnpm test:workflow-policy`、`pnpm test:replay`，以及 `pnpm test:for-change` 给出的全部命令都通过；`pnpm typecheck` 通过
- [ ] 回放测试：在隔离的本地 Git 远端上，用一份合成的飞书表格快照，把一篇合成页面的 `Docs` 换成页面目录地址。一次 Fetch 在同一个 dev 提交中写入 MDX、记录文件与 `active.json`；另一篇飞书页面指向它的链接与锚点都正确。再改一次 Cloud 的变量，下一次运行重新生成这一页并更新记录文件
- [ ] 表格中没有页面目录地址时，Fetch 写入 dev 的内容与合并前逐字节相同
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写，“How to try it”演示回放测试

## 计划中要回答的事

计划要基于 zdoc 现有的代码给出具体方案，推动者审阅后才开始实现。

1. **按飞书文档 ID 工作的模块**：逐个说明怎样处理；换掉链接后“记录删除”会带来什么后果；快照中共享页记录的格式。
2. **在哪里生成**：在 Guides 表渲染的哪一步调用，需要哪些检出与密钥；BYOC 手册中的同一页怎样放进去。
3. **组装身份与缓存**：哪些地方要把共享页的输入算进去。
4. **链接**：`active.json` 怎样传给各张表的渲染任务；计算 `anchors` 用的上一次飞书原文从哪里取；怎样知道哪些块被链接过。
5. **图片**：复用哪段现有的上传代码；在哪一步上传；`shared/` 前缀下的对象会不会被存储的生命周期规则清理（产品需求 5-3 要求不能清理）。
6. **重新生成比对**（WP9b）：放在写 dev 前的哪一步。

## 不做

- 以下归 WP14：激活前的“比较”运行；旧任务遵守归属（全量抓取、旧缓存、删除清单、恢复）；同一路径有两个来源；下线；拦截修改 dev 中生成结果的 PR。
- 在 Fetch 中为未激活的页面生成候选：PR 校验（WP8b）与比较运行（WP14）已经覆盖。
- 翻译清单读记录文件、恢复脚本、缓存的身份：WP15。
- 两版合并：WP11。两个版本不同的页面，按 WP8 的做法拒绝，作为这一页的失败处理。
- `guides` 以外的组、SDK Reference：由其他工作包做。它们会复用本工作包的 `active.json`、记录文件、图片上传与重新生成比对，所以这些代码不要写死 Guides。
- 中文站：Phase 1 的共享页只发英文站的 Guides 与 BYOC。

## 已知的坑

- Fetch 很长，中位 69 分钟，而且与 Translation 共用串行队列 `docs-production-dev`。改动要能在回放测试中验证，不要靠真实运行来试。
- 组装阶段有严格的身份核对（`guides-assembly-identity.js` 等）。共享页的输入要纳入核对，不能绕开。
- 飞书页面之间的链接找不到目标时，现在只打一行日志，链接变成普通文字，运行不会失败。所以 `9-9` 的测试要检查渲染结果中的链接本身，不能只看运行是否成功。
- 生成共享页时用的 dev 基线，要与这次运行的组装基线是同一个提交，否则链接查找用到的 Cloud 页面清单可能不一致。
- 图片下载在 GitHub 的 runner 上通常很快，但仍要用 WP8 的 `--image-timeout`，不要把超时写死。
- 需要另起进程的测试，按 [#824](https://github.com/zilliztech/zdoc/pull/824) 设 120 秒的文件级时限。
