const DEFAULT_BASE_URL = 'https://api.coze.com'

export function getAgentStatus() {
  return {
    provider: 'coze',
    configured: Boolean(getApiKey() && process.env.COZE_BOT_ID),
    baseUrl: getBaseUrl(),
  }
}

export async function askKnowledgeAgent({ question, userId }) {
  const apiKey = getApiKey()

  if (!apiKey || !process.env.COZE_BOT_ID) {
    return {
      answer:
        'Coze API 尚未配置。当前前后端链路已搭好，之后在 .env 填入 COZE_API_KEY 或 COZE_API_TOKEN，以及 COZE_BOT_ID 后即可替换为真实回答。',
      meta: {
        mode: 'placeholder',
      },
    }
  }

  return askCozeV3({
    question,
    userId,
    apiKey,
    botId: process.env.COZE_BOT_ID,
    baseUrl: getBaseUrl(),
  })
}

export async function streamKnowledgeAgent({ question, userId, onText, onMeta }) {
  const apiKey = getApiKey()

  if (!apiKey || !process.env.COZE_BOT_ID) {
    await onText(
      'Coze API 尚未配置。当前前后端链路已搭好，之后在 .env 填入 COZE_API_KEY 或 COZE_API_TOKEN，以及 COZE_BOT_ID 后即可替换为真实回答。'
    )
    await onMeta({ mode: 'placeholder' })
    return
  }

  await streamCozeV3({
    question,
    userId,
    apiKey,
    botId: process.env.COZE_BOT_ID,
    baseUrl: getBaseUrl(),
    onText,
    onMeta,
  })
}

async function askCozeV3({ question, userId, apiKey, botId, baseUrl }) {
  const chat = await cozeRequest({
    apiKey,
    baseUrl,
    endpoint: '/v3/chat',
    method: 'POST',
    body: {
      bot_id: botId,
      user_id: userId,
      stream: false,
      additional_messages: [
        {
          role: 'user',
          content: question,
          content_type: 'text',
        },
      ],
    },
  })

  const chatData = chat.data || chat
  const chatId = chatData.id
  const conversationId = chatData.conversation_id

  if (!chatId || !conversationId) {
    throw new Error(`Coze did not return chat id/conversation id: ${JSON.stringify(chat)}`)
  }

  const finalChat = await waitForCompletion({
    apiKey,
    baseUrl,
    chatId,
    conversationId,
  })

  const messages = await cozeRequest({
    apiKey,
    baseUrl,
    endpoint:
      `/v3/chat/message/list?conversation_id=${encodeURIComponent(conversationId)}`
      + `&chat_id=${encodeURIComponent(chatId)}`,
    method: 'GET',
  })

  return {
    answer: cleanAnswerText(extractAnswer(messages)) || 'Coze 没有返回可展示的文本回答。',
    meta: {
      mode: 'coze-v3',
      chatId,
      conversationId,
      status: finalChat.status,
    },
  }
}

