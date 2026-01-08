# models/load_model.py
import pandas as pd
from typing import Dict, List, Any, Optional
import json
import os

class LoadModel:
    """하중 데이터를 관리하는 모델 클래스"""
    
    def __init__(self):
        """하중 모델 초기화"""
        # 기본 컬럼 정의
        self.columns = [
            'ID', 'floor', 'name',
            'f1', 'd1', 't1', 'l1',  # 마감1 관련 정보
            'f2', 'd2', 't2', 'l2',  # 마감2 관련 정보
            'f3', 'd3', 't3', 'l3',  # 마감3 관련 정보
            'f4', 'd4', 't4', 'l4',  # 마감4 관련 정보
            'f5', 'd5', 't5', 'l5',  # 마감5 관련 정보
            'f6', 'd6', 't6', 'l6',  # 마감6 관련 정보
            'SDL',                    # 추가 고정하중
            'Type',                   # 하중 타입
            'conthk',                 # 콘크리트 두께
            'conLoad',                # 콘크리트 하중
            'DL',                     # 총 고정하중
            'Category',               # 하중 카테고리
            'subcategory',            # 하중 서브카테고리
            'LR',                     # 지붕활하중 저감계수
            'LL',                     # 활하중
            'Service',                # 사용하중
            'Strength'                # 계수하중
        ]
        
        # DataFrame 초기화
        self.loads_data = pd.DataFrame(columns=self.columns)
        self._file_path: Optional[str] = None
        
    def add_load(self, load_data: Dict[str, Any]) -> bool:
        """
        하중 데이터 추가
        
        Args:
            load_data: 추가할 하중 데이터 딕셔너리
            
        Returns:
            bool: 추가 성공 여부
        """
        try:
            # ID 자동 생성
            load_data['ID'] = len(self.loads_data) + 1
            
            # DataFrame에 데이터 추가
            self.loads_data = pd.concat([
                self.loads_data, 
                pd.DataFrame([load_data])
            ], ignore_index=True)
            return True
        except Exception:
            return False
            
    def update_load(self, index: int, load_data: Dict[str, Any]) -> bool:
        """
        하중 데이터 수정
        
        Args:
            index: 수정할 데이터의 인덱스
            load_data: 수정할 하중 데이터
            
        Returns:
            bool: 수정 성공 여부
        """
        try:
            if 0 <= index < len(self.loads_data):
                for key, value in load_data.items():
                    if key in self.columns:
                        self.loads_data.at[index, key] = value
                return True
            return False
        except Exception:
            return False
            
    def delete_load(self, index: int) -> bool:
        """
        하중 데이터 삭제
        
        Args:
            index: 삭제할 데이터의 인덱스
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            if 0 <= index < len(self.loads_data):
                self.loads_data = self.loads_data.drop(index).reset_index(drop=True)
                # ID 재정렬
                self.loads_data['ID'] = range(1, len(self.loads_data) + 1)
                return True
            return False
        except Exception:
            return False
    
    def get_load(self, index: int) -> Optional[Dict[str, Any]]:
        """
        특정 하중 데이터 조회
        
        Args:
            index: 조회할 데이터의 인덱스
            
        Returns:
            Optional[Dict[str, Any]]: 조회된 하중 데이터
        """
        try:
            if 0 <= index < len(self.loads_data):
                return self.loads_data.iloc[index].to_dict()
            return None
        except Exception:
            return None
    
    def get_all_loads(self) -> pd.DataFrame:
        """
        모든 하중 데이터 조회
        
        Returns:
            pd.DataFrame: 전체 하중 데이터
        """
        return self.loads_data.copy()
    
    def clear_loads(self) -> None:
        """하중 데이터 초기화"""
        self.loads_data = pd.DataFrame(columns=self.columns)
        
    def save_to_file(self, filename: str = None) -> None:
        """
        하중 데이터를 파일에 저장
        
        Args:
            filename: 저장할 파일 경로
            
        Raises:
            Exception: 파일 저장 중 오류 발생
        """
        save_path = filename or self._file_path
        if not save_path:
            raise ValueError("저장할 파일 경로가 지정되지 않았습니다.")
            
        try:
            self.loads_data.to_csv(save_path, index=False, encoding='utf-8')
            self._file_path = save_path
        except Exception as e:
            raise Exception(f"하중 데이터 저장 중 오류 발생: {str(e)}")
            
    def load_from_file(self, filename: str) -> None:
        """
        파일에서 하중 데이터 로드
        
        Args:
            filename: 로드할 파일 경로
            
        Raises:
            FileNotFoundError: 파일을 찾을 수 없는 경우
            Exception: 파일 로드 중 오류 발생
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
            
        try:
            self.loads_data = pd.read_csv(filename)
            self._file_path = filename
        except Exception as e:
            raise Exception(f"하중 데이터 로드 중 오류 발생: {str(e)}")
    
    @property
    def current_file_path(self) -> Optional[str]:
        """현재 작업 중인 파일 경로 반환"""
        return self._file_path