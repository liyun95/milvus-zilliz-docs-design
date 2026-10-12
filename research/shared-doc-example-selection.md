# 共享文档试点候选的内容基线

当前已制作本地样例的是 Filtered Search 和 Delete Entities。OpenAI embedding 页是第三个候选，覆盖前提条件整节替换与凭证参数的代码行差异，尚未制作样例；两端差异见 [zdoc 代码变体与发布通道核验](./zdoc-variants-and-channels-audit.md#3-openai-页对照)。二者覆盖不同作者成本，不将简单页强行拆块，也不为体现差异而复制每种 SDK 的连接代码。

| 样例 | 展示内容 | 尚需内容审核 |
|---|---|---|
| [Filtered Search](../examples/filtered-search/walkthrough.md) | 产品名与连接变量；两组共享代码补 Cloud CLI | 共同 SDK 修订、Rust/C++ 补齐、Go v3 适用性、top-K/limit 和结果说明、图片 |
| [Delete Entities](../examples/delete-entities/walkthrough.md) | 整篇共享、两个连接变量、三组语言 Tabs；无命名块 | 共同代码修订、语言补齐、SDK 版本及 Go 统一认证示例 |

## 固定核验范围

- milvus-docs：`7d87b0bf26d7cbc713f40af6453ea2f925367901`。
- zdoc Cloud 英文 Guides：`05e31600f14326073a2c25c1a1eeda8e8d8fcc81`。
- 两篇自带 `evidence/` 保存原始 Markdown、来源记录及拟议共享源 diff，供本地重建和对照。

两篇源稿吸收了 Cloud 既有的共同修订，并非直接取 Milvus 原页即可全部上线。发布页用于阅读背景，未确认其线上修订恰好对应快照。没有执行 SDK/CLI 请求、生产发布或核对飞书最新有效修改。

内容审核先区分历史漂移与真实产品差异。行数差异、组件包装和新增语言不用于计算复用率；代码规范化比较也不能证明业务语义一致。详细源链接与限制分别维护在两篇 walkthrough 中。
