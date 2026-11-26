# ZH-WP0a `<UI>` 全局组件与 `shared-docs` 白名单

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：阶段 0（前置底座）　**依赖**：无　**状态**：待启动

## 目标

在 `packages/docs-ui` 注册全局 MDX 组件 `<UI>`（英文站与中文站共用，无需在正文手写 `import`），并在 `packages/docs-tooling` 的 `shared-docs` 标签白名单中放行 `<UI>`，使作者可以在 `master:shared-docs/guides/pages/<page>/cloud-*.md` 中安全标注控制台界面词（如 `<UI>Create Cluster</UI>`），经英文 Fetch 自动透传到 `dev` 并在双站正确渲染。

## 要读的

| 文档 / 源码 | 位置 | 读它为了什么 |
|---|---|---|
| 中文 Guides 技术设计 | [11 §1 与 §3.3](../../design/11-zh-cn-translation-pipeline.md#33-代码块三档保护统一术语底座与-ui-界面词) | `<UI>` 组件上线顺序与隔离语义 |
| 现有全局组件样例 | `zdoc:packages/docs-ui/src/shared/components/NextChannel/index.tsx` 与 `index.test.tsx` | 复刻全局 MDX 组件与 Vitest 单测写法 |
| 全局 MDX 注册表 | `zdoc:packages/docs-ui/src/shared/theme/MDXComponents/index.tsx` | 确认全局组件注册位置（同时覆盖 EN 与 ZH 站点） |
| `shared-docs` 组件白名单 | `zdoc:packages/docs-tooling/src/shared-docs/core/site/components.ts` 与 `core/transforms/index.ts` | 确认 `compatibilityTags` 放行机制 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-ui/src/shared/components/UI/index.tsx`（新增） | `milvus-docs` 或 `@zilliz/mdtomd` |
| `packages/docs-ui/src/shared/components/UI/index.test.tsx`（新增） | `devOwnedPaths`（`content/`、`generated/`、`i18n/`） |
| `packages/docs-ui/src/shared/theme/MDXComponents/index.tsx` | `scripts/translation/` 或发布工作流 |
| `packages/docs-tooling/src/shared-docs/core/site/components.ts` | 任何与 `<UI>` 无关的 UI 样式或组件 |
| `packages/docs-tooling/src/shared-docs/testing/`（补充 `<UI>` 透传测试） | |
| `scripts/docs-workflow/test-matrix.json`（仅当 `pnpm test:for-change` 报未映射路径时） | |

## 接口与行为约定

1. **组件签名（`packages/docs-ui/src/shared/components/UI/index.tsx`）**：
   ```tsx
   import React, {type ReactNode} from 'react';

   export interface UIProps {
     children?: ReactNode;
   }

   export default function UI({children}: UIProps) {
     return <strong className="zd-ui-label">{children}</strong>;
   }
   ```
   - 保持极简内联语义（渲染为 `<strong>`），不引入额外阻塞脚本或复杂布局，不改变普通文本可读性；
   - 在 `packages/docs-ui/src/shared/theme/MDXComponents/index.tsx` 中注册为 `UI`（与 `NextChannel` 同级）。
2. **`shared-docs` 白名单（`packages/docs-tooling/src/shared-docs/core/site/components.ts`）**：
   - 将 `'UI'` 加入 `compatibilityTags`（而非 `componentImports`），原因：`UI` 已在 `MDXComponents` 全局注册，不需要生成器往每篇 MDX 顶部注入 `import UI from ...`；加入 `compatibilityTags` 后，`isRecognizedContentTag('UI')` 返回 `true`，`transforms` 放行 `cloud-*.md` 中的 `<UI>...</UI>`，`adaptPage` 与 `toMdx` 透传而不报错。
   - 验证在 `cloud-*.md` 的普通段落、列表项与 `<NextChannel>` 内部使用 `<UI>Create Cluster</UI>` 时，均能通过 `transforms`、`adaptPage`、`mergeMarkdown` 与 `toMdx` 校验并原样输出。

## 完成的定义

- [ ] `packages/docs-ui/src/shared/components/UI/index.test.tsx` 覆盖：基本渲染（`<strong className="zd-ui-label">`）、中英文文本内容、空/嵌套子节点。
- [ ] `packages/docs-tooling/src/shared-docs/testing/` 新增单测覆盖：`cloud-*.md` 含 `<UI>Create Cluster</UI>` 时 `transforms` 放行、`adaptPage` 不注入多余 `import`、`mergeMarkdown` / `toMdx` 完整保留 `<UI>` 标签，且未知自定义标签（如 `<UnknownTag>`）仍被拒绝。
- [ ] 运行并全绿：
  - `pnpm test:for-change -- <所有变更文件路径>` 返回的全部命令
  - `pnpm typecheck`
  - `git diff --check`
- [ ] 若改动触发站点构建验证，确认 `pnpm build:en` / `pnpm build:zh-CN` 中至少跑通相关 UI 单测与类型检查（并在交接摘要中明确列出实跑项）。

## 不做

- 不在本次 PR 中修改任何现有 `shared-docs/guides/pages/*/cloud-*.md` 正文去打 `<UI>` 标签。
- 不实现翻译侧 `<UI>` 提取与待确认清单（归属 `ZH-WP1` / `ZH-WP2`）。
- 不修改 Docusaurus `llms.txt` 或全文搜索插件。

## 已知的坑

- **不要把 `UI` 放进 `componentImports`**：否则 `adaptPage` 会在每篇含 `<UI>` 的页面顶部生成 `import UI from '...'`，不仅多余，还要求维护单独的 `@site/src/components/UI` 转发文件。放进 `MDXComponents` + `compatibilityTags` 与 `NextChannel` 机制完全一致。
- **检查 `merge/segment.ts`**：确认内联 `<UI>...</UI>` 不会被块级容器扫描器误判为未支持的块级 JSX 容器标签（只处理 `Tabs`/`TabItem`/`Admonition`/`NextChannel`）。
