# WP11 两版合并与 `channel`

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1b　**依赖**：[WP10](./WP10-zdoc-transforms.md) 已合并（[zilliztech/zdoc#900](https://github.com/zilliztech/zdoc/pull/900)）。从最新的 master 开分支　**状态**：未开始

## 目标

一页的 `lock.yaml` 中 `current` 与 `next` 不同时，`shared-docs build` 能生成这一页：两个版本各生成一遍，再合成一份 MDX，相同的部分只出现一次，不同的部分用 `<NextChannel>` 成对输出。Prod 只显示 `current` 的版本，UAT 只显示 `next` 的版本。做完后：

- 两版不同时不再报 “two-version merging requires WP11”，改为合并；
- 两版相同时，输出与现在逐字节相同（6-1）。现在已接入的 12 篇都是这种情况，WP11 合并后下一次 Fetch 不能让它们发生任何变化；
- WP10 已经支持的 `channel: current` / `channel: next` 变换，从此能真正产生两个版本；
- Fetch 不用改：它调用的就是 `shared-docs build`。

WP11 合并后，生产上仍然没有页面会出现两个版本：`next` 只由 WP12 的上游更新 PR 改变。WP11 先把能力和测试准备好。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 6 全文（含“出错时”与取舍） | 四种情况、成对输出的样子、6-1 到 6-7 |
| [技术设计 04](../../design/04-channels-and-lock.md) | 两个版本怎样合并成一页；只在一个通道存在的页面 | 合并规则、front matter、整页通道 |
| [技术设计 02](../../design/02-page-config.md) | 两遍生成与 `channel` | 规则在两遍中怎样执行 |
| [技术设计 09](../../design/09-error-catalog.md) | `MERGE_NESTED_CHANNEL` | 新错误码 |
| [WP10 任务卡](./WP10-zdoc-transforms.md)，以及 [zilliztech/zdoc#900](https://github.com/zilliztech/zdoc/pull/900) 的说明 | 插入点、行号对照、计划审阅的决定 | 两遍生成现在怎样走 |
| [实现指南](../README.md) | 第 2.4、5 节 | 基准输出、规则与 PR 格式 |

zdoc 中还要读：`apps/docs/plugins/next-channel-view.js`（静态产物怎样解析 `<NextChannel>`）、`packages/docs-ui/src/shared/components/NextChannel/`（运行时怎样显示），以及 Fetch 对 `<NextChannel>` 写法的检查（在计划中指出它在哪里）。

## 范围

| 可以改 | 不能改 |
|---|---|
| 新增 `packages/docs-tooling/src/shared-docs/core/merge/`：两版合并，纯计算 | `spec/requirements.json` |
| `adapters/build-page.ts`：用合并取代“两版不同即失败”；去掉按手册重复的预处理（见下文） | `lark/`、`scripts/docs-workflow/`、`.github/workflows/`：Fetch 不用改 |
| `adapters/inspect-page.ts`、`core/transforms/`：见下文的两处跟进 | `apps/docs/`、`packages/docs-ui/`：只读，测试中可以引用 `next-channel-view.js` |
| `commands/build.ts`：在输出摘要中带上合并的备注 | 已有页面的生成结果；`fixtures/golden/` |
| `fixtures/`、`testing/` 中新增的用例 | `shared-docs/` 下的真实页面配置 |
| `spec/pending.json`：删掉下表中的编号 | |
| `packages/docs-tooling/src/shared-docs/README.md`：两版合并一节 | |

## 怎样实现

**合并在哪一步做。** 现在 `buildPage` 对 `current` 与 `next` 各走一遍，得到两份 MDX，不同就记为失败。改为：两遍都成功后合并，再输出一份。合并放在哪一步由计划决定，但要满足：

- 合并后的页面只做一次 MDX 编译校验和产品名检查，`import` 语句按合并后用到的组件生成，不能缺也不能重复；
- 两版的报错各自指出是哪个版本（6-3），这一点现在已经做到，不要丢；
- 两版相同时，走的路径和输出都与现在相同（6-1）。

建议在站点适配之后、`toMdx` 之前合并，计划中说明选择的理由。

**按块比较。** 按技术设计 04：

- 顶层块是：标题、段落、整个列表、表格、提示框、整个代码组（Tabs）、HTML 块。用 Markdown 解析器切块，不要按空行切。
- 相同的块只输出一次。连续的不同块，输出成一对：先 `<NextChannel action="exclude">` 包住 `current` 的块，再 `<NextChannel action="include">` 包住 `next` 的块；只在一边有的块，只输出那一边的标签。对齐用最长公共子序列一类的算法，在计划中说明。
- 标签各占一行，与内容之间空一行，让里面的 Markdown 照常解析。写法要通过 zdoc 现有的 `<NextChannel>` 检查。
- 不在句子或代码组内部切分（6-2）。代码组中只有一种语言变了，也整组成对输出。

**正确性的判据。** 合并结果按两种视图还原，必须分别等于两版各自的输出（只允许块之间空行的差异，在计划中定义清楚）：

- Prod 视图：去掉 `include` 的内容，`exclude` 只去标签。用 `next-channel-view.js` 的 `resolveNextChannelCurrentView`，它也是 `.md` 副本与 `llms.txt` 用的同一个函数，这样同时证明了 6-4；
- UAT 视图：反过来，去掉 `exclude` 的内容，`include` 只去标签。

用这两条做性质测试：随机或成批构造两版原文，合并后两种视图都还原成功。

**front matter（6-6）。** 不能按通道区分。两版不同时用 `current` 的值，并在结果中给出一条备注，说明哪些字段不同。`BuiltPage` 增加 `notes`，`shared-docs build` 把它写进输出摘要。把备注写进 Fetch 的记录文件（`notes`）属于 Fetch，留给 WP9b。

**手写的 `<NextChannel>`（`MERGE_NESTED_CHANNEL`）。** Cloud 内容文件中可以手写 `<NextChannel>`（产品需求场景 6）。它所在的块如果落进工具生成的成对区域，生成失败，报 `MERGE_NESTED_CHANNEL`，指向内容文件中的那一行。不在成对区域内的手写标签原样保留。

**整页通道（6-5）。** 飞书表格为 `NEXT` 或 `RETIRE-IN-NEXT` 的页面，front matter 中已经由 WP9 写入整页通道。确认合并后的页面照样带上，并有测试覆盖；不要改 Fetch。

**`<NextChannel>` 包住的内容能正确显示（6-7）。** 用合并后的 MDX 编译，并在测试中渲染，覆盖包住列表、提示框和代码 Tabs 三种情况。各语言译文中的整页通道属于翻译，不在本工作包；在 PR 中说明怎样由现有的翻译保护覆盖（README 中说翻译把这些标签当作受保护的 JSX）。

**WP10 审阅中提出的两处跟进。**

- `core/transforms/index.ts` 的 `dedent`：以第一个非空行而不是第一行的缩进作为基准。现在内容文件以空行开头时，公共缩进不会被去掉。加一个用例。
- `adapters/build-page.ts`：带变换的页面现在每个手册都重新预处理一遍（最多 8 次 md2md 调用）。改为每个通道只预处理一次，再按手册做产品过滤。输出必须不变，用现有的变换测试证明。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `6-1` | 两版相同：输出与只有一个版本时逐字节相同；没有 `<NextChannel>` |
| `6-2` | 段落、整个列表、表格、提示框、代码组各改一处：每处成对输出，块内不切分；代码组只改一种语言时整组成对 |
| `6-3` | 一条不带 `channel` 的变换只在 `next` 上找不到目标：报错带 `channel: next`；两版都失败时各报一次 |
| `6-4` | 合并结果经 `resolveNextChannelCurrentView` 后等于 `current` 的输出：`next` 独有的内容不出现在静态产物中 |
| `6-5` | 表格为 `NEXT` 的页面合并后仍带整页通道 |
| `6-6` | 两版的 `title` 或 `description` 不同：输出用 `current` 的值，`notes` 中有一条备注 |
| `6-7` | 成对区域包住列表、提示框、代码 Tabs：MDX 编译通过，渲染出两版的内容 |
| `T13` | 共享页部分：两个通道各显示对应版本；Cloud 规则在两个版本上都校验；`channel: next` 的替换只出现在 UAT 视图；`<NextChannel>` 包住列表、提示框、代码 Tabs 时渲染正确。T13 中“过滤”与“提升后不留通道标记”分别已由 WP10 覆盖、留给 WP13，在 PR 中写明 |
| `MERGE_NESTED_CHANNEL` | 内容文件中手写的 `<NextChannel>` 落进成对区域：失败，指向内容文件的行 |

做完后把这些编号从 `spec/pending.json` 中删掉。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；`pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] 编号覆盖检查通过，上表的编号不在 `pending.json` 中
- [ ] **已有页面不变**：用 master 上的 `shared-docs/guides/`（12 篇）和 milvus-docs `v3.0.x`，改动前后各运行一次 `shared-docs build`，输出逐字节相同。在 PR 说明中贴出比较方法与结果
- [ ] **两版的真实例子**：在测试 fixture 中，用 Delete Entities 的原文做一个合成的 `next` 版本（例如改写一段、增加一个参数说明、改一个代码示例），展示合并后的 MDX，以及两种视图的还原结果
- [ ] `pnpm test:replay:shared-pages` 通过
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的格式写。“How to try it”以 `gh pr checkout` 开始，用一个两版不同的合成页面运行 `shared-docs build`，说明应看到的成对输出

## 不做

- 上游更新 PR（改 `next`）：WP12。
- 提升（`current` 改成 `next`、清理 `channel` 规则与成对标记）：WP13。
- Fetch 记录文件中的 `notes`、Fetch 中的任何改动：WP9b。
- 标题改名后的锚点处理（技术设计 04 “标题改名与锚点”）：WP13 提升时处理。
- `docs-ui` 与 `apps/docs` 中 `<NextChannel>` 的显示逻辑：沿用现有实现。

## 已知的坑

- **只改了一个字的段落**：整段成对输出，这是设计如此（6-2），不要做句内的差异。
- **相同的块在两边位置不同**：例如一段被移到了后面。对齐算法要给出稳定、可解释的结果；在计划中说明这种情况的输出。
- **标题成对出现时的锚点**：旧标题与新标题各有一个锚点，目录中会同时列出两个。zdoc 现有的 NEXT 内容锚点问题见 [zilliztech/zdoc#864](https://github.com/zilliztech/zdoc/issues/864)，不在本工作包修。确认两个锚点不重复；重复时在计划中提出怎样处理。
- **空行**：两种视图还原时，`exclude` / `include` 标签周围的空行会留下多余的空行。判据中要明确怎样比较，不能为了让测试通过而放宽到忽略所有空白。
- **代码块中的通道指令**：zdoc 的代码块中有 `# next-channel-start` 这类指令（`next-channel-view.js` 处理它们）。WP11 不生成这种指令，按整个代码组成对；原文或内容文件中出现时，在计划中说明怎样处理。
- 要另起进程的测试，按 [#824](https://github.com/zilliztech/zdoc/pull/824) 设 120 秒的文件级时限。
