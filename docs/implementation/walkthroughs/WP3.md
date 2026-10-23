# WP3 走读：读取页面配置、锁定的原文与命名块

**仓库**：zdoc　**上游 PR**：WP3a [zilliztech/zdoc#796](https://github.com/zilliztech/zdoc/pull/796)（commit [`5844587`](https://github.com/zilliztech/zdoc/commit/5844587037d5397e8ebd1510235db5d8592584d7)），WP3b [zilliztech/zdoc#800](https://github.com/zilliztech/zdoc/pull/800)（commit [`31a9b54`](https://github.com/zilliztech/zdoc/commit/31a9b54176c9adc50515f84a559b4082700b6620)）　**任务卡**：[WP3](../tasks/WP3-zdoc-read.md)

## 解决什么问题

一篇共享页要生成，先得回答四个问题：

1. 这一页的配置写得对不对：`source.yaml`、`page.yaml`、`lock.yaml`、`Variables.json`；
2. Prod 与 UAT 各用 milvus-docs 的哪个 commit，那个 commit 中的原文是什么；
3. 原文中有哪些命名块，每块是普通 Markdown 还是代码组、有哪些语言；
4. 删掉标记、换成 Cloud 的变量与片段之后，交给下一步的 Markdown 是什么。

WP3 把这四步做成一个只读的命令 `shared-docs inspect`。它不写任何文件、不联网、不改 milvus-docs 的检出，只把结果打印出来；出错时一次列出全部错误，不给出半成品。之后的站点适配（WP4）、链接与图片（WP5）、产品名检查（WP6）都接在它的输出之后。

WP3 分两个 PR 合并：WP3a 做第 1、2 步，WP3b 做第 3、4 步和命令。

## 文件地图

都在 `packages/docs-tooling/src/shared-docs/` 下：

| 文件 | 做什么 | PR |
|---|---|---|
| `core/yaml.ts`、`core/config.ts` | 读 YAML 并记下每个字段的行号；校验 `source.yaml` 与 `page.yaml` | WP3a |
| `core/lock.ts` | 校验 `lock.yaml`；没有 lock 时算出应写的 lock（产品需求 3-1） | WP3a |
| `core/variables.ts` | 校验 `Variables.json`：是 JSON、顶层是对象、没有只差大小写的键 | WP3b |
| `core/blocks.ts` | 判断每个命名块的类型与语言，得到命名块清单；把行号换算回删标记前的原文 | WP3b |
| `adapters/git-milvus-docs-reader.ts` | 按 commit 从本地 Git 读文件；判断 commit 是否在跟踪分支上、谁是谁的祖先；取出某个 commit 的 `fragments/` | 两个都有 |
| `adapters/read-page.ts` | 把配置、lock 与 Git 读取串起来，得到两个版本的原文 | WP3a |
| `adapters/md2md.ts` | 调用 npm 上的 `@zilliz/mdtomd@1.3.0` | WP3b |
| `adapters/inspect-page.ts` | 整个读取流程：校验 → 读原文 → 命名块清单 → 删标记 → 展开变量与片段 | WP3b |
| `commands/inspect.ts` | 命令行：读文件、调用上面的流程、打印结果 | WP3b |
| `fixtures/read-errors/` 等 | 每个错误码一个最小的错误样例 | 两个都有 |
| `fixtures/md2md-contract/` | 从 md2md `a143b27` 原样复制的 28 个契约用例 | WP3b |

`core/` 中的文件只做计算；读文件、跑 Git、调用 md2md 都在 `adapters/` 与 `commands/` 中，WP0 的边界测试会拦下越界的写法。

## 代码怎样工作

1. **先校验全部配置，再碰 Git**（`inspect-page.ts`）。四个文件各自校验，错误合在一起报；只要有一个出错，就不往下读原文。每个错误都带文件、行号、页面与版本。
2. **确定两个版本的 commit**：
   - 有 `lock.yaml` 时，检查 `current` 与 `next` 都是完整的 commit 号、都在跟踪分支上、`current` 不晚于 `next`；
   - 没有时，按产品需求 3-1，两个版本都取跟踪分支的最新提交，输出中标明“planned (no lock.yaml)”，不写文件。
3. **读原文**（`git-milvus-docs-reader.ts`）。从 Git 对象中按 commit 读，不看工作区：milvus-docs 检出中未提交的修改不会混进来。有两个前提：
   - 跟踪分支要有本地分支，如 `refs/heads/v3.0.x`；
   - 历史要完整，不能是浅克隆，否则判断不了祖先关系。不满足时直接报错，不给出错误的答案。WP8、WP9 准备检出时要照此做。
4. **命名块清单**（`core/blocks.ts`）。先交给 md2md 的 `parseBlocks` 检查标记；标记写错就停在这里。再看每个块里装着什么：

   | 块内的内容 | 类型 | 语言 |
   |---|---|---|
   | 恰好一个代码块 | 代码组 | 取代码块开头的语言名 |
   | 恰好一个语言切换栏加紧跟的代码块 | 代码组 | 按顺序取每个代码块的语言名，不看切换栏的文字 |
   | 其他 | Markdown 块 | — |

   - 代码块的边界与 md2md 的规则逐行一致。
   - 列表中缩进 4 个以上空格的代码块，md2md 不认，这里额外用 `markdown-it` 认出来。
   - 没写语言名的记为 `null`，重复的照原样记，Phase 1 不报错。
5. **删标记、展开变量与片段**：
   - `stripBlockMarkers` 只删标记所在的行；
   - 再调用 md2md 的 `preprocess`，变量表就是 `Variables.json` 原样，不回退到 Milvus 的值（产品需求 1-1）；
   - 片段从同一个 commit 的 Git 对象中取出，放进一个临时目录交给 md2md，用完即删；仓库中的符号链接照样还原，由 md2md 拒绝。
6. **把错误指回作者要改的地方**：
   - 删掉标记后行号会前移，页面上的错误按删掉的行换算回原文的行号；
   - 片段中的错误写成 `site/en/fragments/…` 这样从仓库根目录算起的路径；
   - 用到的每个片段都再检查一遍，片段中不能有命名块标记。
7. **打印**：配置与 lock 的结果、两个版本的 commit、命名块清单、用到的片段与变量、展开后的 Markdown。两个版本即使是同一个 commit 也各打印一份。

## 一个例子走一遍

在一份 milvus-docs `v3.0.x` 的临时克隆中，给 Delete Entities 加两个命名块、一个片段和一个变量（只为演示，没有提交到上游）：

<details>
<summary>改动后的原文（节选）与 Cloud 的变量</summary>

```markdown
<!-- doc:block:start id="filter-intro" -->
## Delete Entities by Filtering Conditions

When deleting multiple entities that share some attributes in a batch, you can use filter expressions. …

{{fragments/cloud-note.md}}
<!-- doc:block:end id="filter-intro" -->

<!-- doc:block:start id="delete-by-filter-code" -->
<div class="multipleCode">
    <a href="#python">Python</a>
    …
</div>

```python
…
```

…

```bash
export CLUSTER_ENDPOINT="{{var.example_endpoint}}"
…
```
<!-- doc:block:end id="delete-by-filter-code" -->
```

`site/en/fragments/cloud-note.md`：`You are using {{var.product_name}}.`

Cloud 的 `Variables.json`（试点页的测试素材）：

```json
{ "product_name": "Zilliz Cloud", "example_endpoint": "YOUR_CLUSTER_ENDPOINT", "example_token": "YOUR_CLUSTER_TOKEN" }
```

</details>

运行 `inspect`，以 0 结束。输出的开头：

```
Page: delete-entities
Configuration: valid
Lock: planned (no lock.yaml)
Source: https://github.com/milvus-io/milvus-docs (v3.0.x) site/en/userGuide/insert-and-delete/delete-entities.md
Publish: guides/tutorials/development/insert-and-delete/delete-entities
Publish: guides-byoc/tutorials/development/insert-and-delete/delete-entities
```

命名块清单：

| ID | 类型 | 语言 | 原文行号 |
|---|---|---|---|
| `filter-intro` | Markdown 块 | — | 11–17 |
| `delete-by-filter-code` | 代码组 | python、java、javascript、go、bash | 19–132 |

依赖中记下了片段 `fragments/cloud-note.md`（被页面引用），以及两个变量：`product_name` 用在片段中，`example_endpoint` 用在页面中。

展开后的 Markdown 中：

- 标记都没有了；
- 片段的位置变成 `You are using Zilliz Cloud.`；
- 被标出的那一处 cURL 示例变成 `export CLUSTER_ENDPOINT="YOUR_CLUSTER_ENDPOINT"`；
- 同一页其他代码组中的 `http://localhost:19530` 仍在。这正是 WP6 产品名检查要查出的漏换。

再弄坏两处，第 140 行加一个 Cloud 没有的变量 `{{var.not_defined}}`，片段中加一对命名块标记，然后再运行：

```
Validation failed: delete-entities
site/en/userGuide/insert-and-delete/delete-entities.md:140 [delete-entities/current] VAR_MISSING: Variable is missing: not_defined
site/en/fragments/cloud-note.md:2 [delete-entities/current] BLOCK_IN_FRAGMENT: Named block markers are not allowed in fragments.
site/en/fragments/cloud-note.md:4 [delete-entities/current] BLOCK_IN_FRAGMENT: Named block markers are not allowed in fragments.
（next 版本的三条相同）
```

命令以 1 结束，不打印展开后的 Markdown。第 140 行是加了标记之后原文中的行号：前面删掉了 4 行标记，工具已经换算回来。

## 自己试一试

WP3 已合并到 zdoc 的 master。在你的 zdoc 检出中更新到最新、安装依赖，然后在仓库根目录运行下面的命令：

```bash
git checkout master && git pull
```

```bash
corepack enable && pnpm install --frozen-lockfile
```

1. 跑全部测试，应全部通过（WP3b 合并时是 17 个测试文件、138 个测试）：

   ```bash
   pnpm test:shared-docs
   ```

2. 用测试素材建一个临时的演示环境：一份合成的 milvus-docs 仓库与 Delete Entities 的配置，都放在系统的临时目录中：

   ```bash
   wp3_demo="$(mktemp -d)"
   ```

   ```bash
   node -e 'require("./scripts/lib/load-typescript").loadTypeScript(require("node:path").resolve("packages/docs-tooling/src/shared-docs/testing/demo.ts")).createInspectDemo(process.argv[1]).then(() => console.log("Temporary demo:", process.argv[1]))' "$wp3_demo"
   ```

3. 运行 `inspect`，看到 `Lock: planned (no lock.yaml)`、两个版本的 commit 与展开后的 Markdown。演示用的原文没有命名块，所以清单为空：

   ```bash
   pnpm docs-tooling shared-docs inspect --pages "$wp3_demo/shared-docs/pages" --page delete-entities --repo "$wp3_demo/milvus-docs"
   ```

4. 把 `page.yaml` 中的手册改成不存在的名字，再运行上一条命令，看到 `page.yaml:7 … CONFIG_MANUAL_UNKNOWN`，命令以 1 结束：

   ```bash
   sed -i.bak 's/manual: guides$/manual: unknown-manual/' "$wp3_demo/shared-docs/pages/delete-entities/page.yaml"
   ```

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `testing/inspect.test.ts` | 整个流程：变量表原样传入、两个版本各用自己 commit 的片段、错误一次报全、没有 lock 时用计划值 |
| `testing/blocks.test.ts` | 命名块的类型与语言：列表中的代码组、各种代码块边界、必须是 Markdown 块的情况 |
| `testing/variables.test.ts` | `Variables.json` 的三种错误 |
| `testing/read-page.test.ts`、`testing/lock.test.ts` | lock 与跟踪分支：不在分支上、顺序颠倒、fork 中的 PR 不能写 lock |
| `adapters/contract/milvus-docs-reader.test.ts` | Git 读取的真实实现与替身跑同一组测试 |
| `fixtures/read-errors/*/` | 每个配置与 lock 错误码的最小输入与期望 |

## 刻意没做的

- **写 lock、开 PR**：只算出应写的 lock，提交由 WP8 做。
- **变换**：`page.yaml` 中的 `transforms` 只检查是不是列表，规则归 WP10。
- **站点适配、链接与图片、产品名检查**：WP4、WP5、WP6。展开后的 Markdown 中还是 Milvus 的写法，如 `<div class="multipleCode">` 与 `boolean.md`。
- **读飞书表格的真实快照**：WP8。
- **仓库根目录的 `shared-docs/`**：第一篇页面正式接入时再建。

## 证据

- 合并时 `pnpm test:shared-docs` 为 17 个测试文件、138 个测试，全部通过；`pending.json` 中剩 108 条，WP3 的已全部删掉。
- `spec/requirements.json` 与当时设计仓库中的版本逐字节相同（75 个错误码）；之后新增的 `LINK_MAP_INVALID` 由 WP5 复制进来。
- 复制的 md2md 契约用例与 md2md `a143b27` 逐字节相同，只用来测真实的包。
- 上面的例子在 milvus-docs `v3.0.x` `6fb1bf9` 的临时克隆上，用合并后的 master（`31a9b54`）运行（2026-10-23）。
