# 现有发布工具链：第二张图的核验依据

核验日期：2026-10-11。范围为 User Guide 内容进入两端文档站的主链。图示为已检查源码和仓库文档中的流程，不代表本次执行了生产发布或验证了全部线上配置。

## Milvus

| 环节 | 证据 | 图示处理 |
|---|---|---|
| 原始正文 → md2md | [milvus-docs ci.yml](https://github.com/milvus-io/milvus-docs/blob/7d87b0bf26d7cbc713f40af6453ea2f925367901/.github/workflows/ci.yml) 复制 Variables.json、安装 `@zilliz/mdtomd`、执行 `goover`，以 doc_to 替换 site | 原文位于 milvus-docs；变量/片段和 Milvus 展示格式在转换阶段处理 |
| 转换结果 → web-content | 同一 workflow 按 version.json 的版本目录复制转换结果并推送 web-content master | web-content 是另一仓库中的内容消费与处理阶段 |
| 生成站点内容 | [master.yml](https://github.com/milvus-io/web-content/blob/c2fa9c8fc04b071dc320ca6279810f94bdcbeaa8/.github/workflows/master.yml) 执行 `generate:en` 并提交结果；[generate-en.js](https://github.com/milvus-io/web-content/blob/c2fa9c8fc04b071dc320ca6279810f94bdcbeaa8/tools/generate-en.js) 将 Markdown/MDX 转为 HTML 正文，写到 localization 下的 .md 文件，并写伴随 JSON 与导航数据 | 图中“生成 HTML / JSON”表示处理后的内容文件；不是指本次已确认有一个 GitHub Actions artifact 下载交接 |
| 翻译分支 | generate-en.js 在发现新文件时导入 translate.js；[translate.js](https://github.com/milvus-io/web-content/blob/c2fa9c8fc04b071dc320ca6279810f94bdcbeaa8/tools/translate.js) 向 localization 写目标语言文件 | 另核对 [translate.yml](https://github.com/milvus-io/web-content/blob/c2fa9c8fc04b071dc320ca6279810f94bdcbeaa8/.github/workflows/translate.yml)，包含每周 schedule 与 workflow_dispatch；图示列出新文件、每周定时和手动三个入口。仍不承诺每次正文修改都会自动重译 |
| 触发与取内容 | web-content master.yml 向 milvus.io 发送 `prod-deploy`；[milvus.io .gitmodules](https://github.com/milvus-io/milvus.io/blob/1df6c2a9dbfb14a1aafbb1dd0563de3d51aad67c/.gitmodules) 将 web-content 映射到 src/docs；[master_aws.yml](https://github.com/milvus-io/milvus.io/blob/1df6c2a9dbfb14a1aafbb1dd0563de3d51aad67c/.github/workflows/master_aws.yml) 更新子模块 | “触发构建”和“读取内容”是两个动作，都在图中说明；未将 dispatch 载荷描述为内容 artifact |
| 站点构建与部署 | master_aws.yml 构建、推送镜像并更新 Kubernetes deployment；[Builder.Dockerfile](https://github.com/milvus-io/milvus.io/blob/1df6c2a9dbfb14a1aafbb1dd0563de3d51aad67c/Builder.Dockerfile) 执行站点构建、打包 .next 与运行时文档 | 会议图合并成“Next.js → 镜像部署”，省略平台内部参数 |

新增固定源码快照与 manifest 保存在 [publication-chain](./evidence/publication-chain/)。此前 md2md / milvus-docs 的固定快照见[复用审计](./md2md-zdoc-reuse-audit.md)。多个仓库修订是核验基线，不表示一次已完成发布的共同版本。

## Zilliz Cloud

基线仍为 zdoc `3777ec0b322546d716485e8f88da8412b0265e71`；未将 master 源码等同于当前所有生产任务已使用该修订。

| 环节 | 证据 | 图示处理 |
|---|---|---|
| 飞书 → 生成正文 | [Fetch workflow](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/.github/workflows/fetch-docs.yml)、[Guides assembly](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/.github/workflows/_assemble-guides.yml) | 抓取正文/媒体，分表渲染、组装、校验，生成 checkpoint artifact；源生产与站点发布分开 |
| 生成状态 → dev | Fetch 的发布路径串行写入 dev；[README](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/README.md) 描述 dev 对 content/generated/i18n 等生成状态的职责 | 图中 dev 是生成内容，不是共享原文的权威编辑入口。checkpoint 是带校验信息的内容发布产物，并非最终网站镜像 |
| Translation | Fetch 仅在条件满足时 dispatch Translation；译文经 publish-translation 写回 dev | Fetch 的 source_publication_barrier 先确认所选源内容已发布；run_translations、publish 及 handoff 成功条件满足后，由 dispatch_translations 发起翻译。图中点线从 Fetch 引出，dev 是内容所在分支；译文发布回写 dev。英文站包含日文内容，中文产品站独立 |
| 站点构建 | [apps/docs/package.json](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/apps/docs/package.json) 由 build:en 调用 Docusaurus；[_build-publish-site.yml](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/.github/workflows/_build-publish-site.yml) 生成和校验 site-build artifact | 构建产物、生成 Markdown 和正式站点是不同层级 |
| 外部发布 | README 明确外部 Jenkins UAT/Prod 使用相同 site-qualified build 接口，配置在仓库外；_build-publish-site.yml 的 deploy job 仅显示 artifact 校验 | 二者属于同一列，但节点分开：zdoc/apps/docs 的 Docusaurus 为已核实代码；Jenkins 使用虚线框和脚注，表示外部配置未核验。Actions 的 artifact 校验并不证明已部署线上；Jenkins 实际触发、审批、所选分支、镜像复用与线上运行情况尚未核验 |

## 图的阅读边界

- 内容维护图回答“谁改正文、怎样同步”；发布工具链图回答“各自消费哪份输入、经过哪些工具和产物、发布到哪里”。不重复 PR 或人工回同步箭头。
- 实线表示内容消费或处理顺序，点线表示工作流触发；外部系统的虚线框表示其配置待核验。固定源码核验不代表已执行生产发布。
- 两条链之间没有共享内容消费箭头；Git 同源与 Cloud 差异组装属于后面的目标方案。
- 本图简化预览、所有语言、缓存、媒体存储、恢复与发布环境细节。Current/Next 的过滤及单镜像策略仍需结合外部配置确认，未画成已核实运行机制。

## 术语及工具共用核验

- `goover`：[md2md package.json](https://github.com/zilliztech/md2md/blob/635da07276e80fb2a6efdf667686df3913d5de4c/package.json) 将其注册到 `bin/goover.js`，该文件调用 `goOver()`。它是 md2md 的 CLI 入口，不是另一个仓库或服务。
- checkpoint：[create-checkpoint-artifact.js](https://github.com/zilliztech/zdoc/blob/3777ec0b322546d716485e8f88da8412b0265e71/scripts/docs-workflow/create-checkpoint-artifact.js#L267) 把生成文件写入 payload，manifest 记录文件路径、SHA-256、大小、删除清单及校验信息；`_assemble-guides.yml` 打包上传。“交接包”是对实现结构的概括，有直接源码依据，并非对未知行为的推断。
- `dev`：是 zdoc Git 分支，不是目录或 UAT 环境。README 的 Git branch ownership 和 Fetch 发布步骤均支持这一含义。
- Cloud 站点：zdoc 的 `apps/docs/package.json` 定义 Docusaurus 依赖和 build 命令；站点与内容工具位于同一仓库。
- md2md 共用：检查固定 zdoc 快照中的实现、工作流、package manifests 与 pnpm-lock.yaml，未发现 md2md / mdtomd / goover 依赖或调用。结论限定于本次所查 Cloud Guides 链，不扩展为组织内从未使用。
- 其他脚本共用：[Milvus sync-shared-scripts.manifest.js](https://github.com/milvus-io/milvus-docs/blob/7d87b0bf26d7cbc713f40af6453ea2f925367901/scripts/sync-shared-scripts.manifest.js) 存在从 `../zdoc/plugins/lark-docs` 同步 Lark 脚本到 `scripts/lib` 的配置，但现有 zdoc 布局为 packages。它是编辑/导出相关工具的同步记录，不证明发布工具链图 的两条发布链共用 md2md，也不能证明当前执行状态。

配色沿用图 1 的黄色内容含义，处理和构建改用紫色，站点/外部系统用白色，避免将蓝色人和绿色社区角色改作工具含义。发布工具链图 保留五阶段对齐，并仅给仓库说明支持、实际外部配置未核验的 Jenkins 节点加虚线框。

## 原文来源补充（用户确认）

2026-10-11 用户明确：SDK Reference 原文存放并维护在 web-content；milvus-docs 不对 SDK Reference 做单独内容维护。该事实来自用户对现有流程的确认，不再列为“SDK 原文仓库待核验”。发布工具链图 的 milvus-docs → web-content 路径仅描述 User Guide；后续需确认的是 SDK 原文在 web-content 内的具体路径、版本和消费规则。web-content 同时承担 User Guide 发布内容加工与 SDK Reference 原文维护，不能把整个仓库一概视为生成产物。
