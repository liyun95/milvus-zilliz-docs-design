# WP4 站点适配

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP3](./WP3-zdoc-read.md)：WP3a 已合并（[zilliztech/zdoc#796](https://github.com/zilliztech/zdoc/pull/796)，commit [`5844587`](https://github.com/zilliztech/zdoc/commit/5844587037d5397e8ebd1510235db5d8592584d7)）；WP3b 已合并（[zilliztech/zdoc#800](https://github.com/zilliztech/zdoc/pull/800)，commit [`31a9b54`](https://github.com/zilliztech/zdoc/commit/31a9b54176c9adc50515f84a559b4082700b6620)），可以开工。可与 [WP5](./WP5-zdoc-links-images.md)、[WP6](./WP6-zdoc-product-names.md) 同时进行　**状态**：未开始

## 目标

做完后，给定一个版本、一个手册的页面 Markdown（WP3 已展开变量与片段），zdoc 能把它转换成 Cloud 站点的 MDX：

- 多语言代码组按 Tabs 规则重新生成 `<Tabs>`；
- 提示框换成 `<Admonition>`；
- 按页面配置生成 front matter；
- 每个标题都有显式锚点；
- 经过 zdoc 现有的 MDX 修补后能编译。

不认识的写法一律报错，不原样放过。

本工作包只提供纯计算的函数和测试，不接入任何命令；与读取、链接与图片、产品名检查接成一条生成命令是 WP8 的事。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 2：系统行为 2-6；场景 3：`page.yaml` 的 `metadata` 字段、系统行为 3-5 | 行为 |
| [技术设计 07](../../design/07-site-adaptation.md) | 除“产品名检查”外的全部 | 转换规则、Tabs 规则文件、出错时 |
| [技术设计 01](../../design/01-named-blocks.md) | 识别规则 | 代码组的定义；语言缺失与重复 |
| [技术设计 09](../../design/09-error-catalog.md) | 错误的结构、站点适配 | 错误码 |
| [实现指南](../README.md) | 2.4（只读“内容对齐之前”一段）、2.5、第 5 节 | 临时结果、错误样例表、规则 |
| [WP0 走读](../walkthroughs/WP0.md) | 全文 | 目录、替身与测试工具 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新建 `core/site/`：Tabs、提示框、front matter、标题锚点的纯计算 | `core/types.ts`、`adapters/types.ts`：WP3 是主人，要加共用类型先在 PR 中提出；本工作包的类型放在 `core/site/` 中 |
| `core/blocks.ts`：只导出代码块与代码组的识别，供 `core/site/` 使用，不改行为；WP3b 的测试全部保持通过 | `packages/docs-tooling/src/mdx/`、`lark/`：只调用，不修改 |
| 新建 `adapters/mdx.ts`：调用 zdoc 现有的 [`packages/docs-tooling/src/mdx`](https://github.com/zilliztech/zdoc/blob/master/packages/docs-tooling/src/mdx/index.ts)（`applyMdxPatches`、`validateMdxStructure`）与 `@mdx-js/mdx` 编译 | `commands/`、`cli-main.ts`：接入命令归 WP8 |
| 新建 `fixtures/site/`：Tabs 规则文件 `cloud-sdk-tabs.yaml`（按技术设计 07 的 Phase 1 建议值）、合成的小样例 | 链接、锚点换算与图片（WP5）；产品名检查（WP6） |
| 新建 `fixtures/site-errors/<样例>/`、`testing/site/` | `fixtures/golden/`：内容对齐前不产生基准输出 |
| `spec/pending.json`：删掉本工作包的编号；`3-4` 改为 `"WP8"` | `spec/requirements.json`：WP5 会复制带新错误码的版本，本工作包不复制 |

## 接口

```ts
// core/site/：纯计算
parseTabsRules(yamlText, context): { rules: TabsRules } | { errors }   // TABS_RULES_INVALID
adaptPage(input: {
  markdown: string                  // 一个版本的页面，含原文的 front matter；变量与片段已展开
  pageId: string
  manual: 'guides' | 'guides-byoc'
  metadata?: PageConfig['metadata'] // page.yaml 中的 metadata
  tabsRules: TabsRules
  betaValues: readonly string[]     // 与 WP3 相同：DOC_HEADING_TAGS 去掉 BYOC，由调用方传入
  headingAnchor: (headingMarkdown: string) => string   // 标题 → Cloud 锚点；算法由 WP5 提供，WP8 接入
  navigation?: { sidebar_label?: string; sidebar_position?: number }   // 由 WP8 从飞书节点读出
  context: DiagnosticContext        // page、channel、file（页面原文路径）
}): { markdown: string; components: ('Admonition' | 'Tabs' | 'TabItem')[] } | { errors }

// adapters/mdx.ts：修补并编译
toMdx(adapted, context): Promise<{ mdx: string } | { errors }>          // ADAPT_MDX_INVALID
```

- **Tabs**：处理页面中的每个多语言代码组，不只是命名块中的，包括列表中缩进的。识别规则用 `core/blocks.ts` 已有的实现，不另写一份。
  - 只有一种语言的代码组输出普通代码块。
  - 不在代码组中的代码块照原样输出。
  - `aliases` 只在代码组中换算。
- **front matter**：按技术设计 07 的表生成，原文 front matter 中的其他字段不输出。
  - 原文的 front matter 用 `core/yaml.ts` 读。
  - 后缀规则与 zdoc 飞书转换器中的 [`__title_suffix`](https://github.com/zilliztech/zdoc/blob/master/packages/docs-tooling/src/lark/larkDocWriter.js) 相同。在测试中直接调用它比对，只比 `guides` 与 `guides-byoc` 两种路径。
  - `channel` 暂不输出，整页通道归 WP13。
- **标题锚点**：除一级标题外，每个标题输出锚点，`id` 由 `headingAnchor` 算出；写法以 dev 上现有页面为准，见技术设计 07 的“标题锚点”。
  - 同一页中重复的锚点，第一个不变，之后依次加 `-1`、`-2`。
  - 代码块中的 `#` 行不是标题。
  - 测试中传入一个简单的替身函数。
- **组件引入**：输出开头按用到的组件加 `import`，写法与飞书转换器相同：`import Admonition from '@theme/Admonition';`、`import Tabs from '@theme/Tabs';`、`import TabItem from '@theme/TabItem';`。
- **错误**：结构同 WP3。`file` 是页面原文的路径，`line` 是输入 Markdown 中的行号，`detail.text` 附上这一行的内容。片段展开后行号可能与原文不同，WP8 接入时再决定是否换算。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `2-6` | 切换栏中的链接文字、顺序与代码块不一致时，`<Tabs>` 仍按代码块与规则生成：顺序按规则、只列实际有的语言、`defaultValue` 按规则；`cpp`、`curl` 换成 `c++`、`bash` |
| `3-5` | `guides` 加 `\| Cloud`、`guides-byoc` 加 `\| BYOC`；`metadata` 中写了 `title`、`description` 时用它；与 `__title_suffix` 比对 |
| `TABS_UNKNOWN_LANGUAGE` | 规则中没有的语言；多语言代码组中没写语言名的代码块 |
| `TABS_REQUIRED_MISSING` | 多语言代码组缺少 `python` |
| `TABS_RULES_INVALID` | `value` 重复、`default` 不在 `languages` 中、不是合法的 YAML |
| `ADAPT_UNSUPPORTED_MARKUP` | `alert notes`、`alert alert-info`、`admonition note`；`start_card_container` 等版式 `div`；同一代码组中一种语言出现两次 |
| `ADAPT_MDX_INVALID` | 修补后仍不能编译的输入 |

每个错误码一个错误样例（实现指南 2.5），断言 `code`、`file`、`line`、`page`、`channel`。

另外，三篇试点页的原文（`fixtures/pilots/`，经 WP3 的读取与预处理）都要能转换并编译通过。这是临时结果：测试只断言编译成功和 Tabs 的语言列表，不比较全文，不写入 `fixtures/golden/`。

做完后把上表的编号从 `spec/pending.json` 中删掉，并把 `3-4` 的归属改为 `"WP8"`：它要求链接、锚点与图片也可用，要在 WP8 接成整条流水线后才能测。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；上表的编号不在 `pending.json` 中，`3-4` 归 WP8
- [ ] `pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] WP3b 的测试没有改动且全部通过
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写。“How to try it”从 `gh pr checkout` 开始，不写本机路径，演示两件事：把 Delete Entities 转换成 MDX，看到 `<Tabs>` 与 front matter；把 Tabs 规则中的 `default` 改成不存在的语言，看到 `TABS_RULES_INVALID`。可以像 WP3b 的 `testing/demo.ts` 那样写一个小脚本，在临时目录中运行

## 不做

- 链接、锚点换算、图片地址（WP5）；产品名检查（WP6）；接入命令（WP8）。
- 变换、Cloud 内容文件中手写组件的报错（WP10）；两版合并与 `<NextChannel>`（WP11）；整页通道的 `channel`（WP13）。
- 从飞书节点读 `sidebar_label`、`sidebar_position`：只接受参数。
- 基准输出：等内容对齐后由推动者审核。

## 已知的坑

- 列表中的代码组：`<Tabs>` 输出到列表项中时要保持缩进，否则 MDX 编译失败或跳出列表。至少加一个列表中的多语言代码组样例并编译。
- `{`、`}`、`<` 的转义只在代码块之外，用 zdoc 现有的 `applyMdxPatches`，不另写一套转义。
- 提示框中可以嵌套代码组或另一个提示框；`</div>` 只把与提示框配对的那个换成 `</Admonition>`。
- 代码组的语言名区分大小写：`Python` 不是规则中的 `python`，报 `TABS_UNKNOWN_LANGUAGE`。milvus-docs `v3.0.x` `6fb1bf9` 的多语言代码组中，语言名都是小写：`python`、`java` 各 454 处，`javascript` 442，`go` 429，`bash` 428，`cpp` 67，`curl` 8，`shell` 3。规则之外的只有 `plaintext`（2 处，adminGuide）与 `scala`（1 处，integrations），都不在 User Guide 中。
- 改 `core/blocks.ts` 时只加导出，不改函数行为；WP3b 的 `inventoryBlocks` 依赖它。
