# 共享内容消费配置（草案）

**状态：草案，用于说明设计和驱动本地样例，不是定稿接口。** 字段名、文件位置和目录布局将在实现设计中与 zdoc 维护者共同确定，并与 zdoc 现有的手册注册、front matter 和导航配置对齐。本次方向对齐只需确认下面的概念约束。

## 0. 需要对齐的概念约束

- 只按整页或源内命名块定位；不使用行号、正则、文本搜索或标题选择器。
- 内容变换只有 add、replace、remove 三种动作，另可把命名块包进 `<NextChannel>`；不按业务类型增加专用操作。
- 变量沿用 md2md 的 `Variables.json` 与 `{{var.xxx}}`；缺少 Cloud 绑定时报错，不静默使用 Milvus 的值。
- 代码行的产品差异沿用 zdoc 的产品行指令，写在共享代码中，不通过配置表达；段落与章节差异不在共享原文中写条件。
- 生成文件不作为编辑源。
- 作者成本：每个共享页一份页面配置，差异片段按需提供，共用规则在站点范围维护一次。

## 待与 zdoc 维护者共同确定

| 问题 | 现状与考虑 |
|---|---|
| 链接与图片映射 | 样例在每页配置中手工维护 `links`、`assets`，页数增多后成本线性增长；可考虑由 registry 推导或站点级规则 |
| 页面元数据 | 样例的 `metadata` 与 zdoc 现有 front matter、导航配置重复；应挂接现有手册注册，而不是重新定义 |
| 注册文件 | `shared/modules.yaml` 让文件改名时模块 ID 不变，但多一个共用文件；试点阶段是否可以简化 |
| lock 粒度与跟踪分支 | 每页独立采用还是全仓统一；Cloud 跟踪哪个 Milvus 版本分支 |
| 发布通道 | 整页通道目前在飞书多维表格的 `Release Channel` 字段中维护，迁移后在 Git 中的位置（例如页面配置）；命名块包裹的写法；Git 页面的整页通道如何传递到译文 |

以下内容记录本地样例使用的草案字段。实际配置见 [Filtered Search](../examples/filtered-search/zdoc/filtered-search.page.yaml)，作者操作见[样例说明](../examples/filtered-search/walkthrough.md)。[Delete Entities](../examples/delete-entities/zdoc/delete-entities.page.yaml)使用相同版本的整篇消费子集。架构与发布要求见[架构设计](./architecture.md)，实施验收见[首期方案](./phase-1.md)。

`schema_version` 标识配置格式，样例为 `1`，与 Milvus 产品版本无关；不支持的版本应明确报错。

## 1. 首期范围

处理顺序是：整篇引用 → 产品变量绑定 → 必要的内容变换 → 站点展示适配。只有需要被变换的位置才要求稳定命名。

| 首期能力 | 用途 | 当前验证状态 |
|---|---|---|
| 整篇引用 | 正文标题、内容与代码保持一份来源 | 两篇样例已演示 |
| 产品变量绑定 | 产品名、endpoint、token 等值差异 | 三变量、两产品已演示 |
| 在命名块前后增加 Markdown | 前置条件、提示、限制说明、普通段落 | 通用 add 的本地测试通过 |
| 替换命名 Markdown 块 | 产品说明或步骤内容不同 | 通用 replace 的本地测试通过 |
| 删除命名块 | 消费方不适用的段落或完整代码组 | 通用 remove 的本地测试通过 |
| 增加、替换、删除代码组中的语言项 | CLI 或其他语言示例的覆盖差异 | 三个动作均有本地测试；实际页只使用 add |
| 用 `<NextChannel>` 包裹命名块 | 共享内容中 Cloud 尚未上线的部分 | 首期工程目标；样例未覆盖 |

