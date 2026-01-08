"""풍하중 페이지"""

from PyQt6 import QtWidgets, QtCore
from typing import Optional
import io
import json
import folium

# WebEngine을 선택적으로 import
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    # WebEngine이 없을 때를 위한 대체 클래스
    class QWebEngineView(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            label = QtWidgets.QLabel("WebEngine을 사용할 수 없습니다.\nPyQt6-WebEngine 패키지를 설치해주세요.", self)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(label)
        
        def setHtml(self, html: str):
            pass

from dys.core.models.project import ProjectModel
from dys.core.services.geocoding_service import GeocodingService
from dys.utils.validators import Validators
from dys.config.settings import settings
from PyQt6.QtWidgets import QMessageBox


class WindLoadPage(QtWidgets.QWidget):
    """풍하중 페이지"""
    
    def __init__(
        self,
        project_model: ProjectModel,
        parent=None
    ):
        """
        풍하중 페이지 초기화
        
        Args:
            project_model: 프로젝트 모델
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.project_model = project_model
        self.validator = Validators.create_double_validator()
        
        # 지오코딩 서비스 초기화
        self.geocoding_service = GeocodingService()
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """UI 설정"""
        # 메인 레이아웃
        layout_main = QtWidgets.QHBoxLayout(self)
        layout_main.setContentsMargins(10, 10, 10, 10)
        
        # 입력 영역
        input_widget = QtWidgets.QWidget()
        input_layout = QtWidgets.QVBoxLayout(input_widget)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        # 스타일시트
        style_sheet1 = "QLineEdit {background-color: #7d7d7d; color: #ffffff; border: none;}"
        style_sheet2 = "QLineEdit {background-color: #cfcfcf; border: 1px solid #777777;}"
        
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
            QLineEdit {
                background-color: #efefef;
                border: 1px solid #777777;
            }
        """)
        
        # MiDAS 직접 입력 여부
        midas_layout = QtWidgets.QHBoxLayout()
        label_midas = QtWidgets.QLabel("MiDAS 직접 입력")
        self.btn_yes_midas = QtWidgets.QRadioButton("네")
        self.btn_yes_midas.setChecked(True)
        self.btn_no_midas = QtWidgets.QRadioButton("아니오")
        
        midas_layout.addWidget(label_midas)
        midas_layout.addWidget(self.btn_yes_midas)
        midas_layout.addWidget(self.btn_no_midas)
        input_layout.addLayout(midas_layout)
        
        # 지표면 조도 구분
        categories_layout = QtWidgets.QHBoxLayout()
        label_categories = QtWidgets.QLabel("지표면 조도구분")
        self.combobox_categories = QtWidgets.QComboBox()
        self.combobox_categories.addItems(['A', 'B', 'C', 'D'])
        self.combobox_categories.setCurrentIndex(2)
        
        categories_layout.addWidget(label_categories)
        categories_layout.addWidget(self.combobox_categories)
        input_layout.addLayout(categories_layout)
        
        # 건물 길이 입력
        len_layout = QtWidgets.QHBoxLayout()
        label_len = QtWidgets.QLabel('건물길이')
        label_lx = QtWidgets.QLabel('Lx')
        self.txt_lx = QtWidgets.QLineEdit()
        self.txt_lx.setStyleSheet(style_sheet2)
        label_ly = QtWidgets.QLabel('Ly')
        self.txt_ly = QtWidgets.QLineEdit()
        self.txt_ly.setStyleSheet(style_sheet2)
        label_af = QtWidgets.QLabel('Af')
        self.txt_af = QtWidgets.QLineEdit()
        self.txt_af.setToolTip('기준층 면적 입력, 빈칸으로 할 경우 직사각형으로 자동 계산됨.')
        self.txt_af.setStyleSheet(style_sheet2)
        
        len_layout.addWidget(label_len)
        len_layout.addWidget(label_lx)
        len_layout.addWidget(self.txt_lx)
        len_layout.addWidget(label_ly)
        len_layout.addWidget(self.txt_ly)
        len_layout.addWidget(label_af)
        len_layout.addWidget(self.txt_af)
        input_layout.addLayout(len_layout)
        
        # 주소 입력
        address_layout = QtWidgets.QHBoxLayout()
        label_address = QtWidgets.QLabel('주소')
        self.txt_address = QtWidgets.QLineEdit()
        self.txt_address.setReadOnly(True)
        self.txt_address.setStyleSheet(style_sheet2)
        self.btn_address = QtWidgets.QPushButton('지도 표시')
        self.btn_address.setStyleSheet(style_sheet1)
        
        address_layout.addWidget(label_address)
        address_layout.addWidget(self.txt_address)
        address_layout.addWidget(self.btn_address)
        input_layout.addLayout(address_layout)
        
        input_layout.addStretch()
        
        # 지도 영역
        map_layout = QtWidgets.QVBoxLayout()
        
        # 지도 창
        self.map_view = QWebEngineView()
        self.map_view.setContentsMargins(10, 10, 10, 10)
        self.map_view.setFixedHeight(680)
        
        # 기본 지도 생성
        self.m = folium.Map(
            location=[36.111470, 128.397285],
            zoom_start=7,
            tiles='cartodbpositron'
        )
        
        # 한국 지도 GeoJSON 추가
        try:
            geo_json_path = settings.get_data_path("skorea_municipalities_geo_simple.json")
            if geo_json_path.exists():
                with open(geo_json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                folium.GeoJson(
                    json_data,
                    name='json_data',
                    style_function=self.default_style_function
                ).add_to(self.m)
        except Exception as e:
            print(f"지도 데이터 로드 오류: {e}")
        
        # 지도를 HTML로 변환하여 표시
        if WEBENGINE_AVAILABLE:
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.map_view.setHtml(data.getvalue().decode())
        else:
            # WebEngine이 없으면 지도 생성만 하고 표시는 안 함
            pass
        
        map_layout.addWidget(self.map_view)
        
        # 레이아웃에 추가
        layout_main.addWidget(input_widget, 1)
        layout_main.addLayout(map_layout, 2)
    
    def default_style_function(self, feature):
        """기본 스타일 함수"""
        return {
            'fillColor': '#ffff00',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.5,
        }
    
    def connect_signals(self):
        """시그널 연결"""
        self.btn_address.clicked.connect(self.on_show_map)
        # 프로젝트 모델의 주소 변경 시그널 연결
        if self.project_model:
            # 주소 업데이트 시그널은 InfoPage에서 발생하므로
            # 메인 윈도우를 통해 연결해야 함
            pass
    
    def on_show_map(self):
        """지도 표시 버튼 클릭"""
        address = self.txt_address.text()
        if not address or not address.strip():
            QMessageBox.warning(self, '경고', '주소를 입력해주세요.')
            return
        
        if not self.geocoding_service.is_available():
            QMessageBox.warning(
                self,
                'API 키 없음',
                'Google Maps API 키가 설정되지 않았습니다.\n\n'
                '설정 방법:\n'
                '1. 환경 변수 GOOGLE_MAPS_API_KEY 설정\n'
                '2. .env 파일에 GOOGLE_MAPS_API_KEY=your_key 추가\n'
                '3. config/api_key.txt 파일에 API 키 저장 (개발용)\n\n'
                'API 키는 Google Cloud Console에서 발급받을 수 있습니다.'
            )
            return
        
        # 지오코딩 수행
        lat, lng = self.geocoding_service.geocode(address)
        
        if lat is not None and lng is not None:
            # 좌표를 입력 필드에 설정 (필요한 경우)
            # self.txt_lat.setText(str(lat))
            # self.txt_lng.setText(str(lng))
            
            # 지도 중심 이동 및 마커 추가
            self.update_map_with_location(lat, lng, address)
            
            QMessageBox.information(self, '성공', f'주소를 찾았습니다.\n위도: {lat:.6f}, 경도: {lng:.6f}')
        else:
            QMessageBox.warning(self, '오류', '주소를 찾을 수 없습니다. 주소를 확인해주세요.')
    
    def set_address(self, address: str):
        """
        주소 설정
        
        Args:
            address: 주소 문자열
        """
        self.txt_address.setText(address)
    
    def update_map_with_location(self, lat: float, lng: float, address: str):
        """
        지도를 특정 위치로 업데이트
        
        Args:
            lat: 위도
            lng: 경도
            address: 주소
        """
        # 기존 마커 제거 (새로운 지도 생성)
        self.m = folium.Map(
            location=[lat, lng],
            zoom_start=15,
            tiles='cartodbpositron'
        )
        
        # 한국 지도 GeoJSON 추가
        try:
            geo_json_path = settings.get_data_path("skorea_municipalities_geo_simple.json")
            if geo_json_path.exists():
                with open(geo_json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                folium.GeoJson(
                    json_data,
                    name='json_data',
                    style_function=self.default_style_function
                ).add_to(self.m)
        except Exception as e:
            print(f"지도 데이터 로드 오류: {e}")
        
        # 마커 추가
        folium.Marker(
            [lat, lng],
            popup=address,
            tooltip=address
        ).add_to(self.m)
        
        # 지도 업데이트
        if WEBENGINE_AVAILABLE:
            data = io.BytesIO()
            self.m.save(data, close_file=False)
            self.map_view.setHtml(data.getvalue().decode())
        else:
            # WebEngine이 없으면 지도 생성만 하고 표시는 안 함
            pass
    
    def refresh(self):
        """페이지 새로고침"""
        # 프로젝트 정보에서 주소 가져오기
        if self.project_model:
            address = self.project_model.get_info('address')
            self.set_address(address)
            
            # 주소가 있으면 자동으로 지오코딩 시도 (선택적)
            # if address and self.geocoding_service.is_available():
            #     lat, lng = self.geocoding_service.geocode(address)
            #     if lat and lng:
            #         self.update_map_with_location(lat, lng, address)
