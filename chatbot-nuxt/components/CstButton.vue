<template>
  <button 
    class="custom-button" 
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">

</script>

<style scoped>
.custom-button {
  padding: 2px 10px;
  border-radius: 5px;
  cursor: pointer;
  border: 1px solid #000;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}
.custom-button:hover{
  border-color: #0396ff
}

.custom-button.primary {
  background-color: #0396ff;
  color: white;
}

.custom-button.primary:hover {
  background-color: #0280db;
}

.custom-button.secondary {
  background-color: transparent;
  color: #0396ff;
  text-decoration: underline;
}

.custom-button.secondary:hover {
  color: #0280db;
}
</style>