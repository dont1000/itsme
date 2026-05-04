<template>

  <!-- ── MOBILE ─────────────────────────────────────────────────── -->
  <div v-if="isMobile" :style="mb.root">

    <!-- Header -->
    <div :style="mb.header">
      <div :style="mb.brandRow">
        <div :style="mb.dot"></div>
        <div class="mono" :style="mb.brand">ralf<span :style="{ color: HL }">.</span>chat</div>
        <div style="flex:1"></div>
        <button
          :style="{ ...mb.tabBtn, ...(view === 'home' ? mb.tabActive : {}) }"
          @click="view = 'home'"
        >home</button>
        <button
          :style="{ ...mb.tabBtn, ...(view === 'thread' ? mb.tabActive : {}) }"
          @click="view = 'thread'"
        >
          chat
          <span v-if="messages.length > 0" :style="mb.badge">{{ Math.ceil(messages.length / 2) }}</span>
        </button>
      </div>
    </div>

    <!-- HOME view -->
    <div v-if="view === 'home'" :style="mb.scrollArea">
      <div :style="mb.intro">
        <div class="mono" :style="mb.kicker">
          <span :style="mb.eyeDot"></span> session #2026.05 · live
        </div>
        <h1 class="display" :style="mb.h1">
          Hi. Ich bin <span :style="{ color: HL }">Ralf</span>.<br/>
          Eine API für Erfahrung.
        </h1>
        <p :style="mb.lede">
          20+ Jahre Web. Dev → Lead → Product Owner.
          <strong style="color:#111">Wählen Sie ein Modul</strong> oder tippen Sie eine eigene Frage.
        </p>
        <div :style="mb.metricRow">
          <div :style="mb.metric">
            <div class="display" :style="mb.metricN">20<span style="font-size:14px">+</span></div>
            <div class="mono" :style="mb.metricL">Jahre</div>
          </div>
          <div :style="mb.metricSep"></div>
          <div :style="mb.metric">
            <div class="display" :style="mb.metricN">3</div>
            <div class="mono" :style="mb.metricL">Rollen</div>
          </div>
          <div :style="mb.metricSep"></div>
          <div :style="mb.metric">
            <div class="display" :style="mb.metricN">∞</div>
            <div class="mono" :style="mb.metricL">Fragen</div>
          </div>
        </div>
      </div>

      <!-- Topic list -->
      <div :style="mb.section">
        <div class="mono" :style="mb.sectionHead">
          <span>› topics.json</span>
          <span style="color:#6b7a93">{{ topics.length }} entries</span>
        </div>
        <div :style="mb.topicList">
          <TopicButton
            v-for="t in topics"
            :key="t.id"
            :topic="t"
            :asked="askedTopics.has(t.id)"
            :disabled="isLoading"
            @click="pickMobile(t)"
          />
        </div>
      </div>

      <!-- Contact -->
      <div :style="mb.section">
        <div class="mono" :style="mb.sectionHead"><span>› contact.txt</span></div>
        <div :style="mb.contactCard">
          <div class="mono" :style="mb.contactLine">
            <span style="color:#6b7a93">mail </span>
            <a href="mailto:work@braitling.de" style="color:#111;text-decoration:none">work@braitling.de</a>
          </div>
          <div class="mono" :style="mb.contactLine">
            <span style="color:#888">location </span>
            <span style="color:#111">München</span>
          </div>
          <div class="mono" :style="mb.contactLine">
            <span style="color:#6b7a93">status </span>
            <span style="color:#16a34a">● verfügbar ab Q3 · 2026</span>
          </div>
        </div>
      </div>
      <div style="height:16px"></div>
    </div>

    <!-- THREAD view -->
    <div v-if="view === 'thread'" ref="scrollRef" :style="mb.thread">
      <div class="mono" :style="mb.threadHead">
        › stdout · {{ messages.length }} {{ messages.length === 1 ? 'message' : 'messages' }}
      </div>

      <div v-if="messages.length === 0 && !isLoading" :style="mb.empty">
        <div :style="mb.emptyMark">?</div>
        <div class="display" :style="mb.emptyText">Awaiting input.</div>
        <button :style="mb.emptyBack" @click="view = 'home'">← Themen wählen</button>
      </div>

      <template v-for="(m, i) in messages" :key="i">
        <div v-if="m.role === 'user'" :style="mb.qRow">
          <div :style="mb.qBubble">
            <div class="mono" :style="mb.qLabel">you ›</div>
            <div :style="mb.qText">{{ m.text }}</div>
          </div>
        </div>
        <div v-else :style="mb.aRow">
          <div :style="mb.aAvatar">R</div>
          <div :style="mb.aBubble">
            <div class="mono" :style="mb.aMeta">ralf · {{ messageTimes[i] }}</div>
            <div :style="mb.aText">{{ m.text }}</div>
          </div>
        </div>
      </template>

      <div v-if="isLoading" :style="mb.aRow">
        <div :style="mb.aAvatar">R</div>
        <div :style="mb.aBubble">
          <div class="mono" :style="mb.aMeta">denkt nach…</div>
          <div style="color:#6b7a93">
            <span :style="mb.tdot"></span>
            <span :style="{ ...mb.tdot, animationDelay: '.15s' }"></span>
            <span :style="{ ...mb.tdot, animationDelay: '.3s' }"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Composer (always visible) -->
    <form @submit.prevent="handleSubmit" :style="mb.composer">
      <div :style="mb.composerInner">
        <span class="mono" style="color:#3b82f6;font-size:13px">›</span>
        <input
          v-model="input"
          placeholder="frage tippen…"
          :style="mb.input"
          :disabled="isLoading"
        />
        <button
          type="submit"
          :disabled="isLoading || !input.trim()"
          :style="{ ...mb.sendBtn, opacity: input.trim() ? 1 : 0.4 }"
        >↑</button>
      </div>
    </form>
  </div>

  <!-- ── DESKTOP ─────────────────────────────────────────────────── -->
  <div v-else :style="mn.root">

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
          Kontakt <span style="margin-left:6px">→</span>
        </a>
      </div>
    </nav>

    <div class="mn-body">

      <!-- LEFT -->
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
              <path d="M2 8 Q 120 2, 240 7 T 478 6" :stroke="HL" stroke-width="6" fill="none" stroke-linecap="round" />
            </svg>
          </span><br />
        </h1>

        <p :style="mn.lede">
          20 Jahre Web — vom Entwickler zum Product Owner.
          Ein Chatbot, der für mich antwortet. Klar. Persönlich. Kurz.
        </p>

        <div :style="mn.topicWrap">
          <div :style="mn.topicLabel">
            <span :style="mn.topicLabelNum">08</span>
            <span>Themen — eines wählen, oder eigene Frage stellen</span>
          </div>
          <div class="mn-topic-grid">
            <TopicButton
              v-for="t in topics"
              :key="t.id"
              :topic="t"
              :asked="askedTopics.has(t.id)"
              :disabled="isLoading"
              @click="pick(t)"
            />
          </div>
        </div>

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

      <!-- RIGHT: chat -->
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
            <div :style="mn.emptySub">Wählen Sie ein Thema links — oder tippen Sie unten Ihre eigene Frage.</div>
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
          <input v-model="input" placeholder="Eigene Frage stellen…" :style="mn.input" :disabled="isLoading" />
          <button
            type="submit"
            :disabled="isLoading || !input.trim()"
            :style="{
              ...mn.sendBtn,
              background: input.trim() ? HL : '#f0f0f0',
              color: input.trim() ? '#111' : '#bbb',
              cursor: input.trim() && !isLoading ? 'pointer' : 'default',
            }"
          >Senden <span :style="mn.sendArrow">↑</span></button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue';
