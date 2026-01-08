# ⚠️ API 키 보안 감사 보고서

## 발견된 문제

### 🔴 심각: 하드코딩된 API 키 발견

**파일:** `UI/DYL.py` (2302번째 줄)
```python
gmaps = googlemaps.Client(key='AIzaSyASWyn_2d_GsDk0a8yNJTTGK30LTSAFRNY')
```

**위험도:** 🔴 매우 높음
- 실제 Google Maps API 키가 코드에 하드코딩되어 있음
- 이 파일이 Git에 커밋되어 있다면 API 키가 공개됨
- 누구나 이 키를 사용하여 API를 남용할 수 있음
- 예상치 못한 비용 발생 가능

### 🟡 경고: 문서 파일에 예시 포함

**파일:** `SECURITY_WARNING.md`
- 경고 문서이므로 예시로 포함된 것임
- 실제 API 키는 아니지만 주의 필요

## 즉시 조치 사항

### 1. API 키 비활성화 (최우선)

1. Google Cloud Console 접속: https://console.cloud.google.com/
2. "API 및 서비스" → "사용자 인증 정보"로 이동
3. 해당 API 키(`AIzaSyASWyn_2d_GsDk0a8yNJTTGK30LTSAFRNY`) 찾기
4. **즉시 삭제 또는 비활성화**

### 2. 코드 수정

`UI/DYL.py` 파일의 2302번째 줄을 수정:

**기존 (위험):**
```python
gmaps = googlemaps.Client(key='AIzaSyASWyn_2d_GsDk0a8yNJTTGK30LTSAFRNY')
```

**수정 후 (안전):**
```python
import os
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if api_key:
    gmaps = googlemaps.Client(key=api_key)
else:
    # API 키가 없을 때 처리
    gmaps = None
```

또는 새로운 모듈화된 서비스 사용:
```python
from dys.core.services.geocoding_service import GeocodingService

geocoding_service = GeocodingService()
if geocoding_service.is_available():
    lat, lng = geocoding_service.geocode(address)
```

### 3. Git 히스토리에서 제거 (이미 커밋된 경우)

만약 이 파일이 이미 Git에 커밋되어 있다면:

```bash
# Git 히스토리에서 API 키 제거
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch UI/DYL.py" \
  --prune-empty --tag-name-filter cat -- --all

# 또는 BFG Repo-Cleaner 사용 (더 빠름)
# bfg --replace-text passwords.txt
```

**주의:** Git 히스토리를 수정하면 다른 개발자들과 충돌이 발생할 수 있습니다.

### 4. 새 API 키 발급

1. Google Cloud Console에서 새 API 키 발급
2. API 키 제한 설정:
   - IP 주소 제한
   - HTTP 리퍼러 제한
   - Geocoding API만 허용
3. 사용량 알림 설정

## 예방 조치

### .gitignore 확인
다음 파일들이 .gitignore에 포함되어 있는지 확인:
- `.env`
- `config/api_key.txt`
- `**/api_key.txt`
- `*.key`
- `*.secret`

### 코드 검토 체크리스트
- [ ] 하드코딩된 API 키 제거
- [ ] 환경 변수 또는 설정 파일 사용
- [ ] .gitignore에 API 키 파일 추가
- [ ] 코드 리뷰 시 API 키 확인
- [ ] CI/CD 파이프라인에서 API 키 검사

## 참고

- [GOOGLE_API_POLICY.md](GOOGLE_API_POLICY.md): API 사용 정책
- [SECURITY_WARNING.md](SECURITY_WARNING.md): 보안 경고 상세
- [setup_api_key.md](setup_api_key.md): 안전한 API 키 설정 방법
