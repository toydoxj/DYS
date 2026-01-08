"""좌측 메뉴 위젯"""

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt


class LeftMargin(QtWidgets.QWidget):
    """좌측 여백 위젯 (폭 20px)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        
        self.setStyleSheet('background-color: #007e8e;')
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(20, 0))
        self.setMaximumSize(QtCore.QSize(20, 16777215))


class LeftMenu(QtWidgets.QWidget):
    """좌측 메뉴 위젯"""
    
    # 시그널 정의
    menu_clicked = QtCore.pyqtSignal(int)  # 메뉴 인덱스
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        self.setStyleSheet("background-color: #007e8e;")
        
        # 레이아웃
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 메뉴 버튼들
        self.menu_buttons = []
        menu_items = [
            ("Project Info", 0),
            ("Gravity Load", 1),
            ("Wind Load", 2),
            ("Seismic Load", 3),
            ("Load Combination", 4)
        ]
        
        for text, index in menu_items:
            btn = self.create_menu_button(text)
            btn.clicked.connect(lambda checked, idx=index: self.menu_clicked.emit(idx))
            self.menu_buttons.append(btn)
            layout.addWidget(btn)
        
        layout.addStretch()
    
    def create_menu_button(self, text: str) -> QtWidgets.QPushButton:
        """
        메뉴 버튼 생성
        
        Args:
            text: 버튼 텍스트
            
        Returns:
            QtWidgets.QPushButton: 생성된 버튼
        """
        btn = QtWidgets.QPushButton(text)
        btn.setMinimumHeight(40)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 5px 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        return btn
    
    def set_active_menu(self, index: int):
        """
        활성 메뉴 설정
        
        Args:
            index: 메뉴 인덱스
        """
        for i, btn in enumerate(self.menu_buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 0.2);
                        color: white;
                        text-align: left;
                        padding: 5px 10px;
                        border: none;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: white;
                        text-align: left;
                        padding: 5px 10px;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.1);
                    }
                """)
