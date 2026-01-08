from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from controllers.project_controller import ProjectController
import sys

class WindLoadPage(QtWidgets.QWidget):
    """풍하중 계산 페이지"""
    
    def __init__(self, project_controller: ProjectController, parent=None):
        super().__init__(parent)
        self.project_controller = project_controller
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """UI 초기 설정"""
        # 메인 레이아웃
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 스크롤 영역 설정
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
        """)
        
        # 스크롤 내부 위젯
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        
        # 기본 정보 그룹
        self.setup_basic_info_group(scroll_layout)
        
        # 지형 계수 그룹
        self.setup_terrain_group(scroll_layout)
        
        # 건물 치수 그룹
        self.setup_building_dimension_group(scroll_layout)
        
        # 계산 결과 그룹
        self.setup_result_group(scroll_layout)
        
        # 여백 추가
        scroll_layout.addStretch()
        
        # 스크롤 영역에 위젯 설정
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
    def setup_basic_info_group(self, parent_layout):
        """기본 정보 그룹 설정"""
        group = QtWidgets.QGroupBox("Basic Information")
        layout = QtWidgets.QFormLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 기본풍속
        self.txt_basic_wind_speed = self.create_line_edit("기본풍속을 입력하세요")
        layout.addRow("Basic Wind Speed (m/s):", self.txt_basic_wind_speed)
        
        # 중요도 계수
        self.txt_importance_factor = self.create_line_edit("중요도 계수를 입력하세요")
        layout.addRow("Importance Factor:", self.txt_importance_factor)
        
        parent_layout.addWidget(group)
        
    def setup_terrain_group(self, parent_layout):
        """지형 계수 그룹 설정"""
        group = QtWidgets.QGroupBox("Terrain Information")
        layout = QtWidgets.QFormLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 지표면 조도구분
        self.cmb_terrain_category = QtWidgets.QComboBox()
        self.cmb_terrain_category.addItems(["A", "B", "C", "D"])
        layout.addRow("Terrain Category:", self.cmb_terrain_category)
        
        # 지형계수
        self.txt_topography_factor = self.create_line_edit("지형계수를 입력하세요")
        layout.addRow("Topography Factor:", self.txt_topography_factor)
        
        parent_layout.addWidget(group)
        
    def setup_building_dimension_group(self, parent_layout):
        """건물 치수 그룹 설정"""
        group = QtWidgets.QGroupBox("Building Dimensions")
        layout = QtWidgets.QFormLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 건물 높이
        self.txt_height = self.create_line_edit("건물 높이를 입력하세요")
        layout.addRow("Height (m):", self.txt_height)
        
        # 건물 폭
        self.txt_width = self.create_line_edit("건물 폭을 입력하세요")
        layout.addRow("Width (m):", self.txt_width)
        
        # 건물 길이
        self.txt_length = self.create_line_edit("건물 길이를 입력하세요")
        layout.addRow("Length (m):", self.txt_length)
        
        parent_layout.addWidget(group)
        
    def setup_result_group(self, parent_layout):
        """계산 결과 그룹 설정"""
        group = QtWidgets.QGroupBox("Calculation Results")
        layout = QtWidgets.QVBoxLayout(group)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 계산 버튼
        self.btn_calculate = QtWidgets.QPushButton("Calculate Wind Load")
        self.btn_calculate.setFixedSize(200, 40)
        self.btn_calculate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_calculate.setStyleSheet("""
            QPushButton {
                background-color: #007e8e;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #006d7a;
            }
        """)
        layout.addWidget(self.btn_calculate, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 결과 테이블
        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels([
            "Height (m)", "Velocity Pressure (kN/m²)",
            "GCp", "Design Pressure (kN/m²)"
        ])
        
        self.result_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: none;
                border-right: 1px solid #cccccc;
                border-bottom: 1px solid #cccccc;
            }
        """)
        
        layout.addWidget(self.result_table)
        
        parent_layout.addWidget(group)
        
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
        # 계산 버튼 시그널
        self.btn_calculate.clicked.connect(self.calculate_wind_load)
        
        # 입력값 변경 시그널
        self.txt_basic_wind_speed.textChanged.connect(self.on_input_changed)
        self.txt_importance_factor.textChanged.connect(self.on_input_changed)
        self.cmb_terrain_category.currentTextChanged.connect(self.on_input_changed)
        self.txt_topography_factor.textChanged.connect(self.on_input_changed)
        self.txt_height.textChanged.connect(self.on_input_changed)
        self.txt_width.textChanged.connect(self.on_input_changed)
        self.txt_length.textChanged.connect(self.on_input_changed)
        
    def calculate_wind_load(self):
        """풍하중 계산"""
        try:
            # 입력값 검증
            if not self.validate_inputs():
                return
                
            # 여기에 풍하중 계산 로직 구현
            self.update_result_table()
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "경고", f"계산 중 오류가 발생했습니다: {str(e)}")
            
    def validate_inputs(self) -> bool:
        """입력값 검증"""
        # 필수 입력값 확인
        required_fields = {
            'Basic Wind Speed': self.txt_basic_wind_speed,
            'Importance Factor': self.txt_importance_factor,
            'Topography Factor': self.txt_topography_factor,
            'Height': self.txt_height,
            'Width': self.txt_width,
            'Length': self.txt_length
        }
        
        for field_name, widget in required_fields.items():
            if not widget.text().strip():
                QtWidgets.QMessageBox.warning(
                    self, "경고", f"{field_name}을(를) 입력하세요."
                )
                widget.setFocus()
                return False
                
        return True
        
    def update_result_table(self):
        """결과 테이블 업데이트"""
        # 여기에 결과 테이블 업데이트 로직 구현
        pass
        
    def on_input_changed(self):
        """입력값 변경 시 처리"""
        # 입력값이 변경될 때마다 필요한 처리를 여기에 구현
        pass
