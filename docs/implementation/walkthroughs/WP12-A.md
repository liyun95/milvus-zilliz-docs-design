# WP12-A 走读：上游变化分析与报告

WP12 要把 Milvus 上游变化变成可审核的 Cloud 更新 PR。A 先实现其中的变化分析与报告；B 才连接定时检查、生命周期快照、滚动 PR 和工作流。

[A 的实现 PR](https://github.com/zilliztech/zdoc/pull/1027) 已通过主会话技术验收，固定 head [`68151311f`](https://github.com/zilliztech/zdoc/commit/68151311fafa25710b6f9c7c3a18f96cb522c0ec)；尚未合并或发布。范围见[任务卡](../tasks/WP12-zdoc-upstream-updates.md)；验证结果见下文“审阅与验证”。

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

## 审阅与验证

2026-11-02 主会话完成复审，固定版本为上文的 `68151311f`。Standards 和 Spec 均无剩余可操作问题；结论仅覆盖 A 的技术验收，上游维护者 review、合并和生产发布另记。

| 首轮问题 | 修复与验证 |
|---|---|
| R1 / P1：被 Cloud 替换的原文含缺失变量时，收集器中断整批报告 | 保留 unresolved/null 及 raw 诊断；覆盖缺失/有值双向变化、实际构建失败时 unknown、同批独立页面正常返回 |
| R2 / P2：只改图片字节时漏标候选 | 从已有读取获取来源、实际与输出摘要；使用中图片变化产生候选，未使用图片不产生候选 |

主会话在验收 head 独立执行上面的 5 文件 / 75 项测试和原始两项缺陷复现，均通过；`git diff --check` 也通过。原组合 fixture 保留先前的图片变化，隐藏变量输出不变由隔离回归证明。

以下为执行方在同一 head 重新运行的结果，主会话核查了日志和相关脚本，没有重复运行整套回放或站点检查：

| 验证 | 结果 |
|---|---|
| `pnpm test:shared-docs` | 63 文件，823 passed，4 既有 skipped |
| typecheck、完整 diff selector、workflow matrix/policy、REST publication contract | 全部通过；路径均已映射、归 master |
| shared-pages replay | 29 passed |
| 真实留存输入认证 | 10 个 checkpoint / 3363 文件、695 源文件、5 个图片对象 |
| 真实生成及 observer 比对 | 23 页 / 46 输出，无差异、无 fallback；独立 runtimes 的图片请求/读取流相同 |
| 受影响 Guides checkpoint | 743 文件，仅在隔离本地 bare remote 发布，远端状态确定 |
| 站点及 inventory | EN（含 JA）、ZH 构建和 Guides/BYOC 浏览器检查通过 |

真实留存来源为 [Fetch 41335409455](https://github.com/zilliztech/zdoc/actions/runs/41335409455) attempt 1，源 artifact `13095887154`，ZIP SHA256 `2cabe42d039ebbdf6ac4537ef1aee325a4d4cbec26e684987a369c64cabfe4f1`。原 tooling 为 `48c0d7bfa7a6e74d7f645cf626bd81bae8003473`，dev 为 `76c053277f44b23148ad998c279c27a99ba86d67`。重建只在内存比较 receipt 中替换执行工具 SHA，原 receipt 不变。

图片验证是接受字节的离线回放，不是新的 HTTP 观察；站点验证是恢复留存状态后的合成覆盖，真实原文重建单独验证。初次相对路径前置检查失败和既有中文 home 断链警告如实保留，不声称生产发布、完整 FIFO 或下游 Translation 已验收。

原始日志保存在实现 checkout 的 `.claude/wp12-a/revision-r1-r2/evidence/` 和 `.claude/wp12-main-review/`，未上传为源码或 Actions artifact。[PR #1027](https://github.com/zilliztech/zdoc/pull/1027) 在验收 head 的 CI 已完成：10 项通过，4 项按条件跳过；合并与发布状态以该 PR 及后续发布记录为准。
