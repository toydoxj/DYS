from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from controllers.load_controller import LoadController
import pandas as pd

class GravityLoadPage(QtWidgets.QWidget):
    """중력하중 관리 페이지"""
    
    def __init__(self, load_controller: LoadController, parent=None):
        super().__init__(parent)
        self.load_controller = load_controller
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """UI 초기 설정"""
        # 메인 레이아웃
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 상단 도구 모음
        self.setup_toolbar()
        
        # 하중 테이블
        self.setup_load_table()
        
        # 하단 입력 폼
        self.setup_input_form()
        
    def setup_toolbar(self):
        """도구 모음 설정"""
        toolbar = QtWidgets.QFrame()
        toolbar_layout = QtWidgets.QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        
        # 버튼들
        self.btn_add = self.create_toolbar_button("Add", "plus.png")
        self.btn_edit = self.create_toolbar_button("Edit", "edit.png")
        self.btn_delete = self.create_toolbar_button("Delete", "delete.png")
        self.btn_copy = self.create_toolbar_button("Copy", "copy.png")
        
        toolbar_layout.addWidget(self.btn_add)
        toolbar_layout.addWidget(self.btn_edit)
        toolbar_layout.addWidget(self.btn_delete)
        toolbar_layout.addWidget(self.btn_copy)
        toolbar_layout.addStretch()
        
        self.layout().addWidget(toolbar)
        
    def setup_load_table(self):
        """하중 테이블 설정"""
        self.table = QtWidgets.QTableWidget()
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        
        # 컬럼 설정
        columns = [
            'ID', '층', '부재명',
            'F1', 'D1', 'T1', 'L1',
            'F2', 'D2', 'T2', 'L2',
            'F3', 'D3', 'T3', 'L3',
            'SDL', '타입', '콘크리트두께',
            '콘크리트하중', 'DL', '카테고리',
            '서브카테고리', 'LR', 'LL',
            '사용하중', '계수하중'
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # 테이블 스타일
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: none;
                border-right: 1px solid #cccccc;
                border-bottom: 1px solid #cccccc;
            }
        """)
        
        self.layout().addWidget(self.table)
        
    def setup_input_form(self):
        """입력 폼 설정"""
        form_group = QtWidgets.QGroupBox("Load Input")
        form_layout = QtWidgets.QGridLayout(form_group)
        
        # 기본 정보 입력
        self.txt_floor = self.create_line_edit("층")
        self.txt_name = self.create_line_edit("부재명")
        form_layout.addWidget(QtWidgets.QLabel("Floor:"), 0, 0)
        form_layout.addWidget(self.txt_floor, 0, 1)
        form_layout.addWidget(QtWidgets.QLabel("Name:"), 0, 2)
        form_layout.addWidget(self.txt_name, 0, 3)
        
        # 마감하중 입력 (F1~F3)
        for i in range(3):
            num = i + 1
            setattr(self, f'txt_f{num}', self.create_line_edit(f'마감{num}'))
            setattr(self, f'txt_d{num}', self.create_line_edit(f'밀도{num}'))
            setattr(self, f'txt_t{num}', self.create_line_edit(f'두께{num}'))
            setattr(self, f'txt_l{num}', self.create_line_edit(f'하중{num}'))
            
            form_layout.addWidget(QtWidgets.QLabel(f"F{num}:"), i+1, 0)
            form_layout.addWidget(getattr(self, f'txt_f{num}'), i+1, 1)
            form_layout.addWidget(QtWidgets.QLabel(f"D{num}:"), i+1, 2)
            form_layout.addWidget(getattr(self, f'txt_d{num}'), i+1, 3)
            form_layout.addWidget(QtWidgets.QLabel(f"T{num}:"), i+1, 4)
            form_layout.addWidget(getattr(self, f'txt_t{num}'), i+1, 5)
            form_layout.addWidget(QtWidgets.QLabel(f"L{num}:"), i+1, 6)
            form_layout.addWidget(getattr(self, f'txt_l{num}'), i+1, 7)
        
        # 추가 정보 입력
        self.txt_sdl = self.create_line_edit("추가고정하중")
        self.cmb_type = QtWidgets.QComboBox()
        self.cmb_type.addItems(["슬래브", "보", "기둥", "벽체"])
        self.txt_concrete_thick = self.create_line_edit("콘크리트두께")
        
        form_layout.addWidget(QtWidgets.QLabel("SDL:"), 4, 0)
        form_layout.addWidget(self.txt_sdl, 4, 1)
        form_layout.addWidget(QtWidgets.QLabel("Type:"), 4, 2)
        form_layout.addWidget(self.cmb_type, 4, 3)
        form_layout.addWidget(QtWidgets.QLabel("Concrete:"), 4, 4)
        form_layout.addWidget(self.txt_concrete_thick, 4, 5)
        
        self.layout().addWidget(form_group)
        
    def create_toolbar_button(self, text: str, icon_name: str = None) -> QtWidgets.QPushButton:
        """도구 모음 버튼 생성"""
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(80, 30)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if icon_name:
            btn.setIcon(QtGui.QIcon(f'icons/{icon_name}'))
        
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #007e8e;
                color: white;
            }
        """)
        return btn
        
    def create_line_edit(self, placeholder: str) -> QtWidgets.QLineEdit:
        """라인 에디트 위젯 생성"""
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #007e8e;
            }
        """)
        return line_edit
        
    def connect_signals(self):
        """시그널 연결"""
        # 버튼 시그널
        self.btn_add.clicked.connect(self.add_load)
        self.btn_edit.clicked.connect(self.edit_load)
        self.btn_delete.clicked.connect(self.delete_load)
        self.btn_copy.clicked.connect(self.copy_load)
        
        # 테이블 선택 시그널
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
    def add_load(self):
        """하중 데이터 추가"""
        load_data = self.get_form_data()
        success, message = self.load_controller.add_load_data(load_data)
        
        if success:
            self.refresh_table()
            self.clear_form()
        else:
            QtWidgets.QMessageBox.warning(self, "경고", message)
            
    def edit_load(self):
        """하중 데이터 수정"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            load_data = self.get_form_data()
            success, message = self.load_controller.update_load_data(selected_row, load_data)
            
            if success:
                self.refresh_table()
            else:
                QtWidgets.QMessageBox.warning(self, "경고", message)
        else:
            QtWidgets.QMessageBox.warning(self, "경고", "수정할 항목을 선택하세요.")
            
    def delete_load(self):
        """하중 데이터 삭제"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            reply = QtWidgets.QMessageBox.question(
                self, '확인',
                "선택한 항목을 삭제하시겠습니까?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                success, message = self.load_controller.delete_load_data(selected_row)
                
                if success:
                    self.refresh_table()
                    self.clear_form()
                else:
                    QtWidgets.QMessageBox.warning(self, "경고", message)
        else:
            QtWidgets.QMessageBox.warning(self, "경고", "삭제할 항목을 선택하세요.")
