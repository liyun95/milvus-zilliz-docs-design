# WP10 变换：命名块、语言、代码行三级的 add / replace / remove

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1b　**依赖**：[WP4](./WP4-zdoc-site-adaptation.md)、[WP8](./WP8-zdoc-build-and-validate.md)、[WP9](./WP9-zdoc-fetch-handoff.md) 已合并（WP9a [zilliztech/zdoc#863](https://github.com/zilliztech/zdoc/pull/863)，commit [`8289d74`](https://github.com/zilliztech/zdoc/commit/8289d7451b85a710ab5f075640a7ebec63752739)）。从最新的 master 开分支　**状态**：已合并（[zilliztech/zdoc#900](https://github.com/zilliztech/zdoc/pull/900)）

## 目标

`page.yaml` 中的 `transforms` 可以用了：对 Milvus 原文的命名块、代码组中的一种语言、一种语言中连续的几行，做增加、替换、删除，新内容来自同一目录的 Cloud 内容文件或配置中的 `content.lines`。做完后：

- `shared-docs build` 不再拒绝非空的 `transforms`，按规则执行，任何一条不成立时这一页生成失败；
- Cloud 内容文件与原文经过同样的处理：变量、片段、链接、产品过滤、站点适配、产品名检查；
- Fetch 不用改：它调用的就是 `shared-docs build`，已激活页面的变换随之生效；
- **没有 `transforms` 的页面，生成结果逐字节不变。** 现在已有 5 篇页面在 Fetch 中由 Git 生成（Delete Entities 已激活，另外 4 篇正在激活），WP10 合并后，下一次 Fetch 不能让它们发生任何变化。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 4 全文（含“出错时”与例子）；场景 6 中 `channel` 的写法 | 作者怎样写、系统行为 4-1 到 4-6、报错 |
| [技术设计 01](../../design/01-named-blocks.md) | 标记的写法；块的类型 | 命名块怎样定位，什么算代码组 |
| [技术设计 02](../../design/02-page-config.md) | 变换的执行；出错时 | 代码行的匹配与缩进、两遍生成、冲突规则 |
| [技术设计 07](../../design/07-site-adaptation.md) | 代码 Tabs | 加了语言后 Tabs 怎样重新生成 |
| [技术设计 09](../../design/09-error-catalog.md) | “变换”一节 | 16 个错误码 |
| [WP8 走读](../walkthroughs/WP8.md)、[WP9 走读](../walkthroughs/WP9.md) | 生成命令的各个阶段；Fetch 怎样调用生成 | 变换插在哪里 |
| [实现指南](../README.md) | 第 2.4、5 节 | 基准输出、规则与 PR 格式 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新增 `packages/docs-tooling/src/shared-docs/core/transforms/`：变换的校验与执行，纯计算 | `spec/requirements.json` |
| `core/config.ts`、`core/types.ts`：`transforms` 各项的 schema | `lark/`、`scripts/docs-workflow/`、`.github/workflows/`：Fetch 不用改。真的需要改时，先在计划中说明 |
| `adapters/inspect-page.ts`、`adapters/build-page.ts`：接入变换，删掉“Nonempty transforms require WP10”的拒绝 | 已有页面的生成结果；`fixtures/golden/` |
| `commands/build.ts` 的 `readSharedDocs`：读入页面目录中的 Cloud 内容文件 | WP4、WP5、WP6 的规则本身：只把内容文件接进这些阶段 |
| `fixtures/`、`testing/` 中新增的用例 | `shared-docs/` 目录下的真实页面配置 |
| `spec/pending.json`：删掉下表中的编号 | |
| `packages/docs-tooling/src/shared-docs/README.md`：变换一节 | |

## 怎样实现

**插入点。** 在 `inspectPage` 中，每个通道按下面的顺序处理：

1. `parseBlocks`、`inventoryBlocks` 之后，在**带标记的原文**上执行变换：用块清单定位命名块，按块的类型和语言执行，插入内容文件或 `content.lines`；
2. 再去掉命名块标记；
3. 再对整页（包括插入的内容）运行 `md2md.preprocess`，展开变量与片段。

这样内容文件中的 `{{var.xxx}}` 取 Cloud 的值，后面的链接、站点适配、产品名检查也都按原来的方式处理插入的内容，不用另写一套。

**三级目标。** 按产品需求场景 4 的对照表：

| 目标 | 怎样定位 | 要注意的 |
|---|---|---|
| 整个命名块 | 块清单中的起止行 | 替换代码组时，内容文件写完整的代码组，多语言时含切换栏 |
| 代码组中的一种语言 | 块中的代码组，按代码块的语言 | 增加语言时，把新的代码块放进代码组，顺序交给 WP4 的 Tabs 规则；先确认 WP4 是否只看代码块、不看切换栏的文字，在计划中写明 |
| 一种语言中连续的几行 | 这种语言的代码块内部 | 匹配与缩进按技术设计 02“代码行的匹配”；列表中缩进的代码块也要对 |

**语言名。** `target.language` 与代码块的语言名比较时，按 `presentation/cloud-sdk-tabs.yaml` 中的 `aliases` 归一，例如 `cpp` 与 `c++` 视为同一种语言。在计划中写明。

**Cloud 内容文件。**

- 只能是 `page.yaml` 所在目录中的文件，路径用 `realpath` 检查，不能用 `..` 或符号链接逃出这个目录（`TRANSFORM_CONTENT_NOT_FOUND`）。
- 不能有命名块标记，也不能有手写的 `<Tabs>`、`<TabItem>`、`<Admonition>`（`TRANSFORM_CONTENT_MARKUP`）。
- **产品过滤**：沿用 zdoc 飞书侧的写法和语义（`lark/larkDocWriter.js` 的 `categorize_node`、`__filter_content`）。`<include target="…">`、`<exclude target="…">` 与 `</include>`、`</exclude>` 各占一行，可以嵌套。飞书侧的当前目标是 Guides `zilliz.saas`、BYOC `zilliz.paas`，按 `.` 拆成词后逐个比较，所以标签中写一个词，如 `saas`、`paas`、`zilliz`；嵌套按栈正确配对，不照搬 `categorize_node` 中提前结束跳过的计数写法；标签不配对时报 `TRANSFORM_CONTENT_MARKUP`。只在插入的内容上执行，按手册分别执行。实现时不要引用 `lark/`，在 `core/` 中按同样的语义重写，并用测试对照飞书侧的结果。
- 图片：外部图片地址交给现有的图片阶段处理。页面目录中的图片文件这次不做，遇到时报 `TRANSFORM_CONTENT_MARKUP`，指向内容文件中的那一行，说明可以改用外部图片地址；不能静默丢掉。

**`channel`。** 只做到产品需求与技术设计 02 已经写明的部分：

- 值只能是 `current` 或 `next`，页面在那个通道中必须存在，否则报 `TRANSFORM_CHANNEL_INVALID`；
- 第一遍（`current`）只执行不带 `channel` 和 `channel: current` 的规则，第二遍（`next`）同理；
- 冲突按通道分别检查，不带 `channel` 的规则同时计入两个通道。

两遍生成结果不同时，`buildPage` 现在会报“two-version merging requires WP11”。这个行为保持不变，两版合并留给 WP11。

**报错的位置。** 原文中的问题指向 milvus-docs 中的文件和行号，现在 `originalPageLine` 已经这样做。插入内容中的问题（链接解析不了、产品名、Tabs）要指向 Cloud 内容文件和它的行号；`content.lines` 中的问题指向 `page.yaml` 中那一项。插入内容之后，后面阶段的行号与原文对不上，要维护一张行号对照表，不能让报错指到错误的文件。对照表只覆盖变换、去掉标记、产品过滤这几步；md2md 展开变量与片段后，行数不变时行号要准确，行数变了时不比现在对原文的处理差。不另写一套 md2md 的展开逻辑来追踪行号；要做到完全准确，需要 md2md 提供输出的行号对照，列为后续工作。

**记录文件。** Fetch 写的记录文件已经列出 `shared-docs/guides/` 下的全部文件（`inputs.zdoc.files`），内容文件应当自动包括在内。用一个带内容文件的页面确认这一点；没有包括时，在 PR 中说明，不要自己改 Fetch。

## 计划审阅的决定

在 [liyun95/zdoc#13](https://github.com/liyun95/zdoc/pull/13) 中审定，以 PR 中的[裁决评论](https://github.com/liyun95/zdoc/pull/13#issuecomment-6459791357)为准：

| 问题 | 决定 |
|---|---|
| 产品过滤的目标 | 只按飞书侧的拆词语义，标签中写一个词；不接受 `zilliz.paas` 这种带点的完整目标 |
| 同一位置多条 `add` | 块的前后、同一组定位行的前后都允许，按列表顺序输出；同一种语言增加两次、重复的 `replace` / `remove`、范围相交、上下级重叠报 `TRANSFORM_CONFLICT` |
| 删除语言 | WP4 不改：只检查必须有的语言，默认语言不在时取第一种可用的语言。删掉代码组中仅剩的一种语言报 `TRANSFORM_TARGET_KIND`，提示改为删除整块 |
| T04 的证据 | 真实的 OpenAI Python 原文（只加命名块标记）加上标明为合成的多语言用例；PR 中写明哪些部分由合成用例覆盖，真实的多语言证据在 C3 内容对齐后补 |
| `shared-docs inspect` | 仍只看原文，不改 `commands/inspect.ts`，在 README 中说明 |
| 页面目录中的图片 | `TRANSFORM_CONTENT_MARKUP`，不用 `IMAGE_NOT_IN_COMMIT` |
| 合并时机 | 第一批 4 篇在 UAT 验收后，再开上游 PR 并合并 |

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `4-1` | 一页中有一条合法、一条非法的变换：整页失败，合法的那条也不执行，报出非法那条的错误 |
| `4-2` | Markdown 块上写 `language`，或 `lines` 没有 `language`：`TRANSFORM_TARGET_KIND`；单个代码块和带切换栏的代码组都按代码组处理 |
| `4-3` | 定位行缩进 8 个空格、新内容有两级缩进：写入后分别是 8 和 12 个空格；Tab 缩进的原文写入后仍是 Tab；替换、删除后不留多余空行 |
| `4-4` | 给代码组加 `shell`：Tabs 按规则排序，显示为 Zilliz CLI；删掉 Python：`TABS_REQUIRED_MISSING` |
| `4-5` | 内容文件中的变量取 Cloud 的值；片段展开；Milvus 写法的提示框转成 `Admonition`；`.md` 链接按 `links.yaml` 改写；`<include target="paas">` 中的内容只出现在 BYOC 的输出中 |
| `4-6` | 同一份原文，`page.yaml` 中有没有变换，md2md 给 Milvus 站点的输出都相同 |
| `T04` | 用 OpenAI 的凭证参数作真实用例，在每种语言中验证代码行的 `replace` 与 `add`，覆盖 T04 列出的全部失败情况。fixture 在 [`fixtures/pilots/openai`](https://github.com/zilliztech/zdoc/tree/master/packages/docs-tooling/src/shared-docs/fixtures/pilots/openai) 的原文上加命名块标记，只放在测试 fixture 中 |
| 16 个错误码 | `TRANSFORM_TARGET_NOT_FOUND` 到 `TRANSFORM_CHANNEL_INVALID`，以及 `LINE_NOT_FOUND`、`LINE_AMBIGUOUS`、`LINE_TOO_MANY`、`LINE_INVALID`：每个至少一个失败用例，放在 `fixtures/errors/` 下，断言错误码、文件与行号 |

做完后把这些编号从 `spec/pending.json` 中删掉。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；`pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] 编号覆盖检查通过，上表的编号不在 `pending.json` 中
- [ ] **已有页面不变**：用 master 上的 `shared-docs/guides/`（5 篇页面）和 milvus-docs `v3.0.x`，分别在改动前后运行 `shared-docs build`，输出逐字节相同。在 PR 说明中贴出比较方法与结果
- [ ] `pnpm test:replay:shared-pages` 通过
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的格式写。“How to try it”以 `gh pr checkout` 开始，用一个合成的页面（带一个命名块替换和一处代码行替换）运行 `shared-docs build`，说明应看到的输出和一个故意写错时的报错

## 不做

- 两版合并、`<NextChannel>` 的生成、提升时清理 `channel` 规则：WP11、WP13。
- 页面目录中的图片文件：等图片存储的检查（P1-2）完成后再定。
- 行号、正则、全文搜索等其他定位方式；移动、复制、嵌套的变换（产品需求场景 4 的“不做”）。
- 修改 Fetch、工作流或 milvus-docs 中的真实页面。
- 基准输出：OpenAI 的基准输出要等 C3 内容对齐后由推动者确认，这次只用断言测试。

## 已知的坑

- **块清单的行号**：`inventoryBlocks` 的 `startLine` 是标记后的第一行（从 0 开始），`endLine` 与它的约定不同。先读懂再用，并在测试中覆盖块在文件开头和结尾的情况。
- **执行顺序**：同一个块上的多条规则（比如前后各加一段）要按列表顺序输出；先算好全部位置再统一写入，不要边改边算，否则后面的行号会偏。
- **对刚插入的内容再变换**：例如先给代码组加了 `java`，又对 `java` 写了代码行规则。这种情况报 `TRANSFORM_ON_INSERTED`，不要按插入后的内容去匹配。
- **一个代码组中同一种语言出现两次**（按别名归一后）：语言级和代码行级的规则都无法确定目标，报 `ADAPT_UNSUPPORTED_MARKUP`，指向第二个代码块。
- **`content.lines` 与 YAML**：`|` 块的末尾有换行，比较和写入前先去掉；行内的注释符号（`#`、`//`）是代码的一部分，不能当成 YAML 注释。
- **产品名检查的来源**：WP6 按来源（原文、片段、变量、内容文件）报告问题，类型中已有 `content-file`。内容文件中出现 `Milvus` 时，报告的来源要是内容文件。
- 要另起进程的测试，按 [#824](https://github.com/zilliztech/zdoc/pull/824) 设 120 秒的文件级时限。
