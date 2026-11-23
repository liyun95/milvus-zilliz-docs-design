# Zilliz Cloud 中文 Guides 改造方案

**草案 · 待文档团队评审**

## 1. 背景、目标与首期范围

目前，Cloud 采用新的英文 Guide 后，文档工程师需要自己发现变化、找到对应的飞书中文稿，再逐段核对。交接时，下一位编辑很难判断中文上次审到哪版英文，也很难分辨哪些差异是欠译，哪些是为中文读者有意保留的写法。

![现状工作流。Cloud 生成英文页后，文档工程师人工跟进飞书中文，Fetch 取稿，中文站随部署更新。](./assets/zh-guides-current-workflow.png)

**改造目标**是让每次需要跟进的英文变化都能找到负责的中文审校人，让人工审过的译文可以持续修订，并让团队能按页确认哪份稿件已经上线。拟将中文正文逐页从飞书迁入 Git，由模型起草局部修改，文档工程师在 GitHub 审校并决定是否合入。未经批准的草稿不能进入发布流程。

**首期范围**为已有飞书中文底稿、能对应到已生成 Cloud 英文的 Guides 正文。先从 `shared-docs/guides/pages/` 已注册的共享页中选择试点。Guides 首页、工具教程（`tutorials/tools/`）、Reference 和日文沿用现行流程。Cloud 独有页可在具备可核对版本的英文文件后接入。过渡期飞书继续管理导航。

## 2. 目标工作流与分工

共享英文原文在 `milvus-docs` 维护。Cloud 团队在 zdoc 的 `shared-docs` 中选择采用的上游版本，配置目标手册，按需补写 Cloud 专用英文片段。**翻译依据是这些输入最终生成的、对应手册和版本的 Cloud 英文文件。** 同一共享页若同时生成 Guides 和 BYOC，中文 Guides 应明确绑定 Guides 的英文输出。

![首次导入：Fetch 读取飞书中文，文档工程师对照英文审导入 PR，形成 Git 底稿。后续更新：根据 Cloud 英文变化起草中文，工程师审更新 PR，随对应版本部署上线。](./assets/zh-guides-source-map.png)

