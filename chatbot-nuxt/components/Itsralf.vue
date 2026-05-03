<template>
  <div :style="mn.root">

    <!-- Nav -->
    <nav :style="mn.nav">
      <div :style="mn.brand">
        <div :style="{ ...mn.brandSquare, background: HL }"></div>
        <span :style="mn.brandName">Ralf</span>
        <span :style="mn.brandSlash">/</span>
        <span :style="mn.brandRole">Personal Bot</span>
      </div>
      <div :style="mn.navRight">
        <span :style="mn.navLink">About</span>
        <span :style="mn.navLink">Work</span>
        <span :style="mn.navLink">CV</span>
        <a href="mailto:work@braitling.de" :style="{ ...mn.navCta, background: HL }">
          Kontakt <span style="margin-left: 6px">→</span>
        </a>
      </div>
    </nav>

    <!-- Body -->
    <div class="mn-body">

      <!-- LEFT: hero + topics + stats -->
      <div :style="mn.left">
        <div :style="mn.kicker">
          <span :style="{ ...mn.kickerDot, background: HL }"></span>
          <span :style="mn.kickerText">Verfügbar ab Q3 · 2026</span>
        </div>

        <h1 :style="mn.h1">
          Stell mir<br />
          <span :style="mn.h1Highlight">
            eine Frage
            <svg :style="mn.underline" viewBox="0 0 480 14" preserveAspectRatio="none">
              <path
                d="M2 8 Q 120 2, 240 7 T 478 6"
                :stroke="HL"
                stroke-width="6"
                fill="none"
                stroke-linecap="round"
              />
            </svg>
          </span><br />
          <span :style="mn.h1Light">statt zu lesen.</span>
        </h1>

        <p :style="mn.lede">
          20 Jahre Web — vom Entwickler zum Product Owner.
          Ein Chatbot, der für mich antwortet. Klar. Persönlich. Kurz.
        </p>

        <!-- Topic chips -->
        <div :style="mn.topicWrap">
          <div :style="mn.topicLabel">
            <span :style="mn.topicLabelNum">08</span>
            <span>Themen — eines wählen, oder eigene Frage stellen</span>
          </div>
          <div class="mn-topic-grid">
            <button
              v-for="t in topics"
              :key="t.id"
              @mouseenter="hoveredId = t.id"
              @mouseleave="hoveredId = null"
              @click="pick(t)"
              :disabled="isLoading"
              :style="{
                ...mn.topic,
                background: askedTopics.has(t.id) ? HL : hoveredId === t.id ? '#fafafa' : '#fff',
                borderColor: askedTopics.has(t.id) ? HL : hoveredId === t.id ? '#111' : '#eaeaea',
              }"
            >
              <span :style="mn.topicNum">{{ t.n }}</span>
              <span :style="mn.topicName">{{ t.label }}</span>
              <span :style="{
                ...mn.topicArrow,
                transform: hoveredId === t.id || askedTopics.has(t.id) ? 'translateX(0)' : 'translateX(-4px)',
                opacity: hoveredId === t.id || askedTopics.has(t.id) ? 1 : 0.4,
              }">↗</span>
            </button>
          </div>
        </div>

        <!-- Stats -->
        <div :style="mn.stats">
          <div :style="mn.stat">
            <div :style="mn.statN">20<span :style="mn.statPlus">+</span></div>
            <div :style="mn.statL">Jahre</div>
          </div>
          <div :style="mn.statSep"></div>
          <div :style="mn.stat">
            <div :style="mn.statN">03</div>
            <div :style="mn.statL">Rollen</div>
          </div>
          <div :style="mn.statSep"></div>
          <div :style="mn.stat">
            <div :style="mn.statN">∞</div>
            <div :style="mn.statL">Fragen</div>
          </div>
          <div :style="mn.statSep"></div>
          <div :style="mn.stat">
            <div :style="{ ...mn.statN, color: HL_DEEP }">●</div>
            <div :style="mn.statL">Live · Claude</div>
          </div>
        </div>
      </div>

      <!-- RIGHT: chat panel -->
      <div :style="mn.right">
        <div :style="mn.chatHead">
          <div :style="mn.chatHeadLeft">
            <div :style="{ ...mn.statusOrb, background: HL }">
              <div :style="mn.statusOrbInner"></div>
            </div>
            <div>
              <div :style="mn.chatTitle">Im Gespräch</div>
              <div :style="mn.chatSub">Antwort in ~2 Sek.</div>
            </div>
          </div>
          <div :style="mn.chatHeadCount">
            <span :style="mn.countN">{{ Math.ceil(messages.length / 2) }}</span>
            <span :style="mn.countL">Fragen heute</span>
          </div>
        </div>

        <div ref="scrollRef" :style="mn.thread">
          <div v-if="messages.length === 0 && !isLoading" :style="mn.empty">
            <div :style="{ ...mn.emptyTick, background: HL }"></div>
            <div :style="mn.emptyTitle">Bereit, wenn Sie es sind.</div>
            <div :style="mn.emptySub">
              Wählen Sie ein Thema links — oder tippen Sie unten Ihre eigene Frage.
            </div>
          </div>

          <template v-for="(m, i) in messages" :key="i">
            <div v-if="m.role === 'user'" :style="mn.qWrap">
              <div :style="mn.qLine"></div>
              <div :style="mn.qBubble">
                <div :style="mn.qLabel">Sie fragen</div>
                <div :style="mn.qText">{{ m.text }}</div>
              </div>
            </div>
            <div v-else :style="mn.aWrap">
              <div :style="{ ...mn.aSpine, background: HL }"></div>
              <div :style="mn.aBubble">
                <div :style="mn.aMeta">
                  <span :style="mn.aName">Ralf</span>
                  <span :style="mn.aDot">·</span>
                  <span :style="mn.aTime">{{ messageTimes[i] }}</span>
                </div>
                <div :style="mn.aText">{{ m.text }}</div>
              </div>
            </div>
          </template>

          <div v-if="isLoading" :style="mn.aWrap">
            <div :style="{ ...mn.aSpine, background: HL }"></div>
            <div :style="mn.aBubble">
              <div :style="mn.aMeta">
                <span :style="mn.aName">Ralf</span>
                <span :style="mn.aDot">·</span>
                <span :style="mn.aTime">denkt nach</span>
              </div>
              <div :style="mn.typing">
                <span :style="mn.tdot"></span>
                <span :style="{ ...mn.tdot, animationDelay: '.15s' }"></span>
                <span :style="{ ...mn.tdot, animationDelay: '.3s' }"></span>
              </div>
            </div>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" :style="mn.composer">
          <input
            v-model="input"
            placeholder="Eigene Frage stellen…"
            :style="mn.input"
            :disabled="isLoading"
          />
          <button
            type="submit"
            :disabled="isLoading || !input.trim()"
            :style="{
              ...mn.sendBtn,
              background: input.trim() ? HL : '#f0f0f0',
              color: input.trim() ? '#111' : '#bbb',
              cursor: input.trim() && !isLoading ? 'pointer' : 'default',
            }"
          >
            Senden <span :style="mn.sendArrow">↑</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import type { Message } from '@/types/chat';

