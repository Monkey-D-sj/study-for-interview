<script setup lang="ts">
import { ref } from 'vue';
import { ElCard, ElInput, ElButton } from 'element-plus';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const messages = ref<Message[]>([])
const input = ref('')

const sendMessage = async () => {
  const res = await fetch('http://localhost:8000/chat/interview', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_input: input.value }),
  });
  if (!res.ok) {
    throw new Error('Failed to fetch');
  }
  messages.value.push({ role: 'user', content: input.value })
  input.value = ''
  messages.value.push({ role: 'assistant', content: '' })
  const stream = res.body!;
  const decoder = new TextDecoder();
  const reader = stream.getReader();
  let chunk = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }
    const decoded = decoder.decode(value);
    const jsonStr = decoded.match(/data: (.*)/)?.[1];
    if (jsonStr) {
      const data = JSON.parse(jsonStr);
      chunk += data.message;
      messages.value[messages.value.length - 1].content = chunk;
    }
  }
}
</script>

<template>
  <div>
    <div v-for="message in messages" :key="message.content" style="margin-bottom: 10px;">
      {{ message.role }}: {{ message.content }}
    </div>
    <el-input v-model="input" @keydown.enter="sendMessage" placeholder="Say something..." />
    <el-button @click="sendMessage">Submit</el-button>
  </div>
</template>
