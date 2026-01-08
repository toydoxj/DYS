"""헤더 위젯"""

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, pyqtSignal


class Header(QtWidgets.QWidget):
    """헤더 위젯"""
    
    # 시그널 정의
    new_clicked = pyqtSignal()
    open_clicked = pyqtSignal()
    save_clicked = pyqtSignal()
    save_as_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        self.setMinimumSize(QtCore.QSize(0, 40))
        self.setMaximumSize(QtCore.QSize(16777215, 40))
        self.setStyleSheet("""
            QWidget#headerFrame {
                border-bottom: 1px solid black;
                border-right: none;
                border-top: none;
                border-left: none;
            }
            QLabel#Title_Label {
                border: none;
            }
            QPushButton {
                border-color: #cfcfcf;
                border-style: solid;
                border-width: 1px;
            }
            QPushButton:hover {
                background-color: #007e8e;
                color: white;
            }
        """)
        
        # 레이아웃
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # 제목 레이블
        self.title_label = QtWidgets.QLabel("Project Information")
        self.title_label.setObjectName("Title_Label")
        self.title_label.setFixedSize(600, 25)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(50)
        self.title_label.setFont(font)
        
        # 버튼들
        self.btn_new = self.create_button("New", 100, 25)
        self.btn_open = self.create_button("Open", 100, 25)
        self.btn_save = self.create_button("Save", 100, 25)
        self.btn_save_as = self.create_button("SaveAs", 100, 25)
        
        # 시그널 연결
        self.btn_new.clicked.connect(self.new_clicked.emit)
        self.btn_open.clicked.connect(self.open_clicked.emit)
        self.btn_save.clicked.connect(self.save_clicked.emit)
        self.btn_save_as.clicked.connect(self.save_as_clicked.emit)
        
        # 레이아웃에 추가
        layout.addWidget(self.title_label)
        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_save_as)
        layout.addSpacerItem(
            QtWidgets.QSpacerItem(
                350, 20,
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Minimum
            )
        )
    
    def create_button(self, text: str, width: int, height: int) -> QtWidgets.QPushButton:
        """
        버튼 생성
        
        Args:
            text: 버튼 텍스트
            width: 너비
            height: 높이
            
        Returns:
            QtWidgets.QPushButton: 생성된 버튼
        """
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(width, height)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn
    
    def set_title(self, title: str):
        """
        제목 설정
        
        Args:
            title: 제목 텍스트
        """
        self.title_label.setText(title)
