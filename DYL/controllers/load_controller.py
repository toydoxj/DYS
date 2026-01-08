# controllers/load_controller.py
from typing import Tuple, Dict, Any, List, Optional
import pandas as pd
from models.load_model import LoadModel

class LoadController:
    """하중 데이터와 관련된 사용자 인터페이스와 모델 사이의 중재자"""
    
    def __init__(self, load_model: LoadModel):
        """
        LoadController 초기화
        
        Args:
            load_model: 하중 데이터 모델
        """
        self.load_model = load_model
    
    def add_load_data(self, load_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        하중 데이터 추가
        
        Args:
            load_data: 추가할 하중 데이터
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            if self.load_model.add_load(load_data):
                return True, "하중 데이터가 추가되었습니다."
            return False, "하중 데이터 추가 실패"
        except Exception as e:
            return False, f"하중 데이터 추가 중 오류 발생: {str(e)}"
    
    def update_load_data(self, index: int, load_data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        하중 데이터 수정
        
        Args:
            index: 수정할 데이터의 인덱스
            load_data: 수정할 하중 데이터
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            if self.load_model.update_load(index, load_data):
                return True, "하중 데이터가 수정되었습니다."
            return False, "하중 데이터 수정 실패"
        except Exception as e:
            return False, f"하중 데이터 수정 중 오류 발생: {str(e)}"
    
    def delete_load_data(self, index: int) -> Tuple[bool, str]:
        """
        하중 데이터 삭제
        
        Args:
            index: 삭제할 데이터의 인덱스
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            if self.load_model.delete_load(index):
                return True, "하중 데이터가 삭제되었습니다."
            return False, "하중 데이터 삭제 실패"
        except Exception as e:
            return False, f"하중 데이터 삭제 중 오류 발생: {str(e)}"
    
    def get_load_data(self, index: int) -> Optional[Dict[str, Any]]:
        """
        특정 하중 데이터 조회
        
        Args:
            index: 조회할 데이터의 인덱스
            
        Returns:
            Optional[Dict[str, Any]]: 조회된 하중 데이터
        """
        return self.load_model.get_load(index)
    
    def get_all_loads(self) -> pd.DataFrame:
        """
        모든 하중 데이터 조회
        
        Returns:
            pd.DataFrame: 전체 하중 데이터
        """
        return self.load_model.get_all_loads()
    
    def calculate_total_load(self, index: int) -> Tuple[bool, float, str]:
        """
        특정 하중의 총 하중 계산
        
        Args:
            index: 계산할 하중 데이터의 인덱스
            
        Returns:
            Tuple[bool, float, str]: (성공 여부, 계산된 총 하중, 메시지)
        """
        try:
            load_data = self.load_model.get_load(index)
            if load_data is None:
                return False, 0.0, "해당 인덱스의 하중 데이터가 없습니다."
            
            # 여기에 총 하중 계산 로직 구현
            total_load = 0.0  # 실제 계산 로직으로 대체 필요
            
            return True, total_load, "총 하중이 계산되었습니다."
        except Exception as e:
            return False, 0.0, f"총 하중 계산 중 오류 발생: {str(e)}"