# WP13 Guides 提升

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)｜**阶段**：Phase 1b｜**依赖**：[WP11 双通道生成](https://github.com/zilliztech/zdoc/pull/921)｜**状态**：首片已同步 dev，只读 UAT 预览已通过本地验证，真实部署验收待补

## 目标

发版负责人选定一次已验收的 UAT 部署，工具先筛出待提升的 Guides 页面。负责人一次确认本次上线的页面清单，工具按清单生成一条指向 `master` 的提升 Draft PR，供人员审阅和合并。多个上游更新 PR 可以汇入同一次提升，按本次发版范围分组。目标是把验收过的内容带到生产：若 UAT 验收的是 `B`，该页从 `current=A / next=B` 提升为 `B / B`。

WP12 推进页面的 `next`，WP13 推进页面的 `current`。已有已验收的 UAT 版本就可以设计和验证提升，WP12 多页 Draft 与新 Fetch 的来源认证可以独立推进。现有 [#1334](https://github.com/zilliztech/zdoc/pull/1334) 的本地 `promote` 命令服务整本手册布局，Guides 首片应复用配置读取、通道生成及校验能力，保留整本手册的接口。

## 要读的

| 文档 | 用途 |
|---|---|
| [通道与锁](../../design/04-channels-and-lock.md#提升) | 确认提升、通道规则、飞书整页标记和锚点的行为 |
| [工作流与权限](../../design/08-workflows-and-permissions.md) | 人工触发、PR 审阅及写权限边界 |
| [发布交接](../../design/05-publish-handoff.md) | 核对生成记录、Fetch 写入 dev 与站点部署 |
| [WP12 接口](./WP12-zdoc-upstream-updates.md#接口) | 复用影响分析，处理同页上游更新冲突 |
| [Zdoc 发布证据](https://github.com/zilliztech/zdoc/blob/57977f06c7165a4eb0d9e945ce3c72c7fc10fc7e/README.md#release-verification-uat--production) | 识别 UAT 的部署提交、镜像摘要和构建记录 |

## 首片交付方式

1. **先用本地命令验收同一流程。** 先以一页有 `current/next` 差异、可核验 UAT 部署的已激活 Guides 验证预览和候选，再补多页筛选、部分选择及整组暂停的测试。首个样例是单页，发版清单和报告从一开始按多页表达。本地方案可由人按已验证补丁创建 PR。
2. **把预览与生成接入一个手动 Actions 工作流。** 预览是默认操作。生成 Draft 必须明确选择该操作和发版范围，由有仓库写权限的发版负责人发起。
3. **在 Draft PR 里做最终审批。** Actions 的选择记录发版意图。人审阅清单、补丁和验证结果后合并。合并后正式 Fetch 写入 dev，沿已有站点 release/Jenkins 流程发版。

## Actions 操作与结果

| 操作 | 发版人提供 | 工具产出 |
|---|---|---|
| **预览发版清单** | 已验收的 UAT 部署编号 | 查询该次部署的实际发布记录和页面产物，生成 Actions 摘要及完整预览产物。按页分成「可提升」「无需提升」「需处理」，列出当前 `current → 已验收 next`、当前 `next`、目标和原因。只读，无分支或 PR 写入 |
| **生成提升 Draft** | 预览运行编号及明确的页面 ID 列表，或 `all-eligible` | 验证预览是受信工作流的成功产物，重新核对当前输入，按选中页面和必要依赖生成补丁、复核报告和一条 Draft PR |
| **审阅并合并** | 在 PR 上确认范围、改动和验证结果 | PR 展示页面清单、旧/新锁、验收部署、视图比对、预览运行及报告。合并校验核对同一证据和候选，确保仍能复现预览承诺 |

- **工具判断是否可提升，发版人决定是否本次上线。** 预览列出 9 页可提升、3 页需处理时，`all-eligible` 表示那次预览中的 9 页。若只发其中 7 页，一次输入 7 个 ID。生成 Draft 时不能追加后来才出现在可提升集合中的页，也不能悄悄跳过有问题的已选页。这里的 `all-eligible` 是本卡对通用设计中 `all-pending` 在 Guides 的具体定义。
- **复核发生在写入前。** 预览产物绑定运行/尝试、UAT 部署和产物、预览基线、分类清单及每页验收版本。生成候选前核对当前 `master` 与相关输入，检查同页开放更新 PR 和所需依赖。已选页过期、选中预览未列为可提升的页、依赖缺失、预览产物无法验证或整组比对失败，整批暂停并列出原因，无可用候选，也不开 PR。空清单只报告。
- **同一次发版保持一条提升 PR。** 相同预览与清单的重跑返回已有 Draft。审阅中要缩减范围时，明确指定已有 Draft 和新清单，从同一仍有效的预览重新生成候选，再用普通提交更新同一条 Draft 的候选与报告。更新前确认 Draft 还是工具生成时的版本，发现人工改动、并发变更或归属不明就暂停，交由审阅人处理。原来的校验不适用于改过的清单。
- **最终审批发生在 PR。** 工具只负责预览、准备和写 Draft，不代替人批准或合并。候选提交、选页范围或相关输入变动后，必须按新的候选重跑校验。工作流只在生成 Draft 的阶段授予所需的仓库写权限，首轮本地方案不依赖该权限。

## 固定的输入与输出

| 输入 | 必须证明什么 |
|---|---|
| 预览运行、已选页面与发版人身份 | 页面属于这次预览的可提升集合，最终范围由发版人确认。每个已配置目标都要纳入核对，如 Cloud、BYOC |
| UAT 发布记录与发版人验收 | 发布记录包含实际部署的 zdoc 提交、站点、构建或镜像身份。发版人确认本次页面和目标。构建成功本身不能代替内容验收 |
| UAT 部署提交中的生成记录及产物 | 从实际发布产物和记录交叉核对页面使用的 `next`、配置和生成输出。不能仅按现在的 dev tip 或工作流输入推断当时显示的内容 |
| 当前 PR 基线和页面输入 | 读取 `current/next`、共享配置、Cloud 内容和相关通道规则，校验候选基线。验收后 `next` 或影响视图的输入变化，报告差异并要求重新验收。基线前进时重建候选并重做检查 |

预览输出分类报告和可回读的固定清单，生成阶段输出一份整批候选补丁及一份可复核报告。报告列出旧 `current`、已验收 `next`、UAT 证据、受影响目标、允许的编辑和每项校验结果。证据缺失、无法恢复精确部署产物、存在未解释的配置差异或验证失败时，仅输出暂停原因。

## 补丁和审阅范围

- 提升范围由这次选定的页面清单确定。`current` 采用已确认的 `next`，`next` 保留其原值。对同页明确可提升的 Transform，移除仅用于旧 current 的规则，解除要进入生产的 next 规则限定。保留手写 `<NextChannel>`，在报告中列出供人决定。
- 查找旧锚点的入链。首片若需改跨页 Git 链接、调整飞书整页通道，或无法确认锚点映射，暂停并列出必要动作。首个正例使用现有页面且无需这些配套变更。后续子片再实做经过认证的 Git 锚点修复、整页通道协调和仅本地规则变化的提升。
- 有同页开放更新 PR 时先暂停，提示合并、关闭或重新审阅该 PR。等后续补齐 WP12 重建接口，再处理提升后的自动重建。候选生成后，PR 检查重新核对同一验收输入和允许变更。
- 复用 WP11 的两通道生成。对每个配置目标，把候选的 Prod 视图与验收时的 UAT 视图比较，检查正文、代码、图片、标题锚点和页内链接。比较使用现有渲染语义，仅排除部署通道包装和环境标识差异，保留内容次序及链接目标。提升范围内由工具产生的双版本包装应消失。工具报告与人工发布动作各自留证。

## 验收与交接

| 验收 | 断言 |
|---|---|
| 正常单页 | 验收版本为 B 时生成 `A / B → B / B`。每个配置目标的候选 Prod 视图与已验收 UAT 视图一致，可按报告创建并复核一条 PR |
| 多页初筛与选范围 | 同次 UAT 部署产生三类清单。显式选择只改变指定页，`all-eligible` 只展开已固定的可提升集合。两种选择各自生成一条 PR 候选 |
| 验收后变化 | `next` 从 B 到 C、配置或 Cloud 内容影响视图、UAT 证据来自错误构建，均暂停且无可用补丁。已选组中一页失效，整组暂停 |
| 页面与链接边界 | 未激活、目标证据缺失、旧锚点需要协调、同页开放更新 PR、最终视图不一致，逐项报告阻塞 |
| 空清单、重跑和缩减范围 | 无有效编辑只报告。相同请求复用 Draft；缩减范围后重校验并更新同一 Draft；Draft 有人工改动或并发更新则暂停并保留现场 |
| 正式发布旅程 | 本地候选和实际 UAT／Prod 分开记录。实际生产上线另需核对合并提交、Fetch 产物及部署记录 |

## 首片实施计划

**Goal:** 从固定的本地重放材料预览待提升 Guides 页面，并为一次选中的页面生成一份可审阅补丁。

**Architecture:** 本地 CLI 分为预览和准备，两个阶段共用页面资格和证据读取。首片只消费样本记录并标记为重放，可以给真实记录核验留接口；实际 Jenkins 记录读取与认证、Actions 创建 Draft 各自验收。

**Tech Stack:** zdoc TypeScript CLI、Git 固定提交读取、现有 SharedReceipt 和 WP11 生成、Vitest。

在 [产品基线 57977f06](https://github.com/zilliztech/zdoc/commit/57977f06c7165a4eb0d9e945ce3c72c7fc10fc7e) 核对接口；开工时取最新 master，并报告任何影响本卡的漂移。负责人提供的部署脚本默认查 Jenkins `zdoc-release`。人可用「任务 + 构建号」定位记录，单个任务运行可能含 oversea、cn 或两者，实际站点分别核对。构建结果、描述和 image tag 只用于定位；真实验收记录还必须给出成功部署、精确 zdoc SHA 和镜像 digest。本地开发先构造同形状样本，保持测试与真实验收分开。首批先由人员根据已验证补丁开 PR，等只读记录入口跑通后再接自动 Draft。

允许改动：

| 文件（相对于 zdoc） | 职责 |
|---|---|
| `packages/docs-tooling/src/shared-docs/core/promotion.ts` | 纯分类、选页和整组决定 |
| `packages/docs-tooling/src/shared-docs/adapters/promotion.ts` | 读取固定 Git 对象、核对记录和生成视图证据 |
| `packages/docs-tooling/src/shared-docs/commands/promote-guides.ts` | 本地入口、重新核对输入、输出报告和补丁 |
| `packages/docs-tooling/src/cli-main.ts` | 独立注册 `promote-guides`，保留整本手册命令 |
| `packages/docs-tooling/src/shared-docs/testing/promotion.test.ts`、`packages/docs-tooling/src/cli-main.integration.test.ts` | 样本重放、失败回归和 CLI 契约 |

### 1. 固定样本，生成预览

- [ ] 用本地 Git fixture 构造三页。A 页的 UAT 已验收 B，当前锁为 A/B；B 页已同步；C 页在验收 B 后变成 C。以已部署样本记录的 `sourceSha` 查找该 zdoc 生成提交，读取 `generated/en/manifests/shared-pages/guides/active.json` 和相应的每页记录。复用 `validateActiveState` 和 `validateSharedReceipt`，按记录的输出路径核对 Git 对象原始内容摘要。关联不明、缺少目标产物或已验收版本不符，记录原因。不能用 Git 工作区当前文件替代受锁的 UAT 提交。
- [ ] 实现 `preview` 严格参数解析。默认只报告三类页面。输出 `promotion-preview.json`，记录 `observation: replay`、实际输入的 UAT 记录摘要、Git 基线、确定排序的分类、页面目标、每页旧锁与相关输入摘要。fixture 用临时 Git 文件模拟真实内容，输出始终与正式验收区分。
- [ ] 验收 A 页可提升、B 页无需提升、C 页需处理；换记录、失去 Cloud/BYOC 任一必要产物、结果摘要错误和无关未激活目录均不能增加可提升页。

### 2. 一次选页，产出整批补丁

- [ ] `prepare` 只接受上一步预览及明确的页面 ID 列表或 `all-eligible`。用同一组固定仓库与记录重算预览，逐项核对基线、选集和活动记录，勿从报告文字取得授权。用临时输出比对候选 Prod 与批准快照的 UAT 视图；复用 WP11 生成和观察接口。核对原 UAT 产物，使用语义一致的通道投影；无法证明某处差异等价就报告暂停。首个正例用无需改跨页链接、飞书整页通道或手写通道块的页面。
- [ ] 只在所有选中页通过时输出一份 `promotion.patch` 和对应 `promotion-result.json`。检查补丁只改所选页 `lock.current` 与必要的同页通道规则。写入新的输出目录，不修改源检出。证据不完整、选中页失效或比对失败时输出暂停报告，目录里没有可采纳补丁。首片不创建 Git 提交、PR 或发布。
- [ ] 增加两页可提升的正例，分别验证显式子集和 `all-eligible`。篡改预览选集、在两阶段间推进一页 next、改变视图依赖、未选页多出编辑、空选集、已存在输出目录分别验证。对正例执行 `git apply --check`，打到隔离检出后检查实际差异和视图。

### 3. 从 CLI 重放并交主审

本地重放命令。

`--uat-record` 接收版本化重放输入，内含形如发布契约的 UAT 记录以及显式 `openUpdatePages` 清单（无冲突时填空数组）。当前证明范围为英文站的 Cloud/BYOC，读取固定 Git 对象，无法验证的通道或证据应暂停。

```sh
pnpm docs-tooling shared-docs promote-guides --mode preview --uat-record "$record" \
  --repo "$milvus_repo" --dev "$zdoc_repo" --out "$preview_out"
pnpm docs-tooling shared-docs promote-guides --mode prepare --uat-record "$record" \
  --repo "$milvus_repo" --dev "$zdoc_repo" --preview "$preview_out/promotion-preview.json" \
  --pages all-eligible --out "$candidate_out"
```

- [ ] 从 zdoc master 的独立工作树跑一遍真实 CLI 加驱动测试。用 CLI 集成断言覆盖缺参数、产物目录限制、报告和退出语义。成功预览、空清单和成功准备正常退出；参数错误或明确暂停返回非零值，并按阶段记录可读原因。
- [ ] 开工前按允许路径查 `pnpm test:for-change -- <paths...>`，提交后用实际完整 diff 重跑选择器。当前预计门禁包括 CLI/validation、shared-docs grouped、Fetch 合约与 replay、workflow policy、typecheck、matrix 和 diff-check。将实际执行命令、结果、Git SHA 及输出样本带回主会话；已通过的样本明确标为 replay。
- [ ] 用得到的真实只读 UAT 记录做额外验收，首先核对记录来源、站点、成功状态、完整 SHA/digest 是否能与生成物串起来。缺记录不影响前两项本地交付，但需报告真实验收未完成。Actions 预览、自动 Draft、真实部署各自另行验收。

### 本地实施记录（2026-11-18）

执行分支以 zdoc master `1bc57ff6` 为基线，本地实现提交 `cb48e26d`。首片真实 CLI 重放验证两页同批提升，补丁只修改两页的 `lock.current`，四个英文 Cloud/BYOC 视图与样本 UAT 一致。过期页、历史文件或导航证据不一致、不可用链接及发布补丁失败均有暂停用例。英文站同 token 通道由生产路由插件判定；本地重放只证明英文 Guides 及 BYOC 的范围，站点其他目的地和本地化视图仍需后续验收。

最终提交的 115 项定向测试、8 项发布路由测试、类型检查、Fetch 合约/回放、workflow policy、matrix 和 diff 检查通过。默认并发的 shared-docs 全量两次在未修改的 WP12 小数快照用例达到 5 秒时限后提前终止，单例复跑约 3.5 秒通过。降低本地 light 并发至 4 workers 后，light 2,006 passed / 0 failed / 6 skipped；合跑触及 900 秒总时限。按 CI 划分单独运行 transactions、local-runner 和 update-prepare，68 passed / 0 failed / 0 skipped。所有分组覆盖同一个最终提交，合跑记录保留为未通过。Jenkins 真实 UAT 记录和 Actions 接入保持待验收。

首片已验证本地候选与视图。需求 [8-1–8-4](../../prd.md#场景-8功能上线时提升) 保持待验收，工作流创建 PR、真实生产发布及既有更新 PR 自动重建分别结项。SDK 整本手册的完整提升旅程使用其独立契约。

### 合并与定时 Fetch 验证（2026-11-18）

- 产品 PR [#1342](https://github.com/zilliztech/zdoc/pull/1342) 已合入 `master@2778f169`。合并树与 CI、[仅产物 Fetch 44262771912](https://github.com/zilliztech/zdoc/actions/runs/44262771912) 验证的候选 `960f2ca9` 一致。[同步 PR #1348](https://github.com/zilliztech/zdoc/pull/1348) 已将工具交接到 `dev@2b2c1a40`。
- 当晚[定时 Fetch 44283079178](https://github.com/zilliztech/zdoc/actions/runs/44283079178) 从包含 #1342 与 #1347 的 `master@c062875f` 运行。英文 Cloud 4 项、BYOC 4 项通过，组装后写入 `dev@09b32d97`。中文 Cloud 8 项、BYOC 6 项通过，组装后确认无变化，回执引用 `35fac446`。两种语言的 Cloud/BYOC 候选内容清单和侧栏均与各自回执提交中的字节一致。原先因权限受阻的英文《Configure Access Logs》成功读取。
- `dev` 派生状态同步至 `aebeeacd` 并通过最终站点校验。全量 Fetch 的 Node.js 分组因发布基线摘要不一致而失败，整轮结论为 failure，Translation 跳过。此次验收覆盖 Guides 到 `dev` 的发布链路，实际 Jenkins UAT 内容验收仍待补。[发布结果](https://github.com/zilliztech/zdoc/actions/runs/44283079178/artifacts/14421436243) · [Node.js 日志](https://github.com/zilliztech/zdoc/actions/runs/44283079178/job/134729322531) · [站点校验](https://github.com/zilliztech/zdoc/actions/runs/44283079178/job/134755572359)

## 下一片 · 真实 UAT 发布证据与只读预览

发版负责人用明确的 Jenkins 任务和构建号定位已部署的英文站 UAT，再确认本次验收的页面和目标。先跑通一页的只读预览和隔离候选重放。发版人的页面验收与 Jenkins 的成功部署记录都进入报告。

1. **确定证据入口。** 优先确认发布侧能否在现有受信环境提供 `evidence/uat-records.json` 的只读导出，沿用 zdoc 发布契约的信任边界。部署脚本显示的 image tag 用于定位。正式证据应包含英文 UAT 的成功部署状态、完整 `sourceSha`、实际部署镜像的不可变 digest 和 `jenkinsBuildIdentity`。核对部署镜像的 revision 和 Jenkins build 标签是否与记录一致。若证据交付位置或身份尚未确认，先用同形状 fixture 验证解析和暂停行为，报告标为重放。
2. **接到固定 Git 读取。** 从唯一的受信成功记录解析出实际 UAT 提交。复用 `deploy/contracts/release.schema.json`、发布校验器及现有 `promote-guides` 的生成记录读取、通道投影和 Cloud/BYOC 比对。受信记录须由运行环境提供，命令行参数只选择构建身份。基于该固定提交读取 `active.json`、页面生成记录和输出对象。真实预览保留部署记录摘要、镜像 digest、已验收目标和选页依据。
3. **验证正常与暂停路径。** 选一页在该次 UAT 中有 current/next 差异、Cloud/BYOC 证据齐全且无需锚点别名协调的英文 Guides。正常样例输出分类和语义比对。重复或缺失记录、错误站点、失败部署、SHA 或 digest 不一致、产物或目标缺失、验收后 next 前进都必须暂停。原 `observation: replay` 入口继续支持本地回归，样本不能冒充正式证据。Actions 接入、Draft 写入及生产发布留待这片的真实验收完成后再推进。

主审通过的实施范围为单页英文只读预览。命令用完整 Jenkins 构建身份选择发布侧挂载的成功记录，沿用现有受信证据树及其检查。报告分别记录部署证据、固定 Git 输入与双目标视图比对，并保留镜像标签核验、人工验收和开放更新 PR 的观测状态。镜像标签尚未独立核验时，状态保持待核。新入口只输出报告，原 replay 的 `prepare` 拒绝这类报告，保持现有重放契约。

### 执行 Agent 交接

> 以最新 zdoc master 为基线，先读本卡「真实 UAT 发布证据与只读预览」及 zdoc `deploy/contracts/README.md`。给出短方案，标明现有 verifier 的可复用入口、由谁提供受信发布记录、预览如何绑定具体部署与 Git 对象，以及资料缺失时的暂停条件。主审通过后实现只读证据接入与上述回归，用最终 diff 查 selector、跑完命中的检查，交回确切 base/head、通过与暂停样本、真实 Jenkins 验收状态。保持现有 replay 入口，无 Jenkins 触发、工作流、远端写入或 Draft 操作。

### 只读预览本地验证（2026-11-18）

以 zdoc `master@b701ac59` 为基线，最终本地提交为 `281f5903d203f5415db10cb8ea72c0bc6a29c0a3`。主审复核了经修正的工作树和证据目录隔离、Git 历史检查、双目标内容比对及 replay 边界。CLI 样本产生单页 Cloud/BYOC 只读报告，覆盖缺失和重复构建、路径重叠、Git 历史标记、`next` 漂移及报告进入 replay prepare 时的拒绝。最终提交的 124 项定向回归、56 项部署合约检查、类型检查和 selector 其余门禁通过。分组测试按顺序执行，合计 2,112 项通过，6 项跳过。早期失败或中止的运行单独保留。

产品 [Draft PR #1353](https://github.com/zilliztech/zdoc/pull/1353) 的合并候选 `93dfbaa9` 与本地提交同树。CI 13 项成功、8 项按条件跳过，最终站点门禁成功。真实 Jenkins 只读挂载、部署镜像标签、发版人对页面和目标的验收，以及开放更新 PR 的独立核对仍待补。挂载记录沿用现有发布校验器的 JSON 解析约定。

### 直接读取 Jenkins 部署证据 · 方案待审

**已核查。** 通过 Jenkins 界面和只读 API，能从固定发布任务读取已完成的构建、阶段结果和 `output.json`。一组历史英文 UAT 与 Prod 的最终部署 digest 一致，可以从归档追溯复用关系。最近核查的英文 UAT 构建可以作过期反例：当时筛出的 12 个待提升页面，其发布回执均已与复核时的 dev 不同。现有可见任务和仓库未能确认有证据挂载，也尚未独立读取实际镜像标签。内部构建链接、任务位置和镜像引用保留在内部验收记录。

**首片交付。** 给 Guides 单页只读预览增加实时 Jenkins 记录来源，复用 [#1353](https://github.com/zilliztech/zdoc/pull/1353) 的固定 Git 读取、页面分类和 Cloud/BYOC 视图比对。Jenkins 直读证据带独立来源标记，输出只读预览。原挂载仍服务现有验证入口，既有 replay 继续显式标注。不将下载文件转换成挂载证据，也不授予 `prepare`、生产发布或回滚权限。

| 步骤 | 契约和验收 |
|---|---|
| 1. 固定读取来源 | 受信运行环境固定 Jenkins HTTPS origin 和发布 job，操作者只提供具体构建号与页面 ID。读取该编号的构建元数据、阶段和唯一归档 `output.json`。使用有期限、有限大小的 GET，拒绝重定向及响应中的任意下载地址。自动执行身份只需该 job 的构建和归档读取权限；从预期环境确认连通和权限，不能依赖个人浏览器登录。 |
| 2. 绑定实际英文 UAT | 构建须已完成且成功，`uat-en` 阶段唯一且成功。归档须绑定同一 job、构建号和实际 Jenkins build ID，并明确选中 `oversea` / `uat`，且英文镜像及其 UAT 部署均为 selected。校验完整 `zdoc_sha`、源镜像 revision 和 UAT 部署 digest；从 dev 源码构建的首片正例要求 revision 与 `zdoc_sha` 一致、源 digest 与实际 UAT 部署 digest 相同。仅凭 tag、总成功状态、阶段名称或 Prod 归档均不准入。保留原始 Jenkins 身份，使用明确的一对一绑定，不能仅凭编号替代挂载契约里的 `jenkinsBuildIdentity`。 |
| 3. 复用预览并复核 | 用部署的完整 SHA 读取已提交的页面回执和生成产物，与固定的 master、dev 和上游版本比较。校验配置中的 Cloud/BYOC 目标，记录构建和阶段身份、归档原始字节 SHA-256、部署 SHA/digest、Git 基线和比较结果；结束前重读构建证据与 refs，任一变化则暂停。镜像标签、发版人对两个页面视图的验收、开放更新 PR 分别记录状态；没有独立观察就保留 pending/unobserved。 |
| 4. 验收正常与暂停 | 先用已留存归档验证真实字段布局；用英文 Prod、中文 UAT、旧英文 UAT、错误 SHA/digest、歧义阶段、归档变化和访问失败验证停止原因。下一次正常英文 UAT 到来后，用一页仍有 current/next 差异、回执未变且两目标齐备的 Guides 跑真实预览。正式发版验收还需对不可变 digest 独立核对镜像的 revision 和 Jenkins build ID 标签，并记录发版人确认及同页开放更新 PR 的观察。 |

**实现交接。** 在最新 master 核对 #1353 的状态与差异后定实现基线。将 Jenkins HTTP 边界和归档验证收在 shared-docs 的发布证据 adapter，`packages/docs-tooling/src/shared-docs/adapters/promotion.ts` 复用已有单页比对，`packages/docs-tooling/src/shared-docs/commands/promote-guides.ts` 明确区分 Jenkins 实时、挂载和 replay 的预览入口。定向测试放在 `packages/docs-tooling/src/shared-docs/testing/`，覆盖请求目标、身份绑定、读回漂移、过期停止和正式预览进入 `prepare` 的拒绝。以 `pnpm test:for-change -- --base <base> --head HEAD` 核对完整差异并执行命中的命令。先交短方案和只读运行身份的证据，主审通过后再实现。Actions、批量提升 Draft 和实际部署各自另行交付。
