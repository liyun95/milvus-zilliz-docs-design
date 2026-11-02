# WP9b 走读：写 dev 前复核共享输出

**任务卡**：[WP9b](../tasks/WP9b-zdoc-fetch-followups.md)。分两次交付：

| 部分 | 合并结果 |
|---|---|
| WP9b-1：删除块后的空行与内部清理 | [#950](https://github.com/zilliztech/zdoc/pull/950)，[`4b453a0`](https://github.com/zilliztech/zdoc/commit/4b453a0b9815e99b6e603e652aa76fc9496d4029) |
| WP9b-2：Fetch 保护、别名、收据与真实运行修复 | [#960](https://github.com/zilliztech/zdoc/pull/960)，[`0f9a4d4`](https://github.com/zilliztech/zdoc/commit/0f9a4d4529bfd795c0792df5564215b09a60b5ca)；[工具链同步 #968](https://github.com/zilliztech/zdoc/pull/968) 已合并 |

本文说明已合并的实现与合并前验证。正式发布和网站验收另记；2026-10-30 核对时，后续 [Fetch 41034927510](https://github.com/zilliztech/zdoc/actions/runs/41034927510) 仍在运行。当时未完成发布验收，本文不据此判断当前运行状态。

## 解决什么问题

[WP9a](./WP9.md) 已能把激活页从 Git 生成并交给 Fetch。WP9b 要保证“交给发布的这份内容，确实能从记录的输入重新得到”，并补齐真实运行暴露的别名、图片和证据体积问题。

| 以前的缺口 | 现在的处理 |
|---|---|
| 候选正文虽有摘要，却缺独立再生成核对 | 从固定 Git 输入恢复干净目录，重新生成并对照收据与候选字节；单页不一致则保留已有版本 |
| 图片原地址可能被同名覆盖 | 读取之前采用的图片摘要，沿用已采用图片；变化通知走现有卡片 |
| 同一飞书文档有不同 token 链接 | 保留 `feishu_token`，增加经证据验证的 `feishu_aliases`；路由与链接报告都识别别名 |
| 激活总要重新读取旧飞书正文 | 只有需要换算旧锚点时才读取；没有带锚点的引用时不要求旧正文仍可访问 |
| WP11 的 front matter 备注停留在构建结果 | 写入收据 `notes[]`，便于解释两版不同但采用 current 元数据的情况 |
| 删块后多出空行 | WP9b-1 收拢空行，并清理已不用的 `failures` 返回值 |

## 文件地图

代码链接固定到 WP9b-2 合并版本。

| 文件 | 看什么 |
|---|---|
| [guides-shared-sources.js](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/scripts/docs-workflow/guides-shared-sources.js) | 抓取阶段生成、收据、别名证据、图片通知与 bundle 输出 |
| [guides-shared-regeneration.js](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/scripts/docs-workflow/guides-shared-regeneration.js) | 恢复固定输入、校验工具身份、独立生成与逐文件核对 |
| [sharedPageAliases.js](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/packages/docs-tooling/src/lark/sharedPageAliases.js) | 有界的旧快照/缓存证据、Git 归属证明、别名恢复与补齐 |
| [sharedPageFetch.js](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/packages/docs-tooling/src/lark/sharedPageFetch.js) | 激活时按实际引用决定是否取旧正文、换算锚点 |
| [sharedPageBundle.js](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/packages/docs-tooling/src/lark/sharedPageBundle.js) | 生成结果交接、路径/体积/数量界限和证据绑定 |
| [sharedPagePublication.js](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/packages/docs-tooling/src/lark/sharedPagePublication.js) | 检查点发布前再次验证输出、收据、再生成证明和别名归属 |
| [guides-shared-images.js](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/scripts/docs-workflow/guides-shared-images.js) | 已采用图片与当前图片读取；配合现有 uploader 保持图片身份 |
| [spec/coverage.ts](https://github.com/zilliztech/zdoc/blob/0f9a4d4529bfd795c0792df5564215b09a60b5ca/packages/docs-tooling/src/shared-docs/spec/coverage.ts) | 将相关 Fetch JavaScript 测试纳入编号覆盖，不再只扫描 shared-docs TypeScript 测试 |

## 一页怎样从生成走到发布验证

1. Fetch 固定配置、Milvus current/next、dev 和导航输入。新的收据在 `inputs.fetch.render_targets` 中保存版本 1 的渲染目标，包括两个手册的路径、扩展名和导航信息，避免重新生成时猜测现场状态。
2. 正常生成 Guides/BYOC 候选，记录输出 SHA-256、已采用图片及 `notes`。有共享页时必须有合法的 `IMAGE_BED_URL`。
3. 独立再生成先核对输入清单和工具身份，从 Git 恢复干净配置、源与 dev 输入。读取已采用图片并校验摘要，用同一固定渲染上下文重新构建。
4. 核对两个手册的路径、输出集合和实际字节。再生成中的图片改写只处理图片目标，不替换代码里的相同字符串，所以能发现原生成路径的整页替换误伤。
5. 不一致报 `PUBLISH_REGEN_MISMATCH`，指出文件和预期/实际摘要。这一页回退已有版本，其他成功页仍可继续。通过时生成与本次收据绑定的证明。
6. bundle、表输出和检查点继续验证这些绑定；别名也要能证明属于原来的那条记录，不能靠增加一个字符串就接管别的文档链接。

**旧收据不伪装成新证据。** 没有 `render_targets` 的旧收据只用来做升级对照；新工具与历史产物不同，不应直接当成历史发布损坏。新运行产生的新收据才执行本次独立再生成契约。

别名恢复只用已有激活状态、同记录旧缓存和固定 dev 祖先快照等本地证据，不为补别名额外调用飞书。证据找不到时给提示；验证出的所有权冲突仍然失败。已有条目只补别名，不改原身份和锚点字段。

## 真实运行暴露的 bundle 大小问题

首次 Guides 验证 [41012796536](https://github.com/zilliztech/zdoc/actions/runs/41012796536) 失败，原英文 bundle 未留存，不能声称读到了那个失败文件。用另一份已认证的历史输入重新生成，复现了单文件越界：漂亮打印的 JSON 为 33,639,144 字节，超过 32 MiB 的 33,554,432 字节上限。

修复只把外层 JSON 改成紧凑编码，并在生产端使用与读取端相同的边界检查。保留证据字符串、收据、正文和既有限制：单文件 32 MiB、总 payload 256 MiB、最多 8,192 个文件。报错区分路径、单文件、总大小和文件数量，并带实际值；紧凑编码后仍超限就失败，不通过放大限制掩盖增长。

## 已有验证证据

| 证据 | 结论与边界 |
|---|---|
| [最终 Guides 运行 41023321589](https://github.com/zilliztech/zdoc/actions/runs/41023321589) | 实际工具版本 `1f7e91e93`；publish=false、runTranslations=false、media_upload_mode=skip。39 个 ZIP 身份与摘要验证通过；16 页成功、0 回退、32 份共享输出与固定 dev 基线逐字节相同 |
| 同次收据与构建 | 16 份收据有成对 render_targets，notes 为空；激活清单增加 32 个已认证别名，其他原字段不变。bundle 25,193,699 字节；Actions 英/日/中构建成功 |
| [C++ SDK 运行 41012812433](https://github.com/zilliztech/zdoc/actions/runs/41012812433) | 工具版本 `81217aa`，142 页未变。此后仅修 Guides bundle；保留这次原版本归属，不宣称它验证了后续提交 |
| 真实留存 artifact 隔离回放 | 20 个 ZIP 验证、10 个检查点预检并应用；32 份共享输出不变；回放使用本地 bare remote，未写真实 dev |
| 最终修复的测试联集 | 24 个命令通过，含完整 replay、shared-docs、typecheck 与 workflow-policy；部分既有测试跳过如实保留，不计作执行成功 |

全量 Guides 对照中，中文 598 份 Markdown 全相同；英文 702 份中两份 Query 页面因经认证的飞书原文修订而变化，其余 700 份相同。29 条历史失效引用逐条未变，没有新增。Actions 组装跳过了完整链接检查，因此构建通过不等于完整 HTTP 抓取或 Prod 浏览器验收。

详细验证结论与后续修复说明见 [PR #960 的审阅记录](https://github.com/zilliztech/zdoc/pull/960#issuecomment-6517838954) 及上述 Actions。大体积原始证据保留在原验证工作区，不复制进设计仓库。

## 可以自己检查

在安装好固定依赖的 zdoc 独立 checkout 中运行；重现本文版本时使用上述合并 commit。以下测试使用 fixture/隔离输入，不发起真实 Fetch。

```sh
node --test scripts/docs-workflow/guides-shared-regeneration.test.js
node --test --test-name-pattern='bundle limits|compact generated|still-oversized' scripts/docs-workflow/guides-shared-sources.test.js
pnpm test:replay:shared-pages
```

第一项值得重点看：字节/摘要/缺文件/多文件/输入清单篡改，以及代码中出现图片地址时是否只回退有问题的页。第二项验证压缩前后对象不变、边界一致，以及仍超限时拒绝。第三项检查 Fetch 的完整共享页场景。它们是回归检查，不代替 README 规定的真实 artifact 回放。

## 尚未结项的工作

- 正式 Fetch 完成后核对发布收据、别名和本次实际页面集合；不能沿用 16 页/32 份作为后续增加页面后的固定数量。
- 单独确认 Translation 结果与实际 UAT/Prod 部署 SHA；Fetch 成功不证明翻译或网站验收完成。
- 激活前比较、完整下线、旧任务归属和直接修改 dev 生成内容的拦截归 WP14；共享页的完整翻译、恢复和缓存验收归 WP15。
- 第二个来源组的 bundle/publication 泛化留给 Rust 接入；本次没有实现 Rust，也没有自动激活新页面。
