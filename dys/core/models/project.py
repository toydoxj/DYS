"""프로젝트 정보 모델"""

from typing import Dict, Any, Optional
from datetime import datetime
from .base import BaseModel
from dys.config.constants import PROJECT_INFO_FIELDS


class ProjectModel(BaseModel):
    """프로젝트 정보 모델"""
    
    def __init__(self):
        """프로젝트 모델 초기화"""
        super().__init__()
        self._info: Dict[str, str] = {
            field: '' for field in PROJECT_INFO_FIELDS
        }
        self._info['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._info['modified_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_info(self, key: str) -> str:
        """
        프로젝트 정보 조회
        
        Args:
            key: 정보 키
            
        Returns:
            str: 정보 값
        """
        return self._info.get(key, '')
    
    def set_info(self, key: str, value: str):
        """
        프로젝트 정보 설정
        
        Args:
            key: 정보 키
            value: 정보 값
        """
        if key in self._info:
            if self._info[key] != value:
                self._info[key] = value
                self._info['modified_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.set_modified(True)
    
    def get_all_info(self) -> Dict[str, str]:
        """
        모든 프로젝트 정보 조회
        
        Returns:
            Dict[str, str]: 전체 프로젝트 정보
        """
        return self._info.copy()
    
    def set_all_info(self, info: Dict[str, str]):
        """
        모든 프로젝트 정보 설정
        
        Args:
            info: 프로젝트 정보 딕셔너리
        """
        for key, value in info.items():
            if key in self._info:
                self._info[key] = value
        self._info['modified_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.set_modified(True)
    
    def clear(self):
        """프로젝트 정보 초기화"""
        self._info = {
            field: '' for field in PROJECT_INFO_FIELDS
        }
        self._info['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._info['modified_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.set_modified(False)
        self.set_file_path(None)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return self._info.copy()
    
    def from_dict(self, data: Dict[str, Any]):
        """딕셔너리에서 로드"""
        self.set_all_info(data)
        self.set_modified(False)
