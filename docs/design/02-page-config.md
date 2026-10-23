# 02 页面配置的读取与变换

`page.yaml` 的字段、变换的写法与规则、Cloud 内容文件能写什么，见[产品需求场景 3](../prd.md#场景-3接入一页)、[场景 4](../prd.md#场景-4写-cloud-的差异) 与[写法速查](../authoring-spec.md#3-pageyaml-的全部字段)。本篇定义 `shared-docs/` 放在哪里、工具怎样匹配和执行变换，以及完整的校验规则。工具生成的 front matter 见 [07](./07-site-adaptation.md)，链接与图片见 [02b](./02b-links-and-images.md)。

**参与方**：zdoc 生成（读取、校验与执行）。

**状态**：由原接口设计迁入，待工程维护者完善。

## 约定

### `shared-docs/` 的位置

`shared-docs/` 位于 zdoc 仓库根目录，在 master 分支上维护：所有修改都向 master 开 PR，合并后发布流程直接从 master 读取（见 [05](./05-publish-handoff.md#交接发生在哪里)）。

```
shared-docs/
  source.yaml                        # 共享来源配置：仓库与跟踪分支（见 04）
  Variables.json                     # Cloud 变量（见 03）
  links.yaml                         # 链接映射表（见 02b）
  product-names.yaml                 # 产品名检查规则（见 07）
  presentation/cloud-sdk-tabs.yaml   # 代码 Tabs 规则，工程维护
  pages/
    delete-entities/                 # 目录名即页面标识
      page.yaml                      # 页面配置，作者编写
      lock.yaml                      # 版本记录，工具写入（见 04）
    openai/
      page.yaml
      lock.yaml
      before-you-start.md            # Cloud 内容文件，按需提供
```

**页面标识**就是 `pages/` 下的目录名，必须等于这一页现有的 slug（如 `delete-entities` 对应 `/delete-entities`）。目录名只能用小写字母、数字和连字符。它怎样替代飞书 `token`、供翻译清单与路由插件使用，见 [05](./05-publish-handoff.md#页面身份token)。

### 变换的执行

#### 代码行的匹配

- **定位。** 只在目标代码组的目标语言中查找；`lines` 是一行或连续的几行，每行去掉行首缩进和行尾空格后比较，其余（包括行尾注释前的空格）必须完全一致，并且恰好出现一次。最多 5 行。
- **缩进。** 先去掉 `content.lines` 各行共同的行首空白，再在每行前加上原文中被替换或被定位的第一行的缩进，原样复制空格或 Tab；各行之间的相对缩进保留。新内容整体对齐到定位行，所以要选与新内容同一层级的行作定位。
- **不能有空行。** `lines` 与 `content.lines` 中都不能有空行，也不能有代码块的三个反引号或命名块标记。
- **超出范围就替换整种语言。** 一段代码中有多处不同，或连续超过 5 行，改为替换这种语言的代码。

#### 两遍生成与 `channel`

每次生成分两遍：第一遍用 `lock.yaml` 中 `current` 的原文，第二遍用 `next` 的原文，两遍使用同一份 `page.yaml`、Cloud 内容文件与 `Variables.json`（见 [04](./04-channels-and-lock.md#两个版本怎样合并成一页)）。不带 `channel` 的变换两遍都执行，在两版原文上都必须成立；`channel: current` 只在第一遍执行，`channel: next` 只在第二遍执行。提升时由工具删除 `channel: current` 的变换、去掉 `channel: next` 的标记（见 [04](./04-channels-and-lock.md#提升)）。

#### 其他规则

- 变换对 `publish` 中的所有手册都生效。SaaS 与 BYOC 之间的差异，用 Cloud 内容文件中 zdoc 现有的产品过滤写法表达。
- 同一位置有多条 `add` 时，按列表顺序输出。
- 目标的类型由原文结构决定，不由文件名决定；动作只由配置决定。
- Cloud 内容文件插入原文后，和原文一起往下处理：展开变量与片段、产品过滤，最后在站点适配中转换为 Cloud 组件；用到的变量和片段一并记入依赖。

## 出错时

工具先校验全部配置，再生成页面。以下情况该页生成失败，不会静默跳过：

| 类别 | 生成失败的情况 |
|---|---|
| 页面与字段 | `page.yaml` 不是合法的 YAML；页面目录名不符合 slug 规则；缺少必填字段；未知的字段、动作或 `schema_version`；`source.file` 在 lock 记录的 commit 中不存在；`publish[].manual` 不是 zdoc 已有的手册；Phase 1 中 `publish[].path` 在该手册中没有飞书节点生成的页面；`metadata.beta` 不是[产品需求](../prd.md#场景-3接入一页)列出的可选值（zdoc 遇到不认识的值会不显示标签、也不报错，所以在生成前拦下） |
| 变量表 | `Variables.json` 不是合法的 JSON、顶层不是对象，或同一层中有只差大小写的两个键；这时所有共享页都生成失败 |
| 目标 | 目标命名块、语言或内容文件不存在；内容文件路径指向页面目录之外 |
| `position` 与内容 | 在块旁或代码行旁 `add` 时没写 `position`；给代码组增加语言、`replace` 或 `remove` 时写了；`remove` 提供了内容 |
| 冲突（同一个通道中） | 同一个目标被多次变换；整块的 `replace` 或 `remove` 与该块的语言项变换、前后增加同时出现；语言项的 `replace` 或 `remove` 与该语言内的行级变换同时出现；同一语言内两条行级规则定位的行有重叠。不带 `channel` 的规则同时计入两个通道 |
| `channel` | 不是 `current` 或 `next`；页面在该通道中不存在（飞书表格中为 `NEXT` 的页面写了 `channel: current`） |
| 代码行 | `lines` 在目标语言中找不到、出现多次或超过 5 行；`lines` 用在没有 `language` 的目标上；`lines` 或 `content.lines` 中有空行 |
| 内容文件与 Tabs | 内容文件中出现命名块标记或手写的 Tabs；试图对本轮刚插入的内容再做变换；删除了 Tabs 规则要求必须存在的语言或默认语言 |

链接与图片的错误见 [02b](./02b-links-and-images.md#出错时)，变量与片段的错误见 [03](./03-md2md-interfaces.md#出错时)，生成结果被手动修改见 [05](./05-publish-handoff.md#发布保护)。

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么放在 `shared-docs/`。** zdoc 规定 `content/`、`generated/` 等目录归 dev 分支，只由发布工作流写入；人编写的文件走 master，经同步 PR 进入 dev。共享页的配置由人编写，所以放在 `content/` 之外、归 master 管理的新目录中。

**产品过滤沿用现有能力。** zdoc 的产品过滤（zilliz、saas、paas、milvus 等目标）在 Fetch 阶段执行。共享原文不写产品指令；Cloud 内容文件迁入 Git 后仍可使用现有写法，处理对象从飞书输入扩展到 Git 输入。

产品上的取舍（页面标识、按手册发布、只开放三项元数据、代码行差异写在 zdoc、`channel`、Cloud 内容文件的写法）见[产品需求场景 3](../prd.md#场景-3接入一页)、[4](../prd.md#场景-4写-cloud-的差异)、[6](../prd.md#场景-6让内容先只在-uat-显示)。

</details>

## 验收

- **T04**：内容变换的目标存在性、类型、语言和冲突检查；以 OpenAI 的凭证参数为真实用例验证代码行的 replace 与 add。
- **T06**：MDX、路由与 front matter 正确。
- **T13**：不适用的内容被过滤；通道相关部分见 04。
