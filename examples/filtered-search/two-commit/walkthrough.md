# 双 commit 通道：Prod 与 UAT 各读一个 milvus-docs 版本

本例验证一种发布通道的写法：页面的 lock 记录两个 milvus-docs commit，Prod 用 `current`，UAT 用 `next`。生成器用两个版本各生成一遍 Cloud 页面，按块比较，只把不同的块包进 `<NextChannel>`。milvus-docs 不写通道标记，也不为通道加命名块。

这是讨论用的本地样例，不代表 lock 格式已经确定。真实工具链中两个版本来自 Git commit；本例用两个目录快照代替。

## 1. 文件

| 文件 | 作用 |
|---|---|
| [lock.yaml](lock.yaml) | 两个通道各自的 commit 与快照目录 |
| `current` 快照：[../milvus-docs](../milvus-docs/site/en/userGuide/search-query-get/filtered-search.md) | 即 Filtered Search 样例的共享原文 |
| `next` 快照：[milvus-docs-next](milvus-docs-next/site/en/userGuide/search-query-get/filtered-search.md) | 在 current 上做了四处小改动（见第 2 节），是演示用的改动，不是上游内容 |
| [build_channels.py](build_channels.py) | 调用现有 Filtered Search 生成器各生成一遍，再按块合并 |
| [generated/filtered-search.mdx](generated/filtered-search.mdx) | 合并后的单份 MDX |
| [generated/channel-receipt.json](generated/channel-receipt.json) | 两个通道的 commit、成对的块和警告 |

Cloud 页面配置、Cloud 内容文件（CLI 示例）和变量与 Filtered Search 样例完全相同，没有为通道做任何修改。

## 2. next 版本的四处改动与生成结果

| milvus-docs 中的改动 | 生成结果 |
|---|---|
| Overview 一句措辞调整 | 一对：旧段落 `exclude`，新段落 `include` |
| 列表第三项 “Returns” 改为 “Return the” | 一对：整个列表作为一块 |
| Examples 段落里多余的空格 | 一对：整段 |
| 迭代过滤的引导句改写，并在其后新增一段 | 一对：旧的一段对新的两段（相邻的修改与新增合为一组） |
| 两个代码组没有变化 | 各只输出一次，Cloud CLI 标签在其中 |

摘录（Overview 一节）：

```mdx
## Overview

<NextChannel action="exclude">

In Zilliz Cloud, filtered searches are categorized … depending on the stage at which the filtering is applied.

</NextChannel>

<NextChannel action="include">

In Zilliz Cloud, filtered searches are categorized … depending on when the filter is applied relative to the vector search.

</NextChannel>

### Standard filtering
```

## 3. 测试验证了什么

`test_channels.py` 共 15 项：

| 结论 | 怎样验证 |
|---|---|
| 每个通道看到的正好是自己那个版本的生成结果 | 按 NextChannel 规则分别取出 Prod 与 UAT 视图，逐块与单独生成的结果比较 |
| 细碎改动自动成对，不需要命名块 | 第 2 节四处改动得到四对，种类与块数符合预期 |
| 未变化的代码组和 Cloud CLI 只出现一次 | 代码组与 CLI 标签计数；任何一对中都不包含代码组 |
| 代码组有变化时，整个代码组成为一对，两边都带 Cloud CLI | 在 next 中改 Java 的 `.topK(5)`，两个视图各自带 CLI 与各自的取值 |
| Cloud 规则已替换的内容，上游再改也不会产生一对 | 在 next 中改 Python 的 `limit`：没有替换规则时多出一对；加上替换 Python 的规则后不再多出 |
| Cloud 规则必须在两个版本上都成立，失败时指出是哪个通道 | 在 next 中把命名块改名，报 `next:MISSING_BLOCK:standard-filtering-code` |
| 两个 commit 相同时没有任何通道标记 | 输出与原 Filtered Search 样例逐字节相同 |
| 上线只改 lock | `promote` 把 current 设为 next，输出与 next 单独生成的结果相同，不再有通道标记；原 lock 不被修改 |
| 只在一侧存在的块 | 删除只有 `exclude`，新增只有 `include` |
| 标题变化 | 记录 `HEADING_DIFFERS_BY_CHANNEL`，提示目录和锚点会因通道而不同 |
| front matter 无法按通道区分 | 不同时沿用 current，记录 `METADATA_FOLLOWS_CURRENT` |
| Cloud 内容文件中手写的 NextChannel | 两版相同时原样保留；落入成对区域时报 `NESTED_CHANNEL` |
| lock 格式错误 | 缺通道、字段不全、快照越界、同一 commit 对应不同快照都会报错 |

## 4. 本例没有验证的内容

- **zdoc 渲染。** NextChannel 包住列表、提示框或整个 Tabs 时能否正确渲染，目录是否过滤 NextChannel 中的标题，需要在 zdoc 中确认。
- **真实 Git 读取。** 两个 commit 共用一次检出，按 commit 读取文件和 md2md 片段。
- **翻译。** 成对的块两边都需要译文。
- **lock 的位置与提升方式。** 每页一份还是全站统一；提升 PR 由谁在 Cloud 发布时发起。
- **块切分的范围。** 只覆盖本例出现的标题、段落、列表、代码块、Tabs 与提示框。

## 5. 运行

```bash
cd examples/filtered-search
python3 two-commit/build_channels.py --check
python3 -m unittest discover -s two-commit -p 'test_*.py'
```
