// 실시간 진행 상태 타임라인
// timeline : [{ kind: 'status' | 'result' | 'error', msg, t(요청 후 경과 초) }]
export default function StatusLog({ timeline, loading, result, error }) {
  let badge = null;
  if (loading) badge = <span className="live on">LIVE</span>;
  else if (result) badge = <span className="live done">완료</span>;
  else if (error) badge = <span className="live fail">오류</span>;

  return (
    <div className="card status-card">
      <div className="card-title">
        <span>📡 실시간 진행 상태</span>
        {badge}
      </div>

      {timeline.length === 0 ? (
        <div className="empty-state">
          <div className="ico">📨</div>
          <div>예측을 시작하면 서버가 보내는<br />진행 메시지가 실시간으로 표시돼요</div>
        </div>
      ) : (
        <ol className="timeline">
          {timeline.map((item, i) => {
            // 요청 중이면 마지막 상태 메시지는 "진행 중"
            const current = loading && i === timeline.length - 1 && item.kind === 'status';
            let mark = '✓';
            if (item.kind === 'error') mark = '!';
            else if (item.kind === 'result') mark = '★';
            else if (current) mark = '';
            return (
              <li key={i} className={`tl-item ${item.kind} ${current ? 'current' : ''}`}>
                <span className="tl-dot">{mark}</span>
                <span className="tl-text">{item.msg}</span>
                <span className="tl-time">+{item.t.toFixed(1)}s</span>
              </li>
            );
          })}
        </ol>
      )}

      <div className="card-foot">SSE · FastAPI → Spring → React 실시간 중계</div>
    </div>
  );
}
