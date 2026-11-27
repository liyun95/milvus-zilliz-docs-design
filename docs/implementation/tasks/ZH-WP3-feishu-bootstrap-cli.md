# ZH-WP3 飞书存量底稿一次性建仓导入 CLI

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 1（离线核心引擎）　**依赖**：[ZH-WP1](./ZH-WP1-localized-docs-core.md)（[#1507](https://github.com/zilliztech/zdoc/pull/1507)）、[ZH-WP2](./ZH-WP2-incremental-draft-cli.md)（[#1516](https://github.com/zilliztech/zdoc/pull/1516)）　**状态**：待启动（第三批，可与 ZH-WP6a 并行）

## 目标

为约 89 篇已有飞书中文旧稿的存量共享页提供一次性建仓导入 CLI（`pnpm docs-tooling localized-docs bootstrap`）：从固定 `dev` 提交中已发布的中文产物（或导出的飞书 Markdown）剥离机器生成的发布态壳子（导航 front matter、顶部 `import`）生成干净的 pre-`md2md` 源稿 `source.md`，对照最新已验证 `dev` 英文构建初始 `page.yaml` 与 `.baseline.json`（可选调用 `ZH-WP2` 辅助标出/起草历史欠译），产出可直接提导入 PR 的候选目录与核对报告——**绝不触碰飞书多维表格、不自动切源、不写入 `dev`**。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §2.3、§6.1](../../design/11-zh-cn-translation-pipeline.md#61-存量页逐页切流) | 首次飞书取底稿、导入 PR 核对项与建仓不发布边界 |
| `ZH-WP1` 剥壳与组装接口 | `zdoc:packages/docs-tooling/src/localized-docs/core/{strip-en,config,baseline,assemble}.ts` | 复用剥壳规则、Schema 校验与 `md2md` + MDX 离线预检 |
| `ZH-WP2` 分段与起草引擎 | `zdoc:packages/docs-tooling/src/localized-docs/core/{sections,diff,draft}.ts` | 复用章节对齐与可选历史欠译辅助起草 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/localized-docs/core/bootstrap.ts`（新增，纯计算：中文旧稿剥壳、初始 `page.yaml`/`.baseline.json` 构造、历史欠译与锚点核对清单） | `packages/docs-tooling/src/lark/**`（不在线改写飞书文档或 Base 表格） |
| `packages/docs-tooling/src/localized-docs/commands/bootstrap.ts`（新增） | `packages/docs-tooling/src/shared-docs/**` |
| `packages/docs-tooling/src/localized-docs/testing/bootstrap.test.ts`（新增） | `.github/workflows/**`、`devOwnedPaths` |
| `packages/docs-tooling/src/cli-main.ts`（注册 `localized-docs bootstrap` 子命令） | 仓库根目录 `localized-docs/`（不在本 PR 提交真实业务页面） |
| `scripts/docs-workflow/test-matrix.json` 与 `.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md` | |

## 接口与行为约定

1. **输入来源（离线确定性输入，零隐式网络拉取）**：
   - `--page <page-id>`（必填，合法小写连字符 slug）
   - `--shared-page <en-shared-page>`（默认同 `--page`）
   - `--en-file <path>` 与 `--en-manifest <path>`（或 `--en-dev-commit <sha>`）：最新已验证 `dev` 英文正文与来源凭据
   - `--zh-legacy-file <path>`：固定 `dev` 提交上的旧中文产物（例如 `dev:content/zh-CN/guides/...`）或飞书导出的中文 Markdown
   - `--mode <incremental|manual>`（默认 `incremental`）、`--sync-policy <independent|bilingual_sync>`（默认 `independent`）
   - `--align-gap`（可选开关：启用时把旧中文与最新英文按节比对，标出中文缺失小节/疑似过时段落，或经 `ZH-WP2` 受限起草辅助生成候选补齐稿与 `ReviewTodo`；默认只做剥壳建仓与差异报告，不调用 LLM）
   - `--out <dir>`（空/不存在目录，写入 `pages/<page-id>/{page.yaml, source.md, .baseline.json}` 与 `bootstrap-report.md`）
2. **旧中文剥壳与规范化（`core/bootstrap.ts`）**：
   - 剥离旧飞书/发布态产出的机器 front matter（`slug`、`sidebar_label`、`sidebar_position`、`token`、`custom_edit_url`、`type`、`displayed_sidebar`、`beta`、`added_since`、`last_modified`、`deprecate_since`、`notebook`）与顶部 Docusaurus 组件 `import` 行；
   - 保留干净正文、`title`/`description`、已有 `<NextChannel>`、`<UI>` 与代码块（含中国站定制代码块，并自动检测每个代码块与英文的字节差异，初始化 `customized_for_zh: true | false`）；
   - 生成的 `page.yaml` **绝不写入 `owner` 或 `feishu_record_id`**；
   - 自动对产出的 `source.md` 运行 `validateSourceShell`、`validateChannelTags`、`validateUiTags`（并在 `--variables-file` 存在时跑 `assembleLocalizedPage` 预检），确保产出的建仓目录可直接通过 `localized-docs check`。
3. **导入 PR 核对清单（`bootstrap-report.md`）**：
   - 列出：旧中文与最新英文的标题/小节锚点对照、自动识别为 `customized_for_zh: true` 的代码块数量、正文内残留飞书图片/站内旧链接清单、以及 `<!-- localized-docs:review-todos:start/end -->` 核对勾选框（主审必须确认“已核对历史欠译与最近一次飞书修订”才能过 `ZH-WP4` 门禁）。

## 完成的定义

- [ ] `core-boundary.test.ts` 覆盖 `core/bootstrap.ts`，确认零 `lark/`、fs、网络依赖。
- [ ] `bootstrap.test.ts` 覆盖：
  - 剥离真实形态旧中文 `dev` MDX（含 front matter + `import Tabs/Admonition`）后产出可通过 `localized-docs check` 的 `page.yaml` + `source.md` + `.baseline.json`；
  - 自动识别与英文不同的中国站定制代码块并置 `customized_for_zh: true`；
  - 拒绝覆盖已有非空目标目录或符号链接，拒绝写入 `owner` / `feishu_record_id`；
  - `--align-gap` 模式（使用 fake LLM）检测缺失小节并产出带 `review-todos` 区块的 `bootstrap-report.md`；
  - `cli-main.ts` 端到端集成测试跑通 `pnpm docs-tooling localized-docs bootstrap`。
- [ ] 运行并全绿：
  - `pnpm exec vitest run packages/docs-tooling/src/localized-docs --pool=forks --isolate --maxWorkers=1`
  - `pnpm test:for-change -- --base origin/master --head HEAD`（0 未映射路径，且跑完返回的所有命令）
  - `pnpm test:typescript-runtime-boundary`、`pnpm typecheck`、`pnpm test:workflow-matrix`、`pnpm test:workflow-policy`、`git diff --check`。

## 不做

- 不在线修改飞书多维表格的 `Docs` 链接（切链操作由文档负责人在导入 PR 合并后人工执行，由 `ZH-WP6b` 承接）。
- 不批量自动把全部 89 篇一次性提交进 `master`（生产建仓分 6–8 批逐批审校合入）。

## 已知的坑

- **旧中文标题锚点差异**：旧飞书中文标题往往自动生成拼音/英文锚点或缺失显式 `{#anchor}`；`bootstrap.ts` 应在 `bootstrap-report.md` 明确列出与英文锚点不一致的标题供主审核对，不要静默重写历史旧锚点以免破坏外部深链。
- **保留原有中国站代码块定制**：建仓阶段一旦检测到中文代码块与英文不同（且不命中 Tier-2 固定域名映射），必须标为 `customized_for_zh: true`，避免后续第一次日常增量把历史定制代码覆盖掉。
