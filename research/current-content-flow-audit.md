# 现状内容流程：事实核验与证据边界

核验日期：2026-10-11。服务于[第一次方案对齐会](../docs/proposal.md)的现状描述。采用此前固定源码快照补查关键入口；未执行生产导出、修改远端文件或触发 PR。

## 已确认与待确认

| 事项 | 结论 | 依据与边界 |
|---|---|---|
| 参与者与编辑入口 | 文档工程师可以编辑飞书后导出提 PR，也可以直接向 Milvus 提 PR；社区贡献者通过 PR 修改 Milvus | 用户确认；“文档工程师”是两侧共同角色，不要求由同一个人承担 |
| 回同步触发 | 没有同步提醒或固定检查 | 用户在本轮明确确认；不能据此扩大成“所有流程都无通知” |
| 冲突优先规则 | 双方不知道冲突时以哪一方为准 | 用户在本轮明确确认 |
| 导出写入方式 | 按飞书生成内容重写对应工作区文件，再创建 PR | 固定 Milvus 源码 `scripts/index.js` 与 `.github/workflows/doc.yml`，见下文 |
| 覆盖社区修订 | 存在条件性风险：飞书缺少修订 → 再导出产生回退 diff → 审核遗漏并合并 → 当前正文回退 | 是实现支持的风险分析，未核实实际事故。PR 审核可以拦截，Git 历史仍可追溯 |
| 分叉检测 | 在已检查的导出入口、生成逻辑与 PR 检查工作流中未发现跨源分叉检测 | 不是对全部内部工具、组织配置和实际运行状态的穷尽审计；会上确认是否另有检测 |
| 飞书修订记录 | zdoc 已有 snapshot / revision inventory 实现，保留 revisionId 等字段并生成修订差异 | 不能写成“飞书侧没有版本记录”；未据此证明团队飞书评审或恢复规则 |
| 飞书正文评审 | 未确认实际评审入口、人员与放行规则 | 列入会议待确认，不推断飞书没有评审 |
| 共用规模 | 尚无可用于本节的 User Guide 页数或重合比例统计 | 删除“大量”“高度重合”等规模断言；会议中提及的 SDK 页数不能移用为本节数据 |
| 内容过滤与版本控制 | 会议明确提及内容过滤标签体系、版本过滤标签体系，以及产品未 ready 时不能先发布文档 | 会议记录 16–18 分钟附近；详见本地逐字稿，不将描述替代生产配置验证 |

## 导出与 PR 的证据链

固定 Milvus 修订：`7d87b0bf26d7cbc713f40af6453ea2f925367901`。

1. [`scripts/index.js:34`](https://github.com/milvus-io/milvus-docs/blob/7d87b0bf26d7cbc713f40af6453ea2f925367901/scripts/index.js#L34) 调用 `write_doc`，得到飞书生成的正文。
2. 同文件第 46–71 行通过 page_id 查找现有文件，确定输出路径，并执行 `fs.writeFileSync(outputPath, [front_matters, content].join('\n\n'))`。递归导出第 92–119 行采用相同写入模式。现有正文被读取用于定位文件，不是用来与飞书内容做三方合并。
3. [`.github/workflows/doc.yml`](https://github.com/milvus-io/milvus-docs/blob/7d87b0bf26d7cbc713f40af6453ea2f925367901/.github/workflows/doc.yml) checkout 仓库、运行生成脚本，再通过 `peter-evans/create-pull-request` 创建或更新 PR，并报告该 PR 的 URL。因此“生成时整页重写”与“PR 可审核 diff”同时成立。
4. [`.github/workflows/check.yml`](https://github.com/milvus-io/milvus-docs/blob/7d87b0bf26d7cbc713f40af6453ea2f925367901/.github/workflows/check.yml) 在所查修订中运行链接检查，未显示跨源正文一致性检查。其他已保存的 workflow 也未显示社区 PR 合并后发起飞书回同步的入口。仓库外流程与团队工作方式不能仅靠此搜索判定。

风险示例：Git 中说明从 A 修正为 B，飞书仍是 A；导出器基于当前 Git 工作区写回飞书生成的 A，会形成 B → A 的变更。即使 Git 没有报告合并冲突，该变更也可能是内容回退。能否阻止回退取决于审核和其他保护是否识别，不能将“无 Git 冲突”等同于“语义正确”。

## 飞书版本信息的证据

固定 zdoc 修订：`3777ec0b322546d716485e8f88da8412b0265e71`。

[`revisionInventory.ts`](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/lark/revisionInventory.ts) 定义并保留 `revisionId`、编辑时间等字段，比较新旧 inventory，并生成修订差异。它追踪飞书输入变化，不自动等于 Milvus Git 与飞书两套正文的分叉检测，也不证明组织采用了怎样的飞书人工评审。

[上次会议纪要](https://zilliverse.feishu.cn/docx/D6zidlbaTo6DfYxdnleceiUtnlX)支持“人工同步负担”和“内容过滤、版本控制不能丢”的描述。回同步提醒和冲突优先规则则以本轮用户补充为准。
