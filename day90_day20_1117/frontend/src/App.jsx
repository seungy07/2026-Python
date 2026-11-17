import { useRef, useState } from 'react';
import axios from 'axios';
import Scene, { getPhase, PHASE_INFO } from './components/Scene';
import OrderForm, { WEATHER } from './components/OrderForm';
import StatusLog from './components/StatusLog';
import DriverCard from './components/DriverCard';
import ResultCard from './components/ResultCard';

// Spring 게이트웨이 주소 (React 는 FastAPI 주소를 모른다)
const API_URL = 'http://localhost:8080/api/predict';

// 폼 기본값 , 키 이름은 Spring → FastAPI 로 그대로 전달된다
const INITIAL_FORM = {
  distance_km: 5,
  order_time: '19:30',
  weather: 'Sunny',
  traffic: 'Medium',
  festival: 'No',
  city: 'Urban',
};

export default function App() {
  const [form, setForm] = useState(INITIAL_FORM);  // 1. 입력값 (바꾸는 즉시 배경에 반영)
  const [submitted, setSubmitted] = useState(null); // 2. 예측 요청 당시의 입력값
  const [loading, setLoading] = useState(false);   // 3. 요청 중 여부 (버튼 비활성화)
  const [timeline, setTimeline] = useState([]);    // 4. 진행 상태 타임라인
  const [driver, setDriver] = useState(null);      // 5. Spring 이 배정한 랜덤값
  const [result, setResult] = useState(null);      // 6. 예측 결과 + R2
  const [error, setError] = useState('');          // 7. 에러 메시지

  // 이미 처리한 응답 글자 수 (responseText 는 누적되므로 새로 온 부분만 읽기 위함)
  const readLenRef = useRef(0);
  // 요청 시작 시각 (각 메시지가 몇 초 만에 왔는지 표시)
  const startRef = useRef(0);

  const addLog = (kind, msg) => {
    const t = (performance.now() - startRef.current) / 1000;
    setTimeline((prev) => [...prev, { kind, msg, t }]);
  };

  // [1] SSE 이벤트 1개 처리 : "event:이름\ndata:내용"
  const handleEvent = (block) => {
    let type = 'message';
    const dataLines = [];
    block.split('\n').forEach((raw) => {
      const line = raw.replace(/\r$/, '');
      if (line.startsWith('event:')) type = line.slice(6).trim();
      else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
    });
    const data = dataLines.join('\n');

    if (type === 'status') {
      addLog('status', data);
    } else if (type === 'driver') {
      try { setDriver(JSON.parse(data)); } catch { setDriver(null); }
    } else if (type === 'result') {
      try {
        setResult(JSON.parse(data));
        addLog('result', '예측 결과 수신 완료');
      } catch {
        setError('결과 형식을 읽을 수 없습니다: ' + data);
        addLog('error', '결과 형식을 읽을 수 없습니다');
      }
    } else if (type === 'error') {
      // FastAPI 는 {"success":false,"message":"..."} 형태로 보내므로 message 만 꺼냄
      let msg = data;
      try { msg = JSON.parse(data).message ?? data; } catch { /* 일반 문자열 */ }
      setError(msg);
      addLog('error', msg);
    }
  };

  // [2] 지금까지 받은 전체 텍스트에서 "완성된 이벤트"만 잘라 처리
  const processText = (fullText) => {
    const newText = fullText.substring(readLenRef.current); // 새로 도착한 부분
    const lastSep = newText.lastIndexOf('\n\n');            // 이벤트는 빈 줄로 구분
    if (lastSep === -1) return;                             // 아직 완성된 이벤트 없음
    readLenRef.current += lastSep + 2;                      // 처리한 위치 기록
    newText.substring(0, lastSep).split('\n\n').forEach((block) => {
      if (block.trim()) handleEvent(block);
    });
  };

  // [3] 예측 요청 : axios POST + onDownloadProgress 로 SSE 스트림 실시간 수신
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeline([]);
    setDriver(null);
    setResult(null);
    setError('');
    setSubmitted(form);
    readLenRef.current = 0;
    startRef.current = performance.now();

    try {
      const response = await axios.post(API_URL, form, {
        headers: { Accept: 'text/event-stream' },
        responseType: 'text',
        // 응답이 끝나기 전에도 데이터가 도착할 때마다 호출된다
        onDownloadProgress: (progressEvent) => {
          const xhr = progressEvent.event?.target;
          if (xhr && typeof xhr.responseText === 'string') processText(xhr.responseText);
        },
      });
      // 스트림 종료 후 남은 이벤트 처리 (마지막 빈 줄 누락 대비)
      processText(String(response.data ?? '') + '\n\n');
    } catch (err) {
      console.error('예측 요청 오류:', err);
      const msg = 'Spring 서버에 연결할 수 없습니다. (localhost:8080 실행 여부 확인)';
      setError(msg);
      addLog('error', msg);
    } finally {
      setLoading(false);
    }
  };

  // 밤에는 카드도 어두운 유리로
  const phase = getPhase(form.order_time);
  const theme = phase === 'night' ? 'theme-dark' : 'theme-light';
  const weather = WEATHER.find((w) => w.value === form.weather);
  const festival = form.festival === 'Yes';

  return (
    <>
      <Scene form={form} loading={loading} result={result} />

      <div className={`app ${theme}`}>
        <div className="container">
          <header className="card header">
            <div className="brand">
              <div className="logo">🛵</div>
              <div>
                <h1>배달 시간 예측</h1>
                <p>LightGBM · FastAPI → Spring → React 실시간 SSE</p>
              </div>
            </div>
            <div className="scene-chips">
              <span className="chip">{PHASE_INFO[phase].icon} {PHASE_INFO[phase].label} · {form.order_time}</span>
              {weather && <span className="chip">{weather.icon} {weather.label}</span>}
              {festival && <span className="chip festival">🎉 축제 진행 중</span>}
            </div>
          </header>

          <main className="layout">
            <OrderForm form={form} setForm={setForm} onSubmit={handleSubmit} loading={loading} />

            <section className="right">
              <ResultCard
                result={result}
                loading={loading}
                error={error}
                orderTime={submitted?.order_time ?? form.order_time}
              />
              <StatusLog timeline={timeline} loading={loading} result={result} error={error} />
              <DriverCard driver={driver} loading={loading} />
            </section>
          </main>
        </div>
      </div>
    </>
  );
}
