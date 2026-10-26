# WP6 走读：产品名检查

**仓库**：zdoc　**上游 PR**：[zilliztech/zdoc#812](https://github.com/zilliztech/zdoc/pull/812)（commit [`ca64aa6`](https://github.com/zilliztech/zdoc/commit/ca64aa6992311623127c44ddc6b16e3d346c3923)）　**任务卡**：[WP6](../tasks/WP6-zdoc-product-names.md)

## 解决什么问题

共享页靠变量把 Milvus 的写法换成 Cloud 的。作者漏写一个变量，或者某一段讲的是 Cloud 没有的功能却没做变换，Milvus 的东西就会原样出现在 Cloud 页面上：

- 产品名 `Milvus`；
- 本机地址 `localhost:19530`、`127.0.0.1`；
- 默认的用户名与密码 `root:Milvus`；
- 自部署才有的配置文件 `milvus.yaml`。

WP6 检查**生成后的页面**，出现规则文件 `product-names.yaml` 中的写法、又不在放行清单中的，这一页失败（[产品需求场景 1](../../prd.md#场景-1把产品名和连接值写成变量)，系统行为 1-6）。它只提供函数，还没有接入任何命令（WP8）。

## 文件地图

都在 `packages/docs-tooling/src/shared-docs/` 下：

| 文件 | 做什么 |
|---|---|
| `core/product-names/rules.ts` | 读并校验规则文件 |
| `core/product-names/syntax.ts` | 找出不检查的部分：front matter、链接与图片的地址、HTML 的 `href` 与 `src` |
| `core/product-names/scan.ts` | 按整词查找，处理放行短语与最长匹配 |
| `core/product-names/index.ts` | `checkProductNames`：查生成的页面，再到输入中找回位置 |
| `fixtures/product-names-errors/` | 2 个错误码各一个最小样例 |

## 代码怎样工作

1. **读规则文件**：`check` 是必填、不能为空的列表；`allow` 可以不写。`allow` 中每一项去掉首尾空格后，必须含一个空格分开的两部分，防止写一个 `Milvus` 就把产品名整个放过。不合要求报 `PRODUCT_NAMES_INVALID`。
2. **按整词匹配，区分大小写**：

   | 写法 | 规则中有 `Milvus` 时 |
   |---|---|
   | `Milvus`、`(Milvus)`、`Milvus-based` | 命中 |
   | `MilvusClient`、`pymilvus`、`Milvus2` | 不算：前后紧挨着字母、数字或 `_` |
   | `Milvus.yaml`、`docs/Milvus` | 不算：用 `.` 或 `/` 与字母数字连在一起，是文件名或路径 |

   - `milvus.yaml` 本身要查，就在 `check` 中单独列一项。
   - 写不带端口的 `localhost`，任何端口都能查出。
   - 一处同时命中几项时，如 `root:Milvus` 里的 `Milvus`，只报最长的一项，一处错误只出一条报错。
3. **不检查的部分**：front matter；链接与图片的地址。链接文字要检查，代码块也要检查，因为代码示例中的 `localhost:19530` 正是要查出的。
4. **放行**：命中位置落在同一行的某个 `allow` 短语之内时放过，如 `Zilliz Cloud is built on Milvus`。
5. **是否失败只看生成的页面**。生成的页面中有命中，再到这一页用到的输入中，按同样的规则找同一写法：
   1. Cloud 内容文件；
   2. 原文；
   3. 用到的片段；
   4. 用到的变量的值。

   每处找到的位置报一条 `PRODUCT_NAME_FOUND`，指向作者要改的文件与行号；变量的命中指向 `shared-docs/guides/Variables.json` 与键名。同一个片段被引用多次，也只报一条。所有输入中都找不到时（写法来自站点适配），报在页面原文上，不给行号。

## 一个例子走一遍

演示用的小样例，第 2 行写着 `Milvus`，第 3 行写着 `MilvusClient`：

```
example.md:2 PRODUCT_NAME_FOUND  Generated guides page contains "Milvus"
  修改：换成 Cloud 的变量，或在 product-names.yaml 的 allow 中补一个完整的短语
```

只报第 2 行。然后在规则文件的 `allow` 中加一个单词 `Milvus`：

```
shared-docs/guides/product-names.yaml:4 PRODUCT_NAMES_INVALID  allow entries must contain a space separating two nonempty parts
```

对三篇试点页的原文运行（内容对齐前，经 WP3 的读取与预处理），每个版本、每个手册的命中数：

| 试点页 | `Milvus` | `localhost:19530` | `root:Milvus` |
|---|---:|---:|---:|
| Delete Entities | 0 | 7 | 6 |
| Filtered Search | 6 | 10 | 10 |
| OpenAI | 17 | 1 | 0 |

这是当时用的三项规则的结果。审阅后规则扩成了五项（见下文），对齐时还会多出 `milvus.yaml` 与其他端口的 `localhost`。这些就是内容对齐时要逐处处理的清单。

## 审阅后改的规则

审阅时讨论了 `milvus.yaml` 与 `localhost`：它们在 Cloud 上都不该出现，但 WP6 的匹配规则不用改，要改的是清单。产品需求中 Phase 1 的初始清单因此扩成五项（设计仓库 [#38](https://github.com/liyun95/milvus-zilliz-docs-design/pull/38)）：

```yaml
check:
  - Milvus
  - localhost       # 任何端口
  - 127.0.0.1
  - root:Milvus
  - milvus.yaml
```

修改提示也分成两类：

- 产品名、连接地址、用户名与密码：改成变量；
- `milvus.yaml` 这类写法：说明这一段讲的是 Cloud 没有的功能，要用变换删掉或替换这一段。

正式的 `shared-docs/guides/product-names.yaml` 在接入第一篇页面时按这份清单建。

## 自己试一试

WP6 已合并到 zdoc 的 master。在你的 zdoc 检出中更新到最新、安装依赖，然后在仓库根目录运行下面的命令：

```bash
git checkout master && git pull
```

```bash
corepack enable && pnpm install --frozen-lockfile
```

1. 运行上面的小样例，看到两个结果：

   ```bash
   wp6_demo="$(mktemp -d)"
   ```

   ```bash
   node -e 'require("./scripts/lib/load-typescript").loadTypeScript(require("node:path").resolve("packages/docs-tooling/src/shared-docs/testing/product-names/demo.ts")).runProductNamesDemo(process.argv[1])' "$wp6_demo"
   ```

2. 重新统计三篇试点页的命中数：

   ```bash
   node -e 'require("./scripts/lib/load-typescript").loadTypeScript(require("node:path").resolve("packages/docs-tooling/src/shared-docs/testing/product-names/pilots.ts")).countPilotProductNames().then(rows => console.log(JSON.stringify(rows, null, 2)))'
   ```

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `testing/product-names/check.test.ts` | 整词规则的每个例子、最长匹配、放行、不检查的部分、找回位置（片段、内容文件、变量） |
| `testing/product-names/rules.test.ts` | 规则文件的各种写错的情况 |
| `testing/product-names/pilots.test.ts` | 三篇试点页、两个版本、各个手册都能跑通 |

## 刻意没做的

- **接入命令、在两版合并前调用**：WP8、WP11。
- **排除被变换替换或删除的原文**：WP10。现在找回位置时查的是整篇原文。
- **milvus-docs 侧只提示、不拦截的检查**：技术设计 07 留给实现决定，不在 Phase 1a。

## 证据

- 合并时 `pnpm test:shared-docs` 为 25 个测试文件、293 个测试，全部通过；`pending.json` 只删了 WP6 的 4 个编号。
- 上面的演示与试点页统计在合并后的 master（`ca1cbd5`）上实际运行（2026-10-23）。
- 扩充清单前，用 WP6 的代码实测：`` Edit `milvus.yaml` `` 命中 `milvus.yaml`，`http://localhost:8080` 命中 `localhost`，`127.0.0.1:19530` 命中 `127.0.0.1`。
