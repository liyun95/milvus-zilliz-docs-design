# Keycloak 文档中产品名属性的使用情况

来源：[keycloak/keycloak](https://github.com/keycloak/keycloak/tree/f5055043072a3e8e2ee958ab5d7ee09b759ba893/docs/documentation) `docs/documentation` 下 451 个 `.adoc` 文件，固定在 commit `f5055043`（2026-10-13 读取）。

属性定义见 [document-attributes.adoc](https://github.com/keycloak/keycloak/blob/f5055043072a3e8e2ee958ab5d7ee09b759ba893/docs/documentation/topics/templates/document-attributes.adoc)：`:project_name: Keycloak`，并有 `:project_community: true` 与 `:project_product: false` 两个开关。

统计方法：跳过 `templates`、`internal_resources` 目录，跳过代码块（`----`）、注释行、属性定义行和 `include::` 等指令行；在其余行中去掉行内代码与 URL 后，分别计数 `{project_name}` / `{project_name_full}` 与独立单词 `Keycloak`。统计为启发式，未区分 “Keycloak CR”“Keycloak JS” 这类组件名。

| 指南 | 属性 | 字面 “Keycloak” |
|---|---:|---:|
| server_admin | 1136 | 15 |
| server_development | 131 | 10 |
| authorization_services | 100 | 0 |
| api_documentation | 1 | 0 |
| upgrading | 497 | 183 |
| release_notes | 352 | 194 |
| 合计 | 2217 | 402 |

使用属性的文件 302 个，含字面 “Keycloak” 的文件 78 个。抽查 `upgrading` 中的字面用法，多为组件名，如 “Keycloak CR”“Keycloak JS”。
