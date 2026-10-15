# 03 md2md 预处理

zdoc 生成 Cloud 页面时，要用 Cloud 的值展开 Milvus 原文中的变量与片段，规则必须和 Milvus 侧一致。本篇定义 zdoc 怎样调用 md2md 新增的预处理入口，以及它返回什么。

**参与方**：zdoc 生成（调用方）、md2md（提供方）。

**状态**：已定义，待文档负责人确认。

## 约定

### 调用

```js
import { preprocess } from "@zilliz/mdtomd/preprocess.js";

const result = preprocess({ content, fragmentRoot, variables, sourceName, limits });
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `content` | 是 | 待处理的整页 Markdown，即完成流水线第 ③ 步变换、并清除命名块标记后的文本 |
| `fragmentRoot` | 是 | 同一 commit 的 milvus-docs 检出中 `site/en` 的绝对路径；`{{fragments/x.md}}` 解析为 `<fragmentRoot>/fragments/x.md` |
| `variables` | 是 | 完整的变量表；md2md 不按目录查找，也不合并其他来源的值。Cloud 的变量表只来自 `shared-docs/Variables.json` |
| `sourceName` | 否 | 报错时显示的文件名 |
| `limits` | 否 | 默认：嵌套深度 5、片段数 100、单个片段 256 KiB、输出 2 MiB |

### 处理规则

- 先递归展开片段，再替换变量；片段使用调用页的变量表，代码块中的变量照常替换。这与原有入口一致。
- 支持 `{{var.a.b}}` 嵌套键，不区分大小写；变量值原样插入，不再展开。
- `{{var.*}}` 与 `{{fragments/*}}` 之外的 `{{...}}`（如代码中的 `{{ doc.content }}`）原样保留。
- 片段只能读 `<fragmentRoot>/fragments/` 之内的 `.md` 普通文件，路径中任何一段都不能是符号链接；同一片段多次引用时只读一次。
- 调用之间互不影响，两个产品可以在同一进程中并行生成。

### 返回

```js
{
  ok: true,
  content: "...",                 // ok 为 false 时为 null，不返回部分结果
  dependencies: {
    fragments: [{ path, sha256, bytes, includedBy: [...] }],
    variables: [{ key, usedIn: [...] }]
  },
  errors: [{ code, message, file, line, detail }],   // 一次收集全部错误
  engine: { name: "@zilliz/mdtomd", version: "<精确版本>" }
}
```

zdoc 收到 `ok: false` 时让该页生成失败；`dependencies` 与 `engine` 写入记录文件（见 [05](./05-publish-handoff.md#记录文件)），用于缓存判断和恢复。参数类型错误属于调用方的编程错误，直接抛出 `TypeError`。zdoc 与 Milvus CI 都锁定 md2md 的精确版本。

## 出错时

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
<summary>Delete Entities（1a）</summary>

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

**为什么另开入口。** md2md 原有入口不满足 Cloud 生成的要求（实测见[复用审计第 3.1 节](../../research/md2md-zdoc-reuse-audit.md#31-实测补充2026-10-14)）：

| 原有行为 | 新入口的处理 |
|---|---|
| 根目录取自 `PATH_ROOT` 或当前目录；配置和插件在加载时读入，存放在全局状态中 | 不依赖这些状态，调用之间互不影响 |
| 变量从根目录逐级合并各层 `Variables.json`，再合并页面 front matter（遇到冒号会截断） | 不查找变量，由调用方传入 |
| 缺失的变量被替换为空串 | 报错 |
| `{{fragments/../x.md}}` 能读出片段目录；循环引用会卡死 | 报错 |

zdoc 现有的 LarkDocWriter 只接收飞书 JSON，不能充当 Markdown 编译器；现有 local source 也没有 Git 锁定与命名块消费。所以由 md2md 提供预处理，两端共用同一套展开规则。

**为什么用变量表而不是目录。** 按目录查找会把隐式作用域带回来，Cloud 无法确定哪些值来自哪里。milvus-docs `v3.0.x` 中 97 处变量引用全部来自 `site/en/Variables.json`，没有子目录变量文件，也没有页面用到 front matter 变量，所以由调用方传入一张表不会损失原有能力。

**为什么由 md2md 读片段。** 受控读取的检查（越界、符号链接、循环、上限）由 md2md 负责，Milvus 侧以后也能复用。milvus-docs 中 34 页共引用片段 39 次，没有片段再引用片段，默认上限足够宽松。

**为什么锁定版本。** milvus-docs 的 `ci.yml`、`pre.yml`、`preview.yml` 目前都安装未固定版本的 md2md；新入口发版后，两边要使用同一个确定的版本，结果才可重现。

## 验收

- **T02**：显式绑定、缺失变量报错、并行不串值、不运行插件。
- **T03**：嵌套与重复引用记录在依赖中；循环、越界、符号链接、深度或体积超限都失败。
- **T11**：以 `site/en/Variables.json` 调用新入口，milvus-docs 全部页面的输出与原有入口在插件之前的结果逐字相同。