async function streamCozeV3({ question, userId, apiKey, botId, baseUrl, onText, onMeta }) {
  const response = await fetch(`${baseUrl}/v3/chat`, {
    method: 'POST',
    headers: {
      authorization: `Bearer ${apiKey}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      bot_id: botId,
      user_id: userId,
      stream: true,
      additional_messages: [
        {
          role: 'user',
          content: question,
          content_type: 'text',
        },
      ],
    }),
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Coze stream API error: ${text || response.statusText}`)
  }

  const decoder = new TextDecoder()
  let buffer = ''
  let chatMeta = null
  let answerText = ''

  for await (const chunk of response.body) {
    buffer += decoder.decode(chunk, { stream: true })
    const events = buffer.split(/\n\n|\r\n\r\n/)
    buffer = events.pop() || ''

    for (const rawEvent of events) {
      const event = parseSseEvent(rawEvent)
      if (!event.data || event.data === '[DONE]') {
        continue
      }

      const payload = safeJsonParse(event.data)
      if (!payload) {
        continue
      }

      const data = payload.data || payload
      const type = data.type || payload.type
      const content = data.content || payload.content || ''

      if (data.conversation_id || data.chat_id || data.id) {
        chatMeta = {
          mode: 'coze-v3-stream',
          conversationId: data.conversation_id || chatMeta?.conversationId,
          chatId: data.chat_id || data.id || chatMeta?.chatId,
          status: data.status || chatMeta?.status,
        }
      }

      if (type === 'answer' && content) {
        const delta = getAnswerDelta(answerText, content)

        if (delta) {
          answerText += delta
          await onText(cleanAnswerText(delta))
        }
      }
    }
  }

  if (buffer.trim()) {
    const event = parseSseEvent(buffer)
    const payload = safeJsonParse(event.data)
    const data = payload?.data || payload
    const content = data?.content || payload?.content
    if ((data?.type || payload?.type) === 'answer' && content) {
      const delta = getAnswerDelta(answerText, content)

      if (delta) {
        await onText(cleanAnswerText(delta))
      }
    }
  }

  await onMeta(chatMeta || { mode: 'coze-v3-stream' })
}

async function waitForCompletion({ apiKey, baseUrl, chatId, conversationId }) {
  const intervalMs = readPositiveNumber(process.env.COZE_POLL_INTERVAL_MS, 1000)
  const timeoutSeconds = readPositiveNumber(process.env.COZE_TIMEOUT_SECONDS, 180)
  const attemptsFromTimeout = Math.ceil((timeoutSeconds * 1000) / intervalMs)
  const configuredMaxAttempts = Number(process.env.COZE_MAX_POLL_ATTEMPTS)
  const maxAttempts = Number.isFinite(configuredMaxAttempts) && configuredMaxAttempts > 0
    ? Math.max(configuredMaxAttempts, attemptsFromTimeout)
    : attemptsFromTimeout

  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const response = await cozeRequest({
      apiKey,
      baseUrl,
      endpoint:
        `/v3/chat/retrieve?conversation_id=${encodeURIComponent(conversationId)}`
        + `&chat_id=${encodeURIComponent(chatId)}`,
      method: 'GET',
    })
    const data = response.data || response
    const status = data.status

    if (status === 'completed') {
      return data
    }

    if (status === 'failed' || status === 'canceled') {
      const reason = data.last_error?.msg || data.last_error?.message || status
      throw new Error(`Coze chat ${status}: ${reason}`)
    }

    await delay(intervalMs)
  }

  throw new Error(
    `Coze response timed out after about ${Math.round((maxAttempts * intervalMs) / 1000)} seconds.`
  )
}

async function cozeRequest({ apiKey, baseUrl, endpoint, method, body }) {
  const response = await fetch(`${baseUrl}${endpoint}`, {
    method,
    headers: {
      authorization: `Bearer ${apiKey}`,
      'content-type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  })

  const text = await response.text()
  const data = text ? JSON.parse(text) : {}

  if (!response.ok || (data.code && data.code !== 0)) {
    const message = data.msg || data.message || response.statusText
    throw new Error(`Coze API error: ${message}`)
  }

  return data
}

function extractAnswer(payload) {
  const messages = Array.isArray(payload.data) ? payload.data : []

  return messages
    .filter((item) => item.type === 'answer')
    .map((item) => item.content)
    .filter(Boolean)
    .join('\n\n')
    .trim()
}

function getBaseUrl() {
  return (process.env.COZE_BASE_URL || DEFAULT_BASE_URL).replace(/\/$/, '')
}

function getApiKey() {
  return process.env.COZE_API_KEY || process.env.COZE_API_TOKEN
}

function readPositiveNumber(value, fallback) {
  const number = Number(value)
  return Number.isFinite(number) && number > 0 ? number : fallback
}

function parseSseEvent(rawEvent) {
  const event = { event: '', data: '' }

  for (const line of rawEvent.split(/\r?\n/)) {
    if (line.startsWith('event:')) {
      event.event = line.slice(6).trim()
    }

    if (line.startsWith('data:')) {
      event.data += line.slice(5).trim()
    }
  }

  return event
}

function safeJsonParse(text) {
  try {
    return JSON.parse(text)
  } catch {
    return null
  }
}

function getAnswerDelta(currentAnswer, incomingContent) {
  if (!currentAnswer) {
    return incomingContent
  }

  if (incomingContent === currentAnswer) {
    return ''
  }

  if (incomingContent.startsWith(currentAnswer)) {
    return incomingContent.slice(currentAnswer.length)
  }

  return incomingContent
}

function cleanAnswerText(text) {
  if (!text) {
    return ''
  }

  return text
    .replace(/经过解读与整理，?反馈给用户一份工整的报告[。.]?/g, '')
    .replace(/下面我将为你生成一份报告[。.]?/g, '')
    .replace(/我将以工整的报告形式反馈[。.]?/g, '')
    .replace(/以下是整理后的结果[：:]?[。.]?/g, '')
    .replace(/为您呈现如下[：:]?[。.]?/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
