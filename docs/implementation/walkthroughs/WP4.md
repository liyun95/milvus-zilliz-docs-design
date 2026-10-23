# WP4 走读：站点适配

**仓库**：zdoc　**上游 PR**：[zilliztech/zdoc#804](https://github.com/zilliztech/zdoc/pull/804)（commit [`09859d7`](https://github.com/zilliztech/zdoc/commit/09859d750ea0a88ea71a4b7359794db00b840dcf)）　**任务卡**：[WP4](../tasks/WP4-zdoc-site-adaptation.md)

## 解决什么问题

WP3 读出来的是 Milvus 写法的 Markdown：代码组用 `<div class="multipleCode">` 切换栏，提示框用 `<div class="alert note">`，front matter 是 Milvus 的字段。Cloud 站点（Docusaurus）要的是另一套：

| Milvus 原文 | Cloud 页面 |
|---|---|
| 切换栏加几个代码块 | `<Tabs>` 与 `<TabItem>`，顺序与默认语言按 Cloud 的规则 |
| `<div class="alert note">` | `<Admonition type="info" icon="📘" title="Notes">` |
| `id`、`title`、`summary` | `title`、`slug`、`beta`、`token` 等 Cloud 字段，标题加 `\| Cloud` 或 `\| BYOC` |
| `## 标题` | `## 标题\{#锚点}` |

WP4 做这一步转换，并保证结果能编译成 MDX。认不出的写法直接报错，不原样放过：原样输出可能编译通过，却在页面上显示成乱码。

它只提供函数，还没有接入任何命令；接成一条生成命令是 WP8 的事。

## 文件地图

都在 `packages/docs-tooling/src/shared-docs/` 下：

| 文件 | 做什么 |
|---|---|
| `core/site/tabs.ts` | 读 Tabs 规则文件；把一个代码组重新生成为 `<Tabs>` |
| `core/site/front-matter.ts` | 生成 Cloud 的 front matter |
| `core/site/index.ts` | `adaptPage`：整页转换，包括提示框、标题锚点、组件引入；记下每一行来自原文的哪一行 |
| `core/blocks.ts` | 从 WP3 的命名块清单中抽出代码组识别，供整页使用；WP3 的行为不变 |
| `adapters/mdx.ts` | 调用 zdoc 现有的 MDX 修补模块，再编译一次，确认能用 |
| `fixtures/site/cloud-sdk-tabs.yaml` | Tabs 规则的样例，按技术设计 07 的 Phase 1 建议值 |
| `fixtures/site-errors/` | 5 个错误码各一个最小样例 |

## 代码怎样工作

1. **front matter**：取原文的 `title`、`summary`，`page.yaml` 的 `metadata` 中写了就用它；按手册加后缀，`guides` 加 `| Cloud`，`guides-byoc` 加 `| BYOC`。字段的顺序与 dev 上飞书生成的页面相同。
2. **代码组**：
   - 找出页面中的每个多语言代码组，不只是命名块中的，列表中缩进的也算。
   - 切换栏的内容一概不用，只看代码块的语言。
   - 先按 `aliases` 换算语言名（`cpp` → `c++`，`curl` → `bash`），再按规则的顺序输出；只列实际有的语言。
   - 只有一种语言的代码组输出普通代码块。

   下面三种情况报错：

   | 情况 | 错误码 |
   |---|---|
   | 规则中没有的语言，包括没写语言名的代码块 | `TABS_UNKNOWN_LANGUAGE` |
   | 缺少必须有的 `python` | `TABS_REQUIRED_MISSING` |
   | 同一种语言出现两次 | `ADAPT_UNSUPPORTED_MARKUP` |

3. **提示框与其他 `<div>`**：
   - `alert note` 与 `alert warning` 换成 `<Admonition>`，配对的 `</div>` 换成 `</Admonition>`，嵌套的也能处理。
   - 其余任何 `<div>` 都报 `ADAPT_UNSUPPORTED_MARKUP`。这比技术设计原来写的“其余照原样输出”更严，审阅时决定采用它，并改了设计。原因见“已知的影响”。
4. **标题锚点**：
   - 二到六级标题后面加 `{#锚点}`，一级标题不加；同一页中重复的依次加 `-1`、`-2`。
   - 锚点怎样从标题算出，由调用方传入一个函数。真正的算法在 WP5，WP8 接入时把它传进来；WP4 的测试中用一个简单的替身。
5. **组件引入**：用到哪个组件就在开头加哪一行 `import`。
6. **修补与编译**（`adapters/mdx.ts`）：
   - 交给 zdoc 现有的 MDX 修补模块，用法与飞书转换器完全相同；它会把 `{#锚点}` 转义成 dev 上的写法 `\{#锚点}`。
   - 修补前先查一遍不支持的写法，免得修补模块的清理把问题藏起来。
   - 修补后再用 `@mdx-js/mdx` 编译；编译失败报 `ADAPT_MDX_INVALID`，并按第 3 步记下的行号指回原文。

## 一个例子走一遍

Delete Entities 的原文中，第一个代码组是这样开头的：

```markdown
<div class="multipleCode">
    <a href="#python">Python</a>
    <a href="#java">Java</a>
    <a href="#javascript">NodeJS</a>
    <a href="#go">Go</a>
    <a href="#bash">cURL</a>
</div>

```python
from pymilvus import MilvusClient
…
```

转换后：

```mdx
## Delete Entities by Filtering Conditions\{#delete-entities-by-filtering-conditions}

When deleting multiple entities that share some attributes in a batch, you can use filter expressions. …

<Tabs groupId="code" defaultValue='python' values={[{"label":"Python","value":"python"},{"label":"Java","value":"java"},{"label":"Go","value":"go"},{"label":"NodeJS","value":"javascript"},{"label":"cURL","value":"bash"}]}>
<TabItem value='python'>

```python
from pymilvus import MilvusClient
…
```

</TabItem>

<TabItem value='java'>
…
```

原文的代码块依次是 python、java、javascript、go、bash，输出按 Cloud 的规则把 Go 排在 NodeJS 前面。

和 dev 上飞书生成的同一页（`content/en/guides/tutorials/development/insert-and-delete/delete-entities.md`）逐行比较：

| 部分 | 结果 |
|---|---|
| 三个二级标题 | 逐字相同，包括 `\{#…}` 的写法 |
| front matter | 只有 `token` 不同：共享页用 `shared-delete-entities`，这是有意的 |
| `<Tabs>` 那一行 | 写法相同；dev 上还多了 Rust 与 C++，那是 Cloud 以后用变换加上的（WP10） |

激活前与飞书版比较时，剩下的差异就只是内容上的，不会有一堆只因写法不同的噪音。

## 自己试一试

WP4 已合并到 zdoc 的 master。在你的 zdoc 检出中更新到最新、安装依赖，然后在仓库根目录运行下面的命令：

```bash
git checkout master && git pull
```

```bash
corepack enable && pnpm install --frozen-lockfile
```

1. 在临时目录中建一个 Delete Entities 的演示并转换。会打印 front matter 与第一个 `<Tabs>` 那一行，并把整页 MDX 写到临时目录中：

   ```bash
   wp4_demo="$(mktemp -d)"
   ```

   ```bash
   node -e 'const demo = require("./scripts/lib/load-typescript").loadTypeScript(require("node:path").resolve("packages/docs-tooling/src/shared-docs/testing/site/demo.ts")); demo.createSiteDemo(process.argv[1]).then(() => demo.runSiteDemo(process.argv[1])).then(code => { process.exitCode = code })' "$wp4_demo"
   ```

2. 打开生成的页面看看：

   ```bash
   less "$wp4_demo/delete-entities.mdx"
   ```

3. 把临时规则文件中的 `default` 改成不存在的语言，再转换一次，看到 `TABS_RULES_INVALID`，位置是 `presentation/cloud-sdk-tabs.yaml:3`：

   ```bash
   node -e 'const fs = require("node:fs"); const rules = require("node:path").join(process.argv[1], "presentation/cloud-sdk-tabs.yaml"); fs.writeFileSync(rules, fs.readFileSync(rules, "utf8").replace("default: python", "default: missing-language")); const demo = require("./scripts/lib/load-typescript").loadTypeScript(require("node:path").resolve("packages/docs-tooling/src/shared-docs/testing/site/demo.ts")); demo.runSiteDemo(process.argv[1]).then(code => { process.exitCode = code })' "$wp4_demo"
   ```

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `testing/site/adapt.test.ts` | 每条转换规则：Tabs 的顺序与默认语言、别名、列表中的代码组、提示框嵌套、锚点编号、front matter |
| `testing/site/pilots.test.ts` | 三篇试点页都能转换并编译 |
| `testing/site/blocks-baseline.test.ts` | 抽出代码组识别后，WP3 的命名块清单与合并前逐项相同 |
| `fixtures/site-errors/*/` | 5 个错误码的最小输入与期望 |

## 已知的影响

milvus-docs `v3.0.x` 的 User Guide 中有 36 处按 SDK 语言显示的说明，如 `<div class="language-python">`，分布在 5 篇页面中，如 `index-vector-fields.md`、`import-data.md`。它们在 milvus.io 上只在读者选中这种语言时显示；原样搬到 Cloud，所有语言的说明会同时出现。所以这 5 篇页面现在会报 `ADAPT_UNSUPPORTED_MARKUP`，接入前要在内容对齐时改写。

## 刻意没做的

- **接入命令**：WP8。
- **链接、锚点换算、图片**：WP5。WP4 只在标题后输出锚点，算法由 WP5 提供。
- **Cloud 增加的语言**：如 Delete Entities 的 Rust 与 C++，由变换加入（WP10）。
- **两版合并与整页通道**：WP11、WP13。
- **基准输出**：等内容对齐后由推动者审核，现在的测试只断言能编译、Tabs 的语言对。

## 证据

- 合并时 `pnpm test:shared-docs` 为 21 个测试文件、181 个测试，全部通过；与 WP5、WP6 一起合并到 master 后为 33 个文件、346 个测试通过，另有 4 个需要联网的测试默认跳过。
- 与 dev 上 Delete Entities 的比较、上面的演示输出，都在合并后的 master（`ca1cbd5`）上实际运行（2026-10-23）。
- dev 上英文 Guides 的写法统计（390 篇）：一级标题 391 个中 5 个带锚点；二到六级标题 2847 个中 2819 个是 `文字\{#锚点}`；`<TabItem>` 5090 个中 5068 个用单引号。
