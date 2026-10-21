# 08 工作流与权限

对应的产品需求见[产品需求场景 3](../prd.md#场景-3接入一页)、[7](../prd.md#场景-7审核上游更新)、[8](../prd.md#场景-8功能上线时提升)、[9](../prd.md#场景-9从飞书切换到-git激活)，以及[第 6 节](../prd.md#6-对现有能力的要求)中的“发布保护”。本篇汇总 Phase 1 在 zdoc 中新增或改动的 GitHub 工作流：各自怎样触发、以什么身份运行、有哪些权限、怎样排队、失败时通知谁。各工作流的业务规则仍在对应的篇目中定义。

**参与方**：zdoc 维护者（实现与仓库配置）。

**状态**：草稿，待工程维护者确认。依据 zdoc master [`b832f16`](https://github.com/zilliztech/zdoc/tree/b832f16cd) 中现有的 `fetch-docs.yml`、`fetch-guides-requested.yml` 与 `sync-master-tooling-to-dev.yml`；工作流名称为建议，可以改。

## 约定

### 现有做法

新工作流沿用 zdoc 已有的三种做法：

| 做法 | 现在在哪里用 |
|---|---|
| 所有写 dev 的工作流共用并发组 `docs-production-dev`，排队执行 | `fetch-docs.yml`、`fetch-guides-requested.yml`、`sync-master-tooling-to-dev.yml` |
| 用 `GITHUB_TOKEN` 开 PR，再用 `gh workflow run` 显式触发校验并等待结果 | `sync-master-tooling-to-dev.yml` |
| 运行进度与失败用飞书卡片通知（`docs-tooling report-card`） | `fetch-docs.yml` |

Fetch 已有的手动参数中，`media_upload_mode`（`write` / `skip`）、`publish`、`target_branch`、`source_ref`、`tooling_ref` 直接用于候选运行与激活。

### 工作流一览

| 工作流（建议名称） | 触发 | 权限 | 并发组 | 写什么 | 见 |
|---|---|---|---|---|---|
| `shared-docs-lock` 接入时写 lock | `pull_request`：`shared-docs/pages/**` 变化 | `contents: write`、`actions: write` | 每个 PR 一组 | 向 PR 分支提交 `lock.yaml`，再触发 `shared-docs-validate` | [04](./04-channels-and-lock.md#接入一页) |
| `shared-docs-validate` PR 校验 | `pull_request`：`shared-docs/**` 变化；`workflow_dispatch`：工具推送后显式触发 | `contents: read`；不读任何 secret | 每个 PR 一组，新运行取消旧运行 | 不写；结果作为 PR 的检查项 | [05](./05-publish-handoff.md#pr-校验) |
| `shared-docs-upstream` 上游更新 | `schedule` 每天一次；`workflow_dispatch`，可填页面与目标提交 | `contents: write`、`pull-requests: write`、`actions: write` | `shared-docs-master-pr` | 推送分支，开、更新或关闭上游更新 PR，触发校验 | [06](./06-upstream-changes.md#发现与运行) |
| `shared-docs-promote` 提升 | `workflow_dispatch`：填页面标识或 `all-pending` | 同上 | `shared-docs-master-pr` | 开一个 PR，触发校验 | [04](./04-channels-and-lock.md#lockyaml-怎样变化) |
| 比较 | `workflow_dispatch`：填页面标识 | `contents: read`；读飞书需要的凭据与 Fetch 相同 | 无 | 不写 dev；差异与激活前的检查结果写进运行摘要与可下载的产物 | [05b](./05b-cutover-and-ownership.md#切换与激活) |
| Fetch（改动） | 现有的每天 3 次与手动；`shared-docs/` 合并到 master 后是否新增触发待确认 | 不变 | `docs-production-dev` | 新增“生成共享页”步骤；按飞书表格写 `active.json` | [05](./05-publish-handoff.md#交接发生在哪里)、[05b](./05b-cutover-and-ownership.md) |

激活和下线不是工作流：都在飞书表格中操作，下一次 Fetch 生效（见 [05b](./05b-cutover-and-ownership.md)）。

- **比较的形式**：做成 Fetch 的新参数，还是单独的工作流，由 zdoc 维护者确定（见[Phase 1 实施计划第 6.1 节](../phase-1.md#61-待确认的接口)）。
- **读飞书表格**：`shared-docs-validate` 不读 secret，需要表格中的 placement type 与 `Release Channel` 时，读 dev 中的 `packages/docs-tooling/src/lark/meta/snapshots/guides-uat-last-success.json`（Fetch 保存的表格快照，格式见 [04](./04-channels-and-lock.md#只在一个通道存在的页面)）与 `active.json`；上游更新与提升在仓库自己的上下文中运行，同样读快照即可，不必直接调用飞书。
- **`shared-docs-master-pr` 并发组**：上游更新与提升都改 master 上的 `lock.yaml`，放进同一组排队，避免同时为同一页开出冲突的 PR。它们不写 dev，所以不进 `docs-production-dev`。
- **用 `GITHUB_TOKEN` 推送的提交不会自动触发其他工作流**，凡是工具推送的提交，都用 `gh workflow run shared-docs-validate` 显式触发并等待结果，与 `sync-master-tooling-to-dev.yml` 相同。

### 权限与发布保护

发布保护各环节的要求见 [05](./05-publish-handoff.md#发布保护)。落到仓库配置上：

| 要求 | 仓库配置 |
|---|---|
| 修改 `shared-docs/` 必须经 PR 审核，校验不过不能合并 | master 分支保护：要求 PR、要求审核、把 `shared-docs-validate` 设为必需的检查项。必需检查项不能按路径区分，所以没有改 `shared-docs/` 的 PR 也要运行它，并立即通过 |
| 工作流和校验器的改动需工程审核 | `CODEOWNERS` 中 `.github/workflows/` 与生成工具的代码归 zdoc 维护者，master 分支保护要求代码所有者审核 |
| 普通作者不能直接写 dev | 沿用现有 dev 分支保护，只允许工作流写入 |
| 候选运行没有生产写权限 | `shared-docs-validate` 与比较只有 `contents: read`，不读取图片存储、飞书等任何 secret |
| 社区 PR 不需要 Cloud 凭据 | 只用 `pull_request` 触发，不用 `pull_request_target`；来自 fork 的 PR 拿不到写权限与 secret，`shared-docs-lock` 不写入，在 PR 中提示改从仓库内的分支提交 |
| 只有文档负责人能激活 | 飞书表格的权限设置：只有文档负责人能修改 placement type；修改记录留在表格历史与 `active.json` 的提交历史中 |
| 只有对 zdoc 有写权限的人能运行提升与比较 | GitHub 对 `workflow_dispatch` 的默认限制，无需额外配置 |

### 仓库准备

一次性配置，由 zdoc 维护者在上线前完成：

- 按上表设置 master 分支保护与 `CODEOWNERS`。
- 在飞书表格的 placement type 中加入表示 Git 的新值，并设置谁能修改。
- 把新增的代码与工作流路径登记到 zdoc 的代码与测试对照表（`scripts/docs-workflow/test-matrix.json`），运行 `pnpm test:for-change` 确认没有遗漏；`shared-docs/` 默认归 master，`deploy/contracts/master-tooling-sync.json` 不用改。
- 确认仓库设置允许 `GITHUB_TOKEN` 创建 PR（Settings → Actions → Workflow permissions），`sync-master-tooling-to-dev.yml` 已依赖这一设置。

### 失败通知

| 工作流 | 怎样算失败 | 通知 |
|---|---|---|
| `shared-docs-validate` | 校验不通过 | PR 的检查项失败，摘要中写明原因与应改的文件；不另行通知 |
| `shared-docs-lock`、`shared-docs-upstream`、`shared-docs-promote` | 工作流本身出错，如网络问题、无法推送 | 飞书卡片，沿用 `report-card`；上游更新在下一次定时运行时自动重试 |
| `shared-docs-upstream` | 生成失败（如命名块被删） | 不算工作流失败：照样开 PR，校验标为失败，见 [06](./06-upstream-changes.md#出错时) |
| `shared-docs-promote` | 部分页面不符合条件 | 运行摘要中列出，其余页面照常进入 PR |
| 比较 | 检查不通过或运行出错 | 运行摘要写明原因 |
| Fetch | 现有规则 | 现有的飞书卡片 |
| Fetch（共享页） | 标为 `git` 的页面检查不通过；placement type 被改回；表格标为 `git` 但没有页面目录；记录已删、目录还在 | 飞书卡片通知文档负责人或文档工程师；前三种这一页保留现有版本，最后一种只提示删除目录 |
| Fetch（图片） | 已记录的图片在原地址的内容变了 | 飞书卡片通知文档工程师，不阻断 |

## 出错时

各工作流的业务出错规则见上表“见”一列中的篇目；错误码见 [09](./09-error-catalog.md)。

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么不新建机器人账号或 GitHub App。** `sync-master-tooling-to-dev.yml` 已经用 `GITHUB_TOKEN` 开 PR、显式触发校验并等待结果，照搬即可。代价是工具推送的提交不会自动触发校验，要显式触发。

**为什么激活不做成工作流。** Phase 1 导航与整页通道本来就在飞书表格中维护，文档负责人在同一处改 placement type，与其他页面一致；不用另建 GitHub 环境审批。代价是表格的修改没有 PR 审核，由 Fetch 的检查与 `active.json` 的对比兜底（见 [05b](./05b-cutover-and-ownership.md#设计理由)）。

**为什么只用 `pull_request`。** `pull_request_target` 会让来自 fork 的 PR 在有写权限和 secret 的上下文中运行，社区 PR 就可能拿到 Cloud 凭据。

为什么定时检查上游，见 [06](./06-upstream-changes.md#设计理由)。

</details>

## 验收

- **T12**：完整旅程；没有权限的候选任务不能写生产。
- **发布保护**：实际的 Git 服务端拒绝普通作者直接推送或强推正式生成分支；内容 PR 不能关闭核心检查。
