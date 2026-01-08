# Google Maps API 설정 가이드

## 빠른 시작

### 1. API 키 발급
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 생성 또는 선택
3. Geocoding API 활성화
4. API 키 생성

### 2. API 키 설정

**방법 1: 환경 변수 (권장)**
```bash
# Windows PowerShell
$env:GOOGLE_MAPS_API_KEY="your_api_key_here"

# Windows CMD
set GOOGLE_MAPS_API_KEY=your_api_key_here

# Linux/Mac
export GOOGLE_MAPS_API_KEY=your_api_key_here
```

**방법 2: .env 파일**
```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집하여 API 키 입력
GOOGLE_MAPS_API_KEY=your_api_key_here
```

**방법 3: 로컬 설정 파일 (개발용)**
```
config/api_key.txt 파일에 API 키 저장
```

### 3. 애플리케이션 실행
```bash
python dys/main.py
```

## 주의사항

⚠️ **API 키는 절대 Git에 커밋하지 마세요!**

- `.env` 파일은 자동으로 `.gitignore`에 포함됩니다
- `config/api_key.txt`도 `.gitignore`에 포함됩니다
- API 키가 포함된 코드는 절대 커밋하지 마세요

## 상세 가이드

자세한 내용은 [GOOGLE_API_POLICY.md](GOOGLE_API_POLICY.md)를 참조하세요.
