"""파일 I/O 유틸리티"""

import csv
import codecs
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import pandas as pd

from dys.config.constants import (
    MARKER_END_GRAVITY_LOAD,
    MARKER_INFORMATION,
    MARKER_END_INFORMATION
)


class FileIO:
    """파일 입출력 처리 클래스"""
    
    @staticmethod
    def load_dyl_file(file_path: str) -> Tuple[pd.DataFrame, Dict[str, str]]:
        """
        DYL 파일 로드
        
        Args:
            file_path: 파일 경로
            
        Returns:
            Tuple[pd.DataFrame, Dict[str, str]]: (하중 데이터프레임, 프로젝트 정보)
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 하중 데이터 로드
        data = []
        data_started = True
        end_marker = MARKER_END_GRAVITY_LOAD
        
        for line in lines:
            line = line.strip()
            if line == end_marker:
                break
            if data_started:
                row = list(csv.reader([line]))[0]
                data.append(row)
        
        if not data:
            df_load = pd.DataFrame()
        else:
            df_load = pd.DataFrame(data[1:], columns=data[0])
            if 'ID' in df_load.columns:
                df_load = df_load.set_index('ID')
                df_load.reset_index(inplace=True)
        
        # 프로젝트 정보 로드
        project_info = {}
        start_marker = MARKER_INFORMATION
        end_marker = MARKER_END_INFORMATION
        in_info_section = False
        
        for line in lines:
            line = line.strip()
            if line == start_marker:
                in_info_section = True
                continue
            if line == end_marker:
                break
            if in_info_section and ':' in line:
                key, value = line.split(':', 1)
                project_info[key] = value
        
        return df_load, project_info
    
    @staticmethod
    def save_dyl_file(
        file_path: str,
        df_load: pd.DataFrame,
        project_info: Dict[str, str]
    ) -> bool:
        """
        DYL 파일 저장
        
        Args:
            file_path: 저장할 파일 경로
            df_load: 하중 데이터프레임
            project_info: 프로젝트 정보 딕셔너리
            
        Returns:
            bool: 성공 여부
        """
        try:
            # CSV로 먼저 저장
            df_load.to_csv(file_path, index=False, encoding='utf-8')
            
            # 추가 정보 추가
            with codecs.open(file_path, 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([MARKER_END_GRAVITY_LOAD])
                writer.writerow([MARKER_INFORMATION])
                for key, value in project_info.items():
                    writer.writerow([f'{key}:{value}'])
                writer.writerow([MARKER_END_INFORMATION])
            
            return True
        except PermissionError:
            raise PermissionError(f"파일을 저장할 수 없습니다: {file_path}. 파일이 열려있는지 확인하세요.")
        except Exception as e:
            raise Exception(f"파일 저장 중 오류 발생: {str(e)}")
