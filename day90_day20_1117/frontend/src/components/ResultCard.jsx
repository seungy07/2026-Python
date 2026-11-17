import { useEffect, useState } from 'react';

// 최종 예측 결과 (SSE result 이벤트) : { "prediction": 27.4, "r2": 0.82 }

// 숫자가 0 부터 목표값까지 올라가는 연출
function useCountUp(target, duration = 1300) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (!Number.isFinite(target)) return undefined;
    let raf;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      setValue(target * (1 - (1 - p) ** 3)); // 끝에서 천천히 멈춤
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);
  return value;
}

// "19:30" + 27.4분 → "19:57" (자정을 넘기면 다음날 표시)
function addMinutes(time, minutes) {
  const [h, m] = String(time).split(':').map(Number);
  const total = h * 60 + m + Math.round(minutes);
  const t = ((total % 1440) + 1440) % 1440;
  const hh = String(Math.floor(t / 60)).padStart(2, '0');
  const mm = String(t % 60).padStart(2, '0');
  return { text: `${hh}:${mm}`, nextDay: total >= 1440 };
}

const RADIUS = 52;
const CIRCLE = 2 * Math.PI * RADIUS;

export default function ResultCard({ result, loading, error, orderTime }) {
  const minutes = Number(result?.prediction ?? result?.predicted_minutes); // FastAPI 는 predicted_minutes 로 보냄
  const r2 = Number(result?.r2);
  const shown = useCountUp(result ? minutes : NaN);

  const title = (sub) => (
    <div className="card-title">
      <span>⏱️ 예상 배달 시간</span>
      <span className="sub">{sub}</span>
    </div>
  );

  // 1) 결과 도착
  if (result && Number.isFinite(minutes)) {
    const eta = addMinutes(orderTime, minutes);
    const r2ok = Number.isFinite(r2);
    const r2Clamped = Math.min(Math.max(r2, 0), 1);
    let grade = null;
    if (r2ok) {
      if (r2 >= 0.8) grade = { label: '우수', cls: 'good' };
      else if (r2 >= 0.6) grade = { label: '양호', cls: 'fair' };
      else grade = { label: '보통', cls: 'low' };
    }

    return (
      <div className="card result-card has-result">
        {title('LightGBM 예측 결과')}
        <div className="result-body">
          <div className="result-main">
            <div className="eta-value">
              {shown.toFixed(1)}
              <small>분</small>
            </div>
            <div className="journey">
              <div className="journey-track">
                <div className="journey-fill" />
                <div className="journey-rider">🛵</div>
              </div>
              <div className="journey-times">
                <div><span>주문</span>{orderTime}</div>
                <div>
                  <span>도착 예정</span>{eta.text}
                  {eta.nextDay && <em> (다음날)</em>}
                </div>
              </div>
            </div>
          </div>

          <div className="gauge-wrap">
            <div className="gauge">
              <svg width="132" height="132" viewBox="0 0 132 132" aria-hidden="true">
                <defs>
                  <linearGradient id="gauge-grad" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0" stopColor="#ff6b35" />
                    <stop offset="1" stopColor="#ff3d7f" />
                  </linearGradient>
                </defs>
                <circle className="gauge-bg" cx="66" cy="66" r={RADIUS} />
                {r2ok && (
                  <circle
                    key={r2}
                    className="gauge-fg" cx="66" cy="66" r={RADIUS}
                    strokeDasharray={CIRCLE}
                    style={{ '--C': `${CIRCLE}px`, '--target': `${CIRCLE * (1 - r2Clamped)}px` }}
                  />
                )}
              </svg>
              <div className="gauge-center">
                <strong>{r2ok ? r2.toFixed(3) : '-'}</strong>
                <span>R² Score</span>
              </div>
            </div>
            {grade && (
              <div className="gauge-caption">
                모델 설명력 <span className={`grade ${grade.cls}`}>{grade.label}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // 2) 예측 중
  if (loading) {
    return (
      <div className="card result-card">
        {title('LightGBM 예측 중')}
        <div className="result-loading">
          <div className="loading-text">
            <span className="dots"><i /><i /><i /></span>
            AI 모델이 배달 시간을 계산하고 있어요
          </div>
          <div className="skeleton big" />
          <div className="skeleton mid" />
        </div>
      </div>
    );
  }

  // 3) 실패
  if (error) {
    return (
      <div className="card result-card">
        {title('예측 실패')}
        <div className="result-empty error">
          <div className="big-ico">😵</div>
          <strong>예측에 실패했어요</strong>
          <span>진행 상태의 오류 메시지를 확인해 주세요</span>
        </div>
      </div>
    );
  }

  // 4) 대기
  return (
    <div className="card result-card">
      {title('LightGBM 예측 결과')}
      <div className="result-empty">
        <div className="big-ico">🛵</div>
        <strong>예측 결과가 여기에 표시돼요</strong>
        <span>왼쪽에서 주문 조건을 고르고 예측하기를 눌러 주세요</span>
      </div>
    </div>
  );
}
