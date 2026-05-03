<template>
  <div>
    <ChatMobile
      v-if="isMobile && openMobileChat"
      :messages="messages"
      :isLoading="isLoading"
      @submit="handleSubmitMobile"
      v-model:openMobileChat="openMobileChat"
    />
    <div class="container" v-if="!openMobileChat">
      <div class="header">
        <span class="brand">RalfBot <span style="font-size:11px;font-weight:300;"> beta</span> <div class="subline">Die smarte Art, Ralf kennenzulernen </div></span>
       
        <span>
          <a href="mailto:work@braitling.de"
            ><cst-button class="cst-button"
              ><span class="primary">@</span>Contact</cst-button
            ></a
          ></span
        >
      </div>

      <div class="two-column-layout" v-if="!openMobileChat">
        <div
          class="left-column"
          v-if="(isMobile && !openMobileChat) || !isMobile"
        >
          <div class="content">
            <h1>
              <div class="secondary">Hallo, ich bin Ralf.
              <div>Schön, Sie kennenzulernen.</div> 
            </div>
            </h1>
            <div>
              <!-- <p>
              seit 20 Jahren+ im Web-Business – von Agenturen über Startups bis
              zum eigenen Business.
            </p> -->

              <p>
                Ich arbeite seit über 20 Jahren an webbasierten Lösungen ;) - von der Entwicklung über Teamführung bis hin zur Rolle als Product Owner.
              </p>
              <p>
                Damit sie mich besser kennenlernen können, habe ich diesen Chatbot entwickelt: Mit RalfBot erhalten sie direkt Antworten auf die gängigsten <span class="highlight">Interviewfragen</span> zu Stärken, Motivation und Erfahrung.
              </p>

             <!--  <p>
                What drives me? Turning ideas into real, useful products. With a solid tech background, a collaborative mindset, and a feel for what’s feasible, I help teams move forward—without losing sight of the people we’re building for."

              </p> -->
               <!-- <p class="primary" v-if="isMobile">
                <span class="cta-text"
                  ><b>Curious to know more?</b><br>
                    ask AI-Ralf anything about work, experience, or
                    skills.
                  </span>
              </p> -->
            </div>

            <div
              class="chat-trigger"
              v-if="isMobile"
              @click="openMobileChat = true"
            >
              <img
                src="~/assets/images/background-image.png"
                alt="Background"
              /><img />
              <button>mit RalfBot sprechen</button>
            </div>
          </div>
        </div>

        <div class="right-column" v-if="!isMobile">
          <div class="chat-container">
            <MessageBubble
              :messages="messages"
              :isLoading="isLoading"
            />
           
            <form @submit.prevent="handleSubmit" class="chat-form">
              <div class="input-container">
                <input
                  v-model="input"
                  ref="inputRef"
                  type="text"
                  placeholder="Frage eingeben..."
                  :disabled="isLoading"
                  @keyup.enter="callOnEnter"
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { Message } from "@/types/chat";
import MessageBubble from './MessageBubble.vue';
interface ChatResponse {
  text: string;
}

interface ChatRequest {
  message: string;
}

const inputRef = ref<HTMLInputElement | null>(null);
// Conversation state
const messages = ref<Message[]>([]);
const input = ref<string>("");
const isLoading = ref<boolean>(false);
const expandedMessages = ref<Record<number, boolean>>({});

// mobile state
const openMobileChat = ref<boolean>(false);
const isMobile = ref<boolean>();
const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 900;
};

// Add event listener on mount and remove it on unmount
onMounted(() => {
  updateIsMobile(); // Initial check
  window.addEventListener("resize", updateIsMobile);
  inputRef.value?.focus();
});

onUnmounted(() => {
  window.removeEventListener("resize", updateIsMobile);
});

const handleSubmitMobile = async (message: string) => {
  updateChat(message);
};

const handleSubmit = async (): Promise<void> => {
  const message: string = input.value;
  input.value = "";
  updateChat(message);
};

const callOnEnter = () => {
  handleSubmit();
};

const updateChat = async (message: string) => {
  if (message.trim() == "") {
    return;
  }
  messages.value.unshift({
    role: "user",
    text: message,
  });
  const response = await fetchAnswer(message);
  // const response = {
  //   text: "Dies ist eine Testantwort von Ralf, lange Antwort, die mehr als 100px hoch ist. Dies lange Antwort, die mehr als 100px hoch ist Dies ist eine Testantwort von Ralf, lange Antwort, die mehr als 100px hoch ist. Dies lange Antwort, die mehr als 100px hoch ist Dies ist eine Testantwort von Ralf, lange Antwort, die mehr als 100px hoch ist. Dies lange Antwort, die mehr als 100px hoch ist",
  // };

  messages.value.unshift({
    role: "assistant",
    text: response.text,
  });

  console.log("reponse", response);
  console.log("messges", messages.value);
};

