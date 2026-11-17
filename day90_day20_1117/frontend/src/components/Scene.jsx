import { memo, useMemo } from 'react';
import '../Scene.css';

/* =====================================================================
   Scene : 입력한 주문 조건(주문 시각 · 날씨 · 교통 · 도시 유형 · 축제)을
           화면 전체 배경 풍경으로 그려주는 컴포넌트
   * 라이브러리 없이 CSS 애니메이션 + SVG 로만 구현
   * 그리는 순서 = 겹치는 순서 (뒤에 그린 것이 앞에 보임)
     하늘 → 별 → 해/달 → 구름 → 불꽃놀이 → 건물 → 도로 → 날씨 효과 → 축제 장식
   ===================================================================== */

// ---------- 1. 주문 시각 → 하루 단계 ----------
// "19:30" → 19.5
export function toHour(time) {
  const [h, m] = String(time ?? '').split(':').map(Number);
  if (!Number.isFinite(h)) return 12;
  return h + (Number.isFinite(m) ? m : 0) / 60;
}

// 새벽 5~7시 , 낮 7~17시 , 노을 17~19시 , 밤 19~5시
export function getPhase(time) {
  const h = toHour(time);
  if (h >= 5 && h < 7) return 'dawn';
  if (h >= 7 && h < 17) return 'day';
  if (h >= 17 && h < 19) return 'sunset';
  return 'night';
}

export const PHASE_INFO = {
  dawn: { icon: '🌅', label: '새벽' },
  day: { icon: '☀️', label: '낮' },
  sunset: { icon: '🌇', label: '노을' },
  night: { icon: '🌙', label: '밤' },
};

