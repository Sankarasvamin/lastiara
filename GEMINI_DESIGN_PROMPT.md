# Gemini Design Prompt

请你只负责美化下面这个单页聊天网站的 HTML/CSS，不要改变 JavaScript 的接口逻辑，不要改任何元素 id，也不要改 `/api/health` 和 `/api/chat` 的 fetch 调用。

项目背景：
- 项目名：Lastiara
- 目标：一个本地浏览器上的数据库问答助手
- 用户在 textarea 输入问题
- 前端把 `{ question }` POST 到 `/api/chat`
- 后端会调用 Coze agent 查询指定知识库/数据库
- 页面展示用户问题和 agent 回答

必须保留的 id：
- `#form`
- `#question`
- `#send`
- `#messages`
- `#status`

必须保留的主要 class：
- `.app`
- `.topbar`
- `.brand`
- `.status`
- `.chat`
- `.messages`
- `.message`
- `.message.user`
- `.message.agent`
- `.label`
- `.bubble`
- `.composer-wrap`
- `.composer`
- `.empty`

设计要求：
- 做成一个成熟、克制、现代的数据库 AI assistant 界面，不要做营销落地页
- 第一屏直接是可用的聊天界面
- 适合学生/研究者查询数据库，感觉要清晰、可靠、偏工具型
- 不要使用夸张渐变、装饰性大图、过度卡片堆叠
- 移动端和桌面端都要可用
- 文本不能溢出按钮、气泡或容器
- 对话气泡要能显示较长的数据库分析文本
- 输入区固定在底部或自然位于底部均可，但不要遮挡消息
- 可以重写 `<style>` 内所有 CSS
- 可以微调 HTML 文案，但不要改 id、class、表单结构和 script 逻辑

请输出完整的 `public/index.html` 文件内容。
