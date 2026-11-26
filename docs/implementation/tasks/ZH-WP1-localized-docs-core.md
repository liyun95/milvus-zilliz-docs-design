# ZH-WP1 `localized-docs` 核心契约、英文剥壳与 `md2md` 组装

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 1（离线核心引擎）　**依赖**：[ZH-WP0a](./ZH-WP0a-ui-component.md)　**状态**：待启动

## 目标

在 `packages/docs-tooling/src/localized-docs/` 建立中文 Guides 的纯核心模块与离线 CLI（`check` / `build`）：解析并校验 `localized-docs/zh-CN/guides/` 的目录结构（`Variables.json`、`fragments/`、`pages/<page-id>/{page.yaml, source.md, .baseline.json}`），实现 `dev` 英文产物的壳子剥离、`<UI>` 节点解析校验，以及经 `@zilliz/mdtomd` 预处理 + 站点组装（front matter / 组件 `import` / 双通道与 MDX 校验）的离线编译能力。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §2.1–2.2、§3.1、§4.1](../../design/11-zh-cn-translation-pipeline.md#2-数据流目录结构与职责边界) | 目录结构、`page.yaml`/`.baseline.json` schema、pre-`md2md` 边界与双通道约束 |
| `shared-docs` 分层范式 | `zdoc:packages/docs-tooling/src/shared-docs/adapters/md2md.ts` 与 `core/variables.ts` | 直接复用 `@zilliz/mdtomd` 适配器与变量校验，保持 `core/` 纯计算 |
| `shared-docs` 站点组装与 MDX 校验 | `zdoc:packages/docs-tooling/src/shared-docs/core/site/components.ts` 与 `adapters/mdx.ts` | 复用组件 `import` 注入、`<UI>` 白名单和 MDX 解析校验 |
| `zdoc` CLI 注册入口 | `zdoc:packages/docs-tooling/src/cli-main.ts` | 确认子命令注册方式 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/localized-docs/core/**`（新增：types、config、baseline、strip-en、ui-tags、assemble） | `packages/docs-tooling/src/lark/**`（禁止直接耦合飞书适配器） |
| `packages/docs-tooling/src/localized-docs/adapters/**`（新增：fs-reader、md2md 复用封装） | `packages/docs-tooling/src/shared-docs/**`（只读复用，不改英文共享页逻辑） |
| `packages/docs-tooling/src/localized-docs/commands/**`（新增：check、build） | `.github/workflows/**`（工作流留到 ZH-WP4 / ZH-WP5） |
| `packages/docs-tooling/src/localized-docs/testing/**`（新增：合成 fixtures 与全套 Vitest 单测） | `devOwnedPaths` |
| `packages/docs-tooling/src/cli-main.ts`（注册 `localized-docs` 子命令） | |
| `scripts/docs-workflow/test-matrix.json`（登记 `packages/docs-tooling/src/localized-docs/**`） | |

## 接口与行为约定

1. **目录结构与配置 Schema（`core/config.ts`、`core/baseline.ts`）**：
   - `localized-docs/zh-CN/guides/` 下支持：
     - `Variables.json`（复用 `parseVariables` 校验，拒绝非法结构）；
     - `fragments/`（可选目录，禁止符号链接与路径逃逸）；
     - `pages/<page-id>/`（`<page-id>` 匹配 `/^[a-z0-9]+(?:-[a-z0-9]+)*$/`，禁用 `active` 等保留名）：
       - `page.yaml`（严格 schema，`schema_version: 1`、`mode: 'incremental' | 'manual' | 'paused'`、`en_source: { manual: 'guides', shared_page: string }`、`sync_policy?: 'independent' | 'bilingual_sync'`、`notify_on_en_change?: boolean`、`pause_reason?: string`、`follow_up?: string`、`variables?: Record<string, string>`；**显式拒绝旧字段 `owner`、`feishu_record_id`**）；
       - `source.md`（可选存在：仅当 `mode === 'incremental'` 且同时缺少 `source.md` 与 `.baseline.json` 时判定页面状态为 `'pending-initial-translation'`；若存在 `source.md` 但缺少 `.baseline.json` 则判定为 `'baseline-missing-error'`，严禁误当新页首译！）；
       - `.baseline.json`（严格校验 `schema_version: 1`、`page_id`、`en_baseline`、`zh_reviewed.source_sha256`、`last_notified_en_sha`、`sections[]`）。
2. **`dev` 英文产物剥壳器（`core/strip-en.ts`）**：
   - 输入 `dev:content/en/guides/...` 原始 MDX 文本；
   - 提取并保留 `title`、`description`（去掉 ` | Cloud` 站点后缀时记录原始值）及正文；
   - 剥离机器生成的导航/发布 front matter（`slug`、`sidebar_label`、`sidebar_position`、`token`、`custom_edit_url`、`type`、`displayed_sidebar`、`beta`、`added_since`、`last_modified`、`deprecate_since`、`notebook`）和正文顶部由生成器注入的 Docusaurus `import` 语句（如 `import Tabs from '@theme/Tabs';`、`import Admonition from '@theme/Admonition';`）；
   - 原样保留 `<NextChannel action="include|exclude">`、`<UI>...</UI>`、fenced 代码块、表格与锚点，并输出稳定的 `body` 与 `sha256`。
3. **`<UI>` 标签解析与校验（`core/ui-tags.ts`）**：
   - 忽略 fenced 代码块与行内反引号 `` `...` ``，扫描并提取所有 `<UI>...</UI>` 文本及行号；
   - 对未闭合 `<UI>`、嵌套 `<UI><UI>...</UI></UI>`、多余属性或空标签返回确定性错误码（如 `UI_TAG_MALFORMED`）。
4. **`md2md` 预处理与站点组装（`core/assemble.ts` + `adapters/md2md.ts`）**：
   - 校验 `source.md` 不得包含机器生成的导航 front matter 或手写 `import` 壳代码；
   - 合并组级 `Variables.json` 与可选页面级 `page.yaml` `variables` 覆盖，调用 `@zilliz/mdtomd/preprocess.js` 展开变量与 `fragments/`；
   - 校验 `<NextChannel action="include|exclude">` 合法性（拒绝 `variant`、未闭合、非法嵌套）与 `<UI>` 标签合法性；
   - 根据调用方传入的组装元数据（`title`、`description`、`slug`、`sidebar_label`、`sidebar_position`、`channel` 等）生成最终 MDX：注入 front matter、按正文实际使用的组件（`Tabs`/`TabItem`/`Admonition`/`Supademo`/`Procedures`/`DocCardList`，**不含全局注册的 `UI` 与 `NextChannel`**）自动补齐 `import`，并过 `toMdx` 语法校验。
5. **离线 CLI 子命令（`commands/check.ts`、`commands/build.ts`）**：
   - `pnpm docs-tooling localized-docs check --root <dir> [--page <page-id>]`：校验全部或单页配置、`Variables.json`、`source.md`、`<UI>`、通道、`.baseline.json` 一致性与 `md2md` + MDX 编译；
   - `pnpm docs-tooling localized-docs build --root <dir> --out <dir> [--page <page-id>]`：将离线组装后的最终 MDX 与依赖清单写入空目标目录（拒绝覆盖非空目录或符号链接）。

## 完成的定义

- [ ] 全套 Vitest 离线测试覆盖：
  - `page.yaml` 三种模式（`incremental` / `manual` / `paused`）合法与非法用例（含拒绝 `owner`、`feishu_record_id`、非法 `page-id`、路径逃逸）；
  - 页面状态机：`pending-initial-translation`（有 `page.yaml` 无 `source.md`/`.baseline.json`）与 `baseline-missing-error`（有 `source.md` 缺 `.baseline.json`）严格区分；
  - `stripEnShell` 在真实 `delete-entities.md` 与 `get-and-scalar-query.md` 样例形态下准确剥离导航 front matter 与 `import`，保留 `<NextChannel>`、`<UI>` 与代码块；
  - `<UI>` 解析忽略代码块/行内代码，拦截未闭合/嵌套/空标签；
  - `md2md` 预处理展开中文 `Variables.json` 与 `fragments/`，组装输出合法 MDX（不生成多余 `import UI`），双通道错误（`variant`、未闭合、嵌套）被拦截；
  - `cli-main.ts` 端到端集成测试跑通 `localized-docs check` 与 `localized-docs build`。
- [ ] 运行并全绿：
  - `pnpm exec vitest run packages/docs-tooling/src/localized-docs --pool=forks --isolate --maxWorkers=1`
  - `pnpm test:for-change -- <所有变更文件路径>` 返回的全部命令
  - `pnpm test:typescript-runtime-boundary`
  - `pnpm typecheck`
  - `pnpm test:workflow-matrix`
  - `git diff --check`

## 不做

- 不实现增量 diff、三档代码块同步或 LLM 调用（归属 `ZH-WP2`）。
- 不实现飞书底稿导入（归属 `ZH-WP3`）或 Fetch 切流接线（归属 `ZH-WP6a` / `ZH-WP6b`）。
- 不在 `zdoc` 仓库根目录提交真实的 `localized-docs/zh-CN/guides/` 内容页面（测试用 `testing/fixtures/` 合成目录）。

## 已知的坑

- **TypeScript 运行时边界**：`zdoc` 有 `pnpm test:typescript-runtime-boundary` 门禁，新增 `localized-docs/` 文件需遵守 `packages/docs-tooling/src/` 既有的相对导入与 CommonJS/ESM 边界（可对照 `shared-docs/` 写法）。
- **`md2md` 的 `fragmentRoot` 要求**：`fragments/` 在组内为可选目录；当目录不存在时，传给 `@zilliz/mdtomd/preprocess.js` 须使用安全空临时目录（且校验正文未引用不存在的片段），不得把仓库根目录传作 `fragmentRoot`。
- **不要把中文 `source.md` 的 `# 标题` 强绑死在 `front matter`**：允许 `source.md` 用极简 front matter（如 `title`、`description`）或由组装器回退到一级标题，具体解析逻辑在单测里固定契约，方便 `ZH-WP2` 和 `ZH-WP3` 直接复用。