// ---------- 2. 고정 시드 난수 : 다시 그려도 같은 배치가 나오도록 ----------
function seeded(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const between = (rand, min, max) => min + rand() * (max - min);
const clamp01 = (v) => Math.min(Math.max(v, 0), 1);

const FESTIVE_COLORS = ['#ff4d6d', '#ffd23f', '#3bceac', '#4d96ff', '#c77dff', '#ff8c42'];

// 날씨별로 해 · 달 · 별이 가려지는 정도 (1 = 잘 보임)
const SUN_DIM = { Sunny: 1, Windy: 1, Cloudy: 0.5, Fog: 0.35, Stormy: 0, Sandstorms: 0.45 };
const STAR_DIM = { Sunny: 1, Windy: 1, Cloudy: 0.35, Fog: 0.25, Stormy: 0.08, Sandstorms: 0.15 };
const PHASE_STARS = { night: 1, dawn: 0.4, sunset: 0.15, day: 0 };

/* ---------- 구름 그라데이션 정의 (색은 Scene.css 의 하루 단계 변수 사용) ---------- */
function SceneDefs() {
  return (
    <svg className="scene-defs" width="0" height="0" aria-hidden="true">
      <defs>
        <linearGradient id="cloud-light" gradientUnits="userSpaceOnUse" x1="0" y1="8" x2="0" y2="100">
          <stop offset="0" style={{ stopColor: 'var(--cloud-top)' }} />
          <stop offset="1" style={{ stopColor: 'var(--cloud-bottom)' }} />
        </linearGradient>
        <linearGradient id="cloud-dark" gradientUnits="userSpaceOnUse" x1="0" y1="8" x2="0" y2="100">
          <stop offset="0" style={{ stopColor: 'var(--storm-top)' }} />
          <stop offset="1" style={{ stopColor: 'var(--storm-bottom)' }} />
        </linearGradient>
        <linearGradient id="cloud-sand" gradientUnits="userSpaceOnUse" x1="0" y1="8" x2="0" y2="100">
          <stop offset="0" stopColor="#f0d2a0" />
          <stop offset="1" stopColor="#c4945a" />
        </linearGradient>
      </defs>
    </svg>
  );
}

/* ---------- 하늘 : 단계별 4장 + 날씨 색을 겹쳐 두고 투명도로 전환 ---------- */
const PHASES = ['dawn', 'day', 'sunset', 'night'];
const SKY_TINTS = ['Cloudy', 'Fog', 'Stormy', 'Sandstorms'];

function Sky({ phase, weather }) {
  return (
    <>
      {PHASES.map((p) => (
        <div key={p} className={`sky sky-${p} ${phase === p ? 'on' : ''}`} />
      ))}
      {SKY_TINTS.map((w) => (
        <div key={w} className={`sky-tint tint-${w} ${weather === w ? 'on' : ''}`} />
      ))}
    </>
  );
}

/* ---------- 별 ---------- */
const Stars = memo(function Stars({ opacity }) {
  const stars = useMemo(() => {
    const rand = seeded(42);
    return Array.from({ length: 110 }, (_, i) => ({
      id: i,
      x: rand() * 100,
      y: rand() * 60,
      size: between(rand, 1, 2.6),
      dur: between(rand, 2, 5),
      delay: -rand() * 5,
    }));
  }, []);

  return (
    <div className="stars" style={{ opacity }}>
      {stars.map((s) => (
        <span
          key={s.id}
          className="star"
          style={{
            left: `${s.x}%`, top: `${s.y}%`, width: s.size, height: s.size,
            animationDuration: `${s.dur}s`, animationDelay: `${s.delay}s`,
          }}
        />
      ))}
      <span className="shooting-star" />
    </div>
  );
});

/* ---------- 해 / 달 : 시각에 따라 왼쪽 → 오른쪽 포물선 이동 ---------- */
function Celestial({ hour, weather }) {
  // 화면 가로 8% → 92% , 세로는 포물선 (transform 으로 이동해야 가벼움)
  const arc = (t) => ({ transform: `translate(${8 + t * 84}vw, ${66 - Math.sin(Math.PI * t) * 54}vh)` });
  const sunT = (hour - 5) / 14;                    // 05시 뜨고 19시 짐
  const moonT = ((((hour - 18) % 24) + 24) % 24) / 13; // 18시 뜨고 07시 짐
  const dim = SUN_DIM[weather] ?? 1;

  return (
    <>
      <div className="sun" style={{ ...arc(clamp01(sunT)), opacity: sunT >= 0 && sunT <= 1 ? dim : 0 }}>
        {weather === 'Sunny' && <div className="sun-rays" />}
        <div className="sun-core" />
      </div>
      <div className="moon" style={{ ...arc(clamp01(moonT)), opacity: moonT <= 1 ? Math.max(dim, 0.15) : 0 }}>
        <div className="moon-core" />
      </div>
    </>
  );
}

/* ---------- 구름 : 날씨에 따라 개수 · 크기 · 속도 · 색이 다름 ---------- */
const CLOUD_CFG = {
  Sunny: { n: 4, dur: [90, 140], scale: [0.55, 1], top: [6, 30], op: 0.9, fill: 'light' },
  Cloudy: { n: 9, dur: [70, 110], scale: [0.9, 1.6], top: [2, 36], op: 0.95, fill: 'light' },
  Fog: { n: 4, dur: [120, 170], scale: [1, 1.6], top: [12, 40], op: 0.5, fill: 'light' },
  Windy: { n: 7, dur: [14, 24], scale: [0.6, 1.1], top: [4, 32], op: 0.85, fill: 'light' },
  Stormy: { n: 10, dur: [45, 70], scale: [1, 1.8], top: [-4, 26], op: 0.97, fill: 'dark' },
  Sandstorms: { n: 5, dur: [22, 34], scale: [0.9, 1.5], top: [8, 34], op: 0.55, fill: 'sand' },
};

const Clouds = memo(function Clouds({ weather }) {
  const cfg = CLOUD_CFG[weather] ?? CLOUD_CFG.Sunny;
  const clouds = useMemo(() => {
    const rand = seeded(weather.length * 131 + 7);
    return Array.from({ length: cfg.n }, (_, i) => {
      const dur = between(rand, ...cfg.dur);
      return {
        id: i,
        top: between(rand, ...cfg.top),
        width: 240 * between(rand, ...cfg.scale),
        dur,
        delay: -rand() * dur,
        op: cfg.op * between(rand, 0.75, 1),
      };
    });
  }, [weather, cfg]);

  return (
    <div className="clouds" key={weather}>
      {clouds.map((c) => (
        <div
          key={c.id}
          className="cloud"
          style={{
            top: `${c.top}%`, width: c.width, opacity: c.op,
            animationDuration: `${c.dur}s`, animationDelay: `${c.delay}s`,
          }}
        >
          <svg viewBox="0 0 200 110" aria-hidden="true">
            <g fill={`url(#cloud-${cfg.fill})`}>
              <circle cx="58" cy="66" r="32" />
              <circle cx="100" cy="48" r="42" />
              <circle cx="143" cy="64" r="33" />
              <rect x="28" y="62" width="148" height="38" rx="19" />
            </g>
          </svg>
        </div>
      ))}
    </div>
  );
});

/* ---------- 불꽃놀이 (축제 + 노을/밤) ---------- */
const FIREWORKS = [
  { x: 14, y: 18, c: '#ff4d6d', delay: 0 },
  { x: 34, y: 9, c: '#ffd23f', delay: 1.3 },
  { x: 55, y: 20, c: '#3bceac', delay: 0.6 },
  { x: 74, y: 8, c: '#c77dff', delay: 2.0 },
  { x: 90, y: 22, c: '#4d96ff', delay: 2.7 },
];

const Fireworks = memo(function Fireworks() {
  return (
    <div className="fireworks">
      {FIREWORKS.map((f, i) => (
        <div key={i} className="firework" style={{ left: `${f.x}%`, top: `${f.y}%`, '--c': f.c, '--delay': `${f.delay}s` }}>
          <i className="rocket" />
          <i className="flash" />
          {Array.from({ length: 18 }, (_, k) => (
            <i key={k} className="spark" style={{ '--a': `${k * 20}deg`, '--d': `${64 + (k % 3) * 16}px` }} />
          ))}
        </div>
      ))}
    </div>
  );
});

/* ---------- 건물 / 집 / 나무 : 도시 유형에 따라 스카이라인이 달라짐 ---------- */
const H = 420; // SVG viewBox 높이 (바닥 y = 420)
const CITY_CFG = {
  Metropolitian: {
    far: { w: [40, 90], h: [170, 320], gap: [0, 6] },
    near: { w: [60, 125], h: [110, 340], gap: [4, 16] },
    antenna: true,
  },
  Urban: {
    far: { w: [60, 120], h: [100, 190], gap: [0, 10] },
    near: { w: [80, 150], h: [70, 200], gap: [8, 26] },
    antenna: false,
  },
};

const hillY = (x) => 318 - 26 * Math.sin(x / 170) - 14 * Math.sin(x / 63 + 1);

function buildLayer(city, layer) {
  const rand = seeded((city === 'Metropolitian' ? 11 : city === 'Urban' ? 23 : 37) + (layer === 'near' ? 100 : 0));
  const items = [];

  // 교외 : 언덕 위 나무 + 낮은 집과 나무
  if (city === 'Semi-Urban') {
    if (layer === 'far') {
      for (let x = -10; x < 1620; x += between(rand, 26, 70)) {
        items.push({ type: 'tree', x, base: hillY(x) + 4, s: between(rand, 12, 22) });
      }
      return items;
    }
    let x = -30;
    while (x < 1620) {
      if (rand() < 0.42) {
        const s = between(rand, 22, 36);
        items.push({ type: 'tree', x: x + s, base: H, s });
        x += s * 2 + between(rand, 6, 20);
      } else {
        const w = between(rand, 84, 130);
        items.push({ type: 'house', x, w, h: between(rand, 52, 86), roof: between(rand, 26, 42), seed: Math.floor(rand() * 1e6) });
        x += w + between(rand, 18, 44);
      }
    }
    return items;
  }

  // 대도시 / 도시 : 빌딩
  const city_ = CITY_CFG[city] ?? CITY_CFG.Urban;
  const cfg = city_[layer];
  let x = -20;
  while (x < 1620) {
    const w = between(rand, ...cfg.w);
    const h = between(rand, ...cfg.h);
    const top = rand();
    const antenna = city_.antenna && layer === 'near' && h > 270 && rand() > 0.3;
    items.push({ type: 'building', x, w, h, top, antenna, seed: Math.floor(rand() * 1e6) });
    x += w + between(rand, ...cfg.gap);
  }
  return items;
}

function Building({ b, layer }) {
  const y = H - b.h;
  const rand = seeded(b.seed);
  const wins = [];
  if (layer === 'near') {
    const cols = Math.max(1, Math.floor((b.w - 14) / 15));
    const rows = Math.max(1, Math.floor((b.h - 24) / 19));
    const ox = b.x + (b.w - (cols * 15 - 6)) / 2;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        wins.push(
          <rect key={`${r}-${c}`} className={rand() < 0.38 ? 'win lit' : 'win'}
            x={ox + c * 15} y={y + 14 + r * 19} width="9" height="11" rx="1.5" />
        );
      }
    }
  } else {
    const cols = Math.max(1, Math.floor((b.w - 8) / 10));
    const rows = Math.max(1, Math.floor((b.h - 14) / 13));
    const ox = b.x + (b.w - (cols * 10 - 5)) / 2;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        if (rand() < 0.22) {
          wins.push(<rect key={`${r}-${c}`} className="winfar" x={ox + c * 10} y={y + 10 + r * 13} width="5" height="7" />);
        }
      }
    }
  }
  const roofBox = layer === 'near' && b.top > 0.72;
  const cx = b.x + b.w / 2;
  return (
    <g>
      <rect className={`bld ${layer}`} x={b.x} y={y} width={b.w} height={b.h + 4} />
      {roofBox && <rect className="bld near" x={b.x + b.w * 0.22} y={y - 12} width={b.w * 0.56} height={14} />}
      {b.antenna && (
        <>
          <line className="antenna" x1={cx} y1={y - (roofBox ? 12 : 0)} x2={cx} y2={y - 46} />
          <circle className="beacon" cx={cx} cy={y - 47} r="3.2" />
        </>
      )}
      {wins}
    </g>
  );
}

