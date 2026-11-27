# ZH-WP6b 中文 Fetch 入口接线、Promote 交接与真实回放验收

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 3（生产切流前提 · 需对齐涂文家新架构 Base 字段）　**依赖**：[ZH-WP6a](./ZH-WP6a-handoff-core.md)（+ 确认英文 Fetch 新架构 `page url` 解耦后的 Base 记录结构）　**状态**：待启动（最终收官包）

## 目标

将 `ZH-WP6a` 的中文路由/激活/Promote 纯核心与 `ZH-WP1` 的 `md2md` 组装引擎接入 `zdoc` 现有的中文 Guides Fetch 流水线（`produce_zh_guides_sources` / `render_zh_guides_tables` / `produce_zh_guides`），实现已切换页读固定 `master` 中文源码（`source.md` + `Variables.json` + 片段）经 `@zilliz/mdtomd` 组装写入 `dev:content/zh-CN/guides/...`、未切换页继续读飞书的混源原子发布，并建立独立回放套件 `pnpm test:replay:localized-pages` 完成真实保留产物隔离 bare remote 回放验收。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §4.2、§6、§7](../../design/11-zh-cn-translation-pipeline.md#63-fetch-接线与恢复) | 五项 Fetch 硬契约、回退保护、路径隔离与真回放验收要求 |
| `zdoc` 仓库安全与回放规范 | `zdoc:AGENTS.md`（Publication workflow safety & Replay harness selection） | 严格遵守隔离 bare remote 回放、不得修改真实 `origin`/`dev`、`test-matrix` 与 `test:replay` 合同 |
| 现有英文共享页 Fetch 接线 | `zdoc:scripts/docs-workflow/guides-shared-sources.js` 与 `packages/docs-tooling/src/lark/sharedPageRouting.js` | 参照事务级回退、凭据原子提交与失败隔离机制 |
| 现有中文 Guides Fetch 通道 | `zdoc:.github/workflows/fetch-docs.yml`（`produce_zh_guides*`）、`_fetch-guides-sources.yml`、`_assemble-guides.yml` | 确认 `site: zh-CN` 入口参数与产物交接格式 |
| 现有共享页回放套件 | `zdoc:scripts/docs-workflow/replay-shared-pages.test.js` | 复刻真实保留检查点 + 隔离 bare remote 回放测试结构 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/localized-docs/adapters/handoff/{routing,fetch-build}.ts`（新增：固定 `master` commit 读盘 + 调 `ZH-WP6a` 路由 + 调 `ZH-WP1` `assembleLocalizedPage` 生成最终 MDX 与凭据） | `packages/docs-tooling/src/shared-docs/**`（英文共享页路由与生成零改动） |
| `scripts/docs-workflow/guides-localized-sources.js` 与 `.test.js`（新增，对称于 `guides-shared-sources.js`） | `scripts/translation/**`、`translate-codex.yml`、`publish-translation.yml` |
| `packages/docs-tooling/src/lark/` 中中文路由分流接入点（仅 `site=zh-CN` 路径调用 `localized-docs` 适配器，保持 `site=en` 零行为变化） | 真实 `origin` / `dev` 分支（回放仅用本地临时 bare remote） |
| `.github/workflows/_fetch-guides-sources.yml` / `_assemble-guides.yml`（仅在 `site == 'zh-CN'` 路径传递固定 `master_sha` 与 localized 源产物） | `content/zh-CN/guides/tutorials/tools/` 与 Reference 路径归属 |
| `scripts/docs-workflow/replay-localized-pages.test.js`（新增回放套件） | |
| `package.json`（新增 `test:replay:localized-pages` 并按规范接入 `test:replay`） | |
| `scripts/validate-workflow-policy.{js,test.js}`、`scripts/docs-workflow/test-matrix.json`、`.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md`、`README.md` / `runbook/replay-harnesses.md` | |

## 接口与行为约定

1. **双源路由接入（`site=zh-CN` 专属，与 `site=en` 彻底互斥）**：
   - 在 `site=zh-CN` 源准备阶段，扫描中文 Base `canonical` 记录的 `Docs` 链接：
     - 匹配 `localized-docs/zh-CN/guides/pages/<page-id>` → 经 `ZH-WP6a` `classifyLocalizedSourceRoute` 与 `createLocalizedRoutingContext`（**以 `page_id` / `page_url` 为主键，忽略 `record_id` 变动**）进入 Git 中文源构建；
     - 匹配飞书文档链接 → 若该 `page_url` 已在 `generated/zh-CN/manifests/localized-pages/guides/active.json` 中激活则直接报 `OWNERSHIP_REVERTED` 拦截，否则沿用现行飞书抓取；
     - 误填 `shared-docs/...` → 报 `OWNERSHIP_PATH_MISMATCH` 拦截；
     - 英文 `site=en` 遇到 `localized-docs/...` → 报 `OWNERSHIP_PATH_MISMATCH` 拦截。
2. **逐页事务组装与原子提交**：
   - 仅从 Fetch 固定的 `master_sha`（绝不读脏工作区）读取 `localized-docs/zh-CN/guides/{Variables.json, fragments/, pages/<page-id>/{page.yaml, source.md, .baseline.json}}`；
   - 调用 `ZH-WP1` `assembleLocalizedPage` 经 `@zilliz/mdtomd` 展开变量/片段并注入当前中文 Base 导航 front matter（`sidebar_label`、`sidebar_position`、`slug`、`channel`）、旧飞书锚点别名与组件 `import`，校验完整 MDX 与图片；
   - 单页失败时按 `page_url` 回退保留该页上次已验证的 `dev` 产物与凭据，不影响同批兄弟页面发布；
   - 成功页在同一 `dev` 检查点提交中原子写入最终 MDX（`content/zh-CN/guides/...`）、导航、旧链接映射、`generated/zh-CN/manifests/localized-pages/guides/<page-id>.json` 与 `active.json`。
3. **缓存身份与 Promote 交接**：
   - 中文 Guides 源快照与缓存身份纳入固定 `master` 下 `source.md`/`page.yaml`/`Variables.json`/片段 SHA-256——**飞书表格记录未变、但 Git 中文源码更新时必须命中重生成**；
   - 接入 `ZH-WP6a` `promoteLocalizedSource`，在受保护 Promote PR 合入后经 Fetch 重验并发布到 Prod，任何英文 `next` 推进或通道不匹配均保留上次可用中文。
4. **真实保留产物隔离回放验收（`AGENTS.md` 硬要求）**：
   - 先用 `group=guides`、`publish=false`、`run_translations=false`、`media_upload_mode=skip` 验证只读候选；
   - 再在隔离本地 bare remote 中使用真实保留的中文 Fetch 检查点回放，完整覆盖 8 类场景：冷热缓存、飞书未变但 Git 源码已变、切流失败回退、重复激活拦截、飞书 `record_id` 变化但 `page_url` 不变、重命名/删除保护、已审 NEXT 提升，以及验证与英文/日文/`zh-CN-reference` 写入边界零交叉；
   - 保留真实回放输出根目录，在 PR 报告中写明精确命令、保留产物身份、结果计数与 `pnpm build:zh-CN`（先确认 `test -e apps/docs/node_modules/jiti`）实跑结果。

## 完成的定义

- [ ] 新增 `scripts/docs-workflow/replay-localized-pages.test.js` 并通过 `pnpm test:replay:localized-pages`；
- [ ] 回放用例显式验证：**调整飞书目录导致 `record_id` 改变但 `page_url` 不变时，已激活中文页正常发布与回退，零断链**；
- [ ] 同步更新 `test-matrix.json`、`.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md`、`replay` 契约测试与 `runbook/replay-harnesses.md`；
- [ ] 运行并全绿：
  - `pnpm test:for-change -- --base origin/master --head HEAD`（0 未映射路径，且跑完返回的全部命令）
  - `pnpm test:replay:localized-pages`、`pnpm test:replay:all`、`pnpm test:workflow-policy`、`pnpm test:workflow-matrix`、`pnpm test:typescript-runtime-boundary`、`pnpm typecheck`
  - `pnpm build:zh-CN`（验证中文站实际构建通过）
  - `git diff --check`。

## 不做

- 不开启付费 Translation 任务来补验证证据（遵循 `AGENTS.md` 第 6 条安全规则）。
- 不在本 PR 中直接切换线上生产中文飞书多维表格的 `Docs` 链接（代码合入并通过真实回放后，再按 3+1 试点页逐页切链）。

## 已知的坑

- **对齐涂文家新架构 Base 字段**：开工前先 `git fetch origin master` 核对涂文家关于 `record_id` 解耦后最新合入的 `guidesBaseRecordSemantics.js` / `sharedPageRouting.js` 接口，避免字段名漂移。
- **隔离 checkout 的中文构建依赖**：在临时 worktree 中跑 `pnpm build:zh-CN` 前，务必先检查 `test -e apps/docs/node_modules/jiti`（按 `AGENTS.md` 在当前 worktree 跑 `pnpm install --frozen-lockfile`），切勿只靠根 `node_modules` 误诊构建失败。
- **严禁重入 `docs-production-dev` 锁**：可复用工作流 `_fetch-guides-sources.yml` / `_assemble-guides.yml` 绝不可重新申请 `docs-production-dev` 并发组。
