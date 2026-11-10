# WP12 上游更新：发现、影响报告与滚动 PR

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1b　**依赖**：[WP11 #921](https://github.com/zilliztech/zdoc/pull/921)、[WP9b #960](https://github.com/zilliztech/zdoc/pull/960) 已合并。

**状态（2026-11-10）**：A（[#1027](https://github.com/zilliztech/zdoc/pull/1027)）、B1（[#1055](https://github.com/zilliztech/zdoc/pull/1055)）与 B2（[#1155](https://github.com/zilliztech/zdoc/pull/1155)）均已合并。B2 按“Guides 本地规划与准备”的限定范围收尾；B3 第一片已合并（[#1189](https://github.com/zilliztech/zdoc/pull/1189)），其余 B3 切片与 B4 尚未实现，整个 WP12-B / WP12 均未完成，需求 pending 编号保留。实现和验证分别见 [A 走读](../walkthroughs/WP12-A.md)与 [B 阶段走读](../walkthroughs/WP12-B.md)。

## 目标

Guides 的上游原文或依赖变化时，形成可审核的更新 PR 和影响报告；只推进 next，不直接发布，失败时已采用版本仍有效。本卡先覆盖 Guides，Rust 手册级策略等 R1 配置契约稳定后单独补齐，WP12 总体状态保留该后续项。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 7 全文；场景 6、8 | 更新行为、通道变换、提升与锚点 |
| [技术设计 06](../../design/06-upstream-changes.md) | 全文 | 发现、滚动 PR、依赖页合并、失败处理 |
| [技术设计 04](../../design/04-channels-and-lock.md) | 来源配置、lock、快照、提升与标题改名 | 固定输入和 WP13 的边界 |
| [技术设计 05](../../design/05-publish-handoff.md) | PR 校验与触发时机 | 候选权限及合并后的采用路径 |
| [实现指南](../README.md) | 第 2、5、6 节 | fixture、验证层次、协作与 PR 格式 |

先读 zdoc README、适用 AGENTS 和实时测试/分支归属矩阵；有 CodeGraph 时先用它定位实现。核查当前 master，不仅依据历史计划。

## 范围

### 分阶段交付

| 阶段 | 内容 | 状态与停止点 |
|---|---|---|
| A：变化分析与报告 | 固定输入、原文/依赖与 Cloud 输出、锚点关系、采用单元、报告 | 已合并 #1027 |
| B1：只读发现与生命周期证据 | 固定输入、认证观察、只读 CLI 和报告 | 已合并 #1055，不写远端 |
| B2：本地规划与准备 | `update-plan` / `update-prepare`、可信工具集、隔离候选、proof/journal 与恢复 | 已合并 #1155；按受限范围收尾，不代表远端事务或 Linux 支持完成 |
| B3：GitHub 事务与恢复 | 远端身份、保留人工改动、滚动 PR、精确 head 校验、响应丢失与并发恢复 | 第一片已合并 #1189；第二片进入短计划审阅，第 3–4 片未实施，第 3 片须先通过有界 API 预检 |
| B4：工作流与 rollout | 定时/手动 report-only、权限隔离、真实外部 smoke 与需求验收 | 未开始；既有 Fetch schedule 不等于新的上游更新 workflow |

### A 的允许路径

A 的可改路径如下，均相对于 zdoc 根目录。计划和验证证据不混入实现 PR：

- `packages/docs-tooling/src/shared-docs/core/updates/types.ts`
- `packages/docs-tooling/src/shared-docs/core/updates/impact.ts`
- `packages/docs-tooling/src/shared-docs/core/updates/anchors.ts`
- `packages/docs-tooling/src/shared-docs/core/updates/units.ts`
- `packages/docs-tooling/src/shared-docs/adapters/update-inputs.ts`
- `packages/docs-tooling/src/shared-docs/adapters/build-page.ts`（仅可选只读观察，默认结果与失败行为不变）
- `packages/docs-tooling/src/shared-docs/testing/updates/impact.test.ts`
- `packages/docs-tooling/src/shared-docs/testing/updates/anchors.test.ts`
- `packages/docs-tooling/src/shared-docs/testing/updates/units.test.ts`
- `packages/docs-tooling/src/shared-docs/testing/build/build.test.ts`
- `packages/docs-tooling/src/shared-docs/fixtures/updates/scenarios.json`
- `packages/docs-tooling/src/shared-docs/fixtures/updates/SOURCE.md`
- `packages/docs-tooling/src/shared-docs/fixtures/milvus-docs/build.ts`
- `packages/docs-tooling/src/shared-docs/fixtures/milvus-docs/build.test.ts`
- `packages/docs-tooling/src/shared-docs/README.md`（只记录 A 已实现的内部接口）

B3/B4 不能直接沿用下面的总体范围开工。下线证据缺失不能推断删除；完整 7-9 还需与 WP14 对接。Rust 手册级更新待 R1 契约稳定后单独细化，不计入已验收的 A。

### B 的计划交付

固定最新 master，细化 B 的精确路径、code-to-test selector、GitHub API 身份、权限、并发及失败恢复策略；明确默认只报告的 rollout 和真实外部 smoke。计划经主会话审定后才实施，不因 A 通过而自动获得 workflow、Base/dev、上传或付费翻译权限。

### B2 收尾裁决与保留边界

- #1155 于 2026-11-09 合并，merge SHA `98de1d8426b1d251b8393ea9b5ad91686de14776`。Guides 本地规划和候选准备完成；原始 B 路线图中的远端身份和 mutation 设想不计入 B2。
- [scheduled Fetch 42599114207](https://github.com/zilliztech/zdoc/actions/runs/42599114207) 在含 B2 的工具版本 `15387649ba38bcea441366df8d3a5ccafae8ecfd` 上成功，10 个源发布单元全部写入 dev，中英文 assembly 和最终验证通过。这是合并后既有发布链兼容性证据，不是本地更新 CLI 或自动更新 PR 的执行记录。
- 此次 `runTranslations=false`，不能声称下游 Translation 或线上部署完成；canonical-link 报告中的告警另作内容维护，run 成功不等于页面全部无问题。
- Linux 可信工具集捕获仍由生产代码明确拒绝；SDK provider 仍返回 `PROVIDER_NOT_INSTALLED`。两项保持未交付，不能借 Fetch 在 Linux 成功而取消限制。
- `7-1`—`7-10` / T05 不因阶段收尾从 pending 删除。完整生命周期仍与 WP14 衔接，Rust/SDK 更新另按已合并接口安排。

### B3 精确实施计划（2026-11-09，主审已审定）

**目标**：在保留人工历史的前提下，把 Guides 本地候选接到可读取重建的 GitHub PR 事务；默认不授予远端写能力。B3 交付库与离线契约，B4 交付合格 runner、工作流、rollout 和真实 smoke。第 1/2 片可先实施；第 3 片入口增加下述有界 API 可行性预检，通过后才进入事务实现，第 4 片依赖第 3 片。各片合并后再从最新 master 开下一片，不叠 PR；实施时逐项执行 `executing-plans` 的测试、实现、自审步骤，不再拆出独立协调文档。

**固定基线**：产品 `origin/master=11fb432e006e297381a29e3f038b6124b76438cd`（含 #1155）；本卡设计 base `8765410c6e28786599b6d6e0ab06863fc00be91d`。产品证据均来自该 ref 的 `git show` / `git grep`，不是 root 的旧 checkout 或 B2 worktree 的测试结果。两仓当前检查位置均无 `.codegraph/`；实施分支若存在则先用 CodeGraph。技术栈沿用 TypeScript、Zod、Vitest、Git objects 和 GitHub REST/GraphQL，不增加 SDK 或依赖。

#### 执行与审阅流程

- 本卡维护总计划；每片在 `liyun95/zdoc` 建一个 Draft PR，先提交 `.claude/plans/wp12-b3-slice-N.md` 的短实施计划，引用本卡固定版本，不复制或重做完整 B3 设计。计划列出接口、测试断言、允许路径和相对总计划的差异。
- fork 内 PR 的 base 必须等于已核验的上游 master 基线；fork master 不适用时建立专用 review-base 分支，不重置已有分支。方案经主会话明确通过后，同一分支/PR 增量实现和修订；先跑 focused 与快速检查，经主审及修正复核后，再在最终 HEAD 跑完整测试，避免旧版本全量阻塞修正；review 绑定精确 HEAD，作者逐条回复证据，由 reviewer 复核后解决线程。
- 第一片只实现本卡两个允许产品文件。计划文件是 fork 审阅阶段的文档例外；上游提审前用普通提交移除它，计划和讨论仍保留在 fork PR 历史。完整 diff 必须再经 selector 核查，不能跳过 unmapped 路径。
- 本地 code review 通过后，从同一 feature 分支向 `zilliztech/zdoc:master` 提 PR，附 fork review 链接与最终 HEAD 测试结果。fork PR 不必先合并到 fork master；上游 PR 仍需自己的 CI 和 review。每片上游合并后才开启下一片，不提前启动后续范围。

#### 已核实的接口与缺口

以下产品路径均相对 zdoc 根；链接固定到上述产品基线。

| 当前实现 | 可复用部分；B3 必须补上的边界 |
|---|---|
| [`commands/update-plan.ts`](https://github.com/zilliztech/zdoc/blob/11fb432e006e297381a29e3f038b6124b76438cd/packages/docs-tooling/src/shared-docs/commands/update-plan.ts)、`commands/update-prepare.ts` → `adapters/updates/local-runner.ts` | `runLocalCommand` 先校验 launcher，捕获真实 tooling HEAD；`createLocalUpdateRunner(capture)` 才能得到生产 runner。`LocalUpdateRequest` 固定 M/D/source；`existing.localEvidence` 是本地 owned evidence 路径，不能改成远端凭证。结果 `operations: []` 不变。 |
| [`core/updates/envelope.ts`](https://github.com/zilliztech/zdoc/blob/11fb432e006e297381a29e3f038b6124b76438cd/packages/docs-tooling/src/shared-docs/core/updates/envelope.ts) | `ObservedPr`、`TransactionPreconditions`、`BotRevision`、`PreparedBase`、`CandidateSnapshotProof` 已有严格 schema；它们本身不认证 GitHub。新远端类型放 `remote.ts`，不扩大这些冻结 v1 envelope。 |
| [`adapters/updates/transactions.ts`](https://github.com/zilliztech/zdoc/blob/11fb432e006e297381a29e3f038b6124b76438cd/packages/docs-tooling/src/shared-docs/adapters/updates/transactions.ts) | `createScratchTransaction` / `prepare` 普通 merge M、human head、donor heads；`createCandidate` / `validateCandidate` 独立验证 next-only、完整 tree、祖先和确定性 K；`install` 只有 scratch ref 的 CAS。不会 fetch/push。 |
| [`adapters/updates/metadata-store.ts`](https://github.com/zilliztech/zdoc/blob/11fb432e006e297381a29e3f038b6124b76438cd/packages/docs-tooling/src/shared-docs/adapters/updates/metadata-store.ts) | `createMetadataStore().read()` 仍返回 `REMOTE_AUTH_REQUIRED`；`createLocalMetadataInspector` 只认重新验证的本地 journal、同一 trusted baseline 和本地 origin。`core/updates/metadata.ts` 的 trailer 是一致性数据，作者字符串不是身份。远端历史须另设认证入口。 |
| [`adapters/updates/github.ts`](https://github.com/zilliztech/zdoc/blob/11fb432e006e297381a29e3f038b6124b76438cd/packages/docs-tooling/src/shared-docs/adapters/updates/github.ts) | `GitHubReads` 只放行 zdoc repository/actions/contents GET 和 artifact ZIP；`retainedMetadata` 绑定 repository ID `660446555`、run/attempt/artifact。没有 PR/ref/commit/check 客户端，错误也未区分不存在。保持 B1 行为，B3 独立 typed client。 |
| [`adapters/updates/toolset.ts`](https://github.com/zilliztech/zdoc/blob/11fb432e006e297381a29e3f038b6124b76438cd/packages/docs-tooling/src/shared-docs/adapters/updates/toolset.ts)、`local-runner.ts` | `captureTrustedToolset` 明确拒绝 Linux；`collectFixedGuidesUnits` 遇 SDK 返回 `PROVIDER_NOT_INSTALLED`。Darwin 本地证据不证明 GitHub macOS runner 合格。 |
| [现有 PR 校验](https://github.com/zilliztech/zdoc/blob/11fb432e006e297381a29e3f038b6124b76438cd/.github/workflows/shared-docs-validate.yml) | dispatch 有 `source_sha/base_sha/request_id`，没有固定 D；执行 H 上的工具并在运行时解析 dev。它服务普通 PR，但不满足 B3 的可信 H/M/D 收据，不把现有同名 green check 当作验收。 |
| `scripts/docs-workflow/publication-github-client.js`、`publication-transaction.js`、`checkpoint-publication.js` | 可参考 artifact 鉴别、push 后读回与 `REMOTE_STATE_UNKNOWN` 分类；它们绑定生产 publication，不抽成通用 writer，不修改或调用其 dev 写入路径。 |

#### 已定的工程决策与平台停止点

1. **先纯适配，后真实 runner**：第 1/2 片可以在普通 Node/Vitest 上实现和验证，不调用 `captureTrustedToolset`；第 3 片也以离线测试开发，但开始大规模实现前必须通过下述 API 可行性预检；第 4 片的故障测试使用内部 fixture capability，明确不算生产资格。生产桥接必须由真实 capture 创建能力；Linux 保持拒绝。B4 首选评估 GitHub macOS runner 的现有 Darwin 路径，固定镜像、架构、Node/Git/pnpm/gh、权限/ACL/native closure 和无候选代码执行证据；不合格就停止，Linux 支持另开前置任务，不能现场降级。
2. **默认零写入**：只读 client 和 writer capability 分开；普通请求 JSON、环境变量 `true`、CLI 参数都不能自行创建 writer。B3 不新增 schedule、公开写 CLI 或 workflow。生产能力只能由未来受信工作流入口在资格、仓库、身份和授权均满足后创建。允许离线验证 writer 的真实请求序列，不把 fake adapter 算真实 GitHub 接线。
3. **精确提交与签名分开**：记 M=固定 master/tools，D=固定 dev，H=survivor 当前 head，P=普通合并后的 prepared base，K=B2 的确定性候选。保持 `P → K` 及 `proof.candidate=K`。上传缺失的 blob/tree/commit objects 时逐个验证返回 OID；REST create-commit 若规范化导致 OID 不同，直接 hold，不能以同树代替 K。上传不更新目标 PR ref。
4. **推荐写原语**：用 [GraphQL `updateRefs`](https://docs.github.com/en/graphql/reference/git#updaterefs) 的 `beforeOid`、`afterOid`、`force:false` 做目标 ref CAS；创建用全零 before。REST ref 的 `force:false` 只保证快进，不保证 expected-old，写前重读也不是 CAS。该原子性仅涵盖一次调用内 refs，不涵盖 PR、dispatch 或 donor。
5. **独立 seal S**：在 `refs/heads/shared-update-staging/<transactionId>` 上先 CAS absent→K，再以 [`createCommitOnBranch`](https://docs.github.com/en/graphql/reference/commits#createcommitonbranch) 的 `expectedHeadOid=K` 创建无文件变化 S；[FileChanges](https://docs.github.com/en/graphql/reference/git#filechanges) 允许两列表为空。要求 `parent(S)=[K]`、`tree(S)=tree(K)`、签名验证有效及 API actor 匹配才 CAS H→S。签名只在 GitHub 支持时提供，缺失即 hold。S 消息用独立 `Shared-Update-Seal` schema，绑定 repositoryId、transactionId、unit/plan/proof 摘要、M/D/P/K、tree、previousSeal、保留 heads、执行 run/attempt；不复制 `BotRevision` trailer。S 不能写入 B2 proof，最终精确验证针对 S。
6. **身份不是昵称**：策略固定 github.com、zdoc 数字 repository ID、完整名、base=master、允许的 branch 前缀、actor 数字 ID、check App 数字 ID、受信 workflow 路径和定义摘要。actor、App、workflow 是不同身份；不得由提交 email、PR body、label、请求自报 ID 或任意 `GET /user` 成功替代。策略值从受信工具代码/工作流配置给出，不从候选 H 读；B3 fixture 用测试 ID；第 3 片前的 API 预检核验测试仓库的真实身份，生产身份仍由 B4 只读核验，不猜数字。
7. **运行身份的限度**：GitHub commit 的作者关联和签名不单独证明是哪一个 workflow 使用了 token。远端 origin 认证还要求受信执行 run/attempt、工作流定义与不可变 artifact 收据共同绑定 S/K；不能让同 App 的任意 green check 冒充。现有 GITHUB_TOKEN 路线保留，不新增 PAT/App；token 只在独立 writer 进程可见，不进候选生成或报告。若预检中实际 GITHUB_TOKEN 不支持所需签名/API，则在第 3 片前停止并修订架构，不能悄悄放宽；测试仓库通过仍不等于生产平台资格。
8. **PR 状态不是 CAS**：draft/ready/close API 没有 head 条件写。B3 默认新建 draft，已有 PR 必须确认 draft 后才尝试 ref CAS，前后重读检测人工变更；检测到变化立即 hold，保留分支和提交。默认不自动 ready、不自动 close donor；输出精确 `readyProposal` / `donorCloseProposals`，需后续明确接受这类非原子状态写的策略才能启用。这样不能宣称完整滚动 PR 收尾已验收；并发 ready/merge 的剩余窗口须在 B4 仓库保护与 smoke 中验证，不能只靠 draft 保证禁止合并。

**对设计的有界差异**：B3 先交完整事务内核与默认保守策略；自动 ready/关闭 donor、可信验证 producer 和工作流激活仍未交付。保留 [06](../../design/06-upstream-changes.md) 的最终产品目标，不改设计或删 pending。第一片无待用户裁决问题；第 1/2 片不依赖真实写权限。API 可行性预检阻止第 3 片进入大规模实现；完整平台资格、生产身份和非 CAS 收尾策略继续阻止 B4 激活。

#### 第 3 片入口：有界 API 可行性预检

这是 B4 资格工作的前置小项，用来及早验证事务架构依赖的 GitHub 行为；不等于完整 runner 资格或生产激活。本计划不执行任何外部写。第 1/2 片可以先完成；如果还没有获准的隔离测试仓库及写入授权，第 3 片保持草案，不大规模实现，第 4 片也不绕过此前置。

- 在获准的隔离测试仓库使用该仓库真实 `GITHUB_TOKEN`，记录仓库 ID、token 所属 App/actor 与执行 run/attempt；不用 PAT 冒充。授权范围先固定：一组小型 Git objects（含普通双亲 merge 和确定性 K）、一个 `shared-update-staging/<transactionId>` ref、无 PR/生产分支/生产 workflow 写入；清理仅限该 ref，并另按已授予的清理范围执行。
- 验证 REST 上传返回的每个 blob/tree/commit OID 与本地完全一致；验证零文件修改 seal S 的 `parent=[K]`、`tree(S)=tree(K)`、有效签名及实际 API actor。任何规范化、签名缺失或身份不符都停止，不用同树或作者字符串替代。
- 仅在该单 staging ref 上验证 `updateRefs(beforeOid, afterOid, force:false)`：absent 创建、正确 expected-old 快进、错误 expected-old 拒绝且 ref 不变；用真实请求成功后故意丢弃客户端响应，再通过读取精确 ref/objects 重建结果，不盲重试。
- 留存脱敏请求/响应、实际 object/ref OID、签名/actor、错误 CAS 前后 ref、丢响应读回结果。主审确认全部行为符合契约后才进入第 3 片；预检失败先修订本卡架构，不能先实现再将失败推迟 B4。测试仓库通过只证明 API 可行性，native closure、ACL、runner/权限隔离、可信 validation producer 与生产 smoke 仍由 B4 完成。

#### 公共远端契约（新增，不覆盖 B2 schema）

新文件中的类型全部带 strict schema、明确尺寸上限；以下是接口草图，不是现有 API。`Oid`/`Digest` 使用已有 schema。`RemotePolicy` 是受信调用方注入的策略，`RemoteFacts` 只能由只读 adapter 重新读取；反序列化 JSON 不产生 capability。

```ts
type ReadResult<T> = { kind: 'found'; value: T }
  | { kind: 'absent'; evidence: BlobRef[] }
  | { kind: 'unknown'; reasons: string[] };
type Decision = { status: 'accepted'; evidence: BlobRef[] }
  | { status: 'hold'; reasons: string[] };
// ExactValidationReceiptV1: repositoryId, prNumber, head=S, master=M, dev=D,
// tools=M, unitKey, planSha256, seal=S, requestId, runId, runAttempt,
// workflowPath, workflowDefinitionSha256, outputDigest, conclusion.
acceptExactValidation(expected, apiFacts, receipt, policy): Decision;
// RemoteSealV1 and RemoteTransactionJournalV1 are separate from BotRevision.
// transactionId = SHA256(canonical repo/unit/plan/M/D/expected heads/proof identity).
reconcileRemoteTransaction(intent, observedFacts): NextAction | Hold;
```

接受谓词同时检查：run repository/head repository、event、workflow ID/path/定义、run attempt、执行工具 M、receipt 的 H/M/D、requestId、check suite/run/app/head/status/conclusion，以及唯一未过期 artifact 的 API digest 与真实字节。dispatch run 的 `head_sha` 是工具 M 时不能要求它等于 S；用可信 receipt 与检查目标单独绑定 S。当前 PR head/base 和 master/dev 再读必须仍匹配预期。失败、pending、cancelled、skipped、旧 attempt、同名错误 App、receipt 缺失或 malformed 均 hold。

原始 `404` 不自动等于 absent：先认证 repository 仍可读、端点范围正确，再用精确 ref/PR 清单与有界分页交叉确认；403/429/5xx/超时/GraphQL errors/截断/分页上限都为 unknown。API HTTP 200 内含 GraphQL errors 也不算成功。所有诊断脱敏，不保留 Authorization、子进程 stderr 或 token。

#### 切片 1 — 纯远端观察与精确接受谓词（已合并）

**执行记录（2026-11-10 更新）**：[fork Draft PR #18](https://github.com/liyun95/zdoc/pull/18) 保留方案、主审意见和修订；[上游 PR #1189](https://github.com/zilliztech/zdoc/pull/1189) 的 HEAD 为 `4d33a1131716c8db2b3063c0b08800b69e5caa7a`，净差异仅下列两个产品文件。主审已验证 base=M、触发者/写入者身份分离等修正；本地完整检查在该 HEAD 上通过：shared-docs 1352 passed / 0 failed / 6 既有 skipped、typecheck、matrix 25/25、policy 118/118、完整 diff selector 与 diff-check。上游 CI 通过后于 2026-11-10 合并，merge SHA `87f103f926d27943861278181308ebbb7cb73fe0`；总计划亦已由设计 PR #78 合并（`4cc9e9436e6e9670443276196734979653065300`）。第二片从该产品基线开始准备短计划。此通过不代表真实远端认证、runner 或 Linux 资格完成。

**允许路径**：新增 `packages/docs-tooling/src/shared-docs/core/updates/remote.ts`、`packages/docs-tooling/src/shared-docs/testing/updates/remote.test.ts`。无其他产品文件改动；不触网、不捕获工具集、不新增入口。

**输入/输出**：上述严格远端事实、策略及验证 receipt → accepted/hold 与原因；保留 `ObservedPr` v1，通过新外层结构携带 repo/ref/actor/App/run 事实。第一片只实现读取状态分类、`RemoteSealV1` 和 `ExactValidationReceiptV1` schema、`acceptExactValidation`；事务 state machine 留第 3 片，避免首次 PR 过大。

- [ ] 写表驱动失败测试：唯一满足所有约束的 S/M/D 成功；分别改变 head、M、D、tools、repositoryId、actorId、App ID、workflow path/definition、run attempt、requestId、artifact digest，必须得到明确 hold 原因；相同 check 名不能覆盖错 App；缺字段/额外字段拒绝。
- [ ] 运行 focused，确认因接口尚不存在而失败；实现纯函数，仅依赖已有 canonical/schema，无网络/Git/文件读取。
- [ ] 再跑 focused 与本片 selector 联集。断言 input 不被修改；unknown 永不转为 absent；两份匹配 run/artifact 判歧义，旧 check 即使 success 也拒绝。

```bash
pnpm test:for-change -- packages/docs-tooling/src/shared-docs/core/updates/remote.ts packages/docs-tooling/src/shared-docs/testing/updates/remote.test.ts
pnpm vitest run packages/docs-tooling/src/shared-docs/testing/updates/remote.test.ts
```

**验收/停止**：首片纯测试全部通过、selector 无 gap；只声明“接受契约已实现”。无平台/凭据前置；不实现 Github transport、不宣称远端身份已认证。返回主会话独立 review 后才进入第 2 片。

#### 切片 2 — GitHub 只读事实与远端历史认证

**执行状态（2026-11-10）**：产品基线 `87f103f926d27943861278181308ebbb7cb73fe0`；[fork Draft PR #19](https://github.com/liyun95/zdoc/pull/19) 进入短计划主审，尚未实现。先确定签名/API 身份、attempt 归属、原始 Git/证明材料和传输边界，再批准代码；全量测试在主审修正完成后的最终 HEAD 执行。

**允许路径**：新增 `adapters/updates/remote-github.ts`、`adapters/updates/remote-metadata.ts`、`testing/updates/remote-github.test.ts`、`testing/updates/remote-metadata.test.ts`；修改 `core/updates/remote.ts`、`testing/updates/remote.test.ts`。以上均在 `packages/docs-tooling/src/shared-docs/` 下。

**入口**：`createRemoteReads({ policy, transport, evidence })` 返回 typed `readRepository/readRef/readPull/scanPulls/readCommit/readRun/readChecks/readArtifact`；`inspectRemoteHistory({ head, donorHeads, master, policy }, reads, objects)` 返回 `verified` 的不可序列化 history capability 或 hold。GET/只读 GraphQL 查询 allowlist，不导出任意 URL/GraphQL 字符串接口。默认 transport 只访问 github.com/API 的固定 host；测试注入本地故障服务，不改生产 host。

- [ ] 先用 API fixture 与真实临时 Git objects 测：伪造作者、复制 trailer、错误签名 actor、fork head、错 base、删除 ref、权限隐藏404、重复/漏分页、history 截断、大小超限和不可比较 revision，均 hold。
- [ ] 实现受限 transport 与 evidence 留存；复用 B1 的规范化/摘要思想，不能扩大 `GitHubReads` 的放行表来获得隐式写入口。PR 全量扫描按同仓、base、namespace、已认证 subjects 分组；重叠但身份未知的 PR 必须阻止该 unit，不能忽略后重复创建。
- [ ] 独立读取完整 Git graph，验证每个 seal 的签名/API identity、执行 provenance、唯一 K parent 和同 tree；再验证 K 的原始 BotRevision、P/previous chain、完整 next-only delta、保留人类 heads、报告/计划摘要。历史 M/tools 以该次受信运行验证，不能强制等于本次 M，也不能仅因为旧 M 是祖先就信任。
- [ ] 本次 H 可以是 S 或 S 的人工后继；后继全部作为数据检查，保留普通 merge 祖先；候选执行路径有改动则 hold。失效/过期 provenance 无法独立重建时 hold，不降为本地一致性。
- [ ] focused 绿后运行 selector；adapter contract 测试直接调用生产解析器和谓词，网络替身只模拟传输与竞态。

```bash
pnpm test:for-change -- packages/docs-tooling/src/shared-docs/adapters/updates/remote-github.ts packages/docs-tooling/src/shared-docs/adapters/updates/remote-metadata.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-github.test.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-metadata.test.ts packages/docs-tooling/src/shared-docs/core/updates/remote.ts packages/docs-tooling/src/shared-docs/testing/updates/remote.test.ts
pnpm vitest run packages/docs-tooling/src/shared-docs/testing/updates/remote-github.test.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-metadata.test.ts packages/docs-tooling/src/shared-docs/testing/updates/remote.test.ts
```

**验收/停止**：全程零 mutation 请求；全部图/身份/收据证据可以定位。`createMetadataStore` 原占位和 B2 local inspector 不被包装成远端认证；未有真实 trusted producer 时只用 fixture 证明契约，生产读取返回证据缺口。

#### 切片 3 — 精确 ref CAS、draft PR 与响应丢失重建

**入口条件**：第 1/2 片已合并，且上述有界 API 预检证据已由主审接受。未满足时本片仅为草案，不开始大规模实现；不能用 HTTP fixture 代替真实 API 可行性。

**允许路径**：新增 `adapters/updates/remote-transaction.ts`、`testing/updates/remote-transaction.test.ts`；修改 `adapters/updates/remote-github.ts`、`testing/updates/remote-github.test.ts`、`core/updates/remote.ts`、`testing/updates/remote.test.ts`。均在 shared-docs 下；不接 CLI/workflow。

**入口**：`createRemoteTransaction({ reads, writerCapability, evidence })` 的 `apply(intent)` / `reconcile(intent)`；writer 是内存能力，不能由 journal 的 `authorized:true` 构造。`intent` 绑定 repository、M/D、unit、plan/proof、K/P、expected PR heads、staging ref 与 transactionId。journal 新增独立 schema，按动作前 intent/动作后读取事实落盘；journal 是恢复提示，所有远端成功状态都须读回重建。

```text
disabled → report-only (zero writes)
authenticated intent → upload exact objects → staging absent→K CAS
→ append signed S at expected K → verify S → target H(or absent)→S CAS
→ discover/create draft PR → request exact validation → accepted/held
```

- [ ] 先测试 mutation allowlist：对象 POST、staging/target ref 的 `updateRefs(force:false)`、seal、创建 draft PR、显式校验 dispatch；禁止 master/dev ref、force、删除 ref、merge、Base/图片/翻译、ready 和 close。缺 capability 时包含对象上传在内全部零写。
- [ ] 对象上传只遍历已验证 scratch 闭包中远端缺失对象；已有对象按 OID 读回，新增对象逐项比 hash。不能重建人工提交来替代已有 OID；不支持的对象/签名头保留原对象或 hold，不能丢字段。
- [ ] staging 名由固定前缀+transactionId 唯一确定。创建响应丢失后读取该精确 ref：K 可继续封签；满足同一 intent 的 S 可复用；其他值 hold。封签响应丢失读取 K 的唯一已验证后继，不能靠 `clientMutationId` 假设幂等；多个 seal/未知后继 hold。B3 不自动删 staging。
- [ ] 写 target 前重读 M/D、H、donor heads、PR state/base/draft 与 authority。M/D 或任何 head 改变则原 intent 作废、重新规划；最终 ref CAS 再拒绝读取与写入之间的人工 push。M/D 不在同一次 ref CAS 锁内，写后再读发现移动则 held，不接受旧验证、不回滚。
- [ ] 创建 PR 响应丢失：按已知 repository+exact head ref+base 列出 open/closed/merged PR，再验证 actor、seal/unit 身份；唯一匹配复用，无匹配且完整读取确认后才重试 create，同 ref 已 closed/merged 不重开/改名绕过，多匹配 hold。不能只用标题或 marker 去重。
- [ ] ref 写响应丢失：远端等于 S → 确认写成；远端为 S 的人工后继 → 记录已写成但 stale、重新规划；仍是 H → 完整读取后重新预检才可再 CAS；其他 ancestry、读取失败 → `REMOTE_STATE_UNKNOWN`，不盲重试。
- [ ] dispatch 带稳定 requestId 和 S/M/D；超时先按 workflow/request/run/attempt 查询，等待有界，歧义/未知即 hold。未找到不接受旧 green，也不循环派发。真实 workflow 尚未安装则 `VALIDATOR_NOT_INSTALLED`，PR 留 draft。
- [ ] donor 选已认证集合中最早 `created_at`、相同时间按 PR number 的 survivor，合入所有 donor 精确 head。只有 S 精确验证成功才输出 close proposals；若仅部分 donor 已被人工关闭，重跑核对关闭状态和已保留 ancestry，只输出剩余且未变化者。任一 donor 新 push 则不提关闭；保留所有 branches。成功响应也必须读回。

```bash
pnpm test:for-change -- packages/docs-tooling/src/shared-docs/adapters/updates/remote-transaction.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-transaction.test.ts packages/docs-tooling/src/shared-docs/adapters/updates/remote-github.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-github.test.ts packages/docs-tooling/src/shared-docs/core/updates/remote.ts packages/docs-tooling/src/shared-docs/testing/updates/remote.test.ts
pnpm vitest run packages/docs-tooling/src/shared-docs/testing/updates/remote-transaction.test.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-github.test.ts packages/docs-tooling/src/shared-docs/testing/updates/remote.test.ts
```

**验收/停止**：本地 Git + HTTP 故障服务覆盖每次 mutation 前后中断/响应丢失/并发写，断言请求序列、ref、PR 数量、preserved ancestry 和 hold 原因。本片实施测试除临时裸仓/fixture 服务外无真实远端写；CAS、原样 OID、签名及 GITHUB_TOKEN 的 API 可行性必须已有入口预检证据，完整 runner 与生产可用性仍列 B4 资格项。禁止声称跨 PR 原子事务或完整 donor 自动收尾。

#### 切片 4 — B2/远端历史桥接与默认只读编排

**允许路径**：新增 `adapters/updates/remote-runner.ts`、`testing/updates/remote-runner.test.ts`；修改 `adapters/updates/local-runner.ts`、`adapters/updates/transactions.ts`、`adapters/updates/remote-metadata.ts`、`testing/updates/local-runner.test.ts`、`testing/updates/transactions.test.ts`、`testing/updates/remote-metadata.test.ts`、`README.md`（此项仅指 shared-docs 包内 README）。均在 `packages/docs-tooling/src/shared-docs/` 下。不改根 README、package scripts、CLI 注册或现有 workflows。

**入口/边界**：`createRemoteUpdateRunner({ capture, reads, policy, writerCapability? })` 为内部库入口。`observe` 生成 intent/holds；只有调用方已持有 writer capability 才能 `apply`。capture 仍由真实 `captureTrustedToolset` 提供，保留 Linux 拒绝；request 不能提供 runtime、provider 或 trusted flag。必要纯编排 seam 只供测试，沿用 B2 的内部注入模式。

- [ ] 测试先证明旧命令契约不变：`LocalUpdateRequest.existing.localEvidence` 仍只认 owned local journal；把远端 seal/S 路径伪装为 localEvidence 会拒绝，`operations: []` 仍成立。未经 remote inspection 的 S 不可作为可信 origin。
- [ ] 新增 `prepareRemoteCandidate` 桥接：消费第 2 片在同进程创建的 history capability，重读 H/donors/M/D；在新的 evidence root 调用 `createScratchTransaction.prepare` 普通合并，调用 `collectFixedGuidesUnits(capture, ...)` 和 `planUpdateBatch` 重新采集/规划，再 `createCandidate/validateCandidate` 得到新的 P/K/proof。复用 B2 的 fresh/source/access 检查，抽出最小内部 helper，不复制整套 runner。
- [ ] 远端历史 K/S 的 provenance 作为独立 `remote-origin` 证据留存，不能重造 B2 owned journal。新 candidate 的 `previousBotCommit` 指向已认证的旧 K，`previousSeal` 只在新 seal 中记录；旧 S 是 H 的普通祖先。历史 M 可不同于当前 M，旧 proof 不改写；本次计划与 proof 完全基于当前 M。无法验证旧 origin 或完成桥接就 hold，不回退成 new PR。
- [ ] 使用 capability 授权的旧 origin 边界校验新 K；B2 的 `createLocalMetadataInspector` 继续只处理纯本地链。`createScratchTransaction` 如需新增 history 验证 helper，仍仅处理 Git facts，不访问 GitHub。新 K 不要求被旧 local inspector 当成纯本地 origin；远端 reader 负责后续跨运行认证。
- [ ] 人工改配置/Cloud 内容且在允许数据路径内时按新 H 重算，tree 和祖先都保留；改工具/依赖/工作流则 hold。master 合并提升导致 current/next 两侧同改时沿用 `BOTH_SIDES_LOCK_CHANGED` 安全停止并报告，不自行解决冲突；不做 WP13。无变化不增 K/S、不新建 PR，draft-failure 可保留失败报告但不得产生 ready/close proposals。
- [ ] 恢复不信 journal phase：遗失本地输出可从远端身份/objects/收据恢复观察并重新规划；缺 raw 证据或精确验证 receipt 就 hold。重跑相同完成 intent 无新 commit/PR；新增内容变化才生成新 intent。
- [ ] 包内 README 写清库状态、P/K/S、默认零写、未知状态和恢复输出，明确无公开写命令。根 operator README 与真实 workflow 使用说明一起由 B4 更新，不能提前记载不存在的命令。

```bash
pnpm test:for-change -- packages/docs-tooling/src/shared-docs/adapters/updates/remote-runner.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-runner.test.ts packages/docs-tooling/src/shared-docs/adapters/updates/local-runner.ts packages/docs-tooling/src/shared-docs/adapters/updates/transactions.ts packages/docs-tooling/src/shared-docs/adapters/updates/remote-metadata.ts packages/docs-tooling/src/shared-docs/testing/updates/local-runner.test.ts packages/docs-tooling/src/shared-docs/testing/updates/transactions.test.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-metadata.test.ts packages/docs-tooling/src/shared-docs/README.md
pnpm vitest run packages/docs-tooling/src/shared-docs/testing/updates/remote-runner.test.ts packages/docs-tooling/src/shared-docs/testing/updates/local-runner.test.ts packages/docs-tooling/src/shared-docs/testing/updates/transactions.test.ts packages/docs-tooling/src/shared-docs/testing/updates/remote-metadata.test.ts
```

**验收/停止**：真实临时 Git 证明确切 P→K→S→人工后继→新 P→新 K 的连续 ancestry，跨 M 的旧 origin 不混成新本地 journal。内部 fake 平台测试通过不能解锁生产。B3 停在可审库/测试与明确的 B4 handoff，不开工作流、不升级 Linux、不调用生产 Fetch/Translation。

#### 共用验收、证据与 B4 交接

每片开始前按上列**全部实际变更路径**运行 selector，新增路径已被 `shared-docs/**` 覆盖；新增 narrow matrix 行不是首片前置。若实际范围扩展导致 unmapped，先修实时 matrix 与人读 specification，再实施；不能漏选来缩短验证。命令中的新增文件是实施允许路径，不表示本次规划已创建产品文件。

本次从固定基线提取 `select-tests-for-changes.js`、`test-matrix.json`、`master-tooling-sync.json` 到设计 worktree 的临时证据目录运行 selector：允许路径均为 master-tooling，现有联集为 `pnpm test:shared-docs`、`pnpm typecheck`、`pnpm test:workflow-matrix`、`git diff --check`。这是固定源文件的 selector 预检，不是产品 checkout 的测试通过。证据根 `.claude/wp12-b3-plan/` 不提交。

每片 focused 完成后运行完整 diff 的最终 selector，执行返回联集并加 workflow policy；第一次独立分支未提交时用逐路径模式覆盖 working diff，提审用 base/head 模式防止遗漏：

```bash
pnpm test:for-change -- --base origin/master --head HEAD
pnpm test:shared-docs
pnpm typecheck
pnpm test:workflow-matrix
pnpm test:workflow-policy
git diff --check
```

不修改 Fetch/Translation/publication/recovery，故这四片不主动触发真实 production replay；若越过该边界必须重新审范围并按 README/实时 selector 补 hermetic 与真实 retained-artifact replay。若改根 README/matrix/package scripts，当前矩阵还会选 `test:replay:contract` 与 `test:replay:all`，不能省略。保留所有 `7-1`—`7-10` / T05 pending、golden、requirements、dev-owned 内容；编号测试只证明本片行为，不表示端到端验收。

B4 必备交接清单（仅定义条件，本卡不实施）：

- 受信 validation producer 从 M 的代码执行，把 H/S 当数据，固定 D；生成上述 receipt，留存 run/attempt/定义/artifact 身份。候选不得选择执行脚本或覆盖 verifier；不改现有普通 community PR 校验语义。没有该 producer，B3 的 `acceptExactValidation` 必须保持拒绝，不能临时接受现有 green check。
- 资格报告须覆盖实际 runner 的 capture、native/ACL/依赖闭包、生成过程无写 token、writer 权限隔离；现有 macOS 本地结果及 scheduled Fetch 都不能代替。第 3 片前已预检的 GITHUB_TOKEN actor/App、对象原样上传、seal 签名与 CAS 证据必须复核适用性；完整 runner 上的显式 dispatch/收据与权限隔离仍须在隔离测试仓库验证。
- 真 smoke 开始前列出获准仓库/branch 前缀、最多 PR/ref 数、固定输入、允许写入和清理路径；只操作该次创建对象，不 force/delete 他人 ref。第 3 片前的 API 预检与 B4 完整 smoke 均须取得各自范围的真实外部写入授权；本次计划和第 1/2 片无生产凭据前置。
- PR ready/donor 自动 close 的非 CAS 竞态、精确检查是否为合并必需条件、人工更新后如何阻止误验收，须形成可测试 rollout 策略；默认人工确认保留。不得宣称“校验成功→关闭所有 donor”为跨 API 原子事务。

**本次计划自审**：接口名/新旧 schema 边界、全部四片路径、focused/最终命令、K/S 身份、unknown 恢复、部分 donor、平台停止点与相对链接已检查。规划阶段仅更新本卡并检查文档；未执行产品测试或实现产品代码。设计文档提交/PR 不代表产品实现或远端事务已获验收。主审已审定本卡，首片已合并，第二片沿用 fork Draft PR 方案审阅流程；第 3 片必须先通过有界 API 预检，未获准预检不阻止第 1/2 片交付。

### B 可提议的范围（须由计划细化后批准）

| 可以提议改动 | 不在范围 |
|---|---|
| shared-docs 的 core/adapters/commands、CLI 注册、测试和 fixture 构建器的删除支持 | 手改 requirements.json、真实 page.yaml/lock、既有 golden 输出 |
| 专用上游更新 workflow/脚本及相关校验接线、最小 GitHub adapter | Fetch/Translation 的生产调度、并发队列、发布和恢复实现 |
| pending/coverage、测试矩阵、必要 package scripts 与 operator README | Base、dev 内容、图片上传、付费翻译、站点 UI、Rust 生成器 |

core 维持纯计算；Git、网络、文件、GitHub 操作经过 adapters。新增外部调用使用最小权限。复用现有通知时要分别界定候选生成无 Cloud 凭据与通知作业权限，计划中说明，不向社区 PR 暴露 secrets。

## 接口

A 已实现的内部类型位于 zdoc 的 [`core/updates/types.ts`](https://github.com/zilliztech/zdoc/blob/68151311fafa25710b6f9c7c3a18f96cb522c0ec/packages/docs-tooling/src/shared-docs/core/updates/types.ts)。调用方通过 adapter 收集固定输入，core 只计算影响、锚点关系与采用单元，输出 JSON/Markdown。WP13 使用同一份固定输入重算，不依赖 PR 正文或易失 artifact。

下表是 WP12 与 WP13 的交接边界；涉及 PR、快照和提升写入的部分仍待 B/WP13 实现：

| 约定 | WP12 上游更新 | WP13 提升 |
|---|---|---|
| 身份 | 用组 + 页面 ID 标识 Guides 更新单元；依赖页可组成同一个 PR | 输入组内页面集合，输出一次提升 PR |
| 基线 | 固定 master SHA、来源仓库/分支及 commit、旧 current/next、表格快照身份 | 固定 master SHA、待提升页面 current/next、通道变换和快照身份 |
| 变化报告 | 源及依赖变化、Cloud 输出变化、被覆盖的源变化、标题/锚点变化与引用位置、生成失败 | 消费或重新计算相同的锚点变化信息；不能只依赖 PR 正文或易失 artifact |
| 不变性 | Guides 只推进 next；生成候选无生产写入 | current 跟随 next；清理通道规则，保留手写 NextChannel，由报告提示人工处理 |
| 幂等 | 相同输入不提交重复变更；同页已有 PR 则更新；依赖页合并不能制造重叠 PR | 无有效变化不创建空 PR；明确报告不存在或无需提升的输入 |
| 并发 | 推送前核对远端 base/head；保护审核人修改；不 force-push | 同样核对远端；提升合并后 WP12 按新基线更新仍打开的 PR |
| 安全停止 | 网络/权限/快照不可用不等于页面已删除；无法认证页面状态时不关闭 PR | 无法确定目标、基线或锚点关系时不写生产状态，也不猜测替换 |
| 发布路径 | PR 合并后由现有定时/获准手动 Fetch 与部署采用 | 同左；不新增 master push 自动 Fetch |

## 计划审阅的决定

在 [zdoc #1027](https://github.com/zilliztech/zdoc/pull/1027) 的 A 阶段实现中落实；阶段边界记录在本任务卡，验证结果见[走读](../walkthroughs/WP12-A.md#审阅与验证)。

| 问题 | 决定 |
|---|---|
| 分阶段交付 | A 只做固定输入分析和报告；B 的快照、滚动 PR 与 workflow 另审精确计划 |
| 原文与输出 | 分别报告源/依赖变化与实际 Cloud 输出变化；被替换的原文不能漏报，实际构建失败标记 unknown |
| 锚点与采用单元 | 多义或删除只报告；仅有证据的跨页采用依赖才合组，共用 fragment 本身不强制合组 |
| 提升条件 | SHA 不同，或有待清理的 channel 规则时可提升；仅手写 NextChannel 不构成自动提升。WP13 开工前统一设计 04/09 的等 SHA 旧表述 |
| PR 事务 | 保留人工编辑、普通 merge 祖先、最早 PR 作为 survivor、draft 隔离；B 仍须审竞态、响应丢失、显式校验与失败恢复，不能承诺多 PR 原子更新 |
| 快照与下线 | 不从 effective 快照或陈旧 candidate 推断删除；证据缺失、过期或冲突时保留 PR 并报告。完整 7-9 与 WP14 对接 |
| 机器人身份 | 持久化 manifest 留给 B；验证 schema、尺寸、ref/ancestry、实际 API 身份和摘要，不能只信提交作者字符串 |
| Rust | 等 R1 配置契约稳定后单独细化手册级更新；不计入本次 A 的完成范围 |

## 要覆盖的编号

| 编号 | 必须证明 |
|---|---|
| 7-1 | 每日检查及手动指定页/提交；固定输入处理一天内多次提交 |
| 7-2、7-3 | 更新只入 PR、Guides 只改 next；候选不写 dev；合并后的 UAT/Prod 视图分别正确 |
| 7-4、7-6 | 单页滚动 PR、暂缓互不阻塞；保留人工修改，避免重复 PR |
| 7-5 | 互相依赖的页同 PR；覆盖从独立 PR 转为依赖集合的情况 |
| 7-7 | 无关变化不改 lock；源被 Cloud 替换但自身变化仍进入复核报告；重复运行无新提交 |
| 7-8 | 提升后的新 current/next 被下一次运行读取，更新仍打开的 PR |
| 7-9 | 认证快照中的退役/删除停止更新并关闭相应 PR；快照缺失或读取失败不误判删除 |
| 7-10 | 社区 PR 不运行 zdoc 生产逻辑、不获取 Cloud 凭据 |
| T05 | 块改名/删除、lines 失配、源文件删除/改名均给出失败报告；旧采用版本不变 |

补充：历史改写、网络失败、PR 创建成功但响应丢失、校验触发失败、远端并发更新，都有确定的恢复或停止策略。上下文报告按设计给完整代码组/块上下文，不只报摘要不同。

## 完成的定义

- 计划与公共接口经主会话批准；实际变更不超批准范围。
- 逐项测试真实断言行为，编号覆盖通过，仅删除已经覆盖的 pending 编号。
- 跑完整 PR diff 的 selector 联集、shared-docs、workflow-policy、typecheck、diff check；必要真实回放按 zdoc README/矩阵执行。未跑、跳过、不同 checkout 的结果明确注明。
- 固定源和候选生成证明旧页面不受无关变更影响；验证真实 GitHub 接线的外部操作另行取得授权，不以模拟 API 冒充真实运行。
- 按实现指南格式提供 PR 草稿及精确 head SHA 的交接包；主会话独立 review 后再决定提交与发布动作。

## 不做

不手工升级生产 lock 来演示，不修改 Base，不做 WP13 提升、WP14 下线或 WP15 恢复。设计中的合并后采用仍走现行 Fetch/部署路径，不增加 master push 自动 Fetch。

## 已知的坑

- 完成 A 不等于完成 7-1～7-10/T05；只删除端到端满足的 pending 编号，本次 A 全部保留。
- 缺失 raw 变量与实际 Cloud 构建失败不是同一件事；隐藏原文失败不能中断有效页面的报告。
- 图片字节变化可能不改 Markdown；要记录实际读取来源和摘要，不能只检查源文件文本。
- 远端状态不明时停止，不通过 force-push、盲目重试或关闭 PR 来消除不确定性。
