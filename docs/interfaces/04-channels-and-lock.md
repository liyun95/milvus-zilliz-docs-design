# 04 通道与 commit 记录

Cloud 要能在 UAT 提前看到上游的修改，同时让 Prod 保持已上线的版本。本篇定义每个共享页怎样记录 Prod 与 UAT 各用 milvus-docs 的哪个 commit（lock），两个版本怎样合并成一份页面，以及怎样提升。场景说明见[方案总览第 4.3 节](../proposal.md#43-何时上线prod-与-uat-各固定一个-commit)。

**参与方**：zdoc 生成（读取 lock、按两个版本生成）、上游更新 PR 与提升 PR（写入 lock）、zdoc 发布（按通道显示）。

**状态**：已定义，待文档负责人确认。

## 约定

### lock

```yaml
# shared-docs/pages/delete-entities/lock.yaml
# 工具生成，不要手改
schema_version: 1
current: 1997ce96782b31f8628f22d31fad11007e4b924b   # Prod 读取
next: 1997ce96782b31f8628f22d31fad11007e4b924b      # UAT 读取
```

| 字段 | 说明 |
|---|---|
| `schema_version` | lock 格式版本 |
| `current` | Prod 使用的 milvus-docs commit，完整 SHA；写 `none` 表示 Prod 上没有这一页 |
| `next` | UAT 使用的 milvus-docs commit，完整 SHA；写 `none` 表示 UAT 上没有这一页 |

- lock 不记页面标识：所在的页面目录已经说明属于哪一页。
- 仓库地址与跟踪分支记在共享来源配置中（见 [01](./01-named-blocks.md#共享来源配置)），不在每页重复。
- lock 只记“采用哪个版本”，不记文件摘要。一次构建实际用到的输入及其摘要记在记录文件中（见 [05](./05-publish-handoff.md#记录文件)）。

### 整页上线与下线

| lock | 含义 | 生成结果 |
|---|---|---|
| `current: none`，`next` 有值 | 新页面，功能还没上线：UAT 显示，Prod 没有这一页 | 带 zdoc 现有的整页标记 `channel: next` |
| `current` 有值，`next: none` | 要下线的页面：Prod 照常显示，UAT 上已没有 | 带 `channel: retire-in-next` |

Prod 上的隐藏，以及从导航、搜索、`llms.txt` 中去掉，都沿用 zdoc 现有的整页通道实现。这两种情况替代飞书多维表格中的 `Release Channel`。

### 写入与提升

| 写入方 | 改什么 | 何时 |
|---|---|---|
| 接入一页 | `current` 与 `next` 都设为内容对齐后的 commit；功能还没上线时 `current` 写 `none` | 1a；两者相同时，生成结果不含 `<NextChannel>` |
| 下线一页 | 把 `next` 改为 `none` | 按需 |
| 上游更新 PR | 只改 `next` | 1b，见 [06](./06-upstream-changes.md) |
| 提升 PR | 把 `current` 改为 `next` 的值。新页面提升后上线；下线页面提升后两边都没有，页面删除 | 1b |

- **提升由 Cloud 文档工程师在功能上线时发起**，也就是现在修改 `Release Channel` 的时机。工具生成提升 PR，可以指定若干页，也可以选所有 `current` 与 `next` 不同的页。合并后到达 Prod 的路径与时延见 05。
- **跟踪分支是 milvus-docs 的默认分支**，目前为 `v3.0.x`，记在共享来源配置中，只用于发现新提交；正式生成始终使用 lock 中的 commit。Milvus 发布新的大版本分支时，用一个显式的 PR 切换。只写在 `preview` 分支中的内容，合入 `v3.0.x` 后 Cloud 才能读到；Cloud 先于 Milvus 上线的功能写在 Cloud 内容文件中，用 `<NextChannel>` 包住。

### 两个版本怎样合并

每个版本各自经过 [01](./01-named-blocks.md)–[03](./03-md2md-preprocess.md) 的处理，Cloud 规则在两边都必须成立，失败时指出是哪个通道。然后按以下规则合并：

- 结果按顶层块比较：标题、段落、整个列表、表格、提示框各算一块，代码组整体算一块。相同的块只输出一次；连续的不同块输出成 `exclude`（旧）与 `include`（新）一对；只在一侧存在的块只输出那一侧。
- 两个版本相同时，输出不带通道标记，与单版本生成的结果逐字相同。提升之后即是这种状态。
- front matter 无法按通道区分，两版不同时沿用 `current`，并写入记录文件的备注。
- Cloud 内容文件中手写的 `<NextChannel>` 若落在成对的区域内，生成失败，避免嵌套。
- 共享原文不写通道标记，也不为通道加命名块。作者在哪些地方手写 `<NextChannel>`，见[共享页面的写法与配置第 3.9 节](../consumption-schema.md#39-让内容只在-next-显示)。
- **急需上线的修正**：这一页的 `current` 与 `next` 原本相同时，直接把 `current` 更新到新 commit；两者已有差异时，直接更新会把未上线的内容一起带进 Prod，可改为在 zdoc 中用一条临时规则修正，发布后删除；或者把 `current` 一并更新，再用命名块把尚未上线的一段包进 `<NextChannel>`。

仍需在 zdoc 中核实：`<NextChannel>` 包住列表、提示框和代码 Tabs 时的渲染，以及目录是否过滤其中的标题。

### 标题改名与锚点

锚点由标题文字生成，标题改名后锚点随之改变。共享页在过渡期内（`current` 与 `next` 不同），Prod 显示旧标题、UAT 显示新标题，同一个链接无法同时对准两个锚点，因此链接改为新锚点的时机是提升。上游更新 PR 把两个版本的标题逐一配对，识别改名，并按链接所在位置处理：

| 链接所在位置 | 处理 |
|---|---|
| milvus-docs 中的其他页 | 报告提示改名与受影响的链接，由作者判断是否回上游修改 |
| zdoc 中 Git 来源的页面，包括 Cloud 内容文件 | 提升 PR 中由工具自动改为新锚点 |
| 仍在飞书的页面 | 报告列出，由文档工程师在飞书中修改；首期不拦截提升 |
| 站外链接 | 首期不处理 |

过渡期内，指向旧锚点的链接在 UAT 上落到页面顶部，报告中写明。同一 commit 中互相依赖的页面要一起采用，见 06。

## 出错时

| 情况 | 结果 |
|---|---|
| 共享页没有 lock，或字段缺失、格式不对 | 该页生成失败 |
| commit 在 milvus-docs 中不存在，或不在跟踪分支的历史上 | 该页生成失败 |
| 两者都有值时，`current` 不是 `next` 的祖先（Prod 比 UAT 新，或两者不在同一条历史上） | 该页生成失败 |
| `current` 与 `next` 都是 `none` | 该页生成失败；页面已下线时应删除页面目录 |
| Cloud 规则只在 `next` 上失效 | 失败并指出是 `next`；`current` 与 Prod 不受影响 |

## 例子

<details>
<summary>Delete Entities 接入（1a）与 OpenAI 的更新和提升（1b）</summary>

Delete Entities 在 1a 接入时，`current` 与 `next` 都是内容对齐后的 commit，如上面的 lock 示例。生成结果与只读一个版本时逐字相同。

OpenAI 在 1b 中：

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

</details>

## 设计理由

**为什么两个版本必须合并进同一页。** zdoc 的 UAT 与 Prod 由同一个 dev commit 构建同一个镜像，部署时才注入通道（`ZDOC_RELEASE_CHANNEL`）。Prod 与 UAT 不能各读一份文件，只能在同一份页面中放两个版本，由 `<NextChannel>` 切换。只给改动的段落打标记做不到这一点：原文中已经只剩新文，Prod 无法保留旧文。

**为什么按页。** zdoc 现在的提升就是按页进行的：整页在多维表格中把 `NEXT` 改为 `CURRENT`，块级去掉标签，没有全站统一发布的动作。全站共用一个 lock 会让不同时间上线的功能被迫一起进入 Prod。每页一份文件，多个上游更新 PR 同时修改不同页面时也不会冲突。

**为什么 lock 不记摘要。** lock 只表达决定；实际用到的输入与摘要属于构建结果，记在记录文件中。旧版本内容可以随时按 commit 从 Git 重新读取，比较变化不需要事先存摘要。

**为什么整页上线、下线不另设字段。** “UAT 读 `next`、Prod 读 `current`”这一条规则就能覆盖“这一页在某个通道中不存在”的情况，作者不用另学一个字段，提升也仍是同一个动作。

**为什么不跟踪 `preview`。** milvus-docs 的 `preview` 分支放未发布功能，相对 `v3.0.x` 多 265 个、少 1424 个提交，已大幅分叉；两边一比较就会产生大面积差异。

**为什么锚点跟随标题。** 这与 zdoc 现在修改飞书标题时的行为一致，标题改名本身是正常的修改。milvus-docs 一年内有 17% 的候选页改过或删过标题，所以不能只给提示，要在提升时处理链接。milvus-docs 的链接检查目前不校验锚点；直接加校验要先修历史断链，首期不做，列在[待确认事项](../phase-1.md#61-待确认的接口)中。

依据的核验见 [zdoc 代码变体与发布通道核验第 2.1 节](../../research/zdoc-variants-and-channels-audit.md#21-补充核验2026-10-14)；合并规则与测试见[本地原型](../../examples/filtered-search/two-commit/walkthrough.md)。

## 验收

- **T13**：两个通道各自显示对应版本的生成结果；Cloud 规则在两个版本上都校验；提升后不留通道标记；`<NextChannel>` 包住列表、提示框和代码 Tabs 时渲染正确。
- **T10**：可以从 Git 按 lock 重建。
