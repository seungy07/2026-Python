import { getPhase, PHASE_INFO } from './Scene';

// 주문 정보 입력 폼
// value : 실제로 Spring → FastAPI 로 보내는 값 (원본 데이터 표기 그대로)
// label : 화면에 보여줄 한글
export const WEATHER = [
  { value: 'Sunny', label: '맑음', icon: '☀️' },
  { value: 'Cloudy', label: '흐림', icon: '☁️' },
  { value: 'Fog', label: '안개', icon: '🌫️' },
  { value: 'Windy', label: '바람', icon: '🌬️' },
  { value: 'Stormy', label: '폭풍', icon: '⛈️' },
  { value: 'Sandstorms', label: '모래폭풍', icon: '🏜️' },
];
const TRAFFIC = [
  { value: 'Low', label: '원활', color: '#22c55e' },
  { value: 'Medium', label: '보통', color: '#eab308' },
  { value: 'High', label: '혼잡', color: '#f97316' },
  { value: 'Jam', label: '정체', color: '#ef4444' },
];
const CITY = [
  { value: 'Metropolitian', label: '대도시', icon: '🏙️' }, // 원본 데이터 철자 그대로
  { value: 'Urban', label: '도시', icon: '🏢' },
  { value: 'Semi-Urban', label: '교외', icon: '🏡' },
];
// 시각 빠른 선택 : 새벽 / 낮 / 노을 / 밤 배경을 바로 확인할 수 있도록
const TIME_PRESETS = [
  { time: '06:00', label: '🌅 새벽' },
  { time: '12:30', label: '☀️ 점심' },
  { time: '18:00', label: '🌇 저녁' },
  { time: '22:00', label: '🌙 밤' },
];
const DIST_MAX = 25;

export default function OrderForm({ form, setForm, onSubmit, loading }) {
  const set = (name, value) => setForm({ ...form, [name]: value });
  const phase = getPhase(form.order_time);
  const distance = Number(form.distance_km);
  const festival = form.festival === 'Yes';
  const toggleFestival = () => set('festival', festival ? 'No' : 'Yes');

  return (
    <form className="card form-card" onSubmit={onSubmit}>
      <div className="card-title">
        <span>🧾 주문 정보</span>
        <span className="sub">값을 바꾸면 배경도 바뀌어요</span>
      </div>

      {/* 1. 거리 */}
      <div className="section">
        <div className="section-label">
          <span>📍 배달 거리</span>
          <b>{distance.toFixed(1)} km</b>
        </div>
        <input
          className="range" type="range" min="0" max={DIST_MAX} step="0.1"
          value={distance}
          onChange={(e) => set('distance_km', Math.max(0.1, Number(e.target.value)))}
          style={{ '--pct': `${(distance / DIST_MAX) * 100}%` }}
          aria-label="배달 거리"
        />
        <div className="range-ticks">
          <span>0</span><span>5</span><span>10</span><span>15</span><span>20</span><span>25km</span>
        </div>
      </div>

      {/* 2. 주문 시각 */}
      <div className="section">
        <div className="section-label">
          <span>🕒 주문 시각</span>
          <b>{PHASE_INFO[phase].icon} {PHASE_INFO[phase].label}</b>
        </div>
        <div className="time-row">
          <input
            className="time-input" type="time" required
            value={form.order_time}
            onChange={(e) => set('order_time', e.target.value || '12:00')}
            aria-label="주문 시각"
          />
          <div className="presets">
            {TIME_PRESETS.map((p) => (
              <button key={p.time} type="button" className={`preset ${form.order_time === p.time ? 'active' : ''}`}
                onClick={() => set('order_time', p.time)}>
                {p.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 3. 날씨 */}
      <div className="section">
        <div className="section-label"><span>🌦️ 날씨</span></div>
        <div className="tiles cols-6" role="radiogroup" aria-label="날씨">
          {WEATHER.map((w) => (
            <button key={w.value} type="button" role="radio" aria-checked={form.weather === w.value}
              className={`tile ${form.weather === w.value ? 'active' : ''}`}
              onClick={() => set('weather', w.value)}>
              <span className="ico">{w.icon}</span>
              {w.label}
            </button>
          ))}
        </div>
      </div>

      {/* 4. 교통 혼잡도 */}
      <div className="section">
        <div className="section-label"><span>🚦 교통 혼잡도</span></div>
        <div className="segment" role="radiogroup" aria-label="교통 혼잡도">
          {TRAFFIC.map((t) => (
            <button key={t.value} type="button" role="radio" aria-checked={form.traffic === t.value}
              className={`seg ${form.traffic === t.value ? 'active' : ''}`}
              style={{ '--c': t.color }}
              onClick={() => set('traffic', t.value)}>
              <i className="dot" />
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* 5. 도시 유형 */}
      <div className="section">
        <div className="section-label"><span>🗺️ 도시 유형</span></div>
        <div className="tiles cols-3" role="radiogroup" aria-label="도시 유형">
          {CITY.map((c) => (
            <button key={c.value} type="button" role="radio" aria-checked={form.city === c.value}
              className={`tile row ${form.city === c.value ? 'active' : ''}`}
              onClick={() => set('city', c.value)}>
              <span className="ico">{c.icon}</span>
              {c.label}
            </button>
          ))}
        </div>
      </div>

      {/* 6. 축제 여부 */}
      <div
        className={`festival-row ${festival ? 'on' : ''}`}
        role="switch" aria-checked={festival} tabIndex={0}
        onClick={toggleFestival}
        onKeyDown={(e) => {
          if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggleFestival(); }
        }}
      >
        <div className="festival-text">
          <strong>🎉 축제 진행 중</strong>
          <span>{festival ? '축제 기간이라 주문이 몰려요!' : '축제가 없는 평범한 날이에요'}</span>
        </div>
        <span className={`switch ${festival ? 'on' : ''}`} aria-hidden="true" />
      </div>

      <button className="submit" type="submit" disabled={loading}>
        {loading ? (
          <>
            <span className="spinner" />
            AI가 예측하는 중…
          </>
        ) : (
          <>🛵 배달 시간 예측하기</>
        )}
      </button>
    </form>
  );
}
