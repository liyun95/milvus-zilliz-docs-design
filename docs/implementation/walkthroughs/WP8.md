# WP8 走读：生成命令与 PR 校验

**仓库**：zdoc　**上游 PR**：WP8a [zilliztech/zdoc#822](https://github.com/zilliztech/zdoc/pull/822)（commit [`d3d1cbe`](https://github.com/zilliztech/zdoc/commit/d3d1cbe58af0324039a9086366c0e3d823c7f902)）；WP8b [zilliztech/zdoc#832](https://github.com/zilliztech/zdoc/pull/832)（commit [`8680736`](https://github.com/zilliztech/zdoc/commit/86807361cdca0f2b768f51d7ff47c5b78461bee8)，经 zdoc 文档负责人 review）　**任务卡**：[WP8](../tasks/WP8-zdoc-build-and-validate.md)

## 解决什么问题

WP3 到 WP6 各自做好了一步：读取、链接与图片、站点适配、产品名检查。但还没有一条命令把它们串起来，也没有任何东西在 PR 中自动运行。WP8 补上这两件事：

- **WP8a**：一条命令 `shared-docs build`，为每一页、每个手册生成 Cloud 的 MDX。有错误时一次全部报出，一个文件都不写。
- **WP8b**：两个工作流。接入一页时，自动给 PR 写入 `lock.yaml`；每个发往 master 的 PR 都跑一遍生成，生成失败就不能合并（[产品需求](../../prd.md#场景-3接入一页) 3-3）。

WP8 不写 dev、不上传图片。合并后进入 Fetch、真正发布，是 WP9 的事。

## 文件地图

都在 `packages/docs-tooling/src/shared-docs/` 下，除非另外写明：

| 文件 | 做什么 | PR |
|---|---|---|
| `adapters/build-page.ts` | 一页的整条流水线；一次运行中共用的缓存 | WP8a |
| `adapters/guides-snapshot.ts` | 从 dev 检出中读飞书表格快照（`GuidesBase` 的真实实现） | WP8a |
| `commands/build.ts` | 命令行 `shared-docs build` | WP8a |
| `commands/lock.ts` | 命令行 `shared-docs lock`：给还没有 `lock.yaml` 的页面写入 | WP8b |
| `.github/workflows/shared-docs-validate.yml`（仓库根目录） | PR 校验 | WP8b |
| `.github/workflows/shared-docs-lock.yml`（仓库根目录） | 接入时写 lock | WP8b |
| `scripts/validate-workflow-policy.js`（仓库根目录） | zdoc 现有的工作流规则检查，新增对这两个工作流的约束 | WP8b |

## 代码怎样工作

### WP8a：`shared-docs build`

```bash
pnpm docs-tooling shared-docs build --shared-docs <目录> --repo <milvus-docs 检出> --dev <zdoc dev 检出> --out <输出目录> [--page <页面标识>] [--image-timeout <秒>]
```

1. **先读全部配置**：`source.yaml`、`Variables.json`、`links.yaml`、`product-names.yaml`、Tabs 规则，以及每一页的 `page.yaml` 与 `lock.yaml`。即使只生成一页，也要知道全部共享页，因为别的页面可能链接到它。
2. **核对页面在飞书中存在**：Phase 1 只能接入飞书目录中已有节点的页面。所以 `publish[].path` 必须在 dev 的这个手册中有对应的页面，飞书表格快照中也要有这一页，否则报 `CONFIG_PATH_UNKNOWN`。导航（`sidebar_label`、`sidebar_position`）也取自 dev 上这一页现有的 MDX。
3. **对每一页**：
   1. 读取（WP3）：两个版本的原文、命名块、删标记、展开变量与片段；
   2. 对每个版本准备链接与图片的材料（WP5），读目标页的原文、下载图片；
   3. 对每个手册依次：改写链接与图片（WP5）→ 站点适配并编译（WP4）→ 产品名检查（WP6）。
4. **比较两个版本**：每个手册分别比较 `current` 与 `next` 生成的 MDX。相同就输出一份；不同就拒绝这一页，提示两版合并要等 WP11。
5. **全部通过才写**：输出 `<输出目录>/<手册>/<publish.path>.mdx`，以及一份 `images.json`，列出每张图片的原地址、摘要与新地址。有任何一页出错，就一个文件都不写。

两个限制：

- `page.yaml` 中写了 `transforms` 就报 `CONFIG_FIELD_UNKNOWN`，因为变换要等 WP10。不能跳过：跳过会生成内容不对的页面。
- 输出目录必须是空的，不覆盖上一次的结果。

**省时间的地方**：

- 同一个提交的 Milvus 原文只读一次，用一次批量读取。
- 同一个外部图片只下载一对（每次都下载两遍来比较），所有版本、手册、页面共用这一对结果；所以“读取过程中图片被换掉”仍能查出。
- dev 的页面清单与飞书快照各读一次。

### WP8b：两个工作流

| | `shared-docs-validate` | `shared-docs-lock` |
|---|---|---|
| 什么时候跑 | 每个发往 master 的 PR，打开、更新、重新打开时；也可以被手动触发（由 lock 工作流使用） | 发往 master、并且改了 `shared-docs/pages/**` 的 PR |
| 权限 | 只读，不用任何 secret | 可以向 PR 分支推送、触发其他工作流；只在推送与触发这两步拿到令牌 |
| 做什么 | 没改 `shared-docs/` 的 PR 约 10 秒通过，不装依赖也不生成；改了的就完整跑一遍 `shared-docs build` | 给还没有 `lock.yaml` 的新页面写入（两个版本都取跟踪分支的最新提交），推送到 PR 分支，再触发校验并等它跑完 |
| fork 来的 PR | 照常校验（只读） | 不写任何东西，在检查结果中提示“请改从仓库内的分支提交”（`LOCK_FORK_PR`） |

几个细节：

- **为什么要“触发并等待”**：用工作流自带的令牌推送的提交，不会自动触发其他工作流。所以 lock 工作流推送后，要显式触发一次校验，并按一个唯一的请求编号找到那次运行、等它结束，这与 zdoc 现有的 `sync-master-tooling-to-dev.yml` 相同。
- **推送很保守**：只允许推送新增的 `lock.yaml`，文件模式必须是普通文件。推送前确认 PR 分支没被别人动过，动过就停下，绝不强推。
- **校验读什么**：
  - 只克隆 milvus-docs 跟踪的那一个分支，但保留完整历史，因为 WP3 判断祖先关系要用；
  - zdoc dev 只取英文 Guides、BYOC 与飞书快照三个路径，固定在一个确定的提交上。
- **只在发往 master 的 PR 上跑**：工具同步会把工作流文件复制到 dev。不限定分支的话，发往 dev 的自动化 PR（几乎全是机器人开的）上也会多出一项“等待批准”的检查。审阅时加上了这条限制。

## 一个例子走一遍

### `shared-docs build` 的合成演示

演示建一个临时的 milvus-docs、一个临时的 dev，在本机起一个图片服务，然后运行真实的命令行。Guides 手册的输出中有这些行：

```mdx
title: "Pipeline example | Cloud"
slug: /build-pipeline
sidebar_label: "guides navigation"
sidebar_position: 4
Use Zilliz Cloud in eu-west.
A fragment for Zilliz Cloud.
## Local & API\{#local-and-api}
[Here](#local-and-api), [shared](./shared-target#target-and-api), [mapped](./mapped-cloud), [Cloud](./cloud-page).
![Repository](shared/cdf3cefe…f79.png)
<Tabs groupId="code" defaultValue='python' values={[{"label":"Python","value":"python"},{"label":"Java","value":"java"}]}>
```

前面各工作包的结果都在一页里出现了：

| 输出 | 来自 |
|---|---|
| 变量与片段换成 Cloud 的值 | WP3 |
| 页内锚点、共享页链接、映射表链接、同名页链接都换成 Cloud 的写法 | WP5 |
| 图片换成按内容命名的地址 | WP5 |
| 标题锚点、`<Tabs>`、front matter，导航取自 dev | WP4 |

然后在 `page.yaml` 中加一条变换，再运行一次：报 `CONFIG_FIELD_UNKNOWN`，命令以 1 结束，什么都没写。

### 三篇试点页（内容对齐之前）

在 milvus-docs `9acdc99` 上运行，dev 取当时的最新提交。三篇都失败，这是预期的，失败的原因就是内容对齐要做的事：

| 试点页 | 结果 |
|---|---|
| Delete Entities（两个版本 × Guides、BYOC） | 52 处 `PRODUCT_NAME_FOUND`：每个版本、每个手册 7 处 `localhost`、6 处 `root:Milvus` |
| Filtered Search（两个版本 × Guides、BYOC） | 4 处 `LINK_UNKNOWN_FORM`：第 257 行的 `filtering` 漏写 `.md` |
| OpenAI（两个版本 × Guides） | 4 处 `LINK_UNRESOLVED`：第 126 行的 `configure-docker.md` 与第 198 行的 `embedding-function-overview.md` |

Filtered Search 最初还报了 8 处 `IMAGE_FETCH_FAILED`。审阅时查明是超时：从国内下载 Milvus 在美国西部存储中的一张图片要 47 秒左右，而下载器只等 30 秒。所以命令的默认超时改为 120 秒，加了 `--image-timeout`，报错也附上了原因（如 “The operation was aborted due to timeout”）。

### 两个工作流的演示

在 fork 中开了一个演示 PR（[liyun95/zdoc#10](https://github.com/liyun95/zdoc/pull/10)），加一篇合成的页面：

| 提交 | 发生了什么 | 结果 |
|---|---|---|
| `4646faf` | 新增页面，没有 `lock.yaml` | lock 工作流成功，自动推送了下一个提交 |
| `fd30c64`（作者 github-actions） | 自动写入的 `lock.yaml` | 校验被显式触发，通过 |
| `1d0ae8e` | 故意写入一个产品名 | 校验失败，指出第 8、10 行 |
| `ce97d49` | 改回来 | 校验通过；lock 工作流发现 lock 已存在，什么都不做 |

## 自己试一试

WP8a 已合并到 zdoc 的 master。在你的 zdoc 检出中更新到最新、安装依赖，然后在仓库根目录运行下面的命令：

```bash
git checkout master && git pull
```

```bash
corepack enable && pnpm install --frozen-lockfile
```

运行合成演示。会打印输出的统计、Guides 手册的整页 MDX，以及加了变换后那次运行的报错：

```bash
wp8_demo="$(mktemp -d)"
```

```bash
node -e 'const { loadTypeScript } = require("./scripts/lib/load-typescript"); const path = require("node:path"), fs = require("node:fs"); loadTypeScript(path.resolve("packages/docs-tooling/src/shared-docs/testing/build/demo.ts")).runBuildDemo(process.argv[1]).then(result => { console.log(JSON.stringify(result.summary, null, 2)); console.log(fs.readFileSync(path.join(result.out, "guides/tutorials/build-pipeline.mdx"), "utf8")); console.log(result.failure.stdout) })' "$wp8_demo"
```

WP8b 已合并。在 zdoc 任何一个发往 master 的 PR 的检查列表中，都能看到 `shared-docs-validate`：没改 `shared-docs/` 的 PR，它约 10 秒通过，运行摘要写着 “No shared-docs inputs changed”。`shared-docs-lock` 要等第一篇页面接入时才会出现。

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `testing/build/build.test.ts` | 整条流水线（`3-4`）；只生成一页时仍认得全部共享页；两版不同时拒绝；变换报错；图片的成对下载与失败原因；`CONFIG_PATH_UNKNOWN` 的两种情况 |
| `testing/build/guides-snapshot.test.ts` | 飞书快照的实际格式：`publish_targets` 是产品名、`output_paths` 为空、`release_channel` 大小写不定 |
| `testing/lock-command.test.ts` | 只给没有 lock 的页面写入、已有的不改、fork 拒绝（WP8b） |
| `testing/workflows.test.ts` | 两个工作流在真实的 Git 仓库与模拟的 GitHub 上逐步运行：没改 `shared-docs/` 时直接通过、推送前检查分支、只推 `lock.yaml`（WP8b） |
| `scripts/validate-workflow-policy.test.js`（仓库根目录） | 违反约束的写法会被拦下：多了权限、令牌出现在不该出现的步骤、漏了分支限制（WP8b） |

## 刻意没做的

- **写 dev、上传图片、记录文件、接入 Fetch**：WP9。
- **两版合并**：WP11；**变换**：WP10；**整页通道 `channel`**：WP13。
- **上游更新、提升、比较三个工作流**：WP12、WP13、WP14。
- **分支保护与 `CODEOWNERS`**：不在 PR 中改，由推动者在 GitHub 上设置：把 `shared-docs-validate` 设为 master 的必需检查。
- **整站构建**：PR 校验只做逐页编译；整站的试构建在 Fetch 中做（WP9）。

## 已知的问题

- **测试的时限**：WP8a 合并后，master→dev 的工具同步失败过一次（[#823](https://github.com/zilliztech/zdoc/pull/823)）。那次分到的 runner 每一步都慢了 4 到 6 倍，几个要另起进程的测试超过了 5 秒的默认时限。[#824](https://github.com/zilliztech/zdoc/pull/824) 给这类测试统一设了 120 秒的文件级时限，WP8b 的两个新测试文件也照此设置。以后新增要另起进程的测试，也要这样设。

## 证据

- WP8a 合并时 `pnpm test:shared-docs` 为 37 个测试文件、397 个测试通过，另有 4 个需要联网的测试默认跳过；`spec/requirements.json` 与设计仓库逐字节相同（77 个错误码）。
- WP8b 合并时为 39 个测试文件、474 个测试通过；zdoc 的工作流规则测试 118 个通过。zdoc 文档负责人独立复现了测试数字，并找出 1 个 P1（作者推送可能取消正在等待的校验，造成误报失败）与 4 个 P2，都在合并前修复。[#832](https://github.com/zilliztech/zdoc/pull/832) 本身跑出了第一次 `shared-docs-validate`，因为没改 `shared-docs/`，约 10 秒通过；合并后的站点校验与同步到 dev 都成功。
- Filtered Search 的图片超时由审阅人在国内网络上复现，放宽超时后两张图片都下载成功（2026-10-23）。
