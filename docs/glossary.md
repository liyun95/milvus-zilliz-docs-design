# 术语

## 页面与配置

- **共享页**：正文引用 milvus-docs 原文、在 zdoc 中只维护差异的 Cloud 页面。每个共享页对应 `shared-docs/pages/` 下的一个目录。
- **页面标识**：共享页目录的名字，等于这一页现有的 slug（见 [02](./design/02-page-config.md#shared-docs-的位置)）。
- **页面配置**：每个共享页目录中的 `page.yaml`，说明引用哪篇原文、发布到哪些手册、做哪些变换（见 [02](./design/02-page-config.md)）。
- **Cloud 内容文件**：一个共享页面中 Cloud 用来新增或替换的内容，与页面配置放在同一目录，由页面配置的 `content.file` 指定。
- **overlay**：zdoc 中只记录 Cloud 差异的一层文件，即 `shared-docs/` 中的页面配置、`Variables.json` 和 Cloud 内容文件。用于[生成流水线](./design/README.md#生成流水线)的图 1。是本次新建的，与 zdoc 现有的 `sidebar-overrides` 或部署仓库的 Kubernetes overlays 无关。
- **共享来源配置**：`shared-docs/source.yaml`，记录读哪个仓库、跟踪哪个分支。**跟踪分支**目前是 milvus-docs 的 `v3.0.x`，只用于发现新提交（见 [04](./design/04-channels-and-lock.md#共享来源配置与跟踪分支)）。
- **链接映射表**：`shared-docs/links.yaml`，登记 Milvus 页面到 Cloud 页面的对应关系（见 [02b](./design/02b-links-and-images.md)）。
- **产品名检查规则**：`shared-docs/product-names.yaml`，列出生成后的 Cloud 页面中不能出现的 Milvus 产品名与连接值，以及放行的短语（见 [07](./design/07-site-adaptation.md#产品名检查)）。

## 原文

- **片段（fragment）**：milvus-docs 中多篇文章共用的一段内容，放在 `site/en/fragments/`，正文用 `{{fragments/xxx.md}}` 引用，由 md2md 展开。本方案只在这个意义上使用“片段”。
- **命名块（block ID）**：原文中用 `doc:block` 注释标出的一段 Markdown 或一个完整代码组，是 Cloud 做差异处理的定位点（见 [01](./design/01-named-blocks.md)）。
- **代码组**：恰好包住一整组示例代码的命名块：多语言时是语言切换栏 `<div class="multipleCode">` 加紧跟其后的全部代码块，或者一个独立的代码块。可以按语言或代码行做变换；其他命名块只能整块变换（见 [01](./prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段)）。
- **命名块清单**：工具扫描各共享页的源文件后得到的命名块列表，包括类型、语言、位置和摘要；每次生成时重新扫描，不提交到仓库。

## 版本与生命周期

- **Prod / UAT**：zdoc 的正式站点与预发布站点。两者由同一个 dev 提交构建，部署时才区分。
- **lock（`lock.yaml`）**：每个共享页一份，放在页面目录中（`shared-docs/pages/<页面标识>/lock.yaml`），记录 Prod 与 UAT 分别采用的 milvus-docs commit（`current` 与 `next`）。由接入、上游更新、提升三类 PR 写入，人不手改（见 [04](./design/04-channels-and-lock.md#lockyaml-怎样变化)）。
- **通道**：Prod 与 UAT 各显示哪个版本。本方案中有三处用到：整页的 front matter `channel`（`next` / `retire-in-next`，Phase 1 由飞书表格的 `Release Channel` 决定，作者不在 zdoc 中写）；变换的可选字段 `channel`（`current` / `next`，规则只对一个版本生效，见 [02](./prd.md#场景-6让内容先只在-uat-显示)）；页面中的 `<NextChannel>` 组件（一段内容只在 UAT 显示）。
- **接入**：文档工程师开 PR 新增页面目录（`page.yaml`，需要时加 Cloud 内容文件），工具在同一个 PR 中写入 `lock.yaml`。接入后只生成候选结果，不改变网站（见 [04](./design/04-channels-and-lock.md#接入一页)）。
- **飞书表格（DocsList）**：zdoc 现有的飞书多维表格，Guides 的每一页一条记录，决定导航、发布目标与整页通道。Phase 1 共享页仍在其中保留记录。
- **placement type**：飞书表格中每条记录的字段，说明这一行在导航中是什么，现有 `canonical`、`section`、`link`、`ref`。Phase 1 新增 `git`，表示这一页由 Git 生成（见 [05b](./design/05b-cutover-and-ownership.md#切换与激活)）。
- **Release Channel**：飞书表格中每条记录的字段，`CURRENT`、`NEXT` 或 `RETIRE-IN-NEXT`，决定整页只在 Prod、只在 UAT 还是两边都显示。Phase 1 共享页的整页通道沿用它。
- **激活**：一页从飞书切换到 Git 生成。文档负责人先运行比较，再在飞书表格中把 placement type 改为 `git`，一页只做一次（见 [05b](./design/05b-cutover-and-ownership.md#切换与激活)）。与提升无关。
- **生效配置**：dev 中的 `active.json`，列出已切换到 Git 的页面；由 Fetch 按飞书表格生成，激活后的第一次 Fetch 加入、下线完成时移除，人不手改（见 [05b](./design/05b-cutover-and-ownership.md#生效配置activejson)）。
- **提升（promotion）**：功能上线时，按页把 lock 中 `current` 的 commit 值改成 `next` 的 commit 值，Prod 由此采用 UAT 已在显示的版本。沿用 zdoc 对上线的叫法。
- **下线**：Phase 1 沿用飞书表格：把这一页的 `Release Channel` 改为 `RETIRE-IN-NEXT`，UAT 先不再显示；发版时删除表格记录与飞书节点，由 Fetch 把它从网站移除；之后用普通 PR 删除页面目录（见 [05b](./design/05b-cutover-and-ownership.md#下线完成)）。

## 发布

- **Fetch**：zdoc 现有的发布工作流，每天定时运行 3 次，也可以手动触发，一次约 1 小时；抓取飞书内容、生成共享页，校验后写入 dev（见 [05](./design/05-publish-handoff.md#交接发生在哪里)）。
- **docs-tooling**：zdoc 中的 `packages/docs-tooling`，是 Fetch 等工作流调用的工具包，入口是 `pnpm docs-tooling`。共享页的生成代码放在其中的 `src/shared-docs/`（见[技术设计 README](./design/README.md#代码位置)）。
- **候选结果（候选运行）**：不写 dev、不上传图片、不需要 Cloud 凭据的生成，用于 PR 校验，以及激活之前的共享页（见 [05](./design/05-publish-handoff.md#pr-校验)）。
- **dev**：zdoc 存放生成结果的分支，由 Fetch 写入；网站从它构建，Prod 与 UAT 用同一个 dev 提交，部署时才区分。人编写的文件在 master，不在 dev。
- **stage**：zdoc 现有发布流程中的内容暂存区，生成结果在这里校验后进入发布。
- **记录文件（receipt）**：每个已切换的共享页在 dev 中的一份记录，说明一次构建用到的输入（按仓库分组）与输出摘要，兼作来源记录；用于追溯、重新生成比对和恢复（见 [05](./design/05-publish-handoff.md#记录文件)）。
- **摘要（hash）**：用 SHA-256 这类标准算法、按文件全部内容算出的一串固定长度的字符，相当于内容的指纹：内容相同摘要就相同，改动一个字节摘要就完全不同。Git 的 commit 号也是这样得来的。本方案用它识别内容是否相同、是否被改过：图片的新地址（见 [02b](./design/02b-links-and-images.md#图片)）、记录文件和恢复（见 [05](./design/05-publish-handoff.md#记录文件)）都用它。
- **manifest**：来源版本、文件及摘要的清单，不能代替实际内容。
- **artifact**：构建产出的实际文件或包。
