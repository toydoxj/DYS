"""CSV 로더 유틸리티"""

import pandas as pd
from pathlib import Path
from typing import Dict


def load_csv_data(file_path: str) -> Dict[str, Dict[str, float]]:
    """
    CSV 파일을 읽어서 대분류, 소분류 카테고리로 변환
    
    Args:
        file_path: CSV 파일 경로
        
    Returns:
        Dict[str, Dict[str, float]]: {대분류: {소분류: 활하중값}}
    """
    df = pd.read_csv(file_path)
    data = {}
    
    for _, row in df.iterrows():
        category = row['대분류']
        subcategory = row['소분류']
        value = row['활하중']
        
        if category not in data:
            data[category] = {}
        data[category][subcategory] = value
    
    return data