function House({ b }) {
  const y = H - b.h;
  const rand = seeded(b.seed);
  const litL = rand() < 0.6;
  const litR = rand() < 0.5;
  return (
    <g>
      <rect className="chimney" x={b.x + b.w * 0.68} y={y - b.roof * 0.9} width="10" height={b.roof * 0.7} />
      <polygon className="roof" points={`${b.x - 7},${y + 1} ${b.x + b.w / 2},${y - b.roof} ${b.x + b.w + 7},${y + 1}`} />
      <rect className="house" x={b.x} y={y} width={b.w} height={b.h + 4} />
      <rect className={litL ? 'win lit' : 'win'} x={b.x + b.w * 0.12} y={y + 14} width={b.w * 0.2} height="16" rx="2" />
      <rect className={litR ? 'win lit' : 'win'} x={b.x + b.w * 0.68} y={y + 14} width={b.w * 0.2} height="16" rx="2" />
      <rect className="door" x={b.x + b.w * 0.42} y={H - 30} width={b.w * 0.16} height="30" rx="2" />
    </g>
  );
}

function Tree({ t, far }) {
  const s = t.s;
  const leaf = far ? 'tree far' : 'tree';
  return (
    <g>
      <rect className="trunk" x={t.x - (far ? 1.5 : 3)} y={t.base - s * 0.9} width={far ? 3 : 6} height={s * 0.9 + 2} />
      <circle className={leaf} cx={t.x} cy={t.base - s * 1.25} r={s * 0.62} />
      <circle className={leaf} cx={t.x - s * 0.42} cy={t.base - s * 0.9} r={s * 0.48} />
      <circle className={leaf} cx={t.x + s * 0.42} cy={t.base - s * 0.92} r={s * 0.5} />
    </g>
  );
}

