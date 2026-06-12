# Lastiara

一个本地网页骨架：浏览器输入问题，Node 后端接收 `/api/chat`，再转发给 Coze agent。当前 Coze API 信息还没填时，后端会返回占位回答，用来先验证前后端链路。

## Run

```bash
cd /Users/apple/hajime/lastiara
npm run dev
```

打开：

```text
http://localhost:5173
```

## API Flow

```text
Browser
  -> POST /api/chat { question }
  -> server.js
  -> src/cozeAgent.js
  -> Coze agent
  -> answer
  -> Browser renders answer
```

## Coze Config

等 Coze API 准备好后，新建 `lastiara/.env`：

```env
COZE_API_KEY=your_coze_personal_access_token
COZE_BOT_ID=your_coze_agent_bot_id
COZE_BASE_URL=https://api.coze.com
PORT=5173
```

如果是 Coze 中国区，`COZE_BASE_URL` 改为：

```env
COZE_BASE_URL=https://api.coze.cn
```

后续如果 Coze 的接口字段和当前假设不同，只改 `src/cozeAgent.js`，不要动前端页面的数据流。
