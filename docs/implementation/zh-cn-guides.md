# 中文 Guides 工程实施计划与任务拆解

**状态**：已定稿，启动实施（2026-11-26）· **方案依据**：[中文 Guides 翻译方案（对齐稿）](../prd/zh-cn-guides.md) · **技术契约**：[11 中文 Guides 翻译与发布](../design/11-zh-cn-translation-pipeline.md)

本文定义中文 Guides 翻译与发布流水线在 [zdoc](https://github.com/zilliztech/zdoc) 中的工程拆包、依赖顺序、去阻塞策略以及 **Controller（决策与审阅）+ Claude Opus（工程实施）** 协作规约。

---

## 1. 协作模式与一卡一 PR 铁律

- **分工**：
  - **Controller（Coordinator）**：负责任务卡拆解与接口锁定、派发实施、对每个工作包做深度 Code Review（逻辑、权限边界、`zdoc` 契约与测试矩阵覆盖）、协调关键架构取舍并向推动者汇报。
  - **实现 Worker（Claude Opus）**：在独立工作副本（`share` worktree）中严格按单张任务卡实现代码与测试，不越界修改其他工作包或生产发布路径，交付前自跑任务卡规定的全部检查命令。
- **一卡一 PR**：每个工作包对应 `zdoc` `master` 上的一个独立 PR；未通过 Controller 审阅与 `pnpm test:for-change` 返回的全部测试集合，不得合入。
- **不阻塞原则**：阶段 0、1、2 与阶段 3 的纯核心逻辑（`ZH-WP6a`）**完全不依赖**涂文家正在进行的英文 Fetch `record_id` 改造；做完阶段 2 即可启动「3 存量 + 1 新增」只读试点与首批存量底稿建仓，仅最后 `ZH-WP6b`（Fetch 入口接线与真实回放）在合入前对齐涂文家新架构的 Base 字段即可。

---

## 2. 工作包总览与依赖关系

```text
阶段 0（前置底座，可并行）
  ZH-WP0a (<UI> 组件与白名单) ─────────────────────────────┐
  ZH-WP0b (zh-CN-common.json 术语底座) ────────────────────┤
                                                           ▼
阶段 1（离线核心引擎，零发布链耦合）
  ZH-WP1 (localized-docs Schema + 英文剥壳 + md2md 组装) ──► ZH-WP2 (增量 Diff / 三档代码保护 / 受限起草 CLI)
                                                           └──► ZH-WP3 (飞书存量底稿一次性导入 CLI)
                                                                       │
阶段 2（工作流、PR 门禁与只读试点）                                      ▼
  ZH-WP4 (PR 候选检查工作流 + CODEOWNERS) ─────────────────► ZH-WP5 (08:00 调度 + 滚动 PR + 飞书日报卡片)
                                                                       │  ← 此时可启动 3+1 只读试点与存量建仓
阶段 3（中文 Fetch 切流与真实回放）                                      ▼
  ZH-WP6a (独立中文路由 / active.json / md2md 渲染核心，不强绑 record_id)
       │  （对齐涂文家新架构 Base 字段）
       ▼
  ZH-WP6b (中文 Fetch 入口接线 + Promote 交接 + 真实保留产物隔离回放验收)
```

| 编号 | 名称 | 核心范围 | 依赖 | 状态 | 任务卡 |
|---|---|---|---|---|---|
| **ZH-WP0a** | `<UI>` 组件与白名单 | `packages/docs-ui` 全局 `<UI>` 组件 + `shared-docs` `compatibilityTags` 白名单 | 无 | **已合并**（[#1503](https://github.com/zilliztech/zdoc/pull/1503)） | [ZH-WP0a](./tasks/ZH-WP0a-ui-component.md) |
| **ZH-WP0b** | 全站统一中文术语底座 | `zh-CN-common.json` + `localeContract.js` `extends` 合并 + 薄壳 `zh-CN-guides.json` + `promptContractSha256` 联动 | 无 | **已合并**（[#1502](https://github.com/zilliztech/zdoc/pull/1502)） | [ZH-WP0b](./tasks/ZH-WP0b-zh-cn-common-glossary.md) |
| **ZH-WP1** | `localized-docs` 核心与 `md2md` 组装 | `page.yaml`/`.baseline.json`/`Variables.json` Schema、剥离 `dev` 英文壳子、`<UI>` 提取、`@zilliz/mdtomd` 组装与离线 `check`/`build` CLI | ZH-WP0a | **待合并**（[#1507](https://github.com/zilliztech/zdoc/pull/1507)） | [ZH-WP1](./tasks/ZH-WP1-localized-docs-core.md) |
| **ZH-WP2** | 增量 Diff、代码保护与受限起草 CLI | 确定性分段 diff、未涉及段落逐字校验、代码块三档同步、`<UI>` 与疑点清单、新页首译 vs 基线缺失阻塞、受限 LLM 适配器 | ZH-WP0b, ZH-WP1 | **待启动（第二批，可并行）** | [ZH-WP2](./tasks/ZH-WP2-incremental-draft-cli.md) |
| **ZH-WP3** | 飞书存量底稿一次性导入 CLI | 从固定飞书修订剥离壳子生成 `source.md`，对照最新 `dev` 英文辅助补齐历史欠译并产出导入 PR 素材 | ZH-WP1, ZH-WP2 | 待拆卡 | — |
| **ZH-WP4** | PR 候选检查工作流与分支保护 | 新增只读候选检查工作流（`md2md` 预处理 + 双通道/MDX 检查 + 待确认项清零门禁 + 预览产物）、文档团队 `CODEOWNERS` 与策略守卫 | ZH-WP1 | **待启动（第二批，可并行）** | [ZH-WP4](./tasks/ZH-WP4-pr-validation-workflow.md) |
| **ZH-WP5** | 定时调度工作流与飞书日报 | `translate-zh-guides.yml`（08:00 定时 + 手动按页）、按页滚动 PR、`deferred`/`paused` 规则、复用 `report-card` 推每日 PR 与 `manual` 去重汇总卡片 | ZH-WP2, ZH-WP4 | 待拆卡 | — |
| **ZH-WP6a** | 中文路由与激活核心（解耦 `record_id`） | `localized-docs/core/handoff/` 纯逻辑：`site=zh-CN` 路由互斥、按 `page_id`/`page url` 绑定激活态与回退基线、`OWNERSHIP_CONFIG_MISSING`/`OWNERSHIP_REVERTED`、独立凭据 schema 与 Promote 解包 | ZH-WP1 | **待启动（第二批，可并行）** | [ZH-WP6a](./tasks/ZH-WP6a-handoff-core.md) |
| **ZH-WP6b** | 中文 Fetch 入口接线与真实回放 | 将 `ZH-WP6a` 接入中文 Fetch 入口与 Promote 交接，补齐 `test-matrix.json`，完成 `publish=false` 预检与隔离 bare remote 真实保留产物回放 | ZH-WP6a（并对齐英文 Fetch 新架构 Base 字段） | 待拆卡 | — |

---

## 3. 通用质量与仓库门禁（所有工作包必须遵守）

1. **路径与测试矩阵**：每张 PR 修改或新增的 `zdoc` 路径都必须运行 `pnpm test:for-change -- <changed-path>...`；若出现未映射路径，必须在同一 PR 补齐 `scripts/docs-workflow/test-matrix.json` 并运行 `pnpm test:workflow-matrix` 与 `pnpm test:workflow-policy`。
2. **核心与适配器隔离**：`packages/docs-tooling/src/localized-docs/core/` 保持纯计算，不依赖 `lark/`、网络或文件系统；`lark/` 与飞书交互只能通过 `adapters/` 接入。
3. **分支所有权铁律**：严禁在 `master` 手改 `deploy/contracts/master-tooling-sync.json` 中的 `devOwnedPaths`（如 `content/`、`i18n/`、`generated/`）；所有中文配置与 `source.md` 均维护在 `master:localized-docs/zh-CN/guides/`。
4. **审阅交接格式**：每个工作包完成后，Worker 须提交改动清单、精确验证命令与输出摘要、以及“未覆盖项/风险说明”，由 Controller 复核后再决定是否提 PR 或合入。
