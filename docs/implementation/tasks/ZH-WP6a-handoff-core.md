# ZH-WP6a 中文路由、激活态与 Promote 核心（解耦 `record_id`）

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 3（纯核心，可提前并行）　**依赖**：[ZH-WP1](./ZH-WP1-localized-docs-core.md)（[#1507](https://github.com/zilliztech/zdoc/pull/1507)）　**状态**：待启动（第二批，可与 ZH-WP2、ZH-WP4 并行，不阻塞于英文 Fetch 改造）

## 目标

在 `packages/docs-tooling/src/localized-docs/core/handoff/` 实现中文 Guides 独立的发布交接纯核心模块（零 `lark/`、文件系统或网络依赖）：站点互斥路由分类器、**按 `page_id` 与目标 `page_url` 绑定（彻底解耦飞书 `record_id`）**的激活状态与回退索引、独立 `dev` 凭据 schema（`generated/zh-CN/manifests/localized-pages/guides/`），以及双通道 Promote 候选解包纯计算逻辑，为 `ZH-WP6b` 接入中文 Fetch 铺平道路。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §4.2、§6.1、§6.3](../../design/11-zh-cn-translation-pipeline.md#63-fetch-接线与恢复) | 五项中文 Fetch 硬契约、`record_id` 解耦原则、独立凭据路径、Promote 解包规则 |
| 英文共享页交接参考 | `zdoc:packages/docs-tooling/src/shared-docs/core/handoff/source-state.ts` 与 `adapters/handoff/routing.ts` | 对照英文契约模型，并明确剥离其旧版 `record_id` 主键强绑定 |
| `ZH-WP1` 已落地接口 | `zdoc:packages/docs-tooling/src/localized-docs/core/{types,config,assemble}.ts` | 复用 `validatePageId`、`PAGE_ID_PATTERN`、`validateChannelTags` |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/localized-docs/core/handoff/{source-state,routing,receipt,promote}.ts`（新增，纯计算） | `packages/docs-tooling/src/lark/**`（中文 Fetch 入口接线留到 `ZH-WP6b`） |
| `packages/docs-tooling/src/localized-docs/testing/handoff/{source-state,routing,receipt,promote}.test.ts`（新增） | `packages/docs-tooling/src/shared-docs/**`（绝不改动英文共享页路由与激活契约） |
| `scripts/docs-workflow/test-matrix.json` 与 `.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md`（如有新增未映射路径） | `scripts/docs-workflow/guides-*.js`、`.github/workflows/**` |
| | `devOwnedPaths` |

## 接口与行为约定

1. **站点互斥路由分类（`core/handoff/source-state.ts`）**：
   - `classifyLocalizedSourceRoute(value, context)`:
     - 仅当 `site === 'zh-CN'` 且原始字节严格匹配 `^https://github\.com/zilliztech/zdoc/tree/master/localized-docs/zh-CN/guides/pages/([a-z0-9]+(?:-[a-z0-9]+)*)/?$`（禁止 `active` 保留名，且 `<page-id>` 存在于固定 `master` 提交的 `availablePages` 中）时，返回 `{ kind: 'localized-page', locale: 'zh-CN', group: 'guides', page, directory: 'localized-docs/zh-CN/guides/pages/<page>', url }`；
     - 遇到 `shared-docs/...` 或其他 locale 路径时明确拒绝，返回 `{ kind: 'invalid', code: 'OWNERSHIP_PATH_MISMATCH', ... }`；
     - 合法飞书文档 URL（`feishu.cn` / `larksuite.com` 的 `/wiki|doc|docs|docx/<token>`）返回 `{ kind: 'feishu', token, url }`；
     - 其余无效或缺失目录返回 `{ kind: 'invalid', code: 'OWNERSHIP_CONFIG_MISSING', ... }`。
   - 提供对称校验工具 `isLocalizedDocsUrl(value)` 供英文侧拒绝误填 `localized-docs/...`。
2. **解耦 `record_id` 的激活清单与路由上下文（`core/handoff/routing.ts`）**：
   - `ActiveLocalizedPage` 主键为 `{ page: PageId, page_url: string, feishu_token: string | null, feishu_aliases?: string[], anchors: Record<string, string>, activated_in: string, last_seen_record_id?: string | null }`：
     - **`page` 与 `page_url`（规范化后的目标相对发布路径/slug）均为全局唯一主键**；
     - **`last_seen_record_id` 仅为可选参考元数据，不参与唯一性约束、路由查找或回退匹配**！
   - `createLocalizedRoutingContext({ records, availablePages, active })`：
     - 按 `page_url`（而非 `record_id`！）关联 `active.pages` 中的已激活记录；
     - **关键场景**：同一 `page_url` 在飞书 Base 中被移表或重建导致 `record_id` 改变（如 `recOLD` → `recNEW`），只要 `Docs` 仍指向同一 `localized-docs/zh-CN/guides/pages/<page>`，路由判定与回退基线查找**完全正常通过，零误报**；
     - 若已激活的 `page_url` 将 `Docs` 误改回飞书链接 → 抛出 `OWNERSHIP_REVERTED`；
     - 若已激活的 `page_url` 指向不同的 `<page-id>`，或两个不同 `page_url` 指向同一个 `<page-id>` → 报 `OWNERSHIP_CONFIG_MISSING` / 重复所有者错误。
3. **独立的 `dev` 激活与来源凭据 Schema（`core/handoff/receipt.ts`）**：
   - 路径函数：
     - `localizedActiveStatePath('zh-CN', 'guides')` → `generated/zh-CN/manifests/localized-pages/guides/active.json`
     - `localizedReceiptPath('zh-CN', 'guides', page)` → `generated/zh-CN/manifests/localized-pages/guides/<page>.json`
   - `validateLocalizedReceipt(value, expected)` 严格校验：`schema_version: 1`、`locale: 'zh-CN'`、`page`、`page_url`、`inputs`（`master_commit`、`dev_commit`、`source_files[]` 含 `source.md`/`page.yaml`/`Variables.json`/片段 SHA-256、`md2md_version`、`navigation_digest`、`image_base_url`、`images[]`）、`output`（`path` 必须落在 `content/zh-CN/guides/...` 且带 SHA-256）、`channel`（`null | 'next' | 'retire-in-next'`）、`fetch_run_id`，以及可选参考字段 `reference_record_id?: string | null`。
4. **Promote 候选解包纯计算（`core/handoff/promote.ts`）**：
   - 实现 `promoteLocalizedSource({ sourceMarkdown, expectedEnNextSha, baselineEnNextSha, authoredChannelBlockIds })`：
     - 先核验 `expectedEnNextSha === baselineEnNextSha`（不一致时直接阻断并返回 `PROMOTE_EN_MISMATCH`，保留现网中文不放行）；
     - 对生成器管理的通道块：解包 `<NextChannel action="include">` 保留其已审中文 NEXT 正文，移除配对的旧 `<NextChannel action="exclude">` 块；
     - 保留作者显式标记的独立手写通道块（不被误解包）；
     - 对解包后的结果运行 `validateChannelTags` 与 `validateUiTags`（含确保无未闭合/残留标记），输出干净的 `promotedMarkdown` 与变更摘要。

## 完成的定义

- [ ] `core-boundary.test.ts` 覆盖 `localized-docs/core/handoff/**`，确认零 `lark/`、fs、网络依赖。
- [ ] 全套 Vitest 单元测试覆盖：
  - 站点路由互斥：`localized-docs/zh-CN/guides/pages/<id>` 通过；`shared-docs/...`、`localized-docs/ja-JP/...`、保留名 `active`、路径逃逸被拒；
  - **`record_id` 变更免疫测试**：模拟已激活页面在飞书 Base 跨表移动导致 `record_id` 从 `recA` 变为 `recB` 但 `page_url` 不变时，路由识别、回退基线与别名追踪全部正常通过；
  - `OWNERSHIP_REVERTED`（已激活 `page_url` 误改回飞书链接拦截）与重复所有者冲突测试；
  - `active.json` 与 `<page-id>.json` 路径及严格 schema 正/负面校验（拒绝输出越界到 `content/en/` 或 `content/zh-CN/reference/`）；
  - Promote 解包：英文 NEXT 摘要匹配时正确解包 `include` + 删除 `exclude`；英文 NEXT 摘要变化时阻断并报错 `PROMOTE_EN_MISMATCH`。
- [ ] 运行并全绿：
  - `pnpm exec vitest run packages/docs-tooling/src/localized-docs --pool=forks --isolate --maxWorkers=1`
  - `pnpm test:for-change -- --base origin/master --head HEAD`（0 未映射路径，且跑完返回的所有命令）
  - `pnpm test:typescript-runtime-boundary`、`pnpm typecheck`、`pnpm test:workflow-matrix`、`pnpm test:workflow-policy`、`git diff --check`。

## 不做

- 不修改 `packages/docs-tooling/src/lark/` 或 `scripts/docs-workflow/guides-*.js` 接入生产 Fetch（归属 `ZH-WP6b`，待对齐最新 Base 抓取入口后一次性接线并跑真实回放）。
- 不修改英文 `shared-docs` 的 `source-state.ts` 或 `routing.ts`。

## 已知的坑

- **`page_url` 规范化**：不同表格或历史快照里路径可能带或不带前导 `/` 或 `.md`/`.mdx` 后缀；在 `core/handoff/routing.ts` 中定义唯一的 `normalizeLocalizedPageUrl()` 函数（去前导/尾部 `/`、去 `.mdx?`、拒绝 `..` 和空段），所有主键比对与查找统一走规范化后的 `page_url`。
- **路径隔离防写串**：`validateLocalizedReceipt` 必须强制校验输出路径落在 `content/zh-CN/guides/` 内，且排除 Guides 首页和 `content/zh-CN/guides/tutorials/tools/`（防止与现行流程及 `zh-CN-reference` 冲突）。