代码行的产品差异（如 `credential` 与 `integration_id`）不在本配置中表达，而是在共享代码中使用 zdoc 产品行指令，见[架构设计](./architecture.md#代码行产品指令)。

不同业务内容不对应不同 operation。没有 add_cli、add_prerequisite、replace_credentials 等专用操作。

首期暂不新增：

- 行号、正则、文本搜索、标题 selector；任意 AST/DOM 路径或数组下标定位。
- 代码子区域替换和任意代码行插入。行级差异使用产品行指令；差异较多时替换整个语言项。
- move/copy、任意嵌套变换，以及继续寻址本轮刚插入的内容。
- 变量表达式、循环、条件模板、把整段代码塞进 JSON 变量。
- 动态执行脚本生成内容、任意插件式 operation、自动判断 SDK/CLI 语义等价。
- 独立页面框架语言；多来源编排保留为扩展路径，当前两篇样例不覆盖。

这限定的是本次消费 schema 的新增范围，不删除已确认的内容保护、翻译、锁定和发布设计。

## 2. 变量统一叫 Variables.json

```text
milvus-docs/site/en/Variables.json    Milvus 默认值，沿用现有位置
zdoc/Variables.json                  Cloud 绑定，本例的消费配置根目录
```

大小写沿用已核对的 Milvus 文件名。两边都是同一种 JSON 键值结构；目录不同只是仓库布局不同。真实 zdoc 接入可放到确定的内容根目录，通过下面的配置明确读取位置：

```yaml
variables:
  file: Variables.json
```

`variables.file`、`content.file`、`presentation.code_groups` 均相对于 zdoc 消费配置根目录解析。首期不引入按 SDK 覆盖、递归搜文件或多层隐式继承。

共享原文沿用 md2md 的 `{{var.product_name}}`、`{{var.example_endpoint}}`、`{{var.example_token}}`。同一产品各语言共用连接值。新增变量需要更新源默认值、导出契约与消费方绑定；缺失绑定必须报错，不能静默使用另一个产品的默认值。

共用变量变更要检查所有依赖页面。跨页影响索引、锁定与审核属于 CI 接入工作；本地示例只记录本页依赖摘要。

## 3. 统一字段与三个动作

```yaml
schema_version: 1
page: cloud.filtered-search
source:
  take: page
  module: filtered-search
variables:
  file: Variables.json
transforms:
  - operation: add
    target:
      module: filtered-search
      block: standard-filtering-code
      language: shell
    content:
      file: fragments/filtered-search/standard-filtering-cli.md
```

| 字段 | 作用 |
|---|---|
| operation | 做什么：固定为 add、replace、remove |
| target.module | 共享模块 ID |
| target.block | 原文中的命名块 ID |
| target.language | 可选；进一步指定代码组内的语言项 |
| position | 仅在命名块旁 add 时使用：before 或 after |
| content.file | 新增或替换内容的文件；remove 不允许提供 |

模块 ID 在同一 registry 内唯一，块 ID 在模块内唯一，语言键在代码组内唯一。目标类型由源结构/registry 判定，不由 writer 随意指定。

内容片段统一放在中性命名的 `fragments/` 中，新增和替换都能引用。目录名不决定操作行为，YAML 才决定。

### add：新增内容

在一个命名块前增加普通 Markdown：

```yaml
transforms:
  - operation: add
    target:
      module: some-guide
      block: setup
    position: before
    content:
      file: fragments/some-guide/cloud-prerequisites.md
```

同一个操作可增加前置条件、说明、列表或含代码围栏的 Markdown。改成 `position: after` 就放在该块之后。源中必须存在 setup 的命名标记，工具不根据标题猜位置。

给代码组增加语言项，则提供 `target.language`，不提供 position；语言顺序由展示规则决定。Filtered Search 的 CLI 补充使用同一个 add 操作。

### replace：替换已有内容

```yaml
transforms:
  - operation: replace
    target:
      module: some-guide
      block: product-notes
    content:
      file: fragments/some-guide/cloud-product-notes.md
```

- Markdown 块：文件提供完整替换 Markdown。
- 语言项：target 再加 language，文件包含一个匹配语言的完整代码围栏。
- 完整代码组：文件提供完整组结构，再执行相同的语言校验。

### remove：删除已有内容

```yaml
transforms:
  - operation: remove
    target:
      module: some-guide
      block: product-notes
```

删除语言项时再指定 target.language。不提供内容文件，也不使用空文件表达删除。它只改变 Cloud 输出，不修改 Milvus 原文。

如果不再需要 Cloud 自己补入的 CLI，直接删掉那条 add 配置即可，不再追加一条 remove。

删除代码组不会自动删除其外面的标题或说明；作者应命名完整语义边界，并预览结果。正式站点检查还需发现悬空链接和锚点。

## 4. 固定校验与执行规则

1. 所有目标相对于同一份锁定原文解析。当前整篇模式只允许本页 source.module；多来源页面框架不在此本地示例范围。
2. 先校验全部配置，再合成。未知动作/字段、块缺失、语言不匹配、文件缺失都报错。
3. add 语言时该键必须不存在；replace/remove 时必须存在。不会静默覆盖。
4. 同一目标不能重复变换。整块 replace/remove 不能同时与该块的语言项变换或前后插入组合，冲突直接报错。
5. 同一块旁允许多次 add，同一方向按 YAML 列表顺序输出。Tab 顺序始终由展示规则决定。
6. 新插入内容不会成为本轮可寻址目标，不执行变换链。片段不能再引入命名标记或手写 Tabs；首期不支持在普通 add 片段中嵌套一个新 multipleCode 组。
7. 删除站点规定必须保留的语言或默认语言时构建失败。确有产品范围要求时，应审核相应展示规则，不生成空 Tab。
8. 新增/替换片段也参与变量绑定与依赖摘要。源块或片段变化需要升级审阅；摘要变化不能证明各语言语义仍一致。
9. 生成文件不作为编辑源。重新构建比对与正式发布门禁沿用既定设计，本地 receipt 不构成发布授权。

## 5. Filtered Search 的落地边界

实际页面只需要两条 add，将两份 CLI 补进两个命名代码组。普通段落和语言项的 replace/remove 在独立测试中验证，没有为了演示而往真实文章增加差异。

构建器应明确拒绝不支持的版本和未知字段。语言展示规则、链接映射、图片适配和站点元数据仍各有明确配置，不扩展成正文专用 operation，也不重写既有发布或翻译机制。

变量文件、片段路径和消费 YAML 已统一，两篇样例均提供可重建的 Cloud MDX 和检查脚本。当前本地验证覆盖 Markdown 块和语言项；通道包裹、代码行指令过滤、真实 md2md/Docusaurus/SDK/CLI 构建运行、跨仓升级和生产门禁仍需工程实现或验证。

站点展示规则由工程维护者共用维护。两篇样例使用相同的 `cloud-sdk-tabs.yaml`：语言项以 `required` 声明是否必须存在；可选语言只在页面提供内容时显示，默认语言必须存在。Cloud 的页面标题、导航标签和路由由 `metadata` 配置，正文标题与章节结构随共享原文引用。
