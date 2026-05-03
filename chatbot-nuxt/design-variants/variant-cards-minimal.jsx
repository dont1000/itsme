/* global React */
const { useState: useStateMin, useRef: useRefMin, useEffect: useEffectMin } = React;

/**
 * Card-stack v04 — Modern Minimalistic Edition.
 * One bold highlight: a saturated lime/chartreuse against pure white & deep ink.
 * Asymmetric layout: oversized type + sparse grid + a single accent that
 * "passes" between the question card and the answer card as a graphic line.
 */
function VariantCardsMinimal() {
  const HL = '#D4F542'; // bold electric lime — single highlight
  const HL_DEEP = '#A8C932'; // for hover/depth

  const { messages, pending, draft, setDraft, send } = window.useChat(window.RALF_PROMPT, []);
  const [askedTopics, setAskedTopics] = useStateMin(new Set());
  const [hoveredId, setHoveredId] = useStateMin(null);
  const scrollRef = useRefMin(null);

  useEffectMin(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages, pending]);

  const topics = [
  { id: 'staerken', n: '01', label: 'Stärken', q: 'Was sind deine größten Stärken?' },
  { id: 'projekt', n: '02', label: 'Projekte', q: 'Erzähl mir von einem erfolgreichen Projekt.' },
  { id: 'team', n: '03', label: 'Team', q: 'Wie arbeitest du im Team?' },
  { id: 'po', n: '04', label: 'Product', q: 'Was reizt dich an Product Ownership?' },
  { id: 'konflikt', n: '05', label: 'Konflikt', q: 'Wie gehst du mit Konflikten um?' },
  { id: 'ai', n: '06', label: 'AI · Tools', q: 'Wie nutzt du AI in deiner Arbeit?' },
  { id: 'lernen', n: '07', label: 'Lernen', q: 'Wie hältst du dein Wissen aktuell?' },
  { id: 'hire', n: '08', label: 'Warum du', q: 'Warum sollten wir dich einstellen?' }];


  function pick(t) {
    setAskedTopics((prev) => new Set(prev).add(t.id));
    send(t.q);
  }

  return (
    <div className="artboard" style={mn.root}>
      {/* Top nav — minimal, single line */}
      <div style={mn.nav}>
        <div style={mn.brand}>
          <div style={{ ...mn.brandSquare, background: HL }}></div>
          <span style={mn.brandName}>Ralf</span>
          <span style={mn.brandSlash}>/</span>
          <span style={mn.brandRole}>Personal Bot</span>
        </div>
        <div style={mn.navRight}>
          <span style={mn.navLink}>About</span>
          <span style={mn.navLink}>Work</span>
          <span style={mn.navLink}>CV</span>
          <span style={{ ...mn.navCta, background: HL }}>
            Kontakt <span style={{ marginLeft: 6 }}>→</span>
          </span>
        </div>
      </div>

      {/* Main */}
      <div style={mn.body}>
        {/* LEFT: hero + topics */}
        <div style={mn.left}>
          <div style={mn.kicker}>
            <span style={{ ...mn.kickerDot, background: HL }}></span>
            <span style={mn.kickerText}>Verfügbar ab Q3 · 2026</span>
          </div>

          <h1 style={mn.h1}>
            Stell mir<br />
            <span style={mn.h1Highlight}>
              eine Frage
              <svg style={mn.underline} viewBox="0 0 480 14" preserveAspectRatio="none">
                <path d="M2 8 Q 120 2, 240 7 T 478 6" stroke={HL} strokeWidth="6" fill="none" strokeLinecap="round" />
              </svg>
            </span><br />
            <span style={{ ...mn.h1Light, fontFamily: "\"Inter Tight\"" }}>statt zu lesen.</span>
          </h1>

          <p style={mn.lede}>
            20 Jahre Web — vom Entwickler zum Product Owner.
            Ein Chatbot, der für mich antwortet. Klar. Persönlich. Kurz.
          </p>

          {/* Topic chips — flowing layout, no card chrome */}
          <div style={mn.topicWrap}>
            <div style={mn.topicLabel}>
              <span style={mn.topicLabelNum}>08</span>
              <span>Themen — eines wählen, oder eigene Frage stellen</span>
            </div>
            <div style={mn.topicGrid}>
              {topics.map((t) => {
                const asked = askedTopics.has(t.id);
                const hover = hoveredId === t.id;
                return (
                  <button
                    key={t.id}
                    onMouseEnter={() => setHoveredId(t.id)}
                    onMouseLeave={() => setHoveredId(null)}
                    onClick={() => pick(t)}
                    disabled={pending}
                    style={{
                      ...mn.topic,
                      background: asked ? HL : hover ? '#fafafa' : '#fff',
                      borderColor: asked ? HL : hover ? '#111' : '#eaeaea',
                      color: asked ? '#111' : '#111'
                    }}>
                    
                    <span style={mn.topicNum}>{t.n}</span>
                    <span style={mn.topicName}>{t.label}</span>
                    <span style={{
                      ...mn.topicArrow,
                      transform: hover || asked ? 'translateX(0)' : 'translateX(-4px)',
                      opacity: hover || asked ? 1 : 0.4
                    }}>↗</span>
                  </button>);

              })}
            </div>
          </div>

          {/* Stat strip */}
          <div style={mn.stats}>
            <div style={mn.stat}>
              <div style={mn.statN}>20<span style={mn.statPlus}>+</span></div>
              <div style={mn.statL}>Jahre</div>
            </div>
            <div style={mn.statSep}></div>
            <div style={mn.stat}>
              <div style={mn.statN}>03</div>
              <div style={mn.statL}>Rollen</div>
            </div>
            <div style={mn.statSep}></div>
            <div style={mn.stat}>
              <div style={mn.statN}>∞</div>
              <div style={mn.statL}>Fragen</div>
            </div>
            <div style={mn.statSep}></div>
            <div style={mn.stat}>
              <div style={{ ...mn.statN, color: HL_DEEP }}>●</div>
              <div style={mn.statL}>Live · Claude</div>
            </div>
          </div>
        </div>

        {/* RIGHT: chat panel */}
        <div style={mn.right}>
          <div style={mn.chatHead}>
            <div style={mn.chatHeadLeft}>
              <div style={{ ...mn.statusOrb, background: HL }}>
                <div style={mn.statusOrbInner}></div>
              </div>
              <div>
                <div style={mn.chatTitle}>Im Gespräch</div>
                <div style={mn.chatSub}>Antwort in ~2 Sek.</div>
              </div>
            </div>
            <div style={mn.chatHeadCount}>
              <span style={mn.countN}>{Math.ceil(messages.length / 2)}</span>
              <span style={mn.countL}>Fragen heute</span>
            </div>
          </div>

          <div ref={scrollRef} style={mn.thread}>
            {messages.length === 0 && !pending &&
            <div style={mn.empty}>
                <div style={{ ...mn.emptyTick, background: HL }}></div>
                <div style={mn.emptyTitle}>Bereit, wenn Sie es sind.</div>
                <div style={mn.emptySub}>
                  Wählen Sie ein Thema links — oder tippen Sie unten Ihre eigene Frage.
                </div>
              </div>
            }

            {messages.map((m, i) =>
            m.role === 'user' ?
            <div key={i} style={mn.qWrap}>
                  <div style={mn.qLine}></div>
                  <div style={mn.qBubble}>
                    <div style={mn.qLabel}>Sie fragen</div>
                    <div style={mn.qText}>{m.content}</div>
                  </div>
                </div> :

            <div key={i} style={mn.aWrap}>
                  <div style={{ ...mn.aSpine, background: HL }}></div>
                  <div style={mn.aBubble}>
                    <div style={mn.aMeta}>
                      <span style={mn.aName}>Ralf</span>
                      <span style={mn.aDot}>·</span>
                      <span style={mn.aTime}>{new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>
                    <div style={mn.aText}>{m.content}</div>
                  </div>
                </div>

            )}
            {pending &&
            <div style={mn.aWrap}>
                <div style={{ ...mn.aSpine, background: HL }}></div>
                <div style={mn.aBubble}>
                  <div style={mn.aMeta}>
                    <span style={mn.aName}>Ralf</span>
                    <span style={mn.aDot}>·</span>
                    <span style={mn.aTime}>denkt nach</span>
                  </div>
                  <div style={mn.typing}>
                    <span style={mn.tdot}></span>
                    <span style={{ ...mn.tdot, animationDelay: '.15s' }}></span>
                    <span style={{ ...mn.tdot, animationDelay: '.3s' }}></span>
                  </div>
                </div>
              </div>
            }
          </div>

          <form onSubmit={(e) => {e.preventDefault();send();}} style={mn.composer}>
            <input
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="Eigene Frage stellen…"
              style={mn.input}
              disabled={pending} />
            
            <button
              type="submit"
              disabled={pending || !draft.trim()}
              style={{
                ...mn.sendBtn,
                background: draft.trim() ? HL : '#f0f0f0',
                color: draft.trim() ? '#111' : '#bbb',
                cursor: draft.trim() ? 'pointer' : 'default'
              }}>
              
              Senden
              <span style={mn.sendArrow}>↑</span>
            </button>
          </form>
        </div>
      </div>

      <style>{`
        @keyframes mn-pulse { 0%,100% { transform: scale(1); opacity: 1 } 50% { transform: scale(0.6); opacity: 0.5 } }
        @keyframes mn-typing { 0%,60%,100% { transform: translateY(0); opacity: 0.4 } 30% { transform: translateY(-3px); opacity: 1 } }
      `}</style>
    </div>);

}

