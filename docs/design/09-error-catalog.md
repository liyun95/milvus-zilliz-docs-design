# 09 错误目录

对应的产品需求见[产品需求](../prd.md#5-场景)各场景的“出错时”，以及[第 6 节](../prd.md#6-对现有能力的要求)中的“出错”：一律失败，说明原因与应改的文件，不静默跳过。本篇汇总所有错误，给每一种一个错误码，并约定报给作者的提示包含什么。

**参与方**：md2md、zdoc 生成、zdoc 新增工作流（报错方）；文档工程师（读提示）。

**状态**：骨架，待工程维护者补充。目前只有命名块与预处理定义了错误码，其余错误只有文字描述。

## 约定

### 每个错误包含什么

| 内容 | 说明 |
|---|---|
| 错误码 | 大写字母与下划线，按来源加前缀 |
| 在哪里报 | milvus-docs 的 PR 检查、zdoc 的 PR 校验、上游更新 PR、Fetch、激活运行 |
| 位置 | 文件，能定位时加行号 |
| 原因 | 作者能看懂的一句话 |
| 怎样改 | 应改哪个文件，怎样改；对应产品需求各场景“出错时”中的“怎样改” |

提示的具体格式：待补。

### 已定义错误码

| 来源 | 错误码 | 见 |
|---|---|---|
| 命名块 | `BLOCK_DUPLICATE_ID`、`BLOCK_UNCLOSED`、`BLOCK_UNMATCHED_END`、`BLOCK_CROSSED`、`BLOCK_NESTED`、`BLOCK_EMPTY`、`BLOCK_MALFORMED`、`BLOCK_IN_FRAGMENT`、`BLOCK_PARTIAL_CODE_GROUP` | [01](./01-named-blocks.md#出错时) |
| 变量与片段 | `VAR_MISSING`、`VAR_NOT_SCALAR`、`FRAGMENT_NOT_FOUND`、`FRAGMENT_OUT_OF_ROOT`、`FRAGMENT_SYMLINK`、`FRAGMENT_CYCLE`、`LIMIT_EXCEEDED`、`UNSUPPORTED_MARK` | [03](./03-md2md-interfaces.md#出错时) |

### 待定义错误码

以下错误已有文字描述，错误码待补：

| 来源 | 错误情形见 |
|---|---|
| 页面配置与变换 | [02](./02-page-config.md#出错时) |
| 链接与图片 | [02b](./02b-links-and-images.md#出错时) |
| `lock.yaml` 与两版合并 | [04](./04-channels-and-lock.md#出错时) |
| 交接与发布 | [05](./05-publish-handoff.md#出错时) |
| 切换与归属 | [05b](./05b-cutover-and-ownership.md#出错时) |
| 上游更新 | [06](./06-upstream-changes.md#出错时) |
| 站点适配 | [07](./07-site-adaptation.md#出错时) |

## 验收

- 每个错误都有错误码，提示中包含位置、原因与怎样改；对照产品需求各场景的“出错时”逐条核对。