const HL = '#D4F542';
const HL_DEEP = '#A8C932';

const messages = ref<Message[]>([]);
const messageTimes = ref<Record<number, string>>({});
const input = ref('');
const isLoading = ref(false);
const askedTopics = ref(new Set<string>());
const hoveredId = ref<string | null>(null);
const scrollRef = ref<HTMLElement | null>(null);

const topics = [
  { id: 'staerken', n: '01', label: 'Stärken',  q: 'Was sind deine größten Stärken?' },
  { id: 'projekt',  n: '02', label: 'Projekte', q: 'Erzähl mir von einem erfolgreichen Projekt.' },
  { id: 'team',     n: '03', label: 'Team',     q: 'Wie arbeitest du im Team?' },
  { id: 'po',       n: '04', label: 'Product',  q: 'Was reizt dich an Product Ownership?' },
  { id: 'konflikt', n: '05', label: 'Konflikt', q: 'Wie gehst du mit Konflikten um?' },
  { id: 'ai',       n: '06', label: 'AI · Tools', q: 'Wie nutzt du AI in deiner Arbeit?' },
  { id: 'lernen',   n: '07', label: 'Lernen',   q: 'Wie hältst du dein Wissen aktuell?' },
  { id: 'hire',     n: '08', label: 'Warum du', q: 'Warum sollten wir dich einstellen?' },
];

function now() {
  return new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
}

function pick(t: typeof topics[number]) {
  askedTopics.value = new Set([...askedTopics.value, t.id]);
  updateChat(t.q);
}

const handleSubmit = () => {
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  updateChat(msg);
};

const updateChat = async (message: string) => {
  messages.value.push({ role: 'user', text: message });
  const response = await fetchAnswer(message);
  const idx = messages.value.length;
  messageTimes.value[idx] = now();
  messages.value.push({ role: 'assistant', text: response.text });
};

