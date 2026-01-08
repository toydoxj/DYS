"""하중 데이터 모델"""

import pandas as pd
from typing import Dict, Any, Optional
from .base import BaseModel
from dys.config.constants import LOAD_TABLE_COLUMNS


class LoadModel(BaseModel):
    """하중 데이터 모델"""
    
    def __init__(self):
        """하중 모델 초기화"""
        super().__init__()
        self._df = pd.DataFrame(columns=LOAD_TABLE_COLUMNS)
    
    @property
    def dataframe(self) -> pd.DataFrame:
        """데이터프레임 반환"""
        return self._df.copy()
    
    def set_dataframe(self, df: pd.DataFrame):
        """
        데이터프레임 설정
        
        Args:
            df: 하중 데이터프레임
        """
        if not self._df.equals(df):
            self._df = df.copy()
            self.set_modified(True)
    
    def add_load(self, load_data: Dict[str, Any]) -> int:
        """
        하중 데이터 추가
        
        Args:
            load_data: 하중 데이터 딕셔너리
            
        Returns:
            int: 추가된 행의 인덱스
        """
        new_row = pd.DataFrame([load_data])
        self._df = pd.concat([self._df, new_row], ignore_index=True)
        self.set_modified(True)
        return len(self._df) - 1
    
    def update_load(self, index: int, load_data: Dict[str, Any]):
        """
        하중 데이터 업데이트
        
        Args:
            index: 행 인덱스
            load_data: 하중 데이터 딕셔너리
        """
        if 0 <= index < len(self._df):
            for key, value in load_data.items():
                if key in self._df.columns:
                    self._df.at[index, key] = value
            self.set_modified(True)
    
    def remove_load(self, index: int):
        """
        하중 데이터 삭제
        
        Args:
            index: 행 인덱스
        """
        if 0 <= index < len(self._df):
            self._df = self._df.drop(index).reset_index(drop=True)
            self.set_modified(True)
    
    def get_load(self, index: int) -> Optional[Dict[str, Any]]:
        """
        하중 데이터 조회
        
        Args:
            index: 행 인덱스
            
        Returns:
            Optional[Dict[str, Any]]: 하중 데이터 또는 None
        """
        if 0 <= index < len(self._df):
            return self._df.iloc[index].to_dict()
        return None
    
    def clear(self):
        """하중 데이터 초기화"""
        self._df = pd.DataFrame(columns=LOAD_TABLE_COLUMNS)
        self.set_modified(False)
        self.set_file_path(None)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return self._df.to_dict('records')
    
    def from_dict(self, data: Dict[str, Any]):
        """딕셔너리에서 로드"""
        if isinstance(data, list):
            self._df = pd.DataFrame(data)
        elif isinstance(data, dict):
            self._df = pd.DataFrame([data])
        else:
            self._df = pd.DataFrame(columns=LOAD_TABLE_COLUMNS)
        self.set_modified(False)
