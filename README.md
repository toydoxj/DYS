# DYL - PyQt6 Application

DYL은 PyQt6를 사용한 구조 설계 애플리케이션입니다.

## 주요 기능

- 구조물 정보 입력 및 관리
- 중력하중(Gravity Load) 계산
- 풍하중(Wind Load) 계산
- 활하중(Live Load) 계산
- 지진하중(Earthquake Load) 계산
- 하중 조합(Load Combination) 관리

## 요구사항

- Python 3.11+
- PyQt6
- PyQt6-WebEngine (지도 기능 사용 시 필요)
- pandas
- folium
- googlemaps (선택적, 지오코딩 기능 사용 시)
- 기타 의존성 패키지

### Google Maps API 설정 (선택적)

지오코딩 기능을 사용하려면 Google Maps API 키가 필요합니다.

**빠른 설정:**
```bash
# 환경 변수로 설정
export GOOGLE_MAPS_API_KEY="your_api_key_here"

# 또는 .env 파일 사용
cp .env.example .env
# .env 파일 편집하여 API 키 입력
```

자세한 내용은 [README_GOOGLE_API.md](README_GOOGLE_API.md)를 참조하세요.

## 설치 방법

1. 가상환경 활성화:
```bash
.\Scripts\Activate.ps1
```

2. 필요한 패키지 설치:
```bash
pip install PyQt6 PyQt6-WebEngine pandas folium googlemaps
```

3. (선택적) Google Maps API 키 설정:
```bash
# 환경 변수로 설정
export GOOGLE_MAPS_API_KEY="your_api_key_here"

# 또는 .env 파일 사용
cp .env.example .env
# .env 파일 편집하여 API 키 입력
```

## 실행 방법

```bash
python UI\DYL.py
```

## 프로젝트 구조

```
DYS/
├── UI/              # 사용자 인터페이스
├── DYL/             # MVC 패턴 구조
│   ├── controllers/ # 컨트롤러
│   ├── models/      # 데이터 모델
│   └── views/       # 뷰
├── Win32/           # Windows 관련 모듈
├── DYSteel/         # 강구조 관련 모듈
└── KDS/             # 한국설계기준 관련 모듈
```

## 라이선스

이 프로젝트의 라이선스 정보를 여기에 추가하세요.
