# ZH-WP4 中文候选 PR 检查工作流、待办清零门禁与 CODEOWNERS

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 2（工作流与门禁）　**依赖**：[ZH-WP1](./ZH-WP1-localized-docs-core.md)（[#1507](https://github.com/zilliztech/zdoc/pull/1507)）　**状态**：待启动（第二批，可与 ZH-WP2、ZH-WP6a 并行）

## 目标

为 `master:localized-docs/zh-CN/guides/**` 建立受信任的只读 PR 候选检查工作流（`.github/workflows/localized-docs-validate.yml`）与配套 CLI（`pnpm docs-tooling localized-docs pr-check`），补齐 `site-validation.yml`（`skip_content=true`）与 `shared-docs-validate.yml` 对中文候选稿的覆盖空白：校验 `md2md` 预处理、双通道（CURRENT / NEXT）实际视图投影与哨兵隔离、MDX 语法、待确认项清零门禁与候选预览产物，并配置文档团队 `CODEOWNERS` 与工作流策略守卫。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §1、§2.3、§4.1、§5.3](../../design/11-zh-cn-translation-pipeline.md#1-生产准入) | 生产准入四项底线、双通道视图核验、待办清零门禁、不持生产锁契约 |
| 现有共享页 PR 校验工作流 | `zdoc:.github/workflows/shared-docs-validate.yml` | 复刻不可变 PR SHA 校验、只读权限、并发组与安全边界写法 |
| 现有工作流策略守卫 | `zdoc:scripts/validate-workflow-policy.js` 与 `scripts/validate-workflow-policy.test.js` | 为新工作流加策略防回归测试，确保不触碰生产锁与写权限 |
| 双通道当前视图投影 | `zdoc:apps/docs/plugins/next-channel-view.js` 与 `packages/docs-tooling/src/shared-docs/testing/merge/demo.ts` | 复用 CURRENT / NEXT 视图投影语义验证双通道渲染隔离 |
| `ZH-WP1` 已落地命令 | `zdoc:packages/docs-tooling/src/localized-docs/commands/{check,build}.ts` | 直接复用离线 `check` 与 `build` 能力 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/localized-docs/core/review-gate.ts`（新增：PR 待办清零机检 + CURRENT/NEXT 视图投影与哨兵校验，纯计算） | `packages/docs-tooling/src/localized-docs/core/{config,baseline,strip-en,ui-tags,assemble}.ts`（只读复用） |
| `packages/docs-tooling/src/localized-docs/commands/pr-check.ts`（新增） | `.github/workflows/fetch-docs.yml`、`translate-codex.yml`、`publish-translation.yml`、`shared-docs-*.yml` |
| `packages/docs-tooling/src/localized-docs/testing/{review-gate,pr-check}.test.ts`（新增） | `packages/docs-tooling/src/lark/**`、`packages/docs-tooling/src/shared-docs/**` |
| `packages/docs-tooling/src/cli-main.ts`（注册 `localized-docs pr-check` 子命令） | `devOwnedPaths` |
| `.github/workflows/localized-docs-validate.yml`（新增） | |
| `.github/CODEOWNERS`（新增或补充 `localized-docs/zh-CN/guides/` 团队归属条目；如仓库已有 `.github/CODEOWNERS` 则只增量追加，不改现有条目） | |
| `scripts/validate-workflow-policy.js`、`scripts/validate-workflow-policy.test.js` | |
| `scripts/docs-workflow/test-matrix.json` 与 `.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md` | |

## 接口与行为约定

1. **待确认项清零机检（`core/review-gate.ts`）**：
   - 解析 PR Description（或本地传入的 `--pr-body-file`）中受控区块（例如 `<!-- localized-docs:review-todos:start -->` … `<!-- localized-docs:review-todos:end -->`）内的 Markdown 任务列表项：
     - 存在任意未勾选 `- [ ]` → 返回失败（错误码 `REVIEW_TODOS_UNRESOLVED`），列出未清零条目；
     - 全部为 `- [x]` 或 `- [X]` 或区块无待办 → 通过；
     - 区块起止标记缺失/被破坏（仅当标记了需待办校验标志或出现半截标记时）→ 报错拦截，防止误删待办区绕过检查。
2. **双通道 CURRENT / NEXT 视图投影校验（`core/review-gate.ts`）**：
   - 接收 `assembleLocalizedPage` 编译出的最终 MDX，分别生成 CURRENT 视图（保留 `exclude`、剔除 `include`）与 NEXT 视图（保留 `include`、剔除 `exclude`）；
   - 校验两份视图中均无残留 `<NextChannel` 标签、均合法、标题/锚点无重复冲突，并产出可读的两通道预览文件（供工作流打包为只读 artifact 供主审下载/查看）。
3. **CLI 子命令（`commands/pr-check.ts`）**：
   - `pnpm docs-tooling localized-docs pr-check --root <dir> [--page <page-id>...] [--pr-body-file <file>] [--preview-out <dir>]`
   - 串联：① `runCheck`（`Variables.json`、`page.yaml`、`source.md`、`.baseline.json`、`<UI>`、通道、`md2md` + MDX 编译）；② 双通道视图投影与预览输出；③ 待办清零机检（传入 `--pr-body-file` 时执行）。
   - 当变更的 PR 中尚未存在 `localized-docs/zh-CN/guides/` 目录或无受影响中文页面时，显式以 `0` 退出并打印清晰说明（避免阻断无关 PR）。
4. **GitHub Actions 工作流（`.github/workflows/localized-docs-validate.yml`）**：
   - 触发：`pull_request`（`branches: [master]`，`paths: ['localized-docs/zh-CN/guides/**', 'config/translation/zh-CN-common.json', 'config/translation/zh-CN-guides.json']`，`types: [opened, synchronize, reopened, ready_for_review, edited]`——含 `edited` 确保主审勾选 PR body 待办框后自动重跑门禁！）+ `workflow_dispatch`（接受 `pr_number`、`source_sha`、`base_sha`，与 `shared-docs-validate.yml` 对齐）。
   - 安全与隔离铁律：
     - `permissions: { contents: read }`（绝不申请 `contents: write`、绝不触碰生产 secrets）；
     - 独立并发组 `localized-docs-validate-${{ github.event.pull_request.number || inputs.pr_number }}-${{ github.event_name }}`，**绝不持有 `docs-production-dev` 锁**；
     - 校验不可变 PR head SHA，产出只读双通道预览 artifact（`retention-days: 14`）。
5. **工作流策略守卫（`scripts/validate-workflow-policy.js`）**：
   - 新增针对 `.github/workflows/localized-docs-validate.yml` 的策略断言与变异测试：验证只读权限、不可变 SHA、未持有 `docs-production-dev`、触发路径与 `edited` 事件、以及调用 `pnpm docs-tooling localized-docs pr-check`。

## 完成的定义

- [ ] `review-gate.test.ts` 与 `pr-check.test.ts` 覆盖：
  - 未勾选 `- [ ]` 拦截、全部 `- [x]` 放行、半截标记被拦截；
  - 故意置入的 NEXT 哨兵在 CURRENT 视图中缺失、在 NEXT 视图中准确出现，且两视图均无残留 `<NextChannel>`；
  - 结合 `ZH-WP1` 合成 fixture 跑通 `localized-docs pr-check` 输出双通道预览与报告。
- [ ] `scripts/validate-workflow-policy.test.js` 新增变异测试全绿（破坏权限、触发、锁边界或命令均被策略守卫拦住）。
- [ ] `.github/CODEOWNERS` 已登记 `/localized-docs/zh-CN/guides/ @zilliztech/docs-team`（若仓库暂用其他团队 slug，先核对仓库现有 `.github/CODEOWNERS` 或在注释标明待在 GitHub 组织确认团队 slug）。
- [ ] 运行并全绿：
  - `pnpm exec vitest run packages/docs-tooling/src/localized-docs --pool=forks --isolate --maxWorkers=1`
  - `pnpm test:for-change -- --base origin/master --head HEAD`（0 未映射路径，且跑完返回的所有命令）
  - `pnpm test:workflow-policy`、`pnpm test:workflow-matrix`、`pnpm test:typescript-runtime-boundary`、`pnpm typecheck`、`git diff --check`。

## 不做

- 不实现 08:00 定时扫描与自动开 PR（归属 `ZH-WP5`）。
- 不修改 GitHub 仓库线上 Branch Protection 设置（该项由仓库管理员在 PR 合并后配置，并在 PR 说明里给出明确操作清单）。

## 已知的坑

- **务必包含 `pull_request.types: [..., edited]`**：因为主审通过勾选 PR Description 里的 `- [ ]` 来清零待办，如果不监听 `edited`，勾选后必需检查不会重跑，PR 会卡死在红灯。
- **不要改动 `shared-docs-validate.yml` 现有断言**：只为 `localized-docs-validate.yml` 新增独立策略块，防止误伤已有 120 条工作流策略测试。
- **注意 `cli-main.ts` 并发合并**：本包与 `ZH-WP2` 都会在 `cli-main.ts` 的 `localized-docs` 子命令分发处各加 1 行分支，保持极简独立函数调用，合并零摩擦。
