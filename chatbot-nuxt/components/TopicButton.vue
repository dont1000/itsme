<template>
  <button
    @mouseenter="hovered = true"
    @mouseleave="hovered = false"
    @click="$emit('click')"
    :disabled="disabled"
    :style="{
      ...style.btn,
      background: asked ? HL : hovered ? '#fafafa' : '#fff',
      borderColor: asked ? HL : hovered ? '#111' : '#eaeaea',
      opacity: disabled && !asked ? 0.6 : 1,
    }"
  >
    <span :style="style.num">{{ topic.n }}</span>
    <span :style="style.label">{{ topic.label }}</span>
    <span :style="{
      ...style.arrow,
      transform: hovered || asked ? 'translateX(0)' : 'translateX(-4px)',
      opacity: hovered || asked ? 1 : 0.4,
    }">{{ asked ? '✓' : '↗' }}</span>
  </button>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const HL = '#D4F542';

defineProps<{
  topic: { n: string; label: string };
  asked: boolean;
  disabled: boolean;
}>();

defineEmits<{ click: [] }>();

const hovered = ref(false);

const style = {
  btn: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '14px',
    border: '1px solid #eaeaea',
    borderRadius: '8px',
    fontFamily: 'inherit',
    fontSize: '14px',
    fontWeight: 500,
    cursor: 'pointer',
    textAlign: 'left' as const,
    transition: 'all 0.18s ease',
    width: '100%',
    color: '#111',
  },
  num: {
    fontSize: '11px',
    color: '#999',
    fontFamily: "'JetBrains Mono', monospace",
    fontWeight: 400,
    flexShrink: 0,
  },
  label: { flex: 1 },
  arrow: {
    fontSize: '13px',
    color: '#111',
    transition: 'all 0.18s ease',
    flexShrink: 0,
  },
};
</script>
