# WP12-B 走读：本地更新准备已完成，远端自动化待实现

截至 2026-11-10，B1 的只读报告、B2 的本地规划/准备与 B3 前两片的纯远端校验契约、只读事实和历史认证已合并；整个 B 尚未完成。阶段与下一步计划入口统一放在 [WP12 任务卡](../tasks/WP12-zdoc-upstream-updates.md)，不另设 coordination 或 review 状态入口。

## 已交付的部分

| 阶段 | 实现 | 合并证据 |
|---|---|---|
| B1 | 固定输入、生命周期观察、只读更新报告 | [#1055](https://github.com/zilliztech/zdoc/pull/1055)，`d06339345458a7465140a85389a9df5e9f68a603`，2026-11-03 |
| B2 | `update-plan` / `update-prepare`、可信工具集、隔离 Git 候选、proof/journal 与恢复 | [#1155](https://github.com/zilliztech/zdoc/pull/1155)，`98de1d8426b1d251b8393ea9b5ad91686de14776`，2026-11-09 |
| B3 第一片 | 远端观察的严格 schema、读取状态分类、精确验证收据的纯一致性校验 | [#1189](https://github.com/zilliztech/zdoc/pull/1189)，`87f103f926d27943861278181308ebbb7cb73fe0`，2026-11-10 |
| B3 第二片 | 有界 GitHub 只读事实、artifact 证明和原始 Git 历史认证 | [#1193](https://github.com/zilliztech/zdoc/pull/1193)，`38a721e3e720fee4a43d401a69b53663bdf423b4`，2026-11-10 |

B2 的含义是：在本地证明“这些固定输入应产生什么候选”，不自动推送分支、创建 PR 或发布。对真实 Guides 的收集和生成使用受约束的工具集；输入或身份不充分时输出 hold，不通过扩大权限继续运行。

Linux 的可信工具集捕获当前明确 fail-closed；SDK subject 当前返回 `PROVIDER_NOT_INSTALLED`。这些不是成功分支，也不因常规 CI 或 Fetch 在 Linux 运行就视为已支持。

## B3 第一片：纯远端校验契约

新增 [core/updates/remote.ts](https://github.com/zilliztech/zdoc/blob/87f103f926d27943861278181308ebbb7cb73fe0/packages/docs-tooling/src/shared-docs/core/updates/remote.ts) 和对应 `testing/updates/remote.test.ts`，没有接入现有 CLI 或生产 workflow。

`classifyRemoteRead` 区分已找到、已证明不存在与未知；HTTP 404 本身不能证明不存在。`acceptExactValidation` 检查独立取得的远端观察和收据是否一致：PR base 必须等于固定 master，producer/validator 运行分开，workflow 触发者与实际写入者分开，工具 M 的运行检查与候选 S 的目标检查分开，archive/member/output 的摘要也分别绑定。证据缺失、过期、错配或歧义时返回 hold。

这些纯函数只检查一致性。JSON、签名标记或一个成功 check 不能自行产生真实远端身份；API/签名/工作流来源、归档成员归属和 Git 历史的认证留给第二片及后续接线。第一片不会创建 PR、改 ref、执行候选代码或解除 Linux 限制。

方案和代码审阅保留在 [fork PR #18](https://github.com/liyun95/zdoc/pull/18)。最终产品 HEAD `4d33a1131716c8db2b3063c0b08800b69e5caa7a` 的本地验收为 1352 passed / 0 failed / 6 既有 skipped；59 个新增测试全部执行。typecheck、matrix 25/25、policy 118/118、完整 diff selector 和 diff-check 均通过；[上游 CI](https://github.com/zilliztech/zdoc/actions/runs/42635810941) 亦通过。此处记录已有留存结果，本次文档收尾未重跑产品测试。

六个既有跳过项为四个可选 loopback 图片测试、需显式开启的 measured Guides collector 测试和一个需大小写敏感文件系统的用例，不计作通过。完整本地证据根为 `/Users/liyun/.cache/zdoc-vitest/run-koV6yc`。

## B3 第二片：只读事实与历史认证

[fork PR #19](https://github.com/liyun95/zdoc/pull/19) 已完成方案和代码主审；最终产品 HEAD 为 `9db162557a80450ba6cf7d922ab653bbadf2d6d2`，本地主审与最终验证通过，[上游 PR #1193](https://github.com/zilliztech/zdoc/pull/1193) 已在 CI 通过后于 2026-11-10 合并，merge SHA `38a721e3e720fee4a43d401a69b53663bdf423b4`。

`createRemoteReads` 读取并绑定 GitHub repository/ref/PR/run/check、签名与 artifact；网络层只允许固定的 GET 和只读 GraphQL 查询。分页不完整、来源不明、归档不合法或前后观察变化都会停止。`inspectRemoteHistory` 独立核对原始 Git object 哈希、完整祖先、P/K/S 关系、next-only 改动及人工合并；分批保存原始对象和定位清单，避免逐提交写盘。`inspectRemotePulls` 只归组已认证的 subjects，未知来源或跨 unit key 重叠不继续。

最终 HEAD 的完整测试为 1435 passed / 0 failed / 6 既有 skipped；142 个远端契约/API/历史测试全部执行，其中 83 项是第二片新增。完整 diff selector、typecheck、matrix 25/25、policy 118/118 和 diff-check 均通过。全量只执行一次，约 700 秒；证据根为 `/Users/liyun/.cache/zdoc-vitest/run-wgVDW0`。接近当前仓库规模的 3,003 个提交头 fixture 约 3–5 秒完成校验；这是本地有界读写验证，不代表真实平台资格。

新增适配器尚未被 CLI、Fetch、Translation 或发布入口调用。真实 producer 默认未安装，生产 raw-object 获取与平台资格未交付；复杂 merge 和跨单元重叠保守 hold。历史 closure 是受信 producer 的摘要证明，不等于本次重新捕获工具或重跑 B2。

## 从固定输入到候选

请求指定固定 master/dev/source 身份、待处理的页面和比较条件。`update-plan` 收集材料、分析源与实际 Cloud 输出、构造采用单元，必要时在隔离区准备合并基线；不修改真实输入仓库。

操作人检查 `result.json`、`reports/`、`units/` 后选定一个 unit。`update-prepare` 再核对 plan、source、配置、权限和工具集，在自有输出目录内准备最多一个候选，只改变选定的 next 锁。scratch Git 对象、journal 和 proof 留在输出目录。恢复必须匹配原请求和自有 journal，并重新验证；不能拿任意非空目录当作 resume 输入。

命令返回 0 不一定产生候选：必须查看 status、disposition 和 reasons；held 不提供候选/proof，draft-failure 不能发布，外部 operations 仍为空。

具体请求契约与操作步骤以 [合并版本 README](https://github.com/zilliztech/zdoc/blob/98de1d8426b1d251b8393ea9b5ad91686de14776/README.md) 为准。不能把不完整示例请求当成生产请求；需要通过捕获资格的环境及真实固定输入。

```sh
pnpm docs-tooling shared-docs update-plan \
  --request /absolute/request.json --out /absolute/new-plan
pnpm docs-tooling shared-docs update-prepare \
  --request /absolute/request.json --plan /absolute/new-plan \
  --unit '<unitKey from the plan>' --out /absolute/new-candidate
```

## 文件地图与值得读的测试

下列路径相对于 zdoc 的 `packages/docs-tooling/src/shared-docs/`，参见 [合并版本源码](https://github.com/zilliztech/zdoc/tree/98de1d8426b1d251b8393ea9b5ad91686de14776/packages/docs-tooling/src/shared-docs)。

| 文件 | 负责什么 |
|---|---|
| `commands/update-plan.ts`、`update-prepare.ts` | 严格请求/输出参数与命令边界 |
| `adapters/updates/toolset.ts` | 工具闭包与原生依赖捕获、访问检查、每次启动前再验证 |
| `adapters/updates/guides-provider.ts` | Guides 固定输入收集与受约束的执行 |
| `adapters/updates/local-runner.ts` | 本地规划、准备与恢复编排 |
| `adapters/updates/transactions.ts` | 隔离 Git 事务及候选准备 |
| `core/updates/canonical.ts`、`envelope.ts` | canonical 数据与严格内部信封校验 |

重点阅读 `testing/updates/toolset.test.ts` 的缓存污染、未测量加载、缺失候选和符号链接路径测试；`transaction.test.ts` / `transactions.test.ts` 的 Git 事务；`local-runner.test.ts` 和 `update-prepare.test.ts` 的请求、hold、恢复及候选绑定。测试运行器还拆分了重型 Git 阶段，避免把单机资源竞争误当产品行为。

需要自己核对实现时，在独立 checkout 使用固定合并提交，不改变已有开发工作区：

```sh
git fetch origin master
git switch --detach 98de1d8426b1d251b8393ea9b5ad91686de14776
corepack enable
pnpm install --frozen-lockfile
pnpm test:shared-docs
pnpm typecheck
pnpm test:workflow-matrix
```

遵循仓库固定工具链与 README 中的运行环境要求。Linux 下跳过的真实捕获用例不能被记作通过；运行器支持 Linux 不等于可信捕获支持 Linux。

## B2 审阅与验证证据（2026-11-09）

合并前审阅修复了缓存执行、原生库查找位置、悬空/多层符号链接和遍历路径等安全边界问题；Linux 捕获入口保持明确拒绝。全量本地与 CI 的资格结论有各自的固定环境和跳过范围，不将一个平台的结论转移到另一个平台。本次收尾没有重新执行这些昂贵测试，以下新增核验是读取 GitHub 的不可变 run 与留存结果。

- [Translation FIFO replay 42584534917](https://github.com/zilliztech/zdoc/actions/runs/42584534917)：在最终修复 head `4fa44064aa159a57093388f50d55dbe354b0fa25` 上成功。这是 replay 验证，不是生产 Translation。
- [合并前 artifact-only Fetch 42584532856](https://github.com/zilliztech/zdoc/actions/runs/42584532856)：前次主审已核对中英文 assembly 和最终只产物结果，无发布提交或 Translation。本次保留该既有结论，不冒充重新执行。
- [合并后 scheduled Fetch 42599114207](https://github.com/zilliztech/zdoc/actions/runs/42599114207)：本次重新下载 selection/results/card-report 和最终 verification。event=schedule，工具 SHA 为 `15387649ba38bcea441366df8d3a5ccafae8ecfd`；10 个源发布单元全部为 published，包含英文/中文 Guides、六个 SDK/CLI 分组以及中英文 REST。中英文 assembly、revision reconciliation、final verification 和 aggregate 均成功。

正式 run 的 publication-results 显示 `mode=publish`、`overallStatus=success`，dev 从 `1b1ed2712ca1c3bb845a69c6e5c361469cc26fa7` 推进到源发布最终结果 `1950f3a09180045e3290c14dc36740c3628c67c6`。selection 与 results 的摘要一致：`a0c8d2899b435033ddb1315612d07894d39815ef94f56065560af02fd9df513e`。对应 artifacts：selection `13666097890`，results `13670900341`，card-report `13670352872`，final verification `13670776393`。

这是既有 Fetch 在包含 B2 的工具版本上的生产兼容性证据；该工作流没有执行 WP12 本地更新 CLI，更没有自动创建更新 PR。本次选择 `runTranslations=false`，下游 Translation 未请求；不据此宣称 Prod/UAT 网站已经部署。

card-report 仍列出英文 25 条、中文 22 条 canonical-link 问题，以及部分 alias 证据提示。它们作为独立内容/证据维护项保留，未在本次归因或修复；整体 run 成功不等于所有内容告警清零。

## 收尾与下一步

**B2 可以按本地 Guides 阶段标记完成。** 新增 scheduled Fetch 证据补充了合并后发布兼容性观察，不替代此前安全与本地事务验收。Linux 可信捕获、真实 SDK provider、远端滚动 PR、B4 schedule/rollout、完整退役处理和 WP13 提升不在这一完成声明里；WP12 的 pending 编号不变。

B3 总计划已合并设计 PR #78，第一片已合并产品 PR #1189。第二片只读事实与远端历史认证已通过主审、本地验证和上游 CI，合并 #1193。第三片入口已进行两次获准的隔离 API 预检，尚未通过。第二次已验证 7 个 fixture 对象及 absent→K、空文件变化 seal 创建；签名查询语法遗漏阻止了后续步骤。只读补证发现真实 author 为机器人、committer/signer 为 GitHub 平台身份，与冻结的 committer 规则不相容，另有签名续行字节重建遗漏。下一步先审阅身份认证规则及修正预检代码，再准备额外获准的验证；不以当前结果进入第三片产品实现。第三片的真实 API 可行性预检和 B4 平台资格仍保留。具体交付清单见 [任务卡](../tasks/WP12-zdoc-upstream-updates.md)。
