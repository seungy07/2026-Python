package team;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Flux;

@Service
public class PredictService {
    // 1. FastAPI 와 통신할 WebClient
    private final WebClient webClient;

    public PredictService( @Value("${fastapi.url}") String fastapiUrl ) {
        this.webClient = WebClient.builder().baseUrl( fastapiUrl ).build();
    }

    // 배달원 랜덤 배정용
    private final Random random = new Random();
    private static final String[] VEHICLES = { "motorcycle", "scooter", "electric_scooter", "bicycle" };

    // 2. FastAPI 스트리밍 엔드포인트 호출 → SSE 이벤트를 하나씩 받는 Flux 반환
    // Flux는 List와 다르게 정보를 다 받아서 한번에 보내는 것이 아니라 실시간으로 바로 바로 보냄
    public Flux<ServerSentEvent<String>> predictStream( Map<String, Object> request ) {
        // 2-1. 배달원 정보 랜덤 배정
        int age = 20 + random.nextInt( 20 );                                     // 20 ~ 39세
        double rating = Math.round( ( 4.0 + random.nextDouble() ) * 10 ) / 10.0;        // 4.0 ~ 5.0 (소수 첫째 자리)
        int multipleDeliveries = random.nextInt( 4 );                            // 0 ~ 3건
        String vehicle = VEHICLES[ random.nextInt( VEHICLES.length ) ];                 // 4종 중 1개

        // 2-2. React 주문 정보 + 랜덤 배달원 정보 → 모델 학습 컬럼 이름/값으로 변환
        Map<String, Object> body = new HashMap<>();
        String city = String.valueOf( request.get( "city" ) );
        body.put( "distance_km", request.get( "distance_km" ) );
        body.put( "order_hour", Integer.parseInt( String.valueOf( request.get( "order_time" ) ).split( ":" )[0] ) ); // "19:30" → 19
        body.put( "Weatherconditions", "conditions " + request.get( "weather" ) );   // "Sunny" → "conditions Sunny"
        body.put( "Road_traffic_density", request.get( "traffic" ) );
        body.put( "Festival", request.get( "festival" ) );
        body.put( "City", "Metropolitian".equals( city ) ? "Metropolitan" : city ); // 모델은 고친 철자로 학습
        body.put( "Delivery_person_Age", age );
        body.put( "Delivery_person_Ratings", rating );
        body.put( "multiple_deliveries", multipleDeliveries );
        body.put( "Type_of_vehicle", vehicle );

        // 2-3. React 에 보낼 배정 결과 (JSON 문자열)
        String driver = String.format(
                "{\"age\":%d,\"rating\":%.1f,\"multiple_deliveries\":%d,\"vehicle\":\"%s\"}",
                age, rating, multipleDeliveries, vehicle );

        return webClient.post()
                .uri( "/api/predict/stream" )                  // FastAPI 엔드포인트
                .contentType( MediaType.APPLICATION_JSON )     // 보내는 형식 : JSON
                .accept( MediaType.TEXT_EVENT_STREAM )         // 받는 형식 : SSE
                .bodyValue( body )                             // 주문 정보 + 배달원 정보 전달
                .retrieve()
                .bodyToFlux( new ParameterizedTypeReference<ServerSentEvent<String>>() {} )
                // 3. 다음 이벤트가 30초 안에 오지 않으면 에러 처리
                .timeout( Duration.ofSeconds( 30 ) )
                // 4. Spring 이 먼저 보내는 이벤트 2개 : 진행 상태 + 배정된 배달원 정보
                .startWith( event( "status", "랜덤값 설정중.." ),
                            event( "driver", driver ) )
                // 5. FastAPI 꺼짐 / 주소 오류 / 4xx·5xx 응답 / 타임아웃 → 에러 이벤트로 변환하여 전달
                .onErrorResume( e -> Flux.just( event( "error", "AI 서버 통신 실패: " + e.getMessage() ) ) );
    }

    // 6. SSE 이벤트 생성 도우미 ( event: 이름 , data: 내용 )
    private ServerSentEvent<String> event( String name, String data ) {
        return ServerSentEvent.<String>builder().event( name ).data( data ).build();
    }
}