const Skyline = memo(function Skyline({ city }) {
  const far = useMemo(() => buildLayer(city, 'far'), [city]);
  const near = useMemo(() => buildLayer(city, 'near'), [city]);
  const hillPath = useMemo(() => {
    let d = `M-20 ${H} L-20 ${hillY(-20).toFixed(1)}`;
    for (let x = 0; x <= 1620; x += 20) d += ` L${x} ${hillY(x).toFixed(1)}`;
    return `${d} L1620 ${H} Z`;
  }, []);

  return (
    <div className="skyline" key={city}>
      <svg viewBox={`0 0 1600 ${H}`} preserveAspectRatio="xMidYMax slice" aria-hidden="true">
        {city === 'Semi-Urban' && <path className="hill" d={hillPath} />}
        <g>
          {far.map((it, i) => (it.type === 'tree'
            ? <Tree key={i} t={it} far />
            : <Building key={i} b={it} layer="far" />))}
        </g>
        <g>
          {near.map((it, i) => {
            if (it.type === 'tree') return <Tree key={i} t={it} />;
            if (it.type === 'house') return <House key={i} b={it} />;
            return <Building key={i} b={it} layer="near" />;
          })}
        </g>
      </svg>
    </div>
  );
});

/* ---------- 도로 : 가로등 + 자동차(교통 혼잡도) + 배달 오토바이 ---------- */
// n : 차선당 자동차 수 , dur : 화면을 한 번 지나가는 시간(초)
const TRAFFIC_CFG = {
  Low: { n: 2, dur: 9 },
  Medium: { n: 4, dur: 13 },
  High: { n: 8, dur: 21 },
  Jam: { n: 15, dur: 50 },
};
const CAR_COLORS = ['#e63946', '#f4a261', '#2a9d8f', '#457b9d', '#e9edf2', '#8d99ae', '#ffb703', '#6d597a', '#1d3557'];
const LAMPS = [7, 25, 43, 61, 79, 95];

