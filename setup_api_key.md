# Google Maps API 키 설정 가이드

## 방법 1: .env 파일 사용 (권장)

1. 프로젝트 루트 디렉토리에 `.env` 파일이 생성되었습니다.
2. `.env` 파일을 열어서 `your_api_key_here`를 실제 API 키로 변경하세요.

```env
GOOGLE_MAPS_API_KEY=실제_API_키_여기에_입력
```

## 방법 2: 환경 변수로 설정

### Windows PowerShell
```powershell
$env:GOOGLE_MAPS_API_KEY="실제_API_키_여기에_입력"
```

### Windows CMD
```cmd
set GOOGLE_MAPS_API_KEY=실제_API_키_여기에_입력
```

### Linux/Mac
```bash
export GOOGLE_MAPS_API_KEY="실제_API_키_여기에_입력"
```

## 방법 3: 로컬 설정 파일 (개발용)

1. `config` 디렉토리에 `api_key.txt` 파일을 생성하세요.
2. 파일에 API 키만 입력하세요 (줄바꿈 없이).

```
실제_API_키_여기에_입력
```

## API 키 발급 방법

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/

2. **프로젝트 생성 또는 선택**
   - 새 프로젝트를 만들거나 기존 프로젝트를 선택하세요.

3. **API 활성화**
   - "API 및 서비스" → "라이브러리"로 이동
   - "Geocoding API" 검색 후 활성화

4. **API 키 생성**
   - "사용자 인증 정보" → "사용자 인증 정보 만들기" → "API 키"
   - 생성된 API 키를 복사하세요.

5. **API 키 제한 설정 (권장)**
   - 생성된 API 키를 클릭하여 편집
   - "애플리케이션 제한사항" 설정
   - "API 제한"에서 "Geocoding API"만 선택

## 설정 확인

API 키를 설정한 후 애플리케이션을 다시 시작하면 지오코딩 기능을 사용할 수 있습니다.

## 주의사항

⚠️ **중요:**
- API 키는 절대 Git에 커밋하지 마세요!
- `.env` 파일과 `config/api_key.txt`는 `.gitignore`에 포함되어 있습니다.
- API 키를 공유하지 마세요.
- 사용량 모니터링을 설정하세요.

## 문제 해결

### API 키가 작동하지 않는 경우

1. API 키가 올바르게 입력되었는지 확인
2. Geocoding API가 활성화되었는지 확인
3. API 키 제한 설정 확인
4. 애플리케이션 재시작

### 사용량 한도 초과

- Google Maps Platform은 월 $200의 무료 크레딧을 제공합니다
- Geocoding API: 월 40,000건 무료
- 사용량이 초과되면 결제 정보를 추가하거나 사용량을 줄이세요
