# ZH-WP2 增量 Diff、三档代码保护与受限起草 CLI

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 1（离线核心引擎）　**依赖**：[ZH-WP0b](./ZH-WP0b-zh-cn-common-glossary.md)（[#1502](https://github.com/zilliztech/zdoc/pull/1502)）、[ZH-WP1](./ZH-WP1-localized-docs-core.md)（[#1507](https://github.com/zilliztech/zdoc/pull/1507)）　**状态**：待启动（第二批，可与 ZH-WP4、ZH-WP6a 并行）

## 目标

基于 `ZH-WP1` 的 `localized-docs` 核心与 `ZH-WP0b` 的 `zh-CN-guides` 术语契约，实现中文 Guides 的确定性增量起草引擎与离线 CLI（`pnpm docs-tooling localized-docs draft`）：完成三方输入核验、按节确定性 diff、代码块三档保护、`<UI>` 词隔离、未改段落逐字复核、受限 LLM 提案拼接、新页首译 vs 基线缺失阻塞分流，以及结构化 PR 说明生成。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §3、§4.1、§5.2–5.3](../../design/11-zh-cn-translation-pipeline.md#3-英文基线增量起草代码块与术语规则) | 三方输入核验、确定性门禁、代码块三档、疑点保留、PR 结构模板 |
| `ZH-WP1` 已落地接口 | `zdoc:packages/docs-tooling/src/localized-docs/core/{types,config,baseline,strip-en,ui-tags,assemble}.ts` | 复用 `stripEnShell`、`scanUiTags`、`validateUiTags`、`resolvePageLifecycleState`、`assembleLocalizedPage` |
| `ZH-WP0b` 术语加载器 | `zdoc:scripts/translation/localeContract.js` 与 `config/translation/zh-CN-guides.json` | 复用 `loadLocaleContract('zh-CN-guides')` 与 `validateLocaleContractDraft` |
| 现有分段与保护参考 | `zdoc:scripts/translation/protectedContent.js`、`scripts/translation/surgicalUpdate.js` | 参考受保护字节、代码块与语义分段实践 |
| 中文通则风格指南 | `zdoc:.github/prompts/codex-style-guide.zh-CN-reference.md`（第 0–1 章） | 提取通则作为受限 LLM 系统上下文 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/localized-docs/core/{sections,diff,code-sync,draft,pr-body}.ts`（新增，保持纯计算零 `lark/`/fs/网络依赖） | `packages/docs-tooling/src/localized-docs/core/{config,baseline,strip-en,ui-tags,assemble}.ts`（只读复用，避免与并发包冲突） |
| `packages/docs-tooling/src/localized-docs/adapters/{en-reader,llm,contract}.ts`（新增） | `packages/docs-tooling/src/lark/**`、`packages/docs-tooling/src/shared-docs/**` |
| `packages/docs-tooling/src/localized-docs/commands/draft.ts`（新增） | `scripts/translation/**`（只读调用 `localeContract.js`，不改旧翻译脚本） |
| `packages/docs-tooling/src/localized-docs/testing/{diff,code-sync,draft,pr-body}.test.ts`（新增） | `.github/workflows/**`（工作流归属 `ZH-WP4` / `ZH-WP5`） |
| `packages/docs-tooling/src/cli-main.ts`（注册 `localized-docs draft` 子命令） | `devOwnedPaths` |
| `scripts/docs-workflow/test-matrix.json` 与 `.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md`（如有新增未映射路径） | |

## 接口与行为约定

1. **输入身份与状态分流（`core/draft.ts`）**：
   - 输入三方材料：`baseEn`（按 `.baseline.json` 取回的上次已审英文，新页首译时为 `null`）、`newEn`（本次已验证 `dev` 英文及其来源凭据摘要）、`curZh`（当前 `master` `source.md` 与 `.baseline.json`）。均先经 `stripEnShell` 剥离导航壳子与 `import`。
   - 状态分流：
     - `mode === 'paused'` → 返回 `{ status: 'skipped', reason: 'paused' }`；
     - `mode === 'manual'` → 不起草译文；检测 `newEn.fileSha256 !== baseline.en_baseline.file_sha256` 且 `!== baseline.last_notified_en_sha` 时返回 `{ status: 'manual-notify', enDiffSummary, newEnSha }`，否则 `{ status: 'skipped', reason: 'manual-already-notified' | 'unchanged' }`；
     - `pending-initial-translation`（`incremental` 且无 `source.md` / `.baseline.json`）→ 进入合法首译流程，生成完整 `source.md` 与首份 `.baseline.json`；
     - `baseline-missing-error`（有 `source.md` 缺 `.baseline.json`、或英文凭据/摘要校验失败、或 `curZh` 摘要与 `.baseline.json` 异常冲突且无法判定合法手改）→ **整页阻塞**，返回 `{ status: 'blocked', reason, diagnostics }`，**绝不误当新页首译**；
     - 无实质英文变化 → `{ status: 'skipped', reason: 'unchanged' }`。
2. **确定性分段与 3-way Diff（`core/sections.ts`、`core/diff.ts`）**：
   - 按标题锚点（`## ...{#anchor}`）+ 块级结构（段落、列表、表格、提示框、代码组、`<NextChannel>` 块）拆分 `baseEn`、`newEn`、`curZh`，计算每个 section 及代码块的 SHA-256。
   - 精确区分：`unchanged`（未变，**强锁逐字不动**）、`modified`（唯一结构对应且局部变更，送受限 LLM 起草）、`added` / `removed`、`ambiguous`（拆并段、标题改名、多候选匹配或夹层中文独有段受影响 → **保留原中文一字不改**，生成结构化 `ReviewTodo` 交主审决定）。
   - 严格保护通道边界：程序计算/保留 `<NextChannel action="include|exclude">`，**禁止模型生成或修改通道标签**；若模型提案越界修改了未涉及段落或篡改通道标签，门禁直接拒绝并回退/冻结。
3. **代码块三档保护（`core/code-sync.ts`）**：
   - **绝不把 fenced 代码块交给 LLM 翻译**（英文注释保持英文）：
     - **档位 1（`customized_for_zh: false`）**：`curZh` 代码块与 `baseEn` 字节一致 → 程序直接原样同步 `newEn` 代码块；
     - **档位 2（确定性映射规则）**：命中显式声明的域名/地域确定性替换规则（如 `cloud.zilliz.com` → `cloud.zilliz.com.cn`）→ 程序确定性换算并在变更摘要中显式标注；
     - **档位 3（`customized_for_zh: true`）**：`curZh` 代码块与 `baseEn` 原本就不同且 `newEn` 再次变化 → **不覆写中文代码**，暂停自动同步该块并生成带英文 diff 与中文定制代码的 `ReviewTodo`。
4. **`<UI>` 词隔离与术语约束**：
   - 调用 `ZH-WP1` 的 `scanUiTags` 提取所有 `<UI>...</UI>` 节点，在送交 LLM 前替换为不可变占位符，拼接回稿后恢复英文原词并自动生成“核对中文控制台文案”的 `ReviewTodo`；
   - 通过 `adapters/contract.ts` 加载 `loadLocaleContract('zh-CN-guides')` 并校验译文草稿，将术语告警附入 PR 摘要。
5. **受限 LLM 适配器（`adapters/llm.ts`）与离线 CLI（`commands/draft.ts`）**：
   - 定义纯接口 `DraftLlmProvider`（输入：仅限变更段落 + 邻接中文上下文 + `zh-CN-guides` 术语契约 + 通则风格指南；输出：按块 ID 索引的局部译文提案；无文件写权限）；
   - 提供离线测试用 `FakeDraftLlmProvider` 与预留可插拔真实模型 Provider（可通过环境变量/CLI 参数注入，单元测试严禁访问外网）；
   - CLI：`pnpm docs-tooling localized-docs draft --root <dir> --en-new <file> [--en-base <file>] --page <page-id> --out <dir> [--provider fake|...]`，输出候选 `source.md`、更新后的 `.baseline.json`、结构化报告 `draft-report.json` 及符合[技术设计 §5.3](../../design/11-zh-cn-translation-pipeline.md#53-参考示例一份翻译-pr-的实际结构)的 `pr-body.md`。

## 完成的定义

- [ ] `core-boundary.test.ts` 扩展覆盖新增 `core/*.ts`，确认 `localized-docs/core/` 仍零 `lark/`、fs、网络依赖。
- [ ] Vitest 单元测试全面覆盖：
  - 增量模式未涉及段落**逐字节不变**校验（含刻意构造模型越界改稿时门禁拦截）；
  - 代码块三档保护（原样同步、固定域名换算、定制代码冲突暂停并生成 `ReviewTodo`）；
  - `<UI>Create Cluster</UI>` 占位隔离、原词保留与待办提取；
  - 拆并段夹层中文独有提示（如《删除 Entity》场景）保留原中文一字不改并生成 `ReviewTodo`；
  - 新页首译（`pending-initial-translation`）与基线缺失阻塞（`baseline-missing-error`）严格区分；
  - `manual` 模式产出 `manual-notify`（含 `last_notified_en_sha` 去重）且不起草译文；`paused` 模式跳过；
  - 模型尝试编造/翻转 `<NextChannel>` 边界时被门禁拦截；
  - `cli-main.ts` 端到端集成测试跑通 `localized-docs draft`（使用 fake provider，产出可经 `localized-docs check` 通过的候选稿与 `pr-body.md`）。
- [ ] 运行并全绿：
  - `pnpm exec vitest run packages/docs-tooling/src/localized-docs --pool=forks --isolate --maxWorkers=1`
  - `pnpm test:for-change -- --base origin/master --head HEAD`（0 未映射路径，且跑完返回的所有命令）
  - `pnpm test:typescript-runtime-boundary`、`pnpm typecheck`、`pnpm test:workflow-matrix`、`pnpm test:workflow-policy`、`git diff --check`。

## 不做

- 不编写 GitHub Actions 工作流或调用 GitHub API 开 PR（归属 `ZH-WP5`）。
- 不实现飞书底稿导入（归属 `ZH-WP3`）或 Fetch 路由（归属 `ZH-WP6a` / `ZH-WP6b`）。
- 不在单元测试中调用真实付费 LLM API。

## 已知的坑

- **只读复用 `ZH-WP1` 文件**：尽量不改动 `config.ts`/`baseline.ts`/`strip-en.ts`/`ui-tags.ts`/`assemble.ts`，确保本包与 `ZH-WP4`、`ZH-WP6a` 三路并行时零代码冲突。
- **中文手写 PR 后的 `curZh` 演进**：文档工程师直接手改 `source.md` 并合入后，`cur_zh` 与上次 `.baseline.json` 中记录的 `zh_reviewed.source_sha256` 应保持同步（由 PR 门禁维护）；若遇到 `source_sha256` 漂移但 `en_baseline` 完整，应明确区分“合法人工修订”与“基线缺失/损坏”，不可静默吞掉人工手写段落。