function Car({ color, brake }) {
  return (
    <div className="car-body">
      <div className="headlight-beam" />
      <svg viewBox="0 0 80 34" width="74" height="31" aria-hidden="true">
        <path d="M6 22 Q6 15 14 14 L24 13 L32 5 Q34 3 38 3 L56 3 Q60 3 62 6 L68 13 Q76 14 77 20 L77 25 Q77 27 75 27 L8 27 Q6 27 6 25 Z" fill={color} />
        <path d="M35 6 L39 5 L55 5 Q58 5 59 7 L63 12 L30 12 Z" fill="rgba(190, 220, 255, 0.85)" />
        <rect x="45" y="5" width="2.4" height="7" fill={color} />
        <circle cx="20" cy="27" r="6" fill="#1e222b" />
        <circle cx="20" cy="27" r="2.4" fill="#aab3c2" />
        <circle cx="62" cy="27" r="6" fill="#1e222b" />
        <circle cx="62" cy="27" r="2.4" fill="#aab3c2" />
        <rect x="73" y="16" width="4" height="4" rx="1" fill="#ffe9a8" />
        <rect className={brake ? 'taillight brake' : 'taillight'} x="5" y="16" width="3" height="5" rx="1" fill="#ff4d4d" />
      </svg>
    </div>
  );
}

function Scooter() {
  return (
    <svg viewBox="0 0 130 96" width="124" height="92" aria-hidden="true">
      <ellipse cx="66" cy="91" rx="52" ry="4" fill="rgba(0, 0, 0, 0.28)" />
      {/* 배달통 */}
      <rect x="4" y="18" width="38" height="32" rx="6" fill="#ff8a5c" />
      <rect x="4" y="18" width="38" height="9" rx="4.5" fill="#e4572e" />
      <text x="23" y="43" textAnchor="middle" fontSize="10" fontWeight="800" fill="#fff">배달</text>
      {/* 차체 */}
      <path d="M16 72 C16 57 29 50 46 50 L76 50 C82 50 86 54 88 60 L92 69 L52 71 C40 75 26 77 16 72 Z" fill="#ff6b35" />
      <path d="M86 61 L97 29 L105 31 L99 67 Z" fill="#ff6b35" />
      <path d="M40 50 C44 42 59 42 67 46 L67 50 Z" fill="#2d3340" />
      {/* 앞 포크 · 핸들 · 전조등 */}
      <line x1="101" y1="42" x2="104" y2="77" stroke="#2d3340" strokeWidth="5" strokeLinecap="round" />
      <line x1="92" y1="27" x2="107" y2="25" stroke="#2d3340" strokeWidth="4" strokeLinecap="round" />
      <circle className="scooter-light" cx="105" cy="37" r="4.5" fill="#ffe8a3" />
      {/* 바퀴 */}
      <circle cx="32" cy="78" r="13" fill="#1f2430" />
      <circle cx="32" cy="78" r="5" fill="#c9d1dd" />
      <circle cx="103" cy="78" r="13" fill="#1f2430" />
      <circle cx="103" cy="78" r="5" fill="#c9d1dd" />
      {/* 라이더 */}
      <path d="M54 47 L75 53 L81 70" stroke="#2b3a55" strokeWidth="8" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <ellipse cx="84" cy="71" rx="6.5" ry="3.5" fill="#1b1f27" />
      <path d="M49 48 C47 35 54 23 64 19 L73 23 C69 33 67 42 63 50 Z" fill="#3a86ff" />
      <path d="M67 26 L85 32 L97 27" stroke="#3a86ff" strokeWidth="7" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="97" cy="27" r="3.5" fill="#f2c7a5" />
      <circle cx="71" cy="14" r="8" fill="#f2c7a5" />
      <path d="M61 14 C61 4 69 0 76 2 C83 4 85 10 84 15 L67 16 Z" fill="#ff6b35" />
      <path d="M75 9 L85 11 L84 15 L75 14 Z" fill="#1f2a44" opacity="0.85" />
    </svg>
  );
}

