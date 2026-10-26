# WP9 接入 Fetch：生成与交接

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP8](./WP8-zdoc-build-and-validate.md) 已合并（WP8a [zilliztech/zdoc#822](https://github.com/zilliztech/zdoc/pull/822)，WP8b [#832](https://github.com/zilliztech/zdoc/pull/832)，commit [`8680736`](https://github.com/zilliztech/zdoc/commit/86807361cdca0f2b768f51d7ff47c5b78461bee8)）。改动 Fetch，计划与上游 PR 都要 zdoc 文档负责人 review　**状态**：未开始

## 目标

做完后，zdoc 的发布工作流 Fetch：

- **每次运行都生成全部共享页**：用 master 上的 `shared-docs/` 与工具，跑一遍 `shared-docs build`，结果留在这次运行的产物中。生成失败只报告，不让 Fetch 失败。这一页还没激活，网站上仍是飞书版。
- **对已激活的页面，把结果交给发布**：
  - 页面 MDX 放进 Guides 的组装目录，替换飞书渲染的同一页；
  - 写入每页的记录文件；
  - 上传还不存在的图片；
  - 写 dev 之前，按记录文件重新生成一遍并比对。

  这些任何一步失败，这一页保留 dev 上现有的版本，其他页面照常发布。
- **dev 上的共享页生成结果不能被手改**：修改它们的 PR，检查失败，并指出应改的源文件。

哪些页面已激活，读 dev 上的 `generated/en/manifests/shared-pages/active.json`（格式见技术设计 05b）。这个文件由 WP14 生成；现在 dev 上还没有它，就当作没有页面激活。所以 WP9 合并后，网站不会有任何变化。真正的第一次写入在 WP14 激活第一篇页面时发生。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 第 6 节：发布保护、及时生效、时延；场景 5：系统行为 5-3、5-5、5-6；场景 9：系统行为 | 行为 |
| [技术设计 05](../../design/05-publish-handoff.md) | 全文 | 交接物、记录文件的格式、图片上传、发布保护、缓存与运行、出错时 |
| [技术设计 05b](../../design/05b-cutover-and-ownership.md) | 生效配置、切换与激活、激活之后的归属规则 | `active.json` 的格式；哪些归 WP14 |
| [技术设计 02b](../../design/02b-links-and-images.md) | 图片 | 已采用版本的图片以第一次转存为准 |
| [技术设计 08](../../design/08-workflows-and-permissions.md) | 现有做法、失败通知 | 并发组、飞书卡片 |
| [技术设计 09](../../design/09-error-catalog.md) | 发布与切换 | 错误码 |
| [实施计划](../../phase-1.md) | 6.1 节中的“Fetch 的接入点”“重新生成比对的接法” | 要在计划中回答的两项 |
| [WP8 走读](../walkthroughs/WP8.md) | 全文 | 要接入的生成命令 |
| [实现指南](../README.md) | 第 3 节 L4、第 5 节 | 回放测试、规则 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `.github/workflows/fetch-docs.yml`：新增调用生成共享页的任务 | 其他工作流的行为，除非计划审阅时批准 |
| 新建 `.github/workflows/_render-shared-pages.yml`（或计划中提出的等价写法） | |
| `.github/workflows/_assemble-guides.yml`：恢复共享页的产物，对已激活的页面替换组装目录中的同一页 | 飞书侧的抓取与渲染逻辑：WP14 再让飞书跳过 `git` 记录 |
| `scripts/docs-workflow/` 中组装、校验、检查点相关的脚本：只做接入共享页所需的最小改动 | `lark/` 中的记录语义（placement type `git` 归 WP14） |
| `packages/docs-tooling/src/shared-docs/` 下：记录文件、重新生成比对、图片上传的代码与测试；`commands/` 新增需要的子命令 | `active.json` 的生成与比较运行（WP14） |
| 图片上传：复用 zdoc 现有的图片存储上传代码，实现 WP0 定义的 `ImageStore` 适配器 | 翻译清单、恢复脚本、缓存（WP15） |
| 回放测试：复用 zdoc 现有的回放测试工具（`pnpm test:replay`） | 真实的 dev 分支、真实的图片存储：测试中都用隔离的替身 |
| `scripts/docs-workflow/test-matrix.json`、工作流规则检查与测试 | |
| `spec/pending.json`：删掉本工作包的编号；把下表中改归 WP9 的三个错误码改为 `"WP9"` | `spec/requirements.json` |

## 怎样接

### 每次运行都生成（候选）

- **触发**：Fetch 的每次运行，定时与手动都算，都新增一个任务，和 Guides 各表的渲染并行。
- **输入**：master 上的工具与 `shared-docs/`（技术设计 05：不必等 master→dev 同步）；milvus-docs 跟踪分支的检出，要求与 WP8 相同：本地分支、完整历史；dev 的组装基线。
- **输出**：每页、每个手册的 MDX，`images.json`，每页记录文件的草稿，都放进这次运行的产物中，不写 dev。
- **失败**：
  - 仓库根目录没有 `shared-docs/` 时，这个任务直接成功；
  - 生成失败时，在运行摘要与飞书卡片中列出页面与错误，Fetch 照常继续；
  - 只有已激活的页面失败才影响它自己：保留 dev 上现有的版本（产品需求 9-1）。
- **及时生效**：共享页每次都重新生成，不读飞书侧的“未变化”缓存。所以只改了 Cloud 的变量或内容文件，下一次运行也会生效（产品需求第 6 节）。

### 交接（只对已激活的页面）

1. **页面 MDX**：在 `_assemble-guides.yml` 中恢复共享页的产物，用 Git 生成的 MDX 替换组装目录中同一路径上的文件，两个手册分别替换。导航仍按飞书记录生成，与技术设计 05b 中的“导航（Phase 1）”相同。
2. **记录文件**：
   - 按技术设计 05 的格式，写到 `generated/en/manifests/shared-pages/<页面标识>.json`，与页面 MDX 在同一个 dev 提交中；
   - `inputs` 中的摘要都按实际读到的字节计算；
   - `outputs` 是最终写入 dev 的 MDX 的摘要。
3. **图片**：
   - 沿用 Fetch 的 `media_upload_mode`：`write` 时，把存储中还没有的对象按 `shared/<摘要>.<扩展名>` 上传，上传后读回核对摘要；`skip` 时只算地址；
   - 已存在的对象不覆盖；
   - 任何一张失败，这次运行不写 dev，报 `PUBLISH_IMAGE_UPLOAD_FAILED`。
4. **已采用的图片不变**：上一次的记录文件中记过的图片，把“原地址 → 摘要”作为 `recorded` 传给 WP5。原地址内容变了时，沿用记录的摘要，发飞书卡片通知文档工程师（`IMAGE_SOURCE_CHANGED`，不算错误）。
5. **重新生成比对**：写 dev 之前，按记录文件中的输入，在一个干净的目录中重新生成，与 `outputs` 的摘要逐个比对。不一致时这次运行不写这一页，报 `PUBLISH_REGEN_MISMATCH`，指出不一致的文件。
6. **编辑入口**：生成的页面在 front matter 中加 `custom_edit_url`，指向 milvus-docs 跟踪分支上原文的编辑页（`https://github.com/milvus-io/milvus-docs/edit/<跟踪分支>/<source.file>`）。这样预览与网站上的“编辑此页”指向真正的源文件，而不是生成的 MDX（技术设计 05 的“源 PR”一行，技术设计 07 的 front matter 表）。WP4 的站点适配要能接受这个字段，计划中说明怎样传入。

### dev 上的保护

有 PR 修改 dev 中已激活页面的生成结果（MDX 或记录文件）时，检查失败，报 `PUBLISH_REGEN_MISMATCH`，指出应改的源文件：`shared-docs/pages/<页面标识>/` 或 milvus-docs 的原文。判断依据是 `active.json` 与记录文件中的 `outputs` 摘要。由哪个现有检查承担，在计划中提出，例如站点校验中的 “Gate dev-owned paths”。Fetch 自己写 dev 的提交要能通过。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `5-3` | 图片存储中已有的对象不覆盖；同一张图被两个版本、两个页面引用时只上传一次；在回放测试中，一页的图片换了之后，旧对象仍在 |
| `T06` | 回放测试中激活一篇合成的页面，组装后的站点试构建通过。检查 Tabs 可切换、语言完整，锚点、导航、链接、图片、编辑入口都正确；缺图、图片字节变化、不认识的写法都让这一页失败 |
| `PUBLISH_IMAGE_UPLOAD_FAILED`（从 WP14 改归 WP9） | 上传失败、上传后读回的摘要不一致，各一个样例；这次运行不写 dev |
| `PUBLISH_REGEN_MISMATCH`（从 WP14 改归 WP9） | 写 dev 前重新生成不一致；PR 修改了 dev 中已激活页面的 MDX；PR 修改了记录文件，各一个样例 |
| `IMAGE_SOURCE_CHANGED`（从 WP14 改归 WP9） | 记录中的图片在原地址被同名覆盖：沿用记录的摘要，发出通知，不失败 |

另外两条不对应编号，但要有测试：

- **候选失败不影响 Fetch**：一篇没激活的共享页生成失败，Fetch 其余部分照常成功，运行摘要中列出错误。
- **没有 `active.json` 时什么都不交接**：dev 与合并前逐字节相同，只多了这次运行的候选产物。

## 完成的定义

- [ ] `pnpm test:shared-docs`、`pnpm test:workflow-policy`、`pnpm test:replay` 与 `pnpm test:for-change` 给出的全部命令通过；`pnpm typecheck` 通过
- [ ] 回放测试：在隔离的本地 Git 远端上，用一份合成的 `active.json` 激活一篇合成的页面，一次 Fetch 在同一个 dev 提交中写入 MDX 与记录文件；再改一次 Cloud 的变量，下一次运行重新生成并更新这两样
- [ ] 没有激活任何页面时，Fetch 写入 dev 的内容与合并前逐字节相同
- [ ] 在 fork 中手动运行一次 Fetch 的候选部分（不写 dev、不上传图片），把运行链接写进 PR 说明。不能运行时说明原因
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写，“How to try it”演示回放测试

## 计划中要回答、并请 zdoc 文档负责人确认的事

实施计划 6.1 节把下面两项留给 zdoc 维护者。WP9 的计划要基于 zdoc 现有的代码给出具体方案；计划审阅时，推动者把计划转给文档负责人确认，确认后才开始实现。

1. **Fetch 的接入点**：
   - 生成共享页的任务放在哪里、需要哪些检出与密钥；
   - 共享页的产物怎样进入 `_assemble-guides.yml`，参照各表渲染结果的恢复方式；
   - 组装身份、缓存、检查点、覆盖率检查（如 `validate-guides-coverage.js`）中，哪些要认得共享页，哪些先不动、留给 WP14。
2. **重新生成比对的接法**：
   - 写 dev 前的比对放在哪一步；
   - dev 上的保护由哪个现有检查承担。
3. **图片存储**：
   - 复用哪段现有的上传代码；
   - `shared/` 前缀下的对象是否会被存储的生命周期规则清理（产品需求 5-3 要求不能）。

## 不做

- placement type `git`、`active.json` 的生成、激活前的“比较”运行、归属规则（飞书让路、不许重复、旧任务遵守归属）：WP14。WP9 只在组装时让 Git 的结果替换同一路径上飞书渲染的文件。WP14 接入后，飞书会跳过 `git` 记录，同一路径上再出现两个来源时改为报 `OWNERSHIP_DUPLICATE_PATH`。
- 翻译清单读记录文件、恢复脚本、缓存的身份：WP15。
- 两版合并：WP11。两个版本不同的页面，按 WP8 的做法拒绝，并作为这一页的失败处理。
- 中文站：Phase 1 共享页只发英文站的 Guides 与 BYOC。

## 已知的坑

- Fetch 很长，中位 69 分钟，而且与 Translation 共用串行队列 `docs-production-dev`。改动要能在回放测试中验证，不靠真实运行来试。
- 组装阶段有严格的身份核对（`guides-assembly-identity.js` 等）。共享页的产物要纳入它，不能绕开。
- 生成共享页时的 dev 基线，要与这次运行的组装基线是同一个提交，否则链接查找用到的 Cloud 页面清单可能不一致。
- 图片下载在 GitHub 的 runner 上通常很快，但仍要用 WP8 的 `--image-timeout`，不要把超时写死。
- 要另起进程的测试，按 [#824](https://github.com/zilliztech/zdoc/pull/824) 设 120 秒的文件级时限。
