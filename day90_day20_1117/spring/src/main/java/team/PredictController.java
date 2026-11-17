package team;

import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping( "/api" )
@RequiredArgsConstructor
@CrossOrigin( origins = "http://localhost:5173" )   // React 로컬 포트 허용
public class PredictController {
    private final PredictService predictService;

    // 1. 예측 요청 + SSE 중계
    // http://localhost:8080/api/predict
    // React 주문 정보 : { "distance_km":5.2, "order_time":"19:30", "weather":"Sunny", "traffic":"High", "festival":"No", "city":"Urban" }
    // 배달원 정보(나이, 평점, 동시배달수, 이동수단)는 PredictService 에서 랜덤 배정하여 추가
    @PostMapping( value = "/predict", produces = MediaType.TEXT_EVENT_STREAM_VALUE )
    public Flux<ServerSentEvent<String>> predict( @RequestBody Map<String, Object> request ) {
        // map 형태로 받아서 서비스로 전달
        return predictService.predictStream( request );
    }
}