// mode : 'idle'(대기) / 'riding'(예측 중) / 'arrived'(결과 도착)
const Road = memo(function Road({ traffic, mode }) {
  const cfg = TRAFFIC_CFG[traffic] ?? TRAFFIC_CFG.Medium;
  const cars = useMemo(() => {
    const rand = seeded(traffic.length * 17 + 3);
    const list = [];
    ['far', 'near'].forEach((lane) => {
      const dur = cfg.dur * (lane === 'far' ? 1.15 : 1); // 같은 차선은 같은 속도 → 겹치지 않음
      const offset = lane === 'far' ? 0.37 : 0;
      for (let i = 0; i < cfg.n; i++) {
        const frac = ((((i + between(rand, -0.12, 0.12)) / cfg.n + offset) % 1) + 1) % 1;
        list.push({ id: `${lane}-${i}`, lane, dur, delay: -frac * dur, color: CAR_COLORS[Math.floor(rand() * CAR_COLORS.length)] });
      }
    });
    return list;
  }, [traffic, cfg]);
  const brake = traffic === 'High' || traffic === 'Jam';

  return (
    <div className="road-wrap">
      <div className="road">
        <div className="sidewalk" />
        <div className="lane-line" />
      </div>
      <div className="lamps">
        {LAMPS.map((x) => (
          <div key={x} className="lamp" style={{ left: `${x}%` }}>
            <div className="lamp-cone" />
            <div className="lamp-pole" />
            <div className="lamp-head" />
          </div>
        ))}
      </div>
      <div className="cars" key={traffic}>
        {cars.map((c) => (
          <div key={c.id} className={`car lane-${c.lane}`} style={{ animationDuration: `${c.dur}s`, animationDelay: `${c.delay}s` }}>
            <Car color={c.color} brake={brake} />
          </div>
        ))}
      </div>
      {mode !== 'idle' && <div className="dest-pin">📍<span>고객</span></div>}
      <div className={`scooter ${mode}`}>
        {mode === 'riding' && (
          <>
            <i className="puff p1" />
            <i className="puff p2" />
            <i className="puff p3" />
          </>
        )}
        <Scooter />
        {mode === 'arrived' && <div className="arrive-bubble">도착!</div>}
      </div>
    </div>
  );
});

/* ---------- 날씨 효과 ---------- */
const Rain = memo(function Rain() {
  const drops = useMemo(() => {
    const rand = seeded(7);
    return Array.from({ length: 150 }, (_, i) => ({
      id: i, x: between(rand, -5, 105), h: between(rand, 40, 85),
      dur: between(rand, 0.45, 0.8), delay: -rand(), op: between(rand, 0.3, 0.75),
    }));
  }, []);
  return (
    <div className="rain">
      {drops.map((d) => (
        <i key={d.id} style={{ left: `${d.x}%`, height: d.h, opacity: d.op, animationDuration: `${d.dur}s`, animationDelay: `${d.delay}s` }} />
      ))}
    </div>
  );
});

