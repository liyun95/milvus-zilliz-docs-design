# WP12-A：固定输入影响报告验收

日期：2026-11-02。状态：技术验收通过，进入上游 PR 审阅；尚未合并或发布。

- 实现 PR：[zilliztech/zdoc#1027](https://github.com/zilliztech/zdoc/pull/1027)。
- 整体 base：`34498a57295e3ab99327e9b00ddd767cab956f6a`。
- 首轮 head：`b7cbca559d983a1358b098a1e633ed7c31a3d38c`。
- 验收 head：`68151311fafa25710b6f9c7c3a18f96cb522c0ec`。
- 范围：任务卡列出的 15 个路径；修订涉及其中 7 个路径。

## 首轮问题与修订

| 问题 | 影响 | 最终验证 |
|---|---|---|
| R1 / P1：隐藏原文缺失变量 | Cloud replace 后正常构建成功，但收集器抛错，阻断整批报告 | 明确保留 unresolved/null、原文诊断与构建错误分离；覆盖缺失/有值双向变化、真实失败时 unknown、同批其他页面继续返回 |
| R2 / P2：只修改图片字节 | 实际输出变化，却返回 candidate=false、changes=[] | 从现有读取取得图片来源、实际摘要和输出摘要；使用中的图片变化产生候选，未使用图片不产生候选 |

Standards：0 项可操作问题。Spec：R1/R2 关闭，0 项新增可操作问题。默认构建和 observer 的结果、图片请求与读取流相同；core 维持纯计算。

## 验证与边界

主会话在最终 head 独立执行：

```sh
pnpm exec vitest run packages/docs-tooling/src/shared-docs/testing/updates packages/docs-tooling/src/shared-docs/testing/build/build.test.ts packages/docs-tooling/src/shared-docs/fixtures/milvus-docs/build.test.ts
git diff --check 34498a572 HEAD
```

5 个文件 / 75 项通过，diff check 通过；原始两项缺陷的隔离复现也重新执行并确认修复。原组合 fixture 含先前图片变化，隐藏变量的输出不变由独立回归证明。

执行方在相同最终 head 运行，下列记录和相关脚本已由主会话核查；主会话没有重复运行全部套件：

| 验证 | 结果 |
|---|---|
| shared-docs | 63 文件，823 passed，4 既有 skipped |
| typecheck、完整 diff selector、workflow matrix/policy、REST publication contract | 全部通过；路径均已映射、归 master |
| shared-pages replay | 29 passed |
| 真实留存输入认证 | 10 个 checkpoint / 3363 文件、695 源文件、5 个图片对象 |
| 真实生成及 observer 比对 | 23 页 / 46 输出；无差异、无 fallback；独立 runtimes 的图片请求/读取流相同 |
| 受影响 Guides checkpoint | 743 文件，仅在隔离本地 bare remote 发布，远端状态确定 |
| 站点与 inventory | EN（含 JA）、ZH 构建和 Guides/BYOC 浏览器检查通过 |

留存身份：Fetch `41335409455` attempt 1，源 artifact `13095887154`；ZIP SHA256 `2cabe42d039ebbdf6ac4537ef1aee325a4d4cbec26e684987a369c64cabfe4f1`。原运行 tooling 为 `48c0d7bfa7a6e74d7f645cf626bd81bae8003473`，dev 为 `76c053277f44b23148ad998c279c27a99ba86d67`。重建只在内存比较 receipt 中替换执行工具 SHA，不修改原 receipt。

图片验证是已认证接受字节的离线回放，不是新 HTTP 请求；站点验证是恢复留存状态后的合成覆盖，真实原文重建单独验证。站点 helper `53e71e6d16580359ca8799aacc1dbfc651f7a6bc` 基于验收 head。初次相对路径前置检查失败及既有中文 home 断链警告均已保留。

证据保存在实现 checkout 的 `.claude/wp12-a/revision-r1-r2/evidence/`，主会话定向日志在 `.claude/wp12-main-review/`，未作为源码或 GitHub Actions artifact 上传。复核不声称生产发布、真实权限 smoke、完整 FIFO 或下游 Translation 验收。

## 下一裁决点

A 的代码与默认行为已通过技术审阅；上游维护者 review、PR CI 和合并状态单独跟踪。提 PR 时 master 为 `0ec24f8cd8d6f6525b2dca3c42fc2dbf659dad19`，merge-tree 无冲突；未把已验收 head 的本地检查冒称为合并树检查。

B 的自动化、快照与滚动 PR 事务需另审计划；WP13 未启动。所有 WP12 pending 编号保持，完整 7-9 仍依赖 WP14；Rust 手册策略等待 R1 契约稳定。
