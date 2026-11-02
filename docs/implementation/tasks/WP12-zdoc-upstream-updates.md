# WP12 上游更新：发现、影响报告与滚动 PR

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1b。依赖 WP11 #921、WP9b #960 已合并。

**状态（2026-11-02）**：WP12-A 已完成技术验收，代码 head `68151311fafa25710b6f9c7c3a18f96cb522c0ec`，[上游 PR #1027](https://github.com/zilliztech/zdoc/pull/1027) 审阅中；WP12-B 未启动。整个 WP12 尚未完成，所有需求 pending 编号保留。见[验收记录](../reviews/WP12-A.md)和[走读](../walkthroughs/WP12-A.md)。

## 目标

Guides 的上游原文或依赖变化时，形成可审核的更新 PR 和影响报告；只推进 next，不直接发布，失败时已采用版本仍有效。本卡先覆盖 Guides，Rust 手册级策略等 R1 配置契约稳定后单独补齐，WP12 总体状态保留该后续项。

## 要读的

| 文档 | 章节/用途 |
|---|---|
| [产品需求](../../prd.md) | 场景 7 全文；场景 6 的通道变换；场景 8 的提升与锚点 |
| [技术设计 06](../../design/06-upstream-changes.md) | 发现、滚动 PR、依赖页合并、失败处理 |
| [技术设计 04](../../design/04-channels-and-lock.md) | 来源配置、lock、快照、提升与标题改名 |
| [技术设计 05](../../design/05-publish-handoff.md) | PR 候选权限与触发时机 |
| [共享接口约定](../wp12-wp13-contract.md) | 必须回答的七项问题 |
| [实现指南](../README.md) | fixture 构建器、验证层次、代码与 PR 规则 |
| [协作约定](../coordination.md) | 分发阶段、裁决与交接 |

先读 zdoc README、适用 AGENTS 和实时测试/分支归属矩阵；有 CodeGraph 时先用它定位实现。核查当前 master，不仅依据历史计划。

## 分阶段交付

| 阶段 | 内容 | 状态与停止点 |
|---|---|---|
| A：变化分析与报告 | 固定输入身份；原文、依赖和实际 Cloud 输出比较；锚点关系；采用单元；JSON/Markdown；只读生成观察 | 已技术验收，进入 PR 审阅；不写 lock，不做外部事务 |
| B：自动更新流程 | 定时/手动发现；认证生命周期快照；只推进 next；滚动 PR、依赖合组、保留人工编辑、并发和恢复；校验工作流 | 尚未启动；先交精确计划、权限和验证矩阵给主会话审定 |

A 的可改路径如下，均相对于 zdoc 根目录。计划和验证证据不混入实现 PR：

- `packages/docs-tooling/src/shared-docs/core/updates/types.ts`
- `packages/docs-tooling/src/shared-docs/core/updates/impact.ts`
- `packages/docs-tooling/src/shared-docs/core/updates/anchors.ts`
- `packages/docs-tooling/src/shared-docs/core/updates/units.ts`
- `packages/docs-tooling/src/shared-docs/adapters/update-inputs.ts`
- `packages/docs-tooling/src/shared-docs/adapters/build-page.ts`（仅可选只读观察，默认结果与失败行为不变）
- `packages/docs-tooling/src/shared-docs/testing/updates/impact.test.ts`
- `packages/docs-tooling/src/shared-docs/testing/updates/anchors.test.ts`
- `packages/docs-tooling/src/shared-docs/testing/updates/units.test.ts`
- `packages/docs-tooling/src/shared-docs/testing/build/build.test.ts`
- `packages/docs-tooling/src/shared-docs/fixtures/updates/scenarios.json`
- `packages/docs-tooling/src/shared-docs/fixtures/updates/SOURCE.md`
- `packages/docs-tooling/src/shared-docs/fixtures/milvus-docs/build.ts`
- `packages/docs-tooling/src/shared-docs/fixtures/milvus-docs/build.test.ts`
- `packages/docs-tooling/src/shared-docs/README.md`（只记录 A 已实现的内部接口）


B 不能直接沿用下面的总体范围开工。下线证据缺失不能推断删除；完整 7-9 还需与 WP14 对接。Rust 手册级更新待 R1 契约稳定后单独细化，不计入已验收的 A。

## 下一阶段计划交付

固定最新 master，细化 B 的精确路径、code-to-test selector、GitHub API 身份、权限、并发及失败恢复策略；明确默认只报告的 rollout 和真实外部 smoke。计划经主会话审定后才实施，不因 A 通过而自动获得 workflow、Base/dev、上传或付费翻译权限。

## 拟实现范围（须由计划细化后批准）

| 可以提议改动 | 不在范围 |
|---|---|
| shared-docs 的 core/adapters/commands、CLI 注册、测试和 fixture 构建器的删除支持 | 手改 requirements.json、真实 page.yaml/lock、既有 golden 输出 |
| 专用上游更新 workflow/脚本及相关校验接线、最小 GitHub adapter | Fetch/Translation 的生产调度、并发队列、发布和恢复实现 |
| pending/coverage、测试矩阵、必要 package scripts 与 operator README | Base、dev 内容、图片上传、付费翻译、站点 UI、Rust 生成器 |

core 维持纯计算；Git、网络、文件、GitHub 操作经过 adapters。新增外部调用使用最小权限。复用现有通知时要分别界定候选生成无 Cloud 凭据与通知作业权限，计划中说明，不向社区 PR 暴露 secrets。

## 行为与编号

| 编号 | 必须证明 |
|---|---|
| 7-1 | 每日检查及手动指定页/提交；固定输入处理一天内多次提交 |
| 7-2、7-3 | 更新只入 PR、Guides 只改 next；候选不写 dev；合并后的 UAT/Prod 视图分别正确 |
| 7-4、7-6 | 单页滚动 PR、暂缓互不阻塞；保留人工修改，避免重复 PR |
| 7-5 | 互相依赖的页同 PR；覆盖从独立 PR 转为依赖集合的情况 |
| 7-7 | 无关变化不改 lock；源被 Cloud 替换但自身变化仍进入复核报告；重复运行无新提交 |
| 7-8 | 提升后的新 current/next 被下一次运行读取，更新仍打开的 PR |
| 7-9 | 认证快照中的退役/删除停止更新并关闭相应 PR；快照缺失或读取失败不误判删除 |
| 7-10 | 社区 PR 不运行 zdoc 生产逻辑、不获取 Cloud 凭据 |
| T05 | 块改名/删除、lines 失配、源文件删除/改名均给出失败报告；旧采用版本不变 |

补充：历史改写、网络失败、PR 创建成功但响应丢失、校验触发失败、远端并发更新，都有确定的恢复或停止策略。上下文报告按设计给完整代码组/块上下文，不只报摘要不同。

## 完成的定义（实现阶段）

- 计划与公共接口经主会话批准；实际变更不超批准范围。
- 逐项测试真实断言行为，编号覆盖通过，仅删除已经覆盖的 pending 编号。
- 跑完整 PR diff 的 selector 联集、shared-docs、workflow-policy、typecheck、diff check；必要真实回放按 zdoc README/矩阵执行。未跑、跳过、不同 checkout 的结果明确注明。
- 固定源和候选生成证明旧页面不受无关变更影响；验证真实 GitHub 接线的外部操作另行取得授权，不以模拟 API 冒充真实运行。
- 按实现指南格式提供 PR 草稿及精确 head SHA 的交接包；主会话独立 review 后再决定提交与发布动作。

## 已知边界

不手工升级生产 lock 来演示，不修改 Base，不做 WP13 提升、WP14 下线或 WP15 恢复。设计中的合并后采用仍走现行 Fetch/部署路径，不增加 master push 自动 Fetch。
