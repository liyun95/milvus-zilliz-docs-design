# Zilliz Cloud 中文文档翻译流水线：方案与流程设计

> 本文定义 Zilliz Cloud 中文文档（Guides）如何脱离飞书多维表格与手动维护，逐步迁入 Git 仓库，并通过大模型辅助与人工审校门禁（PR Gate）实现高质量、可持续的日常维护。
> 
> 文档面向 **文档团队**（日常如何审阅、修改及发布中文）与 **zdoc 维护者**（分支契约、CI 工作流及与 Fetch 发布流的对接）。

---

## 1. 现状与改造要求

### 1.1 现状：中文正文在飞书维护，与 Git 英文脱节

目前英文文档正在推进 Milvus × Cloud 共享文档改造（`shared-docs`），代码与文档均在 Git 中规范化演进。但中文 Guides 仍存在明显的维护断层：

- **双轨脱节与维护负担**：中文 Guides 仍维护在独立的飞书知识库与多维表格中，由文档工程师手动对照英文编写或翻译。英文在 Git 中更新后，中文缺乏自动感知机制，导致中文文档长期滞后于英文。
- **机翻缺乏人审，人工润色易被冲掉**：站内现有的日文翻译链路追求全自动推送到发布分支，缺乏人审把关。如果直接用传统机翻更新中文，每次英文稍有改动就会整篇重翻，文档工程师此前手动精修、润色过的中文表述会被彻底覆盖。
- **缺少通道感知（NextChannel）**：Cloud 英文文档通过 `<NextChannel>` 实现了 Prod（当前线上）与 UAT（预览/下一版本）在同一篇 MDX 里的平滑共存。外部机翻工具无法理解通道语义，极易破坏标签闭合或把未发布的特性提前泄露到中文 Prod 站。

### 1.2 改造需要满足的要求

要求分为四条：

1. **Git 原生维护，逐步退役飞书**：中文文档正式迁入 Git，作为 master 分支的权威源，彻底告别在飞书表格中逐篇复制粘贴的手工维护方式。
2. **人审必经（PR Gate）**：大模型翻译仅作为初稿建议，所有中文更新必须通过 GitHub PR 由文档工程师审阅（Approve）后方可合入 master，严禁未经人工把关直接发布。
3. **保留人工成果（语义 3-way 增量）**：英文更新时，大模型只调整发生语义实质变更的段落；已有审校润色过的中文段落必须一字不差地保留，使人工沉淀的术语和表述永久生效。
4. **通道感知与系统解耦**：中文 MDX 严格保持与英文相同的 `<NextChannel>` 结构；新流水线独立轻量，不改动现有的日文/REST 翻译链路，只复用其成熟的语法保护器和校验库。

---

## 2. 方案总览：Git 原生中文、语义 3-way 增量与 PR 把关

共享中文文档不再在飞书单独维护，改为在 zdoc master 维护；英文更新后由工具发起单页滚动 PR，文档工程师在 GitHub 中审核合并。

下图是整体流水线架构：

![中文文档翻译流水线：英文变更触发，大模型 3-way 增量，PR 审核后由 Fetch 发布](../assets/zh-translation-flow.png)

图 1 · 中文文档翻译与发布流水线

图 1 按 ①–④ 的顺序读：

- **① 统一英文输入**。无论是 Milvus 共享页（由 `shared-docs` 组装完成的英文 MDX），还是未来迁入 Git 的 Cloud 独有英文页，流水线均以 master 上最终组装完成的英文 MDX 作为输入，不直接处理未展开的 Milvus 源码。
- **② 定时扫描与 3-way 增量生成**。工作流在每个工作日早晨定时运行（也可手动按需触发），自动聚合当天的英文变更。工具提取上次审校时的基准英文、最新英文和现有中文，调用大模型生成增量草稿，并通过语法保护与确定性门禁。
- **③ 文档工程师在 GitHub PR 中把关**。校验通过后，工具按页面开出（或滚动更新）翻译 PR。文档工程师在 PR 中查看单页变更并进行微调，确认无误后 Approve 合并到 master 的权威目录。
- **④ Fetch 汇流与站点发布**。Fetch 工作流按 `active.json` 读取 master 上的权威中文，编译后写入 dev 分支的 `content/zh-CN/`，随生产部署上线到中文站点（`docs.zilliz.com.cn`）。

---

## 3. 语义 3-way 增量：保留人工校对，只更新实质变化

### 3.1 为什么需要三方语义合并？

传统机翻主要有两种方式，但都无法满足生产要求：
- **全量机翻 (1-way)**：每次英文有轻微改动，整篇重新机翻覆盖。文档工程师之前辛辛苦苦校对的术语和行文风格全部丢失。
- **行级 Diff 增量 (2-way)**：仅根据 Git 的行级差异翻译变动行。由于自然语言的语序、折行和指代关系复杂，机械拼贴极易产生上下文断裂或语病。

