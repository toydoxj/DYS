"""애플리케이션 설정"""

import os
from pathlib import Path
from typing import Optional

class Settings:
    """애플리케이션 설정 관리"""
    
    def __init__(self):
        """설정 초기화"""
        self.base_dir = Path(__file__).parent.parent.parent
        self.resources_dir = self.base_dir / "resources"
        self.icons_dir = self.resources_dir / "icons"
        self.forms_dir = self.resources_dir / "forms"
        
        # 아이콘 경로
        self.icon_path = self.icons_dir / "icons.png"
        self.icon_ico_path = self.icons_dir / "icons.ico"
        
        # 데이터 디렉토리
        self.data_dir = self.base_dir / "form"
        self.docs_dir = self.base_dir / "docs"
        
    def get_icon_path(self, icon_name: str = "icons.png") -> Path:
        """아이콘 경로 반환"""
        return self.icons_dir / icon_name
    
    def get_data_path(self, filename: str) -> Path:
        """데이터 파일 경로 반환"""
        return self.data_dir / filename
    
    def get_docs_path(self, filename: str) -> Path:
        """문서 파일 경로 반환"""
        # docs 디렉토리가 없으면 상위 디렉토리에서 찾기
        docs_path = self.base_dir / "docs" / filename
        if not docs_path.exists():
            # 상위 디렉토리의 docs 폴더 확인
            parent_docs = self.base_dir.parent / "docs" / filename
            if parent_docs.exists():
                return parent_docs
        return docs_path

# 전역 설정 인스턴스
settings = Settings()