图中第一步复用现有 `fetch lark docs` 工作流，按中文飞书记录的 `Docs` 链接取稿。将中文和来源修订整理成导入 PR 是本次拟新增的步骤。首份底稿合入后，等 Fetch 确认该页已从 Git 取稿，才把日常编辑入口切到 Git。[现有 Fetch 的中文 Guides 任务](https://github.com/zilliztech/zdoc/blob/75e79b0205ce7f9f7b842f163472e64eada35e71/.github/workflows/fetch-docs.yml#L348-L359)

| 角色 | 负责的决定 | 工作完成的标志 |
|---|---|---|
| 文档工程师 | 对齐首次导入的中英文，审校后续改稿，决定采纳、修改或暂缓 | 获批合入的中文能追溯到该页审过的英文版本 |
| 文档负责人 | 选择试点、确认页面对应关系、安排单页停改和交接 | 迁移清单标明该页负责人及当前编辑入口，原网址和旧链接通过验收 |
| 发布负责人 | 确认待发中文是否与已验收的预览一致，决定是否随功能上线 | 能指出正式站采用了哪份中文，以及哪些页面仍在等待审校 |

对已切换的页面，文档团队在 zdoc 的 `master` 分支维护 `localized-docs/zh-CN/guides/<中文页面 ID>/index.md`。**每个 `index.md` 都是一篇完整的中文正文**，包含标题、步骤、示例和链接。只修中文也可以直接给这个文件提 PR。切换后，方案要求 Fetch 从该 Git 目录读取已审正文，写入 `dev` 分支的 `content/zh-CN/`，供中文站部署。

<details>
<summary>目录选择依据：中文编辑源和日文发布目录</summary>

日文随英文站构建，`i18n/ja-JP/` 存放日文翻译流水线的产物。中文有独立站点，从 `content/zh-CN/` 构建。这两处发布内容均由 `dev` 管理。方案拟在 `master` 新增 `localized-docs/`，供文档团队通过 PR 维护中文正文。[站点与目录分工](https://github.com/zilliztech/zdoc/blob/1ceb4eb30e49c105634d313ee374b491b0eb3007/README.md#L169-L188) · [分支所有权契约](https://github.com/zilliztech/zdoc/blob/1ceb4eb30e49c105634d313ee374b491b0eb3007/deploy/contracts/master-tooling-sync.json)

</details>

## 3. 首期产品要求

### 3.1 接入一页并交接编辑权

1. **确认对应关系。** 文档负责人登记英文共享页 ID、目标手册和英文文件、中文飞书记录、中文页面 ID 与主审。中文 ID 用作固定目录名，页面改标题或网址时仍沿用。若一条记录供多本手册使用，先核对所有目标。缺中文的页面列为待评估首译；缺英文或存在拆页、合页的，维持原有维护方式，等待确认。
2. **建立第一份已审底稿。** 首次建仓拟使用 Fetch 取得的中文材料，不发布候选稿。导入 PR 须能追溯飞书修订，主审逐段核对该稿与固定版本的 Cloud 英文。已确认的部分记下对应英文，历史欠译另列待办，中文独有的说明由主审确认保留。导入 PR 合入后，正文仍在飞书维护。
3. **逐页切换。** 文档负责人暂停该页编辑，核对并补齐导出后的飞书修改，再将原飞书记录的 `Docs` 链接指向 Git 目录。**只有 Fetch 确认已采用 Git，才将清单上的编辑入口改为 Git。** 部署后用原网址检查正文、图片和段落链接，验收通过后标记旧稿。

![逐页交接。导入候选稿时仍在飞书编辑；短暂停改并换链接后等待 Fetch 确认，然后更新编辑入口，验收原网址。](./assets/zh-page-cutover.png)

切换结果未知时，保持该页停改，核实发布记录。确认尚未接管可撤回请求并恢复飞书编辑。Git 已接管后发生部署故障，按现有流程恢复站点，编辑入口仍为 Git。

### 3.2 跟进英文更新并保留人工修订

拟在工作日北京时间 09:30 汇总 Cloud 已采用的英文变化，补上周末或上次遗漏的更新。一般每页一个滚动 PR，急修可按页提前发起。

- **审什么。** PR 展示上次已审英文、本次英文、建议修改的中文和页面预览。模型只起草受影响的段落，未受影响的中文逐字保留。数字、限制、命令和链接变化须明确列出，段落或指代无法对应时交给主审。
- **英文又变时怎么办。** 在同一 PR 追加变化，保留审阅中的人工修订。改动重叠时暂停自动更新，由主审处理。最终稿变化须重新批准。
- **何时算审完。** 只有文档工程师批准且 PR 合入后，才推进该页已审英文版本。暂缓或关闭 PR 的更新仍可追踪；只改中文措辞时沿用原英文版本。

### 3.3 确认读者何时看到新稿

| 发版情形 | 预期结果 |
|---|---|
| 修订已上线功能 | Fetch 取到已审稿，正式站（Prod）部署成功后可见。同页有待发功能时，允许单独修正当前线上说明。 |
| 新说明随下个版本上线 | 文档工程师先在预发布站（UAT）验收。发版时，发布负责人确认拟发布英文仍与已审中文相符，将验收稿提升为当前版（Promote），部署成功后在 Prod 可见。 |
| 英文在验收后又变，或中文仍待审批 | 保留上一份可用中文。只有预览稿的新页在 Prod 继续隐藏；要求双语同步发布的页面等两边均就绪。 |

公开 PR 和预览只接收可提前公开的内容。保密材料继续在受限渠道协作。

## 4. 试点验收与待决事项

| 试点场景 | 通过条件 |
|---|---|
| 普通更新页 | 英文在审校期间再次变化时，主审能在原 PR 看见累计差异，先前的人工润色仍在。记录完成一次审校的用时。 |
| 同时有待发功能和线上急修的页面 | Prod 能单独修正旧说明。Promote 后 Prod 展示 UAT 已验收的版本；验收后英文变化时能指出暂缓原因。 |
| 有飞书历史链接和图片的页面 | 切换失败时原网址仍可访问；确认切换后，原链接、锚点和图片可用，旧飞书正文的修改不会覆盖网站。 |

**评审会上要确认**首批三页及主审和备份、单页停改窗口，以及哪些页面须双语同步发布。另有一项命名建议待确认：中英文一一对应且名称可用时，中文 ID 默认沿用英文共享页 ID；发生重名或已有稳定中文 ID 时保留唯一中文 ID，登记对应关系。

试点通过后，再将约 89 篇存量 Guides 分 6～8 批审校入库。每一页按自己的验收结果切换。

## 5. 示例：Delete Entities 从接入到上线

下面的英文配置和中英文文件可在仓库核对。中文 ID、切换和后续发版均为演示情境。

1. **选对英文。** 共享页 `delete-entities` 有一份 Milvus 原稿，Cloud 配置将它生成到 Guides 和 BYOC 两本手册。负责中文 Guides 的主审打开该次生成的 `content/en/guides/tutorials/development/insert-and-delete/delete-entities.md`。[共享原稿](https://github.com/milvus-io/milvus-docs/blob/3e6b7499cbfcb6b5a365fb1f084a74836f625fc2/site/en/userGuide/insert-and-delete/delete-entities.md) · [Cloud 页面配置](https://github.com/zilliztech/zdoc/blob/7ee39054f37047b586ad789d876b2047c6f2c465/shared-docs/guides/pages/delete-entities/page.yaml) · [两本手册的输出记录](https://github.com/zilliztech/zdoc/blob/5a62906a45a4e3250c619a5efcfa4de3f83a8eb6/generated/en/manifests/shared-pages/guides/delete-entities.json)
2. **审第一份中文。** 同一提交的《删除 Entity》中，按条件删除的示例用 `red` 和 `green`，英文用 `red_7025` 和 `purple_4976`。主审对照最新飞书稿和两边的示例代码，决定是否跟进。若确认中文 ID 为 `delete-entities`，整篇底稿放入 `localized-docs/zh-CN/guides/delete-entities/index.md`，经导入 PR 审校。[核对英文示例](https://github.com/zilliztech/zdoc/blob/5a62906a45a4e3250c619a5efcfa4de3f83a8eb6/content/en/guides/tutorials/development/insert-and-delete/delete-entities.md) · [核对同一提交的中文](https://github.com/zilliztech/zdoc/blob/5a62906a45a4e3250c619a5efcfa4de3f83a8eb6/content/zh-CN/guides/tutorials/development/insert-and-delete/delete-entities.md)
3. **切换正文。** 文档负责人复核停改前最后一次飞书修订，换链接并等待 Fetch 确认。清单的编辑入口切到 Git 后，部署验收仍从原网址 `/delete-entities` 打开“按条件删除”一节，检查原有段落链接。
4. **审后续更新。** 假设周一 Cloud 采用了一条新的删除限制，主审在中文 PR 中润色了译文；周二英文又改了示例。主审在原 PR 核对新增示例和周一的措辞，处理重叠修改，批准最终稿。
5. **随功能上线。** 假设这条限制适用于下一个版本，主审先在 UAT 核对《删除 Entity》，Prod 继续显示原操作。发布负责人在功能上线时核对版本、执行 Promote，待 Prod 部署成功后，从原网址确认新限制已可见。

[共享文档改造方案](./proposal.md) · [Phase 1 产品需求](./prd.md) · [中文 Guides 技术设计与验收契约](./design/11-zh-cn-translation-pipeline.md)
