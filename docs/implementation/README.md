# Phase 1 实现指南

**状态**：草稿，待确认。

本文面向实现 Phase 1 的实现 Agent 与审阅人，定义实现怎样切分、每一步怎样验证、怎样审阅。目标有两个：Agent 只读一张任务卡就能交付一个 PR；审阅人判断“做完了没有”时有客观依据，不靠感觉。

要交付什么行为见[产品需求](../prd.md)，工具怎样实现见[技术设计](../design/README.md)，排期与状态见[Phase 1 实施计划](../phase-1.md)。本文不重复它们，只规定实现过程。

## 1. 原则

| 原则 | 落到哪里 |
|---|---|
| **每条需求都有测试** | 产品需求的每条系统行为（如 `4-3`）、每个错误码、每项验收（如 `T04`）都至少有一个测试，测试名中写编号；有脚本检查覆盖（第 2.2 节） |
| **期望结果由人定** | 试点页的基准输出由推动者确认后冻结；Agent 不能为了让测试通过而改它（第 2.4 节） |
| **先离线，后真实** | 核心逻辑全部用合成输入离线验证；真实的 milvus-docs、飞书、凭据和 dev 分支只在最后几层出现（第 3 节） |
| **接入现有体系** | zdoc 用 vitest、代码与测试对照表（`pnpm test:for-change`）和回放测试；md2md 用 Jest；不另建测试平台 |
| **一个工作包一个 PR** | 每个 PR 只做任务卡中的事，改动范围写在卡中（第 4、5 节） |

## 2. 组成

| # | 组成 | 放在哪 | 做什么 |
|---|---|---|---|
| 2.1 | 需求清单 | 本仓库 [`requirements.json`](./requirements.json)，由 [`tools/export_requirements.py`](../../tools/export_requirements.py) 从产品需求、实施计划和错误目录生成；实现仓库各复制一份 | 列出全部可检查的编号：65 条系统行为、14 项验收、73 个错误码 |
| 2.2 | 编号覆盖检查 | zdoc `packages/docs-tooling/src/shared-docs/spec/coverage.test.ts`；md2md `test/spec/coverage.test.js` | 本仓库负责的每个编号至少被一个测试引用；测试不能引用清单中没有的编号 |
| 2.3 | 合成的 milvus-docs 仓库 | zdoc `src/shared-docs/fixtures/milvus-docs/` | 测试时现场建一个本地 Git 仓库，按顺序提交几组文件，得到固定的 commit |
| 2.4 | 试点页输入与基准输出 | zdoc `src/shared-docs/fixtures/pilots/`、`fixtures/golden/` | 三篇试点页的真实输入，以及推动者确认过的期望 MDX |
| 2.5 | 错误样例表 | zdoc `src/shared-docs/fixtures/errors/<错误码>/` | 每个错误码一个最小输入，加上期望的报错 |
| 2.6 | 外部依赖的假实现 | zdoc `src/shared-docs/adapters/fake/` | md2md、GitHub、图片存储、飞书表格各有一个假实现，与真实实现共用一套契约测试 |
| 2.7 | md2md 与 zdoc 的契约用例 | md2md `test/contract/cases/`；zdoc 复制一份 | 同一组输入与期望输出，两边都跑；md2md 发版前，zdoc 用假实现过这组用例 |
| 2.8 | Milvus 回归脚本 | md2md `scripts/regression/` | 新旧 md2md 处理整个 milvus-docs，输出逐字相同（T11） |

表中的 `fixtures/` 是**测试素材**：事先准备好、放在仓库中不变的输入文件，每次测试都用同一份，结果才能比较。这是工程中的常用叫法。

### 2.1 需求清单

- 产品需求每改一次，推动者运行 `python3 tools/export_requirements.py`，提交新的 `requirements.json`；`--check` 发现文件过期时失败。
- 实现仓库复制时保留其中的 `prd_commit`，审阅时据此判断实现依据的是哪一版需求。
- 各编号归哪个仓库：md2md 负责 `1-2`–`1-5`、`2-1`–`2-3`，错误码中的“命名块”“变量与片段”两组（`area_id` 为 `named-blocks`、`variables-and-fragments`），验收 `T01`、`T02`、`T03`、`T11`；其余归 zdoc。一个编号可以同时被两边的测试引用，例如 zdoc 的集成测试也会引用 `1-2`，但只有负责的仓库会因为缺少它而报缺口。

