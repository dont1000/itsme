<template>
  <div class="messages">
    <div v-if="isLoading" class="message assistant loading">
      <div class="dot" />
      <div class="dot" />
      <div class="dot" />
    </div>

    <div
      v-for="(msg, index) in messages"
      :key="index"
      :class="['message', msg.role]"
    >
      <div
        class="message-content"
        :class="{ expanded: expandedMessages[index] }"
      >
        {{ msg.text }}
      </div>
      <button
        v-if="isMessageTooLong(msg.text)"
        class="expand-button"
        @click="toggleMessage(index)"
      >
        {{ expandedMessages[index] ? "Less" : "More" }}
      </button>
    </div>
    <div class="message assistant" style="margin-bottom:200px;">
      <div class="message-content">
        Hast du ein Beispiel aus der Praxis, das deine Stärken gut zeigt?
      </div>
    </div>
    <div class="message assistant" >
      <div class="message-content">
        Was sind deine Stärken?
      </div>
    </div>
    <div class="message assistant" >
      <div class="message-content">
        Hi 👋 Frag mich gern nach meinen Stärken, meiner Motivation oder meiner Erfahrung, zum Beispiel:  
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Message } from "@/types/chat";


const props = defineProps<{
  messages: Message[];
  isLoading: boolean;
}>();

const expandedMessages = ref<Record<number, boolean>>({});


const isMessageTooLong = (content: string) => {
  const tempDiv = document.createElement("div");
  tempDiv.style.width = "247px"; // max-width of message
  tempDiv.style.fontSize = "0.875rem";
  tempDiv.style.lineHeight = "1rem";
  tempDiv.innerText = content;
  document.body.appendChild(tempDiv);
  const height = tempDiv.offsetHeight;
  document.body.removeChild(tempDiv);
  return height > 100;
};

const toggleMessage = (index: number) => {
  expandedMessages.value[index] = !expandedMessages.value[index];
};
</script>

<style scoped>
.messages {
  flex: 1;
  position: absolute;
  z-index: 99;
  display: flex;
  flex-direction: column-reverse;
  width: 100%;
  overflow-y: auto;
  height: calc(100% - 70px);
  align-items: center;
}

.message {
  position: relative;
  padding: 1.2rem 0.9rem;
  margin-bottom: 2rem;
  min-width: 100px;
  max-width: 300px;
  font-size: 0.875rem;
  line-height: 1rem;
  min-height: auto;
  border-width: 0px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 30px;
  border-bottom-left-radius: 30px;
}

.message.user {
  background-color: #fff;
  text-align: left;
  margin-right: 400px;
}

.message.assistant {
  background-color: #0396ff;
  border-bottom-left-radius: 0;
  color: #fff;
  text-align: left;
  margin-left: 31rem;
}

.message.user::after {
  content: "";
  position: absolute;
  bottom: 0px;
  left: -20px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 20px 40px 0 0;
  border-color: transparent #fff transparent transparent;
  transform: rotate(0deg);
}

.message.assistant::after {
  content: "";
  position: absolute;
  bottom: 0px;
  left: -35px;
  width: 0;
  height: 0;
  border-width: 20px 50px 0px 0;
  border-color: transparent #0396ff transparent transparent;
  transform: rotate(0deg);
}

.message.assistant.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.message.assistant.loading .dot {
  width: 6px;
  height: 6px;
  background-color: #fff;
  border-radius: 50%;
  animation: dot-flash 1.5s infinite;
}

.message.assistant.loading .dot:nth-child(1) {
  animation-delay: 0s;
}

.message.assistant.loading .dot:nth-child(2) {
  animation-delay: 0.3s;
}

.message.assistant.loading .dot:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes dot-flash {
  0%,
  20% {
    opacity: 0;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(0.8);
  }
}

.message-content {
  max-height: 97px;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.message-content.expanded {
  max-height: none;
}

.expand-button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 4px;
  margin-top: 8px;
  text-decoration: underline;
}

@media (max-width: 900px) {
  .message.user {
    margin-right: 0;
    width: 85%;
    align-self: flex-start;
  }
  .message.assistant {
    margin-left: 0;
    width: 85%;
    align-self: flex-end;
  }

  .message.user::after {
    bottom: 0px;
    right: -31px;
    left: auto;
    border-width: 20px 0px 0px 50px;
    border-color: transparent transparent transparent #fff;
    transform: rotate(0deg);
  }
}
</style> 