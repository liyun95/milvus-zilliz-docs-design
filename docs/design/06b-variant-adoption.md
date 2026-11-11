# 06b 未合并上游 PR 的采纳（variant）

Milvus 与 Cloud 趋于同步发布，“上游先合并、Cloud 再跟进”的时间差不再成立：需要 Cloud 先发布的修改，可能还只是一个未合并的 milvus-docs PR。本篇定义这种情况的通道：把上游 PR 的原文**采纳（adopt）**为页面目录中的 **variant 覆盖文件**，以 Zilliz 自有内容的身份先进入 UAT，需要时进入生产；上游合并后**对账（reconciliation）**：删除 variant、把 lock 重新钉到 merge commit，内容身份转回共享。lock 本身不动，仍只记跟踪分支上的 commit（见 [04](./04-channels-and-lock.md)）；variant 是它旁边的一层按通道覆盖。

**参与方**：milvus-docs 的未合并 PR（内容来源）、zdoc 中的采纳工作流（抓取一次、写文件、开 PR）、Cloud 文档工程师（评审采纳 PR、发起对账）、每日巡检（watchdog，报告 pin 漂移与 variant 健康）。

对应的产品需求见[产品需求场景 7](../prd.md#场景-7审核上游更新)（上游 PR 未合并时的补充通道）。

**状态**：已定义，待文档负责人确认。zdoc 实现进行中，见[Phase 1 实施计划第 6.1 节](../phase-1.md#61-待确认的接口)。

## 约定

### 文件布局与规则

采纳写进页面目录，与 `page.yaml`、`lock.yaml` 同级，不建子目录：

```
shared-docs/guides/pages/<页面标识>/
  page.yaml
  lock.yaml
  variant-next.md                        # 覆盖 next（UAT）读到的原文；可以单独存在
  variant-next.provenance.json           # 采纳来源记录，工具写入
  variant-current.md                     # 覆盖 current（Prod）读到的原文；必须伴随 variant-next.md
  variant-current.provenance.json        # 仅 --promote 后存在
```

| 文件 | 规则 |
|---|---|
| `variant-next.md` | 字节与上游 PR head 中该页 `source.file` 的内容逐字相同；单独存在 = 只在 UAT 预览 |
| `variant-current.md` | 与 `variant-next.md` 同字节；必须有 `variant-next.md` 伴随——生产不能超前 UAT |
| `variant-<channel>.provenance.json` | 每个内容文件旁一份，字段固定为 `pull`（PR 号）、`head_sha`（完整的 40 位）、`adopted_at`，可选 `adopted_via`；多余或缺字段都算错 |

- variant 文件由采纳工作流写入，人不手改，与 lock 相同（见 [04](./04-channels-and-lock.md#lockyaml-怎样变化)）。要改内容，改上游 PR 后重新采纳；Cloud 自己的差异仍写在页面配置与 Cloud 内容文件中。
- **lock 不变。** 生成时先按 lock 完成全部校验，之后才用 variant 覆盖对应通道读到的原文；pin 失效时该页照样失败，variant 不救。lock 的校验规则（commit 在跟踪分支的历史上等）一条不改。
- 覆盖只替换原文来源：命名块、变换、变量、链接等适配照常发生。片段、变量与图片仍从 lock 钉住的 commit 解析；PR 中新增而 pin 中没有的依赖，会让生成失败。
- 没有 variant 文件时，行为与从前完全一致。

### 采纳

需要同步发布、上游 PR 还没合并时：

1. **手动触发采纳工作流**，填页面标识与 PR 号，可选先空跑（`--dry-run`）只看会写什么。工作流先查同页同 PR 是否已有未合并的采纳 PR（单飞），再从运行被触发时钉住的 master 执行，最终只提交这一页的 variant 文件，不带其他改动。
2. 命令**抓取一次** `refs/pull/<PR>/head`（浅取进临时目录，这是整个机制里唯一的 PR 抓取），按 `page.yaml` 的 `source.file` 取出原文，写入 `variant-next.md` 与 provenance。指定了预期 head（`--ref`）而 PR 已移动时中止。同一 PR 重复采纳：内容相同报 Unchanged，只刷新 `adopted_at`；内容变了按新 head 重写。
3. 工作流用专用 PAT 从分支 `shared-docs-adopt/<页面标识>-p<PR>` 开 master PR。PAT 开的 PR 自动触发校验（区别于 `GITHUB_TOKEN`，见 [05](./05-publish-handoff.md#pr-校验)），对 PR 树全量生成一遍——这次运行就是采纳的证据。PAT 未配置时中止且不直接推送，改动留在运行中。
4. **评审合并。这是采用批准本身**：未合并的上游内容以 Zilliz 自有编辑内容的身份进入，由这个 PR 把关，不是自动采用；允许它进入生产是 2026-11-11 的负责人决定。合并后照常触发 Fetch，UAT 显示采纳内容——与 lock 两版本的差异一样按块包进 `<NextChannel>`，Prod 保持已上线版本（合并规则见 [04](./04-channels-and-lock.md#两个版本怎样合并成一页)）。

### Zilliz 先发布（promote）

Cloud 的发布窗口到点、上游 PR 还没合并时，再次触发采纳工作流并选 promote：补写同字节的 `variant-current.md`。两个通道的输出从此逐字相同、不带通道标记（与提升后的状态相同），下一次生产构建把采纳内容送进 Prod。lock 仍不动：Prod 与 UAT 读的 commit 没变，变的只是这两个 commit 之上叠了一层 Zilliz 自有的覆盖。

### 上游先合并：对账

上游 PR 合并后，内容身份要从“Zilliz 自有”转回“共享”：

- 人工开**对账 PR**：删除这一页的 variant 文件（内容与 provenance），把 lock 的 `current`、`next` 重新钉到 merge commit。merge commit 在跟踪分支上，之后完全回到 04 与 06 的既有机制。
- Cloud 在采纳期间做过的修改，转成页面配置中的 transform，或先回馈上游再对账。
- 巡检在“上游已合并、variant 还在”时提示对账，并附 variant 与上游 tip 的差异预览。不自动对账。

### 再次采纳

上游 PR 在采纳后又有新提交：重跑采纳即可。内容相同 → Unchanged；内容变化 → 按新 head 重写，`head_sha` 随之更新。要不要追，由 Cloud 判断；巡检只报告 head 漂移。

### 每日巡检（watchdog）

新增一个只读的巡检工作流，每天定时（04:47 UTC）或手动运行，逐页报告三类状态：

| 检查 | 内容 | 级别 |
|---|---|---|
| pin 漂移 | lock 的 `next` 之后，跟踪分支上这一页的原文有没有新提交 | 信息 |
| pin 健康 | pin 是否还在跟踪分支的历史上、原文文件是否还存在 | 不健康时红 |
| variant 健康 | 逐个 variant 查上游 PR 实况：head 漂移、已合并未对账（附差异摘要）、已关闭；PR 状态查不到 | 前三项信息；查不到时红 |

- 卡片只在有不健康项（pin 失效、variant 状态不可得）或运行出错时才红。漂移与待对账是信息，不告警：pin 失效意味着下一次 Fetch 会静默把这一页退回基线，必须立刻处理；待对账只是还没做完的事。
- 报告（JSON 与 Markdown）作为 artifact 保留 14 天，摘要里有一个逐日稳定的 digest，供运维日报做日间对比。

### 范围与限制

- 只覆盖已接入的页面。上游 PR 新增整页时仍走现有路径：先在飞书维护，上游合并后按 [04](./04-channels-and-lock.md#接入一页) 接入转共享。
- 不改 lock 的 schema 与语义；生成期不抓 `refs/pull`（采纳时的一次是唯一例外）；不做自动 re-pin 与自动对账，对账是人工 PR。
- `<NextChannel>` 包住的内容随生产镜像分发，是既有行为（见 [04](./04-channels-and-lock.md#设计理由)），采纳不改变它。

## 出错时

生成时（在 [04](./04-channels-and-lock.md#出错时) 的规则之上）：

| 情况 | 结果 |
|---|---|
| `variant-current.md` 存在但没有 `variant-next.md` | 该页生成失败 |
| variant 内容文件为空；provenance 缺失、字段不对或 `head_sha` 不是完整的 40 位 | 该页生成失败 |
| 只有 provenance，没有对应的内容文件 | 该页生成失败 |
| variant 依赖的片段、变量或图片在 pin 的 commit 中不存在 | 该页生成失败 |

采纳工作流：

| 情况 | 结果 |
|---|---|
| 页面标识不是已接入页、没有 lock，或 PR head 中找不到该页的 `source.file` | 中止，不写任何文件 |
| 指定了预期 head（`--ref`）且 PR head 已移动 | 中止并说明 |
| 专用 PAT 未配置 | 中止；改动已提交在运行中，不直接推送 |
| 同页同 PR 已有未合并的采纳 PR | 不重复执行（单飞） |

巡检：

| 情况 | 结果 |
|---|---|
| 上游 PR 已合并而 variant 还在 | 提示对账，附差异预览（信息） |
| 上游 PR head 漂移，或已关闭 | 报告列出（信息） |
| 上游 PR 状态查不到 | 巡检红 |

## 例子

<details>
<summary>OpenAI 的同步发布（假想）</summary>

Milvus 与 Cloud 同天发布 OpenAI 的模型表更新；milvus-docs 侧的修改还在 PR #4242 中。

| 时间 | 谁触发 | 页面目录 | UAT | Prod |
|---|---|---|---|---|
| 决定同步发布 | 采纳工作流（PR #4242） | 新增 `variant-next.md` 与 provenance，评审后合并 | 模型表新行（`<NextChannel>` gating） | 旧版本 |
| Cloud 发布窗口到点 | 采纳工作流（promote） | 补 `variant-current.md`（同字节） | 新内容，无标记 | 下次构建起为新内容 |
| 上游合并 #4242 | 巡检提示 → 人工对账 PR | 删除 4 个 variant 文件，lock 的 `current`、`next` 钉到 merge commit | 回到共享内容 | 同 |

对账时发现 Cloud 在采纳期间改过一段：先把它转成 `page.yaml` 中的 transform（或回馈上游），再合并对账 PR。记录文件在采纳期间照常记录两个通道的输入，variant 文件及其摘要与来源记在 `inputs.variants` 中（见 [05](./05-publish-handoff.md#记录文件)）。

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么不让 lock 直接钉 PR head。** 给 lock 加一种“PR pin”看起来更省文件，但要为它重定义全部校验：PR pin 只该给 next 用，可“上游合并晚于 Cloud 发布”恰恰要求 current 也能用未合并内容；PR head 会漂移，“commit 在跟踪分支历史上”那套规则得推倒重来；生成期还得常备 `refs/pull` 抓取能力。把未合并内容放进旁边一层文件，lock、校验、抓取全部零改动——PR head 只在采纳那一刻被抓取一次。

**为什么 lock 永远只钉跟踪分支上的 commit。** lock 的语义保持“Prod 与 UAT 各用哪个版本”，全部既有校验（在历史上、祖先关系）原样复用；variant 是 lock 之上的覆盖层，来源记在 provenance 中。pin 失效时该页照常失败，不存在“variant 兜底”。

**为什么文件与上游逐字相同。** 对账时才有干净的比较：variant 与 merge 后的上游逐字 diff 为零，说明内容身份干净地转回共享；Cloud 的差异另走 transform，不混进 variant。适配（变量、命名块、链接）照常发生在构建期，与读 pin 的原文没有区别。

**为什么采纳的闸是人工 master PR。** 对应对齐会“Cloud 不审核 milvus-docs PR，在上游更新 PR 中把关”的结论（[方案总览第 7 节](../proposal.md#7-会议结论2026-10-13)）：未合并的上游内容进 Cloud，同样要经过一个可审核的 PR，而不是工具自动采用。采纳后的内容身份是 Zilliz 自有编辑内容，允许进入生产是 2026-11-11 的负责人决定。采纳 PR 用专用 PAT 开出，自动触发校验（`GITHUB_TOKEN` 开的 PR 不会），全量生成一遍即是证据。

**为什么巡检是定时的、只读的。** 与 [06](./06-upstream-changes.md#设计理由)“定时检查而非事件触发”同理：跨组织没有 webhook，晚几个小时发现不影响大局。巡检只报告；对账是人的决定，不做自动 re-pin bot。

**先例。** 下游组装调研建议“被 Cloud 替换的内容应是独立变体，保留基线 hash 与适用原因”（[下游组装证据](../../research/downstream-composition-evidence.md)）；provenance 的 `pull` 与 `head_sha` 就是它的落地。

</details>

## 验收

- **T15**：采纳 → UAT 块级 gating（Prod 不变）→ promote 后两通道逐字相同、无通道标记 → 上游合并后对账删 variant 并 re-pin 到 merge commit；重复采纳同字节报 Unchanged；生成期 lock 校验不受 variant 影响，pin 失效时 variant 不救；巡检三种状态正确，卡片只在有不健康项或运行出错时红。