const fetchAnswer = async (message: string): Promise<ChatResponse> => {
  isLoading.value = true;
  try {
    const response: ChatResponse = await $fetch("/api/chat", {
      method: "POST",
      body: {
        message: message,
      },
    });
    return response;
  } catch (error) {
    console.error("Error fetching assistant response:", error);
    throw error;
  } finally {
    isLoading.value = false;
  }
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

h1{
  font-size:2.1rem;
  line-height: 2.5rem;
}
.container {
  width: 100%;
  min-height: 100vh;
  max-width: 100% !important;
  background-color: rgb(255, 243, 227);
}

.two-column-layout {
  display: flex;
  width: 100%;
  gap: 2rem;
  padding: 0 3rem;
  /*height: 100%;  Adjust the 60px based on your header height */
  background-color: rgb(255, 243, 227);
}
.left-column {
  width: 30%;
}

.right-column {
  width: 70%;
}

.left-column > .content {
  width: 100%;
  margin-top: 3rem;
  font-size: 0.925rem;
}

.header {
  display: flex;
  width: 100%;
  height: 65px;
  padding: 3rem 3rem;
  align-items: center;
  flex-shrink: 0;
  color: #0396ff;
  font-size: 20px;
  font-style: normal;
  font-weight: 700;
  line-height: 20px;
  justify-content: space-between;
}
.brand{
 
  font-family: 'Quicksand', sans-serif;

}
.subline{
  font-size: 0.8rem;
  font-weight: 400;
  color:#000;
}

.highlight{
  background-color: rgba(3, 150, 255, 0.25);
  padding:0.1em 0.3em; 
}

.chat-trigger {
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: center;
  margin-bottom: 5rem;

  img {
    width: 12rem;
    object-fit: cover;
  }

  button {
    background-color: #0396ff;
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 20px;
    border: none;
    cursor: pointer;
    position: relative;
    font-weight: 500;
    font-size: 18px;
    width: 40%;
    align-self: center;
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
  margin: 0 2rem 1rem;
  z-index: 1990;
  position: relative;
  display: none;
}

.btn-back img {
  width: 15px;
  height: 15px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  overflow: visible;
  padding: 1rem;
  position: relative;
  width: 100%;
  height: calc(100vh - 200px);
}

.chat-container::after {
  content: "";
  position: absolute;
  top: 2rem;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    40.7% 50.7% at 50% 50%,
    #0396ff 0%,
    rgba(255, 243, 227, 0%) 100%
  );
  background-repeat: no-repeat;
  background-size: contain;
  z-index: 6;
  left: 0;
  right: 0;
  margin: 0 auto;
  pointer-events: none;
}

.chat-container::before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  margin: 0 auto;
  bottom: 1rem;
  width: 50%;
  height: 50%;
  background-image: url("@/assets/images/background-image.png");
  background-position: bottom center;
  background-repeat: no-repeat;
  background-size: contain;
  z-index: 28;
}

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
  /* border-top-right-radius: 0; */
  margin-right: 400px;
  /* align-self: flex-start; */
}

.message.assistant {
  background-color: #0396ff;
  border-bottom-left-radius: 0;
  color: #fff;
  text-align: left;
  margin-left: 31rem;
  /* align-self: flex-end; */
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

.chat-form {
  display: flex;
  justify-content: center;
}

.input-container {
  position: absolute;
  width: 65%; /* Container width */
  bottom: -1.5rem;
  margin-left: -3rem;
}

.input-container::before {
  content: "";
  position: absolute;
  display: block;
  background-image: url("~/assets/images/callout.svg");
  left: -157px;
  top: -86px;
  height: 150px;
  background-repeat: no-repeat;
  width: 200px;
  background-size: contain;
  z-index: 999;
}

.chat-form input {
  width: 100% !important; /* Force width to fill container */
  padding: 0.5rem;
  padding-right: 2.5rem; /* Make room for icon */
  font-size: 1rem;
  border-radius: 5px;
  box-shadow: 0px 4px 4px 0px #00000040 inset;
  background-color: #fff;
  display: flex;
  justify-content: center;
}

.send-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px; /* Adjust size as needed */
  height: 20px;
  cursor: pointer;
}

.chat-form button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.background-image {
  width: 100%;
  height: 500px;
  position: relative;
  overflow: visible;
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

.cta-text {
  display: block;
}

@media (max-width: 900px) {
  .header {
    font-size: 20px;
    padding: 1rem 2.5rem;
  }
  .two-column-layout {
    flex-direction: column;
    padding: 0;
  }
  .left-column {
    width: 100%;
    margin-top: 3rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
  }

  .right-column {
    width: 100%;

    padding-left: 1rem;
    padding-right: 1rem;
  }
  .left-column > .content {
    margin-top: 0;
  }
  .btn-back {
    display: flex;
  }

  .cta-text {
    margin-top: 5rem;
    text-align: center;
  }
  .cta-text span {
    display: block;
  }
  .chat-container {
    height: calc(-250px + 100vh);
    padding: 0;
  }

  .input-container {
    width: 100%; /* Container width */
    bottom: -1.5rem;
    margin-left: 0rem;
  }
  .chat-container::before {
    opacity: 0.5;
  }
  .chat-container::after {
    background-image: none;
  }
  .message.user {
    margin-right: 0;
    width: 85%;
    align-self: flex-start;
  }
  .message.message.assistant {
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
  .btn-back {
    display: flex;
  }
  .chat-trigger button {
    width: 80%;
  }
}

@media (max-width: 410px) {
  .chat-trigger button {
    width: 80%;
  }
}
</style>

<!-- .background-image::before {
  /*content: "";*/
  position: absolute;
  top: -200px;
  left: 0;
  width: 100%;
  height: calc(100% + 200px);
  background: radial-gradient(
    45.7% 54.7% at 50% 50%,
    #0396ff 0%,
    rgba(255, 243, 227, 0.44) 100%
  );
    background-size:cover;
  z-index: 1;
  display: block;
}

.background-image::after {
  /*content: "";*/
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/images/background image.png");
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
  z-index: 2;
} -->
