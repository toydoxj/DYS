"""입력 검증 유틸리티"""

from PyQt6.QtGui import QDoubleValidator, QIntValidator
from typing import Optional


class Validators:
    """입력 검증기 클래스"""
    
    @staticmethod
    def create_double_validator(
        bottom: float = -999999.0,
        top: float = 999999.0,
        decimals: int = 2
    ) -> QDoubleValidator:
        """
        실수 입력 검증기 생성
        
        Args:
            bottom: 최소값
            top: 최대값
            decimals: 소수점 자릿수
            
        Returns:
            QDoubleValidator: 실수 검증기
        """
        validator = QDoubleValidator()
        validator.setBottom(bottom)
        validator.setTop(top)
        validator.setDecimals(decimals)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        return validator
    
    @staticmethod
    def create_int_validator(
        bottom: int = -999999,
        top: int = 999999
    ) -> QIntValidator:
        """
        정수 입력 검증기 생성
        
        Args:
            bottom: 최소값
            top: 최대값
            
        Returns:
            QIntValidator: 정수 검증기
        """
        validator = QIntValidator()
        validator.setBottom(bottom)
        validator.setTop(top)
        return validator
