# 03 md2md 提供的接口

zdoc 与 Milvus CI 处理命名块、展开变量与片段时，必须用同一套规则。本篇定义 md2md 为此新增的两组接口：命名块的解析与清除（标记规则见 [01](./01-named-blocks.md)），以及用 Cloud 的值展开变量与片段的预处理入口。

对应的产品需求见[场景 1](../prd.md#场景-1把产品名和连接值写成变量)、[场景 2](../prd.md#场景-2在-milvus-原文中标出-cloud-要改的一段)。

**参与方**：md2md（提供方）、zdoc 生成与 Milvus CI（调用方）。

**状态**：由原接口设计迁入，待工程维护者完善。

## 约定

两组接口随 Phase 1a 的 md2md 同一次发版上线。zdoc 与 Milvus CI 都锁定 md2md 的精确版本。两组接口都是 md2md 包中的函数：用 `import` 从包中取出，再像下面的代码那样调用。

### 命名块的解析与清除

**作用与阶段。** 找出原文中的命名块并检查标记写法，供 zdoc 按页面配置修改时定位；修改完成、发布之前，再把标记删掉，网站上不留痕迹（标记规则见 [01](./01-named-blocks.md)）。Milvus 侧在每个 PR 的检查和发布构建时使用；Cloud 侧每次生成时，读入原文后解析，按页面配置完成变换后清除（生成的各步见[接口地图](./README.md#生成流水线)）。

#### 调用

```js
import { parseBlocks, stripBlockMarkers } from "@zilliz/mdtomd/blocks.js";

// 解析：找出全部命名块，检查标记写法，返回块的位置与错误
const result = parseBlocks(content, { sourceName, isFragment });

// 清除：删掉标记所在的整行，返回清除后的 Markdown
const output = stripBlockMarkers(content);
```

`parseBlocks` 的参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content` | 字符串 | 是 | 一篇页面文件的完整 Markdown |
| `sourceName` | 字符串 | 否 | 报错时显示的文件名 |
| `isFragment` | 布尔值 | 否，默认 `false` | 为 `true` 时，任何标记都报 `BLOCK_IN_FRAGMENT`。命令行与 `goover` 按文件是否在 `fragments/` 下传入 |

`stripBlockMarkers` 只有一个参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content` | 字符串 | 是 | 要清除标记的 Markdown |

#### 处理规则

- 标记按 01 的规则识别；代码块（三个反引号围起的部分）中的标记不识别，也不清除。
- `parseBlocks` 一次收集全部错误，不在第一个错误处停下。
- `stripBlockMarkers` 只删除标记所在的整行，其余内容逐字不变。调用方先用 `parseBlocks` 检查，没有错误才清除。
- milvus-docs 的 CI 构建时运行 `goover`（md2md 现有的转换命令）：它在写文件前对每篇文档先检查、再清除，有错误时构建失败。

#### 返回

`parseBlocks` 的返回：

```js
{
  ok: true,
  blocks: [
    { id: "before-you-start", startLine: 12, endLine: 30 }
  ],
  errors: []
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `ok` | 布尔值 | 没有任何错误时为 `true` |
| `blocks` | 数组 | 每个命名块一项；`ok` 为 `false` 时为空数组，不返回部分结果 |
| `blocks[].id` | 字符串 | 命名块 ID |
| `blocks[].startLine`、`blocks[].endLine` | 数字 | 开始标记、结束标记所在的行号，从 1 开始，与编辑器中看到的行号一致 |
| `errors` | 数组 | 全部错误；每项含 `code`（错误码，见 [01](./01-named-blocks.md#出错时)）、`message`（说明）、`file`（即 `sourceName`）、`line`（行号，从 1 开始） |

`stripBlockMarkers` 返回删除标记后的 Markdown 字符串。

#### 命令行

milvus-docs 的 PR 检查（`check.yml`）运行 md2md 提供的命令，例如 `md2md-blocks check site/en`：检查目录下全部页面与片段文件，有错误时逐条输出并以非零状态退出，PR 检查因此失败。

### 预处理

**作用与阶段。** 把 `{{var.xxx}}` 换成 Cloud 的变量值，把 `{{fragments/xxx.md}}` 换成片段的内容。只在 Cloud 生成时使用：清除命名块标记之后、产品过滤之前（见[接口地图](./README.md#生成流水线)）。Milvus 侧继续用现有的 `goover` 展开，不调用它。

md2md 现有的转换入口（`goover` 所用）已能展开变量与片段，但变量来源、错误处理和读取范围不适合 Cloud（见[设计理由](#设计理由)中的“为什么另开预处理入口”）；`preprocess` 是本期新增的入口，复用同一套展开规则，`goover` 保持不变。

#### 调用

```js
import { preprocess } from "@zilliz/mdtomd/preprocess.js";

// 预处理：展开片段、替换变量，返回展开后的 Markdown 与用到的依赖
const result = preprocess({ content, fragmentRoot, variables, sourceName, limits });
```

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `content` | 字符串 | 是 | 待处理的整页 Markdown，即按页面配置完成变换、并清除命名块标记后的文本 |
| `fragmentRoot` | 字符串 | 是 | 同一 commit 的 milvus-docs 检出中 `site/en` 的绝对路径；`{{fragments/x.md}}` 解析为 `<fragmentRoot>/fragments/x.md` |
| `variables` | 对象 | 是 | 完整的变量表：键是变量名，可以嵌套；值只能是字符串、数字或布尔值。md2md 不按目录查找，也不合并其他来源的值。Cloud 的变量表只来自 `shared-docs/Variables.json` |
| `sourceName` | 字符串 | 否 | 报错时显示的文件名 |
| `limits` | 对象 | 否 | 四个数字字段，都可以不写：`maxDepth`（嵌套深度，默认 5）、`maxFragments`（片段数，默认 100）、`maxFragmentBytes`（单个片段大小，默认 256 KiB）、`maxOutputBytes`（输出大小，默认 2 MiB） |

#### 处理规则

- 先递归展开片段，再替换变量；片段使用调用页的变量表，代码块中的变量照常替换。这与 md2md 现有的转换入口（`goover` 所用）一致。
- 支持 `{{var.a.b}}` 嵌套键，不区分大小写；变量值原样插入，不再展开。
- `{{var.*}}` 与 `{{fragments/*}}` 之外的 `{{...}}`（如代码中的 `{{ doc.content }}`）原样保留。
- 片段只能读 `<fragmentRoot>/fragments/` 之内的 `.md` 普通文件，路径中任何一段都不能是符号链接（指向别处的快捷方式文件）；同一片段多次引用时只读一次。
- 调用之间互不影响，两个产品可以在同一进程中并行生成。

#### 返回

```js
{
  ok: true,
  content: "...",
  dependencies: {
    fragments: [{ path, sha256, bytes, includedBy: [...] }],
    variables: [{ key, usedIn: [...] }]
  },
  errors: [],
  engine: { name: "@zilliz/mdtomd", version: "<精确版本>" }
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `ok` | 布尔值 | 没有任何错误时为 `true` |
| `content` | 字符串或 `null` | 展开后的 Markdown；`ok` 为 `false` 时为 `null`，不返回部分结果 |
| `dependencies.fragments` | 数组 | 用到的每个片段：路径、内容摘要（`sha256`）、字节数，以及引用它的文件 |
| `dependencies.variables` | 数组 | 用到的每个变量：变量名，以及在哪些文件中使用 |
| `errors` | 数组 | 全部错误；每项含 `code`、`message`、`file`、`line`，以及补充信息 `detail`（如循环引用的引用链） |
| `engine` | 对象 | md2md 的包名与精确版本 |

zdoc 收到 `ok: false` 时让该页生成失败；`dependencies` 与 `engine` 写入记录文件（见 [05](./05-publish-handoff.md#记录文件)），用于缓存判断和恢复。参数类型错误属于调用方的编程错误，直接抛出 `TypeError`，不放进 `errors`。

依赖与限额的约定（2026-10-22 在 WP2 的计划审阅中确定，由契约用例固定）：

| 项 | 约定 |
|---|---|
| `fragments[].path` | 相对于 `fragmentRoot`、用 `/` 分隔，如 `fragments/a.md` |
| `includedBy`、`usedIn` | 直接引用它的文件，去重；数组按第一次用到的顺序排列 |
| `variables[].key` | 小写、用 `.` 连接的完整键名，如 `cloud.region` |
| `maxFragments` | 按读到的不同片段文件计数 |
| `maxDepth` | 页面直接引用的片段为第 1 层 |
| `maxOutputBytes` | 同一片段被引用多次时，每次展开都计入 |
| 报错的行号 | 指向写着这个变量或片段引用的那个文件中的行，不是展开后的行 |
| 键名只差大小写 | 同一层中有只差大小写的两个键，如 `Product` 与 `product`，整份变量表不合法，抛出 `TypeError`。zdoc 在调用前先检查 `Variables.json`，报 `CONFIG_VARIABLES_INVALID`（见 [09](./09-error-catalog.md)），所有共享页都生成失败 |

## 出错时

命名块的错误码见 [01](./01-named-blocks.md#出错时)。预处理的错误码：

| 错误码 | 何时出现 |
|---|---|
| `VAR_MISSING` / `VAR_NOT_SCALAR` | 变量不存在，或值是对象、数组 |
| `FRAGMENT_NOT_FOUND` | 片段文件不存在 |
| `FRAGMENT_OUT_OF_ROOT` | 绝对路径、`..` 越界，或扩展名不是 `.md` |
| `FRAGMENT_SYMLINK` | 路径中有符号链接 |
| `FRAGMENT_CYCLE` | 循环引用，`detail` 给出引用链 |
| `LIMIT_EXCEEDED` | 深度、数量或体积超限，`detail` 给出是哪一项 |
| `UNSUPPORTED_MARK` | `{{tab}}`、`::glossary.`、`{{glossary.`、`{{images/` 等需要 Milvus 站点插件的标记 |

## 例子

<details>
<summary>Delete Entities 的预处理（1a）</summary>

内容对齐后，原文第 29 行是 `uri="{{var.example_endpoint}}"`。

```js
const result = preprocess({
  content: pageAfterTransforms,
  sourceName: "site/en/userGuide/insert-and-delete/delete-entities.md",
  fragmentRoot: "/work/checkouts/milvus-docs@<commit>/site/en",
  variables: {
    product_name: "Zilliz Cloud",
    example_endpoint: "YOUR_CLUSTER_ENDPOINT",
    example_token: "YOUR_CLUSTER_TOKEN"
  }
});
// result.ok === true；第 29 行变为 uri="YOUR_CLUSTER_ENDPOINT"
// result.dependencies.fragments: []
// result.dependencies.variables: example_endpoint、example_token 各一项
```

如果 Cloud 的 `Variables.json` 缺少 `example_token`，结果为 `ok: false`、`content: null`，`errors` 中有 9 条带行号的 `VAR_MISSING`。该页生成失败，不会改用 Milvus 的 `root:Milvus`。

</details>

## 设计理由

<details>
<summary>展开设计理由</summary>

**为什么放在 md2md。** md2md 与 zdoc 都是公开仓库，但 zdoc 是大型 monorepo，不适合让 Milvus CI 依赖。规则只实现一次，zdoc 与 Milvus 对“标记是否写对”“变量怎样展开”的判断不会出现分歧。

**为什么命名块的能力在 1a 上线。** 命名块的扫描（T01）属于 1a，解析代码 1a 就要可用；清除能力随同一版本进入 Milvus CI，带命名块的原文就不必等 1b。milvus-docs 目前没有命名块，加入校验不会牵出历史问题。

**为什么另开预处理入口。** md2md 原有入口不满足 Cloud 生成的要求（实测见[复用审计第 3.1 节](../../research/md2md-zdoc-reuse-audit.md#31-实测补充2026-10-14)）：

| 原有行为 | 新入口的处理 |
|---|---|
| 根目录取自 `PATH_ROOT` 或当前目录；配置和插件在加载时读入，存放在全局状态中 | 不依赖这些状态，调用之间互不影响 |
| 变量从根目录逐级合并各层 `Variables.json`，再合并页面 front matter（遇到冒号会截断） | 不查找变量，由调用方传入 |
| 缺失的变量被替换为空串 | 报错 |
| `{{fragments/../x.md}}` 能读出片段目录；循环引用会卡死 | 报错 |

zdoc 现有的 LarkDocWriter 只接收飞书 JSON，不能充当 Markdown 编译器；现有 local source 也没有 Git 锁定与命名块消费。所以由 md2md 提供预处理，两端共用同一套展开规则。

**为什么用变量表而不是目录。** 按目录查找会把隐式作用域带回来，Cloud 无法确定哪些值来自哪里。milvus-docs `v3.0.x` 中 97 处变量引用全部来自 `site/en/Variables.json`，没有子目录变量文件，也没有页面用到 front matter 变量，所以由调用方传入一张表不会损失原有能力。

**为什么由 md2md 读片段。** 受控读取的检查（越界、符号链接、循环、上限）由 md2md 负责，Milvus 侧以后也能复用。milvus-docs 中 34 页共引用片段 39 次，没有片段再引用片段，默认上限足够宽松。

**为什么锁定版本。** milvus-docs 的 `ci.yml`、`pre.yml`、`preview.yml` 目前都安装未固定版本的 md2md；新接口发版后，两边要使用同一个确定的版本，结果才可重现。

</details>

## 验收

- **T02**：显式绑定、缺失变量报错、并行不串值、不运行插件。
- **T03**：嵌套与重复引用记录在依赖中；循环、越界、符号链接、深度或体积超限都失败。
- **T11**：以 `site/en/Variables.json` 调用新入口，milvus-docs 全部页面的输出与原有入口在插件之前的结果逐字相同；同一篇原文加命名块前后，Milvus 侧输出逐字相同，没有标记残留。
