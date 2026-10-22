# WP2 走读：预处理入口与发版

**仓库**：md2md　**上游 PR**：[zilliztech/md2md#4](https://github.com/zilliztech/md2md/pull/4)（commit [`a143b27`](https://github.com/zilliztech/md2md/commit/a143b27c475059f1fe22e84e074953b05bd9cd37)）　**发布**：[`@zilliz/mdtomd@1.3.0`](https://www.npmjs.com/package/@zilliz/mdtomd/v/1.3.0)，[GitHub Release `v1.3.0`](https://github.com/zilliztech/md2md/releases/tag/v1.3.0)　**任务卡**：[WP2](../tasks/WP2-md2md-preprocess.md)

## 解决什么问题

Milvus 原文中有两种要展开的写法（[产品需求场景 1](../../prd.md#场景-1把产品名和连接值写成变量)）：

- 变量 `{{var.product}}`：换成变量表中的值；
- 片段 `{{fragments/connect.md}}`：换成 `fragments/` 下那个文件的内容。

Milvus 现在用 `goover` 展开它们：按目录查找 `Variables.json`，出错时只写日志、照样输出。Cloud 共享页不能这样做，要满足三点：

- 变量只用 zdoc 传入的 Cloud 变量表，不去目录中找 Milvus 的（产品需求 1-1）；
- 任何一处出错，这一页就失败，并且一次列出全部错误；
- 告诉调用方用到了哪些片段和变量，zdoc 以后据此判断上游改动是否影响这一页。

WP2 为此新建一个入口 `preprocess`，`goover` 原来的路径一行未改。WP2 还换掉了 md2md 的发版方式，并发布了 1.3.0，WP1 的命名块随之上线。

## 文件地图

| 文件 | 做什么 |
|---|---|
| `src/preprocess/scan.js` | 把文本切成片段：普通文字、变量、片段引用、不支持的标记；建变量表、按键查值。纯计算 |
| `src/preprocess/files.js` | 检查片段路径、读片段文件；只有这里读文件 |
| `src/preprocess/index.js` | `preprocess` 本身：检查参数，三遍处理，返回结果 |
| `package.json` | `exports` 加 `./preprocess.js`，zdoc 用 `require('@zilliz/mdtomd/preprocess.js')` 引用；版本 1.3.0 |
| `yarn.lock` | 第一次提交锁文件，CI 与发版都按它安装 |
| `.github/workflows/release.yml` | 新的发版工作流，代替删掉的 `ci.yml` |
| `test/preprocess/`、`test/contract/cases/preprocess/` | 测试与 13 个契约用例（zdoc 的替身也要通过它们） |

## 代码怎样工作

调用方式：

```js
preprocess({ content, fragmentRoot, variables, sourceName, limits })
// → { ok, content, dependencies: { fragments, variables }, errors, engine: { name, version } }
```

参数类型不对（例如 `fragmentRoot` 不是绝对路径、变量表中有只差大小写的两个键）直接抛 `TypeError`：这是调用方的程序写错了，不是原文的问题，不放进 `errors`。

1. **切分**（`scan.js`）。在文本中找这几种写法：

   | 写法 | 当作 | 说明 |
   |---|---|---|
   | `{{var.…}}` | 变量 | 不区分大小写，`{{VAR.Product}}` 与 `{{var.product}}` 相同 |
   | `{{fragments/…}}` | 片段引用 | 前缀必须是小写的 `fragments/` |
   | `{{tab}}`、`{{glossary.…`、`{{images/…`、`::glossary.…` | 不支持的标记 | 要靠 Milvus 网站的插件处理，报 `UNSUPPORTED_MARK` |
   | 其他 `{{…}}`，如 `{{ doc.content }}` | 普通文字 | 原样保留（产品需求 1-4） |

   每一段都记下所在的行号，展开片段之后仍然能指回原文件的原行。

2. **第一遍：找片段**。从页面开始，逐个处理片段引用：
   - 路径必须是 `fragments/` 下的 `.md` 文件，不能用 `..` 跳出去，否则 `FRAGMENT_OUT_OF_ROOT`；
   - 从 `fragments/` 开始逐段检查，任何一段是符号链接就报 `FRAGMENT_SYMLINK`。`fragmentRoot` 本身及其上层目录不检查（这是审阅中修掉的问题：macOS 的 `/tmp` 本身就是符号链接）；
   - 片段又引用回自己的上一层，报 `FRAGMENT_CYCLE`，并给出整条引用链；
   - 同一个片段只读一次，记下它的 SHA-256、字节数和被谁引用（产品需求 1-5）。

3. **第二遍：查变量**。逐个变量按键查值，`{{var.cloud.region}}` 先找 `cloud` 再找 `region`。查不到报 `VAR_MISSING`；值是对象或数组报 `VAR_NOT_SCALAR`。查到的值原样插入，**不再展开**：值中写着 `{{var.x}}` 也只是文字（产品需求 1-3）。

4. **第三遍：拼出结果**。把片段和变量的值拼进去，同时累计输出的字节数。

5. **返回**。有任何错误时，`ok` 为 `false`、`content` 为 `null`，不给出半成品；`dependencies` 照常返回。错误的 `file` 与 `line` 指向写着这个标记的那个文件，可能是页面，也可能是某个片段。

有四个上限，防止原文写错时无限展开：

| 上限 | 默认值 | 怎样算 |
|---|---|---|
| `maxDepth` | 5 | 页面直接引用的片段是第 1 层 |
| `maxFragments` | 100 | 不同的片段文件数，同一个文件只算一次 |
| `maxFragmentBytes` | 256 KB | 单个片段文件的大小 |
| `maxOutputBytes` | 2 MB | 展开后的总字节数，同一片段引用几次就算几次 |

超出任何一个都报 `LIMIT_EXCEEDED`，`detail.limit` 说明是哪一个。

## 一个例子走一遍

一个好页面、一个坏页面，共用一个 `fragments/` 目录：

<details>
<summary>输入文件与变量表</summary>

`page.md`：

```markdown
Create a collection on {{var.product}}:

{{fragments/connect.md}}
```

`bad.md`：

```markdown
Use {{var.region}} on {{var.product}}.

{{fragments/loop-a.md}}

{{tab}}
```

`fragments/connect.md`：`Connect to {{var.cloud.endpoint}}.`

`fragments/loop-a.md`：`{{fragments/loop-b.md}}`

`fragments/loop-b.md`：`{{fragments/loop-a.md}}`

变量表（注意 `Product` 是大写开头，没有 `region`）：

```json
{ "Product": "Zilliz Cloud", "cloud": { "endpoint": "https://in01.example.zillizcloud.com" } }
```

</details>

`page.md` 的结果（用 npm 上的 1.3.0 实际运行，省略了 SHA-256）：

```json
{
  "ok": true,
  "content": "Create a collection on Zilliz Cloud:\n\nConnect to https://in01.example.zillizcloud.com.\n\n",
  "dependencies": {
    "fragments": [{ "path": "fragments/connect.md", "bytes": 35, "includedBy": ["page.md"] }],
    "variables": [
      { "key": "product", "usedIn": ["page.md"] },
      { "key": "cloud.endpoint", "usedIn": ["fragments/connect.md"] }
    ]
  },
  "errors": [],
  "engine": { "name": "@zilliz/mdtomd", "version": "1.3.0" }
}
```

`cloud.endpoint` 写在片段中，依赖清单记的是 `fragments/connect.md`，不是页面。

`bad.md` 的三处错误一次报出，`content` 为 `null`：

```
fragments/loop-b.md:1 FRAGMENT_CYCLE   chain: fragments/loop-a.md → fragments/loop-b.md → fragments/loop-a.md
bad.md:1              VAR_MISSING      region
bad.md:5              UNSUPPORTED_MARK {{tab}}
```

循环的错误指向 `fragments/loop-b.md` 第 1 行，因为回头引用的标记写在那里。

## 发版

| 以前 | 现在 |
|---|---|
| 合并到 master 就由 semantic-release 自动发版 | 只能在 GitHub Actions 中手动运行 `release.yml` |
| 用存在仓库中的 `NPM_TOKEN`（已失效） | 用 npm 的可信发布者：GitHub 运行时临时证明“我是 `zilliztech/md2md` 的 `release.yml`”，不存任何令牌 |
| 发出去就公开 | 先暂存，推动者在 npmjs.com 上用双因素认证批准后才公开 |

`release.yml` 依次：只在 `zilliztech/md2md` 的 master 上运行；按锁文件安装；跑全部测试；从 `package.json` 读版本，tag 已存在就停；`npm stage publish`；给这个 commit 打 tag、建 GitHub Release。

1.3.0 的经过（2026-10-22）：

1. 推动者运行 `release.yml`（[运行记录](https://github.com/zilliztech/md2md/actions/runs/39718860046)），全部步骤成功。
2. 日志中 npm 提示三个命令行“was invalid and removed”。查了 npm 的源码，它只是把 `./bin/goover.js` 改写成 `bin/goover.js`，三个命令都还在；从 npm 安装 1.3.0 后 `goover`、`md2md`、`md2md-blocks` 都能用。以后可以用 `npm pkg fix` 消掉这条提示。
3. 推动者在 npmjs.com 上批准，1.3.0 公开。
4. 锁文件提交后，GitHub 的 Dependabot 能看到全部依赖，对 `axios` 报了 23 条安全提醒。md2md 从 2021 年起列着 `axios`，却没有任何代码用它，于是另开 [zilliztech/md2md#6](https://github.com/zilliztech/md2md/pull/6) 删掉（commit `eb91900`）。这不影响已发布的 1.3.0，随下一个版本生效。

## 自己试一试

需要 Node 22 以上。

1. 在你的 md2md 检出中更新到最新、跑全部测试（WP2 合并时是 119 个）：

   ```bash
   git checkout master && git pull
   ```

   ```bash
   yarn install --frozen-lockfile && yarn test
   ```

2. 不用检出，直接用 npm 上的 1.3.0 跑上面的例子。在一个临时目录中安装：

   ```bash
   cd "$(mktemp -d)" && npm init -y >/dev/null && npm install @zilliz/mdtomd@1.3.0
   ```

   把上面的输入文件放进这个目录（`page.md`、`bad.md` 和 `fragments/`），再新建 `run.js`：

   ```js
   const fs = require('fs');
   const { preprocess } = require('@zilliz/mdtomd/preprocess.js');
   const variables = { Product: 'Zilliz Cloud', cloud: { endpoint: 'https://in01.example.zillizcloud.com' } };
   for (const name of ['page.md', 'bad.md']) {
     const content = fs.readFileSync(name, 'utf8');
     const result = preprocess({ content, fragmentRoot: process.cwd(), variables, sourceName: name });
     console.log(name, JSON.stringify(result, null, 2));
   }
   ```

   ```bash
   node run.js
   ```

3. 改一处再跑：在变量表中加上 `region: "eu"`，`VAR_MISSING` 消失；把 `loop-b.md` 改成普通文字，循环的错误也消失，只剩 `{{tab}}` 一处。

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `test/contract/cases/preprocess/success.json` | 一个用例看全规则：大小写、嵌套键、重复引用、值中的 `{{…}}` 不再展开、代码块中的变量照样替换 |
| `test/contract/cases/preprocess/README.md` | 契约的约定：哪些字段逐字比较、行号与路径怎样算 |
| `test/contract/cases/preprocess/cycle.json`、`symlink.json`、`limit-*.json` | 各种失败的样子 |
| `test/preprocess/preprocess.test.js` | 并行调用互不串值、`goover` 的结果不变、参数错误抛 `TypeError` |

## 刻意没做的

- **zdoc 侧的调用**：WP3b 接入。在那之前 zdoc 用替身，替身要通过上面的契约用例。
- **改 `goover`**：Milvus 的构建仍走原来的路径，变量与片段的规则一字未改。
- **产品过滤、站点适配**：zdoc 的事。
- **其他分支升级**：只有 milvus-docs 的 `v3.0.x` 升级到 1.3.0，并在 PR 检查中加 `md2md-blocks check`；`v2.6.x`、`v2.5.x`、`preview` 保持 1.2.3。

## 证据

T11 回归：用 npm 上的 1.2.3 与 npm 上的 1.3.0 分别处理 milvus-docs `v3.0.x` 的最新提交 [`6fb1bf9`](https://github.com/milvus-io/milvus-docs/commit/6fb1bf97f49d1556eac2f6cb1c487ebb754d195e) 的全部文档，两份输出都是 506 个文件、5,648,413 字节，逐字节相同；给三篇试点页加上命名块标记后再处理，输出仍然相同（2026-10-22，发布之后重跑）。同一提交上 `md2md-blocks check site/en` 没有报错。