const mn = {
  root: {
    background: '#ffffff',
    color: '#111',
    fontFamily: 'Inter, system-ui, sans-serif',
    display: 'flex', flexDirection: 'column'
  },
  nav: {
    height: 64, padding: '0 40px',
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    borderBottom: '1px solid #f0f0f0'
  },
  brand: { display: 'flex', alignItems: 'center', gap: 12 },
  brandSquare: { width: 18, height: 18, borderRadius: 4 },
  brandName: { fontSize: 16, fontWeight: 600, letterSpacing: '-0.01em' },
  brandSlash: { color: '#ccc', fontWeight: 300 },
  brandRole: { fontSize: 14, color: '#888' },
  navRight: { display: 'flex', alignItems: 'center', gap: 28 },
  navLink: { fontSize: 14, color: '#555', cursor: 'pointer' },
  navCta: {
    padding: '8px 16px', borderRadius: 99, fontSize: 13, fontWeight: 600,
    color: '#111', cursor: 'pointer', display: 'flex', alignItems: 'center'
  },

  body: {
    flex: 1, display: 'grid', gridTemplateColumns: '1.1fr 1fr', minHeight: 0
  },

  /* LEFT */
  left: {
    padding: '40px 48px',
    display: 'flex', flexDirection: 'column', gap: 28,
    minHeight: 0, overflow: 'hidden'
  },
  kicker: { display: 'flex', alignItems: 'center', gap: 8 },
  kickerDot: {
    width: 8, height: 8, borderRadius: 99,
    animation: 'mn-pulse 2s infinite'
  },
  kickerText: {
    fontSize: 12, color: '#666', fontFamily: "'JetBrains Mono', monospace",
    letterSpacing: '0.02em'
  },
  h1: {
    margin: 0, fontFamily: "'Inter Tight', sans-serif",
    fontSize: 76, fontWeight: 600, lineHeight: 0.96,
    letterSpacing: '-0.035em', color: '#111'
  },
  h1Highlight: {
    position: 'relative', display: 'inline-block'
  },
  h1Light: { fontWeight: 300, color: '#888', fontStyle: 'italic' },
  underline: {
    position: 'absolute', left: 0, right: 0, bottom: -8,
    width: '100%', height: 14
  },
  lede: {
    margin: 0, fontSize: 16, lineHeight: 1.55, maxWidth: 480,
    color: '#555', textWrap: 'pretty'
  },

  topicWrap: { display: 'flex', flexDirection: 'column', gap: 12 },
  topicLabel: {
    display: 'flex', alignItems: 'center', gap: 10,
    fontSize: 11, color: '#888', fontFamily: "'JetBrains Mono', monospace",
    textTransform: 'uppercase', letterSpacing: '0.1em'
  },
  topicLabelNum: {
    background: '#111', color: '#fff', padding: '2px 6px', borderRadius: 4
  },
  topicGrid: {
    display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8
  },
  topic: {
    display: 'flex', alignItems: 'center', gap: 10,
    padding: '14px 14px',
    border: '1px solid #eaeaea', borderRadius: 8,
    fontFamily: 'inherit', fontSize: 14, fontWeight: 500,
    cursor: 'pointer', textAlign: 'left',
    transition: 'all 0.18s ease'
  },
  topicNum: {
    fontSize: 11, color: '#999', fontFamily: "'JetBrains Mono', monospace",
    fontWeight: 400
  },
  topicName: { flex: 1 },
  topicArrow: {
    fontSize: 13, color: '#111',
    transition: 'all 0.18s ease'
  },

  stats: {
    display: 'flex', alignItems: 'center', gap: 28,
    padding: '20px 0', borderTop: '1px solid #f0f0f0',
    marginTop: 'auto'
  },
  stat: { display: 'flex', flexDirection: 'column', gap: 4 },
  statN: {
    fontSize: 32, fontWeight: 600, lineHeight: 1, color: '#111',
    fontFamily: "'Inter Tight', sans-serif", letterSpacing: '-0.04em'
  },
  statPlus: { fontSize: 16, color: '#888' },
  statL: {
    fontSize: 11, color: '#888', textTransform: 'uppercase',
    letterSpacing: '0.1em'
  },
  statSep: { width: 1, height: 32, background: '#f0f0f0' },

  /* RIGHT */
  right: {
    display: 'flex', flexDirection: 'column', minHeight: 0,
    borderLeft: '1px solid #f0f0f0',
    background: '#fafafa'
  },
  chatHead: {
    padding: '24px 32px', display: 'flex', justifyContent: 'space-between',
    alignItems: 'center', borderBottom: '1px solid #f0f0f0',
    background: '#fff'
  },
  chatHeadLeft: { display: 'flex', alignItems: 'center', gap: 14 },
  statusOrb: {
    width: 36, height: 36, borderRadius: 99,
    display: 'flex', alignItems: 'center', justifyContent: 'center'
  },
  statusOrbInner: {
    width: 10, height: 10, borderRadius: 99, background: '#111',
    animation: 'mn-pulse 2s infinite'
  },
  chatTitle: { fontSize: 14, fontWeight: 600, color: '#111' },
  chatSub: { fontSize: 12, color: '#888', marginTop: 2 },
  chatHeadCount: {
    display: 'flex', flexDirection: 'column', alignItems: 'flex-end'
  },
  countN: {
    fontSize: 22, fontWeight: 600, color: '#111',
    fontFamily: "'Inter Tight', sans-serif"
  },
  countL: { fontSize: 10, color: '#888', textTransform: 'uppercase', letterSpacing: '0.1em' },

  thread: {
    flex: 1, overflowY: 'auto', padding: '28px 32px',
    display: 'flex', flexDirection: 'column', gap: 22, minHeight: 0
  },

  empty: {
    flex: 1, display: 'flex', flexDirection: 'column',
    alignItems: 'flex-start', justifyContent: 'center', gap: 14,
    padding: '40px 0'
  },
  emptyTick: { width: 64, height: 4, borderRadius: 99 },
  emptyTitle: {
    fontSize: 28, fontWeight: 600, color: '#111',
    fontFamily: "'Inter Tight', sans-serif", letterSpacing: '-0.02em'
  },
  emptySub: { fontSize: 14, color: '#888', maxWidth: 320, lineHeight: 1.5 },

  qWrap: { display: 'flex', alignItems: 'flex-start', gap: 14 },
  qLine: { width: 2, alignSelf: 'stretch', background: '#111', borderRadius: 1, flexShrink: 0 },
  qBubble: { flex: 1 },
  qLabel: {
    fontSize: 11, color: '#888', textTransform: 'uppercase',
    letterSpacing: '0.12em', marginBottom: 6,
    fontFamily: "'JetBrains Mono', monospace"
  },
  qText: {
    fontSize: 18, lineHeight: 1.4, color: '#111', fontWeight: 500,
    letterSpacing: '-0.01em'
  },

  aWrap: { display: 'flex', alignItems: 'flex-start', gap: 14 },
  aSpine: { width: 2, alignSelf: 'stretch', borderRadius: 1, flexShrink: 0 },
  aBubble: { flex: 1 },
  aMeta: {
    display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6
  },
  aName: {
    fontSize: 12, fontWeight: 600, color: '#111',
    textTransform: 'uppercase', letterSpacing: '0.1em'
  },
  aDot: { color: '#ccc' },
  aTime: {
    fontSize: 11, color: '#888',
    fontFamily: "'JetBrains Mono', monospace"
  },
  aText: {
    fontSize: 15, lineHeight: 1.65, color: '#222'
  },
  typing: { display: 'flex', alignItems: 'center', gap: 4, padding: '4px 0' },
  tdot: {
    width: 7, height: 7, borderRadius: 99, background: '#111',
    display: 'inline-block', animation: 'mn-typing 1.2s infinite'
  },

  composer: {
    padding: '16px 24px 24px',
    display: 'flex', gap: 10, alignItems: 'center',
    background: '#fff', borderTop: '1px solid #f0f0f0'
  },
  input: {
    flex: 1, height: 52, border: '1px solid #eaeaea',
    borderRadius: 99, padding: '0 22px',
    fontFamily: 'inherit', fontSize: 15, color: '#111',
    outline: 'none', background: '#fff'
  },
  sendBtn: {
    height: 52, padding: '0 22px', borderRadius: 99, border: 'none',
    fontFamily: 'inherit', fontSize: 14, fontWeight: 600,
    display: 'flex', alignItems: 'center', gap: 8,
    transition: 'all 0.18s ease'
  },
  sendArrow: { fontSize: 16, fontWeight: 700 }
};

window.VariantCardsMinimal = VariantCardsMinimal;