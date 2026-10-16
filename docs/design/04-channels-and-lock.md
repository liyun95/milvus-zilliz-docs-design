# 04 通道与 commit 记录

Cloud 要能在 UAT 提前看到上游的修改，同时让 Prod 保持已上线的版本。本篇定义每个共享页怎样用 `lock.yaml` 记录 Prod 与 UAT 各用 milvus-docs 的哪个 commit，两个版本怎样合并成一份页面，以及 `lock.yaml` 由哪些 PR、怎样改变。对应的产品需求见[产品需求场景 3、6、8、10](../prd.md#场景-6让内容先只在-uat-显示)。

**参与方**：zdoc 生成（读取 `lock.yaml`、按两个版本生成）、接入、下线、上游更新与提升 PR（写入 `lock.yaml`）、文档工程师（发起下线与提升）、zdoc 发布（按通道显示）。

**状态**：由原接口设计迁入，待工程维护者完善。

## 约定

### 共享来源配置与跟踪分支

所有共享页都从同一个仓库读 Milvus 原文。读哪个仓库、跟踪哪个分支，记在共享来源配置中：站点级一份，与页面目录同在 `shared-docs/` 中（见 [02](./02-page-config.md#shared-docs-的位置)）：

```yaml
# shared-docs/source.yaml
schema_version: 1
repository: https://github.com/milvus-io/milvus-docs
track: v3.0.x          # 跟踪分支
```

- **跟踪分支**是 milvus-docs 的默认分支，目前为 `v3.0.x`。接入与上游更新取的“最新提交”都来自它；它只用于发现新提交，正式生成始终使用每页 `lock.yaml` 中锁定的 commit（见下文）。
- Milvus 发布新的大版本分支时，用一个显式的 PR 切换跟踪分支。
- 只写在 `preview` 分支中的内容，合入 `v3.0.x` 后 Cloud 才能读到。Cloud 先于 Milvus 上线的功能，写在 Cloud 内容文件中，用 `<NextChannel>` 包住。

### 每页一份 `lock.yaml`

每个共享页都有一份 `lock.yaml`，放在页面目录中，与 `page.yaml` 并列：`shared-docs/pages/<页面标识>/lock.yaml`（见 [02](./02-page-config.md#shared-docs-的位置)）。它记录这一页在 Prod 与 UAT 上各用 milvus-docs 的哪个 commit，只由工具写入，人不手改（见下文“`lock.yaml` 怎样变化”）。

```yaml
# shared-docs/pages/delete-entities/lock.yaml
# 工具生成，不要手改
schema_version: 1
current: 1997ce96782b31f8628f22d31fad11007e4b924b   # Prod 读取
next: 1997ce96782b31f8628f22d31fad11007e4b924b      # UAT 读取
```

| 字段 | 说明 |
|---|---|
| `schema_version` | 格式版本 |
| `current` | Prod 使用的 milvus-docs commit，完整 SHA；写 `none` 表示 Prod 上没有这一页 |
| `next` | UAT 使用的 milvus-docs commit，完整 SHA；写 `none` 表示 UAT 上没有这一页 |

- 不记页面标识：所在的页面目录已经说明属于哪一页。
- 不记仓库地址与跟踪分支：它们记在共享来源配置中（见上文），不在每页重复；记录的 commit 必须在跟踪分支的历史上。
- 只记“采用哪个版本”，不记文件摘要。一次构建实际用到的输入及其摘要记在记录文件中（见 [05](./05-publish-handoff.md#记录文件)）。

网站上的一页 Cloud 页面由三样东西共同决定，`lock.yaml` 只管其中一样：

| 由什么决定 | 管什么 | 见 |
|---|---|---|
| `lock.yaml` | Git 生成时，Prod 与 UAT 各用 Milvus 原文的哪个版本 | 本篇 |
| `page.yaml` | 拿到原文后怎样加工 | [02](./02-page-config.md) |
| 激活（`active.json`） | 网站上这一页用 Git 生成的版本，还是飞书的版本；只在 Phase 1 过渡时存在 | [05b](./05b-cutover-and-ownership.md#生效配置activejson) |

激活之前，Git 照样按 `lock.yaml` 生成两个版本，只是作为候选结果，网站上仍是飞书版；`lock.yaml` 的变化要等激活之后才体现在网站上。

### 两个版本怎样合并成一页

Prod 与 UAT 由同一个 dev 提交构建，不能各读一份文件，只能在同一份页面中放两个版本，用 `<NextChannel>` 区分（原因见[设计理由](#设计理由)）。所以每次生成分两步：

1. **跑两遍。** 用 `current` 的原文和 `next` 的原文各走一遍生成：定位命名块、按页面配置变换、展开变量与片段、产品过滤、站点适配（见[接口地图](./README.md#生成流水线)）。两遍用同一份 `page.yaml`：不带 `channel` 的规则两遍都必须成立，带 `channel` 的只在对应一遍生效（见 [02](../prd.md#场景-6让内容先只在-uat-显示)）。失败时指出是哪一遍。
2. **合并。** 把两遍的结果合成一份页面：

- 结果按顶层块比较：标题、段落、整个列表、表格、提示框各算一块，代码组整体算一块。相同的块只输出一次；连续的不同块输出成 `exclude`（旧）与 `include`（新）一对；只在一侧存在的块只输出那一侧。
- 两个版本相同时，输出不带通道标记，与单版本生成的结果逐字相同。提升之后即是这种状态。
- front matter 无法按通道区分，两版不同时沿用 `current`，并写入记录文件的备注。
- Cloud 内容文件中手写的 `<NextChannel>` 若落在成对的区域内，生成失败，避免嵌套。
- 共享原文不写通道标记，也不为通道加命名块。作者在哪些地方手写 `<NextChannel>`，见[产品需求场景 6](../prd.md#场景-6让内容先只在-uat-显示)。

### 只在一个通道存在的页面

`lock.yaml` 中一边写 `none`，表示这一页只在另一边存在：

| `lock.yaml` | 含义 | 生成结果 |
|---|---|---|
| `current: none`，`next` 有值 | 新页面，功能还没上线：UAT 显示，Prod 没有这一页 | 带 zdoc 现有的整页标记 `channel: next` |
| `current` 有值，`next: none` | 要下线的页面：Prod 照常显示，UAT 上已没有 | 带 `channel: retire-in-next` |

Prod 上的隐藏，以及从导航、搜索、`llms.txt` 中去掉，都沿用 zdoc 现有的整页通道实现。这两种情况替代飞书多维表格中的 `Release Channel`。

### `lock.yaml` 怎样变化

`lock.yaml` 只由工具写入，人不手改。改它的 PR 共四种，都是普通的 zdoc PR，审核合并后生效：

| PR | 谁发起、怎样发起 | 改什么 | 所属阶段 |
|---|---|---|---|
| 接入一页 | 文档工程师开 PR 新增页面配置，工具自动写入 | `current` 与 `next` 都设为跟踪分支的最新提交；功能还没上线时 `current` 写 `none` | Phase 1a |
| 上游更新 | 工具每天自动发起 | 只改 `next` | Phase 1b |
| 提升 | 文档工程师手动运行工作流 | 把 `current` 的 commit 值改成 `next` 的 commit 值 | Phase 1b |
| 下线一页 | 文档工程师手动运行工作流 | 把 `next` 改为 `none` | Phase 1b，按需 |

提升与下线用 zdoc 中同一个手动工作流：运行时选择操作（“提升”或“下线”）、填写页面，工具生成 PR。

#### 接入一页

1. 文档工程师在 zdoc 中开 PR，新增 `shared-docs/pages/<页面标识>/` 下的 `page.yaml`，需要时加 Cloud 内容文件，不写 `lock.yaml`。
2. 工具在 PR 中自动运行：发现新页面没有 `lock.yaml`，就取跟踪分支的最新提交写入 `lock.yaml`，提交到这个 PR，再触发校验（见 [05](./05-publish-handoff.md#pr-校验)）。
3. 这一页对应的功能还没上线时，文档工程师给 PR 加标签 `shared-docs: not-launched`，工具把 `current` 重写为 `none`。合并前去掉或加上标签，`lock.yaml` 随之重写。这个标签由 zdoc 维护者在仓库中预先创建。
4. 校验通过后合并。合并后只生成候选结果，正式发布要由文档负责人激活（见 [05b](./05b-cutover-and-ownership.md#切换与激活)）。

- `lock.yaml` 写入后就固定在那个提交上，之后的上游修改由每天的上游更新 PR 处理。要重新取最新提交，删掉 PR 中的 `lock.yaml` 即可。
- Phase 1 导航由飞书节点决定，只能接入在飞书目录中已有节点的页面（见 [05b](./05b-cutover-and-ownership.md#导航phase-1)）。

#### 上游更新

milvus-docs 有新提交时，工具每天自动开 PR，把受影响页面的 `next` 改为新提交；合并后 UAT 显示新版本，Prod 不变。怎样发现变化、PR 中附什么报告、失败时怎样处理，见 [06](./06-upstream-changes.md)。

#### 提升

**提升**是指：把 `lock.yaml` 中 `current` 的 commit 值改成 `next` 的 commit 值，Prod 由此采用 UAT 已在显示的版本。新页面（`current: none`）提升后在 Prod 上线。

运行工作流时选择“提升”，填写若干页的页面标识，或选“全部待提升”（`current` 与 `next` 不同的页）。一次提升只开一个 PR，同一次上线的页面一起审核、一起合并。PR 包含：

- 每页 `lock.yaml` 中的 `current` 改成 `next` 的 commit 值；
- Git 页面中指向旧锚点的链接改为新锚点（见[标题改名与锚点](#标题改名与锚点)）；
- 清理页面配置中只对一个通道生效的规则：删除 `channel: current` 的规则，去掉 `channel: next` 的标记（见 [02](../prd.md#场景-6让内容先只在-uat-显示)）；
- 已下线页面的目录被删除，见下文“下线一页”；
- PR 说明中列出这些页面的 Cloud 内容文件里还剩的手写 `<NextChannel>`，提示“对应的功能也在这次上线时，请在本 PR 中一并去掉”。工具不自动去掉：这些包裹对应的是某个 Cloud 功能的上线时间，与这一页的提升不一定同时发生。

提升在功能上线时进行，也就是现在修改 `Release Channel` 的时机；合并后到达 Prod 的路径与时延见 [05](./05-publish-handoff.md#触发时机)。提升或下线合并后，这一页还开着的上游更新 PR 由下一次运行重建或关闭（见 [06](./06-upstream-changes.md#每页一个滚动更新的-pr)）。

#### 下线一页

运行工作流时选择“下线”，填写一页或几页已激活页面的页面标识；工具生成 PR，把这些页的 `next` 改为 `none`：UAT 上不再显示，Prod 照常。

之后的提升中，按提升的规则 `current` 也会变成 `none`，两边都没有这一页了，所以提升 PR 直接删除这一页的目录，`lock.yaml` 随之删除；PR 说明中提醒“合并后请删除这一页的飞书节点”。之后 Fetch 怎样把它从网站上移除，见 [05b](./05b-cutover-and-ownership.md#下线完成)。

只下线已激活的页面。还没激活的页面，网站上显示的是飞书生成的版本，下线工作流改不到它：不再需要时，用普通 PR 删除页面目录，网站上的版本照现有做法在飞书中处理。

#### 急需上线的修正

Milvus 原文中的错误已在上游修好，Cloud 要让 Prod 马上改正、不等下次发布时：

| 这一页的情况 | 做法 |
|---|---|
| `current` 与 `next` 相同（没有待发布的内容） | ① 手动运行上游更新，指定这一页和修正所在的提交，合并后 UAT 先看到修正；② 单独提升这一页，Prod 跟上 |
| `current` 与 `next` 不同（有还不能上线的内容） | 在页面配置中加一条 `channel: current` 的规则，替换出错的那一段；下次提升时工具自动删掉这条规则（见 [02](../prd.md#场景-6让内容先只在-uat-显示)） |

规则只能对准命名块。出错的一段在 Prod 的版本中不在任何命名块里时，只能等下次发布，或者提前提升整页（未上线的内容会一起进入 Prod），由文档工程师判断。

### 标题改名与锚点

这是提升的配套处理。锚点由标题文字生成，标题改名后锚点随之改变。共享页在过渡期内（`current` 与 `next` 不同），Prod 显示旧标题、UAT 显示新标题，同一个链接无法同时对准两个锚点，因此链接改为新锚点的时机是提升。上游更新 PR 把两个版本的标题逐一配对，识别改名，并按链接所在位置处理：

| 链接所在位置 | 处理 |
|---|---|
| milvus-docs 中的其他页 | 报告提示改名与受影响的链接，由文档工程师判断是否回上游修改 |
| zdoc 中 Git 来源的页面，包括 Cloud 内容文件 | 提升 PR 中由工具自动改为新锚点 |
| 仍在飞书的页面 | 报告列出，由文档工程师在飞书中修改；Phase 1 不拦截提升 |
| 站外链接 | Phase 1 不处理 |

过渡期内，指向旧锚点的链接在 UAT 上落到页面顶部，报告中写明。同一 commit 中互相依赖的页面要一起采用，见 06。

## 出错时

生成时：

| 情况 | 结果 |
|---|---|
| 共享页没有 `lock.yaml`，或字段缺失、格式不对 | 该页生成失败 |
| commit 在 milvus-docs 中不存在，或不在跟踪分支的历史上 | 该页生成失败 |
| 两者都有值时，`current` 不是 `next` 的祖先（Prod 比 UAT 新，或两者不在同一条历史上） | 该页生成失败 |
| `current` 与 `next` 都是 `none` | 该页生成失败；页面已下线时应删除页面目录 |
| Cloud 规则只在 `next` 上失效 | 失败并指出是 `next`；`current` 与 Prod 不受影响 |

发起改 `lock.yaml` 的 PR 时：

| 情况 | 结果 |
|---|---|
| 接入时，原文或页面配置引用的命名块在跟踪分支的最新提交中不存在 | 不写入 `lock.yaml`，PR 校验失败并说明原因 |
| 接入 PR 来自 fork，工具无权提交到这个 PR | 不写入 `lock.yaml`，PR 中提示改从 zdoc 仓库内的分支提交 |
| 下线或提升时填写的页面不存在；下线时这一页还没激活；提升时这一页的 `current` 已与 `next` 相同 | 这一页不进入 PR，运行结果中列出 |

## 例子

<details>
<summary>Delete Entities 接入（Phase 1a）与 OpenAI 的更新和提升（Phase 1b）</summary>

Delete Entities 在 Phase 1a 接入时，文档工程师开 PR 新增 `page.yaml`，工具写入 `lock.yaml`，`current` 与 `next` 都是跟踪分支当时的最新提交，如上面的 `lock.yaml` 示例。生成结果与只读一个版本时逐字相同。

OpenAI 在 Phase 1b 中：

```yaml
# 起始：Prod 与 UAT 读同一个 commit
current: a1…
next:    a1…

# 上游更新 PR 合并后：Milvus 修改了“Before you start”以外的一段
current: a1…
next:    b2…    # 变化的段落成对包进 <NextChannel>；UAT 显示新内容，Prod 不变

# Cloud 功能上线，提升 PR 合并后
current: b2…
next:    b2…    # 两边相同，成对的标记消失
```

假设之后某一页要下线：

| 时间 | 谁触发 | `lock.yaml` | UAT | Prod |
|---|---|---|---|---|
| 平时 | — | `current: b2…`，`next: b2…` | 有 | 有 |
| 决定下线 | 下线 PR | `current: b2…`，`next: none` | 没有 | 有 |
| 版本发布 | 提升 PR | 页面目录删除（相当于两边都是 `none`） | 没有 | 没有 |

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

下线与提升手动发起、整页上线与下线不另设字段的理由见[产品需求](../prd.md#场景-8功能上线时提升)。

**为什么两个版本必须合并进同一页。** zdoc 的 UAT 与 Prod 由同一个 dev commit 构建同一个镜像，部署时才注入通道（`ZDOC_RELEASE_CHANNEL`）。Prod 与 UAT 不能各读一份文件，只能在同一份页面中放两个版本，由 `<NextChannel>` 切换。只给改动的段落打标记做不到这一点：原文中已经只剩新文，Prod 无法保留旧文。

**为什么接入时自动写 `lock.yaml`。** 作者不需要自己查 commit，也不会抄错 SHA；功能是否已上线用 PR 标签表达，审核人在 PR 中一眼可见。工具用 zdoc 自带的 `GITHUB_TOKEN` 提交，与 06 的上游更新 PR 相同；用它推送的提交不会自动触发其他工作流，所以要显式触发校验。

**为什么按页。** zdoc 现在的提升就是按页进行的：整页在多维表格中把 `NEXT` 改为 `CURRENT`，块级去掉标签，没有全站统一发布的动作。全站共用一个 lock 会让不同时间上线的功能被迫一起进入 Prod。每页一份文件，多个上游更新 PR 同时修改不同页面时也不会冲突。

**为什么 `lock.yaml` 不记摘要。** 它只表达决定；实际用到的输入与摘要属于构建结果，记在记录文件中。旧版本内容可以随时按 commit 从 Git 重新读取，比较变化不需要事先存摘要。

**为什么不跟踪 `preview`。** milvus-docs 的 `preview` 分支放未发布功能，相对 `v3.0.x` 多 265 个、少 1424 个提交，已大幅分叉；两边一比较就会产生大面积差异。

**为什么锚点跟随标题。** 这与 zdoc 现在修改飞书标题时的行为一致，标题改名本身是正常的修改。milvus-docs 一年内有 17% 的候选页改过或删过标题，所以不能只给提示，要在提升时处理链接。milvus-docs 的链接检查目前不校验锚点；直接加校验要先修历史断链，Phase 1 不做，列在[待确认事项](../phase-1.md#61-待确认的接口)中。

依据的核验见 [zdoc 代码变体与发布通道核验第 2.1 节](../../research/zdoc-variants-and-channels-audit.md#21-补充核验2026-10-14)；合并规则与测试见[本地原型](../../examples/filtered-search/two-commit/walkthrough.md)。

</details>

## 验收

- **T13**：两个通道各自显示对应版本的生成结果；Cloud 规则在两个版本上都校验；提升后不留通道标记；`<NextChannel>` 包住列表、提示框和代码 Tabs 时渲染正确。
- **T10**：可以从 Git 按 `lock.yaml` 重建。
