# controllers/project_controller.py
from typing import Tuple, Optional, Dict, Any
from models.project_model import ProjectModel
from models.load_model import LoadModel

class ProjectController:
    """프로젝트 정보와 관련된 사용자 인터페이스와 모델 사이의 중재자"""
    
    def __init__(self, project_model: ProjectModel, load_model: LoadModel):
        """
        ProjectController 초기화
        
        Args:
            project_model: 프로젝트 정보 모델
            load_model: 하중 데이터 모델
        """
        self.project_model = project_model
        self.load_model = load_model
        
    def update_project_info(self, key: str, value: str) -> Tuple[bool, str]:
        """
        프로젝트 정보 업데이트
        
        Args:
            key: 업데이트할 정보의 키
            value: 업데이트할 값
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            if self.project_model.update_info(key, value):
                return True, f"{key} 정보가 업데이트되었습니다."
            return False, f"잘못된 키 값입니다: {key}"
        except Exception as e:
            return False, f"업데이트 중 오류 발생: {str(e)}"
    
    def get_project_info(self, key: str) -> str:
        """
        프로젝트 정보 조회
        
        Args:
            key: 조회할 정보의 키
            
        Returns:
            str: 조회된 정보 값
        """
        return self.project_model.get_info(key)
    
    def get_all_project_info(self) -> Dict[str, Any]:
        """
        모든 프로젝트 정보 조회
        
        Returns:
            Dict[str, Any]: 전체 프로젝트 정보
        """
        return self.project_model.get_all_info()
    
    def new_project(self) -> Tuple[bool, str]:
        """
        새 프로젝트 생성
        
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            self.project_model.clear_info()
            self.load_model.clear_loads()
            return True, "새 프로젝트가 생성되었습니다."
        except Exception as e:
            return False, f"프로젝트 생성 중 오류 발생: {str(e)}"
    
    def save_project(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """
        프로젝트 저장
        
        Args:
            filename: 저장할 파일 경로 (None인 경우 현재 작업 중인 파일에 저장)
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            # 프로젝트 정보 저장
            self.project_model.save_to_file(filename)
            
            # 하중 데이터 저장
            if filename:
                load_filename = filename.replace('.json', '_loads.csv')
            else:
                load_filename = None
            self.load_model.save_to_file(load_filename)
            
            return True, "프로젝트가 저장되었습니다."
        except Exception as e:
            return False, f"저장 중 오류 발생: {str(e)}"
    
    def load_project(self, filename: str) -> Tuple[bool, str]:
        """
        프로젝트 불러오기
        
        Args:
            filename: 불러올 파일 경로
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            # 프로젝트 정보 로드
            self.project_model.load_from_file(filename)
            
            # 하중 데이터 로드
            load_filename = filename.replace('.json', '_loads.csv')
            self.load_model.load_from_file(load_filename)
            
            return True, "프로젝트를 불러왔습니다."
        except Exception as e:
            return False, f"프로젝트 로드 중 오류 발생: {str(e)}"
    
    @property
    def is_modified(self) -> bool:
        """
        프로젝트 수정 여부 확인
        
        Returns:
            bool: 수정되었으면 True, 아니면 False
        """
        return self.project_model.is_modified
    
    @property
    def current_file_path(self) -> Optional[str]:
        """현재 작업 중인 파일 경로 반환"""
        return self.project_model.current_file_path