const Lightning = memo(function Lightning() {
  return (
    <>
      <div className="lightning-flash" />
      <svg className="lightning-bolt" viewBox="0 0 60 220" aria-hidden="true">
        <path d="M36 0 L12 96 L30 96 L8 220 L52 72 L32 72 L46 0 Z" />
      </svg>
    </>
  );
});

const Fog = memo(function Fog() {
  return (
    <div className="fog">
      {[0, 1, 2, 3].map((i) => <div key={i} className={`fog-band band-${i}`} />)}
    </div>
  );
});

const Wind = memo(function Wind() {
  const streaks = useMemo(() => {
    const rand = seeded(21);
    return Array.from({ length: 18 }, (_, i) => ({ id: i, y: between(rand, 5, 80), w: between(rand, 120, 300), dur: between(rand, 1.4, 2.8), delay: -rand() * 3 }));
  }, []);
  const leaves = useMemo(() => {
    const rand = seeded(33);
    return Array.from({ length: 9 }, (_, i) => ({ id: i, y: between(rand, 30, 85), dur: between(rand, 4, 7), delay: -rand() * 7, size: between(rand, 14, 22) }));
  }, []);
  return (
    <div className="wind">
      {streaks.map((s) => (
        <i key={s.id} className="streak" style={{ top: `${s.y}%`, width: s.w, animationDuration: `${s.dur}s`, animationDelay: `${s.delay}s` }} />
      ))}
      {leaves.map((l) => (
        <span key={l.id} className="leaf" style={{ top: `${l.y}%`, fontSize: l.size, animationDuration: `${l.dur}s`, animationDelay: `${l.delay}s` }}>🍃</span>
      ))}
    </div>
  );
});

const SAND_COLORS = ['#e8c48a', '#d4a35f', '#f3d9a8', '#c08a4a'];
const Sand = memo(function Sand() {
  const grains = useMemo(() => {
    const rand = seeded(55);
    return Array.from({ length: 170 }, (_, i) => ({
      id: i, y: rand() * 100, size: between(rand, 1.5, 3.5),
      dur: between(rand, 1.2, 2.6), delay: -rand() * 2.6, color: SAND_COLORS[i % SAND_COLORS.length],
    }));
  }, []);
  return (
    <div className="sand">
      <div className="sand-haze h1" />
      <div className="sand-haze h2" />
      {grains.map((g) => (
        <i key={g.id} className="grain" style={{ top: `${g.y}%`, width: g.size, height: g.size, background: g.color, animationDuration: `${g.dur}s`, animationDelay: `${g.delay}s` }} />
      ))}
    </div>
  );
});

// 건물까지 뿌옇게 덮는 대기층
const ATMOS = ['Fog', 'Sandstorms', 'Stormy'];
function Atmosphere({ weather }) {
  return ATMOS.map((w) => <div key={w} className={`atmo atmo-${w} ${weather === w ? 'on' : ''}`} />);
}

/* ---------- 축제 장식 : 전구 가랜드 + 삼각 깃발 + 색종이 ---------- */
function buildGarland() {
  const xs = [-20, 390, 800, 1210, 1620]; // 줄이 4번 늘어지도록
  const top = 8;
  const dip = 64;
  const paths = [];
  const flags = [];
  const bulbs = [];
  let id = 0;
  for (let s = 0; s < xs.length - 1; s++) {
    const p0 = [xs[s], top];
    const p1 = [(xs[s] + xs[s + 1]) / 2, dip];
    const p2 = [xs[s + 1], top];
    paths.push(`M${p0[0]} ${p0[1]} Q${p1[0]} ${p1[1]} ${p2[0]} ${p2[1]}`);
    const N = 13;
    for (let k = 1; k < N; k++) {
      const t = k / N;
      // 2차 베지어 곡선 위의 점과 기울기
      const x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0];
      const y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1];
      const dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]);
      const dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]);
      const angle = (Math.atan2(dy, dx) * 180) / Math.PI;
      if (k % 2 === 1) {
        flags.push({ id: id++, x, y, angle, color: FESTIVE_COLORS[(s * 5 + k) % FESTIVE_COLORS.length], delay: -k * 0.3 });
      } else {
        bulbs.push({ id: id++, x, y, color: FESTIVE_COLORS[(s * 3 + k + 2) % FESTIVE_COLORS.length], delay: k % 4 === 0 ? 0 : 0.8 });
      }
    }
  }
  return { paths, flags, bulbs };
}

