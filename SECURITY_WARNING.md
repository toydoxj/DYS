# ⚠️ 보안 경고: 하드코딩된 API 키 발견

## 발견된 문제

`UI/DYL.py` 파일의 2302번째 줄에서 Google Maps API 키가 하드코딩되어 있습니다:

```python
gmaps = googlemaps.Client(key='AIzaSyASWyn_2d_GsDk0a8yNJTTGK30LTSAFRNY')
```

## 보안 위험

1. **API 키 노출**: 코드에 API 키가 노출되면 누구나 사용할 수 있습니다
2. **비용 발생**: 악의적인 사용자가 API를 남용하면 예상치 못한 비용이 발생할 수 있습니다
3. **Git 저장소 노출**: 이 코드가 Git에 커밋되면 API 키가 공개됩니다

## 권장 조치

### 즉시 조치

1. **해당 API 키 비활성화**
   - Google Cloud Console에서 해당 API 키를 즉시 삭제하거나 비활성화하세요
   - 새로운 API 키를 발급받으세요

2. **코드 수정**
   - 하드코딩된 API 키를 제거하세요
   - 새로운 모듈화된 코드(`dys/core/services/geocoding_service.py`)를 사용하세요

### 코드 수정 방법

기존 코드를 다음과 같이 수정하세요:

**기존 (위험):**
```python
gmaps = googlemaps.Client(key='AIzaSyASWyn_2d_GsDk0a8yNJTTGK30LTSAFRNY')
```

**수정 후 (안전):**
```python
from dys.core.services.geocoding_service import GeocodingService

geocoding_service = GeocodingService()
if geocoding_service.is_available():
    lat, lng = geocoding_service.geocode(address)
```

또는 환경 변수 사용:
```python
import os
import googlemaps

api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if api_key:
    gmaps = googlemaps.Client(key=api_key)
```

## 새로운 모듈화된 구조 사용

새로운 모듈화된 코드는 안전하게 API 키를 관리합니다:

- 환경 변수에서 로드
- .env 파일에서 로드
- 로컬 설정 파일에서 로드 (개발용)
- API 키가 없을 때 적절한 에러 메시지 표시

자세한 내용은 [GOOGLE_API_POLICY.md](GOOGLE_API_POLICY.md)를 참조하세요.

## 추가 보안 권장사항

1. **API 키 제한 설정**
   - Google Cloud Console에서 API 키에 IP 주소 제한 설정
   - HTTP 리퍼러 제한 설정
   - 특정 API만 허용 (Geocoding API만)

2. **사용량 모니터링**
   - Google Cloud Console에서 API 사용량 모니터링
   - 사용량 알림 설정

3. **정기적인 키 순환**
   - 주기적으로 API 키를 재발급하고 교체
   - 오래된 키는 삭제