**语义 3-way（三方语义合并）** 借鉴自 Git 的合并机制，同时将三份文档输入给大模型：
1. **`base_en`（基准英文）**：上次完成审校合入时的英文版本快照（记录在 `.baseline.json` 中）。
2. **`new_en`（最新英文）**：当前 master 上的最新英文。
3. **`cur_zh`（现有中文）**：当前 master 上已经被文档工程师校对润色过的中文底稿。

![语义 3-way 增量更新：以现有已润色中文为底稿，仅更新语义变动段落](../assets/semantic-3way-merge.png)

图 2 · 语义 3-way 增量更新逻辑

### 3.2 核心更新规则

大模型处理时的核心规则如下：

- **未变动段落**：只要 `base_en` 与 `new_en` 在语义上一致（即便有纯标点或空格微调），**100% 逐字保留 `cur_zh` 的现有内容**，严禁重新机翻。
- **实质变动段落**：仅针对发生功能增删、参数调整或步骤变化的段落进行翻译，翻译时严格沿用 `cur_zh` 中已有的专业术语和句式风格。
- **示例如下**：
  - `base_en`：`You can create up to 5 collections in a free cluster.`
  - `cur_zh`（已人工润色）：`在免费集群中，您最多可以创建 5 个集合。`
  - `new_en`（配额升级）：`You can create up to 10 collections in a free cluster.`
  - **3-way 输出结果**：`在免费集群中，您最多可以创建 10 个集合。`（自然继承“免费集群”与“集合”的中文习惯，而不是机械直翻为“在一个 Free Cluster 里创建多达 10 个 Collection”）。

---

## 4. NextChannel 通道处理：Prod 保持稳定，UAT 增量翻译

Zilliz Cloud 采用同一套静态产物同时服务线上 Prod 和预览 UAT。在 MDX 中使用 `<NextChannel>` 区分版本：
- `<NextChannel variant="exclude">`：当前线上 Prod 包含的内容；
- `<NextChannel variant="include">`：即将随新版本上线的 UAT 内容（Prod 隐藏）。

为了避免未发布的特性提前污染线上，流水线遵循如下规则：

1. **Prod 存量内容免翻译保护**：
   - 英文 MDX 中属于 `variant="exclude"` 的块，直接提取 `cur_zh` 中现有的已发布中文放回，大模型不介入二次重写，确保线上环境绝对稳定。
2. **UAT 增量内容按需翻译**：
   - 英文源中新增的 `variant="include"` 特性块，调用大模型翻译为中文并包入相同的 `include` 标签中。
3. **标签镜像对称检查**：
   - 生成完毕后，工具强制比对中英文文件中 `<NextChannel>` 的块数量与 variant 属性。数量不完全一致时触发硬性阻断，绝不开出损坏的 PR。

---

## 5. 日常审校体验：单页滚动 PR 与定时去抖

### 5.1 为什么采用「单页滚动 PR」？

在日常维护中，极力推荐 **每页一个独立 PR（1 Page = 1 PR）**，理由如下：

- **审阅负担最轻**：每个 PR 仅包含单篇文档的变更，diff 一目了然。文档工程师花 1~2 分钟即可确认并合并。
- **解耦互不阻塞**：如果一批修改了 3 篇文档，其中 2 篇翻译完美，工程师可以立即 Approve 合并上线；剩下 1 篇若有争议可单独讨论，不会因为单篇延误阻碍其他文档发布。
- **滚动更新（Rolling PR）**：分支采用固定的命名规则（`translate/zh-guides-<page-slug>`）。若英文源在 PR 开启期间再次提交更新，流水线会自动在该分支上追加提交，并在 PR 评论中说明，不会生成重复的 PR。
- **真实工作量可控**：统计显示 master 上涉及 shared-docs 的改动平均每天仅 1~2 篇，采用单页 PR 不会导致 PR 列表泛滥。

### 5.2 触发节奏：工作日定时 + 手动按需

- **工作日定时运行（Daily Cron，如北京时间每天 09:30）**：
  - 自动去抖（Debounce）：合并英文作者前一天提交的多次零碎 commits，每天早晨为团队生成一份稳定、聚合的待审阅列表。
- **手动按需触发（Workflow Dispatch）**：
  - 紧急发版或 hotfix 时，文档工程师可在 GitHub Actions 界面手动触发，输入页面 slug，2 分钟内即刻生成最新 PR。

---

## 6. 工程改动与 Workflow 影响分析（面向 zdoc 维护者）

为了让工程团队和 zdoc 维护者清晰评估实施代价，本节明确本次设计对既有系统的影响边界、受影响的 Workflow 以及具体的新增与扩展范围。

### 6.1 现有 GitHub Actions 工作流影响矩阵