const FestivalDecor = memo(function FestivalDecor() {
  const garland = useMemo(buildGarland, []);
  const confetti = useMemo(() => {
    const rand = seeded(2024);
    return Array.from({ length: 80 }, (_, i) => {
      const round = rand() < 0.3;
      const dur = between(rand, 7, 13);
      return {
        id: i, x: rand() * 100, round,
        w: round ? 8 : between(rand, 6, 10), h: round ? 8 : between(rand, 10, 16),
        color: FESTIVE_COLORS[i % FESTIVE_COLORS.length], dur, delay: -rand() * dur,
        sway: between(rand, -140, 140), spin: between(rand, 360, 1080),
      };
    });
  }, []);

  return (
    <div className="festival-decor">
      <div className="confetti">
        {confetti.map((c) => (
          <i
            key={c.id}
            style={{
              left: `${c.x}%`, width: c.w, height: c.h, background: c.color, borderRadius: c.round ? '50%' : 2,
              '--dur': `${c.dur}s`, '--delay': `${c.delay}s`, '--sway': `${c.sway}px`, '--spin': `${c.spin}deg`,
            }}
          />
        ))}
      </div>
      <svg className="garland" viewBox="0 0 1600 110" preserveAspectRatio="xMidYMin slice" aria-hidden="true">
        <defs>
          <filter id="bulb-glow" x="-150%" y="-150%" width="400%" height="400%">
            <feGaussianBlur stdDeviation="4" />
          </filter>
        </defs>
        {garland.paths.map((d, i) => <path key={i} className="garland-string" d={d} />)}
        {garland.flags.map((f) => (
          <g key={f.id} transform={`translate(${f.x.toFixed(1)} ${f.y.toFixed(1)}) rotate(${f.angle.toFixed(1)})`}>
            <polygon className="flag" points="-13,0 13,0 0,24" fill={f.color} style={{ animationDelay: `${f.delay}s` }} />
          </g>
        ))}
        {garland.bulbs.map((b) => (
          <g key={b.id} transform={`translate(${b.x.toFixed(1)} ${b.y.toFixed(1)})`}>
            <g className="bulb" style={{ animationDelay: `${b.delay}s` }}>
              <circle cy="6" r="10" fill={b.color} filter="url(#bulb-glow)" />
              <circle cy="6" r="5" fill={b.color} />
              <rect x="-2.5" y="-1" width="5" height="4" rx="1" fill="#4a4a4a" />
            </g>
          </g>
        ))}
      </svg>
    </div>
  );
});

/* =====================================================================
   장면 전체 조립
   ===================================================================== */
export default function Scene({ form, loading, result }) {
  const hour = toHour(form.order_time);
  const phase = getPhase(form.order_time);
  const { weather, traffic, city } = form;
  const festival = form.festival === 'Yes';
  const starOpacity = PHASE_STARS[phase] * (STAR_DIM[weather] ?? 1);
  const mode = loading ? 'riding' : result ? 'arrived' : 'idle';

  return (
    <div className={`scene phase-${phase} weather-${weather}`} aria-hidden="true">
      <SceneDefs />
      <Sky phase={phase} weather={weather} />
      <Stars opacity={starOpacity} />
      <Celestial hour={hour} weather={weather} />
      <Clouds weather={weather} />
      {festival && (phase === 'night' || phase === 'sunset') && <Fireworks />}
      <Skyline city={city} />
      <Road traffic={traffic} mode={mode} />
      {weather === 'Fog' && <Fog />}
      {weather === 'Windy' && <Wind />}
      {weather === 'Sandstorms' && <Sand />}
      {weather === 'Stormy' && <Rain />}
      <Atmosphere weather={weather} />
      {weather === 'Stormy' && <Lightning />}
      {festival && <FestivalDecor />}
    </div>
  );
}
