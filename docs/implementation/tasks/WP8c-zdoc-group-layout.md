# WP8c `shared-docs/` 按组分目录

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP8](./WP8-zdoc-build-and-validate.md) 已合并（WP8b [zilliztech/zdoc#832](https://github.com/zilliztech/zdoc/pull/832)，commit [`8680736`](https://github.com/zilliztech/zdoc/commit/86807361cdca0f2b768f51d7ff47c5b78461bee8)）。要在 [WP9](./WP9-zdoc-fetch-handoff.md) 开工和第一篇试点页面提交之前合并　**状态**：未开始

## 目标

`shared-docs/` 下按组分子目录，Phase 1 只有一组 `guides`（[技术设计 02](../../design/02-page-config.md#shared-docs-的位置)）：

```
shared-docs/guides/source.yaml, Variables.json, links.yaml, product-names.yaml, presentation/, pages/<页面标识>/
```

只改路径，不改任何生成结果。做完后：

- 命令的 `--shared-docs` 指向一个组的目录，如 `shared-docs/guides`；
- 报错中的文件位置写成相对仓库根目录的完整路径，如 `shared-docs/guides/pages/openai/page.yaml`；
- 两个 PR 工作流按组处理：只处理有变化的组；
- 遇到 `guides` 以外的组，明确报错，不能当成 Guides 处理。

现在 zdoc master 上还没有 `shared-docs/` 目录，所以这次不用搬任何已提交的页面。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [技术设计 02](../../design/02-page-config.md) | `shared-docs/` 的位置；设计理由中的“为什么按组分目录” | 新的目录结构 |
| [技术设计 04](../../design/04-channels-and-lock.md) | 共享来源配置与跟踪分支 | 每组一份 `source.yaml` |
| [技术设计 08](../../design/08-workflows-and-permissions.md) | `shared-docs-lock`、`shared-docs-validate` 两行 | 触发路径 |
| [WP8 走读](../walkthroughs/WP8.md) | 全文 | 要改的命令与工作流 |
| [实现指南](../README.md) | 第 5 节 | 规则 |

## 范围

| 可以改 | 不能改 |
|---|---|
| `packages/docs-tooling/src/shared-docs/` 中写死 `shared-docs/pages`、`shared-docs/source.yaml` 等路径的代码：`commands/` 的四个命令、`adapters/read-page.ts`、`inspect-page.ts`、`build-page.ts`、`core/config.ts`、`core/variables.ts`、`core/links/seed.ts`、`core/product-names/` 中的报错位置 | 任何生成结果：同样的输入，MDX、`images.json`、报错的错误码与行号都不变，只有报错中的文件路径多一层组名 |
| `fixtures/`、`testing/` 中的路径与期望报错 | `spec/pending.json`：本工作包不覆盖编号 |
| `spec/requirements.json`：从设计仓库逐字节复制最新的 [`requirements.json`](../requirements.json)。只有 `5-2` 的文字变了（映射表改为每组一份） | |
| `.github/workflows/shared-docs-lock.yml`、`shared-docs-validate.yml` 的触发路径与读取的文件 | 其他工作流 |
| `scripts/validate-workflow-policy.js` 及其测试、`scripts/docs-workflow/test-matrix.json` 中与这两个工作流相关的规则 | `lark/` 与 dev 上的任何文件 |
| `packages/docs-tooling/src/shared-docs/README.md` 中的路径与命令示例 | |

## 怎样改

- **命令**：
  - `shared-docs build`、`lock`、`inspect`、`links-seed` 的 `--shared-docs` 都改为接收一个组的目录。
  - 报错中的 `file` 由这个目录相对仓库根目录的路径拼出，不再写死 `shared-docs/`。
  - 组名取目录名；不是 `guides` 时报 `CONFIG_FIELD_MISSING` 或计划中提出的更合适的现有错误码，说明“只支持 guides 组”。不要新增错误码。
- **`shared-docs-lock.yml`**：
  - 触发路径改为 `shared-docs/*/pages/**`；
  - 读 `shared-docs/guides/source.yaml`；
  - 检查新写入的 lock 路径的正则改为 `^shared-docs/guides/pages/<页面标识>/lock\.yaml$`；
  - PR 中改到其他组的页面时失败，并说明原因。
- **`shared-docs-validate.yml`**：
  - 比较范围仍是 `shared-docs/`；
  - 按变化的文件算出涉及哪些组，逐组运行；
  - 只有 `guides` 时，行为与现在相同。
- **测试**：把现有用例的输入移到 `guides/` 下；另加两个用例：
  - `--shared-docs` 指向 `guides` 以外的组时报错；
  - 报错的文件路径带组名。

## 要覆盖的编号

本工作包不覆盖需求编号，只要求现有测试在新路径下全部通过。

## 完成的定义

- [ ] `pnpm test:shared-docs`、`pnpm test:workflow-policy` 全绿；`pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] 同一组输入，改动前后 `shared-docs build` 的输出逐字节相同（报错除外，报错中的文件路径多一层组名）；在 PR 说明中贴出比较方法与结果
- [ ] 仓库中搜不到写死的 `shared-docs/pages`、`shared-docs/source.yaml`（测试中故意构造的旧路径除外）
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写。“How to try it”从 `gh pr checkout` 开始，在一个合成的 `shared-docs/guides/` 上运行 `shared-docs build`

## 不做

- 新增 `guides` 以外的组，以及 web-content 等其他上游：由 SDK Reference 的工作包做。到时 `source.yaml` 还要多一个目录字段。
- dev 中记录文件与 `active.json` 的路径：WP9 定。

## 已知的坑

- 报错位置是需求测试的一部分（`spec/coverage.test.ts` 按错误码查用例），改路径时要连同 `fixtures/**/expected.json` 一起改，不能只改代码。
- `shared-docs-validate` 在 PR 没有改到 `shared-docs/` 时直接成功。按组运行之后，这条快捷路径要保留。
- 要另起进程的测试，按 [#824](https://github.com/zilliztech/zdoc/pull/824) 设 120 秒的文件级时限。
