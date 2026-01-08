# Google Maps API 사용 정책 및 가이드

## 개요

이 애플리케이션은 Google Maps Platform의 Geocoding API를 사용하여 주소를 좌표로 변환합니다.

## 보안 정책

### ⚠️ 중요: API 키 보안

1. **절대 API 키를 코드에 하드코딩하지 마세요**
   - 기존 코드에서 발견된 하드코딩된 API 키는 제거되었습니다
   - API 키는 환경 변수나 설정 파일을 통해 관리합니다

2. **API 키 관리 방법**

   **방법 1: 환경 변수 (권장)**
   ```bash
   # Windows (PowerShell)
   $env:GOOGLE_MAPS_API_KEY="your_api_key_here"
   
   # Windows (CMD)
   set GOOGLE_MAPS_API_KEY=your_api_key_here
   
   # Linux/Mac
   export GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

   **방법 2: .env 파일**
   ```bash
   # .env 파일 생성
   cp .env.example .env
   # .env 파일 편집하여 API 키 입력
   ```

   **방법 3: 로컬 설정 파일 (개발용만)**
   ```
   config/api_key.txt 파일에 API 키 저장
   ```

3. **Git에 커밋하지 않기**
   - `.env` 파일은 `.gitignore`에 포함되어 있습니다
   - `config/api_key.txt`도 `.gitignore`에 포함되어 있습니다
   - API 키가 포함된 파일은 절대 Git에 커밋하지 마세요

## API 키 발급 방법

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/

2. **프로젝트 생성 또는 선택**

3. **API 활성화**
   - Geocoding API 활성화
   - Maps JavaScript API (필요한 경우)

4. **API 키 생성**
   - "사용자 인증 정보" → "사용자 인증 정보 만들기" → "API 키"

5. **API 키 제한 설정 (권장)**
   - IP 주소 제한
   - HTTP 리퍼러 제한
   - API 제한 (Geocoding API만 허용)

## 사용량 및 비용

### 무료 할당량
- Google Maps Platform은 월 $200의 무료 크레딧을 제공합니다
- Geocoding API: 월 40,000건 무료

### 사용량 모니터링
- Google Cloud Console에서 API 사용량을 모니터링하세요
- 사용량이 한도에 근접하면 알림을 설정하세요

### 비용 최적화
1. **캐싱**: 동일한 주소는 캐시하여 재사용
2. **배치 요청**: 가능한 경우 배치로 처리
3. **사용량 제한**: 애플리케이션 레벨에서 요청 제한 구현

## 에러 처리

애플리케이션은 다음 에러를 처리합니다:

- **INVALID_REQUEST**: API 키가 유효하지 않음
- **OVER_QUERY_LIMIT**: 사용량 한도 초과
- **REQUEST_DENIED**: API 요청 거부
- **ZERO_RESULTS**: 검색 결과 없음

## 대안

Google Maps API를 사용할 수 없는 경우:

1. **오픈소스 지오코딩 서비스**
   - Nominatim (OpenStreetMap)
   - Mapbox Geocoding API

2. **로컬 데이터베이스**
   - 한국 행정구역 좌표 데이터베이스
   - CSV/JSON 파일 기반 검색

## 법적 고지사항

Google Maps Platform 사용 시 다음 약관을 준수해야 합니다:

- [Google Maps Platform Terms of Service](https://developers.google.com/maps/terms)
- [Google Maps Platform Service Specific Terms](https://cloud.google.com/maps-platform/terms/maps-service-terms)

## 참고 자료

- [Google Maps Platform 문서](https://developers.google.com/maps/documentation)
- [Geocoding API 가이드](https://developers.google.com/maps/documentation/geocoding)
- [API 키 보안 모범 사례](https://developers.google.com/maps/api-security-best-practices)

## 문제 해결

### API 키가 작동하지 않는 경우

1. API 키가 올바르게 설정되었는지 확인
2. Geocoding API가 활성화되었는지 확인
3. API 키 제한 설정 확인
4. 사용량 한도 확인

### 에러 메시지

- "API 키가 유효하지 않습니다": API 키를 확인하세요
- "사용량 한도를 초과했습니다": 무료 할당량을 확인하거나 결제 정보를 추가하세요
- "API 요청이 거부되었습니다": API 키 권한 및 제한 설정을 확인하세요
