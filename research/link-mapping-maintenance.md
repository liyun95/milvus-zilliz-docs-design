# 链接映射表的维护方式：调研

调研日期：2026-10-21。回答 PRD 评审会上文档负责人提出的问题：链接映射表 `links.yaml` 靠人工维护难、容易出错，而 zdoc 一轮构建要一两个小时，出错代价高。本文只整理做法和数据，不做选择。

数据：milvus-docs `v3.0.x` 的 [`9acdc99`](https://github.com/milvus-io/milvus-docs/tree/9acdc99959e188a54be1df512ea3806c3110ef59)（2026-10-20），User Guide 共 201 篇（`site/en/userGuide/`，含 Embeddings）；zdoc dev 的 [`10d6bd8`](https://github.com/zilliztech/zdoc/tree/10d6bd8)（2026-10-21），英文 Guides 共 390 篇。脚本见 [evidence/links-and-anchors](./evidence/links-and-anchors/)。

## 1. 速览

- **问题拆成三件事**：要登记多少（量）、登记错了怎样发现（准）、什么时候发现（早）。
- **量**：User Guide 中 837 个站内链接指向 181 个不同的 Milvus 页面。只靠同名页面，能自动对上 60 个（33%），其余 121 个要人登记。再用“标题相同”和“从飞书现有页面反推”，能自动对上 116 个（64%），覆盖 75% 的链接；剩下 65 个。
- **新增的量**：一年内 User Guide 新出现了 49 个链接目标，约每月 4 个；最近 3 个月是 3.0 发版期，新增 27 个。
- **准**：三种自动来源两两比较，结果都对得上的有 51、56、98 个目标，没有一个不一致。相似度匹配大多给错。
- **早**：链接在 PR 校验中解析，错误在合并前报出。合并后才暴露的只有一种情况：Cloud 的目标页在飞书中改名或删除。
- **剩下的 65 个**：27 个是自部署、运维与配置，16 个是索引类型，Cloud 大多没有对应页；另外 22 个中，有几个在 Cloud 上有名字不同的对应页。

## 2. 自动查找的来源

“目标”指链接指向的 Milvus 页面（按文件名去重），“链接”按出现次数计。

| 来源 | 怎么做 | 覆盖目标 | 覆盖链接 | 准确性 | 局限 |
|---|---|---|---|---|---|
| 同名页面（PRD 现有第 3 步） | Milvus 文件名去掉 `.md`，等于 Cloud 页面的 slug | 60/181（33%） | 289/837（34%） | 与另两种来源比较，全部一致 | 两边的名字因历史原因大多不同 |
| 标题相同 | Milvus 页面的 `title` 与 Cloud 页面的标题（去掉 `\| Cloud`，忽略大小写与标点）相同，且 Cloud 只有一页是这个标题 | 107/181（59%） | 573/837（68%） | 与反推比较 98/98 一致，与同名比较 56/56 一致 | 任一边改标题，结果就会变；Cloud 有两页同标题时不用 |
| 从飞书现有页面反推 | 先找到 Milvus 页面对应的 Cloud 页面（同名或同标题），再在两页中找链接文字相同的链接，Cloud 那一侧的目标就是映射 | 105/181（58%） | 606/837（72%） | 与同名比较 51/51 一致；3 个目标的反推结果不唯一，按多数取 | 167 篇有链接的 Milvus 页面中，只有 109 篇找得到 Cloud 对应页；链接文字两边要相同；页面迁出飞书后，飞书版不再更新，只能作为一次性的来源 |
| 相似度匹配 | 按标题或文件名的字符相似度，取最接近的 Cloud 页面 | — | — | 抽查大多错误，例如 `hnsw.md` → `chinese-analyzer`、`ivf-pq.md` → `zilliz-ai-prompts` | 只能作为人工判断时的线索 |
| 三种合计（同名、标题、反推） | 任一种找到即可 | 116/181（64%） | 629/837（75%） | 见上 | 剩 65 个目标、208 个链接 |

<details>
<summary>反推的例子：Delete Entities</summary>

Milvus 原文：`For more information about filter expressions, please refer to [Filtering Explained](boolean.md)`。Cloud 现有页面 `delete-entities`（与 Milvus 同名）在同一处写着 `[Filtering Explained](./filtering-overview)`。链接文字相同，所以得到 `boolean.md` → `filtering-overview`。两边页面的标题也都是 “Filtering Explained”，标题来源给出同样的结果。

</details>

## 3. 剩下的 65 个目标

| 类别 | 目标数 | 例子 | Cloud 的情况 |
|---|---|---|---|
| 自部署、运维与配置 | 27 | `configure-docker.md`、`configure-helm.md`、`install_cluster-helm.md`、`birdwatcher_usage_guides.md`、`cdc_failover.md` | 多为 Cloud 不提供的能力；链接常在 Cloud 要替换的段落中，例如 OpenAI 页的 `configure-docker.md` |
| 索引类型 | 16 | `ivf-flat.md`（14 个链接）、`hnsw.md`（12）、`diskann.md`、`gpu-cagra.md` | Cloud 用 AUTOINDEX，没有逐个索引类型的页面 |
| 其他 | 22 | `embedding-function-overview.md`、`limitations.md`、`manage_databases.md`、`snapshot-use-cases.md`、`tei-ranker.md`、`eviction.md`、`warm-up.md` | 有的在 Cloud 上有名字不同的对应页，例如 `limitations.md` 对应 Zilliz Cloud Limits（`limits`），`manage_databases.md` 对应 Database Explained（`database-concept`）；有的 Cloud 没有对应功能，例如 TEI、vLLM 等模型 Ranker |

这 65 个目标的链接共 208 个，占全部的 25%。

## 4. 维护方式的选项

### 4.1 映射从哪里来

| 选项 | 怎么做 | 需要人登记的目标（全部迁移时） | 之后的维护 | 会不会静默出错 |
|---|---|---|---|---|
| A. 现状 | 构建时按共享页、`links.yaml`、同名页面的顺序查找，查不到就失败，人补一行 | 121 | 每个新目标查不到时补 | 不会：查不到就失败 |
| B. 构建时加“标题相同” | A 的第 3 步之后再按标题查 | 70 | 同上 | 会：任一边改标题，映射可能悄悄变成另一页，只在上游更新 PR 的差异中能看到 |
| C. 一次性生成候选表 | 用同名、标题、反推生成一份 `links.yaml` 候选，人审一遍后提交；构建时仍按 A 查找 | 一次审 116 条候选，再补 65 条 | 新目标约每月 4 个，查不到时补 | 不会：映射写在表中，改动经过 PR |
| D. 只在补表时提示候选 | 构建时仍按 A；查不到而失败时，报错中附上标题与反推给出的候选 | 121，但大多只需确认候选 | 同上 | 不会 |

### 4.2 查不到时怎么办

| 选项 | 怎么做 | 影响 | 与 PRD 现有原则 |
|---|---|---|---|
| E. 失败（现状） | 这一页生成失败，提示补表 | 作者必须处理；65 个目标中的链接都会拦下 | 一致：“处理不了的一律报错” |
| F. 降级为指向 milvus.io | 自动改成 `https://milvus.io/docs/<文件名>`，在 PR 报告中列出，不失败 | 不拦人；但“其他”类中有 Cloud 对应页的，也会被指到 milvus.io，只有读报告的人才会发现 | 不一致，要改原则 |
| G. 按类别降级 | 目标在 Milvus 的自部署、运维、配置等目录下时降级，其余仍失败 | 拦下的少了一部分（上文 27 个中的多数） | 部分一致；要维护“哪些目录可降级”的清单 |
| H. 去掉链接、保留文字 | 查不到时只输出链接文字 | Cloud 页面不指向 milvus.io；读者少了一个入口 | 不一致，而且信息会丢失 |

“Cloud 页面能否链接到 Milvus 站点”仍是 PRD 第 7 节的待确认事项，选项 F、G 都以“可以”为前提。

## 5. 出错的时机

| 出错的情形 | 在哪里发现 | 会不会白等一轮构建 |
|---|---|---|
| 共享页中出现新的、查不到的链接（作者修改、接入、上游更新） | PR 校验：只生成共享页，不跑整站构建 | 不会，合并前就报出 |
| 映射表中写的 Cloud 页面不存在 | 可以在 PR 校验中按 dev 上现有的页面清单检查；读哪份清单仍待确定（[技术设计 02b](../docs/design/02b-links-and-images.md#链接)） | 不会 |
| Cloud 的目标页在飞书中改名或删除，映射因此失效 | 合并后的 Fetch：飞书侧的改动不经过 zdoc 的 PR | 会：Fetch 到这一步才发现；按 PRD 9-1，这一页保留现有版本，其他页面照常发布 |

最后一种情形，任何选项都会遇到；区别只在于发现后是失败（E）还是降级（F、G）。

## 6. 试点页

| 页面 | 站内链接 | A（现状） | 加上标题与反推之后 |
|---|---|---|---|
| Delete Entities | `boolean.md` | 要在 `links.yaml` 中登记 | 标题与反推都给出 `filtering-overview`，结果一致 |
| Filtered Search | `primary-key-search.md`；`filtering`（漏写 `.md`） | 第一个同名，自动对上；第二个报错，内容对齐时回上游改 | 同左 |
| OpenAI | `embedding-function-overview.md`；`configure-docker.md` | 第一个要登记，三种来源都找不到；相似度匹配给出的候选是 Function Overview（`function-and-model-inference-overview`），未核实；第二个在被替换的一节中，不处理 | 同左 |

## 7. 方法

- **Milvus 侧**：读 `site/en/userGuide/` 下全部 `.md`，去掉代码块，取 `[文字](目标)` 形式、目标以 `.md` 结尾且不以 `http` 开头的链接；页面标题取 front matter 的 `title`。
- **Cloud 侧**：读 zdoc dev 的 `content/en/guides/`，slug 与标题取 front matter，链接取以 `./` 开头的站内链接。
- **新增目标**：比较 `9acdc99` 与 `v3.0.x` 上 2025-10-21、2026-04-21、2026-07-21 之前的最后一个提交，统计 User Guide 中链接目标的差集。
- 标题比较前转小写，并把非字母数字字符换成空格。反推按链接文字比较，文字相同的链接可能不止一个，取票数最多的目标。
- 各页的 Cloud 对应关系只用同名与同标题判断，没有人工核对；三种来源互相一致，说明误配很少，但不能证明没有。

<details>
<summary>运行脚本</summary>

```bash
# 在 milvus-docs 中取得上游提交
git -C ~/milvus-docs fetch https://github.com/milvus-io/milvus-docs.git v3.0.x
# zdoc dev 的英文 Guides（按需克隆，约 6 MB）
git clone --filter=blob:none --no-checkout --depth 1 --branch dev https://github.com/zilliztech/zdoc.git zdoc-dev
git -C zdoc-dev sparse-checkout set --no-cone '/content/en/guides/'
git -C zdoc-dev checkout dev

python3 research/evidence/links-and-anchors/linkmap.py ~/milvus-docs 9acdc99959e188a54be1df512ea3806c3110ef59 zdoc-dev/content/en/guides
```

`churn.py` 统计新增目标，`anchors.js` 是锚点换算的统计（见[技术设计 02b](../docs/design/02b-links-and-images.md#锚点)），需要 `slugify@1.6.6`。

</details>
