import pandas as pd
import joblib
import uvicorn

from fastapi import FastAPI, APIRouter, HTTPException

# 1) 서비스: 모델 불러오기 및 예측
class DeliveryService:
    def __init__(self):
        # 서비스 객체 생성 시 모델과 지표 불러오기
        self.model = joblib.load('./python/delivery_model.pkl')
        self.metrics = joblib.load('./python/delivery_metrics.pkl')

        self.num_cols = [
            'distance_km',
            'order_hour',
            'Delivery_person_Age',
            'Delivery_person_Ratings',
            'multiple_deliveries'
        ]

        self.cat_cols = [
            'Weatherconditions',
            'Road_traffic_density',
            'Festival',
            'City',
            'Type_of_vehicle'
        ]

    def predict(self, item):

        # 필수 컬럼 확인
        required_cols = self.num_cols + self.cat_cols
        for col in required_cols:
            if col not in item:
                return {'success': False, 'message': f'필수 항목이 없습니다: {col}'}


        # 입력값을 한 행으로 변환
        sample = pd.DataFrame([item])
        sample = sample[required_cols]

        # 학습할 때와 동일한 타입으로 변환
        try:
            for col in self.num_cols:
                sample[col] = sample[col].astype(float)
        except (ValueError, TypeError):
            return {'success': False, 'message': '수치형 항목에 숫자를 입력해야 합니다.' }
        
        for col in self.cat_cols:
            sample[col] = sample[col].astype('category')

        # 예측
        pred = self.model.predict(sample)

        return {
            'predicted_minutes': round(float(pred[0]), 2),
            'r2': float(self.metrics['r2'])
        }


# 2) 서비스 객체 생성
# 요청마다 생성하지 않으므로 모델도 요청마다 불러오지 않음
delivery_service = DeliveryService()

# 3) 라우터: HTTP 요청 처리
router = APIRouter(prefix='/api')


# POST http://127.0.0.1:8000/api/predict/stream
import json
from fastapi.responses import StreamingResponse

@router.post('/predict/stream')
def predict_stream(item: dict):

    def generate():
        # 기존 서비스의 예측 함수 사용
        result = delivery_service.predict(item)

        # 서비스에서 실패 결과를 반환한 경우
        if result.get('success') is False:
            yield (
                'event: error\n'
                f'data: {json.dumps(result, ensure_ascii=False)}\n\n'
            )
            return

        # 예측 결과와 R²를 SSE 이벤트로 전달
        yield (
            'event: result\n'
            f'data: {json.dumps(result, ensure_ascii=False)}\n\n'
        )

    return StreamingResponse(
        generate(),
        media_type='text/event-stream')




# 4) FastAPI 생성 및 라우터 연결
app = FastAPI()
app.include_router(router)


# 5) 서버 실행 — 파일의 마지막에 작성
if __name__ == '__main__':
    uvicorn.run(
        'FastApi:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )