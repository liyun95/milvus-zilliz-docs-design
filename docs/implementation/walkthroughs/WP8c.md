# WP8c 走读：共享输入按组分目录

**上游 PR**：[zilliztech/zdoc#849](https://github.com/zilliztech/zdoc/pull/849)，2026-10-26 合并，commit [`e9ab23f`](https://github.com/zilliztech/zdoc/commit/e9ab23fadbedb35b7069b83dd1a92d77b8fbdc49)。**任务卡**：[WP8c](../tasks/WP8c-zdoc-group-layout.md)。本文补记已合并实现，验证结果引用原 PR，不表示本轮重新运行了当时的测试。

## 解决什么问题

[WP8](./WP8.md) 已提供生成命令、自动写 lock 和 PR 校验。WP8c 把这些入口的共享输入从平铺目录改成按发布组划分：Guides 与 BYOC 共用 `shared-docs/guides/`，以后其他组可以有自己的来源、变量和采用版本。

```text
shared-docs/guides/
  source.yaml
  Variables.json
  links.yaml
  product-names.yaml
  presentation/
  pages/<页面标识>/page.yaml
  pages/<页面标识>/lock.yaml
```

这次只支持 `guides`。目录能分组，不代表 Rust 已经可以接入。WP8c 合并时 master 尚无真实共享页配置，因此没有搬动生产页面。

## 文件地图

以下链接固定到合并版本。

| 文件 | 作用 |
|---|---|
| [adapters/group-context.ts](https://github.com/zilliztech/zdoc/blob/e9ab23fadbedb35b7069b83dd1a92d77b8fbdc49/packages/docs-tooling/src/shared-docs/adapters/group-context.ts) | 在读文件或访问 Git 前验证组名，统一组根目录与诊断路径 |
| [adapters/detect-groups.cjs](https://github.com/zilliztech/zdoc/blob/e9ab23fadbedb35b7069b83dd1a92d77b8fbdc49/packages/docs-tooling/src/shared-docs/adapters/detect-groups.cjs) | 两个 PR 工作流共同使用；校验固定 SHA，以 merge-base 比较变化，拒绝不支持的组 |
| [commands/](https://github.com/zilliztech/zdoc/tree/e9ab23fadbedb35b7069b83dd1a92d77b8fbdc49/packages/docs-tooling/src/shared-docs/commands) | build、inspect、lock、links-seed 的 `--shared-docs` 都接收组目录 |
| [shared-docs-lock.yml](https://github.com/zilliztech/zdoc/blob/e9ab23fadbedb35b7069b83dd1a92d77b8fbdc49/.github/workflows/shared-docs-lock.yml) | 按组识别输入，只暂存允许的 Guides lock 路径 |
| [shared-docs-validate.yml](https://github.com/zilliztech/zdoc/blob/e9ab23fadbedb35b7069b83dd1a92d77b8fbdc49/.github/workflows/shared-docs-validate.yml) | 按受影响组生成；没有共享输入变化时保留快速成功路径 |

错误路径在仓库内显示完整相对位置，例如 `shared-docs/guides/pages/openai/page.yaml`；组目录在仓库外时显示绝对位置。来自 Milvus 原文和片段的路径不改写。

## 一次输入怎样经过工具

以原 PR 的合成 `build-pipeline` 页面为例：

1. `--shared-docs` 指向合成的 `shared-docs/guides/`，group-context 验证目录名。
2. 生成命令从这个组读取 source、变量、链接和页面配置，沿用 WP8 的读取与构建步骤。
3. 生成两页各自的 Guides/BYOC 结果，共四份 MDX，以及含两张图片的 `images.json`。
4. 再加入一条故意不支持的变换，命令报 `CONFIG_FIELD_UNKNOWN`，指出带组名的配置路径，不创建失败输出目录。

原 PR 用同一源 Git 仓库、dev fixture 和本机图片端点，分别执行平铺目录旧实现与分组新实现：**五个输出文件逐字节相同**；四类失败输入的五条诊断只改变组目录前缀，错误码、行号和页面/通道归属不变。这是合成输入经真实 CLI 的验证，不是生产上线证明。

## 可以自己检查

在已有依赖的 zdoc checkout 中运行；若要重现历史版本，请使用独立 checkout 的上述合并 commit，保留自己的改动。

```sh
pnpm exec vitest run packages/docs-tooling/src/shared-docs/testing/group-layout.test.ts
pnpm exec vitest run packages/docs-tooling/src/shared-docs/testing/workflows.test.ts
```

前者覆盖四个命令拒绝未知组、诊断路径和分组后的生成；后者覆盖工作流的组检测与校验路径。完整 demo 的建立输入、命令及输出摘要见 [#849 的 How to try it](https://github.com/zilliztech/zdoc/pull/849)。这些测试不触发真实 GitHub 发布。

## 刻意没做的

- 没有新增 Rust 或其他来源组；这需要后续 SDK Reference 工作包。
- 没有更改 Fetch、dev 上的激活记录或发布所有权；这些由 [WP9a](./WP9.md) 接入。
- 没有改变生成正文、图片地址或产品语义，也没有增加新的错误码。
- 本工作包不消除需求编号；只同步当时的需求清单，并将新增的 `9-9` 留给 WP9。
