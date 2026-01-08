# models/project_model.py
from datetime import datetime
import json
import os
from typing import Dict, Any, Optional

class ProjectModel:
    """프로젝트 정보를 관리하는 모델 클래스"""
    
    def __init__(self):
        """프로젝트 모델 초기화"""
        self.project_info: Dict[str, Any] = {
            'code': '',              # 프로젝트 코드
            'project': '',           # 프로젝트명
            'address': '',           # 주소
            'occupancy': '',         # 용도
            'area': '',              # 면적
            'sfloor': '',           # 지상층수
            'bfloor': '',           # 지하층수
            'height': '',           # 건물높이
            'importance': '',        # 중요도
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'modified_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self._file_path: Optional[str] = None