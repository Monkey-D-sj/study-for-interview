<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { ElInput, ElButton } from 'element-plus'

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const messages = ref<Message[]>([])
const input = ref('')
const isStreaming = ref(false)
const threadRef = ref<HTMLElement | null>(null)

const session_id = ref(Math.random().toString(36).substring(2))

let scrollScheduled = false
const scheduleScrollToBottom = () => {
  if (scrollScheduled) return
  scrollScheduled = true
  requestAnimationFrame(() => {
    scrollScheduled = false
    const el = threadRef.value
    if (!el) return
    el.scrollTop = el.scrollHeight
  })
}

const sendMessage = async () => {
  const trimmed = input.value.trim()
  if (!trimmed || isStreaming.value) return

  isStreaming.value = true
  try {
    const res = await fetch('http://localhost:8000/chat/interview', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: trimmed,
        session_id: session_id.value,
        resume: messages.value.length > 0
      }),
    })

    if (!res.ok || !res.body) {
      throw new Error('Failed to fetch')
    }

    messages.value.push({ role: 'user', content: trimmed })
    input.value = ''
    messages.value.push({ role: 'assistant', content: '' })
    await nextTick()
    scheduleScrollToBottom()

    const decoder = new TextDecoder()
    const reader = res.body.getReader()
    let chunk = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const decoded = decoder.decode(value)
      const jsonStr = decoded.match(/data: (.*)/)?.[1]
      if (!jsonStr) continue

      const data = JSON.parse(jsonStr)
      chunk += data.message
      messages.value[messages.value.length - 1].content = chunk
      scheduleScrollToBottom()
    }
  } finally {
    isStreaming.value = false
  }
}
</script>

<template>
  <div class="chat-shell">
    <header class="chat-header">
      <div class="chat-title">Chat</div>
      <div class="chat-subtitle">session: {{ session_id }}</div>
    </header>

    <main ref="threadRef" class="chat-thread">
      <div v-if="messages.length === 0" class="chat-empty">
        输入问题开始对话
      </div>

      <div v-for="(message, idx) in messages" :key="idx" class="msg-row"
        :class="message.role === 'user' ? 'is-user' : 'is-ai'">
        <div class="msg-avatar">
          {{ message.role === 'user' ? 'U' : 'AI' }}
        </div>
        <div class="msg-card">
          <div class="msg-meta">
            {{ message.role === 'user' ? '你' : 'AI' }}
          </div>
          <div class="msg-content">
            {{ message.content }}
          </div>
        </div>
      </div>
    </main>

    <footer class="chat-composer">
      <el-input v-model="input" class="composer-input" placeholder="输入你的问题，回车发送" :disabled="isStreaming"
        @keydown.enter.prevent="sendMessage" />
      <el-button class="composer-send" type="primary" :loading="isStreaming" :disabled="!input.trim() || isStreaming"
        @click="sendMessage">
        发送
      </el-button>
    </footer>
  </div>
</template>

<style scoped>
.chat-shell {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 100%;
  text-align: left;
  background: radial-gradient(1000px 400px at 50% -10%, rgba(170, 59, 255, 0.12), transparent 65%);
}

.chat-header {
  padding: 18px 18px 10px;
  border-bottom: 1px solid var(--border);
}

.chat-title {
  font-family: var(--heading);
  font-weight: 600;
  letter-spacing: -0.3px;
  color: var(--text-h);
}

.chat-subtitle {
  margin-top: 2px;
  font-family: var(--mono);
  font-size: 13px;
  opacity: 0.7;
}

.chat-thread {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-empty {
  margin: auto;
  font-size: 14px;
  opacity: 0.7;
}

.msg-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.msg-row.is-user {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text-h);
  border: 1px solid var(--border);
  background: var(--social-bg);
  flex: 0 0 auto;
}

.msg-row.is-user .msg-avatar {
  background: var(--accent-bg);
  border-color: var(--accent-border);
  color: var(--accent);
}

.msg-card {
  max-width: min(720px, 78%);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 10px 12px;
  background: var(--social-bg);
  box-shadow: var(--shadow);
}

.msg-row.is-user .msg-card {
  background: var(--accent-bg);
  border-color: var(--accent-border);
}

.msg-meta {
  font-size: 12px;
  opacity: 0.75;
  margin-bottom: 4px;
}

.msg-content {
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--text-h);
  line-height: 150%;
}

.chat-composer {
  position: sticky;
  bottom: 0;
  padding: 14px 18px 18px;
  border-top: 1px solid var(--border);
  background: color-mix(in srgb, var(--bg), transparent 12%);
  backdrop-filter: blur(10px);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
}

.composer-input :deep(.el-input__wrapper) {
  border-radius: 12px;
}

.composer-send {
  height: 40px;
  border-radius: 12px;
}
</style>