import type { Message } from '@/types/chat';

// ── Accent colours (desktop) ──────────────────────────────────────
const HL     = '#D4F542';
const HL_DEEP = '#A8C932';

// ── Shared state ──────────────────────────────────────────────────
const messages     = ref<Message[]>([]);
const messageTimes = ref<Record<number, string>>({});
const input        = ref('');
const isLoading    = ref(false);
const askedTopics  = ref(new Set<string>());
const scrollRef    = ref<HTMLElement | null>(null);

// ── Mobile state ──────────────────────────────────────────────────
const isMobile = ref(false);
const view     = ref<'home' | 'thread'>('home');

function checkMobile() { isMobile.value = window.innerWidth < 900; }
onMounted(() => { checkMobile(); window.addEventListener('resize', checkMobile); });
onUnmounted(() => window.removeEventListener('resize', checkMobile));

// ── Topics (shared) ───────────────────────────────────────────────
const topics = [
  { id: 'staerken', n: '01', label: 'Stärken',    icon: '◆', accent: '#3b82f6', q: 'Was sind deine größten Stärken?' },
  { id: 'projekt',  n: '02', label: 'Projekte',   icon: '▣', accent: '#22d3ee', q: 'Erzähl mir von einem erfolgreichen Projekt.' },
  { id: 'team',     n: '03', label: 'Team',       icon: '◈', accent: '#60a5fa', q: 'Wie arbeitest du im Team?' },
  { id: 'po',       n: '04', label: 'Product',    icon: '◉', accent: '#818cf8', q: 'Was reizt dich an Product Ownership?' },
  { id: 'konflikt', n: '05', label: 'Konflikt',   icon: '◐', accent: '#0ea5e9', q: 'Wie gehst du mit Konflikten um?' },
  { id: 'ai',       n: '06', label: 'AI · Tools', icon: '✦', accent: '#06b6d4', q: 'Wie nutzt du AI in deiner Arbeit?' },
  { id: 'lernen',   n: '07', label: 'Lernen',     icon: '◇', accent: '#7c8cf8', q: 'Wie hältst du dein Wissen aktuell?' },
  { id: 'hire',     n: '08', label: 'Warum du',   icon: '★', accent: '#2563eb', q: 'Warum sollten wir dich einstellen?' },
];

