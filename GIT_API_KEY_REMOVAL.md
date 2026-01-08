# Git에서 API 키 제거 가이드

## ⚠️ 중요: API 키가 Git 히스토리에 포함되어 있습니다

`UI/DYL.py` 파일에 하드코딩된 API 키가 Git에 커밋되어 있습니다.

## 즉시 조치

### 1단계: API 키 비활성화
Google Cloud Console에서 해당 API 키를 즉시 비활성화하세요.

### 2단계: 코드 수정 (완료됨)
`UI/DYL.py` 파일의 하드코딩된 API 키를 제거하고 환경 변수에서 로드하도록 수정했습니다.

### 3단계: Git 히스토리에서 제거

#### 방법 1: git filter-branch 사용 (권장하지 않음)
```bash
# 주의: 이 명령은 Git 히스토리를 완전히 재작성합니다
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch UI/DYL.py" \
  --prune-empty --tag-name-filter cat -- --all

# 또는 특정 라인만 수정
git filter-branch -f --tree-filter \
  "sed -i 's/AIzaSyASWyn_2d_GsDk0a8yNJTTGK30LTSAFRNY/REMOVED_API_KEY/g' UI/DYL.py" \
  -- --all
```

#### 방법 2: BFG Repo-Cleaner 사용 (더 빠름, 권장)
```bash
# 1. BFG 다운로드: https://rtyley.github.io/bfg-repo-cleaner/
# 2. passwords.txt 파일 생성 (API 키 포함)
echo "AIzaSyASWyn_2d_GsDk0a8yNJTTGK30LTSAFRNY" > passwords.txt

# 3. BFG 실행
java -jar bfg.jar --replace-text passwords.txt

# 4. 히스토리 정리
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

#### 방법 3: 새 저장소로 마이그레이션 (가장 안전)
```bash
# 1. 새 저장소 생성
# 2. API 키가 제거된 코드만 복사
# 3. 새 저장소에 푸시
```

### 4단계: 강제 푸시 (주의!)
```bash
# 주의: 이 작업은 다른 개발자들에게 영향을 줍니다
git push origin --force --all
git push origin --force --tags
```

## 주의사항

⚠️ **Git 히스토리를 수정하면:**
- 다른 개발자들과 충돌 발생 가능
- 모든 개발자가 새 히스토리를 받아야 함
- 협업 중이라면 팀과 상의 후 진행

## 대안: 새 API 키 발급

Git 히스토리를 수정하지 않고:
1. 기존 API 키 비활성화
2. 새 API 키 발급
3. 코드 수정 (완료됨)
4. 새 API 키를 안전하게 설정

이 방법이 더 안전하고 간단합니다.

## 예방 조치

1. `.gitignore`에 API 키 파일 추가 (완료됨)
2. 코드 리뷰 시 API 키 검사
3. pre-commit 훅 설정
4. CI/CD에서 API 키 검사
