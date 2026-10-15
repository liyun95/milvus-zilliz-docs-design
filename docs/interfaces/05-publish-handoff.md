# 05 生成结果交给发布

zdoc 生成的共享页要进入 zdoc 现有的暂存、校验、发布、翻译与恢复流程，并与尚未迁移的飞书页面共存。本篇按发生的先后定义两者之间的交接：生成在哪里运行、PR 上怎样校验、写入 dev 时带上什么，以及出了问题怎样恢复。一页什么时候从飞书切换到 Git、导航与归属怎样划分，见 [05b](./05b-cutover-and-ownership.md)。

**参与方**：zdoc 生成（产出）、zdoc 发布（Fetch 工作流、stage、校验与串行发布队列）。

**状态**：已定义，待文档负责人确认；UAT 部署的触发方式、Fetch 的具体接入点与重新生成比对的接法待核实，见[首期实施计划第 6.1 节](../phase-1.md#61-待确认的接口)。

## 约定

### 运行位置与触发

共享页的生成放进 zdoc 现有的 Fetch 工作流，不另起发布线：

- Fetch 中新增“生成共享页”的步骤，与抓取飞书正文并行。生成的 MDX 放进 Guides 的临时组装目录，与飞书渲染出的 MDX 放在一起；之后的导航生成、校验、试构建、打包和写入 dev 沿用现有流程。
- Fetch 运行时工具代码取自 master，`shared-docs/` 也从 master 读取，不必等待 master→dev 同步。

| 时机 | 触发 |
|---|---|
| 现有的每天 3 次定时运行 | 照常，同时生成共享页 |
| 任何修改 `shared-docs/` 的 PR 合并到 master 后 | 新增：自动触发一次只处理 Guides 的 Fetch；是否采用待确认 |
| 手动 | 照常；激活也通过手动触发（见 [05b](./05b-cutover-and-ownership.md#切换与激活)） |

合并后到 UAT 可见的时延 = 一次 Fetch 的耗时 + UAT 部署。不新增触发时，最多等到下一次定时运行（8 小时）。

### PR 校验

zdoc 中修改 `shared-docs/` 的 PR（作者修改配置、接入、上游更新、下线、提升）都经过同一套校验，通过后才能合并：

| 检查 | 出错规则 |
|---|---|
| 页面配置与链接映射表的写法、变换目标与冲突 | [02](./02-page-config.md#出错时) |
| 按 lock 的 `current` 与 `next` 各生成一遍，Cloud 规则在对应版本上成立，两版能合并 | [04](./04-channels-and-lock.md#出错时) |
| 命名块标记、变量与片段 | [01](./01-named-blocks.md#出错时)、[03](./03-md2md-interfaces.md#出错时) |
| 链接与图片都能解析 | [02b](./02b-links-and-images.md#出错时) |
| 生成的 MDX 通过 zdoc 现有的站点校验 | zdoc 现有规则 |

- 校验是候选运行：不写 dev，不上传图片，不需要 Cloud 凭据。
- 人开的 PR 自动触发校验；工具用 `GITHUB_TOKEN` 开的 PR 或提交到 PR 的改动，由工具显式触发校验，因为用它推送的提交不会自动触发其他工作流。
- 上游更新 PR 另附影响报告（见 [06](./06-upstream-changes.md#pr-的内容)）。

### 页面身份（`token`）

共享页的 front matter 写 `token: shared-<页面标识>`，如 `token: shared-delete-entities`。它不是飞书文档 ID，只用来标识这一页：

- 路由插件按 `token` 相等，把整页通道（`channel: next` / `retire-in-next`）传递给日文译文；译文会原样保留 `token`，这部分代码不用改。
- 翻译清单按 `token` 查来源记录时，也要能查到下文的记录文件。

### 记录文件

每次 Fetch 把一个已切换的共享页写入 dev 时，同时写入这一页的记录文件，说明用了哪些输入、生成了什么。它兼作来源记录与 receipt，不写进飞书的 source snapshot：

```
generated/en/manifests/shared-pages/
  active.json              # 生效配置：已切换到 Git 的页面清单（见 05b）
  delete-entities.json     # 每个已切换的页面一份记录文件
  openai.json
```

| 部分 | 内容 | 用途 |
|---|---|---|
| 身份 | 页面标识、`token` | 翻译清单、路由插件 |
| 输入 | 按仓库分组：milvus-docs 的仓库、`current` 与 `next` 两个 commit，以及用到的原文与片段在两个 commit 中的摘要；zdoc 的仓库、`shared-docs/` 所在的 master commit，以及用到的页面配置、Cloud 内容文件、变量文件、链接映射表的摘要。另记工具与 md2md 的版本、每张图片的原地址、摘要与转存地址 | 重新生成、比对、判断是否变化 |
| 输出 | 每个手册的输出路径与内容摘要；整页通道 | 覆盖率检查、比对、恢复 |
| 备注 | 生成时的提示，例如“两个版本的 front matter 不同，已沿用 current” | 审核与排查 |

- 每组中的路径都相对于该仓库的根目录；外部图片用完整地址记录。
- 只有已切换的页面才写入 dev。切换前的候选结果只存在于 Fetch 的临时产物中。
- 用到来源记录的地方（覆盖率检查、翻译清单、归属检查）改为同时读取飞书记录与这些记录文件。
- 记录文件用于追溯，不是签名或授权。

### 图片上传

图片按内容转存的规则见 [02b](./02b-links-and-images.md#图片)。上传沿用 Fetch 现有的图片上传开关：

| 运行 | 做什么 |
|---|---|
| 正式运行（定时、master 推送触发、激活；开关为 `write`） | 写入 dev 之前，把还不存在的图片按内容地址上传到 zdoc 现有的图片存储，上传后核对摘要；任何一张失败，这次运行不写 dev |
| 候选运行（PR 校验；开关为 `skip`） | 只算出最终地址，不上传 |

候选结果中的图片地址与正式结果完全相同，所以新出现的图片在 PR 预览中暂时显示不出来，合并后的正式运行才会上传。上游更新 PR 的报告列出本次新增或变化的图片及其原地址，供审核人查看。图片存储中按内容命名的对象，只要还有已发布或可恢复的页面引用，就不能被生命周期规则删除。

### 发布保护

生成结果接入 zdoc 现有的内容暂存区（stage）、校验和串行发布队列。Git 页面和未迁移的飞书页面可以同批发布，但同一页不能有两个来源。生成文件不作为编辑源，保护靠受控来源、重新生成比对和分支权限共同实现：

| 环节 | 要求 | 首期 |
|---|---|---|
| 源 PR | 作者只改 Milvus 原文或 `shared-docs/`；预览提供跳转到源文件的编辑入口 | 实现 |
| 分支权限 | 普通作者不能直接推送、强推正式生成分支，也不能绕过检查 | 实现 |
| 候选任务 | 可以生成和预览，没有生产分支、部署或图片存储的写权限；社区 PR 不需要 Cloud 凭据 | 实现 |
| 采用批准 | 以 zdoc 中各类 PR（配置修改、接入、上游更新、下线、提升）的审核合并为准；配置中自称已批准不构成授权 | 实现，沿用 GitHub PR |
| 重新生成比对 | 两个时机：Fetch 写 dev 之前，按记录文件中的输入在干净目录重新生成并比对；有 PR 修改 dev 中共享页的生成结果时（包括手动修改），检查失败。都指出应改的源文件 | 实现；具体接法待核实 |
| 产物绑定 | 校验结果绑定实际发布产物的摘要，校验后替换产物时部署拒绝 | 后续按实际风险评估 |
| 核心保护 | 工作流和校验器的改动需工程审核，内容 PR 不能关闭保护 | 实现 |

批准后输入发生变化，需要重新检查和审核。

### 翻译输入

翻译输入是完成组装、产品绑定和格式校验后的 Cloud 正文，沿用 zdoc 现有的 sourceHash、候选选择、语义单元、技术内容保护和批次机制，写作者不需要为翻译额外命名。Cloud 输出不变且已有有效译文时，不因被替换的上游内容变化而重译。英文站包含日文；中文是独立站点，公共构建改动按既有测试矩阵检查两站。

### 恢复

先复用已有的 Git、图片存储和发布记录，只补真实缺口，不先建完整归档：

| 恢复目标 | 做法 |
|---|---|
| 回到 dev 的某个历史状态 | 沿用 zdoc 现有的恢复流程；`generated/en/manifests/shared-pages/` 加进恢复脚本的固定清单，正文、导航、生效配置与记录文件一起恢复 |
| 从输入重新生成 | 读记录文件：按其中的两个 commit 取 milvus-docs，按 zdoc commit 取 `shared-docs/`，用记录中的工具版本生成；结果摘要必须与记录一致 |
| 图片 | 按记录中的摘要检查图片存储中的对象是否存在、内容是否一致 |
| 已发布站点回滚 | 沿用既有的成功发布记录与镜像回滚，不交回飞书 |

源、配置或图片缺失时直接失败，不回退到原地址或最新版本。[恢复核验](../../research/recovery-capability-audit.md)

### 缓存与运行

同一 repository + commit 共用一次检出，每个源文件只解析一次，只展开实际用到的部分。缓存身份包含记录文件中的全部输入与生效配置；冷热构建结果一致，飞书侧的“内容未变”不能跳过 Git 输入的变化。展开深度、体积、下载并发和超时都设上限，沿用原发布队列。

## 出错时

| 情况 | 结果 |
|---|---|
| 图片上传或上传后的摘要核对失败 | 这次正式运行不写 dev |
| 重新生成比对不一致 | Fetch 不写 dev；修改生成结果的 PR 检查失败。都指出应改的源文件 |
| 恢复时源、配置或图片缺失 | 恢复失败，不回退到最新版本 |

## 例子

<details>
<summary>Filtered Search 的记录文件（示意）</summary>

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

`channel` 是整页通道；这一页在两个版本中都存在，所以为 `null`。

</details>

## 设计理由

**为什么放进 Fetch。** zdoc 的发布已由 Fetch 串行完成，所有运行排队执行，结果写入 dev；共享页走同一条线，校验、组装、翻译交接与恢复都能复用，也避免两条线同时写 dev。

**为什么沿用 `token` 字段。** 现有代码中 `token` 只在两处使用：路由插件按相等传递整页通道，翻译清单按它查来源记录；日文译文会保留它。沿用这个字段，填一个唯一的非飞书值，改动最少。另设新字段名字更准确，但要改这两处代码，并让已有的飞书页面兼容两种字段。加 `shared-` 前缀，是为了一眼区分 Git 共享页和飞书页面。

**为什么来源记录与 receipt 合成一份、单独存放。** 两者记的大部分相同，都是这一页用了哪些输入、生成了什么，分成两份只会互相重复。飞书来源记录的格式要求多维表格 token、文档 token 等字段，Git 页面填不了，硬塞只能填假值，反而让依赖这些字段的检查出错。zdoc 已有按手册记录飞书修订的 `generated/en/manifests/lark-revisions/`，记录文件放在它旁边，同样归 dev、由 Fetch 写入。

**为什么候选运行不上传图片。** 候选任务不应有图片存储的写权限；预览改用原地址虽然能看到新图，但预览结果会与正式结果不同，重新生成比对就失去意义。所以候选与正式使用相同的地址，由 PR 报告列出原地址供审核。

## 验收

- **T06**：MDX、路由与资源。
- **T08**：缓存。
- **T09**：翻译。
- **T10**：恢复。
- **T12**：完整旅程与发布保护。
