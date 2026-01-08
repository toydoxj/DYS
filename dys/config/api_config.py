"""API 설정 관리"""

import os
from pathlib import Path
from typing import Optional


class APIConfig:
    """API 설정 관리 클래스
    
    Google Maps API 및 기타 외부 API 키를 안전하게 관리합니다.
    """
    
    def __init__(self):
        """API 설정 초기화"""
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # API 키 파일 경로 (gitignore에 포함됨)
        self.api_key_file = self.config_dir / "api_key.txt"
        self.env_file = self.base_dir / ".env"
    
    def get_google_maps_api_key(self) -> Optional[str]:
        """
        Google Maps API 키 가져오기
        
        우선순위:
        1. 환경 변수 GOOGLE_MAPS_API_KEY
        2. .env 파일
        3. config/api_key.txt (로컬 개발용)
        
        Returns:
            Optional[str]: API 키 또는 None
        """
        # 환경 변수에서 로드
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if api_key:
            return api_key
        
        # .env 파일에서 로드
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if line.startswith('GOOGLE_MAPS_API_KEY='):
                                return line.split('=', 1)[1].strip().strip('"').strip("'")
            except Exception as e:
                print(f".env 파일 읽기 오류: {e}")
        
        # 로컬 설정 파일에서 로드 (개발용)
        if self.api_key_file.exists():
            try:
                with open(self.api_key_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                print(f"API 키 파일 읽기 오류: {e}")
        
        return None
    
    def set_google_maps_api_key(self, api_key: str, save_to_file: bool = False):
        """
        Google Maps API 키 설정
        
        Args:
            api_key: API 키
            save_to_file: 파일에 저장할지 여부 (개발용, 프로덕션에서는 False 권장)
        """
        if save_to_file:
            try:
                with open(self.api_key_file, 'w', encoding='utf-8') as f:
                    f.write(api_key)
                print(f"API 키가 {self.api_key_file}에 저장되었습니다.")
            except Exception as e:
                print(f"API 키 저장 오류: {e}")
    
    def has_api_key(self) -> bool:
        """
        API 키 존재 여부 확인
        
        Returns:
            bool: API 키가 있으면 True
        """
        return self.get_google_maps_api_key() is not None
