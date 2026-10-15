# Milvus md2md 与 zdoc 构建能力复用审计

日期：2026-10-11。目的：核验共享文档方案可复用的工程能力。结论基于固定源码、调用入口及相关测试；没有触发 Fetch、翻译、构建或部署 workflow。共享正文以 milvus-docs 为单一源，产品差异由 zdoc 管理。

本审计形成时曾用 OpenAI 读取样本核验部分内容和恢复路径；这些历史事实按固定修订保留。当前验证样例是 Filtered Search 与 Delete Entities，不能把历史样本的内容覆盖等同于当前样例验收。

## 1. 审计基线与证据边界

| 仓库 | 核对分支 | 固定修订 |
|---|---|---|
| milvus-io/milvus-docs | v3.0.x | `7d87b0bf26d7cbc713f40af6453ea2f925367901` |
| zilliztech/md2md | master | `635da07276e80fb2a6efdf667686df3913d5de4c` |
| zilliztech/zdoc | master | `3777ec0b322546d716485e8f88da8412b0265e71` |

zdoc master 是本次源码能力审计的固定基线。另观察到 dev tip 为 `96d7a73cc0ae9f3882269000eae2ac750e418386`；未将其内容与 master 全量比较，不能据此断言所有 master 能力已经投入生产。仓库运行配置、翻译开关、Jenkins 配置和线上部署修订未核验。机器可读基线见 [manifest.json](./evidence/build-audit/manifest.json)。

## 2. 应保留的现有主干

