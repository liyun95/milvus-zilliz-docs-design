# 05 生成结果交给发布

共享页在 zdoc 现有的 Fetch 工作流中生成，生成完交给 zdoc 现有的发布流程，与尚未迁移的飞书页面一起写入 dev。本篇定义交接的是哪三样东西、各长什么样，以及发布流程怎样用它们做保护、翻译与恢复。一页什么时候从飞书切换到 Git、导航与归属怎样划分，见 [05b](./05b-cutover-and-ownership.md)。

对应的产品需求见[产品需求第 6 节](../prd.md#6-对现有能力的要求)。

**参与方**：zdoc 生成（产出交接物）、zdoc 发布（Fetch 工作流、stage、校验与串行发布队列）。

**状态**：由原接口设计迁入，待工程维护者完善；Fetch 的具体接入点与重新生成比对的接法待核实，UAT 部署目前不是自动的，见[Phase 1 实施计划第 6.1 节](../phase-1.md#61-待确认的接口)。

## 约定

### 交接发生在哪里

几个 zdoc 的现有概念（见[术语表](../glossary.md#发布)）：**Fetch** 是 zdoc 的发布工作流；**dev** 是 zdoc 存放生成结果的分支，网站从它构建，Prod 与 UAT 用同一个 dev 提交；**stage** 是 Fetch 中的内容暂存区，生成结果在这里校验后才进入发布。

共享页的生成放进 Fetch，不另起发布线：

| 顺序 | 做什么 | 是否交接 |
|---|---|---|
| 1. PR 合并前 | PR 校验：生成一遍候选结果，检查能否合并（见下文） | 否，不写 dev |
| 2. 合并后，Fetch 运行 | 新增的“生成共享页”步骤与抓取飞书正文并行；工具代码与 `shared-docs/` 都从 master 读取，不必等 master→dev 同步 | — |
| 3. 交接 | 生成的页面 MDX 放进 Guides 的临时组装目录，与飞书渲染出的 MDX 放在一起；同时交出记录文件与图片 | 是 |
| 4. 现有发布流程 | 导航生成、校验、试构建、打包，上传图片，写入 dev | — |

#### 触发时机

| 时机 | 触发 |
|---|---|
| 现有的每天 3 次定时运行（`fetch-docs.yml`，UTC 02:00、10:00、18:00，即北京时间 10:00、18:00、02:00） | 照常，同时生成共享页 |
| `shared-docs/` 的 PR 合并到 master 后 | Phase 1 不新增自动触发，等下一次定时运行（理由见[设计理由](#设计理由)） |
| 手动 | 照常：急用时，例如提升 PR 要赶上这次发布、激活后想马上生效，手动运行 `fetch-docs.yml` |

合并后到 UAT 可见的时延 = 等到下一次定时运行（最多 8 小时）+ 一次 Fetch 的耗时 + UAT 部署。

zdoc 现状（文档负责人 2026-10-20 介绍，Fetch 耗时为 2026-10-21 从 GitHub Actions 统计）：

- Fetch 最近 60 次运行中成功 41 次，耗时中位数 69 分钟；10 月 20 日 18:22 那次用了 110 分钟，其中中文 Guides 的抓取一项就占 71 分钟。
- 手动运行时选 `group: guides` 也会抓中文 Guides，所以只跑 Guides 并不比全量快多少。
- Fetch 与写 dev 的 Translation 共用并发组 `docs-production-dev`（`queue: max`），多跑一次，排在后面的运行都要多等。
- 每个 PR 合并到 master 后，同步工作流先跑一遍文档构建，确认不会把构建打坏，再合到 dev，约十几分钟。
- 生成结果写入 dev 后，UAT 目前不会自动部署，文档负责人计划改为自动。
- Jenkins 部署在内网，GitHub Actions 连不到，只能靠探测衔接，待文档负责人另找接法。

#### PR 校验

zdoc 中修改 `shared-docs/` 的 PR（作者修改配置、接入、上游更新、下线、提升）都经过同一套校验，通过后才能合并。校验是**候选运行**：完整生成一遍，但不写 dev、不上传图片、不需要 Cloud 凭据。

| 检查 | 出错规则 |
|---|---|
| 页面配置与链接映射表的写法、变换目标与冲突 | [02](./02-page-config.md#出错时) |
| 按 `lock.yaml` 的 `current` 与 `next` 各生成一遍，Cloud 规则在对应版本上成立，两版能合并 | [04](./04-channels-and-lock.md#出错时) |
| 命名块标记、变量与片段 | [01](./01-named-blocks.md#出错时)、[03](./03-md2md-interfaces.md#出错时) |
| 链接与图片都能解析 | [02b](./02b-links-and-images.md#出错时) |
| 生成的 MDX 通过 zdoc 现有的站点校验 | zdoc 现有规则 |

- 人开的 PR 自动触发校验；工具用 `GITHUB_TOKEN` 开的 PR 或提交到 PR 的改动，由工具显式触发校验，因为用它推送的提交不会自动触发其他工作流。
- 上游更新 PR 另附影响报告（见 [06](./06-upstream-changes.md#pr-的内容)）。

### 交给发布的三样东西

| 交接物 | 是什么 | 放在哪 | 谁用 |
|---|---|---|---|
| 页面 MDX | 每个手册一份，两个版本已合并 | 先放进 Guides 的临时组装目录，最终写入 dev 中该手册的内容目录 | 站点构建、路由插件、翻译 |
| 记录文件 | 每页一份 JSON，记录这次生成用了哪些输入、产出了什么 | dev 中的 `generated/en/manifests/shared-pages/<页面标识>.json` | 翻译清单、覆盖率检查、重新生成比对、恢复 |
| 图片 | 按内容摘要命名的图片文件 | zdoc 现有的图片存储 | 页面 MDX 引用 |

只有已激活的页面才交接、写入 dev。激活之前，这三样只存在于 Fetch 的临时产物中（见 [05b](./05b-cutover-and-ownership.md#切换与激活)）。

### 页面 MDX

每个手册一份，例如 Guides 一份、BYOC 一份。**两个版本在交接前已经合并**：Prod 与 UAT 由同一个 dev 提交构建，不能各放一份文件，所以按 [04](./04-channels-and-lock.md#两个版本怎样合并成一页) 的规则，两版相同的块只输出一次、不加标记，不同的块成对包进 `<NextChannel>`：

```mdx
## Delete entities by filter        ← 两版相同，不加标记

<NextChannel action="exclude">
旧的那一段                          ← 只在 Prod 显示
</NextChannel>
<NextChannel action="include">
新的那一段                          ← 只在 UAT 显示
</NextChannel>
```

`current` 与 `next` 相同时，整页没有任何 `<NextChannel>`，与只读一个版本生成的结果逐字相同。front matter 中的字段见 [02](./07-site-adaptation.md#front-matter)，其中两个与交接有关：

#### 页面身份（`token`）

共享页的 front matter 写 `token: shared-<页面标识>`，如 `token: shared-delete-entities`。它不是飞书文档 ID，只用来标识这一页：

- 路由插件按 `token` 相等，把整页通道传递给日文译文；译文会原样保留 `token`，这部分代码不用改。
- 翻译清单按 `token` 查来源记录时，也要能查到下文的记录文件。

整页通道 `channel`（`next` 或 `retire-in-next`）由飞书表格的 `Release Channel` 决定，见 [04](./04-channels-and-lock.md#只在一个通道存在的页面)。

### 记录文件

每个已激活的共享页，在 dev 中都有一份记录文件：一个 JSON，记录这一页最近一次写入 dev 时用了哪些输入、产出了什么，相当于这一页的 receipt。每次 Fetch 把这一页写入 dev，都同时更新它。它兼作这一页的来源记录，不写进飞书的 source snapshot。

```
generated/en/manifests/shared-pages/
  active.json              # 生效配置：已切换到 Git 的页面清单（见 05b）
  delete-entities.json     # 每个已激活的页面一份记录文件
  openai.json
```

以 Filtered Search 为例（示意）：

```json
{
  "schema_version": 1,
  "page": "filtered-search",
  "token": "shared-filtered-search",
  "inputs": {
    "milvus_docs": {
      "repository": "milvus-io/milvus-docs",
      "current": "a1…",
      "next": "b2…",
      "files": [
        { "path": "site/en/userGuide/search-query-get/filtered-search.md", "current": "sha256…", "next": "sha256…" }
      ]
    },
    "zdoc": {
      "repository": "zilliztech/zdoc",
      "commit": "<shared-docs 所在的 master commit>",
      "files": [
        { "path": "shared-docs/pages/filtered-search/page.yaml", "sha256": "…" },
        { "path": "shared-docs/pages/filtered-search/standard-filtering-cli.md", "sha256": "…" },
        { "path": "shared-docs/Variables.json", "sha256": "…" }
      ]
    },
    "tools": { "zdoc": "<tooling commit>", "md2md": "1.3.0" },
    "images": [
      { "source": "https://milvus-docs.s3.us-west-2.amazonaws.com/assets/filtered-search.png", "sha256": "3f9a…", "object": "shared/3f9a….png" }
    ]
  },
  "outputs": [
    { "manual": "guides", "path": "tutorials/development/search-and-query/filtered-search.md", "sha256": "…" },
    { "manual": "guides-byoc", "path": "tutorials/development/search-and-query/filtered-search.md", "sha256": "…" }
  ],
  "channel": null,
  "notes": []
}
```

| 字段 | 含义 | 谁用 |
|---|---|---|
| `schema_version` | 记录文件的格式版本，目前为 `1` | 读取方判断格式 |
| `page` | 页面标识 | — |
| `token` | 页面身份，`shared-<页面标识>` | 翻译清单、路由插件 |
| `inputs.milvus_docs.repository` | 原文所在的仓库 | 重新生成 |
| `inputs.milvus_docs.current`、`next` | `lock.yaml` 中的两个 commit | 重新生成 |
| `inputs.milvus_docs.files[]` | 用到的每个原文与片段：`path` 相对于仓库根目录，`current`、`next` 是它在两个版本中的摘要 | 判断输入是否变化 |
| `inputs.zdoc.repository`、`commit` | zdoc 仓库，以及 `shared-docs/` 所在的 master commit | 重新生成 |
| `inputs.zdoc.files[]` | 用到的页面配置、Cloud 内容文件、变量文件、链接映射表，各自的路径与摘要 | 判断输入是否变化 |
| `inputs.tools` | 生成工具的 commit 与 md2md 的精确版本 | 用同样的版本重新生成 |
| `inputs.images[]` | 每张图片的原地址（`source`）、摘要（`sha256`）与转存地址（`object`）；外部图片用完整地址 | 恢复时核对图片 |
| `outputs[]` | 每个手册的输出路径与内容摘要 | 覆盖率检查、重新生成比对、恢复 |
| `channel` | 整页通道：`null`（两个版本都有这一页）、`next` 或 `retire-in-next` | 与 front matter 一致，供核对 |
| `notes[]` | 生成时的提示，例如“两个版本的 front matter 不同，已沿用 current” | 审核与排查 |

- 只有已激活的页面才有记录文件；切换前的候选结果只存在于 Fetch 的临时产物中。
- 用到来源记录的地方（覆盖率检查、翻译清单、归属检查）改为同时读取飞书记录与这些记录文件。
- 记录文件用于追溯，不是签名或授权。

### 图片上传

图片按内容转存的规则见 [02b](./02b-links-and-images.md#图片)。上传沿用 Fetch 现有的图片上传开关：

| 运行 | 做什么 |
|---|---|
| 正式运行（定时、master 推送触发、激活；开关为 `write`） | 写入 dev 之前，把还不存在的图片按内容地址上传到 zdoc 现有的图片存储，上传后核对摘要；任何一张失败，这次运行不写 dev |
| 候选运行（PR 校验；开关为 `skip`） | 只算出最终地址，不上传 |

- 候选结果中的图片地址与正式结果完全相同，所以新出现的图片在 PR 预览中暂时显示不出来，合并后的正式运行才会上传。上游更新 PR 的报告列出本次新增或变化的图片及其原地址，供审核人查看。
- 图片存储中按内容命名的对象，只要还有已发布或可恢复的页面引用，就不能被存储的生命周期规则（按时间自动清理旧文件的设置）删除。

### 发布流程怎样使用交接物

#### 发布保护

生成结果接入 zdoc 现有的 stage、校验和串行发布队列。Git 页面和未迁移的飞书页面可以同批发布，但同一页不能有两个来源。生成文件不作为编辑源，保护靠受控来源、重新生成比对和分支权限共同实现：

| 环节 | 要求 | Phase 1 |
|---|---|---|
| 源 PR | 作者只改 Milvus 原文或 `shared-docs/`；预览提供跳转到源文件的编辑入口 | 实现 |
| 分支权限 | 普通作者不能直接推送、强推正式生成分支，也不能绕过检查 | 实现 |
| 候选任务 | 可以生成和预览，没有生产分支、部署或图片存储的写权限；社区 PR 不需要 Cloud 凭据 | 实现 |
| 采用批准 | 以 zdoc 中各类 PR（配置修改、接入、上游更新、下线、提升）的审核合并为准；配置中自称已批准不构成授权 | 实现，沿用 GitHub PR |
| 重新生成比对 | 两个时机：Fetch 写 dev 之前，按记录文件中的输入在干净目录重新生成，与 `outputs` 的摘要比对；有 PR 修改 dev 中共享页的生成结果时（包括手动修改），检查失败。都指出应改的源文件 | 实现；具体接法待核实（见[Phase 1 实施计划第 6.1 节](../phase-1.md#61-待确认的接口)） |
| 产物绑定 | 校验结果绑定实际发布产物的摘要，校验后替换产物时部署拒绝 | 后续按实际风险评估 |
| 核心保护 | 工作流和校验器的改动需工程审核，内容 PR 不能关闭保护 | 实现 |

批准后输入发生变化，需要重新检查和审核。

#### 翻译

- **翻译的输入是页面 MDX 中的 Cloud 正文**：完成组装、产品绑定和格式校验后的版本。写作者不需要为翻译额外命名。
- **沿用 zdoc 现有的翻译机制**：按正文摘要（sourceHash）判断是否要重译，按语义单元切分，保护代码等技术内容，分批提交。翻译清单通过 `token` 找到记录文件。
- **只看 Cloud 输出是否变化**：Cloud 输出不变且已有有效译文时，不因被替换掉的上游内容变化而重译。
- 英文站包含日文；中文是独立站点，公共构建改动按既有测试矩阵检查两站。

#### 恢复

先复用已有的 Git、图片存储和发布记录，只补真实缺口，不先建完整归档（依据见[恢复能力核验](../../research/recovery-capability-audit.md)）：

| 恢复目标 | 做法 |
|---|---|
| 回到 dev 的某个历史状态 | 沿用 zdoc 现有的恢复流程；`generated/en/manifests/shared-pages/` 加进恢复脚本的固定清单，正文、导航、生效配置与记录文件一起恢复 |
| 从输入重新生成 | 读记录文件：按 `inputs.milvus_docs` 的两个 commit 取原文，按 `inputs.zdoc.commit` 取 `shared-docs/`，用 `inputs.tools` 中的版本生成；结果摘要必须与 `outputs` 一致 |
| 图片 | 按 `inputs.images` 中的摘要检查图片存储中的对象是否存在、内容是否一致 |
| 已发布站点回滚 | 沿用既有的成功发布记录与镜像回滚，不交回飞书 |

源、配置或图片缺失时直接失败，不回退到原地址或最新版本。

### 缓存与运行

- 同一仓库的同一 commit 只检出一次；每个源文件只解析一次，只展开实际用到的部分。
- 缓存身份包含记录文件中的全部输入与生效配置，冷、热构建的结果一致；飞书侧的“内容未变”不能跳过 Git 输入的变化。
- 展开深度、体积、下载并发和超时都设上限，沿用原发布队列。

## 出错时

| 情况 | 结果 |
|---|---|
| PR 校验不通过 | PR 不能合并；各项的出错规则见上文“PR 校验” |
| 图片上传或上传后的摘要核对失败 | 这次正式运行不写 dev |
| 重新生成比对不一致 | Fetch 不写 dev；修改生成结果的 PR 检查失败。都指出应改的源文件 |
| 恢复时源、配置或图片缺失 | 恢复失败，不回退到最新版本 |

## 例子

<details>
<summary>Filtered Search 的一次正式运行（示意）</summary>

1. 上游更新 PR 合并：`lock.yaml` 的 `next` 从 `a1…` 改为 `b2…`。
2. Fetch 运行：用 `a1…` 与 `b2…` 的原文各生成一遍，合并成 Guides 与 BYOC 各一份 MDX，变化的段落成对包进 `<NextChannel>`。
3. 交接：两份 MDX 放进临时组装目录；新出现的图片按摘要上传；记录文件中 `inputs.milvus_docs.next` 更新为 `b2…`。
4. 现有发布流程校验、试构建后写入 dev。UAT 部署后显示新段落，Prod 不变。

记录文件的完整样例见上文“记录文件”。

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么 Phase 1 不在合并后自动触发 Fetch。** 好处有限：UAT 目前要人工部署，Fetch 提前跑完，UAT 上也不会提前看到；Phase 1 只有 3 篇试点页，共享配置的合并很少。代价不小：一次 Fetch 约 70 分钟，只跑 Guides 也要抓中文 Guides；它与 Translation 共用一个串行队列，多跑一次，其他运行都要排队。急用时手动运行即可。UAT 改为自动部署、迁移的页面变多之后再考虑；更省的做法是扩展现有的按页抓取（`fetch-guides-requested.yml`，按页面选择，一次 1–50 页），让它也能接受共享页的页面标识，只重新生成受影响的几页。

**为什么放进 Fetch。** zdoc 的发布已由 Fetch 串行完成，所有运行排队执行，结果写入 dev；共享页走同一条线，校验、组装、翻译交接与恢复都能复用，也避免两条线同时写 dev。

**为什么沿用 `token` 字段。** 现有代码中 `token` 只在两处使用：路由插件按相等传递整页通道，翻译清单按它查来源记录；日文译文会保留它。沿用这个字段，填一个唯一的非飞书值，改动最少。另设新字段名字更准确，但要改这两处代码，并让已有的飞书页面兼容两种字段。加 `shared-` 前缀，是为了一眼区分 Git 共享页和飞书页面。

**为什么来源记录与 receipt 合成一份、单独存放。** 两者记的大部分相同，都是这一页用了哪些输入、生成了什么，分成两份只会互相重复。飞书来源记录的格式要求多维表格 token、文档 token 等字段，Git 页面填不了，硬塞只能填假值，反而让依赖这些字段的检查出错。zdoc 已有按手册记录飞书修订的 `generated/en/manifests/lark-revisions/`，记录文件放在它旁边，同样归 dev、由 Fetch 写入。

**为什么候选运行不上传图片。** 候选任务不应有图片存储的写权限；预览改用原地址虽然能看到新图，但预览结果会与正式结果不同，重新生成比对就失去意义。所以候选与正式使用相同的地址，由 PR 报告列出原地址供审核。

</details>

## 验收

- **T06**：MDX、路由与资源。
- **T08**：缓存。
- **T09**：翻译。
- **T10**：恢复。
- **T12**：完整旅程与发布保护。
