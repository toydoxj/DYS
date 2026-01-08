# Google Maps API 키 빠른 설정

## 가장 쉬운 방법: 환경 변수 설정

### PowerShell에서 실행 (현재 세션용)
```powershell
$env:GOOGLE_MAPS_API_KEY="여기에_실제_API_키_입력"
```

### 영구적으로 설정하려면
1. Windows 검색에서 "환경 변수" 검색
2. "시스템 환경 변수 편집" 선택
3. "환경 변수" 버튼 클릭
4. "새로 만들기" → 변수 이름: `GOOGLE_MAPS_API_KEY`, 값: `실제_API_키`
5. 확인 클릭

## 방법 2: config/api_key.txt 파일 사용

1. `config` 폴더에 `api_key.txt` 파일 생성
2. 파일에 API 키만 입력 (줄바꿈 없이)
3. 애플리케이션 재시작

## 방법 3: .env 파일 사용

프로젝트 루트에 `.env` 파일을 만들고:
```
GOOGLE_MAPS_API_KEY=여기에_실제_API_키_입력
```

## API 키 발급

1. https://console.cloud.google.com/ 접속
2. 프로젝트 생성/선택
3. "API 및 서비스" → "라이브러리"
4. "Geocoding API" 검색 후 활성화
5. "사용자 인증 정보" → "API 키 만들기"
6. 생성된 키 복사

## 설정 확인

애플리케이션을 다시 시작하면 API 키가 적용됩니다.