| 工作流文件 | 业务用途 | 本次改动影响 | 维护者关注点 |
|---|---|---|---|
| `.github/workflows/translate-codex.yml` | 日文与现有站内翻译调度 | **完全不修改，零影响** | 保持独立运行，日文发布行为完全不受干扰。 |
| `.github/workflows/publish-translation.yml` | 翻译结果自动发布到 dev | **完全不修改，零影响** | 不修改其生产发布队列与分支写入逻辑。 |
| `.github/workflows/sync-master-to-dev.yml` | master 工具向 dev 同步 | **完全不修改，零影响** | 中文源码存放在 `localized-docs/`，属于 master 独占权威路径，不在 `devOwnedPaths` 清单中。 |
| `.github/workflows/fetch-docs.yml`<br/>`_assemble-guides.yml` | 文档正文抓取与组装发布 | **轻微扩展（仅复用 05b 机制）** | 仅扩展链接识别逻辑：当表格记录的链接指向 `localized-docs/` 时，Fetch 改为读取本地 Git 中文源码，跳过飞书正文抓取。核心发布调度与缓存机制不变。 |
| `.github/workflows/translate-zh-guides.yml` ⭐ | **【本次唯一新增】**<br/>中文 Guides 定时翻译与提 PR | **新增独立工作流** | 工作日定时（或手动）在 master 上运行，仅开出或更新 PR。**不直接 push 到 dev 分支，不争抢 `docs-production-dev` 生产并发锁**，零构建冲突风险。 |

### 6.2 仓库具体改动范围清单

整个方案保持极低的代码侵入度，改动清晰集中在三个位置：

1. **【新增】master 权威数据目录**：
   * `localized-docs/zh-CN/guides/<slug>/index.md`：中文权威源码（由文档工程师通过 PR 审校合并）；
   * `localized-docs/zh-CN/guides/<slug>/.baseline.json`：记录上次审校时的英文 commit SHA、时间和 NextChannel 状态。
2. **【新增】轻量 3-way 翻译工具包**：
   * 放在 `packages/docs-tooling/src/translation/guides/` 下，实现 Prompt 组装、大模型 API 调用、NextChannel 块保护和确定性门禁；注册为 `pnpm docs-tooling translate-zh-guides` 命令。
3. **【复用与扩展】既有模块**：
   * **复用** `scripts/translation/protectedContent.js`（占位符保护代码块/链接）与 `validate-translation-file.js`（MDX 语法校验）；
   * **扩展** `packages/docs-tooling/src/lark/guidesBaseRecordSemantics.js`：添加对 `localized-docs` 前缀的识别支持（与 shared-docs 现有逻辑同构）。

---

## 7. 推进节奏与飞书退役路线

方案落地无需过度复杂的细分工作包，在工程上分为 **“原型试点 ➔ 存量建仓 ➔ 逐页切量”** 三大阶段推进：

![中文页面从飞书切换到 Git 的四个阶段](../assets/zh-page-cutover.png)

图 3 · 中文页面从飞书切换到 Git 的四个阶段

### 7.1 三个推进阶段

1. **第一阶段：原型验证与 3 篇试点**
   - 实现核心 3-way 脚本与 CI 工作流；
   - 选取 `delete-entities` 等 3 篇已完成 shared-docs 改造的典型页实测全流程：英文变更 ➔ 自动 PR ➔ 工程师审阅合并 ➔ Fetch 汇流发布 ➔ 线上渲染无误。
2. **第二阶段：存量 89 篇底稿建仓与基线绑定**
   - 编写一次性导出脚本，将飞书现有的 89 篇中文提取到 master 的 `localized-docs/` 目录中，并绑定当前英文 commit 作为初始基线；
   - 按功能分类拆分为 6~8 个批次 PR 集中审校合入 master，完成初始沉淀，避免产生几十个 PR 轰炸仓库。
3. **第三阶段：逐页切换生效（Cutover）与飞书退役**
   - **复用技术设计 05b 机制**：在飞书多维表格中，把页面的 `Docs` 链接逐篇换为 GitHub 目录地址：
     `https://github.com/zilliztech/zdoc/tree/master/localized-docs/zh-CN/guides/<slug>`
   - 换掉链接的页面，Fetch 自动切换为拉取 Git 中文，旧飞书任务失去该页写权；
   - 全部页面切换完毕后，飞书中文编写流程正式退役，日常完全由 Git PR 驱动。

---

## 8. 模型选型与评测建议

为了避免主观臆测，翻译引擎采用标准化测试集进行定量评估：

- **基准测试集**：选取 15 篇覆盖概念说明、复杂步骤、含有 `<NextChannel>` 嵌套以及多语言代码块的典型 Guides 文档。
- **量化评估指标**：
  1. **格式零损坏率（Format Zero-Breakage Rate）**：MDX 解析报错率必须为 0，标签对称率必须达到 100%（硬性门禁）。
  2. **人工编辑距离（PE Ratio）**：人工最终合并的内容相对机器初稿的修改量，评估模型初稿的可用性。
  3. **术语准确率**：关键专业技术词汇的命中一致性。
- **推荐初步选型**：
  - 日常主力推荐 **DeepSeek-V3**（中文表述地道、API 成本与响应速度俱佳）；
  - 对含有复杂双通道嵌套的高难度页面，可配置切换至 **Claude 3.5 Sonnet** 进行对比。
