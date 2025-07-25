<script setup>
import ChatBot from './components/ChatBot.vue'
</script>

<template>
  <main class="chat-container">
    <ChatBot />
  </main>
</template>

<style scoped>
.chat-container {
  height: 100vh;           /* ocupa a altura total da janela */
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: #121212; /* fundo escuro */
}

input, textarea {
  color: #000000;       /* texto preto para ficar visível */
  background-color: #fff; /* fundo branco */
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 100%;
  box-sizing: border-box;
  font-size: 1rem;
}

button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #4338ca;
}
</style>
