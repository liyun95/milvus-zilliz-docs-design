# WP12-A：先看清上游更新会改变什么

WP12 要把 Milvus 上游变化变成可审核的 Cloud 更新 PR。A 先实现其中的变化分析与报告；B 才连接定时检查、生命周期快照、滚动 PR 和工作流。

[A 的实现 PR](https://github.com/zilliztech/zdoc/pull/1027) 已通过主会话技术验收，固定 head `68151311fafa25710b6f9c7c3a18f96cb522c0ec`；尚未合并或发布。范围见[任务卡](../tasks/WP12-zdoc-upstream-updates.md)，验证与限制见[审阅记录](../reviews/WP12-A.md)。

## 从输入到报告

调用方提供固定 master/dev/tool 版本、每页 current/旧 next/候选 next 的源 commit，以及精确本地配置。收集器读取真实原文和依赖，再调用已有 builder 的可选 observer 取得实际 Cloud 输出、手册锚点和图片证据。core 对两个方向分别比较：

- old-next → target：这次上游检查发现了什么新变化？
- current → candidate-next：如果将候选提升，已采用版本会改变什么？

原文变化和输出变化分开。例如 Cloud 已替换某个原文块，这个块仍需要报告上游变化，但 Cloud 输出可能完全不变。原文隐藏部分含缺失变量时保留未解析证据；实际构建失败则标记 outputChanged 为 unknown。

图片报告记录来源、实际读取摘要/长度、最终输出摘要/地址和手册使用位置。改了被使用的仓库图片字节，即使 Markdown 没变也形成候选；未使用图片不产生候选。

## 一个真实输入上的合成变化

验证使用真实 Delete Entities 原文 `3e6b7499cbfcb6b5a365fb1f084a74836f625fc2`，在隔离 Git fixture 中给第 9 行的介绍段落追加一句明确标注的测试文字，得到候选 `d94d5b993738b1cb9c5ff559bf1be11ac296f29c`。没有修改真实上游或生产 lock。

报告片段如下（省略上下文和身份字段）：

```json
{
  "pageId": "delete-entities",
  "sourceImpact": {
    "axis": "old-next-to-target",
    "candidate": true,
    "outputChanged": true
  }
}
```

Markdown 展示第 9 行修改前后的完整段落和邻近标题，列出 Guides/BYOC 锚点未变化，并将同一页面的两个发布目标放入一个采用单元。JSON 还保存固定输入、原文、依赖、摘要、来源位置及比较证据，供后续自动化重算与审计。报告 schema 为 1；这是内部接口，不是已发布的 CLI。

另有 23 页真实留存回放报告。Filtered Search 的相同固定版本比较返回 candidate=false、outputChanged=false，并记录两张图片的实际摘要和使用位置。此结果证明稳定输入不产生更新，不是一次新的上游更新发现。报告文件保留在实现 checkout 的 `.claude/wp12-a/demo/` 和 `.claude/wp12-a/revision-r1-r2/evidence/observed-reports/`，没有把这些本地路径当作可下载的线上 artifact。

## 文件地图

以下相对于 zdoc 的 `packages/docs-tooling/src/shared-docs/`；可在[固定提交](https://github.com/zilliztech/zdoc/tree/68151311fafa25710b6f9c7c3a18f96cb522c0ec/packages/docs-tooling/src/shared-docs)查看：

| 文件 | 负责什么 |
|---|---|
| `adapters/update-inputs.ts` | 读取固定输入、raw 依赖与实际 builder 观测，区分原文和构建诊断 |
| `adapters/build-page.ts` | 可选只读 observer；复用已有图片读取证据，保持默认输出 |
| `core/updates/types.ts` | 输入、变化、图片、锚点和采用单元的 JSON 兼容类型 |
| `core/updates/impact.ts` | 两轴比较、验证、JSON/Markdown 渲染 |
| `core/updates/anchors.ts` | 按手册建立有证据的锚点对应；多义/删除只作提示 |
| `core/updates/units.ts` | 只按已证明的采用依赖分组，不因共用 fragment 就合组 |
| `fixtures/milvus-docs/build.ts` | 合成 Git 历史支持删除/改名，保留旧默认提交身份 |

## 自己验证

在 zdoc checkout 中执行：

```sh
gh pr checkout 1027 -R zilliztech/zdoc
corepack enable
pnpm install --frozen-lockfile
pnpm exec vitest run packages/docs-tooling/src/shared-docs/testing/updates packages/docs-tooling/src/shared-docs/testing/build/build.test.ts packages/docs-tooling/src/shared-docs/fixtures/milvus-docs/build.test.ts
```

不用 GitHub CLI 时，第一步改为 `git fetch origin pull/1027/head:pr-1027`，然后 `git checkout pr-1027`。验收版本预期 5 文件 / 75 项通过。

值得读的测试：`testing/updates/impact.test.ts` 中隐藏变量、状态转换、图片单独变化及跨目录页面依赖；`testing/updates/anchors.test.ts` 的锚点歧义；`testing/updates/units.test.ts` 的证据分组；`testing/build/build.test.ts` 的 observer 默认输出、请求流和图片 provenance。

A 不写 lock、不改链接、不打开更新 PR，也不触发 Fetch。报告中的 promotion eligible 仅是判断，不执行 WP13 提升。完整 WP12 的需求编号尚未结项。
