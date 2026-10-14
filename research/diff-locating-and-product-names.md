# 差异定位与产品名：主流做法调研

调研日期：2026-10-13。回答第一次对齐会留下的两个问题：Cloud 怎样定位要替换的 Milvus 原文，以及产品名能否不在 milvus-docs 中写成变量。本文只整理做法和数据，不做选择；方案另写。

## 1. 速览

- **定位有四类做法**：在原文里加标识、按文档结构找、按原文文字找、按行号找。成熟的内容复用工具默认用第一类；按结构找只在 OpenAPI 这类结构固定的文档中常见，没有找到长期按标题路径维护 Markdown 下游差异的案例。
- **milvus-docs 一年内**有 17% 的共享候选页标题被改名或删除，按结构找需要应对这一点。
- **产品名有三种做法**：上游写变量、下游替换、两者结合。开源上游加商业产品的成熟案例都在上游写变量；下游替换只在代码迁移工具中常见。
- **milvus-docs 中**单纯指产品的 “Milvus” 有 1128 处；抽样 40 处，直接替换有 24 处正确，其余都在 Cloud 不共享或要整节替换的内容里。

## 2. 差异定位

例子统一用 OpenAI 页：Cloud 要整节替换 “Configure credentials”，并把 Step 2 代码中的 `# "credential": "apikey_dev", …` 一行换成 `"integration_id": "YOUR_INTEGRATION_ID",`。示例中的 zdoc 字段名只是示意。

