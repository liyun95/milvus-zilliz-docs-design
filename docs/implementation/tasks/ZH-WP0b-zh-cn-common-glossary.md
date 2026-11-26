# ZH-WP0b 全站统一中文术语底座（`zh-CN-common.json`）

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 0（前置底座）　**依赖**：无　**状态**：待启动

## 目标

将现有 `config/translation/zh-CN-reference.json` 中的全站通用中文术语与通则抽出到单一共享文件 `config/translation/zh-CN-common.json`，轻量扩展 `scripts/translation/localeContract.js` 支持 `extends` 继承合并，使 `zh-CN-reference.json` 对外加载结果与现网**逐字节完全等价**，同时新增极薄壳配置 `config/translation/zh-CN-guides.json` 供中文 Guides 翻译器使用。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §3.3](../../design/11-zh-cn-translation-pipeline.md#33-代码块三档保护统一术语底座与-ui-界面词) | 统一中文术语底座设计要求 |
| 现有中文契约 | `zdoc:config/translation/zh-CN-reference.json` | 确认现有全部字段与词条 |
| 契约加载与校验器 | `zdoc:scripts/translation/localeContract.js` | 确认 `ROOT_KEYS`、`CONTRACT_PATHS`、`exactKeys` 与 `loadLocaleContract` 实现 |
| 现有契约单测 | `zdoc:scripts/translation/localeContract.test.js` | 确认不可破坏的断言与测试风格 |
| 风格指南通则参考 | `zdoc:.github/prompts/codex-style-guide.zh-CN-reference.md`（第 0–1 章） | 确认通用中文规范表述一致 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `config/translation/zh-CN-common.json`（新增） | `config/translation/ja-JP.json`（零改动） |
| `config/translation/zh-CN-reference.json`（转为薄壳继承） | `scripts/translation/surgicalUpdate.js`、`agenticProvider.js` 等运行时翻译逻辑 |
| `config/translation/zh-CN-guides.json`（新增薄壳） | `packages/docs-tooling/src/translation/targets.ts`（首期不把 `zh-CN-guides` 注册进旧 Reference 自动翻译目标，避免触发旧工作流！） |
| `scripts/translation/localeContract.js` | `.github/workflows/translate-codex.yml`、`publish-translation.yml` |
| `scripts/translation/localeContract.test.js` | |
| `scripts/docs-workflow/test-matrix.json`（登记新增的两个 JSON 路径） | |

## 接口与行为约定

1. **`config/translation/zh-CN-common.json` Schema**：
   - 允许的顶层键：`schemaVersion`（`1`）、`locale`（`"zh-CN"`）、`styleRules`、`mandatoryTerms`、`forbiddenTranslations`、`doNotTranslate`、`contextualTerms`、`examples`。
   - 承接原 `zh-CN-reference.json` 中所有全站通用词条与通则（用“您”、中英文半角空格、代码块及注释受保护、`Compaction`/`collection`/`entity`/`schema`/`database`/`partition`/`segment`/`analyzer`/`endpoint`/`Dedicated` 等）。
2. **`extends` 合并语义（`scripts/translation/localeContract.js`）**：
   - `CONTRACT_PATHS` 新增 `'zh-CN-guides': 'config/translation/zh-CN-guides.json'`。
   - `loadLocaleContract(target, repositoryRoot)` 读取目标 JSON 后，若存在 `extends` 字段：
     - 校验 `extends` 为非空相对路径且解析后必须位于 `config/translation/` 目录内（拒绝绝对路径、路径逃逸 `..`、符号链接、嵌套循环 `extends`）；
     - 校验基座文件的 `schemaVersion === 1`、`locale === child.locale` 且顶层键严格匹配 `COMMON_KEYS`；
     - 合并规则：数组字段（`styleRules`、`mandatoryTerms`、`forbiddenTranslations`、`doNotTranslate`、`contextualTerms`、`examples`）按 `[...base, ...child]` 顺序拼接（若 child 省略某数组字段则默认为空数组 `[]`）；标量字段（`schemaVersion`、`contractId`、`target`、`locale`）取 child；
     - 剥离 `extends` 键后送入既有 `validateLocaleContract(merged, target)`，复用全部去重与一致性校验并 `deepFreeze`。
   - **关键向后兼容保证**：
     - `validateLocaleContract(value, expectedTarget)` 对直接传入的完整契约对象保持原有 `exactKeys(value, ROOT_KEYS)` 严格校验不变（不放宽 `extra: true` 等负面测试）；
     - `loadLocaleContract('zh-CN-reference')` 返回的冻结对象与重构前**深度完全相等（`assert.deepEqual`）**！
3. **`config/translation/zh-CN-guides.json` 内容**：
   - `schemaVersion: 1`、`contractId: "zh-CN-guides-2026-11-26-v1"`、`target: "zh-CN-guides"`、`locale: "zh-CN"`、`extends: "./zh-CN-common.json"`；
   - `styleRules` 仅补充 Guides 专属规则：保留 `<UI>...</UI>` 控制台界面词原词不自由翻译（交主审对照中文控制台替换）、保留 `<NextChannel action="include|exclude">` 边界、不将 Global 独有区域/配额引入中国站。

## 完成的定义

- [ ] 新增严格对比测试：用重构前快照或显式断言确认 `loadLocaleContract('zh-CN-reference')` 的所有字段与重构前完全一致，且仍为 `deepFreeze`。
- [ ] 新增 `zh-CN-guides` 加载测试：确认继承了 `zh-CN-common.json` 的全部 `mandatoryTerms`/`forbiddenTranslations`/`doNotTranslate`/`contextualTerms`/`examples`，且包含 Guides 专属 `styleRules`。
- [ ] 新增负面安全测试：路径逃逸 `extends`（如 `../foo.json`）、缺失基座文件、基座 `locale` 不匹配、嵌套/循环 `extends`、合并后重复词条均抛出清晰错误。
- [ ] 运行并全绿：
  - `pnpm test:translation`
  - `pnpm test:for-change -- config/translation/zh-CN-common.json config/translation/zh-CN-reference.json config/translation/zh-CN-guides.json scripts/translation/localeContract.js scripts/translation/localeContract.test.js` 返回的全部命令
  - `pnpm test:workflow-matrix`
  - `pnpm test:workflow-policy`
  - `git diff --check`

## 不做

- **严禁**把 `zh-CN-guides` 加入 `packages/docs-tooling/src/translation/targets.ts` 或 `reconciliation-policy.json`——中文 Guides 使用独立工作流，不能被旧 `translate-codex.yml` 扫描到。
- 不修改 `codex-style-guide.zh-CN-reference.md` 正文。

## 已知的坑

- **`styleRules` 顺序保真**：原 `zh-CN-reference.json` 中第 5 条 `styleRules` 提到了 Reference style guide 注入；把通用 5 条放进 `zh-CN-common.json`，把 Reference 专属那 1 条放进 `zh-CN-reference.json` 时，注意保持 `zh-CN-reference` 合并后的 `styleRules` 与原内容完全一致（或调整顺序时确认无任何测试依赖固定下标）。
- **`scripts/translation/localeContract.test.js` 里有 `extra: true` 负面用例**：`extends` 只应在 `loadLocaleContract` 文件加载层解析并剥离，不要把 `extends` 加进 `ROOT_KEYS` 放宽 `validateLocaleContract`！
