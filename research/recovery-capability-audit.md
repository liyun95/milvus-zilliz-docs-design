# Git、图片与发布产物恢复能力核验

日期：2026-10-11。结论：共享文档首期不新增完整归档机制。优先使用已有 Git 内容状态、图片存储与镜像回滚契约；新增依赖记录、必要的资源固定和恢复验收。短期 CI artifact 过期不等于文档不可恢复。

## 1. 核验范围

通过 GitHub API 确认 zdoc dev 为 `96d7a73cc0ae9f3882269000eae2ac750e418386`，读取其 Git tree 和实际 blob。此前审计 master 为 `3777ec0b322546d716485e8f88da8412b0265e71`。本次核对的六个恢复、图片及部署实现文件，在这两个修订中 blob 相同。

没有访问 Jenkins、容器 registry 或 S3/OSS 管理 API，没有操作生产恢复。GitHub Actions artifact 列表两次读取均返回 `unexpected end of JSON input`，未取得可用清单，因此不对现存任务 artifact 作可用性承诺。仅凭仓库接口不能确认镜像保留期限、图片版本控制和线上部署修订。

证据：[Git 与隔离探针结果](./evidence/recovery-audit/probe-results.json)、[核验时使用的探针](./evidence/recovery-audit/probe-recovery.py)（重跑需准备固定修订的本地 zdoc checkout，并调整脚本中的本机 Node 路径；不属于样例运行依赖）。

## 2. 三种恢复需求分别判断

| 恢复需求 | 已有基础 | 当前结论 |
|---|---|---|
| 恢复已发布的 Markdown、译文、导航及相关状态 | dev Git 跟踪 content/en、i18n/ja-JP、generated、translation cache 等；restore-generated-state 支持 exact ref | 不依赖短期 artifact，已有恢复基础；新共享来源记录须纳入正式 Git 路径与恢复范围 |
| 从共享源重新组装 Cloud 页面 | Milvus 原文在 Git；Cloud 配置、overlay、工具和依赖锁可以在 zdoc Git 固定 | 无需默认复制整份源进新归档；新增 provider 必须把两仓版本与资源身份记录完整，并验证重建 |
| 将线上网站回滚到过去的发布 | release contract 记录 Git SHA、镜像 digest、Jenkins 身份；verifyRollbackTarget 限定同站点成功 Prod 记录 | 已有设计及验证实现，复用；实际镜像和可信发布记录的保留、Jenkins 接线尚待运维证据验证 |

Git 跟踪不保证任意历史网站镜像逐字节可重建，也不保证外部图片从不变化。Dockerfile 当前使用 `node:22-slim` 和 `nginx:1.28-alpine` 标签；重建历史镜像与按已有 digest 回滚是不同保证。本次不为实现后者而另建离线构建依赖仓库。

