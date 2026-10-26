# 09 错误目录

对应的产品需求见[产品需求](../prd.md#5-场景)各场景的“出错时”，以及[第 6 节](../prd.md#6-对现有能力的要求)中的“出错”：一律失败，说明原因与应改的文件，不静默跳过。本篇给每一种错误一个错误码，并约定报错的结构与给作者的提示。

**参与方**：md2md、zdoc 生成、zdoc 新增工作流（报错方）；文档工程师（读提示）。

**状态**：草稿，待工程维护者确认。01 与 03 的错误码已随接口定义；其余错误码为本篇新增的建议，错误情形取自各篇的“出错时”。

## 约定

### 错误的结构

zdoc 的错误与 md2md（[03](./03-md2md-interfaces.md#返回)）用同样的结构，再加三个字段：

| 字段 | 说明 |
|---|---|
| `code` | 错误码，大写字母、数字与下划线，按来源加前缀 |
| `message` | 一句话说明原因 |
| `file`、`line` | 出错的文件与行号（从 1 开始）；指向作者要改的文件，定位不到行时只给文件 |
| `detail` | 补充信息，如循环引用的引用链、找不到的锚点 |
| `page` | 页面标识（zdoc 新增） |
| `channel` | 出错的版本：`current`、`next`，或两个版本都出错时为 `both`（zdoc 新增） |
| `fix` | 应改哪个文件、怎样改（zdoc 新增） |

同一页的错误一次全部报出，不在第一个错误处停下；一页失败不影响其他页的检查。

### 给作者的提示

PR 检查的摘要与上游更新 PR 的报告，按页分组，每个错误一段：

```
✗ LINE_NOT_FOUND  openai · next 版本
  位置：shared-docs/guides/pages/openai/page.yaml 第 18 行
        → 原文 define-function-code（python）
  原因：lines 在 python 代码中找不到
  怎样改：上游可能改了这一行。原规则加 channel: current，
          再按新原文复制一条规则，加 channel: next
```

提示语言沿用 zdoc 现有工具的输出语言，由 zdoc 维护者确定。

### 错误码

**命名块**（md2md 报，见 [01](./01-named-blocks.md#出错时)）：`BLOCK_DUPLICATE_ID`、`BLOCK_UNCLOSED`、`BLOCK_UNMATCHED_END`、`BLOCK_CROSSED`、`BLOCK_NESTED`、`BLOCK_EMPTY`、`BLOCK_MALFORMED`、`BLOCK_IN_FRAGMENT`、`BLOCK_PARTIAL_CODE_GROUP`。

**变量与片段**（md2md 报，见 [03](./03-md2md-interfaces.md#出错时)）：`VAR_MISSING`、`VAR_NOT_SCALAR`、`FRAGMENT_NOT_FOUND`、`FRAGMENT_OUT_OF_ROOT`、`FRAGMENT_SYMLINK`、`FRAGMENT_CYCLE`、`LIMIT_EXCEEDED`、`UNSUPPORTED_MARK`。

**页面配置**（见 [02](./02-page-config.md#出错时)）

| 错误码 | 何时出现 | 怎样改 |
|---|---|---|
| `CONFIG_PAGE_ID_INVALID` | 页面目录名不符合 slug 规则 | 改目录名 |
| `CONFIG_FIELD_MISSING` | 缺少必填字段 | 补字段 |
| `CONFIG_SYNTAX_INVALID` | `page.yaml` 或 `source.yaml` 不是合法的 YAML，或 `Variables.json` 不是合法的 JSON | 按报错的行号改正语法 |
| `CONFIG_VARIABLES_INVALID` | `Variables.json` 的顶层不是对象，或同一层中有只差大小写的两个键，如 `Product` 与 `product` | 改正 `Variables.json`；改好之前所有共享页都生成失败 |
| `CONFIG_FIELD_UNKNOWN` | 未知的字段、动作或 `schema_version` | 删去或改正 |
| `CONFIG_SOURCE_NOT_FOUND` | `source.file` 在该版本中不存在，包括上游改名或删除了原文 | 改 `source.file`；原文被删除时考虑下线 |
| `CONFIG_MANUAL_UNKNOWN` | `publish[].manual` 不是 zdoc 已有的手册 | 改手册 ID |
| `CONFIG_PATH_UNKNOWN` | Phase 1 中，`publish[].path` 在该手册中没有飞书节点生成的页面，或飞书表格快照中没有这一页的记录 | 改 `publish[].path`；全新的页面先在飞书表格与目录中建好记录与节点 |
| `CONFIG_BETA_INVALID` | `metadata.beta` 不是 zdoc 标签定义中的值，或写了 `BYOC` | 改为 zdoc 现有的值，见[产品需求场景 3](../prd.md#场景-3接入一页) |

**变换**（见 [02](./02-page-config.md#出错时)）

| 错误码 | 何时出现 | 怎样改 |
|---|---|---|
| `TRANSFORM_TARGET_NOT_FOUND` | 目标命名块或语言不存在，包括上游改名或删除了命名块 | 改规则中的 ID 或语言，或回上游加命名块 |
| `TRANSFORM_TARGET_KIND` | 在 Markdown 块上写了 `language`，或 `lines` 没有 `language` | 改目标 |
| `TRANSFORM_LANGUAGE_EXISTS` | 给代码组增加的语言已经存在 | 改用 `replace` |
| `TRANSFORM_LANGUAGE_ABSENT` | 替换或删除的语言不存在 | 检查语言名，或改用 `add` |
| `TRANSFORM_POSITION_MISSING` | 块旁或代码行旁的 `add` 没写 `position` | 补 `before` 或 `after` |
| `TRANSFORM_POSITION_UNEXPECTED` | 给代码组增加语言、`replace`、`remove` 时写了 `position` | 删去 |
| `TRANSFORM_CONTENT_UNEXPECTED` | `remove` 提供了内容 | 删去 `content` |
| `TRANSFORM_CONTENT_NOT_FOUND` | 内容文件不存在，或路径在页面目录之外 | 改路径 |
| `TRANSFORM_CONTENT_MARKUP` | 内容文件中有命名块标记或手写的 Cloud 组件 | 删去，改用 Milvus 写法 |
| `TRANSFORM_CONFLICT` | 同一通道中同一目标被多次变换，或不同级别的变换重叠 | 合并成一条，或改用更大一级的目标 |
| `TRANSFORM_ON_INSERTED` | 对本轮刚插入的内容再做变换 | 直接修改内容文件 |
| `TRANSFORM_CHANNEL_INVALID` | `channel` 不是 `current` 或 `next`，或页面在该通道中不存在 | 改 `channel` |
| `LINE_NOT_FOUND` | `lines` 在目标语言中找不到 | 重新从原文复制；上游改了这一行时，加一对 `channel` 规则 |
| `LINE_AMBIGUOUS` | `lines` 出现多次 | 多复制一行，让它只出现一次 |
| `LINE_TOO_MANY` | `lines` 超过 5 行 | 改为替换整种语言 |
| `LINE_INVALID` | `lines` 或 `content.lines` 中有空行、三个反引号或命名块标记 | 删去 |

**链接与图片**（见 [02b](./02b-links-and-images.md#出错时)）

| 错误码 | 何时出现 | 怎样改 |
|---|---|---|
| `LINK_UNRESOLVED` | Milvus 站内页面查不到 Cloud 的对应页 | 在 `links.yaml` 中补一行；`detail` 中附有候选 |
| `LINK_ROOT_PATH` | 出现以 `/` 开头的站内路径 | 在 `links.yaml` 中处理，或回上游改成完整地址 |
| `LINK_UNKNOWN_FORM` | 链接不属于任何一类，如漏写 `.md` | 回上游修正 |
| `LINK_MAP_INVALID` | `links.yaml` 格式不对：不是合法的 YAML，同一个 Milvus 页面登记了两次，键不是 `.md` 文件名，或值既不是页面标识也不是 `https://milvus.io/` 开头的地址 | 改正 `links.yaml`；改好之前所有共享页都生成失败 |
| `LINK_TARGET_ABSENT` | 链接指向的共享页在这个版本中不存在 | 回上游修正，或让两页一起采用 |
| `ANCHOR_NOT_FOUND` | 指向共享页标题的锚点找不到对应标题 | 回上游修正；标题改名见 [04](./04-channels-and-lock.md#标题改名与锚点) |
| `IMAGE_FETCH_FAILED` | 外部图片下载失败或不存在 | 回源头修正 |
| `IMAGE_NOT_IN_COMMIT` | 仓库内的图片在该版本中不存在 | 回上游修正 |
| `IMAGE_CHANGED_DURING_READ` | 同一图片两次读取内容不同 | 重试 |

**版本记录与两版合并**（见 [04](./04-channels-and-lock.md#出错时)）

| 错误码 | 何时出现 | 怎样改 |
|---|---|---|
| `LOCK_INVALID` | 没有 `lock.yaml`，或字段缺失、格式不对 | 删掉 `lock.yaml` 让工具重写；不要手改 |
| `LOCK_COMMIT_NOT_FOUND` | commit 不存在，或不在跟踪分支的历史上（如分支历史被改写） | 人工处理 |
| `LOCK_ORDER` | `current` 不是 `next` 的祖先 | 人工处理 |
| `LOCK_NONE_UNSUPPORTED` | `current` 或 `next` 写了 `none`（Phase 1 不启用） | 删掉 `lock.yaml` 让工具重写；整页通道在飞书表格中设置 |
| `LOCK_FORK_PR` | 接入 PR 来自 fork，工具无法写入 | 改从 zdoc 仓库内的分支提交 |
| `MERGE_NESTED_CHANNEL` | Cloud 内容文件中手写的 `<NextChannel>` 落在工具生成的成对区域内 | 改用变换的 `channel` |

**产品名**（见 [07](./07-site-adaptation.md#产品名检查)）

| 错误码 | 何时出现 | 怎样改 |
|---|---|---|
| `PRODUCT_NAME_FOUND` | 生成的页面中出现 `check` 中的写法，且不在 `allow` 中 | 产品名、连接地址、用户名与密码：回 milvus-docs 改成变量，确实要保留时在 `allow` 中补一行；`milvus.yaml` 这类只有自部署才有的写法：用变换删掉或替换这一段 |
| `PRODUCT_NAMES_INVALID` | `product-names.yaml` 格式不对，或 `allow` 中有单个词 | 改正规则文件 |

提升时不符合条件的页面（页面不存在、两个版本已相同）不算错误，在运行摘要中列出：`PROMOTE_PAGE_NOT_FOUND`、`PROMOTE_NOTHING_TO_DO`。

**站点适配**（见 [07](./07-site-adaptation.md#出错时)）

| 错误码 | 何时出现 | 怎样改 |
|---|---|---|
| `TABS_UNKNOWN_LANGUAGE` | 代码组中有 Tabs 规则中没有的语言，包括多语言代码组中没写语言名的代码块 | 在规则中补充，或用变换删除这种语言 |
| `TABS_REQUIRED_MISSING` | 多语言代码组缺少必须有的语言，或变换删除了它 | 用变换补上，或回上游补齐 |
| `TABS_RULES_INVALID` | Tabs 规则文件格式不对 | zdoc 维护者修正 |
| `ADAPT_UNSUPPORTED_MARKUP` | 提示框写法不在支持范围内；出现代码组切换栏与提示框之外的 `<div>`，如 Milvus 站点专用的版式、按 SDK 语言显示的说明；同一个多语言代码组中一种语言出现两次 | 回上游改为支持的写法 |
| `ADAPT_MDX_INVALID` | 修补后仍不能编译为 MDX | 回上游修正写法 |

**发布与切换**（见 [05](./05-publish-handoff.md#出错时)、[05b](./05b-cutover-and-ownership.md#出错时)）

| 错误码 | 何时出现 | 结果 |
|---|---|---|
| `PUBLISH_IMAGE_UPLOAD_FAILED` | 图片上传或上传后的摘要核对失败 | 这次运行的 Guides 不写 dev，与飞书图片上传失败时相同 |
| `PUBLISH_REGEN_MISMATCH` | 重新生成的结果与记录文件不一致，或有 PR 修改了 dev 中的生成结果 | 这一页保留 dev 中现有的版本，或该 PR 检查失败；指出应改的源文件 |
| `RECOVER_INPUT_MISSING` | 恢复时源、配置或图片缺失 | 恢复失败，不回退到最新版本 |
| `OWNERSHIP_DUPLICATE_PATH` | 同一个输出路径既有飞书页面又有 Git 页面 | 生成失败 |
| `OWNERSHIP_PATH_MISMATCH` | 飞书记录的发布目标或路径与 `publish` 不一致 | 该页生成失败 |
| `OWNERSHIP_WRITE_DENIED` | 飞书任务试图改写或删除已切换的页面 | 失败，页面保持不变 |
| `ACTIVATE_CHECK_FAILED` | 比较时，或 `Docs` 换成页面目录地址后的 Fetch 中，激活前的检查不通过，包括被其他飞书页面链接的锚点在 Git 版中找不到；`detail` 中列出是哪一项 | 比较时：不应激活；Fetch 中：这一页保留现有版本 |
| `OWNERSHIP_CONFIG_MISSING` | 飞书表格中记录的 `Docs` 既不是飞书文档链接，也不是存在的页面目录地址 | 这一页生成失败，保留现有版本；改正链接、补回目录，或先删表格记录 |
| `OWNERSHIP_REVERTED` | `active.json` 中的页面，`Docs` 被改回飞书链接 | Fetch 失败，页面保持 Git 版；把 `Docs` 改回页面目录地址 |
| `RETIRE_DIR_LEFTOVER` | 表格记录已删除，页面目录还在 | 不算错误，不生成这一页，运行摘要中提示删除目录 |
| `IMAGE_SOURCE_CHANGED` | 已记录的图片在原地址的内容变了（同名覆盖） | 不算错误，沿用记录中的图片，通知文档工程师 |

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么与 md2md 用同一种结构。** zdoc 调用 md2md 后，把它的错误原样并入自己的错误列表，作者看到的提示格式一致，不用区分错误来自哪个工具。

**为什么一次报出全部错误。** 作者一次就能改完，不必反复提交、每次只看到下一个错误。

**为什么提升时的不符合条件不算错误。** 选“全部待提升”时，有的页本来就无需提升；整次运行失败会拖住其他页面。

</details>

## 验收

- 每个错误都有错误码，提示中包含页面、版本、位置、原因与怎样改；对照产品需求各场景的“出错时”逐条核对。