| 做法 | 怎么做 | 谁在用 | Milvus 原文中 | 出错时 |
|---|---|---|---|---|
| A. 加标识 | 在原文中给要处理的部分起名字（成对注释，或标题末尾的 ID），下游按名字找 | [AsciiDoc 标签](https://docs.asciidoctor.org/asciidoc/latest/directives/include-tagged-regions/)、[Couchbase](./downstream-composition-evidence.md)、[DITA](./shared-blocks-and-zdoc-consumption.md#23-dita成熟的命名引用与外部块替换机制)、[MkDocs Snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)、[Docusaurus 标题 ID](https://docusaurus.io/docs/markdown-features/toc) | 可见（注释） | 标识被删时报错 |
| B. 按结构找 | 下游写“哪个标题下的第几个 Python 代码块” | [OpenAPI Overlay](https://spec.openapis.org/overlay/v1.0.0)、[Kustomize](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/)、[remark-toc](https://unifiedjs.com/explore/package/mdast-util-heading-range/) | 不可见 | 找不到时报错；**也可能找到别处而不报错** |
| C. 按文字找 | 下游写出要处理的那几行，或起止处的文字 | [Sphinx `start-after`](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html)、[`patch`](https://www.gnu.org/software/diffutils/manual/html_node/Inexact.html)、[Copybara](https://github.com/google/copybara/blob/c99cac4a2ed7840d71da8590753e3f81020af501/docs/reference.md#corereplace)、本项目现有的 `lines` | 不可见 | 精确匹配时报错；模糊匹配可能放错位置 |
| D. 按行号找 | 下游写第几行到第几行 | Asciidoctor `lines`、Sphinx `:lines:` | 不可见 | 不报错，直接错位（不考虑） |

<details>
<summary>A. 加标识：示例</summary>

成对注释（现方案的命名块）。Milvus 原文：

```markdown
<!-- doc:block:start id="configure-credentials" -->
## Configure credentials
…
<!-- doc:block:end id="configure-credentials" -->
```

或者只在标题末尾加 ID（Docusaurus 的写法，标题改名或翻译后 ID 不变）：

```markdown
## Configure credentials <!-- #configure-credentials -->
```

zdoc 页面配置按名字引用：

```yaml
- operation: replace
  target: {module: openai, block: configure-credentials}
  content: {file: configure-credentials.md}
```

| 上游改动 | 结果 |
|---|---|
| 标题改名 | 照常生效 |
| 有人删掉了注释 | 上游更新 PR 报错 |

</details>

<details>
<summary>B. 按结构找：示例</summary>

Milvus 原文不变。zdoc 页面配置：

```yaml
- operation: replace
  target: {module: openai, section: ["Configure credentials"]}
  content: {file: configure-credentials.md}

- operation: replace
  target:
    module: openai
    section: ["Use embedding function", "Step 2: Add embedding function to schema"]
    code: python
    index: 1                     # 这一节的第 1 个 Python 代码块
    lines: '# "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml'
  content: {lines: '"integration_id": "YOUR_INTEGRATION_ID",'}
```

| 上游改动 | 结果 |
|---|---|
| “Configure credentials” 改名 | 报错，要改规则 |
| 标题加上版本徽标 `\| Milvus 3.0.x` | 匹配前去掉徽标则照常生效 |
| Step 2 原有代码前插入一个新的 Python 代码块 | `index: 1` 指向新代码块；写了 `lines` 会报错，整块替换则**静默替换掉新代码块** |

</details>

<details>
<summary>C. 按文字找：示例</summary>

Milvus 原文不变。zdoc 页面配置：

```yaml
- operation: replace             # 从这个标题到下一个标题之前
  target: {module: openai, from: '## Configure credentials', to: '## Use embedding function'}
  content: {file: configure-credentials.md}

- operation: replace             # 整页中必须恰好出现一次
  target: {module: openai, lines: '# "credential": "apikey_dev",               # Optional: Credential label specified in milvus.yaml'}
  content: {lines: '"integration_id": "YOUR_INTEGRATION_ID",'}
```

| 上游改动 | 结果 |
|---|---|
| “Use embedding function” 改名，或这一行被改 | 报错，要改规则 |
| 同样一行出现在别处 | 报错：出现多次 |

</details>

**要点。** 几种做法都会坏，区别在坏的方式：A 被删时一定报错；B 可能找到一个错的位置而不报错，和 `patch` 的模糊匹配是同一类风险。选 B 的话，需要记下被定位内容的指纹，上游变化时提示审核。

### 2.1 milvus-docs 实测

范围：`v3.0.x`（`86a5df11`）的 `userGuide` 与 `embeddings`，共 214 页；改动统计为过去一年的 119 个 commit。[脚本与结果](./evidence/milvus-docs-structure/)

| 指标 | 结果 | 对 B 的影响 |
|---|---|---|
| 一年内标题被实际改名或删除的页面（已排除大小写、版本徽标等差异） | 36 页（17%） | 这些页上指向旧标题的规则要修改 |
| 带版本徽标的标题，如 `… \| Milvus 2.6.11+` | 44 个 | 匹配前要去掉徽标 |
| 有重名标题的页面 | 6 页 | 只写标题无法区分 |
| 同一节有多个代码组的页面 | 26 页 | 要写序号，插入新代码组后会错位 |

统计期包含 3.0 的大规模改写，日常频率可能更低；OpenAI 试点页本身一年内没有改动。

### 2.2 可选组合（不是结论）

| 组合 | Milvus 原文中 | 需要补的 |
|---|---|---|
| A1. 命名块（现方案） | 每处一对注释 | 无 |
| A2. 标题 ID + 代码用 `lines` | 只在要替换的标题加 ID | 核实 milvus.io 与 md2md 是否支持标题 ID |
| B. 按结构找，命名块兜底 | 默认无标记 | 标题规范化、唯一性检查、内容指纹 |
| C. 按文字找 | 无标记 | 起止文字精确匹配 |

都需要：规则找不到目标时在上游更新 PR 中报错。

**待核实**：milvus.io 能否处理标题 ID；大约多少页需要节级或代码级差异；用过去一年的历史回放，比较各组合要改几次规则、有无静默定位错误。

## 3. 产品名

例子统一用 OpenAI 页的 “The Function module in Milvus automatically converts raw data …”。

| 做法 | 怎么做 | 谁在用 | Milvus 原文中 |
|---|---|---|---|
| P1. 上游写变量 | 原文写变量，Milvus 与 Cloud 各给一个值 | [OpenShift](https://github.com/openshift/openshift-docs/blob/56cb75ee08ee2dbd6bf38a90ff2d29b9ed22ebdd/contributing_to_docs/doc_guidelines.adoc#product-name-and-version)、[Keycloak](https://github.com/keycloak/keycloak/blob/f5055043072a3e8e2ee958ab5d7ee09b759ba893/docs/documentation/topics/templates/document-attributes.adoc)、[Infinispan](https://github.com/infinispan/infinispan/blob/85994e3da61628c2e49f8bb1e5976301a3b64d14/documentation/pom.xml#L308) | 看到变量名 |
| P2. 下游替换 | 原文照常写，zdoc 生成时按规则把 “Milvus” 换成 “Zilliz Cloud” | [Copybara](https://github.com/google/copybara/blob/c99cac4a2ed7840d71da8590753e3f81020af501/docs/reference.md#corereplace)（代码迁移）；会上提到的 SDK Reference 计划 | 无变化 |
| P3. 两者结合 | 以 P2 为主；只换名字仍不对的句子，用第 2 节的方式整节替换 | — | 无变化 |

Keycloak 的三份主要指南中，约 98% 的产品名写成了变量，主要靠审核维持（[统计](./evidence/milvus-docs-structure/keycloak-attribute-usage.md)）。

<details>
<summary>P1. 上游写变量：示例</summary>

Milvus 原文：

```markdown
The Function module in {{var.product_name}} automatically converts raw data …
```

milvus-docs 的 Variables.json 写 `"product_name": "Milvus"`，zdoc 的写 `"product_name": "Zilliz Cloud"`。有人新写 “Milvus supports …” 没用变量时，上游更新 PR 的检查会提示。

</details>

<details>
<summary>P2. 下游替换：示例</summary>

Milvus 原文不变。zdoc 的全站规则：

```yaml
term_replacements:
  - find: Milvus
    replace: Zilliz Cloud
    scope: prose                 # 不碰代码块、行内代码、链接
    skip_when_followed_by: [Lite, Standalone, Distributed, Operator, Helm, Backup, CDC, '\d']
    skip_words: [pymilvus, PyMilvus, MilvusClient, milvus.yaml, milvus.io]
```

| 原文 | 结果 |
|---|---|
| The Function module in Milvus … | 换成 Zilliz Cloud，正确 |
| Requires Milvus 2.6.20 or later. | 不替换；这句对 Cloud 本来就要另写 |
| Milvus must know your OpenAI API key … | 字面通顺，但在 “Configure credentials” 节里，Cloud 会整节替换 |

</details>

### 3.1 milvus-docs 实测

| 正文中的 “Milvus”（代码块外） | 次数 | 能否直接替换 |
|---|---:|---|
| 单纯的产品名 | 1128（190 页） | 大多可以 |
| 包名、配置文件、URL，如 `pymilvus`、`milvus.yaml` | 519 | 不能 |
| 版本、产品形态、标题徽标，如 Milvus 2.6、Milvus Lite | 189 | 不能 |

另有 3699 处在代码块中。Variables.json 目前没有产品名变量。

抽样 40 处，直接换成 “Zilliz Cloud”（[明细](./evidence/milvus-docs-structure/product-name-sample.md)）：

- 24 处正确；
- 8 处在 CDC、Backup 等 Milvus 专属页面；
- 8 处在部署、凭证配置段落，这些正是 Cloud 要整节替换的部分。

### 3.2 对比（不是结论）

| | Milvus 原文中 | 前期工作 | 主要风险 |
|---|---|---|---|
| P1 | 写 `{{var.product_name}}` | 约 1100 处改成变量（可脚本批量） | 作者漏写 |
| P2 / P3 | 无变化 | 写替换规则与排除规则 | 误替换；新写法需补规则 |

都需要：保留上游更新 PR 中的“残留 Milvus 写法”检查。

**待核实**：在三篇试点页上跑 P2 规则，与 Cloud 线上页面逐句对比；`localhost:19530` 等其他词是否也适合全站替换。

## 4. 边界

- 公开源码固定到 commit，网页按 2026-10-13 的内容引用；检索没找到不代表不存在。
- milvus-docs 统计只读取 Git 对象，分类是启发式规则；抽样由人工判断，样本 40。
- 示例中的 zdoc 字段名是示意，没有定稿。
