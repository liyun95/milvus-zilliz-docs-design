# ZH-WP5 定时调度工作流、按页滚动 PR 与飞书日报卡片

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 2（工作流与门禁 · 完成后可启动 3+1 只读试点）　**依赖**：[ZH-WP2](./ZH-WP2-incremental-draft-cli.md)（[#1516](https://github.com/zilliztech/zdoc/pull/1516)）、[ZH-WP4](./ZH-WP4-pr-validation-workflow.md)（[#1517](https://github.com/zilliztech/zdoc/pull/1517)）　**状态**：待启动（第三批）

## 目标

新增独立的中文 Guides 翻译调度工作流（`.github/workflows/translate-zh-guides.yml`）与配套编排脚本（`pnpm docs-tooling localized-docs schedule`）：工作日北京时间 `08:00`（`0 0 * * 1-5` UTC）定时扫描与手动按页触发，调用 `ZH-WP2` 起草引擎维护按页滚动 PR（`translate/zh-guides-<page-id>`），落实 `deferred` 短期暂缓与 `paused` 长期挂起规则，并复用 `pnpm docs-tooling report-card` 推送一张每日飞书群汇总卡片（分区列出当日新开/更新 PR 与 `manual` 英文变更去重提醒）。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §2.3、§3.4、§5.1–5.2](../../design/11-zh-cn-translation-pipeline.md#5-滚动-pr两档暂缓异常并发与-pr-模板) | 08:00 调度窗口、滚动 PR、两档暂缓、异常并发矩阵、`manual` 按 SHA 去重提醒 |
| 现有飞书卡片能力 | `zdoc:packages/docs-tooling/src/reporting/lark.ts`（`executeReportCard`） | 复用 `pnpm docs-tooling report-card create|note|finish` 及 `FEISHU_NOTIFICATIONS_DISABLED` 开关 |
| 现有定时巡检工作流参考 | `zdoc:.github/workflows/external-link-watchdog.yml`、`shared-docs-manual-update.yml` | 复刻安全权限、飞书卡片 kill switch 与 GitHub Actions 写法 |
| 现有工作流策略守卫 | `zdoc:scripts/validate-workflow-policy.js`（含 `localized-docs-validate` 与 `report-card` 校验） | 为 `translate-zh-guides.yml` 补全策略守卫与变异测试 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/localized-docs/core/schedule.ts`（新增，纯计算：扫描规划、按页面/输入摘要去重、`deferred` 新变化判定、滚动分支命名与日报卡片 Markdown 渲染） | `.github/workflows/fetch-docs.yml`、`translate-codex.yml`、`publish-translation.yml`、`shared-docs-*.yml` |
| `packages/docs-tooling/src/localized-docs/adapters/github-pr.ts`（新增：最小 GitHub PR 查询/创建/更新适配器，支持注入 fake 用于离线测试） | `packages/docs-tooling/src/lark/**`、`packages/docs-tooling/src/shared-docs/**` |
| `packages/docs-tooling/src/localized-docs/commands/schedule.ts`（新增） | `devOwnedPaths`（绝不向 `dev` 或 `master` 直接 push；只写受控候选分支 `translate/zh-guides-<page-id>`） |
| `packages/docs-tooling/src/localized-docs/testing/{schedule,schedule-cmd}.test.ts`（新增） | |
| `packages/docs-tooling/src/cli-main.ts`（注册 `localized-docs schedule` 子命令） | |
| `.github/workflows/translate-zh-guides.yml`（新增） | |
| `scripts/validate-workflow-policy.js`、`scripts/validate-workflow-policy.test.js` | |
| `scripts/docs-workflow/test-matrix.json` 与 `.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md` | |

## 接口与行为约定

1. **调度决策与去重（`core/schedule.ts`）**：
   - 扫描 `localized-docs/zh-CN/guides/pages/*/page.yaml`（支持 `--page <page-id>` 单页过滤与 `--dry-run` 只读模式）：
     - 每页最多一个活动翻译 PR，固定分支名 `translate/zh-guides-<page-id>`；
     - 已存在活动 PR 且带 `deferred` 标签：若新英文摘要与 PR 当前目标英文一致则**静默跳过不催办**；若有新实质英文变化则追加更新并在摘要单列“自暂缓后新变化”与“自上次合入累计变化”，通知一次；
     - 活动 PR 上检测到人工提交与新英文变化重叠冲突 → 暂停自动写入，记录 `conflict-paused` 并写入日报提醒；
     - `mode: manual` 且 `notify_on_en_change: true`：仅当 `newEnSha !== baseline.en_baseline.file_sha256` 且 `newEnSha !== baseline.last_notified_en_sha` 时纳入飞书日报卡片的「手工维护页英文变更」分区（附英文 GitHub diff 链接 + `master` 中文 `source.md` 链接），并在发送成功后记录去重状态（无变化或已提醒过不重复刷屏）；
     - `mode: paused`：静默跳过；
     - 异常阻塞（`baseline-missing-error` 或来源凭据无法核验）：不开错误 PR，归入日报卡片「阻塞待办」分区。
2. **飞书每日汇总卡片（`renderDailyDigestCardNote`）**：
   - 当日全部扫描结果合并为**一张**飞书卡片（通过 `pnpm docs-tooling report-card create|note|finish` 发送），按 4 个清晰分区汇总：① 新开/更新的中文翻译 PR；② `deferred` 页新增变化 / 到期提醒；③ `manual` 模式英文变更（带英文 diff 链接与 `source.md` 路径）；④ 阻塞待办。
   - 若当日 4 个分区均为空且非强制发送（`--always-notify` 未开启），跳过发卡片零打扰。
3. **GitHub Actions 工作流（`.github/workflows/translate-zh-guides.yml`）**：
   - 触发：`schedule`（`cron: '0 0 * * 1-5'`，即工作日北京时间 08:00）+ `workflow_dispatch`（输入：`page` 选填、`dry_run` boolean 默认 `true` 安全起步、`provider` 选填）。
   - 安全与锁隔离铁律：
     - 独立并发组 `translate-zh-guides`（`cancel-in-progress: false`），**严禁持有 `docs-production-dev` 锁**；
     - 权限最小化：仅需 `contents: write`（限定推送 `translate/zh-guides-*` 分支，**机器人无合并或绕过 `master` 分支保护权限**）与 `pull-requests: write`；
     - 飞书卡片步骤严格遵守仓库策略守卫：仅 best-effort 卡片步骤可接触飞书密钥，且必须尊重 `FEISHU_NOTIFICATIONS_DISABLED` kill switch；
     - 当仓根 `localized-docs/zh-CN/guides/pages/` 尚不存在或为空时正常空跑成功退出（不报红灯）。

## 完成的定义

- [ ] `core-boundary.test.ts` 覆盖 `core/schedule.ts`（纯计算无外部依赖）。
- [ ] `schedule.test.ts` 与 `schedule-cmd.test.ts`（使用 fake GitHub PR adapter + fake LLM）覆盖：
  - 正常增量页开 PR / 已有 PR 追加更新；
  - `deferred` 标签静默不催办 & 新英文变化时单列两档差异并通知一次；
  - 人工编辑与新英文冲突时暂停自动写入不静默覆盖；
  - `manual` 模式合批进入日报卡片、`last_notified_en_sha` 去重防刷屏；
  - `paused` 跳过与 `baseline-missing-error` 阻塞待办（不开错误 PR）；
  - 当日全空时跳过发飞书卡片；`--dry-run` 零写仓/零开 PR。
- [ ] `scripts/validate-workflow-policy.test.js` 新增 `translate-zh-guides.yml` 策略守卫与变异测试（拦截误用 `docs-production-dev` 锁、拦截缺失 `FEISHU_NOTIFICATIONS_DISABLED` 检查、拦截直接 push `master`/`dev`、拦截未声明权限）。
- [ ] 运行并全绿：
  - `pnpm exec vitest run packages/docs-tooling/src/localized-docs --pool=forks --isolate --maxWorkers=1`
  - `pnpm test:for-change -- --base origin/master --head HEAD`（0 未映射路径，且跑完返回的所有命令）
  - `pnpm test:workflow-policy`、`pnpm test:workflow-matrix`、`pnpm test:typescript-runtime-boundary`、`pnpm typecheck`、`git diff --check`。

## 不做

- 不在本 PR 中配置真实付费模型密钥或启用自动合并。
- 不修改现有英文 `shared-docs` 或日文/Reference 翻译调度工作流。

## 已知的坑

- **用 `GITHUB_TOKEN` 开 PR 不触发其他 `pull_request` 工作流的 GitHub 机制**：GitHub Actions 默认用 `GITHUB_TOKEN` 推分支/开 PR 不会触发 `localized-docs-validate.yml`（[11 §1](../../design/11-zh-cn-translation-pipeline.md#1-生产准入) 已指明）。工作流中须预留受限 GitHub App token 或在开/更新 PR 后显式 `workflow_dispatch` 派发 `localized-docs-validate.yml`（传不可变 `pr_number`/`source_sha`/`base_sha`），并在策略测试中验证。
- **`report-card` 密钥隔离策略**：`scripts/validate-workflow-policy.js` 严格检查所有调用 `report-card` 的步骤必须独立于业务步骤且检查 `FEISHU_NOTIFICATIONS_DISABLED`，实现时直接对齐 `external-link-watchdog.yml` 写法。
