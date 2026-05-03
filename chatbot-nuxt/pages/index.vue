<template>
  <div class="">
    <Chatbot />
  </div>
</template>

<script setup>
import Chatbot from "~/components/Itsralf.vue"
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }
  ],
  title: 'Chat'
})
</script>