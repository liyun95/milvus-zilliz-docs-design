# WP5 走读：链接与图片

**仓库**：zdoc　**上游 PR**：[zilliztech/zdoc#815](https://github.com/zilliztech/zdoc/pull/815)（commit [`ca1cbd5`](https://github.com/zilliztech/zdoc/commit/ca1cbd57c3179a202f625391fa4d7b4b84054296)）　**任务卡**：[WP5](../tasks/WP5-zdoc-links-images.md)

## 解决什么问题

Milvus 原文中的链接和图片是按 milvus.io 写的，原样放进 Cloud 页面会出三种问题：

- **页面链接指错**：`boolean.md` 在 Cloud 上叫 `filtering-overview`；
- **锚点失效**：milvus.io 的锚点保留大小写（`#Delete-Entities-by-Primary-Keys`），Cloud 的是小写（`#delete-entities-by-primary-keys`），浏览器按大小写匹配；
- **图片不受控**：图片地址指向 Milvus 的存储，被同名覆盖时 Cloud 页面会悄悄变样。

WP5 把链接改成 Cloud 可用的地址，算出每张图片在 Cloud 存储中的新地址。处理不了的一律报错，不原样放过（[产品需求场景 5](../../prd.md#场景-5链接与图片)）。它只算地址、不上传，上传在正式发布时做（WP9）。

它还提供两个站点的锚点算法。WP4 输出标题锚点时要用 Cloud 的算法，由 WP8 接入时传进去。

## 文件地图

都在 `packages/docs-tooling/src/shared-docs/` 下：

| 文件 | 做什么 |
|---|---|
| `core/links/references.ts` | 找出页面中的链接与图片，记下位置；代码块中的、切换栏中的 `#python` 不算 |
| `core/links/map.ts` | 读 `links.yaml`；判断一个链接属于哪一类 |
| `core/links/anchors.ts` | 从标题算出两个站点的锚点 |
| `core/links/candidates.ts` | 查不到时给出最多三个候选页面；WP7 生成初始映射表时复用 |
| `core/links/rewrite.ts` | 按四步查找改写链接、换算锚点、算图片地址 |
| `adapters/links-input.ts` | 准备上面要用的材料：链接指向的 Milvus 页面原文、仓库中的图片，都按同一个 commit 从 Git 读取 |
| `adapters/images.ts` | 下载外部图片（只读）；测试用的替身可以模拟两次下载内容不同 |
| `fixtures/links-errors/` | 9 个错误码各一个最小样例 |

## 代码怎样工作

1. **分类**：页面中的每个链接先分到一类。

   | 写法 | 处理 |
   |---|---|
   | 页内锚点 `#Heading` | 换算锚点 |
   | 外部网站、`mailto:` | 原样保留 |
   | milvus.io 完整地址 | 原样保留 |
   | Milvus 页面 `boolean.md`、`boolean.md#Heading` | 四步查找，再换算锚点 |
   | 以 `/` 开头 | 报 `LINK_ROOT_PATH` |
   | 其他，如漏写 `.md` 的 `filtering` | 报 `LINK_UNKNOWN_FORM` |

2. **四步查找**，查到即停：

   | 步骤 | 查什么 | 结果 |
   |---|---|---|
   | 1 | 目标页也是共享页 | `./<页面标识>`；目标页在这个版本中不存在时报 `LINK_TARGET_ABSENT` |
   | 2 | `links.yaml` 中登记了 | 页面标识写成 `./<页面标识>`；milvus.io 地址原样用，锚点也原样接上 |
   | 3 | Cloud 有同名页面 | `./<页面标识>` |
   | 4 | 都没有 | 报 `LINK_UNRESOLVED`，附上候选，不自动采用 |

   Cloud 页面的列表现在由调用方传入，真实来源由 zdoc 维护者确定，WP8 接入。

3. **锚点换算**：
   1. 在目标页同一 commit 的原文中，按 milvus.io 的算法算出每个标题的锚点，找到与链接完全相同的那个；只差大小写也算找不到，报 `ANCHOR_NOT_FOUND`。
   2. 再按 Cloud 的算法从这个标题的文字算出新锚点。
   - Cloud 的算法与飞书转换器相同：`slugify(标题文字, 小写, 严格)`，如 `&` 换成 `and`。测试中把它与飞书转换器的结果逐个比对过。
   - 重复的标题依次加 `-1`、`-2`，规则与 WP4 输出锚点时完全相同。这一点是审阅时发现并统一的：两边规则不同，链接就可能跳到错的标题。
4. **找目标页**：
   - 按 Milvus 页面 front matter 中的 `id` 找，与 milvus.io 网站的做法相同。
   - `site/en` 中只有 `schema.md` 有两篇同名：`userGuide/schema/schema.md` 与 `reference/schema.md`。按路径排序取第一个，即 `reference/schema.md`，与 milvus.io 线上页面“编辑此页”指向的那篇一致。
5. **图片**：
   - 仓库内的图片按同一 commit 读取，读的是原始字节；外部图片下载两次，内容不同报 `IMAGE_CHANGED_DURING_READ`。
   - 新地址是 `shared/<内容的 SHA-256>.<扩展名>`：内容一变地址就变，所以 Milvus 换图会出现在上游更新中（产品需求 5-4）。
   - 如果这张图在已采用的版本中记录过摘要、而现在读到的内容变了，仍用记录中的摘要，不报错，只返回一条“原地址内容已变”的提示（产品需求 5-6）。

## 一个例子走一遍

在三篇试点页上运行（WP3 读取与预处理之后）：

- **Delete Entities**：`[Filtering Explained](boolean.md)` 在查找第 2 步命中映射表，变成 `[Filtering Explained](./filtering-overview)`，与 dev 上飞书版的写法相同。
- **OpenAI**：第 198 行指向 `embedding-function-overview.md`，四步都查不到：

  ```
  site/en/userGuide/embeddings-reranking/embedding-function/openai.md:198 LINK_UNRESOLVED
    Add a destination for embedding-function-overview.md to links.yaml.
    候选：text-embedding-functions（Embedding Function Overview）
          model-inference（Embedding Functions）
  ```

  第一个候选的标题与目标页完全相同，排在前面；但工具不会自动采用，要文档工程师在 `links.yaml` 中补一行。

## 自己试一试

WP5 已合并到 zdoc 的 master。在你的 zdoc 检出中更新到最新、安装依赖，然后在仓库根目录运行下面的命令：

```bash
git checkout master && git pull
```

```bash
corepack enable && pnpm install --frozen-lockfile
```

运行演示，看到上面两个结果。不联网、不上传，结果打印为 JSON：

```bash
node -e 'const fs = require("node:fs"), path = require("node:path"), os = require("node:os"); const root = fs.mkdtempSync(path.join(os.tmpdir(), "wp5-links-demo-")); require("./scripts/lib/load-typescript").loadTypeScript(path.resolve("packages/docs-tooling/src/shared-docs/testing/links/demo.ts")).runLinksDemo(root).then(result => console.log(JSON.stringify(result, null, 2)))'
```

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `testing/links/rewrite.test.ts` | 每类链接、四步查找的顺序、milvus.io 地址保留锚点、`./` 的写法 |
| `testing/links/anchors.test.ts` | 两个站点的锚点算法、与飞书转换器的比对、重复标题的编号 |
| `testing/links/references.test.ts` | 哪些位置的链接不处理：代码块、切换栏、HTML 注释 |
| `testing/links/inputs.test.ts`、`images.test.ts` | `schema.md` 选哪一篇；仓库内的图片按同一 commit 读取；外部图片读两次；生成时从不上传 |
| `fixtures/links-errors/*/` | 9 个错误码的最小输入与期望 |

## 刻意没做的

- **上传图片、写记录文件、已存图片的保留**：WP9。所以 `5-3` 与验收 `T06` 改归 WP9。
- **生成初始映射表的命令**：WP7，复用这里的候选函数。
- **Cloud 页面列表的真实来源**：WP8，由 zdoc 维护者确定。
- **Cloud 内容文件中的链接与图片**：WP10。
- **标题改名后锚点的处理**：WP12。

## 已知的问题

- 每篇页面换算锚点前，要读一遍 `site/en` 下全部约 500 篇 Markdown 来建索引。现在够用；WP8 一次生成多页时，可以改成一次批量读取。
- milvus-docs 中现有 49 个带锚点的链接在 milvus.io 上就已失效（技术设计 02b 的统计）。接入这些页面时会报 `ANCHOR_NOT_FOUND`，这是预期的，在内容对齐时回上游修正。

## 证据

- 合并时 `pnpm test:shared-docs` 为 33 个测试文件、346 个测试通过，另有 4 个需要联网的测试默认跳过；`spec/requirements.json` 与设计仓库逐字节相同（76 个错误码）；`pending.json` 中剩 83 条。
- 上面的例子在合并后的 master（`ca1cbd5`）上实际运行（2026-10-23）。
- `schema.md` 的选择依据：milvus.io 线上页面的“编辑此页”链接指向 `site/en/reference/schema.md`；网站按 front matter 的 `id` 查找页面（[milvus-io/milvus.io 的 `src/utils/docs.ts`](https://github.com/milvus-io/milvus.io/blob/43e66d87b3703ce9af6640bb1a1546e97de990e0/src/utils/docs.ts)）。
