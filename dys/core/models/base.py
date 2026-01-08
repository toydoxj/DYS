"""기본 모델 클래스"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseModel(ABC):
    """기본 모델 클래스"""
    
    def __init__(self):
        """모델 초기화"""
        self._modified = False
        self._file_path: Optional[str] = None
    
    @property
    def is_modified(self) -> bool:
        """수정 여부 확인"""
        return self._modified
    
    @property
    def current_file_path(self) -> Optional[str]:
        """현재 파일 경로"""
        return self._file_path
    
    def set_modified(self, modified: bool = True):
        """수정 상태 설정"""
        self._modified = modified
    
    def set_file_path(self, file_path: Optional[str]):
        """파일 경로 설정"""
        self._file_path = file_path
    
    @abstractmethod
    def clear(self):
        """모델 초기화"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        pass
    
    @abstractmethod
    def from_dict(self, data: Dict[str, Any]):
        """딕셔너리에서 로드"""
        pass