证据：[restore-generated-state](https://github.com/zilliztech/zdoc/blob/96d7a73cc0ae9f3882269000eae2ac750e418386/scripts/restore-generated-state.sh)、[部署契约](https://github.com/zilliztech/zdoc/blob/96d7a73cc0ae9f3882269000eae2ac750e418386/deploy/contracts/README.md)、[回滚校验器](https://github.com/zilliztech/zdoc/blob/96d7a73cc0ae9f3882269000eae2ac750e418386/deploy/contracts/verify-image.mjs)、[英文 Dockerfile](https://github.com/zilliztech/zdoc/blob/96d7a73cc0ae9f3882269000eae2ac750e418386/deploy/en/Dockerfile)。

## 3. Git：已验证的内容

在固定 dev tree 中发现 2,133 个 `content/en/` 文件、2,024 个 `i18n/ja-JP/` 文件、21 个 `generated/en/` 文件，以及翻译缓存、assembly 和 snapshot 状态。此处为文件数，不等于页面数。

OpenAI 英文与日文 blob 均已实际读取并计算 SHA-256，大小分别为 27,001 和 28,787 字节。读取 Git blob 无需飞书或 CI artifact。

当前 dev 英文文件路径是 `content/en/guides/tutorials/development/function/text-embedding-funcs/openai.md`，与用户原始 master 示例中的 `text-embedding-functions` 不同；当前 slug 仍为 `/openai`。正式迁移必须基于受控切换时的 dev 基线比较路径、正文、代码语言与译文，不能直接把旧 master 样例当作当前发布页。

必要新增：共享 Milvus SHA、消费配置/overlay、提取器版本、资源映射、页面来源归属与实际发布 receipt 的持久关联。人工输入走既有 master/tooling sync，生成状态走 dev；在同一次发布中绑定它们，并纳入 restore/ownership 合同。旧版本重组装从已记录的 Git 修订读取，源不可获取时明确报错，不退回浮动分支。

## 4. 图片：已持久上传，但历史字节未被发布引用固定

沿真实调用链检查了 Guides media prefetch → downloader → offlineMediaResolver → writer，而非仅查看旧 uploader：

- `guides-media-prefetch.js:92,291,299` 以 caption slug、board token 等生成对象文件名。
- `larkImageDownloader.js:81-95` 比较 MD5，变化时上传到同一个 S3 key；`110-134` 的 OSS 分支也允许覆盖。
- prefetch manifest 的 schema（`174-196`）记录 objectKey 等字段，不包含图像内容摘要或存储 version ID。
- `offlineMediaResolver.js:11-26` 通过媒体根地址与 objectKey 拼 URL；这里的 offline 指渲染时不再向飞书下载，不代表图片字节已封装在 Git/页面/容器中。

因此代码保证“有独立于飞书的图片发布位置”，不能单独保证“旧页面始终显示旧图片”。即使 bucket 有版本控制，页面 URL 未选择对应版本也不足以保证历史一致性。没有证据表明现网已发生丢图；bucket 策略尚未核验。

必要补充仅作用于迁移页实际引用的资源：优先从固定 Git 修订读取仓库内图片；外部资源复用既有图片存储，固定内容摘要和不可覆盖的对象地址或可寻址版本，缺失/摘要变化时报错。生命周期保留应覆盖被已采用页面引用的对象。复用下载/上传基础能力，扩展共享资源映射，不另建归档服务，也不预先改造所有 legacy 页面。

证据：[prefetch](https://github.com/zilliztech/zdoc/blob/96d7a73cc0ae9f3882269000eae2ac750e418386/scripts/docs-workflow/guides-media-prefetch.js)、[uploader](https://github.com/zilliztech/zdoc/blob/96d7a73cc0ae9f3882269000eae2ac750e418386/packages/docs-tooling/src/lark/larkImageDownloader.js)、[offline resolver](https://github.com/zilliztech/zdoc/blob/96d7a73cc0ae9f3882269000eae2ac750e418386/packages/docs-tooling/src/lark/offlineMediaResolver.js)。

### 核验样本与正式资源验收

本次 Git blob 恢复探针使用 OpenAI 作为固定历史样本，其英文和日文读取结果仍是本审计的证据。它不是当前会议或实现样例，也不用于证明其他页面的资源完整性。

当前两篇样例中，Filtered Search 引用了图片，须在正式接入时核对字节、版本和可恢复地址；不能把历史无图片样本的结论推广到它。最终以实际消费依赖决定资源范围，普通外部阅读链接不自动算作构建需要下载的资源。

## 5. 发布产物与恢复边界

`deploy/contracts/README.md` 已明确：回滚是受约束的 specified-image 部署，目标必须是同站点历史成功 Prod 记录的最终镜像 digest。仓库中的纯验证器已实现该判断；它本身不连接 registry，不部署，也不检查真实镜像是否仍可拉取。

`_build-publish-site.yml` 产生的 site artifact 默认保留 14 天；其 deploy job 仅验证 artifact，没有实际 Jenkins 部署指令。它与 Fetch 默认 3 天的 checkpoint 都不能代表容器 registry 的保留策略。

上线验收应由已有发布系统提供：一个真实旧版成功发布记录、其镜像仍可获取、对应部署/回滚流程有效的证据。外部图片不一定包含在镜像里，因此有图页面还要满足资源固定要求。无需据此再造镜像归档或发布系统。

## 6. 本轮验证与限制

- 隔离临时 Git 仓库执行真实 `restore-generated-state.sh --exact --ref <sha>`：5 项检查通过，覆盖英文、日文、导航、翻译缓存恢复，以及新增页面的移除；未配置远程、未使用 artifact。使用人工 fixture，不是生产数据全量 replay。
- 调用真实 `verifyRollbackTarget`：4 项检查通过，覆盖同站点成功记录放行，无记录、失败记录、其他站点拒绝；可信 provider 为人工 fixture，没有实际拉镜像。
- 现有 `offlineMediaResolver.test.js`：2 项通过，覆盖 URL 解析与缺失资源明确报错。
- 尝试运行完整 `verify-image.test.mjs` 和 `restore-generated-state.test.js`，分别因稀疏审计 checkout 未安装 `ajv`、`jiti` 未能启动；不能标记通过。定向探针使用 Node v24.18.0，正式 zdoc 工具链是 Node 22，不能替代其正式 gate。
- GitHub artifact 清单读取失败；未核验存储版本/生命周期、实际镜像保留和外部 Jenkins 配置；未运行付费翻译、完整站点构建或真实生产恢复。

## 7. 方案调整

不新建恢复包存储，不要求永久保存每次 CI 内容包。对已采用页面保留可追溯的 Git 输入及发布身份；registry/fragments 可以从固定输入重新生成。只补共享来源追踪、实际资源固定、恢复清单接线和相应验收。镜像/存储运维条件作为上线核验项，缺少证据不能直接推导为必须新建基础设施。
