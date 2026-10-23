# WP6 产品名检查

**仓库**：[zdoc](https://github.com/zilliztech/zdoc)　**阶段**：Phase 1a　**依赖**：[WP3](./WP3-zdoc-read.md)：WP3a 已合并（[zilliztech/zdoc#796](https://github.com/zilliztech/zdoc/pull/796)，commit [`5844587`](https://github.com/zilliztech/zdoc/commit/5844587037d5397e8ebd1510235db5d8592584d7)）；WP3b 已合并（[zilliztech/zdoc#800](https://github.com/zilliztech/zdoc/pull/800)，commit [`31a9b54`](https://github.com/zilliztech/zdoc/commit/31a9b54176c9adc50515f84a559b4082700b6620)），可以开工。可与 [WP4](./WP4-zdoc-site-adaptation.md)、[WP5](./WP5-zdoc-links-images.md) 同时进行　**状态**：未开始

## 目标

做完后，zdoc 能检查一个版本、一个手册生成后的 MDX 中有没有漏换的产品名或连接值，如 `Milvus`、`localhost:19530`：

- 检查规则读自 `shared-docs/product-names.yaml`；
- 命中检查规则、又不在放行清单中的，这一页失败；
- 报错指回作者要改的位置：原文、片段、Cloud 内容文件或变量。

本工作包只提供纯计算的函数和测试，不接入任何命令（WP8）。

## 要读的

| 文档 | 章节 | 读它为了什么 |
|---|---|---|
| [产品需求](../../prd.md) | 场景 1：产品名检查、系统行为 1-6、出错时 | 规则文件的写法与行为 |
| [技术设计 07](../../design/07-site-adaptation.md) | 产品名检查、出错时的最后两行 | 匹配规则、怎样找回位置 |
| [技术设计 09](../../design/09-error-catalog.md) | 错误的结构、产品名 | 错误码 |
| [实现指南](../README.md) | 2.5、第 5 节 | 错误样例表、规则 |
| [WP0 走读](../walkthroughs/WP0.md) | 全文 | 目录与测试工具 |

## 范围

| 可以改 | 不能改 |
|---|---|
| 新建 `core/product-names/`：规则文件的读取、匹配、位置查找，都是纯计算 | `core/types.ts`、`adapters/types.ts`：WP3 是主人，要加共用类型先在 PR 中提出；本工作包的类型放在 `core/product-names/` 中 |
| 新建 `fixtures/product-names/`：规则文件样例（产品需求场景 1 中的三项检查与一项放行）、合成的小样例 | `commands/`、`cli-main.ts`：接入命令归 WP8 |
| 新建 `fixtures/product-names-errors/<样例>/`、`testing/product-names/` | 站点适配（WP4）；链接与图片（WP5） |
| `spec/pending.json`：删掉本工作包的编号 | `spec/requirements.json`：WP5 会复制带新错误码的版本，本工作包不复制；`fixtures/golden/` |

## 接口

```ts
// core/product-names/：纯计算
parseProductNames(yamlText, context): { rules: ProductNameRules } | { errors }   // PRODUCT_NAMES_INVALID
checkProductNames(input: {
  mdx: string                        // 一个版本、一个手册生成后的 MDX
  rules: ProductNameRules
  manual: string
  sources: readonly {                // 这一版本用到的输入，按查找顺序
    kind: 'content-file' | 'source' | 'fragment' | 'variable'
    file: string                     // 仓库相对路径；变量为 shared-docs/Variables.json
    text: string                     // 文件内容；变量为它的值
    key?: string                     // 变量的键
  }[]
  context: DiagnosticContext         // page、channel
}): { errors: SharedDocsError[] }    // 没有命中时为空
```

- **匹配**：`check` 中每一项按整词、区分大小写匹配。
  - 前后紧挨着字母、数字或 `_` 的不算命中，所以 `MilvusClient`、`pymilvus` 不算；
  - 紧挨着 `.` 或 `/` 再接字母或数字的也不算，所以 `Milvus.yaml`、`milvus.io` 这类文件名与地址不算。
- **不检查的部分**：front matter；Markdown 链接与图片的地址部分（`(...)`）；HTML 的 `href`、`src`。链接文字与代码块要检查。
- **放行**：命中位置落在同一行中某个 `allow` 短语之内时放过。`allow` 中没有空格的项报 `PRODUCT_NAMES_INVALID`。
- **找回位置**（技术设计 07 “怎样找回位置”）：
  - 是否失败只看 MDX。
  - 对 MDX 中命中的每种写法，到 `sources` 中按同样的规则逐个查找，每处没被放过的位置报一条 `PRODUCT_NAME_FOUND`：`file`、`line` 指向这个输入，变量的命中只给 `file`，`detail` 中附上键名。
  - `detail` 中还有命中的写法、手册、MDX 中的行号。
  - 所有输入中都找不到时，报一条，`file` 为页面原文，不给行号。

## 要覆盖的编号

| 编号 | 怎样测 |
|---|---|
| `1-6` | 原文中漏换的 `Milvus` 让检查失败，报错有页面、版本、原文的文件与行号；`current` 与 `next` 两个版本分别检查，各自报出 |
| `T14` | 在两个版本中都查出漏换的产品名与 `localhost:19530`；`Zilliz Cloud is built on Milvus` 与 `MilvusClient`、`pymilvus`、`milvus.yaml` 不误报；命中在片段中时指向片段，在 Cloud 内容文件中时指向内容文件，来自变量值时指向 `Variables.json` 与键名 |
| `PRODUCT_NAME_FOUND` | 错误样例（实现指南 2.5） |
| `PRODUCT_NAMES_INVALID` | 不是合法的 YAML；缺少 `check`；`allow` 中有单个词 |

每个错误码一个错误样例，断言 `code`、`file`、`line`、`page`、`channel`。

另外，对三篇试点页的原文（`fixtures/pilots/`，经 WP3 的读取与预处理，未经站点适配）运行一次，把命中数写进 PR 说明。内容对齐前原文中有很多 `Milvus`，这些是预期的，测试不断言具体数目。

做完后把上表的编号从 `spec/pending.json` 中删掉。

## 完成的定义

- [ ] `pnpm test:shared-docs` 全绿；上表的编号不在 `pending.json` 中
- [ ] `pnpm test:for-change` 给出的命令全部跑过；`pnpm typecheck` 通过
- [ ] PR 说明按[实现指南第 5 节](../README.md#pr-说明的格式)的六个部分写。“How to try it”从 `gh pr checkout` 开始，不写本机路径，演示两件事：对一段含 `Milvus` 与 `MilvusClient` 的小样例运行检查，只报前者，并指回它所在的行；在规则文件的 `allow` 中加一个单词，看到 `PRODUCT_NAMES_INVALID`。可以像 WP3b 的 `testing/demo.ts` 那样写一个小脚本，在临时目录中运行

## 不做

- 生成 MDX（WP4）、接入命令与两版合并前的调用位置（WP8、WP11）。
- 变换接入后排除被替换或删除的原文范围（WP10）；本工作包的 `sources` 中只有原文、片段与变量，Cloud 内容文件只用合成样例测试。
- milvus-docs 的 PR 检查中只提示、不拦截的那一部分：技术设计 07 留给实现决定，不在 Phase 1a。

## 已知的坑

- 同一个片段被引用多次，MDX 中会命中多次，但片段中只有一处，只报一条。
- 变量值中的命中只在用到这个变量时才算：`sources` 中只放这一页实际用到的变量。
- MDX 中的命中可能在站点适配生成的文字中，例如 `<Tabs>` 的属性。这类在所有输入中都找不到，按上面的规则报在页面原文上。
- 按行查找放行短语：短语跨行时不放过。产品需求中的例子都在一行之内，不要为跨行另写规则。
