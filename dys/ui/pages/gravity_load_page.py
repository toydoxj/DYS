"""중력하중 페이지"""

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QAbstractItemView
from PyQt6.QtCore import Qt
from typing import Optional
import pandas as pd

from dys.core.models.load import LoadModel
from dys.core.models.project import ProjectModel
from dys.utils.validators import Validators
from dys.utils.csv_loader import load_csv_data
from dys.config.constants import LOAD_TABLE_COLUMNS
from dys.config.settings import settings


class GravityLoadPage(QtWidgets.QWidget):
    """중력하중 페이지"""
    
    def __init__(
        self,
        load_model: LoadModel,
        project_model: Optional[ProjectModel] = None,
        parent=None
    ):
        """
        중력하중 페이지 초기화
        
        Args:
            load_model: 하중 모델
            project_model: 프로젝트 모델 (선택적)
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.load_model = load_model
        self.project_model = project_model
        
        # 검증기
        self.validator = Validators.create_double_validator()
        
        # 활하중 데이터 로드
        try:
            csv_path = settings.get_docs_path("HShape.csv")
            if csv_path.exists():
                self.KDS_liveloaddata = load_csv_data(str(csv_path))
            else:
                self.KDS_liveloaddata = {}
        except Exception:
            self.KDS_liveloaddata = {}
        
        self.setup_ui()
        self.connect_signals()
        self.load_from_model()
    
    def setup_ui(self):
        """UI 설정"""
        # 스타일시트
        self.setStyleSheet("""
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
        
        # 메인 레이아웃
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 하중 테이블
        self.tbl_load = QtWidgets.QTableWidget(self)
        self.tbl_load.setRowCount(1)
        self.tbl_load.setColumnCount(9)
        self.tbl_load.setFixedSize(800, 365)
        
        # 테이블 헤더
        headers = ['ID', '층수', '실명', '용도', '슬래브두께', '고정하중', '활하중', 'D+L', '1.2D+1.6L']
        self.tbl_load.setHorizontalHeaderLabels(headers)
        self.tbl_load.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # 컬럼 너비 설정
        self.tbl_load.setColumnWidth(0, 0)  # ID 숨김
        self.tbl_load.setColumnWidth(1, 80)
        self.tbl_load.setColumnWidth(2, 120)
        self.tbl_load.setColumnWidth(3, 180)
        self.tbl_load.setColumnWidth(4, 80)
        self.tbl_load.setColumnWidth(5, 80)
        self.tbl_load.setColumnWidth(6, 80)
        self.tbl_load.setColumnWidth(7, 80)
        self.tbl_load.setColumnWidth(8, 80)
        
        self.tbl_load.verticalHeader().setVisible(False)
        self.tbl_load.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.tbl_load)
        
        # 버튼 영역
        button_layout = QtWidgets.QHBoxLayout()
        
        self.btn_add = QtWidgets.QPushButton("추가")
        self.btn_add.setFixedSize(100, 30)
        
        self.btn_delete = QtWidgets.QPushButton("삭제")
        self.btn_delete.setFixedSize(100, 30)
        
        self.btn_up = QtWidgets.QPushButton("↑")
        self.btn_up.setFixedSize(50, 30)
        
        self.btn_down = QtWidgets.QPushButton("↓")
        self.btn_down.setFixedSize(50, 30)
        
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_up)
        button_layout.addWidget(self.btn_down)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # 입력 폼 영역 (간소화된 버전)
        # 실제 구현 시 기존 Page_GL의 복잡한 입력 폼을 추가할 수 있음
        form_label = QtWidgets.QLabel("하중 입력 폼 (상세 구현 예정)")
        form_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(form_label)
    
    def connect_signals(self):
        """시그널 연결"""
        self.tbl_load.cellClicked.connect(self.handle_cell_click)
        self.btn_add.clicked.connect(self.on_add_clicked)
        self.btn_delete.clicked.connect(self.on_delete_clicked)
        self.btn_up.clicked.connect(self.on_move_up)
        self.btn_down.clicked.connect(self.on_move_down)
    
    def handle_cell_click(self, row: int, column: int):
        """
        셀 클릭 핸들러
        
        Args:
            row: 행 인덱스
            column: 열 인덱스
        """
        # 선택된 행의 데이터를 입력 폼에 표시
        if row < len(self.load_model.dataframe):
            load_data = self.load_model.get_load(row)
            # 입력 폼 업데이트 로직 (추후 구현)
    
    def on_add_clicked(self):
        """추가 버튼 클릭"""
        # 기본 하중 데이터 생성
        new_load = {
            'ID': len(self.load_model.dataframe),
            'floor': '',
            'name': '',
            'DL': 0.0,
            'LL': 0.0,
        }
        
        # 나머지 필드는 기본값으로 채움
        for col in LOAD_TABLE_COLUMNS:
            if col not in new_load:
                new_load[col] = ''
        
        self.load_model.add_load(new_load)
        self.update_table()
    
    def on_delete_clicked(self):
        """삭제 버튼 클릭"""
        current_row = self.tbl_load.currentRow()
        if current_row >= 0:
            reply = QtWidgets.QMessageBox.question(
                self,
                '확인',
                '정말로 삭제하시겠습니까?',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.load_model.remove_load(current_row)
                self.update_table()
    
    def on_move_up(self):
        """위로 이동"""
        current_row = self.tbl_load.currentRow()
        if current_row > 0:
            df = self.load_model.dataframe
            # 행 교환
            df.iloc[current_row], df.iloc[current_row - 1] = \
                df.iloc[current_row - 1].copy(), df.iloc[current_row].copy()
            self.load_model.set_dataframe(df)
            self.update_table()
            self.tbl_load.selectRow(current_row - 1)
    
    def on_move_down(self):
        """아래로 이동"""
        current_row = self.tbl_load.currentRow()
        df = self.load_model.dataframe
        if current_row < len(df) - 1:
            # 행 교환
            df.iloc[current_row], df.iloc[current_row + 1] = \
                df.iloc[current_row + 1].copy(), df.iloc[current_row].copy()
            self.load_model.set_dataframe(df)
            self.update_table()
            self.tbl_load.selectRow(current_row + 1)
    
    def update_table(self):
        """테이블 업데이트"""
        df = self.load_model.dataframe
        
        if df.empty:
            self.tbl_load.setRowCount(0)
            return
        
        self.tbl_load.setRowCount(len(df))
        
        # 표시할 컬럼 매핑
        display_columns = ['ID', 'floor', 'name', 'Category', 'conthk', 'DL', 'LL', 'Service', 'Strength']
        
        for row in range(len(df)):
            for col_idx, col_name in enumerate(display_columns):
                if col_name in df.columns:
                    value = str(df.iloc[row][col_name]) if pd.notna(df.iloc[row][col_name]) else ''
                    item = QtWidgets.QTableWidgetItem(value)
                    self.tbl_load.setItem(row, col_idx, item)
    
    def load_from_model(self):
        """모델에서 데이터 로드"""
        self.update_table()
    
    def refresh(self):
        """페이지 새로고침"""
        self.load_from_model()
