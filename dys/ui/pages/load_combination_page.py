"""하중조합 페이지"""

from PyQt6 import QtWidgets, QtCore
from typing import Optional

from dys.core.models.project import ProjectModel


class LoadCombinationPage(QtWidgets.QWidget):
    """하중조합 페이지"""
    
    def __init__(
        self,
        project_model: ProjectModel,
        parent=None
    ):
        """
        하중조합 페이지 초기화
        
        Args:
            project_model: 프로젝트 모델
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.project_model = project_model
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        layout = QtWidgets.QVBoxLayout(self)
        
        label = QtWidgets.QLabel("준비중", self)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setPointSize(20)
        label.setFont(font)
        
        layout.addWidget(label)
        layout.addStretch()
