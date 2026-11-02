# WP12 上游更新：发现、影响报告与滚动 PR

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1b　**依赖**：[WP11 #921](https://github.com/zilliztech/zdoc/pull/921)、[WP9b #960](https://github.com/zilliztech/zdoc/pull/960) 已合并。

**状态（2026-11-02）**：WP12-A 已完成技术验收，代码 head [`68151311f`](https://github.com/zilliztech/zdoc/commit/68151311fafa25710b6f9c7c3a18f96cb522c0ec)，[上游 PR #1027](https://github.com/zilliztech/zdoc/pull/1027) 审阅中；WP12-B 未启动。整个 WP12 尚未完成，所有需求 pending 编号保留。实现和验证结果见[走读](../walkthroughs/WP12-A.md)。

## 目标

Guides 的上游原文或依赖变化时，形成可审核的更新 PR 和影响报告；只推进 next，不直接发布，失败时已采用版本仍有效。本卡先覆盖 Guides，Rust 手册级策略等 R1 配置契约稳定后单独补齐，WP12 总体状态保留该后续项。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 7 全文；场景 6、8 | 更新行为、通道变换、提升与锚点 |
| [技术设计 06](../../design/06-upstream-changes.md) | 全文 | 发现、滚动 PR、依赖页合并、失败处理 |
| [技术设计 04](../../design/04-channels-and-lock.md) | 来源配置、lock、快照、提升与标题改名 | 固定输入和 WP13 的边界 |
| [技术设计 05](../../design/05-publish-handoff.md) | PR 校验与触发时机 | 候选权限及合并后的采用路径 |
| [实现指南](../README.md) | 第 2、5、6 节 | fixture、验证层次、协作与 PR 格式 |

先读 zdoc README、适用 AGENTS 和实时测试/分支归属矩阵；有 CodeGraph 时先用它定位实现。核查当前 master，不仅依据历史计划。

## 范围

### 分阶段交付

| 阶段 | 内容 | 状态与停止点 |
|---|---|---|
| A：变化分析与报告 | 固定输入身份；原文、依赖和实际 Cloud 输出比较；锚点关系；采用单元；JSON/Markdown；只读生成观察 | 已技术验收，进入 PR 审阅；不写 lock，不做外部事务 |
| B：自动更新流程 | 定时/手动发现；认证生命周期快照；只推进 next；滚动 PR、依赖合组、保留人工编辑、并发和恢复；校验工作流 | 尚未启动；先交精确计划、权限和验证矩阵给主会话审定 |

### A 的允许路径

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

### B 的计划交付

固定最新 master，细化 B 的精确路径、code-to-test selector、GitHub API 身份、权限、并发及失败恢复策略；明确默认只报告的 rollout 和真实外部 smoke。计划经主会话审定后才实施，不因 A 通过而自动获得 workflow、Base/dev、上传或付费翻译权限。

### B 可提议的范围（须由计划细化后批准）

| 可以提议改动 | 不在范围 |
|---|---|
| shared-docs 的 core/adapters/commands、CLI 注册、测试和 fixture 构建器的删除支持 | 手改 requirements.json、真实 page.yaml/lock、既有 golden 输出 |
| 专用上游更新 workflow/脚本及相关校验接线、最小 GitHub adapter | Fetch/Translation 的生产调度、并发队列、发布和恢复实现 |
| pending/coverage、测试矩阵、必要 package scripts 与 operator README | Base、dev 内容、图片上传、付费翻译、站点 UI、Rust 生成器 |

core 维持纯计算；Git、网络、文件、GitHub 操作经过 adapters。新增外部调用使用最小权限。复用现有通知时要分别界定候选生成无 Cloud 凭据与通知作业权限，计划中说明，不向社区 PR 暴露 secrets。

## 接口

A 已实现的内部类型位于 zdoc 的 [`core/updates/types.ts`](https://github.com/zilliztech/zdoc/blob/68151311fafa25710b6f9c7c3a18f96cb522c0ec/packages/docs-tooling/src/shared-docs/core/updates/types.ts)。调用方通过 adapter 收集固定输入，core 只计算影响、锚点关系与采用单元，输出 JSON/Markdown。WP13 使用同一份固定输入重算，不依赖 PR 正文或易失 artifact。

下表是 WP12 与 WP13 的交接边界；涉及 PR、快照和提升写入的部分仍待 B/WP13 实现：

| 约定 | WP12 上游更新 | WP13 提升 |
|---|---|---|
| 身份 | 用组 + 页面 ID 标识 Guides 更新单元；依赖页可组成同一个 PR | 输入组内页面集合，输出一次提升 PR |
| 基线 | 固定 master SHA、来源仓库/分支及 commit、旧 current/next、表格快照身份 | 固定 master SHA、待提升页面 current/next、通道变换和快照身份 |
| 变化报告 | 源及依赖变化、Cloud 输出变化、被覆盖的源变化、标题/锚点变化与引用位置、生成失败 | 消费或重新计算相同的锚点变化信息；不能只依赖 PR 正文或易失 artifact |
| 不变性 | Guides 只推进 next；生成候选无生产写入 | current 跟随 next；清理通道规则，保留手写 NextChannel，由报告提示人工处理 |
| 幂等 | 相同输入不提交重复变更；同页已有 PR 则更新；依赖页合并不能制造重叠 PR | 无有效变化不创建空 PR；明确报告不存在或无需提升的输入 |
| 并发 | 推送前核对远端 base/head；保护审核人修改；不 force-push | 同样核对远端；提升合并后 WP12 按新基线更新仍打开的 PR |
| 安全停止 | 网络/权限/快照不可用不等于页面已删除；无法认证页面状态时不关闭 PR | 无法确定目标、基线或锚点关系时不写生产状态，也不猜测替换 |
| 发布路径 | PR 合并后由现有定时/获准手动 Fetch 与部署采用 | 同左；不新增 master push 自动 Fetch |

## 计划审阅的决定

在 [zdoc #1027](https://github.com/zilliztech/zdoc/pull/1027) 的 A 阶段实现中落实；阶段边界记录在本任务卡，验证结果见[走读](../walkthroughs/WP12-A.md#审阅与验证)。

| 问题 | 决定 |
|---|---|
| 分阶段交付 | A 只做固定输入分析和报告；B 的快照、滚动 PR 与 workflow 另审精确计划 |
| 原文与输出 | 分别报告源/依赖变化与实际 Cloud 输出变化；被替换的原文不能漏报，实际构建失败标记 unknown |
| 锚点与采用单元 | 多义或删除只报告；仅有证据的跨页采用依赖才合组，共用 fragment 本身不强制合组 |
| 提升条件 | SHA 不同，或有待清理的 channel 规则时可提升；仅手写 NextChannel 不构成自动提升。WP13 开工前统一设计 04/09 的等 SHA 旧表述 |
| PR 事务 | 保留人工编辑、普通 merge 祖先、最早 PR 作为 survivor、draft 隔离；B 仍须审竞态、响应丢失、显式校验与失败恢复，不能承诺多 PR 原子更新 |
| 快照与下线 | 不从 effective 快照或陈旧 candidate 推断删除；证据缺失、过期或冲突时保留 PR 并报告。完整 7-9 与 WP14 对接 |
| 机器人身份 | 持久化 manifest 留给 B；验证 schema、尺寸、ref/ancestry、实际 API 身份和摘要，不能只信提交作者字符串 |
| Rust | 等 R1 配置契约稳定后单独细化手册级更新；不计入本次 A 的完成范围 |

## 要覆盖的编号

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

## 完成的定义

- 计划与公共接口经主会话批准；实际变更不超批准范围。
- 逐项测试真实断言行为，编号覆盖通过，仅删除已经覆盖的 pending 编号。
- 跑完整 PR diff 的 selector 联集、shared-docs、workflow-policy、typecheck、diff check；必要真实回放按 zdoc README/矩阵执行。未跑、跳过、不同 checkout 的结果明确注明。
- 固定源和候选生成证明旧页面不受无关变更影响；验证真实 GitHub 接线的外部操作另行取得授权，不以模拟 API 冒充真实运行。
- 按实现指南格式提供 PR 草稿及精确 head SHA 的交接包；主会话独立 review 后再决定提交与发布动作。

## 不做

不手工升级生产 lock 来演示，不修改 Base，不做 WP13 提升、WP14 下线或 WP15 恢复。设计中的合并后采用仍走现行 Fetch/部署路径，不增加 master push 自动 Fetch。

## 已知的坑

- 完成 A 不等于完成 7-1～7-10/T05；只删除端到端满足的 pending 编号，本次 A 全部保留。
- 缺失 raw 变量与实际 Cloud 构建失败不是同一件事；隐藏原文失败不能中断有效页面的报告。
- 图片字节变化可能不改 Markdown；要记录实际读取来源和摘要，不能只检查源文件文本。
- 远端状态不明时停止，不通过 force-push、盲目重试或关闭 PR 来消除不确定性。
