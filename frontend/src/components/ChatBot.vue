<template>
  <div class="flex flex-col h-screen w-full items-center justify-center bg-gray-100 overflow-hidden">
    <div class="flex flex-col h-full w-full max-w-4xl bg-white rounded shadow p-4">
      <h1 class="text-2xl font-bold mb-4 text-center">Chatbot BLAC</h1>

      <div
        class="flex-1 overflow-y-auto mb-4 p-3 bg-gray-50 rounded border"
        ref="chatContainer"
      >
        <div v-for="(msg, index) in messages" :key="index" class="mb-3 flex">
          <div
            :class="[
              'px-4 py-2 rounded max-w-2xl',
              msg.from === 'user'
                ? 'bg-blue-500 text-white ml-auto'
                : 'bg-gray-300 text-gray-900',
            ]"
          >
            {{ msg.text }}
          </div>
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="flex mt-auto">
        <input
          v-model="input"
          type="text"
          placeholder="Digite sua pergunta..."
          class="flex-grow rounded-l border border-gray-300 p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          :disabled="loading || !input.trim()"
          class="bg-blue-600 text-white px-4 rounded-r disabled:opacity-50"
        >
          {{ loading ? "Enviando..." : "Enviar" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";

const input = ref("");
const messages = ref([
  { from: "bot", text: "Olá! Pergunte qualquer coisa sobre o BLAC." },
]);
const loading = ref(false);
const chatContainer = ref(null);

async function sendMessage() {
  if (!input.value.trim()) return;

  // Adiciona a mensagem do usuário
  messages.value.push({ from: "user", text: input.value.trim() });
  loading.value = true;

  const pergunta = input.value.trim();
  input.value = "";

  await nextTick();
  scrollToBottom();

  try {
    // Chamada para sua API FastAPI
    const res = await fetch("http://127.0.0.1:8000/perguntar/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta: pergunta }),
    });

    const data = await res.json();

    // Adiciona resposta do bot
    messages.value.push({ from: "bot", text: data.resposta || "Desculpe, não entendi." });
  } catch (e) {
    messages.value.push({ from: "bot", text: "Erro na comunicação com o servidor." });
  } finally {
    loading.value = false;
    await nextTick();
    scrollToBottom();
  }
}

function scrollToBottom() {
  const container = chatContainer.value;
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}
</script>