// ── Chat logic ────────────────────────────────────────────────────
function now() {
  return new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
}

function pick(t: typeof topics[number]) {
  askedTopics.value = new Set([...askedTopics.value, t.id]);
  updateChat(t.q);
}

function pickMobile(t: typeof topics[number]) {
  askedTopics.value = new Set([...askedTopics.value, t.id]);
  view.value = 'thread';
  updateChat(t.q);
}

const handleSubmit = () => {
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  if (isMobile.value) view.value = 'thread';
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

// ── Desktop styles ────────────────────────────────────────────────
const mn = {
  root: { background: '#fff', color: '#111', fontFamily: 'Inter, system-ui, sans-serif', display: 'flex', flexDirection: 'column' as const, minHeight: '100vh' },
  nav: { height: '64px', padding: '0 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #f0f0f0', flexShrink: 0 },
  brand: { display: 'flex', alignItems: 'center', gap: '12px' },
  brandSquare: { width: '18px', height: '18px', borderRadius: '4px' },
  brandName: { fontSize: '16px', fontWeight: 600, letterSpacing: '-0.01em' },
  brandSlash: { color: '#ccc', fontWeight: 300 },
  brandRole: { fontSize: '14px', color: '#888' },
  navRight: { display: 'flex', alignItems: 'center', gap: '28px' },
  navLink: { fontSize: '14px', color: '#555', cursor: 'pointer' },
  navCta: { padding: '8px 16px', borderRadius: '99px', fontSize: '13px', fontWeight: 600, color: '#111', cursor: 'pointer', display: 'flex', alignItems: 'center', textDecoration: 'none' },
  left: { padding: '40px 48px', display: 'flex', flexDirection: 'column' as const, gap: '28px', minHeight: 0, overflow: 'hidden' },
  kicker: { display: 'flex', alignItems: 'center', gap: '8px' },
  kickerDot: { width: '8px', height: '8px', borderRadius: '99px', animation: 'mn-pulse 2s infinite' },
  kickerText: { fontSize: '12px', color: '#666', fontFamily: "'JetBrains Mono', monospace", letterSpacing: '0.02em' },
  h1: { margin: 0, fontFamily: "'Inter Tight', sans-serif", fontSize: '72px', fontWeight: 600, lineHeight: 0.96, letterSpacing: '-0.035em', color: '#111' },
  h1Highlight: { position: 'relative' as const, display: 'inline-block' },
  h1Light: { fontWeight: 300, color: '#888', fontStyle: 'italic' },
  underline: { position: 'absolute' as const, left: 0, right: 0, bottom: '-8px', width: '100%', height: '14px' },
  lede: { margin: 0, fontSize: '16px', lineHeight: 1.55, maxWidth: '480px', color: '#555' },
  topicWrap: { display: 'flex', flexDirection: 'column' as const, gap: '12px' },
  topicLabel: { display: 'flex', alignItems: 'center', gap: '10px', fontSize: '11px', color: '#888', fontFamily: "'JetBrains Mono', monospace", textTransform: 'uppercase' as const, letterSpacing: '0.1em' },
  topicLabelNum: { background: '#111', color: '#fff', padding: '2px 6px', borderRadius: '4px' },
  topic: { display: 'flex', alignItems: 'center', gap: '10px', padding: '14px', border: '1px solid #eaeaea', borderRadius: '8px', fontFamily: 'inherit', fontSize: '14px', fontWeight: 500, cursor: 'pointer', textAlign: 'left' as const, transition: 'all 0.18s ease' },
  topicNum: { fontSize: '11px', color: '#999', fontFamily: "'JetBrains Mono', monospace", fontWeight: 400 },
  topicName: { flex: 1 },
  topicArrow: { fontSize: '13px', color: '#111', transition: 'all 0.18s ease' },
  stats: { display: 'flex', alignItems: 'center', gap: '28px', padding: '20px 0', borderTop: '1px solid #f0f0f0', marginTop: 'auto' },
  stat: { display: 'flex', flexDirection: 'column' as const, gap: '4px' },
  statN: { fontSize: '32px', fontWeight: 600, lineHeight: 1, color: '#111', fontFamily: "'Inter Tight', sans-serif", letterSpacing: '-0.04em' },
  statPlus: { fontSize: '16px', color: '#888' },
  statL: { fontSize: '11px', color: '#888', textTransform: 'uppercase' as const, letterSpacing: '0.1em' },
  statSep: { width: '1px', height: '32px', background: '#f0f0f0' },
  right: { display: 'flex', flexDirection: 'column' as const, minHeight: 0, borderLeft: '1px solid #f0f0f0', background: '#fafafa' },
  chatHead: { padding: '24px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #f0f0f0', background: '#fff', flexShrink: 0 },
  chatHeadLeft: { display: 'flex', alignItems: 'center', gap: '14px' },
  statusOrb: { width: '36px', height: '36px', borderRadius: '99px', display: 'flex', alignItems: 'center', justifyContent: 'center' },
  statusOrbInner: { width: '10px', height: '10px', borderRadius: '99px', background: '#111', animation: 'mn-pulse 2s infinite' },
  chatTitle: { fontSize: '14px', fontWeight: 600, color: '#111' },
  chatSub: { fontSize: '12px', color: '#888', marginTop: '2px' },
  chatHeadCount: { display: 'flex', flexDirection: 'column' as const, alignItems: 'flex-end' },
  countN: { fontSize: '22px', fontWeight: 600, color: '#111', fontFamily: "'Inter Tight', sans-serif" },
  countL: { fontSize: '10px', color: '#888', textTransform: 'uppercase' as const, letterSpacing: '0.1em' },
  thread: { flex: 1, overflowY: 'auto' as const, padding: '28px 32px', display: 'flex', flexDirection: 'column' as const, gap: '22px', minHeight: 0 },
  empty: { flex: 1, display: 'flex', flexDirection: 'column' as const, alignItems: 'flex-start', justifyContent: 'center', gap: '14px', padding: '40px 0' },
  emptyTick: { width: '64px', height: '4px', borderRadius: '99px' },
  emptyTitle: { fontSize: '28px', fontWeight: 600, color: '#111', fontFamily: "'Inter Tight', sans-serif", letterSpacing: '-0.02em' },
  emptySub: { fontSize: '14px', color: '#888', maxWidth: '320px', lineHeight: 1.5 },
  qWrap: { display: 'flex', alignItems: 'flex-start', gap: '14px' },
  qLine: { width: '2px', alignSelf: 'stretch', background: '#111', borderRadius: '1px', flexShrink: 0 },
  qBubble: { flex: 1 },
  qLabel: { fontSize: '11px', color: '#888', textTransform: 'uppercase' as const, letterSpacing: '0.12em', marginBottom: '6px', fontFamily: "'JetBrains Mono', monospace" },
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
  tdot: { width: '7px', height: '7px', borderRadius: '99px', background: '#111', display: 'inline-block', animation: 'mn-typing 1.2s infinite' },
  composer: { padding: '16px 24px 24px', display: 'flex', gap: '10px', alignItems: 'center', background: '#fff', borderTop: '1px solid #f0f0f0', flexShrink: 0 },
  input: { flex: 1, height: '52px', border: '1px solid #eaeaea', borderRadius: '99px', padding: '0 22px', fontFamily: 'inherit', fontSize: '15px', color: '#111', outline: 'none', background: '#fff' },
  sendBtn: { height: '52px', padding: '0 22px', borderRadius: '99px', border: 'none', fontFamily: 'inherit', fontSize: '14px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px', transition: 'all 0.18s ease', flexShrink: 0 },
  sendArrow: { fontSize: '16px', fontWeight: 700 },
};

// ── Mobile styles (same theme as desktop) ─────────────────────────
const mb = {
  root: { width: '100%', minHeight: '100dvh', background: '#fff', color: '#111', display: 'flex', flexDirection: 'column' as const, fontFamily: 'Inter, system-ui, sans-serif' },
  header: { padding: '52px 16px 12px', borderBottom: '1px solid #f0f0f0', background: '#fff', flexShrink: 0 },
  brandRow: { display: 'flex', alignItems: 'center', gap: '8px' },
  dot: { width: '8px', height: '8px', borderRadius: '99px', background: HL, animation: 'mn-pulse 2s infinite' },
  brand: { fontSize: '15px', fontWeight: 600, letterSpacing: '-0.01em', color: '#111' },
  tabBtn: { background: 'transparent', border: '1px solid #eaeaea', color: '#888', fontSize: '11px', padding: '5px 12px', borderRadius: '99px', fontFamily: "'JetBrains Mono', monospace", cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' },
  tabActive: { background: '#111', borderColor: '#111', color: '#fff' },
  badge: { background: 'rgba(255,255,255,0.3)', padding: '0 5px', borderRadius: '99px', fontSize: '9px' },
  scrollArea: { flex: 1, overflowY: 'auto' as const, paddingBottom: '12px' },
  intro: { padding: '24px 20px 16px' },
  kicker: { fontSize: '10px', color: '#888', letterSpacing: '0.14em', textTransform: 'uppercase' as const, display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' },
  eyeDot: { width: '6px', height: '6px', borderRadius: '99px', background: '#16a34a', display: 'inline-block' },
  h1: { margin: 0, fontFamily: "'Inter Tight', sans-serif", fontSize: '32px', fontWeight: 600, lineHeight: 1.05, letterSpacing: '-0.03em', color: '#111' },
  lede: { margin: '12px 0 0', fontSize: '14px', lineHeight: 1.55, color: '#555' },
  metricRow: { marginTop: '18px', display: 'flex', alignItems: 'center', gap: '12px', padding: '12px 14px', background: '#fafafa', border: '1px solid #f0f0f0', borderRadius: '10px' },
  metric: { display: 'flex', flexDirection: 'column' as const, gap: '2px' },
  metricN: { fontSize: '24px', fontWeight: 600, lineHeight: 1, color: '#111', fontFamily: "'Inter Tight', sans-serif", letterSpacing: '-0.04em' },
  metricL: { fontSize: '9px', color: '#888', letterSpacing: '0.12em', textTransform: 'uppercase' as const },
  metricSep: { width: '1px', height: '28px', background: '#eaeaea' },
  section: { padding: '8px 16px' },
  sectionHead: { fontSize: '10px', color: '#888', letterSpacing: '0.1em', padding: '12px 4px 10px', display: 'flex', justifyContent: 'space-between', fontFamily: "'JetBrains Mono', monospace" },
  topicList: { display: 'flex', flexDirection: 'column' as const, gap: '6px' },
  topicRow: { display: 'flex', alignItems: 'center', gap: '12px', padding: '12px 14px', background: '#fff', border: '1px solid #eaeaea', borderRadius: '8px', cursor: 'pointer', textAlign: 'left' as const, fontFamily: 'inherit', color: '#111', width: '100%', transition: 'border-color 0.15s ease' },
  topicIdx: { fontSize: '10px', color: '#bbb', letterSpacing: '0.08em', width: '18px', flexShrink: 0, fontFamily: "'JetBrains Mono', monospace" },
  topicIcon: { width: '28px', height: '28px', borderRadius: '6px', border: '1px solid', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '13px', flexShrink: 0 },
  topicMain: { flex: 1, minWidth: 0 },
  topicLabel: { fontSize: '13px', color: '#111', fontWeight: 500 },
  topicQ: { fontSize: '11.5px', color: '#888', marginTop: '2px', lineHeight: 1.35, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' as const },
  topicArr: { fontSize: '14px', color: '#bbb' },
  contactCard: { background: '#fafafa', border: '1px solid #f0f0f0', borderRadius: '8px', padding: '12px', display: 'flex', flexDirection: 'column' as const, gap: '6px' },
  contactLine: { fontSize: '12px', lineHeight: 1.5, fontFamily: "'JetBrains Mono', monospace", color: '#555' },
  thread: { flex: 1, overflowY: 'auto' as const, padding: '16px 16px', display: 'flex', flexDirection: 'column' as const, gap: '16px' },
  threadHead: { fontSize: '10px', color: '#bbb', letterSpacing: '0.1em', paddingBottom: '4px', fontFamily: "'JetBrains Mono', monospace" },
  empty: { flex: 1, display: 'flex', flexDirection: 'column' as const, alignItems: 'center', justifyContent: 'center', gap: '12px', padding: '40px', color: '#bbb' },
  emptyMark: { width: '56px', height: '56px', borderRadius: '14px', border: '2px dashed #eaeaea', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '26px', color: '#ccc' },
  emptyText: { fontSize: '16px', color: '#888', fontFamily: "'Inter Tight', sans-serif" },
  emptyBack: { marginTop: '8px', background: 'transparent', border: '1px solid #eaeaea', color: '#555', padding: '7px 16px', borderRadius: '99px', fontSize: '12px', fontFamily: "'JetBrains Mono', monospace", cursor: 'pointer' },
  qRow: { display: 'flex', justifyContent: 'flex-start' },
  qBubble: { maxWidth: '82%', background: '#fff', border: '1px solid #eaeaea', color: '#111', padding: '10px 14px', borderRadius: '14px 14px 14px 4px' },
  qLabel: { fontSize: '9px', letterSpacing: '0.14em', textTransform: 'uppercase' as const, color: '#bbb', marginBottom: '4px', fontFamily: "'JetBrains Mono', monospace" },
  qText: { fontSize: '14px', lineHeight: 1.4, color: '#111', fontWeight: 500 },
  aRow: { display: 'flex', gap: '10px', alignItems: 'flex-start' },
  aAvatar: { width: '28px', height: '28px', borderRadius: '99px', background: HL, color: '#111', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '11px', flexShrink: 0, fontFamily: "'Inter Tight', sans-serif" },
  aBubble: { flex: 1, background: '#fafafa', border: '1px solid #f0f0f0', padding: '10px 14px', borderRadius: '4px 14px 14px 14px' },
  aMeta: { fontSize: '9px', color: '#bbb', letterSpacing: '0.1em', marginBottom: '4px', textTransform: 'uppercase' as const, fontFamily: "'JetBrains Mono', monospace" },
  aText: { fontSize: '14px', lineHeight: 1.55, color: '#222' },
  tdot: { width: '5px', height: '5px', borderRadius: '99px', background: '#bbb', display: 'inline-block', margin: '0 2px', animation: 'mn-typing 1.2s infinite' },
  composer: { padding: '8px 14px 16px', background: '#fff', borderTop: '1px solid #f0f0f0', flexShrink: 0 },
  composerInner: { display: 'flex', alignItems: 'center', gap: '8px', background: '#fafafa', border: '1px solid #eaeaea', borderRadius: '99px', padding: '6px 6px 6px 16px' },
  input: { flex: 1, border: 'none', background: 'transparent', outline: 'none', fontSize: '14px', color: '#111', fontFamily: 'inherit', minWidth: 0 },
  sendBtn: { width: '34px', height: '34px', borderRadius: '99px', border: 'none', background: HL, color: '#111', cursor: 'pointer', fontSize: '15px', fontWeight: 700, flexShrink: 0 },
};
</script>

<style>
@keyframes mn-pulse  { 0%,100% { transform:scale(1);  opacity:1   } 50% { transform:scale(0.6); opacity:0.5 } }
@keyframes mn-typing { 0%,60%,100% { transform:translateY(0); opacity:0.4 } 30% { transform:translateY(-3px); opacity:1 } }

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
.mono    { font-family: 'JetBrains Mono', monospace; }
.display { font-family: 'Inter Tight', sans-serif; }
</style>
