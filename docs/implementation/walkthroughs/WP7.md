# WP7 走读：生成初始链接映射表

**仓库**：zdoc　**上游 PR**：[zilliztech/zdoc#818](https://github.com/zilliztech/zdoc/pull/818)（commit [`f19966c`](https://github.com/zilliztech/zdoc/commit/f19966c2aaf1b179180dc747215169ceca7b3b49)）　**任务卡**：[WP7](../tasks/WP7-zdoc-links-seed.md)

## 解决什么问题

Milvus 原文中的站内链接写的是 Milvus 的文件名，如 `boolean.md`。WP5 生成页面时按四步把它换成 Cloud 的页面；第 2 步查的是全站一份的链接映射表 `shared-docs/links.yaml`（[产品需求场景 5](../../prd.md#场景-5链接与图片)）。这张表一开始是空的。只靠同名页面，User Guide 中被链接的 181 个 Milvus 页面要人逐个登记 121 个。

WP7 提供一条一次性的命令 `shared-docs links-seed`，替文档工程师起草这张表：

- 能找到对应页的写成候选，并在注释中写明依据；
- 找不到的写成注释掉的一行，附上相近的 Cloud 页面，留给人判断。

文档工程师审一遍、补全后另开 PR 提交。命令只生成候选文件，不写 zdoc，也不写 milvus-docs。

这份候选要在飞书版页面还在的时候生成：其中一种依据是从 Cloud 现有页面中的链接反推，页面迁出飞书后就没有了。

## 文件地图

都在 `packages/docs-tooling/src/shared-docs/` 下：

| 文件 | 做什么 |
|---|---|
| `core/links/seed.ts` | 由两边的页面算出候选表并输出带注释的 YAML；纯计算 |
| `adapters/zdoc-content.ts` | 从一份 zdoc dev 检出中读某个手册的页面清单（slug、标题）、页面中的站内链接、页面的 front matter；WP8 复用它 |
| `adapters/links-input.ts` | 新增一次批量读取 milvus-docs 中全部页面的方法 |
| `core/links/references.ts`、`candidates.ts` | 新增取链接文字的入口，导出标题的规范化函数；WP5 原有的行为不变 |
| `commands/links-seed.ts` | 命令行 |

## 代码怎样工作

1. **读两边**：
   - Milvus：在给定的提交中，读 `site/en/` 下全部页面（用一次 `git cat-file --batch`），按 front matter 的 `id` 建索引，规则与 WP5 相同；`schema.md` 取 `reference/schema.md`。
   - Cloud：读 dev 中 `content/en/guides/` 的每页 front matter（slug、标题），以及页面中以 `./` 开头的站内链接。
2. **找出被链接的目标**：User Guide 中所有页面正文里指向 Milvus 页面的链接，按文件名去重。识别链接用 WP5 的代码，所以 HTML 写法的 `<a href="bedrock.md">` 也算。
3. **每个目标依次取候选**，取到即停：

   | 顺序 | 依据 | 输出 |
   |---|---|---|
   | 1 | 同名：Cloud 有同样 slug 的页面 | 不写进表，生成页面时第 3 步就能查到；只计数 |
   | 2 | 标题相同，且 Cloud 只有一页是这个标题 | 写一行，注释 `same title` |
   | 3 | 反推：Milvus 源页面对应的 Cloud 页面中，链接文字相同的链接指向哪里，取票数最多的 | 写一行，注释 `inferred` 与票数 |
   | 4 | 按类别：目标在 `adminGuide/`、`getstarted/`、`reference/` 或 `userGuide/indexes/` 下 | 写成 `https://milvus.io/docs/<文件名>`，注释 `category` |
   | 5 | 其余 | 注释掉的一行，`needs review`，附上前三个相近的 Cloud 页面 |

   以下情况都写成 `needs review`，不替人决定：
   - 第 2、3 步给出的结果不同；
   - 反推出现平票；
   - 反推指向的 Cloud 页面已经不存在。
4. **输出**：按 Milvus 文件名排序。开头写明两边的提交与生成日期，末尾写各依据的数目。输出前会用 WP5 的 `parseLinkMap` 读一遍，保证能直接当 `links.yaml` 用。

## 一个例子走一遍

在 milvus-docs `9acdc99` 与 zdoc dev `10d6bd8`（调研时用的两个提交）上运行，候选表中的几行：

```yaml
"boolean.md": "filtering-overview" # same title; same title: filtering-overview; inferred votes: filtering-overview (5)
"ivf-flat.md": "https://milvus.io/docs/ivf-flat.md" # category
# "embedding-function-overview.md": ? # needs review: unresolved; nearby: function-and-model-inference-overview (Function Overview), analyzer-overview (Analyzer Overview), bm25-function (BM25 Function)
```

- `boolean.md`：标题相同，另有 5 票反推，结果一致。
- `ivf-flat.md`：索引类型页，Cloud 没有对应页，指向 milvus.io。
- `embedding-function-overview.md`：四种依据都找不到，留给人判断，第一个相近的页面是 Function Overview。

各依据的数目，与[调研](../../../research/link-mapping-maintenance.md)对照：

| | 调研 | WP7 |
|---|---:|---:|
| 被链接的目标 | 181 | 193 |
| 同名 | 60 | 65 |
| 标题相同 | 107 | 112 |
| 反推 | 105 | 109 |
| 三种合计 | 116 | 121 |
| 剩下 | 65 | 72 |

多出来的 12 个目标与 1 处新的反推，原因都是同一个：Milvus 原文中有些链接写成 HTML（多在表格中），如 `embedding-function-overview.md` 第 62 行的 `<a href="bedrock.md">Bedrock</a>`。调研脚本只认 Markdown 写法，漏掉了这些；正式生成页面时这些链接同样要处理，所以 WP7 的数字才是要用的。审阅时我在同样两个提交上独立跑了一遍，数字完全一致。

在最新提交上（milvus-docs `v3.0.x` `2ffbb88`、zdoc dev `6d0dd8a`，2026-10-23）：

| 输出 | 条数 |
|---|---:|
| 同名，不写进表 | 65 |
| 标题相同 | 51 |
| 反推 | 5 |
| 按类别指向 milvus.io | 36 |
| 待判断 | 38 |

表中生效的有 92 条，待判断 38 条。这份候选表附在 PR 中，交给文档工程师审核。

## 自己试一试

WP7 已合并到 zdoc 的 master。在你的 zdoc 检出中更新到最新、安装依赖，然后在仓库根目录运行下面的命令：

```bash
git checkout master && git pull
```

```bash
corepack enable && pnpm install --frozen-lockfile
```

1. 用一个合成的小例子运行，不联网。会打印一份候选表，标题相同、反推、按类别、待判断各一行，末尾的统计中有 1 个同名目标：

   ```bash
   node -e 'const fs = require("node:fs"), path = require("node:path"), os = require("node:os"); const root = fs.mkdtempSync(path.join(os.tmpdir(), "wp7-seed-demo-")); require("./scripts/lib/load-typescript").loadTypeScript(path.resolve("packages/docs-tooling/src/shared-docs/testing/links-seed/demo.ts")).runSeedDemo(root).then(result => console.log(result.yaml))'
   ```

2. 在真实的仓库上运行，要准备两份检出，都放在临时目录中：milvus-docs（只要 `site/en/`），以及 zdoc dev（只要英文 Guides）。

   ```bash
   seed="$(mktemp -d)"
   ```

   ```bash
   git clone --filter=blob:none --no-checkout --branch v3.0.x https://github.com/milvus-io/milvus-docs.git "$seed/milvus-docs" && git -C "$seed/milvus-docs" sparse-checkout set --no-cone '/site/en/' && git -C "$seed/milvus-docs" checkout v3.0.x
   ```

   ```bash
   git clone --filter=blob:none --no-checkout --depth 1 --branch dev https://github.com/zilliztech/zdoc.git "$seed/zdoc-dev" && git -C "$seed/zdoc-dev" sparse-checkout set --no-cone '/content/en/guides/' && git -C "$seed/zdoc-dev" checkout dev
   ```

   ```bash
   pnpm docs-tooling shared-docs links-seed --repo "$seed/milvus-docs" --commit "$(git -C "$seed/milvus-docs" rev-parse HEAD)" --dev "$seed/zdoc-dev" --out "$seed/links.yaml"
   ```

   结果在 `$seed/links.yaml`。

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `testing/links-seed/seed.test.ts` | 五种依据各自的规则：同标题的 Cloud 页有两页时不用、票数、平票与不一致写成待判断、四个类别目录 |
| `testing/links-seed/adapters.test.ts` | 读 dev 的稀疏检出、`.md` 与 `.mdx`、命令行的参数与默认提交、运行后两份检出都没被改动 |

## 刻意没做的

- **提交正式的 `shared-docs/links.yaml`**：要等文档工程师审核候选表，另开 PR。
- **BYOC 手册与中文页面**：Phase 1 的初始表只按英文 Guides 生成。
- **生成页面时按标题自动匹配**：只在这里给候选，生成时不用（产品需求 5-7）。

## 证据

- 合并时 `pnpm test:shared-docs` 为 35 个测试文件、372 个测试通过，另有 4 个需要联网的测试默认跳过。
- 调研提交上的数字由审阅人独立重跑确认（2026-10-23）；13 处差异的原因在上游 PR 的说明中逐条列出。
- 合成例子的输出在 zdoc master 上运行（2026-10-24）。