const fetchAnswer = async (message: string): Promise<{ text: string }> => {
  isLoading.value = true;
  try {
    return await $fetch<{ text: string }>('/api/chat', {
      method: 'POST',
      body: { message },
    });
  } catch {
    return { text: 'Es tut mir leid, etwas ist schiefgelaufen.' };
  } finally {
    isLoading.value = false;
  }
};

watch([messages, isLoading], () => {
  nextTick(() => {
    if (scrollRef.value) scrollRef.value.scrollTop = scrollRef.value.scrollHeight;
  });
});

const mn = {
  root: {
    background: '#ffffff',
    color: '#111',
    fontFamily: 'Inter, system-ui, sans-serif',
    display: 'flex',
    flexDirection: 'column' as const,
    minHeight: '100vh',
  },
  nav: {
    height: '64px',
    padding: '0 40px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderBottom: '1px solid #f0f0f0',
    flexShrink: 0,
  },
  brand: { display: 'flex', alignItems: 'center', gap: '12px' },
  brandSquare: { width: '18px', height: '18px', borderRadius: '4px' },
  brandName: { fontSize: '16px', fontWeight: 600, letterSpacing: '-0.01em' },
  brandSlash: { color: '#ccc', fontWeight: 300 },
  brandRole: { fontSize: '14px', color: '#888' },
  navRight: { display: 'flex', alignItems: 'center', gap: '28px' },
  navLink: { fontSize: '14px', color: '#555', cursor: 'pointer' },
  navCta: {
    padding: '8px 16px',
    borderRadius: '99px',
    fontSize: '13px',
    fontWeight: 600,
    color: '#111',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    textDecoration: 'none',
  },

  left: {
    padding: '40px 48px',
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '28px',
    minHeight: 0,
    overflow: 'hidden',
  },
  kicker: { display: 'flex', alignItems: 'center', gap: '8px' },
  kickerDot: {
    width: '8px',
    height: '8px',
    borderRadius: '99px',
    animation: 'mn-pulse 2s infinite',
  },
  kickerText: {
    fontSize: '12px',
    color: '#666',
    fontFamily: "'JetBrains Mono', monospace",
    letterSpacing: '0.02em',
  },
  h1: {
    margin: 0,
    fontFamily: "'Inter Tight', sans-serif",
    fontSize: '72px',
    fontWeight: 600,
    lineHeight: 0.96,
    letterSpacing: '-0.035em',
    color: '#111',
  },
  h1Highlight: { position: 'relative' as const, display: 'inline-block' },
  h1Light: { fontWeight: 300, color: '#888', fontStyle: 'italic' },
  underline: {
    position: 'absolute' as const,
    left: 0,
    right: 0,
    bottom: '-8px',
    width: '100%',
    height: '14px',
  },
  lede: {
    margin: 0,
    fontSize: '16px',
    lineHeight: 1.55,
    maxWidth: '480px',
    color: '#555',
  },
  topicWrap: { display: 'flex', flexDirection: 'column' as const, gap: '12px' },
  topicLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    fontSize: '11px',
    color: '#888',
    fontFamily: "'JetBrains Mono', monospace",
    textTransform: 'uppercase' as const,
    letterSpacing: '0.1em',
  },
  topicLabelNum: {
    background: '#111',
    color: '#fff',
    padding: '2px 6px',
    borderRadius: '4px',
  },
  topic: {
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
  },
  topicNum: {
    fontSize: '11px',
    color: '#999',
    fontFamily: "'JetBrains Mono', monospace",
    fontWeight: 400,
  },
  topicName: { flex: 1 },
  topicArrow: { fontSize: '13px', color: '#111', transition: 'all 0.18s ease' },

  stats: {
    display: 'flex',
    alignItems: 'center',
    gap: '28px',
    padding: '20px 0',
    borderTop: '1px solid #f0f0f0',
    marginTop: 'auto',
  },
  stat: { display: 'flex', flexDirection: 'column' as const, gap: '4px' },
  statN: {
    fontSize: '32px',
    fontWeight: 600,
    lineHeight: 1,
    color: '#111',
    fontFamily: "'Inter Tight', sans-serif",
    letterSpacing: '-0.04em',
  },
  statPlus: { fontSize: '16px', color: '#888' },
  statL: {
    fontSize: '11px',
    color: '#888',
    textTransform: 'uppercase' as const,
    letterSpacing: '0.1em',
  },
  statSep: { width: '1px', height: '32px', background: '#f0f0f0' },

  right: {
    display: 'flex',
    flexDirection: 'column' as const,
    minHeight: 0,
    borderLeft: '1px solid #f0f0f0',
    background: '#fafafa',
  },
  chatHead: {
    padding: '24px 32px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: '1px solid #f0f0f0',
    background: '#fff',
    flexShrink: 0,
  },
  chatHeadLeft: { display: 'flex', alignItems: 'center', gap: '14px' },
  statusOrb: {
    width: '36px',
    height: '36px',
    borderRadius: '99px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusOrbInner: {
    width: '10px',
    height: '10px',
    borderRadius: '99px',
    background: '#111',
    animation: 'mn-pulse 2s infinite',
  },
  chatTitle: { fontSize: '14px', fontWeight: 600, color: '#111' },
  chatSub: { fontSize: '12px', color: '#888', marginTop: '2px' },
  chatHeadCount: { display: 'flex', flexDirection: 'column' as const, alignItems: 'flex-end' },
  countN: {
    fontSize: '22px',
    fontWeight: 600,
    color: '#111',
    fontFamily: "'Inter Tight', sans-serif",
  },
  countL: {
    fontSize: '10px',
    color: '#888',
    textTransform: 'uppercase' as const,
    letterSpacing: '0.1em',
  },
  thread: {
    flex: 1,
    overflowY: 'auto' as const,
    padding: '28px 32px',
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '22px',
    minHeight: 0,
  },
  empty: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'flex-start',
    justifyContent: 'center',
    gap: '14px',
    padding: '40px 0',
  },
  emptyTick: { width: '64px', height: '4px', borderRadius: '99px' },
  emptyTitle: {
    fontSize: '28px',
    fontWeight: 600,
    color: '#111',
    fontFamily: "'Inter Tight', sans-serif",
    letterSpacing: '-0.02em',
  },
  emptySub: { fontSize: '14px', color: '#888', maxWidth: '320px', lineHeight: 1.5 },

  qWrap: { display: 'flex', alignItems: 'flex-start', gap: '14px' },
  qLine: { width: '2px', alignSelf: 'stretch', background: '#111', borderRadius: '1px', flexShrink: 0 },
  qBubble: { flex: 1 },
  qLabel: {
    fontSize: '11px',
    color: '#888',
    textTransform: 'uppercase' as const,
    letterSpacing: '0.12em',
    marginBottom: '6px',
    fontFamily: "'JetBrains Mono', monospace",
  },
  qText: { fontSize: '18px', lineHeight: 1.4, color: '#111', fontWeight: 500, letterSpacing: '-0.01em' },

  aWrap: { display: 'flex', alignItems: 'flex-start', gap: '14px' },
  aSpine: { width: '2px', alignSelf: 'stretch', borderRadius: '1px', flexShrink: 0 },
  aBubble: { flex: 1 },
  aMeta: { display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' },
  aName: { fontSize: '12px', fontWeight: 600, color: '#111', textTransform: 'uppercase' as const, letterSpacing: '0.1em' },
  aDot: { color: '#ccc' },
  aTime: { fontSize: '11px', color: '#888', fontFamily: "'JetBrains Mono', monospace" },
  aText: { fontSize: '15px', lineHeight: 1.65, color: '#222' },

  typing: { display: 'flex', alignItems: 'center', gap: '4px', padding: '4px 0' },
  tdot: {
    width: '7px',
    height: '7px',
    borderRadius: '99px',
    background: '#111',
    display: 'inline-block',
    animation: 'mn-typing 1.2s infinite',
  },

  composer: {
    padding: '16px 24px 24px',
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
    background: '#fff',
    borderTop: '1px solid #f0f0f0',
    flexShrink: 0,
  },
  input: {
    flex: 1,
    height: '52px',
    border: '1px solid #eaeaea',
    borderRadius: '99px',
    padding: '0 22px',
    fontFamily: 'inherit',
    fontSize: '15px',
    color: '#111',
    outline: 'none',
    background: '#fff',
  },
  sendBtn: {
    height: '52px',
    padding: '0 22px',
    borderRadius: '99px',
    border: 'none',
    fontFamily: 'inherit',
    fontSize: '14px',
    fontWeight: 600,
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    transition: 'all 0.18s ease',
    flexShrink: 0,
  },
  sendArrow: { fontSize: '16px', fontWeight: 700 },
};
</script>

<style>
@keyframes mn-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.6); opacity: 0.5; }
}
@keyframes mn-typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-3px); opacity: 1; }
}

.mn-body {
  flex: 1;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  min-height: 0;
  height: calc(100vh - 64px);
}

.mn-topic-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

@media (max-width: 900px) {
  .mn-body {
    grid-template-columns: 1fr;
    height: auto;
    overflow: auto;
  }
  .mn-topic-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
