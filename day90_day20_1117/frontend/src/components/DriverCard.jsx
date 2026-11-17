import { useEffect, useState } from 'react';

// Spring 이 랜덤으로 설정한 배달원 정보 (SSE driver 이벤트)
const VEHICLES = {
  motorcycle: { label: '오토바이', icon: '🏍️' },
  scooter: { label: '스쿠터', icon: '🛵' },
  electric_scooter: { label: '전동 스쿠터', icon: '🛴' },
  bicycle: { label: '자전거', icon: '🚲' },
};
const VEHICLE_KEYS = Object.keys(VEHICLES);

// 슬롯머신처럼 값이 돌아가는 연출용 (실제 값은 Spring 이 보낸 driver)
const randomDriver = () => ({
  age: 20 + Math.floor(Math.random() * 20),
  rating: Math.round((4 + Math.random()) * 10) / 10,
  multiple_deliveries: Math.floor(Math.random() * 4),
  vehicle: VEHICLE_KEYS[Math.floor(Math.random() * VEHICLE_KEYS.length)],
});

export default function DriverCard({ driver, loading }) {
  const [shown, setShown] = useState(null);
  const [rolling, setRolling] = useState(false);

  // driver 이벤트를 받으면 0.8초 동안 값을 굴린 뒤 실제 값으로 멈춤
  useEffect(() => {
    if (!driver) {
      setShown(null);
      return undefined;
    }
    setRolling(true);
    const timer = setInterval(() => setShown(randomDriver()), 70);
    const stop = setTimeout(() => {
      clearInterval(timer);
      setShown(driver);
      setRolling(false);
    }, 800);
    return () => {
      clearInterval(timer);
      clearTimeout(stop);
    };
  }, [driver]);

  const d = shown ?? driver;

  const title = (
    <div className="card-title">
      <span>🎲 배정된 배달원</span>
      <span className="sub">Spring 랜덤 생성</span>
    </div>
  );

  if (!d) {
    return (
      <div className="card driver-card">
        {title}
        <div className="empty-state">
          <div className="ico">{loading ? '🎲' : '🧑‍✈️'}</div>
          <div>
            {loading ? '배달원을 배정하는 중…' : <>예측을 시작하면 배달원이<br />무작위로 배정돼요</>}
          </div>
        </div>
      </div>
    );
  }

  const v = VEHICLES[d.vehicle] ?? { label: d.vehicle, icon: '🛵' };
  const rating = Number(d.rating);
  const ratingPct = (Math.min(Math.max(rating, 0), 5) / 5) * 100;

  return (
    <div className={`card driver-card ${rolling ? 'rolling' : 'settled'}`}>
      {title}
      <div className="driver-top">
        <div className="avatar">{v.icon}</div>
        <div>
          <div className="driver-name">{v.label} 라이더</div>
          <div className="rating">
            <span className="stars" aria-label={`평점 ${rating}`}>
              <span className="base">★★★★★</span>
              <span className="fill" style={{ width: `${ratingPct}%` }}>★★★★★</span>
            </span>
            <b>{rating.toFixed(1)}</b>
          </div>
        </div>
      </div>
      <div className="driver-stats">
        <div className="stat"><span>나이</span><strong>{d.age}세</strong></div>
        <div className="stat"><span>동시 배달</span><strong>{d.multiple_deliveries}건</strong></div>
        <div className="stat"><span>이동수단</span><strong>{v.icon}</strong></div>
      </div>
      <div className="card-foot">같은 주문이라도 배달원에 따라 예측 시간이 달라져요</div>
    </div>
  );
}
