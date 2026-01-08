"""파일 관리 서비스"""

from pathlib import Path
from typing import Tuple, Optional
from PyQt6.QtWidgets import QFileDialog, QWidget, QMessageBox

from dys.core.models.project import ProjectModel
from dys.core.models.load import LoadModel
from dys.utils.file_io import FileIO
from dys.config.constants import DYL_FILE_EXTENSION


class FileService:
    """파일 관리 서비스"""
    
    def __init__(self, project_model: ProjectModel, load_model: LoadModel):
        """
        파일 서비스 초기화
        
        Args:
            project_model: 프로젝트 모델
            load_model: 하중 모델
        """
        self.project_model = project_model
        self.load_model = load_model
        self.file_io = FileIO()
    
    def new_project(self, parent: Optional[QWidget] = None) -> Tuple[bool, str]:
        """
        새 프로젝트 생성
        
        Args:
            parent: 부모 위젯 (메시지 박스용)
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            # 수정된 내용이 있으면 확인
            if self.project_model.is_modified or not self.load_model.dataframe.empty:
                if parent:
                    reply = QMessageBox.question(
                        parent,
                        '경고',
                        '정말로 새로 만드시겠습니까? 작업된 내용은 삭제됩니다.',
                        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
                    )
                    if reply == QMessageBox.StandardButton.Cancel:
                        return False, "취소되었습니다."
            
            # 모델 초기화
            self.project_model.clear()
            self.load_model.clear()
            
            return True, "새 프로젝트가 생성되었습니다."
        except Exception as e:
            return False, f"프로젝트 생성 중 오류 발생: {str(e)}"
    
    def open_project(self, parent: Optional[QWidget] = None) -> Tuple[bool, str, Optional[str]]:
        """
        프로젝트 열기
        
        Args:
            parent: 부모 위젯
            
        Returns:
            Tuple[bool, str, Optional[str]]: (성공 여부, 메시지, 파일 경로)
        """
        try:
            # 파일 선택 대화상자
            file_path, _ = QFileDialog.getOpenFileName(
                parent,
                "파일 선택",
                "",
                f"DYL Files (*{DYL_FILE_EXTENSION});;All Files (*)"
            )
            
            if not file_path:
                return False, "파일이 선택되지 않았습니다.", None
            
            # 파일 로드
            df_load, project_info = self.file_io.load_dyl_file(file_path)
            
            # 모델에 데이터 설정
            self.load_model.set_dataframe(df_load)
            self.project_model.set_all_info(project_info)
            self.project_model.set_file_path(file_path)
            self.load_model.set_file_path(file_path)
            self.project_model.set_modified(False)
            self.load_model.set_modified(False)
            
            return True, "프로젝트를 불러왔습니다.", file_path
        except Exception as e:
            return False, f"파일 로드 중 오류 발생: {str(e)}", None
    
    def save_project(
        self,
        file_path: Optional[str] = None,
        parent: Optional[QWidget] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        프로젝트 저장
        
        Args:
            file_path: 저장할 파일 경로 (None이면 현재 파일에 저장)
            parent: 부모 위젯
            
        Returns:
            Tuple[bool, str, Optional[str]]: (성공 여부, 메시지, 저장된 파일 경로)
        """
        try:
            # 파일 경로가 없으면 Save As
            if not file_path:
                return self.save_project_as(parent)
            
            # 파일 저장
            df_load = self.load_model.dataframe
            project_info = self.project_model.get_all_info()
            
            self.file_io.save_dyl_file(file_path, df_load, project_info)
            
            # 모델 상태 업데이트
            self.project_model.set_file_path(file_path)
            self.load_model.set_file_path(file_path)
            self.project_model.set_modified(False)
            self.load_model.set_modified(False)
            
            return True, "저장하였습니다.", file_path
        except PermissionError as e:
            return False, f"파일을 저장할 수 없습니다. 파일이 열려있는지 확인하세요.", None
        except Exception as e:
            return False, f"저장 중 오류 발생: {str(e)}", None
    
    def save_project_as(self, parent: Optional[QWidget] = None) -> Tuple[bool, str, Optional[str]]:
        """
        프로젝트 다른 이름으로 저장
        
        Args:
            parent: 부모 위젯
            
        Returns:
            Tuple[bool, str, Optional[str]]: (성공 여부, 메시지, 저장된 파일 경로)
        """
        try:
            # 파일 선택 대화상자
            file_path, _ = QFileDialog.getSaveFileName(
                parent,
                "파일 선택",
                "",
                f"DYL Files (*{DYL_FILE_EXTENSION});;All Files (*)"
            )
            
            if not file_path:
                return False, "파일이 선택되지 않았습니다.", None
            
            # 확장자 확인
            if not file_path.endswith(DYL_FILE_EXTENSION):
                file_path += DYL_FILE_EXTENSION
            
            return self.save_project(file_path, parent)
        except Exception as e:
            return False, f"저장 중 오류 발생: {str(e)}", None