### 2.2 编号覆盖检查

```ts
// 测试名中写编号，一个测试可以写多个
it('[4-3][LINE_NOT_FOUND] 代码行找不到时报错并指出版本', () => { … })
```

- 检查读复制来的 `requirements.json` 与全部测试文件中的编号，两个方向都查：清单中有、测试中没有的，列为缺口；测试中有、清单中没有的，直接失败。
- 还没开始的工作包，它负责的编号写在 `spec/pending.json` 中，并注明工作包：

  ```json
  { "6-2": "WP11", "T13": "WP11" }
  ```

  缺口只要在 `pending.json` 中就不失败，运行时打印剩余数量。一个工作包做完，必须把它的编号从 `pending.json` 中删掉。

### 2.3 合成的 milvus-docs 仓库

测试时在临时目录中建一个 Git 仓库，按顺序把 `commits/<序号>-<名字>/` 中的文件叠加上去、各提交一次。作者、提交者和时间都固定，所以每次得到的 commit 号相同，基准输出中的 `lock.yaml` 也就固定。

| 提交 | 相对上一次的变化 | 对应的产品需求 |
|---|---|---|
| `01-base` | 三篇试点页的原文、片段、`Variables.json` | 场景 1、2、3 |
| `02-paragraph` | 改一段正文，加一个参数说明 | 场景 6、7：普通修改 |
| `03-typo` | 修一处错字 | 场景 6：累积到同一个上游更新 PR |
| `04-replaced-source` | 改了被 Cloud 整节替换的那一段 | 场景 7：Cloud 页面不变，但要提示复核 |
| `05-heading-rename` | 一个标题改名，另一页的链接指向它 | 场景 7、8：标题改名与锚点 |
| `06-block-added` | 只新增一个命名块标记 | 场景 7：Cloud 页面不变，不重译 |
| `07-line-changed` | 改了 Cloud 定位的那一行代码 | 场景 6、7：规则只在 UAT 失效 |
| `08-block-renamed` | 命名块改名 | 场景 7：校验失败 |
| `09-source-renamed` | 原文改名 | 场景 7 |
| `10-image-changed` | 仓库内的一张图片换了内容 | 场景 5：新图另存 |

每个测试只取需要的那一段历史，例如上游更新测试用 `01` 到 `03`。

构建器目前只叠加文件、不删除文件。`09-source-renamed` 这类需要删除或改名的提交，由用到它的工作包（WP12）给构建器加上删除的写法，例如提交目录中的一份删除清单。

### 2.4 试点页输入与基准输出

**基准输出**（golden file）是一份由推动者确认过的期望 MDX。之后每次改代码，测试都把工具的实际输出与它逐字比较，有任何不同就失败。它不是手写的：工具先生成，推动者审过后冻结。

| 目录 | 内容 |
|---|---|
| `fixtures/pilots/<页面>/milvus-docs/` | 试点页在固定 commit 上的原文，从 milvus-docs 复制，`SOURCE.md` 中记下 commit |
| `fixtures/pilots/<页面>/shared-docs/` | 这一页的 `page.yaml`、Cloud 内容文件，以及 Guides 组的 `Variables.json`、`links.yaml`、Tabs 规则 |
| `fixtures/golden/<页面>/<手册>.<状态>.mdx` | 基准输出 |

**有几份**：每篇试点页 × 发布到的每个手册 × 每种状态，各一份。

| 状态 | 含义 | 什么时候需要 |
|---|---|---|
| `same` | Prod 与 UAT 用同一个 milvus-docs 版本，也就是平常的页面 | Phase 1a 起，每页每个手册一份：Delete Entities 与 Filtered Search 各 2 份（Guides、BYOC），OpenAI 1 份，共 5 份 |
| `diverged` | UAT 已经用了新版本、Prod 还在旧版本，页面中有成对的 `<NextChannel>` | Phase 1b，只为需要演练两版并存的页面加 |

**在内容对齐之后才审，只审一次。** Milvus 原文与网站上的飞书版因为两边都能编辑，已经分叉；不先对齐，比较结果中真正的产品差异会和历史漂移混在一起，没法审。每篇试点页按下面五步走：

