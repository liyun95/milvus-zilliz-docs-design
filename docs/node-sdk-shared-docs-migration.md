> **仓库侧说明（2026-11-17）**：本文复制自 zdoc 仓库 `.claude/plans/2026-11-16-node-sdk-shared-docs-migration-plan.md`，正文逐字未改；文首“状态”行反映的是方案定稿时点。执行进展：引擎泛化（WP-1）= zdoc [#1298](https://github.com/zilliztech/zdoc/pull/1298)，生产链泛化（WP-2）= [#1304](https://github.com/zilliztech/zdoc/pull/1304)，PR CI 与 pin-drift watchdog 泛化（WP-3）= [#1309](https://github.com/zilliztech/zdoc/pull/1309)，均已开出待评审；本机测试环境修复 = [#1303](https://github.com/zilliztech/zdoc/pull/1303)。生产 lane 多段接线（`_fetch-content-group.yml`，原 WP-2b）原递延为 WP-4.5；2026-11-17 拍板转手册级试点后，逐页路线的 WP-4/4.5/5/6 作废（见下方「2026-11-17 更新」），lane 接线归入 R2-node。配套的 201 页逐页清单副本见 [`research/evidence/node-sdk-shared-migration-manifest.json`](../research/evidence/node-sdk-shared-migration-manifest.json)。
>
> 与[技术设计 10（SDK Reference）](./design/10-sdk-reference.md)的关系：本试点不走该篇为 Rust 定义的手册级布局（manual.yaml + 整本 lock + 手册级记录），而是把 Guides 逐页模型泛化为第二个组（`shared-docs/node/pages/**`，逐页 page.yaml / lock.yaml / receipt）。原因见正文 §1.3：上游 web-content 的 node 文档 0/192 含 `doc:block` 标记、无 front matter，transform 零挂载点，逐页 overlay（链接改写 + front matter + product-names）即可覆盖试点目标。**2026-11-17 拍板：改为该篇的手册级布局，node 成为手册级首个落地对象，Rust 退为第二个（绿地变体）**。评估、终态框架与新工作包见下方「2026-11-17 更新」一节；以下正文保留为逐页路线的历史方案，其中与手册级冲突的处置（C 桶留飞书、B 桶 Base 链接语义、逐页种子）以更新一节为准。

## 2026-11-17 更新：拍板转手册级（manual）试点

**决定**：node SDK Reference 试点改用[技术设计 10](./design/10-sdk-reference.md)的手册级布局（`manual.yaml` + 整本 `lock.yaml` + 手册级记录 + `cloud_pages`），成为该布局的首个落地对象；Rust 改为第二个（绿地变体）。逐页路线的 WP-4（139 页种子）、WP-4.5（逐页生产 lane）、WP-5（Base 行编辑）、WP-6（逐页试跑）作废；已开出的 WP-1/2/3（#1298/#1304/#1309，链接见文首）是呈现无关的多组引擎／生产链／CI 泛化，照常合入作地基。201 页清单继续有效——它转为 R2 内容迁移的数据源（A=默认发布清单、B=exclude 清单、C=cloud_pages 迁移清单、D=评审、E=exclude 判定）。

### 为什么

1. **终态收敛**：SDK Reference 只剩手册级一条路线（guides 维持逐页），go/python/java/cpp/cli 后续零引擎改动复用迁移 runbook；否则终态是三套并存模型，node 逐页成为孤例。
2. **总工作量打平**：手册级管线（原 WP-R1）无论谁先做都要建。node 转手册级自身迁移约 +2 会话，rust 省 2 会话（R1 由 node 建成），到 rust 上线合计 8–9.5 vs 逐页路线 7–9 会话——不是更省，是更干净。
3. **迁移最贵的两块消失**：139 行 Base 链接翻转（Base 不再驱动 en 路由）与 139×2 逐页种子文件。
4. **手册级管线的首战就是迁移**：go/python/java/cpp/cli 全是带存量翻译的活手册迁移，rust 只证明绿地。用真值最全（Base Targets/metadata）、团队最熟的 node 先把迁移路径硬化，验证价值高于 rust 绿地先行。

### 事实依据（2026-11-17 dev 侧核实）

| 事实 | 对手册级接入的含义 |
|---|---|
| dev 布局 `content/en/reference/api/nodejs/nodejs/<Module>/<Module>-<Api>.md`（11 模块目录），slug `/node/node/<Module>-<Api>` | 与手册级路径规则同构，模板走 registry（`documentIdPrefix`/`prefix`）；路径、深链、翻译键全部稳定 |
| front matter 为 Base 真值：`added_since`（如 v2.3.x）、`type: docx`、`token`（飞书 token）、`sidebar_position`（Base 序，非字母序）、逐页 keywords | 迁移型手册的 metadata 需按页回填（一次脚本 + 评审），不能按 Rust 绿地型“规则推导 + 4 字段”直接套 |
| registry node 源含 fallback 链 english-v2.4→v2.5→v2.6→v3.0；手册级不支持 `source.previous` | 切换前断言 fallback 当前零贡献（dev 148 = Base 170 叶 − B 22，成立）后显式丢弃 |
| B 桶 22 页判定来自 Base Targets 字段 | exclude 清单有数据源，比 Rust“照 Go 先例”更硬 |
| 上游 0 标记、0 front matter | 两模型同样做不了页内 transform；node v1 整体递延 transforms 接线，随 Rust 接上游标记时一并验证 |

### 工作量对比

单位“会话”≈ 一个 PR 的实现 + 验证 + 评审修复（按 WP-1/2/3 实测节奏）。

| | 路线 A：维持逐页 | 路线 B：转手册级（拍板） |
|---|---|---|
| 前置 | — | R0 合入三 PR 作地基 + 本设计更新（0.5） |
| node 完成 | WP-4 种子(1) + WP-4.5 lane(1) + WP-5 Base 编辑(1) + WP-6 试跑(1) = 4 | R1a 手册呈现核心(1) + R1b 差异链(1) + R1c 通道与记录(1) + R2-node 接线(1) + R2-node 内容迁移(1) + 试跑发布(1) = 6 |
| Rust 之后 | WP-R1(2–3) + WP-R2-rust(1–2) = 3–5 | 只剩 R2-rust 绿地件（dev 初始内容／着陆页／生命周期 UI／current 搜索）= 2–3 |
| 到 Rust 上线合计 | 7–9 | 8–9.5 |
| 终态模型数 | 三套 | 两套 |

### 决策点处置

| 处置 | 项 | 原因 |
|---|---|---|
| 消亡 | §5.1 Base 链接形态（milvus.io vs zdoc URL） | Base 不再驱动 en 路由，139 行链接翻转整体不存在 |
| 消亡 | §5.3/§5.11 B 桶行链接语义；评审 P1-2 invalid 路由 | B 页 = `exclude` 条目 |
| 消亡 | §5.8 云独有功能规则 | `cloud_pages` 给出终态答案：C 桶 9 页迁入 zdoc `content/`；未来 volume 类同理 |
| 消亡 | P0 createImportJobs 重复行（阻塞项身份） | Base 编辑缩到 ~9 行 C 桶 retire；重复行仅剩数据卫生 |
| 存活 | §5.2 transform 挂载点 | 两模型同样等上游标记；node v1 递延 |
| 变形 | §5.4 D 桶 5 页 | 手册级“新增页默认发布”会带上，评审后决定收编或 exclude |
| 落位 | §5.5 product-names 特配 | 手册级 `product-names.yaml`（含 severity 扩展） |
| 新增 | — | token/type 逐页延续策略；sidebar_position 回填 vs 接受重排；fallback 零贡献断言；E 桶 26 页 exclude 判定 |

### 终态框架（两组态、一引擎）

```text
shared-docs/<group>/source.yaml  {repository, track, source_dir, presentation: pages|manual}
├─ pages 呈现（guides 专用，冻结）
│    pages/<id>/{page.yaml, lock.yaml, receipt} · Base 行 classifySourceRoute 接管
│    逐页更新（WP12 逐页 PR）· 逐页提升 · 快照基线
├─ manual 呈现（全部 SDK Reference：node → rust → go/python/java/cpp/cli → REST 最后）
│    manual.yaml{source.dir, publish.manual, exclude, milvus_values,
│                metadata+（迁移型含 type/token/keywords/sidebar_position 回填）,
│                cloud_pages, transforms} + 单 lock.yaml(current/next)
│    + Variables.json + product-names.yaml(severity) + content/
│    registry 来源切 shared · 无飞书 lane · 整本更新/提升
│    手册级记录 generated/en/manifests/shared-manuals/<id>.json
├─ 共享核心（呈现无关；WP-1/2/3 已落大半）
│    变换 WP10 · 双版合并+NextChannel WP11 · 产品名 · 连接值
│    链接换算 · customEditUrl · 组线程化(source-state/lark/aliases/publication/checkpoint)
└─ CI/守卫层（双布局）
     detect-groups 按形态 · lock/validate 逐组循环分叉 · push guard 双正则
     watchdog 双模式：pages=pin 漂移 ／ manual=pin 漂移+transform 目标存在+cloud_pages 引用
```

**SDK 迁移 runbook（node 试点产出，后续 SDK 复用）**：registry 切换 → 能力桶映射（A=默认发、B=exclude、C=cloud_pages、D=评审定、E=exclude+着陆页）→ metadata/token 回填 → Base 行转档案 → fallback 零贡献断言 → 沙盒 artifact 对 artifact 对现 dev 零预期外 diff → 发布。rust = 绿地变体（dev 种子 + 着陆页 + 生命周期 UI + current 搜索）。

### 新工作包

| 包 | 内容 |
|---|---|
| R0 | 合入 #1298/#1304/#1309 作地基；zdoc 执行计划改写（WP-4/5/6 → R 包） |
| R1a 手册呈现核心 | manual.yaml schema+校验、展开为虚拟页（桥接 WP-1 已泛化的 build-page）、手册级 lock、`shared-docs build/lock` 命令分叉、front matter 规则走 registry 模板 |
| R1b 差异链 | 连接值（milvus_values+Variables.json）、product-names severity、exclude、链接清单（LINK_TARGET_EXCLUDED/LINK_UNKNOWN_FORM）、cloud_pages 与 content/ 路径安全 |
| R1c 通道与记录 | current/next 双版生成与合并（复用 WP11）、手册级记录 schema/生成/纯校验、整本更新与提升工具（WP12/13 手册级） |
| R2-node 接线 | registry drive→shared 切换、fetch 无飞书来源分支、watchdog/push-guard/detect-groups 双布局（含手册级 pin 漂移扫描） |
| R2-node 内容迁移 | metadata/token/keywords/sidebar_position 回填脚本（Base 导出→manual.yaml）、C 桶 9 页飞书→content/ 转写、B/D/E 桶处置、Base 行 lifecycle |
| 试跑与发布 | 沙盒 artifact 对 artifact 零预期外 diff、翻译/lark-revisions 连续性断言、发布 |

### 对技术设计 10 的增补（迁移型手册接入）

设计 10 现文按 Rust 绿地书写；node 试点需要补“迁移型手册接入”一节，差异：

1. **metadata 字段扩展**：迁移型按页回填 `type/token/keywords/sidebar_position/last_modified/notebook/beta/added_since/deprecate_since`；绿地型维持现状（4 字段 + token/type 规则生成）。
2. **token/type 延续**：沿用现 dev 页身份（`type: docx` + 飞书 token），避免翻译／修订身份重算；手册级记录按页记录身份。
3. **fallback 断言**：切换前断言旧 fallback 源零贡献（node：v2.4/2.5/2.6 均零）。
4. **C 桶迁移**：云独有页从飞书转写为 `content/` 完整页（H1+正文），Base 行 retire。
5. **Base lifecycle**：A/B 行转档案（不再驱动 en；翻译分组与 lark-revisions 按手册键，不受影响）。
6. **沙盒验收基线**：artifact 对 artifact 对现 dev，差异必须全部归因到已知 overlay（连接值／产品名／链接改写）。

### Rust 的位置

设计 10 的 WP-R1 范围被 R1a–R1c 覆盖大半；Rust 剩 R2-rust 绿地件（dev 初始内容、着陆页、生命周期 UI、current 搜索）。设计 10 与 README 的交叉引用已随本次更新同步修订。

---

# Node SDK 参考文档 shared-docs 迁移方案(pilot study)

日期:2026-11-16
状态:扫描完成,待拍板(决策点见 §5)
配套清单:`.claude/plans/2026-11-16-node-sdk-shared-migration-manifest.json`(201 页逐页明细,含 record_id / 上游文件 / 上游 milvus.io URL / 飞书 URL / 云路径)
扫描工件(临时,可删):`tmp/nodesdk-scan/`(Base 记录 ndjson、上游文件清单、milvus-sdk-node 与 web-content 稀疏克隆)

---

## 0. 一句话结论

node 手册(`reference/api/nodejs`)已在 registry 中由飞书 drive Base 取稿;本次迁移 = 把 **139 个开源/云共用页**的内容来源切换到 shared-docs 管线(上游 `milvus-io/web-content` 的 `API_Reference/milvus-sdk-node/v3.0.x`),**9 个云独有页留在飞书**。共用页在 Base 中的 Docs 链接替换为上游 milvus.io 文档页 URL。shared-docs 引擎目前深度绑定 guides+milvus-docs,需要一轮泛化(引擎 ~10 处、生产 fetch 链 ~15 处、CI 4 个 workflow),这是本试点的主要工程量;**transform 挂载点上游暂不存在**(上游页面无 `doc:block` 命名块),建议试点期 overlay 仅含链接改写 + front matter 徽章,transform 能力后置。

## 1. 扫描结果

### 1.1 三方输入画像

| 输入 | 事实 |
|---|---|
| 飞书 Base `LlrPbysPZau2dGsSVuicHmvCn0e`(表 `tblT65LG94H2vobA` "数据表") | 182 行 = **171 叶行**(147 Function/12 Class/9 method/3 Enum;**170 个唯一 Slug——`DataImport-createImportJobs` 存在 2 条重复行 recvmMHuE5Iat6/recvmMHy6dzJ49,同 slug 同飞书 docx,P0 脏数据须在 WP-5 前去重**)+ 11 VirtualNode 组节点;字段:Slug / Docs(飞书 docx/folder 链接)/ Description / Targets(Milvus±Zilliz)/ Tag(ON REQUEST ×10)/ Added Since / Deprecate Since / Last Modified At / Progress(全 Draft)/ Seq. ID / 父记录。**Base Slug 与 dev 页面文件名 1:1**(`<Group>-<Api>.md`) |
| 上游 `milvus-io/web-content` master `API_Reference/milvus-sdk-node/v3.0.x` | **扫描基线 commit `01ea1bb3397c34b6ddac7381cd41c7e4acd895d9`**(manifest 已记);192 个 md,布局 `<Group>/<File>.md`(11 组);**无 front matter、无 doc:block 命名块(0/192)、无图片(0)、无多语言代码组(0)**;17 个文件含 `<div class="alert note|warning">`(24 note+3 warning;md2md 已支持的 admonition 形态);裸 basename 全局唯一;内部链接目标去重约 42 个(裸文件名 + `../组/文件.md` 相对路径)+ 17 处 `https://milvus.io/docs/*` 绝对链(7 个去重 URL);milvus.io 发布 URL 实测 200(抽样):`https://milvus.io/api-reference/node/v3.0.x/<Group>/<File>.md` |
| 代码仓库 `milvus-io/milvus-sdk-node`(npm 3.0.7) | 用于云独有判定(§1.2 C 桶);9 个候选 API 在代码中**全部存在**(getTelemetry→`milvus/grpc/GrpcClient.ts`、BulkWriterOptions/FlushEvent/Formatter→`milvus/bulkwriter/*`、HttpImport*→`milvus/http/Import.ts`+`types/Http.ts`) |
| 本仓库现状 | node manual 已注册:`packages/docs-tooling/src/manuals/registry.ts:432-464`,`english-v3.0` 源 = 该 drive Base(root `LW67fVlTvlNCZRdxOVYcQZyJnFQ`,generatorManual `nodejs30`);en 发布 `content/en/reference/api/nodejs/nodejs`(landing `nodejs.md` 为 master-preserved);dev 现有 148 页;`generated/en/sidebars/node.sidebar.js` 由 fetch 生成;zh-CN/ja-JP 为机器翻译(无飞书中文源) |

### 1.2 五桶分类(详见 manifest)

| 桶 | 数量 | 定义 | 处置 |
|---|---|---|---|
| **A 迁移集** | **139** | Base 行 ↔ 上游页精确匹配 ∩ Targets 含 Zilliz(= 今天在云上由飞书取稿的共用页) | 建 shared-docs 页 + Base 链接换上游 URL + fetch 接管 |
| B 共用但云不发布 | 22 | 匹配上游 ∩ Targets 仅 Milvus:ResourceGroup 组(11 叶)+ RBAC V1 系(addPrivilegesToGroup/backupRBAC/createPrivilegeGroup/grantPrivilege/restoreRBAC/revokePrivilege 6)+ Management 4(getCompactionStateWithPlans/getPersistentSegmentInfo/getQuerySegmentInfo/loadBalance)+ Vector-getMetric | 云站今天就不发布(170 唯一叶 − 22 = 148 = dev 页数,吻合)。链接处置见决策点 §5.3/§5.11(B 行换上游 URL 会使 `classifySourceRoute` 落 invalid 路由,须先拍板语义) |
| **C 云独有** | **9** | Base 行无上游对应页;API 在 SDK 代码中存在(Client-getTelemetry、DataImport-BulkWriterOptions/FlushEvent/Formatter/HttpImportCreateReq/…CreateResponse/…ListResponse/…ProgressReq/…ProgressResponse) | **留在飞书继续编辑**,Base 链接不动;shared 管线不接管 |
| D 上游新增函数页 | 5 | 上游有、Base 无:function 页(selectGrant/reconnectToPrimary/getImportJobProgress/getIndexStatistics/Vector-deleteEntities) | 是否顺带补齐为新云页,待拍板(§5.4) |
| E 上游 meta 页 | 26 | About.md + 类型/枚举 meta 页(RowData/SearchData/GrantEntity/FieldType/OutputTransformers 等) | 不建云页;进 links.yaml 作为上游外链目标 |

### 1.3 决定方案形态的关键事实

1. **transform 零挂载点**:引擎 transform 的 `target.block` 必填(`packages/docs-tooling/src/shared-docs/core/transforms/schema.ts`,required `['block']`),block 依赖上游 `doc:block:start id="…"` 标记;web-content v3.0.x **0/192 个文件有标记**。→ 试点期 overlay 只能做:links.yaml 链接改写 + front matter(beta 徽章、added_since 等)+ product-names;内容级覆盖(replace/add/remove)需先解决挂载点(§5.2)。
2. **引擎上游布局假设 = milvus-docs `site/en/…`**:公共页面 ID 从 front matter `id:/title:` 推导(`adapters/links-input.ts:140-148`,web-content 无 front matter 会 throw);fragment root 硬编码 `site/en`(`adapters/git-milvus-docs-reader.ts:64,73,75`);页面枚举前缀 `site/en/`(`links-input.ts:136`);fetch inventory `gitInventory(repo, commit, ['site/en'])`(`scripts/docs-workflow/guides-shared-sources.js:81`)。→ 均需按 node 布局(`API_Reference/milvus-sdk-node/v3.0.x/<Group>/<File>.md`)泛化。
3. **publish.manual 引擎层仅认 guides/guides-byoc**:`adapters/build-page.ts:43,310-322`(CONFIG_MANUAL_UNKNOWN)、receipt 校验 `core/handoff/source-state.ts:163,170`(输出路径必须 `content/en/{guides|byoc}/…`)、组门禁 `adapters/group-context.ts:18-20`(basename 必须 'guides')。→ 放行 reference manual + node 输出路径是核心泛化点。
4. **接管机制 = Base 行 doc_link 指向 shared-docs**:`classifySourceRoute`(`core/handoff/source-state.ts:46-67`)把指向 `github.com/zilliztech/zdoc/tree/master/shared-docs/<group>/pages/<page>` 的行路由为 shared-page,fetch 跳过飞书正文抓取(`lark/larkDocScraper.js:902`),receipt 落 `generated/en/manifests/shared-pages/<group>/<page>.json` 并成为源证据(sourceCompleteness/增量规划/revision-inventory 全消费 receipt)。→ node 复用同一机制,需把 URL 识别/组名/路径断言泛化。
5. **侧栏单生产者**:`node.sidebar.js` 由 fetch(drive writer)整棵生成;shared 页经 `sharedPagePublication.projectFallbackSidebar`(`lark/sharedPagePublication.js:281-377`,guides 已用)投影进侧栏 → node 需要同一投影路径(`lark/index.js:644-700` 硬编码 `manualName==='guides'`)。
6. **Snapshot 组 = ON REQUEST**:Base Tag 10 行全部是 Snapshot 组(9 叶+组节点)→ page.yaml `metadata.beta: 'ON REQUEST'`(合法 DOC_HEADING_TAGS,`config.ts:55-60`)。
7. **slug/路径全部不变**:dev 页面路径 `reference/api/nodejs/nodejs/<Group>/<Group>-<Api>.md`、Docusaurus slug `/node/node/<Group>-<Api>` 迁移前后一致 → zh-CN/ja-JP 存量翻译与站内深链不受路径影响;en 正文替换会触发首轮 reconciliation(正文同源,预计以格式 diff 为主)。
8. **node manual 已存在** → manuals README 的"新增 manual 全序列"(registry 声明/landing/翻译 GROUPS/dispatch 矩阵等)**大部分不适用**;本迁移不加 manual,只给现有 manual 的部分页面换内容来源。

### 1.4 云独有功能与页内云专属内容(2026-11-16 追加扫描)

- **Volume/VolumeManager 实查**:SDK 代码有完整云功能面(`milvus/types/Volume.ts`、`milvus/bulkwriter/VolumeManager.ts`:`cloudEndpoint`+`apiKey`、`VolumeType` MANAGED/EXTERNAL、projectId/regionId/storageIntegrationId),但 **Base 0 行、上游 0 页、dev 无独立页**——dev 仅在 createCollection/refreshExternalCollection 页内段落提及 `volume://` scheme。即 volume 属于"代码在开源包里、文档哪里都没有"的待建云页,不在本次迁移范围(迁移只搬已有页)。
- **页内云专属段落规模**:139 个 A 页中仅 **5 页**含 "On Zilliz Cloud, …" 段落,共 **11 处**(Collections-createCollection×6、refreshExternalCollection×2、createAlias/describeAlias/alterAlias 各 1),内容全部是 `external_source` 的 `volume://…`/`milvus://…` scheme;上游 0 处。
- **整体发散度**(规范化 diff:剥 front matter/锚点/链接 URL/强调标记):139 页 dev-only 共 1957 行、upstream-only 共 2938 行;仅 **15/139** 页近似同(dev-only≤3)。top 发散:createCollection(dev-only 235)、Vector-search(80)、addCollectionField(s)(70/68)、queryIterator(56)、describeRole(45)。发散构成 = ①版本偏斜(两边各自演进,部分页上游更超前:IndexType up-only 120、hybridSearch 114、search 166、searchIterator 83)②真云专属内容(external collections 参数、On Zilliz Cloud 段落、部分默认值说明)。
- **结论**:接管 = 以上游 HEAD 为准替换正文;dev 侧 1957 行 dev-only 内容默认丢弃,其中真正云专属的部分(少量、可枚举)必须在接管前显式归类(推上游 / overlay / 暂缓),见决策点 §5.8-9。
- **session()/VolumeManager 裁决(代码证据,2026-11-16 二轮)**:session() = cluster-pinned DQL 会话(MilvusClient.ts:86-97 + MilvusClientSession 7 方法,注入 `cluster_id`),**代码层零云依赖,语义层服务 Zilliz Cloud global cluster**('global-cluster' 端点检测、in07- 集群 ID)→ 共用 API(云场景可选),维持 A 桶;迁移评审时核对上游页/云页是否如实描述 cluster-pinned 语义。VolumeManager(cloudEndpoint+apiKey 强制、Bearer 头、`/v2/volumes` 控制面)→ **100% 云独用**,C 桶模式,文档事实源=控制面 openapi.yaml + OpenVolumeController.java。

## 2. 目标架构(迁移后)

```
飞书 Base(node/v3.0.x 表,182 行)
├─ A 139 行:Docs → https://milvus.io/api-reference/node/v3.0.x/<Group>/<File>.md
│    └─ fetch:shared-page 路由 → 跳过飞书 → shared-docs/node/(pinned web-content + overlay)→ 原路径/原 slug 落 dev + receipt
├─ B 22 行:Docs → 上游 URL(仅导航;不发布,无 shared 页)
├─ C 9 行:Docs → 飞书 docx(不变,继续飞书取稿)
└─ VirtualNode 11 行:Docs → 飞书 folder(不变,编辑导航用)
```

新 shared-docs 组(本仓库 master):

```
shared-docs/node/
├── source.yaml        # repository: https://github.com/milvus-io/web-content, track: master (+ 新增 sourceDir/root: API_Reference/milvus-sdk-node/v3.0.x — schema 需扩展)
├── links.yaml         # 仅非接管目标的内部链接:26 E 页 + 5 D 页 → milvus.io 外链;(A 组内部链接由引擎按页面注册自动改写为 ./<slug>)
├── product-names.yaml # node 特配(API 页大量 Milvus 字样,见 §5.5)
├── Variables.json     # 如需(视 C/A 措辞)
└── pages/<Group>-<Api>/
    ├── page.yaml      # source.file: <Group>/<File>.md; publish: [{manual: node, path: <Group>/<Group>-<Api>}]; metadata.beta: ON REQUEST(Snapshot 9 页)
    └── lock.yaml      # 初始 pin = 扫描时 master 头(shared-docs lock 命令产出)
```

## 3. 工作包分解(全部 master 工具面,走 PR)

### WP-1 引擎泛化(S→M)
组门禁(`group-context.ts:18-20`)、source config 增加 source root/layout 字段(`core/config.ts` schema_version 2 或可选字段)、公共 ID 推导兜底为路径派生(`<Group>-<File>`;`links-input.ts:140-148`+`build-page.ts:223-230`)、页面枚举/fragment root/预热 listFiles 按 source root 参数化(`links-input.ts:136`、`git-milvus-docs-reader.ts:64-75`、`build-page.ts:71`)、跨组相对链接(`../组/X.md`、`组/X.md`)归一化为裸名再走 map(`core/links/map.ts`+`rewrite.ts`)、handoff 校验放行 node+reference(`source-state.ts:50,100,137,163,170`)、`build-page.ts:319-322` 放行 reference manual(输出路径断言改按 registry publication)、`customEditUrl` 由 repository 推导(`build-page.ts:357`)。同步修 `testing/workflows.test.ts` 等 pin 单组的测试。

### WP-2 生产 fetch/发布链泛化(M)
`scripts/docs-workflow/guides-shared-sources.js`(sharedRoot/inventory root/receipt repository 字段)、`lark/sharedPageFetch.js`(manifest 路径、输出路径 regex `content/en/(guides|byoc)/tutorials/…`→node 路径、manuals 枚举、`initializeSharedScraper`)、`lark/sharedPagePublication.js`(tutorials regex、`ref:tutorials` sidebar key、sidebars 名称)、`lark/sharedPageBundle.js`、`lark/sharedPageRenderIdentity.js`(OVERLAY_ROOT)、`lark/index.js:644-700`(shared 逻辑对 reference manual 生效)、`cli-main.ts:187`+`lark/incrementalSharedReceipts.js:22`(receipt manual 放行)。
**per-page 元数据通道(P1-4)**:引擎 front matter 现硬编码 `added_since: FALSE/last_modified: FALSE/type: origin/token: shared-<pageId>/displayed_sidebar: default`(`core/site/front-matter.ts:35-50`),而 dev 现网页带真实 `added_since/last_modified`(Base 列)、`type: docx`、`token: <飞书token>`、`keywords:`。需新增 per-page 元数据通道(page.yaml metadata 扩展或 snapshot 记录注入)承载 Base 的 Added Since/Last Modified,并把 `type/token/keywords` 三字段的取舍写成显式断言(维持原值会影响 shared 语义;改值须先查 token 深链消费方)。

### WP-2b node 生产 lane 接线(P1-1,评审新增)
生产 node fetch 走 `fetch-docs.yml → produce_sdk_reference → _fetch-content-group.yml`,该 lane **没有任何 shared 准备步骤**(shared prep 仅存在于 `_fetch-guides-sources.yml:87-116` 且 `if: site=='en'`)。必须:`scripts/docs-workflow/content-groups.js` node 组 ownedPaths 补 `generated/en/manifests/shared-pages/node`(参照 guides 组的 receipt/assembly/report 路径);`_fetch-content-group.yml` 增 shared 上游准备+基线 receipt 恢复(把 `_fetch-guides-sources.yml:87-116` 抽成 composite 复用);核对 `prepare-content-group-workspace.js`;`scripts/restore-generated-state.sh` 清单补 shared-pages/node 基线。缺此 WP,生产 lane 的 checkpoint 不携带 receipt → 增量 fetch 必然退化全量(即 2026-11-12 en-fetch-incremental-fix 的同型事故)。

### WP-3 CI 与守护(M)
`adapters/detect-groups.cjs:26-28` 多组化;`shared-docs-lock.yml`(source.yaml 路径、lock 路径 regex、clone 各组 repository)、`shared-docs-validate.yml`(sparse checkout 各组上游目录 + dev 证据)、`shared-docs-adopt-variant.yml`(如 node 需要)、pin-drift watchdog 加 node 轮(`shared-docs-pin-drift.js` 本身已组参数化);`_fetch-guides-sources.yml` 的 shared 生成步骤对 node lane 复用(抽出参数化 composite,与 WP-2b 同一改动);test-matrix/path-filters 核对(`scripts/docs-workflow/test-matrix.json` 已有 `shared-docs/**` 通配条目;`deploy/contracts/path-filters.json` 新增 node 相关条目);**新增 node replay 表面时同步更新机器可读矩阵与人类可读 spec(`.claude/specs/2026-08-31-docs-workflow-code-test-matrix.md`)——unmapped path = matrix gap,须在同一 change 修**。

### WP-4 内容种子(S,部分并行——有依赖注意)
按 manifest 生成 `shared-docs/node/` 全量文件(139 page.yaml+lock.yaml、links.yaml、product-names、source.yaml);Snapshot 9 页 `metadata.beta`;`docs-tooling shared-docs lock` 初始化 pin。**依赖(P2-3)**:page.yaml 骨架/links.yaml 可先行;`source.yaml`(schema 扩展字段)与 lock 初始化强依赖 WP-1 合并——`core/config.ts:11-15` 未知键报错,`shared-docs-lock.yml:85-92` 直接读 source.yaml。**pin 基线(P1-3)**:divergence 结论基于 web-content `01ea1bb…`;lock 时若 track HEAD 已移动,必须对最终 pin commit 重跑规范化 divergence 并回填 §5.9 归类清单,再以重跑结果驱动 §6.2 断言。WP-4 的 page.yaml 字段组必须是 §8.2 overlay 字段组的子集(P2-5,防止两套 YAML 方言)。

### WP-5 飞书 Base 编辑(S)
**先去重(P0-1)**:`DataImport-createImportJobs` 双行(recvmMHuE5Iat6/recvmMHy6dzJ49)删一行(或双行同改),否则同 slug 双源路由冲突(`incrementalFetchPlanner` ownership 冲突)。然后 `+record-batch-update` 分批:139 A 行 Docs → 上游 milvus.io URL;B 22 行按 §5.11 拍板结果处理;C/VirtualNode 不动。**改后路由断言**:用 `classifySourceRoute` 对全表 182 行跑一遍,断言零 invalid(尤其 B 行的终态语义)。注意 `+update` 网格类字段的已知坑(本表 Docs 是 text(url) 字段,直接 markdown link 写入即可)。

### WP-6 验证、试跑与发布(M)
序列见 §6;重点:artifact-only/沙盒分支试跑 produce_node,逐页断言(见 §6.2),再生产落 dev。

### WP-3b 上游标记保护(Phase 2 前置;milvus-docs 部分为现存欠账,可随 Phase 1 顺提)
目的:确保我方加在上游的 transform 定位标签(`<!-- doc:block:start id="…" -->` / `doc:block:end` HTML 注释)不被上游维护者或 AI agent 当"遗留注释"清理。三层:
1. **上游说明层(软保护)**:`milvus-io/web-content` 在现有 AGENTS.md 加 "Reserved markers" 一节(标记语法、消费方=zilliztech/zdoc shared-docs 渲染管线、禁止删除/改 id/重排、新增 id 命名约定、触碰须在 PR 描述注明)+ CONTRIBUTING.md 一句;`milvus-io/milvus-docs` **新建 AGENTS.md**(现无任何 AI 指引文件)并同节——guides 现网 55 处标记(如 site/en/reference/multi_tenancy.md:23)已裸奔,此 PR 同时保护存量。SDK 仓库(milvus-sdk-node)不需要——标记只在文档仓库。
2. **消费端 fail-closed(已有,核实于 `core/transforms/index.ts:73`)**:被 transform 引用的标记被删/改 id → `TRANSFORM_TARGET_NOT_FOUND` build 红(validate/lock/生产 fetch 全触发);re-pin 必须走 PR→validate,有闸。
3. **自卫层(本 WP 新增)**:pin-drift watchdog 增加检查——从 `shared-docs/*/pages/**/page.yaml` 收集全部 transform target block id(含尚未写 transform 的预留标记),在上游 HEAD 断言 `doc:block:start id="<id>"` 仍存在,缺失即 watchdog 红。这是对"预留标记静默丢失"的唯一自动探测,也是"务必确保"的落点。

**已核实无需改动(评审负结论,实施时不必重查)**:registry.ts(node 已注册);翻译 selection/candidates/bootstrap-state(registry 驱动 `scripts/translation/selection.js:7-9`,node 目录前缀不变即不变);`generate:reference-presentation` 派生物;`scripts/validate-generated-sidebars.js`(按 site 校验,node.sidebar.js 已在 restore 清单);`deploy/contracts/localization-inputs.inventory.json`(现含 0 条 shared-docs 路径,guides 先例成立);`test-matrix.json` 的 shared-docs 通配条目(已有,仅需补 node replay 表面行);ja-JP 通道(照常机器翻译);REST 管线。

## 4. 分期建议

- **Phase 1(试点闭环)**:WP-1/2/3 最小泛化 + WP-4 种子 + WP-5 Base 编辑 + WP-6 发布,overlay = 链接改写+front matter,不含内容 transform。完成即"node sdk 迁移"的主体目标(139 页切源、9 页留飞书)。
- **Phase 2(按需)**:transform 挂载点方案落地后补云覆盖类 overlay(§5.2)。**前置 = WP-3b 上游标记保护三件套**(见 WP-3b;未做前不得往上游加 `doc:block` 标记)。
- **Phase 3(可选)**:node 接入 `shared-guides-update` 式自动 update bot 与 adopt-variant;上游独有 D 桶页补齐;**sdk-upstream-scan 自动化工作流落地(§8,终局架构)**。

## 5. 决策点(待拍板)

1. **Base 链接形态**:①`https://milvus.io/api-reference/node/v3.0.x/<Group>/<File>.md`(用户指示的"上游文档页面链接";路由需新增"上游 URL → 页"识别,经 links.yaml 反查)②`https://github.com/zilliztech/zdoc/tree/master/shared-docs/node/pages/<page>`(guides 先例,引擎几乎零改动即识别)。**推荐 ①**(编辑者在 Base 里看到的即上游权威文档;且与"链接换成上游链接"的字面要求一致),实现上路由同时兼容两种形态,①失败回退②。
2. **transform 挂载点**:①给 web-content 上游提 PR 加 `doc:block` 标记(跨仓库、上游协作成本高)②引擎扩展 target 类型(heading 定位/整页 replace,node 内容无命名块也可用)③试点期不做内容 transform。**推荐 ③,需求出现时选 ②**;overlay 需求本身要先出现——目前 9 个云独有页不在 shared 管线,A 页与上游正文同源。
3. **B 桶 22 页**:不建 shared 页、不改 Targets、不发布;若未来要上云站,先改 Targets 再入 shared-docs。链接形态与路由终态语义见 §5.11(推荐维持飞书链接)。
4. **D 桶 5 页**(selectGrant/reconnectToPrimary/getImportJobProgress/getIndexStatistics/Vector-deleteEntities):是否随迁移补齐为新云页?补齐则进 A 流程(Base 加行+shared 页+翻译);不补则 links.yaml 指向 milvus.io 外链。**建议本期不补**,保持 Base/侧栏面不变,后续单独提。
5. **product-names 口径**:node API 页必然大量出现 `MilvusClient`/`Milvus`/`@zilliz/milvus2-sdk-node`;node 组的 check 列表需要按 reference 语境特配(如仅 `localhost`/`127.0.0.1`/`root:Milvus` 入 check,`MilvusClient` 等 API 名入 allow),避免 PRODUCT_NAME_FOUND 全红。
6. **VirtualNode 组行**:Docs 保持飞书 folder(编辑导航);上游无组级页面可指。
7. **source.yaml track**:web-content 无版本分支,`track: master` + 每页 lock pin 控 drift;pin-drift watchdog 覆盖 node。
8. **云独有功能(如 volume/VolumeManager)的生产规则**:现状 = 代码在开源包、Base/上游/云均无文档页。规则建议:**云独有页一律走 C 桶模式**(新建 Base 行 + 飞书文档,shared-docs 不接管);"代码开源、功能属云"的 API 是否推上游 web-content PR 由产品逐个拍板——上游一旦有页,自动转正为 A 桶候选进 shared-docs。→ 本期是否补 volume 云文档(飞书新页)待拍板。
9. **页内云专属内容接管前归类**:11 处 "On Zilliz Cloud" 段落 + top 发散页(>20 dev-only 行,约 20 页)逐页评审,三选一:①内容对开源成立 → 推上游 PR(首选);②仅云成立 → Phase 2 transform overlay(page.yaml;Phase 1 无挂载点);③暂缓该页接管,维持飞书源。其余 ~115 页小发散默认以上游为准(dev 侧版本偏斜内容放弃),抽样 ≥10 页复核。评审清单由 manifest + `tmp/nodesdk-scan/divergence.pkl` 生成。
10. **function_white_list 数据通道**(终局架构 §8 的关键缺口):内容在 cloud-meta 运行库,两仓库只有 schema。三选一:①云团队定期导出 JSON/CSV 进 zilliz-cloud-config(推荐,与 manifest↔override 分层同构);②工作流调 `/cloud/v1/function/white/list`(需凭证+region 路由);③人工维护 data 文件叠加。SDK 方法名↔function name 映射首建需人工。
11. **B 桶 22 行的路由终态(P1-2,评审新增)**:`classifySourceRoute`(`source-state.ts:46-67`)只识别 zdoc shared-docs URL 与飞书域;B 行换 milvio 上游 URL 会永久落 `invalid` 路由(OWNERSHIP_CONFIG_MISSING)。三选一:①**B 行维持飞书链接(推荐,最稳,改动为零)**;②路由层显式增加"上游 URL ∩ 不在发布集(Targets 无 Zilliz)= 容忍跳过"语义;③B 行也用 shared-docs URL 形态但豁免 availablePages 反查。无论选哪项,WP-5 改后必须对全表 182 行跑路由断言(§WP-5)。

## 6. 验证与发布序列

### 6.1 本地/master PR 闸
- `pnpm test:for-change -- <全部变更路径>`(矩阵 union;`packages/docs-tooling/src/shared-docs/**`、`packages/docs-tooling/src/lark/shared*`、`scripts/docs-workflow/guides-shared-sources*`、4 个 shared-docs workflow、`shared-docs/node/**` 各有对应测试组;新增 node 表面须同步补 test-matrix 行,unmapped path = matrix gap)
- `pnpm test:shared-docs`、`pnpm test:replay:shared-pages`(新增 node replay 表面后)、**`pnpm test:replay:all` + `pnpm test:workflow-policy`(本迁移横跨 Fetch+shared 发布契约,按 AGENTS.md 必跑)**、`pnpm typecheck`、`git diff --check`

### 6.2 试跑断言(沙盒分支 artifact-only fetch,勿碰生产 dev)
0. **迁移前内容评审先于一切**:11 处 "On Zilliz Cloud" 段落与 top 发散页按 §5.9 逐处归类落档(推上游 PR 已开/已合;overlay 待 Phase 2;暂缓接管名单),暂缓页从本轮接管范围剔除。
1. 139 A 页(扣除暂缓):输出路径/slug/sidebar_label 与 dev 现网逐页一致;front matter beta(Snapshot=ON REQUEST,其余 false)保持,**added_since/last_modified 按 WP-2 元数据通道保持真实值(非 FALSE),type/token/keywords 按 §5.11 拍板的断言核对**;正文 = 上游内容+链接改写(内部链→`./<slug>`、E/D 目标与 milvus.io/docs 链→外链);product-names 全绿;**"On Zilliz Cloud" 段落按归类结果存在/缺失符合预期,不得静默丢失**。
2. 9 C 页:字节不变(仍走飞书)。
3. receipt:`generated/en/manifests/shared-pages/node/<page>.json` 逐页生成且 `validatePublishedReceipt` 通过;`revision-inventory build --group node` 通过;`validate-revision-inventory --site en` 通过;**生产 lane(`_fetch-content-group.yml`+`content-groups.js` node ownedPaths)携带 receipt(WP-2b 验收点)**。
4. `node.sidebar.js` 由 fetch 产出且含 shared 投影条目;`pnpm build:en`/`build:zh-CN` 通过。
5. 增量验收:连续两次 fetch,**在生产等价 lane**第二次零漂移(receipt 命中,不退化全量——复用 #1284/#907 的验证方法)。

### 6.3 上线顺序
master PR 合并 → WP-5 Base 编辑(建议在 fetch 停窗内或与 fetch 排队错开)→ 生产 fetch(produce_node)落 dev → 预览验收 → 翻译 lane 跟进首轮 reconciliation。护栏:任何 `REMOTE_STATE_UNKNOWN`/publication 闸红即停,按 runbook 处置;不在无评审下 force-push 或重置。

## 7. 风险清单

| 风险 | 缓解 |
|---|---|
| 坏 pin → 生产 fetch 静默 fallback(guides 已知形态) | pin-drift watchdog 增 node 轮;试跑断言产物指纹 |
| receipt 链不完整 → en node fetch 退化全量 | §6.2-5 增量验收;`incrementalSharedReceipts` 泛化必测 |
| 上游 `master` 无版本轨,内容漂移快 | 每页 lock pin + watchdog;web-content 更新节奏进周报观察 |
| 首轮 en 正文替换触发 zh/ja 大面积 reconciliation | 正文同源、diff 以格式为主;翻译预算预留;必要时分批接管(先 1-2 组试) |
| `<div class="alert">` 18 文件的 MDX 转换 | md2md 已支持该形态(guides 同款);build 闸兜底 |
| Base 批量编辑与 fetch 竞态 | 分批 +record-batch-update,避开 fetch 窗口;改完抽验 classifySourceRoute 路由结果 |
| Base 脏数据:重复行(P0-1)→ 同 slug 双源路由冲突 | WP-5 先去重;改后全表 182 行路由断言零 invalid |
| front matter type/token 漂移(type: docx→origin、token→shared-*)影响按 token 深链的消费方 | WP-2 元数据通道显式断言;试跑期专项核对深链消费方 |
| 扫描基线(web-content 01ea1bb…)与 lock pin 漂移 → §5.9/§6.2 断言失配 | WP-4 对最终 pin 重跑 divergence 并回填(§6.2-0 前置) |
| 上游误删 `doc:block` 标记:被 transform 引用的 → `TRANSFORM_TARGET_NOT_FOUND`(`core/transforms/index.ts:73`)build 红;**未被引用的"预留标记"被删则完全静默**(引擎不校验未使用标记) | 三层防护(WP-3b):①上游 AGENTS.md/CONTRIBUTING 说明(web-content 有现成 AGENTS.md;milvus-docs 连 AI 指引文件都没有而 guides 已有 55 处标记=现存欠账)②消费端 fail-closed(已有)③pin-drift watchdog 增"声明的标记集合在上游 HEAD 仍存在"检查(覆盖预留标记) |

## 8. 终局架构:sdk-upstream-scan 自动化工作流(仿 REST upstream 双件套,2026-11-16 二轮调查定稿)

目标(用户拍板方向):workflow 扫描 SDK 仓库→方法清单→归属推理→扫描 zilliz-cloud/zilliz-cloud-config 得云适用范围→生成 overlay 初稿→自动开 PR 供评审,迭代式维持 shared-docs/node 与 Base/上游三方一致。

### 8.1 归属推理的关键修正:docstring 规则无推断力

全库 ≈242 公开方法(156 gRPC mixin 链 + 74 HttpClient + BulkWriter 7 + VolumeManager 5)。gRPC 链 JSDoc 覆盖 92.9%(145/156),但 **143 个带 docstring 方法中 `zilliz/cloud/localhost/19530` 关键词命中全部为 0**——"docstring 提 Zilliz Cloud → 云"类规则在主链上永不触发。云硬信号实际分布在:

| 信号 | 位置 | 判定 |
|---|---|---|
| 构造强制 `cloudEndpoint`+`apiKey`、Bearer 头、`/v2/volumes` 路径 | VolumeManager.ts:13-35,97-103 | 5 方法 100% 云独用 |
| `cluster_id` 注入 + `'global-cluster'` 常量 + `isGlobal` | MilvusClient.ts:86-97、utils/GlobalTopology.ts:12、types/Client.ts:79-82 | session 系 7 方法+reconnectToPrimary = 共用偏云场景 |
| 类型注释提 Zilliz Cloud / 测试硬编码 api.cloud.zilliz.com | types/Client.ts:14-16、test/bulkwriter/VolumeManager.spec.ts:4 | 点状增强 |
| in-repo Astro Starlight 文档(13 个 api-reference mdx,标题即方法名,近全量覆盖) | docs/src/content/docs/api-reference/*.mdx | 机器可消费的第三对照源+云注意事项散点 |
| 控制面 REST 路径/参数(projectId/regionId/storageIntegrationId) | types/Volume.ts:7-16 | 云控制面判定 |

**归属引擎设计**:默认"共用" → 硬信号规则判"云相关" → 与上游 web-content 存在性 join(有上游页→A 桶;无页+硬云信号→C 桶候选;无页+无信号→缺口清单) → 人工兜底 10-25 项(session 语义档、版本门槛 vs 部署门槛、cross-cluster replication、HTTP 74 方法无 docstring 靠 mdx 分组、两文档面命名对齐)。`npx typedoc milvus --json` 可生成结构化清单(typedoc.json 现指向已失效旧路径,需修 entryPoints);`sdk.json`/`llms.txt` 不可用作清单。

### 8.2 云适用范围:两仓库的可程序化事实源

| 数据 | 来源 | 自动化 |
|---|---|---|
| 控制面接口存在性+集群类型+beta | zilliz-cloud `vdc/global/cloud-control-api/openapi.yaml`(`x-beta`、description "仅适用于 Dedicated"句式;`openapi-required-exceptions.json`;已有 `openapi-zdoc-compare.sh` 逆向对接 zdoc 的先例) | 全自动 |
| gRPC 方法云接受面 | `vdc/region/cloud-open-api/grpcproxy/proxy/milvus.go`(MilvusServiceServer 表面 ≈144 方法透明代理,文件含 ~145 个 func 声明;**无 per-method allowlist**,拒绝仅在认证/RBAC/StateMatrix/Milvus 版本三层) | 全自动 |
| 套餐/region/集群类型矩阵 | zilliz-cloud-config `milvus-instance/manifests/*.yaml`(`supportedRegions/category/maxCu`)、`classes/*.yaml`(`clusterTypes/enabled/onlyForWhiteList/regions`) | 全自动 |
| 实例状态×允许动作 | cloud-service `MetaController.java:799` stateMatrix | 全自动(结构) |
| **功能×集群类型×套餐×版本×云矩阵** | `function_white_list` 表(FunctionWhiteListDO:`dbVersionNum/instanceTypeRange/projectPlanRange/cloudRange/requiredMilvusParamName/Value`;另有 deny list)——**内容在运行库,仓库只有 schema** | 半自动(决策点 §5.10) |
| region 上线粒度/ON REQUEST/org 白名单 | `supportedRegions` 现全为 ALL;名单在 DB/ops | 人工兜底 |

overlay(共享页 page.yaml metadata)的字段组直接对齐 function_white_list schema:`{available, clusterTypes, minMilvusVersion, plans, regions, restrictions, beta}`。

### 8.3 五阶段管道与复用清单

```
S1 SDK 扫描     pin milvus-sdk-node tag/release → TS AST/typedoc 提取 ≈242 方法清单+签名+JSDoc 快照(别名去重)
S2 归属推理     硬信号规则 + web-content 存在性 join → A/C/缺口 三榜 + 人工兜底清单(ledger 记账)
S3 云适用范围   zilliz-cloud @ pin(openapi.yaml+grpcproxy 面) + zilliz-cloud-config @ pin(matrices) + white_list 数据通道
S4 overlay 初稿 shared-docs/node/ page.yaml(云适用范围字段组+beta)+ links.yaml + 暂缓接管名单(§5.9 评审结论回填)+ C 桶新页提案卡
S5 提案 PR      master draft PR(PAT+预算化正文+评审 checklist+evidence artifact+ledger append-only);merge=pin 移动+sync 再生成
```

直接复用 REST upstream 组件:`rest-upstream-drift-watchdog.yml` 只读骨架(schedule+dispatch plan+artifact always()+report card)、`rest-upstream-refresh.yml` 的 single-flight gate/PAT 开 PR/base_ref 白名单、`upstreamDiff/lock.js`+9-schema 契约布局、`ledger.js` append-only+`accounting.js` T4 gate、tag 扫描范式(`checkMilvusTrackCoverage` 改造为 SDK release/tag 扫描)、dispatch linkage(重读 master lock+24h backoff)、预算化 PR 正文生成器、lifecycle-evidence 的 inventory-sha256 模式、`shared-docs-pin-drift-watchdog.yml` 第二范式。

需要新写:TS 扫描器(vendored 无构建链依赖,仿 `milvus/extractor.go` 决策)、签名/JSDoc 快照 diff(类别仿 diff.js 的 category/changeKind+`substantiveDriftEntries` 过滤)、云仓库扫描器(openapi.x-beta 解析+grpcproxy 方法面+config 矩阵)、overlay emitter(`parsePageConfig` 校验+写入,core 现无写入侧)。

### 8.4 文件落点(仿 REST 布局)

- `.github/workflows/sdk-upstream-scan.yml`(每日 watchdog+dispatch)、`.github/workflows/sdk-upstream-refresh.yml`(single-flight+提案 PR)
- `scripts/sdk-upstream/`:`scan-watchdog.js`、`dispatch-refresh.js`、`decide-batches.js`(如需模型阶段)、`refresh-*-inventory.js`
- `packages/docs-tooling/src/reference/sdk/upstreamDiff/`:`lock/diff/ledger/accounting/staging/cli` + `sdkNode/`(TS 扫描器)
- `packages/docs-tooling/src/reference/sdk/meta/upstream/{sdk-upstream-lock.json, ledger.json, refresh-rules.json}` + `contracts/*.schema.json`
- 前置必读:`.claude/specs/2026-10-28-rest-upstream-pipeline-design.md`、`2026-10-29-rest-upstream-decisions-pipeline-design.md`、`runbook/rest-reference-pipeline.md`

### 8.5 架构级注意

1. 生成器写 shared-docs/node/ 时必须走既有 `parsePageConfig`/`planLock` 校验面,不得平行造 YAML 方言;overlay 的"云适用范围"字段组先在手册级 schema(§2)定义并进 config schema_version。
2. 静态扫描只能出 ~90% 结构;运行时事实(white_list 行数据、region 上线、org 白名单)以独立 data 文件叠加——与 zilliz-cloud-config 自身的 manifest↔override 分层天然同构。
3. 该工作流是 §3 各 WP 的长期替代/收编方向:WP-4 种子可由 S1-S4 首轮跑出后人工评审代替手写;Base 链接替换(WP-5)可由 S4 提案卡携带。
4. WP-4 的 page.yaml 字段组必须是 §8.2 overlay 字段组的子集,两处 schema 单源演进,禁止出现平行 YAML 方言(评审 P2-5)。
