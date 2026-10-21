# WP0 走读：测试与目录骨架

**仓库**：zdoc　**上游 PR**：[zilliztech/zdoc#792](https://github.com/zilliztech/zdoc/pull/792)　**任务卡**：[WP0](../tasks/WP0-skeleton.md)

## 解决什么问题

WP0 没有任何业务功能，网站上什么都不会变。它是“工作间”而不是“机器”：之后 zdoc 侧的每个工作包都在这里写代码、跑测试。它要保证三件事：

- 新代码有固定的家，而且核心逻辑碰不到外部系统；
- 不用连真实的 milvus-docs、GitHub、飞书，也能把功能测完；
- 每条需求都有人负责，漏掉任何一条，检查都会变红。

## 文件地图

都在 `packages/docs-tooling/src/shared-docs/` 下：

| 目录或文件 | 做什么 | 类比 |
|---|---|---|
| `core/` | 核心逻辑的家；现在只有共用类型，例如错误对象的字段 | 机器的主体，还是空的 |
| `adapters/types.ts` | 与五个外部系统打交道的接口：milvus-docs、md2md、GitHub、图片存储、飞书表格 | 插座的规格 |
| `adapters/fake/` | 五个外部系统的替身，测试时用 | 彩排用的道具 |
| `adapters/contract/` | 每个接口一组“契约测试”：替身必须通过，以后的真实实现也必须通过 | 插头插座的国标检测 |
| `spec/requirements.json` | 从设计仓库原样复制的需求清单 | 验收清单 |
| `spec/pending.json` | 还没做的 124 条需求，各归哪个工作包 | 还没开工的项目单 |
| `spec/coverage.ts` | 覆盖检查：每条需求要么有测试，要么在 `pending.json` 中 | 对账员 |
| `fixtures/pilots/` | 三篇试点页在 milvus-docs `9acdc99` 上的原文，与草拟的页面配置 | 测试素材 |
| `fixtures/milvus-docs/` | 合成的 milvus-docs 仓库：测试时现场建一个 Git 仓库，每次的 commit 号都相同 | 模拟考场 |
| `testing/golden.ts` | 与基准输出（样板间）逐字比较的工具 | 样板间的验收尺 |
| `testing/errors.ts` | 错误样例表的运行器 | 报错的验收尺 |
| `testing/core-boundary.test.ts` | 检查 `core/` 中没有读文件、跑命令、联网、引用飞书代码 | 门禁 |

仓库根目录还加了两处：`pnpm test:shared-docs` 命令，以及 PR 检查中跑这条命令的一步。

## 几个关键机制

**需求账本**。测试名中写需求编号，例如 `it('[4-3][LINE_NOT_FOUND] …')`。覆盖检查把三样东西对一遍：

| 情况 | 结果 |
|---|---|
| 一条需求既没有测试，也不在 `pending.json` 中 | 失败：漏了 |
| 一条需求已经有测试，却还在 `pending.json` 中 | 失败：提醒把它删掉 |
| 测试引用了清单中不存在的编号 | 失败：写错了或需求已删 |
| 被跳过的测试（`skip`、`todo`） | 不算覆盖 |

现在 124 条都在 `pending.json` 中，每做完一个工作包就删掉一批。剩下的数量就是进度。

**替身和契约测试**。核心逻辑以后要读 milvus-docs、调 md2md、开 PR、上传图片、读飞书表格。WP0 先把这些动作定义成接口，再各做一个只在内存中运转的替身。契约测试规定“任何实现都必须这样表现”，替身现在就要通过；以后接入真实系统时，同一组测试再跑一遍，两边的行为就不会不一致。

**合成仓库**。上游更新、两版并存这些功能，需要一段 milvus-docs 的历史来演练。构建器把 `commits/01-base/`、`02-paragraph/` 这样的目录依次叠加、各提交一次，作者和时间都固定，所以每次得到的 commit 号都相同，基准输出中的 `lock.yaml` 也就固定了。目前只能新增和修改文件；删除文件留给 WP12。

**基准输出工具**。比较不一致时测试失败。只有在本地设置 `UPDATE_GOLDEN=1` 才会改写文件，CI 中永远不会。基准输出目前是空的，WP4、WP5 之后才会产生第一批。

## 自己试一试

WP0 合并到上游之前，在 Agent 的工作树中运行；合并之后，在 `~/zdoc` 中 `git pull`、安装依赖后运行。

```bash
cd ~/zdoc/.claude/worktrees/wp0-skeleton
```

1. 跑全部测试，应看到 11 个测试文件、19 个测试通过：

   ```bash
   pnpm test:shared-docs
   ```

2. 看还剩多少需求、各归哪个工作包：

   ```bash
   python3 -c "import json,collections; p=json.load(open('packages/docs-tooling/src/shared-docs/spec/pending.json')); print(len(p), sorted(collections.Counter(p.values()).items(), key=lambda x:int(x[0][2:])))"
   ```

   现在是 124 条：WP3 16、WP4 8、WP5 16、WP6 4、WP8 4、WP10 23、WP11 9、WP12 11、WP13 6、WP14 23、WP15 4。

3. 看三篇试点页的配置，与[产品需求场景 3](../../prd.md#场景-3接入一页)的例子对照：

   ```bash
   cat packages/docs-tooling/src/shared-docs/fixtures/pilots/*/shared-docs/page.yaml
   ```

## 值得读的测试

| 文件 | 看什么 |
|---|---|
| `spec/coverage.test.ts` | 覆盖检查在什么情况下失败 |
| `fixtures/milvus-docs/build.test.ts` | 两次构建得到相同的 commit 号 |
| `testing/golden.test.ts` | 不一致时失败、CI 中不改写 |
| `testing/core-boundary.test.ts` | 哪些写法会被门禁拦下 |

## 刻意没做的

- 任何业务逻辑：读 `page.yaml`、调用 md2md、生成 MDX，都从 WP3 开始。
- 代码 Tabs 规则文件：WP4。Filtered Search 与 OpenAI 的变换：WP10，要等内容对齐后才有命名块。
- 基准输出目录的 `CODEOWNERS`：WP4 产生第一批基准输出之前，另找 zdoc 维护者确认。