Milvus：`site` 原始 Markdown → 现有 `goover`（fragment 展开、变量替换及插件）→ 转换后 Markdown 推送到 web-content → 后续既有发布。变量和 fragment 应从 goover 之前的原始 Git 输入消费。源仓库的 [ci.yml](https://github.com/milvus-io/milvus-docs/blob/7d87b0bf26d7cbc713f40af6453ea2f925367901/.github/workflows/ci.yml) 可以确认这一转换和推送顺序；本次不重新审计 web-content 与 milvus.io 后续发布实现。

zdoc Guides：Fetch 获取飞书源与媒体 → 分表渲染 → Guides 组装 → docs-tooling stage 校验/安装 → 带摘要的 checkpoint artifact → 串行发布到 dev → 可触发 Translation → 站点构建/发布。`publish-group --stage publish` 的本地发布边界和 workflow 的 Git dev 发布事务不是同一动作。接入共享内容应进入现有生产链路，不能另起脚本直接覆盖生产分支。[Fetch workflow](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/.github/workflows/fetch-docs.yml)、[Guides assembly](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/.github/workflows/_assemble-guides.yml)。

## 3. md2md：可以直接沿用什么

| 需求 | 现有能力 | 方案处理 |
|---|---|---|
| 产品名称变量 | `Variables.json`、`{{var.key}}`，支持嵌套键、目录配置和页面变量 | 沿用语法；新增 `product_name`；Cloud 适配器给出有效绑定 |
| 文件片段引用 | `{{fragments/path.md}}`；先展开片段，再绑定变量；支持片段内继续引用 | 沿用引用语法和展开能力；命名块提取成只读文件后交给它处理 |
| 基于 JSON 的模板生成 | `useTemplate`、`path`、`var` | 普通共享页面不需要启用模板生成模式 |
| 扩展转换 | `register(mark, fn)`、`markdownToString`，串联自定义处理函数 | 可承接清理命名标记等后处理；提取命名块仍须在变量展开前独立处理 |
| 图片标记、术语、页面标签导航 | `ImageDestination`、`Glossary`、`Tab` 插件 | Milvus 原链保留；不要把其 HTML 直接当作 Cloud MDX 组件 |

证据：[变量、fragment 与模板实现](https://github.com/zilliztech/md2md/blob/635da07276e80fb2a6efdf667686df3913d5de4c/src/helpers/File.js)、[扩展注册与执行顺序](https://github.com/zilliztech/md2md/blob/635da07276e80fb2a6efdf667686df3913d5de4c/index.js)、[默认插件](https://github.com/zilliztech/md2md/blob/635da07276e80fb2a6efdf667686df3913d5de4c/src/plugin/index.js)。

**片段引用沿用 md2md 语法。** `embedding-workflow#index` 由 registry 提取为 `fragments/embedding-workflow/index.md`，Cloud 写：

```markdown
{{fragments/embedding-workflow/index.md}}
```

路径按模块 ID 与 block ID 确定性生成，是制品地址，不是选择器，也不是第二份人工编辑正文。四个后续步骤沿用同样规则。registry 负责输出 manifest 关联“fragment 路径 → 源文件/commit/block ID/hash”。

复用需要补充的边界：

- md2md 只会读片段文件，不会从一篇 Markdown 按命名区域抽块；提取器仍新增。
- 现有 `_replaceFragment` 循环展开未显示循环引用和路径白名单校验；调用前应验证整个允许引用图、文件归属与路径，不能把原循环当完整 registry。
- 变量缺失会得到空替换，不能仅靠渲染后查未解析 token；必须事先查定义。
- 目录/front matter 会改变变量作用域。片段按消费页作用域绑定；registry 必须记录原作用域依赖，由 Cloud 显式决定哪些值继承。不要将所有 Milvus 版本值无条件传播给 Cloud。
- 自定义插件在片段与变量处理之后运行，因此不能把原始源提取放在普通后处理插件中。
- 源码里的 watcher 对 fragment/variable 文件变化的关联重建留有 TODO；首期使用受控完整构建，不把它当作已有完整反向依赖图。
- 当前 Milvus CI 未固定安装的 npm 包版本。本次读到的是 Git 源码，不是生产 npm 安装记录；接入时需固定版本并做一致性验证。

### 3.1 实测补充（2026-10-14）

为定义预处理入口（[接口设计 03《md2md 预处理》](../docs/interfaces/03-md2md-preprocess.md)），在 md2md [`635da07`](https://github.com/zilliztech/md2md/tree/635da07276e80fb2a6efdf667686df3913d5de4c) 上用小样例实际运行了 `goover`，并统计了 milvus-docs `v3.0.x`（[`1997ce9`](https://github.com/milvus-io/milvus-docs/tree/1997ce96782b31f8628f22d31fad11007e4b924b)）`site/en` 的实际用法。

| 原有行为 | 实测 | 新入口的处理 |
|---|---|---|
| 根目录取自 `PATH_ROOT` 或 cwd，配置和插件在加载时读入，规则存放在模块级状态中 | 读代码确认 | 不依赖这些状态，调用之间互不影响 |
| 变量从根目录逐级合并各层 `Variables.json`，再合并页面 front matter | front matter 的值遇到冒号被截断：`title: Connect: quick start` 读成 `Connect` | 不查找变量，由调用方传入 |
| 缺失的变量 | 替换为空串，`token="{{var.example_token}}"` 变成 `token=""`，没有报错 | 报错 |
| 片段路径带 `..` | `{{fragments/../outside.md}}` 读出了片段目录之外的文件 | 报错 |
| 片段循环引用 | 运行 10 秒仍未结束，被强制终止 | 报错 |
| 代码中的 `{{ doc.content }}` | 原样保留 | 保持 |

milvus-docs 的实际用法：

| 项目 | 结果 |
|---|---|
| 变量文件 | 只有 `site/en/Variables.json` |
| `{{var.*}}` | 29 页共 97 处，19 个变量名，全部在 `site/en/Variables.json` 中；仅未被引用的 `fragments/tail.md` 用了不存在的 `auth.*` |
| front matter 变量 | 0 处 |
| `{{fragments/*}}` | 34 页共 39 处，9 个片段；片段中不再引用片段，路径不含 `..` |
| 站点插件标记 | `{{tab}}` 11 页（安装与升级页，不在共享范围内）；术语与图片标记 0 处 |
| 三个试点页 | 当前没有变量或片段，变量在内容对齐时加入 |

milvus-docs 的 `ci.yml`、`pre.yml`、`preview.yml` 都以 `npm install @zilliz/mdtomd -g` 安装未固定版本的 md2md。

## 4. zdoc：已有平台能力及其限制

| 能力 | 已核对实现 | 复用与新增边界 |
|---|---|---|
| 手册与站点注册 | `manuals/registry.ts`、`schema.ts`；源类型包括 wiki/drive/onePager/rest/local | 沿用手册、站点、输出目录、sidebar 与 ownership。共享模块是其下的内容来源清单，不另建整站 registry；页级混合 Git/Lark 来源仍需扩展 |
| 本地 Markdown 输入 | `cli.ts` 的 `copyLocalSource` 和 local 分支 | 已有安全目录复制和 stage 接入；local 本身没有 Git 锁定、块替换、Git 来源证明，更不意味着 Guides 已支持任意混源 |
| 飞书同步块 | `larkDocScraper.js` 展开 reference_synced，writer 渲染 source_synced 子块 | 过渡期飞书内容继续复用；迁移完成后退出生产链，不能把飞书 block 身份当作 Git block 身份 |
| 产品条件与代码行过滤 | `codeVariantFilter.js`、writer 的 prose include/exclude | 可保留现有 Cloud/飞书变体；不替代外部 replacement，不要求把 Cloud 条件写回 Milvus |
| 多语言代码、提示、表格、图片 | LarkDocWriter 生成 Tabs/TabItem/Admonition；媒体缓存与 offline resolver | 复用目标组件、媒体处理和校验；输入是飞书 JSON，不能直接拿它解析 Milvus Markdown |
| 发布适配器 | `packages/publication-adapters` 有 transformDocument / validatePublication | 可以扩展现有接口；当前 CLI 有 zh-CN 限制，英文侧不是登记一个名字即可启用 |
| 导航调整 | `config/applyOverrides.js` 修改 sidebar | 继续用于导航；不是正文 replacement 引擎 |
| 来源与变化追踪 | Lark snapshot、revision inventory；Guides assembly 的内容图/导航/生成器指纹 | 复用摘要与审计模式。schema 强依赖 doc_token/Base/revision，需加 Git 来源契约，不能伪造飞书 token |
| stage、artifact、发布 | atomicReplace、checkpoint 文件 hash/删除清单、ownership gate、生产队列、恢复工具 | 沿用框架；共享 package/lock/provenance 要纳入可验证输入、归属及恢复范围，不新建第二套发布系统 |
| 文件级来源替换证据 | checkpoint 的 authoritativeReplacements 字段 | 是文件生命周期替换元数据，不是“按 block ID 替换正文” |
| 检查与构建 | MDX validate、完整性/链接检查、site profiles、Docusaurus 构建 | 沿用；补充命名结构、替换语法、源依赖有效性检查 |

上述判断来源于实际入口和 schema，而非仅阅读 README：

- [manual source schema](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/manuals/schema.ts)、[Guides 与 BYOC 的现有绑定](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/manuals/registry.ts)、[CLI 的 local/source/adapter 分支](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/cli.ts)。
- [代码变体规范](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/lark/CODE_VARIANTS.md)、[过滤实现](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/lark/codeVariantFilter.js)、[Lark 源抓取](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/lark/larkDocScraper.js)。
- [Lark MDX writer](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/lark/larkDocWriter.js)、[publication adapter 接口](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/publication-adapters/src/types.ts)。
- [来源 snapshot](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/lark/sourceSnapshot.js)、[Guides 组装指纹](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/scripts/docs-workflow/guides-assembly-identity.js)、[checkpoint 生成](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/scripts/docs-workflow/create-checkpoint-artifact.js)。

还核对了两个容易误用的工具：`renderMarkdownHtml.js` 是 Markdown→HTML，不是 Milvus Markdown→Cloud MDX；`larkUtils.js` 有 Tabs→Milvus multipleCode 的处理，方向相反，不能当作已存在的逆转换。[Markdown renderer](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/markdown/renderMarkdownHtml.js)、[LarkUtils](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/lark/larkUtils.js)。

## 5. 翻译：先沿用现有页面输入，避免重建体系

已有的不是简单“全文调用模型”：

1. `translation/candidates.ts` 比较 sourceHash、目标是否存在及既有状态，选择 current_delta / missing_target / stale_source。
2. `semanticUnits.js` 从 MDX 抽取正文、表格等单元；`protectedContent.js` 保护技术内容；locale contract 与样式规范已有管理位置。
3. `semanticSeeds.js` 可从同页历史源和已发布目标对齐未变化单元，再交给 runner。workflow 已接线，但 `semantic_seeds` 默认 false，需要输入或仓库变量打开；本次未确认线上开关。
4. 批次、checkpoint、reconciliation、发布与恢复已有脚本和工作流。

证据：[候选选择](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/packages/docs-tooling/src/translation/candidates.ts)、[语义单元](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/scripts/translation/semanticUnits.js)、[增量 seed 实现](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/scripts/translation/semanticSeeds.js)、[工作流开关](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/.github/workflows/_translate-content-group.yml)。

**首期接法：** 先完成共享组装、Cloud 替换、产品变量绑定、链接与 MDX 适配，生成稳定路径的 Cloud 英文页及 provenance；再交给现有翻译 candidate/runner/publication。不要在 Milvus 原始 HTML 格式上另建翻译链。现有语义单元身份用于翻译，不要求作者逐段命名；本方案 block ID 只承担共享复用契约，两者不应强行合并。

跨 Milvus/Cloud 的共同译文库不是现有 semantic seeds 已有的保证。`tm-retrieve.js` 是离线 EN/JA 近邻检索，README 明确尚未被 workflow 调用。首期不把跨产品译文缓存列为前置条件；后续可在现有翻译系统扩展带产品、上下文和有效文本身份的复用。产品名不同也会改变译文有效输入。

zh-CN 是独立产品站点，不等于英文 Guides 的普通翻译 locale；英文站构建包含 ja-JP。首期 User Guide 接入以英文与现有日文链为范围，中文产品内容需要单独适用性判断。英语源 checkpoint 成功不等于英文/日文站点已成功发布，不能承诺按语言独立上线。[站点与翻译说明](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/README.md)。

## 6. 真正新增的最小范围

| 新增/扩展项 | 原因 | 复用基础 |
|---|---|---|
| 命名区域提取、结构校验与稳定身份 | md2md 只有文件 include；zdoc 没有本例 Git 命名块消费接口 | Markdown 解析基础、现有结构测试经验 |
| 共享 Git source provider 与内容包 | Lark token/revision 不等于 Git commit/path/block | manual registry、stage、摘要和 artifact 框架 |
| zdoc 外部块替换 | 条件过滤需要变体同源，不符合既定内容归属 | 既有代码/MDX校验；新加 replacement 组装逻辑 |
| 跨仓依赖 lock 与影响分析 | 现有来源记录没有完整的上游块、被遮蔽块、上下文和消费绑定关系 | 文件 hash、源码差异、现有 checkpoint/provenance |
| Markdown 方言适配 | Milvus HTML、多代码结构与现有 Lark JSON 输入不同 | Cloud 组件、MDX 校验、publication adapter 接口 |
| Git/Lark 页级 ownership 与发布接线 | 当前 Guides 主源是 Lark，整组渲染/组装会覆盖或漏掉迁移页 | 既有 ownership、preserved/external 路径、导航与发布契约；需扩展而非绕过 |

“新增”指当前检查范围未发现能完成此项的接入实现；不表示基础算法必须全新手写。

## 7. 共享内容接入边界

共享源从 milvus-docs 的固定修订读取，由 zdoc 扫描、组装和适配，再接入既有发布流程。具体规则以[接口设计](../docs/interfaces/README.md)和[消费规范](../docs/consumption-schema.md)为准；本审计记录现有能力，不另行维护一套配置方案。

Milvus 的 `sync-shared-scripts` 有同步 Lark 脚本的历史机制，但其路径与当前 zdoc 布局不同，不能据此认定生产仍共享同一版本，也不能把脚本同步当成共享正文消费接口。

## 8. 验证与未验证事项

补充恢复核验见 [Git、图片与发布产物恢复能力](./recovery-capability-audit.md)。已读取固定 dev 的实际 OpenAI 英文/日文 blob，并对恢复相关六个实现文件核对 master/dev 一致性；正文恢复可复用 Git，线上回滚已有镜像 digest 契约。图片存储存在同 key 覆盖行为，应只为迁移页真实消费的资源补身份固定，不据短期 artifact 到期而引入整套归档。

实际运行了 zdoc 现有 `codeVariantFilter.test.js`，10 项通过，覆盖产品行/区域过滤及无效指令。日志见 [code-variant-test.txt](./evidence/build-audit/code-variant-test.txt)。这是局部现成能力验证，不是站点集成验证。


没有运行真实 zdoc 全量构建、paid translation、原始 artifact replay 或线上发布。正式接入前需对 md2md 固定版本、混合源 stage 合同、Cloud MDX 与语言覆盖完成集成验证，再按 zdoc 既有测试矩阵和 artifact replay 流程验收。

当前验证样例为 [Filtered Search](../examples/filtered-search/walkthrough.md) 和 [Delete Entities](../examples/delete-entities/walkthrough.md)。两者都是有限的离线原型，不代替真实 md2md、站点或发布集成。
