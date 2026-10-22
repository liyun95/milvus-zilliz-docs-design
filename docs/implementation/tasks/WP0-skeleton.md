# WP0 测试与目录骨架

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：无　**状态**：已合并（[zilliztech/zdoc#792](https://github.com/zilliztech/zdoc/pull/792)，commit [`5dd0e56`](https://github.com/zilliztech/zdoc/commit/5dd0e56a58054864eda231deeb76f1945be80fb0)）

## 目标

在 zdoc 中建好共享页代码的目录、测试工具和检查，让之后的工作包只需要写业务逻辑和测试。这个工作包不实现任何业务行为。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [实现指南](../README.md) | 第 2、3 节 | 要建的每一样东西 |
| [技术设计 README](../../design/README.md) | 代码位置 | 目录布局与边界 |
| [技术设计 09](../../design/09-error-catalog.md) | 错误的结构 | 错误对象的字段 |
| zdoc `AGENTS.md`、`packages/docs-tooling/src/manuals/README.md` | 全文 | master 与 dev 的归属、对照表、本地检查 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新建 `packages/docs-tooling/src/shared-docs/` 下的全部文件 | `packages/docs-tooling/src/lark/` 等现有模块 |
| `scripts/docs-workflow/test-matrix.json`：新增一条 `shared-docs` | 其他对照表条目 |
| 根目录 `package.json`：新增脚本 `test:shared-docs` | 其他脚本 |
| `.github/workflows/site-validation.yml`：新增一个只跑 `test:shared-docs` 的步骤 | 其他步骤；需要 zdoc 维护者在 PR 中同意 |

## 要建的

```
packages/docs-tooling/src/shared-docs/
  AGENTS.md                     # 实现指南第 5 节“Agent 的规则”
  index.ts                      # 对外导出，暂时只导出类型
  core/types.ts                 # SharedDocsError（技术设计 09 的字段）、PageId、Channel 等共用类型
  adapters/
    types.ts                    # MilvusDocsReader、Md2md、GitHost、ImageStore、GuidesBase 五个接口
    fake/                       # 每个接口一个假实现（实现指南 2.6）
    contract/                   # 每个接口一组契约测试，假实现必跑，真实实现留空待后续工作包
  spec/
    requirements.json           # 从设计仓库 docs/implementation/requirements.json 原样复制
    pending.json                # zdoc 负责、尚未覆盖的编号 → 工作包（按 实现指南第 4 节填）
    coverage.test.ts            # 实现指南 2.2
  fixtures/
    milvus-docs/build.ts        # 合成仓库的构建器（实现指南 2.3）
    milvus-docs/commits/01-base/  02-paragraph/
    pilots/<页面>/milvus-docs/  # 三篇试点页的原文，SOURCE.md 记 commit
    pilots/<页面>/shared-docs/  # page.yaml 等，照产品需求场景 3、4 的例子写
    golden/                     # 先放 .gitkeep；基准输出由 WP4、WP5 产生
    errors/                     # 先放一个示例目录，供运行器自测
  testing/
    golden.ts                   # 比较与 UPDATE_GOLDEN 改写
    errors.ts                   # 错误样例表的运行器
```

- 试点页原文取 milvus-docs `v3.0.x` 的 `9acdc99959e188a54be1df512ea3806c3110ef59`：`site/en/userGuide/insert-and-delete/delete-entities.md`、`site/en/userGuide/search-query-get/filtered-search.md`、`site/en/userGuide/embeddings-reranking/embedding-function/openai.md`。三篇都不引用片段（已核对）。
- `commits/03-typo` 到 `10-image-changed` 不在本工作包中建，由用到它们的工作包补。

## 接口

```ts
// core/types.ts
export type Channel = 'current' | 'next'
export interface SharedDocsError {
  code: string            // requirements.json 中的错误码
  message: string
  file?: string
  line?: number           // 从 1 开始
  detail?: unknown
  page?: string
  channel?: Channel | 'both'
  fix?: string
}

// fixtures/milvus-docs/build.ts
export function buildMilvusDocs(upTo: string): Promise<{ dir: string; commits: Record<string, string> }>
// upTo 如 '03-typo'；返回仓库目录与“提交名 → commit 号”；两次调用得到相同的 commit 号

// testing/golden.ts
export function expectGolden(relativePath: string, actual: string): void
// 不一致时失败并打印差异；UPDATE_GOLDEN=1 时改写文件；CI 环境中忽略 UPDATE_GOLDEN
```

## 要覆盖的编号

本工作包不覆盖业务编号。`pending.json` 中应列出 zdoc 负责的全部编号，覆盖检查在这种状态下通过。

| 自测 | 断言 |
|---|---|
| 覆盖检查 | 引用清单中不存在的编号时失败；缺口不在 `pending.json` 中时失败；`pending.json` 中的编号已被测试覆盖时也失败，提示删掉它 |
| 合成仓库 | 两次构建得到相同的 commit 号；`upTo` 之后的提交不出现 |
| 基准输出 | 不一致时失败；`UPDATE_GOLDEN=1` 时改写；`CI=true` 时即使设了 `UPDATE_GOLDEN` 也不改写 |
| 假实现 | 每个假实现通过自己接口的契约测试 |

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿
- [ ] `pnpm test:for-change -- packages/docs-tooling/src/shared-docs scripts/docs-workflow/test-matrix.json .github/workflows/site-validation.yml` 给出的命令全部跑过
- [ ] `pnpm typecheck`、`pnpm test:workflow-policy`、`git diff --check` 通过
- [ ] `core/` 中没有 `node:fs`、`node:child_process`、网络调用，也不引用 `lark/`（由一个测试检查导入）
- [ ] PR 说明按 [实现指南第 5 节](../README.md#pr-说明的格式)的格式写

## 不做

- 任何业务逻辑：解析 `page.yaml`、调用 md2md、生成 MDX 都在后续工作包中。
- `cli-main.ts` 中的子命令：等第一个需要命令的工作包（WP3）再加。
- 基准输出本身。

## 已知的坑

- zdoc 的 vitest 配置在根目录，环境是 `jsdom`；共享页的测试需要 Node 环境，在测试文件顶部用 `// @vitest-environment node`。
- Git 的 commit 号受作者、提交者与时间影响：构建器里固定 `GIT_AUTHOR_NAME`、`GIT_AUTHOR_EMAIL`、`GIT_AUTHOR_DATE` 及对应的 `GIT_COMMITTER_*`，并关闭签名（`commit.gpgsign=false`）。
- zdoc 的 PR 检查目前不跑 vitest，新增的步骤只跑本目录，不要顺手把全部 vitest 加进去。
