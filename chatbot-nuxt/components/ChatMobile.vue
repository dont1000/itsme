<template>
  <div class="chat-container-mobile">
    <button
        @click="emit('update:openMobileChat', false)"
        class="btn-back"
      >
      <img src="@/assets/images/arrow-left.svg" alt="Back" />
    </button>
    <div class="chat-messages">
     
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
          <div>
       
          <button
            v-if="isMessageTooLong(msg.text)"
            class="expand-button"
            @click="toggleMessage(index)"
          >
            {{ expandedMessages[index] ? "Show Less" : "Show More" }}
          </button>
        
        </div>
     
      </div>
               <div class="message assistant">
                <div class="message-content">
                   👋 Hi, ich beantworte dir gerne Fragen zu mir und meiner Karriere. 

                </div>
               </div>
    </div>

    <form @submit.prevent="handleSubmit" class="chat-form">
      <div class="input-container">
        <textarea
          ref="input"
          class="input"
          rows="1"
          v-model="localInput"
          type="text"
          placeholder="Type your question..."
          @input="autoResize"
          :disabled="isLoading"
        />
        <img
          src="@/assets/images/Vector.svg"
          alt="Send"
          class="send-icon"
          @click="handleSubmit"
        />
      </div>
    </form>
  
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import type { Message } from '@/types/chat'

const props = defineProps<{
  messages: Message[];
  isLoading: boolean;
  openMobileChat:boolean;
}>();

const localMessages = ref(props.messages);

const input = ref();

const localInput = ref<string>("");
const expandedMessages = ref<Record<number, boolean>>({});
const emit = defineEmits<{
  (e: 'update:openMobileChat', value: boolean): void
  (e: 'submit', value: string): void
}>()

watch(() => props.messages, (newVal) => {
  localMessages.value = newVal
})



const handleSubmit = () => {
  const userMessage: Message = { role: "user", text: localInput.value };
  emit('submit', localInput.value)
  localInput.value = "";
};

const autoResize = () => {
  const el = input.value;
  el.style.height = "auto";
  el.style.height = el.scrollHeight + "px";
};

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

.meImage{
  width:400px;
  height:400px;
  
}

.chat-container-mobile {
  display: flex;
  flex-direction: column;
  height: 100dvh; /* Vollbildhöhe */
  background-color: rgb(255, 243, 227);
 
}

.chat-form {
  position: fixed;
  width: 100%;
  /* bottom: 15px; */
  left: 0;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  background-color: rgb(255, 243, 227);
  z-index: 999;
  position: relative;
  margin-bottom: 2rem;
}

/*-----------input field---------------------*/

.input-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background-color: #ffffff;
  box-shadow: 0px 4px 4px 0px #00000040 inset;
  width: 90%;
  align-self: center;
  position: relative;
  z-index: 998;
}

.input {
  resize: none; 
  overflow: hidden;
  width: 100%;
  position: relative;
}


textarea:focus {
  outline: none;
  box-shadow: none;
}

.send-icon {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

/*-----------message fields---------------------*/
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  flex-direction: column-reverse;
  justify-content: end;
  display: flex;
  padding-bottom: 3rem;
  position: relative;
  z-index: 10001;
}

.message {
  position: relative;
  padding: 1.2rem 0.9rem;
  margin-bottom: 2rem;
  min-width: 100px;
  max-width: 80%;
  font-size: 0.875rem;
  line-height: 1rem;
  min-height: auto; /* Remove fixed min-height */
  border-width: 0px;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 30px;
  border-bottom-left-radius: 30px;
}

.message.user {
  background-color: #fff;
  text-align: left;
  align-self: flex-start;
}

.message.assistant {
  background-color: #0396ff;
  border-bottom-left-radius: 0;
  color: #fff;
  text-align: left;
  align-self: flex-end;
}
.message.user::after {
  content: "";
  position: absolute;
  bottom: 0px;
  right: -31px;
  left: auto;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 20px 0px 0px 50px;
  border-color: transparent transparent transparent #fff;
  /* rotate: 0deg; */
  transform: rotate(0deg);
}

.message.assistant::after {
  content: "";
  position: absolute;
  bottom: 0px;
  left: -35px;
  width: 0;
  height: 0;
  /* border: 3px solid red; */
  border-width: 30px 0 00px 30px;
  border-color: #0396ff transparent transparent transparent;
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
.message-content {
  max-height: 81px;
  overflow: hidden;
  transition: max-height .3s linear;
}
.message-content.expanded {
  max-height: none; /* Set a large value to allow full expansion */

}

.expand-button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 4px;
  margin-top: 2px;
  text-decoration: underline;
  text-align: right;
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

  .btn-back {
  width: 30px;
  height: 30px;
  background-color: white;
  border: none;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  z-index: 19990;
  position: fixed;
  top: 15px;
  left: 15px;
 
}

.btn-back img {
  width: 30px;
  height: 15px;
}

/*-------------background input---------------------*/
/* .chat-container-mobile::after {
  content: "";
  position: absolute;
 
  width: 500px;
  height: 500px;
  background: radial-gradient(
    45.7% 54.7% at 50% 50%,
    #0396ff 0%,
    rgba(255, 243, 227, 0.44) 100%
  );
  background-repeat: no-repeat;
  background-size:cover;
  background-position: center;
  z-index: 1;
  left: 0;
  right: 0;

  bottom: -40px;

}  */

.chat-form::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  margin: 0 auto;
  bottom: 1rem;
  width: 300px;
  height: 300px;
  background-image: url("@/assets/images/background-image.png");
  background-position: bottom center;
  background-repeat: no-repeat;
  background-size: contain;
  z-index: 2;
  opacity: 0.3;
  pointer-events: none;

}


</style>