| 步骤 | 做什么 | 谁 |
|---|---|---|
| 1. 冻结 | 对齐期间，飞书上的这一页先不改 | 文档工程师 |
| 2. 生成与比较 | 用工具当前的版本生成 Git 版，与 dev 上的飞书版比较；这时的结果是临时的，不需要批准 | 工具 |
| 3. 逐处处理差异 | Milvus 原文缺了、或飞书版写得更好：合进 milvus-docs；Cloud 本来就不同：写成变量或变换；飞书版过时或写错：以 milvus-docs 为准 | 文档工程师 |
| 4. 合并 | milvus-docs 的对齐 PR 合并，得到固定的 commit，复制进 `fixtures/pilots/` | 文档工程师 |
| 5. 审基准输出 | 用这个 commit 生成基准输出，再与飞书版比较：剩下的差异应当都是预期的，逐处确认后冻结 | 推动者 |

- 第 2、5 步的比较，与激活前的“比较”（[产品需求场景 9](../prd.md#场景-9从飞书切换到-git激活)）是同一件事，相当于提前演练激活。
- 内容对齐之前，Agent 用临时结果与合成的小样例开发，测试中标为临时，不进入 `fixtures/golden/`，开发不用等对齐。
- `examples/` 中的原型已在本地整理过 Delete Entities 与 Filtered Search 的原文，尚未合入上游，可以作为对齐的起点。

**冻结之后怎样改**：

1. 只有本地运行 `UPDATE_GOLDEN=1 pnpm vitest run …` 才会改写它；CI 中永不改写。
2. PR 改了基准输出时，PR 说明中单列“基准输出的变化”，逐个文件说明原因。
3. 这个目录在 zdoc 的 `CODEOWNERS` 中归推动者，没有推动者的批准不能合并。

### 2.5 错误样例表

每个错误码一个目录：`input/` 是触发它的最小输入，`expected.json` 是期望的报错，至少包括 `code`、`file`、`line`、`page`、`channel`（[错误的结构](../design/09-error-catalog.md#错误的结构)）。一个表驱动的测试逐个运行，测试名带上错误码，所以覆盖检查能看出哪个错误码还没有样例。

### 2.6 外部依赖的假实现

核心逻辑不读写任何外部系统（[代码位置](../design/README.md#代码位置)），外部依赖都经过适配器：

| 适配器 | 真实实现 | 假实现 | 用在 |
|---|---|---|---|
| milvus-docs 读取 | 按 commit 读 Git，测试中读 2.3 的合成仓库 | 按 commit 返回文件的最小替身 | 全部 |
| md2md | 固定版本的 npm 包 | 实现 2.7 契约的替身 | md2md 发版前的 zdoc 开发 |
| GitHub | `gh` / REST | 内存中的 PR、标签、评论、检查项 | 接入写 lock、上游更新、提升 |
| 图片存储 | zdoc 现有的上传 | 记录上传了哪些摘要 | 图片、发布 |
| 飞书表格 | Fetch 读到的记录；PR 校验读 dev 上的表格快照 | 一份与 `guides-uat-last-success.json` 同结构的记录文件 | 激活、整页通道、下线 |

每个适配器有一组契约测试，假实现每次都跑；真实实现只在第 3 节的 L3、L4 层跑。

### 2.7 契约用例

[技术设计 03](../design/03-md2md-interfaces.md) 中的两组接口（命名块的解析与清除、预处理），每组写成一批 JSON 用例：输入文件、参数 → 期望输出、依赖、错误。用例放在 md2md 仓库，跟随 md2md 发版；zdoc 复制与它固定的版本对应的一份。md2md 发版之前，zdoc 的替身必须先过这批用例，发版后再换成真实的包。

### 2.8 Milvus 回归脚本

在一份 milvus-docs 检出上，分别用旧版和新版 md2md 运行 `goover`，比较两份输出，要求逐字相同；再给若干页面加上命名块标记，新版的输出仍与不加时相同（产品需求 2-2）。md2md 每次发版前运行。

## 3. 验证分层

| 层 | 什么时候 | 跑什么 | 谁看结果 |
|---|---|---|---|
| L1 本地 | Agent 每次修改后 | 相关的单元测试；编号覆盖检查；`pnpm test:for-change -- <改动的路径>` 给出的全部命令 | Agent |
| L2 PR 检查 | 每个 PR | zdoc 的 `site-validation.yml` 中加入共享页的测试；md2md 的 CI | Agent、审阅人 |
| L3 真实输入 | 手动，或每天一次 | 用 milvus-docs `v3.0.x` 的最新原文生成三篇试点页，与基准输出比较，只出报告、不拦截；适配器的真实实现跑契约测试 | 推动者 |
| L4 切换前 | 每个试点页激活前 | zdoc 的回放测试（隔离的本地 Git 远端，不碰真实的 dev）；比较运行；权限与恢复核验（实施计划 T12、6.2 节）。改了 Fetch 的代码后，第一次激活前先跑一次不换链接的 Fetch 作基线；激活后确认下一次全量 Fetch 也成功 | 推动者、zdoc 维护者 |

zdoc 的 PR 检查目前不跑 vitest（2026-10-21 核验 `.github/workflows/`：没有工作流调用 `vitest` 或 `test:frontend`），docs-tooling 的单元测试只在本地运行。所以 WP0 要在 `site-validation.yml` 中加一步，只跑 `packages/docs-tooling/src/shared-docs/` 的测试；由推动者在 WP0 的 PR 中确认，并告知 zdoc 维护者。

L1、L2 必须全绿才能提审；L3 的差异要么是上游的正常修改，要么开新的工作包；L4 是激活的前提。

回放测试的输入是合成的，覆盖不到真实运行中的状态。WP9a 合并后，下面三个问题都是在真实运行中才发现的（见 [WP9 走读](./walkthroughs/WP9.md#审阅与真实运行中发现的问题)）：SDK Drive 表格的记录格式、激活时旧文档缓存与新来源并存、激活后的全量抓取。所以改了飞书记录的解析或 Fetch 的流程，合并前要对一个 SDK 分组跑一次只生成不发布（`publish=false`）的真实 Fetch，由 zdoc 维护者发起。

## 4. 工作包

**工作包**（WP，work package）是可以单独交给一个 Agent、单独开一个 PR 的一份活。一个工作包对应一张任务卡、一个 PR；太大时拆成几个 PR，每个改动不超过约 600 行（不含测试素材与基准输出）。

另有两类任务不交给 Agent，但排在工作包之间：

| 任务 | 做什么 | 谁 | 排在哪里 |
|---|---|---|---|
| R1 md2md 发版准备 | ① 给 milvus-docs 开 PR，把 md2md 固定在现在的版本（**已完成**：#3691 `v3.0.x`、#3692 `v2.6.x`、#3693 `v2.5.x`、#3694 `preview`）；② 在 npmjs.com 上为 `@zilliz/mdtomd` 添加可信发布者（Trusted Publishing），代替已失效的 `NPM_TOKEN`：GitHub Actions，`zilliztech` / `md2md`，工作流文件名 `release.yml`，Environment 留空；Allowed actions 中 `npm publish` 与 `npm dist-tag` 都不勾，只允许暂存发布（staged publishing），每个版本由推动者用双因素认证批准后才公开（**已完成**，2026-10-21）；第一次用它发版成功后，再把 Publishing access 改为禁止 bypass 令牌；③ 新建 `.github/workflows/release.yml` 负责发版，不存令牌，用 `npm stage publish`（需要 npm CLI 11.15.0、Node 22.14 及以上；semantic-release 是否支持暂存发布由 WP2 先核实），文件名必须与 ② 中填的一致；删除旧的 `ci.yml`（测试由 `test.yml` 负责）；交给 WP2 | ① 可交给 Agent；② 推动者；③ WP2 | ① 必须在 WP1 合并之前：md2md 合并到 master 就会自动发版，而 milvus-docs 现在安装时不固定版本，新代码会直接进入 Milvus 的正式构建 |
| C1–C3 内容对齐 | Delete Entities（C1，1a）、Filtered Search 与 OpenAI（C2、C3，1b）按 2.4 节的五步对齐 | 文档工程师 | 在批准对应页的基准输出之前；用到 WP4、WP5 生成的临时结果 |

为什么用 Trusted Publishing：md2md 的发版配置最后修改于 2022 年，当时只能用令牌；npm 在 2025 年底作废了旧式令牌，新的写权限令牌最长 90 天就过期。Trusted Publishing 由 GitHub 在发版时现场证明身份，仓库中不存密钥，也不用定期更换。

### 4.1 Phase 1a

| WP | 仓库 | 做什么 | 编号 | 依赖 |
|---|---|---|---|---|
| WP0 | zdoc | 测试与目录骨架：目录、需求清单与覆盖检查、合成仓库的构建器、适配器接口与假实现、基准输出与错误样例的运行器、对照表登记、目录下的 `AGENTS.md`；不含业务逻辑 | — | — |
| WP1 | md2md | 命名块的解析、校验与清除；`md2md-blocks check` 命令；契约用例 | `2-1`–`2-3`、命名块错误码、T01 | 合并前要完成 R1 ① |
| WP2 | md2md | 只做预处理的入口：变量、片段、依赖报告、错误；契约用例；回归脚本；提交锁文件，CI 按锁文件安装；发版工作流改用 Trusted Publishing，发一个版本，再给 milvus-docs 的 `v3.0.x` 开 PR 升级到这个版本，并在 PR 检查中加入命名块校验 | `1-2`–`1-5`、变量与片段错误码、T02、T03、T11 | WP1；R1 |
| WP3 | zdoc | 读取：`source.yaml`、`page.yaml`、`lock.yaml` 的 schema；按 commit 读原文；调用 md2md 定位命名块并判断类型与语言（包括列表中的代码块，见技术设计 01 的已知局限）、展开变量；输出变换前的 Markdown | `1-1`、`2-4`、`2-5`、`3-1`、`3-7`，页面配置与 lock 的错误码 | WP0 |
| WP4 | zdoc | 站点适配：代码 Tabs、提示框、front matter（含 `beta`）、MDX 兼容、标题锚点 | `2-6`、`3-5`，站点适配错误码 | WP3 |
| WP5 | zdoc | 链接与图片：四步查找、锚点换算（两个站点的锚点算法）、图片按内容命名（只算地址） | `5-1`、`5-2`、`5-4`–`5-7`，链接与图片错误码 | WP3 |
| WP6 | zdoc | 产品名检查 | `1-6`，产品名错误码，T14 | WP3 |
| WP7 | zdoc | 初始链接映射表的生成命令 | 技术设计 02b；不覆盖编号 | WP5 |
| WP8 | zdoc | WP8a：把读取、链接与图片、站点适配、产品名检查接成一条生成命令，读取 dev 上的飞书表格快照（`GuidesBase` 的真实实现）；WP8b：工作流，接入时写 lock、PR 校验 | `3-2`、`3-3`、`3-4`，T12 的候选部分 | WP4、WP5、WP6；WP8a 在 WP7 之后；WP8b 在 WP8a 之后 |
| WP8c | zdoc | `shared-docs/` 按组分子目录（Phase 1 只有 `guides`）：命令接收组目录，两个 PR 工作流按组运行；只改路径，不改生成结果 | 不覆盖编号 | WP8b；在 WP9 与第一篇试点页面提交之前 |
| WP9 | zdoc | Fetch 接入：按 `Docs` 链接分流，共享页在 Guides 表渲染时改用 Git 生成；交接：MDX、记录文件、`active.json`、图片上传；保住指向已激活页面的飞书链接；及时生效；Fetch 中的激活检查。WP9b：写 dev 前的重新生成比对、已采用的图片不变 | 第 6 节“及时生效”“发布保护”，`3-6`、`5-3`、`9-1`（Fetch 部分）、`9-2`、`9-3`、`9-6`、`9-9`，T06，`PUBLISH_IMAGE_UPLOAD_FAILED`、`PUBLISH_REGEN_MISMATCH`、`IMAGE_SOURCE_CHANGED`、`ACTIVATE_CHECK_FAILED`、`OWNERSHIP_PATH_MISMATCH`、`OWNERSHIP_CONFIG_MISSING`、`OWNERSHIP_REVERTED` | WP8c |

### 4.2 Phase 1b

| WP | 仓库 | 做什么 | 编号 | 依赖 |
|---|---|---|---|---|
| WP10 | zdoc | 变换：命名块、语言、代码行三级的 add / replace / remove | `4-1`–`4-6`，变换错误码，T04 | WP4 |
| WP11 | zdoc | 两版合并与 `channel` 变换 | `6-1`–`6-7`，T13 | WP10 |
| WP12 | zdoc | 上游更新：发现、每页一个 PR、影响报告 | `7-1`–`7-10`，T05 | WP11 |
| WP13 | zdoc | 提升工作流 | `8-1`–`8-4` | WP11 |
| WP14 | zdoc | 比较运行；旧任务遵守归属；同一路径两个来源；下线；拦截修改 dev 中生成结果的 PR | `9-1`（比较部分）、`9-4`、`9-5`、`9-7`、`9-8`、`10-1`–`10-4`，`OWNERSHIP_DUPLICATE_PATH`、`OWNERSHIP_WRITE_DENIED`、`RETIRE_DIR_LEFTOVER`，T07 | WP9 |
| WP15 | zdoc | 翻译、恢复与缓存的接入 | 第 6 节“翻译”“恢复”，T08、T09、T10 | WP14 |

### 4.3 并行与关键路径

- **关键路径**：WP0 → WP3 → WP4 / WP5 / WP6 → WP7 → WP8 → WP8c → WP9 → WP14。WP7 与 WP8a 都在 `cli-main.ts` 中注册子命令、都读 zdoc dev 的内容（WP7 新建读取的适配器，WP8a 复用），所以先后进行。md2md 的 WP1、WP2 与 zdoc 并行，zdoc 在 WP2 发版前用替身。
- **可以同时交给几个 Agent 的**：WP1 与 WP3；WP4、WP5、WP6（各在自己的目录中，只共用 WP3 的类型；都只提供纯计算的函数，不接入命令，由 WP8 接成一条生成命令；WP4 输出标题锚点时用的算法由 WP5 提供，经参数传入）；WP12 与 WP13。
- **不交给 Agent 的**：R1 中的 npm 设置、C1–C3 内容对齐、基准输出的审核，见本节开头。

### 4.4 项目地图

一页 Cloud 共享页从原文到网站要经过的环节，以及各由哪个工作包实现。每个工作包审阅通过后更新状态，并写一篇走读（第 6 节）。

| 环节 | 做什么 | 工作包 | 状态 | 走读 |
|---|---|---|---|---|
| 测试与目录骨架 | 代码的家、外部系统的替身、需求账本、测试素材 | WP0 | 已合并到上游（`zilliztech/zdoc` `5dd0e56`） | [WP0](./walkthroughs/WP0.md) |
| 命名块（md2md） | 检查标记写法；Milvus 发布前删掉标记 | WP1 | 已合并到上游（`zilliztech/md2md` `07855e4`），已随 1.3.0 发布 | [WP1](./walkthroughs/WP1.md) |
| 变量与片段（md2md） | 只做预处理的入口；发版 | WP2 | 已合并到上游（`zilliztech/md2md` `a143b27`），1.3.0 已发布；milvus-docs `v3.0.x` 已升级（#3697） | [WP2](./walkthroughs/WP2.md) |
| 读取 | 读页面配置与 lock；按 commit 取原文；定位命名块、判断类型 | WP3 | 已合并到上游（`zilliztech/zdoc` WP3a `5844587`、WP3b `31a9b54`） | [WP3](./walkthroughs/WP3.md) |
| 变换 | 按页面配置做 add / replace / remove | WP10 | 未开始 | — |
| 变量展开 | 调用 md2md 的预处理入口，换成 Cloud 的值 | WP3 | 已合并到上游（WP3b `31a9b54`） | [WP3](./walkthroughs/WP3.md) |
| 站点适配 | 生成 Tabs、提示框、front matter、标题锚点 | WP4 | 已合并到上游（`zilliztech/zdoc` `09859d7`） | [WP4](./walkthroughs/WP4.md) |
| 链接与图片 | 换算链接与锚点；图片按内容命名 | WP5、WP7 | WP5 已合并到上游（`zilliztech/zdoc` `ca1cbd5`）；WP7 已合并（`f19966c`） | [WP5](./walkthroughs/WP5.md)、[WP7](./walkthroughs/WP7.md) |
| 产品名检查 | 漏换的产品名报错 | WP6 | 已合并到上游（`zilliztech/zdoc` `ca64aa6`） | [WP6](./walkthroughs/WP6.md) |
| 两版合并 | Prod 与 UAT 的版本合成一页 | WP11 | 未开始 | — |
| 生成命令 | 把各步接成一条命令，按页面与手册输出 MDX | WP8a | 已合并到上游（`zilliztech/zdoc` `d3d1cbe`） | [WP8](./walkthroughs/WP8.md) |
| 工作流 | 接入写 lock、PR 校验、上游更新、提升 | WP8b、WP12、WP13 | WP8b 已合并到上游（`zilliztech/zdoc` `8680736`）；WP12、WP13 未开始 | [WP8](./walkthroughs/WP8.md) |
| 目录结构 | `shared-docs/` 按组分子目录 | WP8c | 已合并到上游（`zilliztech/zdoc` `e9ab23f`） | — |
| 发布与切换 | 接入 Fetch 与激活；比较、归属与下线；翻译与恢复 | WP9、WP14、WP15 | WP9a 已开上游 PR（`zilliztech/zdoc#863`，待文档负责人审）；WP9b 在 WP9a 合并后开始；WP14、WP15 未开始 | [WP9a](./walkthroughs/WP9.md) |
| 试点页接入 | Delete Entities 的原文对齐与页面配置 | 内容（不属于工作包） | milvus-docs 原文已对齐（`milvus-io/milvus-docs#3719`、`#3722`）；zdoc 已接入（`zilliztech/zdoc#861`，lock 锁在 `3e6b749`）；等 WP9a 合并后激活 | — |

## 5. 任务卡

每个工作包一张任务卡，放在 [`tasks/`](./tasks/)，按[模板](./tasks/_template.md)写。Agent 只读任务卡和卡中列出的文档章节，不需要读整套设计。

已写好的任务卡：

| WP | 任务卡 |
|---|---|
| WP0 | [测试与目录骨架](./tasks/WP0-skeleton.md) |
| WP1 | [命名块的解析、校验与清除](./tasks/WP1-md2md-named-blocks.md) |
| WP2 | [只做预处理的入口与发版](./tasks/WP2-md2md-preprocess.md) |
| WP3 | [读取：页面配置、lock、原文与命名块](./tasks/WP3-zdoc-read.md) |
| WP4 | [站点适配](./tasks/WP4-zdoc-site-adaptation.md) |
| WP5 | [链接与图片](./tasks/WP5-zdoc-links-images.md) |
| WP6 | [产品名检查](./tasks/WP6-zdoc-product-names.md) |
| WP7 | [生成初始链接映射表](./tasks/WP7-zdoc-links-seed.md) |
| WP8 | [生成命令与 PR 校验](./tasks/WP8-zdoc-build-and-validate.md) |
| WP8c | [`shared-docs/` 按组分目录](./tasks/WP8c-zdoc-group-layout.md) |
| WP9 | [接入 Fetch：按 `Docs` 链接分流与交接](./tasks/WP9-zdoc-fetch-handoff.md) |
| WP10 | [变换：命名块、语言、代码行三级](./tasks/WP10-zdoc-transforms.md) |

其余的在对应工作包开始前写，写完由推动者确认。

### Agent 的规则

写进 zdoc `packages/docs-tooling/src/shared-docs/AGENTS.md` 与 md2md 根目录的 `AGENTS.md`，与 zdoc 根目录现有的 `AGENTS.md` 一起生效：

- 只改任务卡“可以改”中列出的路径；要改别的，先在 PR 中说明，等审阅人同意。
- `core/` 中不读写文件、网络、Git，不引用 `lark/`；外部依赖只经过 `adapters/`。
- 不改 `spec/requirements.json`；它从本仓库复制而来。
- 不改基准输出，除非任务卡要求；改了就在 PR 说明中逐个解释。
- 不改产品需求和技术设计；发现它们有问题、互相矛盾或不够用，在 PR 中提出，由推动者决定。
- 在单独的工作树中工作，不动仓库主目录中未提交的文件。zdoc：按它的 `AGENTS.md`，工作树建在 `.claude/worktrees/` 下（不论用哪家的 Agent），只向 master 开 PR，不碰 dev。md2md：没有约定，工作树建在仓库外，如 `~/worktrees/md2md/<分支名>`。
- 提审前跑完 L1，在 PR 说明中贴出命令与结果；跳过或没跑完的要写明。
- **语言**：zdoc 与 md2md 中会进入上游的内容一律用英文，包括代码、注释、测试名、提交信息、`AGENTS.md`、PR 标题与说明；PR 标题沿用上游的 conventional commits 写法，如 `feat(shared-docs): …`。fork 中的 PR 评论与讨论也用英文；PR 说明中不链接 fork 中的评论，需要引用的决定写进说明本身，或链接设计仓库。代码只依赖 `requirements.json` 中的编号与 `area_id`，不依赖其中的中文说明。

### 协作规则

几个 Agent 同时工作时，额外遵守下面几条：

| 规则 | 说明 |
|---|---|
| 一个 Agent 一个工作包 | 不同时接两个，也不和别人共用一个工作包 |
| 各用各的工作树和分支 | 分支名用工作包编号加内容，如 `wp3-reader`；都从最新的 master 拉出 |
| 同时进行的工作包不改同一批文件 | 任务卡的“可以改”有重叠时，这两个工作包不同时开工 |
| 共用的部分只有一个主人 | 共用的类型归 WP3；其他工作包要改，先在 PR 中提出，由 WP3 的主人或审阅人决定 |
| 不叠 PR | 前一个工作包合并后，后一个再从 master 拉分支；不以另一个未合并的分支为基础 |
| 依赖合并后先同步 | 依赖的工作包合并了，正在做的工作包先合入最新的 master，再继续 |
| 问题写在 PR 中 | 先开草稿 PR，问题写在 PR 说明或评论中，由推动者或审阅人回答 |

### PR 说明的格式

zdoc 与 md2md 的 PR 用英文写，六个部分依次是：

```markdown
## Summary                        <!-- 做了什么 -->
## Requirements covered           <!-- 覆盖的编号；从 pending.json 删掉了哪些 -->
## Tests                          <!-- 跑了哪些命令，结果 -->
## Golden output changes          <!-- 基准输出的变化；没有就写 None -->
## Deviations from the design     <!-- 与设计不一致的地方；没有就写 None -->
## How to try it                  <!-- 2–3 条推动者能自己运行的命令，以及应看到的结果 -->
```

“How to try it” 要让任何有这个仓库检出的人都能照着运行：第一步用 `gh pr checkout <PR 编号> -R <上游仓库>` 取到这个 PR 的代码（并给出不用 GitHub CLI 的等价写法 `git fetch origin pull/<编号>/head:pr-<编号> && git checkout pr-<编号>`）；需要安装依赖的仓库接着写安装命令；之后的命令都相对于仓库根目录。不写本机的绝对路径，例如 `/Users/…` 或某个工作树的位置；临时文件在命令中自己创建。PR 说明的其他部分也不写本机路径。

## 6. 审阅

| 顺序 | 谁 | 看什么 |
|---|---|---|
| 1 | Claude | 按下表逐项检查，结论写在 PR 评论中 |
| 2 | 推动者 | 行为是否符合产品需求；基准输出的变化 |
| 3 | zdoc 维护者 | zdoc 的 PR：工作流、权限、与 Fetch 的衔接 |

| 检查项 | 怎样判断 |
|---|---|
| 范围 | 只改了任务卡允许的路径；没有顺手重构 |
| 需求 | 覆盖的编号与任务卡一致，`pending.json` 同步删除；行为与产品需求的原文对得上 |
| 测试是真的 | 测试会因为行为错误而失败：断言具体的输出与报错，不是只断言“没有抛错”；出错路径都有测试 |
| 基准输出 | 每处变化都有理由，且与本 PR 的行为改动有关 |
| 边界 | `core/` 不碰外部；不引用 `lark/`；没有新的写死的值（如 beta 的取值、手册名） |
| zdoc 的约定 | 新路径已登记到对照表；`pnpm test:for-change` 给出的命令都跑过 |
| 真实运行 | 改了飞书记录的解析或 Fetch 的流程：合并前有一次只生成不发布的真实 Fetch（见第 3 节） |
| 报错 | 错误码在错误目录中；报错指出文件、行号、版本和怎样改 |

**一个工作包算做完**：L1、L2 全绿；任务卡中的编号都已从 `pending.json` 删除；审阅中的问题都已处理；推动者批准。

**审阅通过后**：审阅人写一篇走读，放在 [`walkthroughs/`](./walkthroughs/)，用中文说明这个工作包解决什么问题、文件地图、一个真实的例子从输入走到输出、推动者可以自己运行的命令、值得读的测试和刻意没做的事；同时更新第 4.4 节的项目地图。目的是让推动者在实现推进的过程中始终看得懂整个项目，不用读每一行代码。

## 7. 开工前的准备

| 事项 | 在哪 | 谁 |
|---|---|---|
| 确认本文与 WP0、WP1 的任务卡 | 本仓库 | 推动者 |
| `CODEOWNERS` 中把基准输出目录交给推动者；`site-validation.yml` 中加入共享页的测试 | zdoc，WP0 的 PR 中完成 | 推动者在 PR 中确认，并告知 zdoc 维护者 |
| milvus-docs 固定 md2md 的版本 | milvus-docs | R1 ①，WP1 合并之前 |
| npm 的可信发布者 | npmjs.com | R1 ②，推动者 |
| md2md 的 CI：Node 版本、Jest | md2md，WP1 中完成 | WP1 |
| 三篇试点页的内容对齐排期 | milvus-docs | 文档工程师 |
