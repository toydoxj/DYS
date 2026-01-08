"""상수 정의"""

# 애플리케이션 정보
APP_NAME = "DYL"
APP_VERSION = "0.0.2(beta)"
APP_TITLE = f"{APP_NAME} - ver{APP_VERSION}"

# 파일 확장자
DYL_FILE_EXTENSION = ".dyl"
CSV_FILE_EXTENSION = ".csv"

# 파일 마커
MARKER_END_GRAVITY_LOAD = "##end_Gravity_Load"
MARKER_INFORMATION = "##Information"
MARKER_END_INFORMATION = "##end_information"

# UI 상수
WINDOW_WIDTH = 1700
WINDOW_HEIGHT = 650
LEFT_MENU_WIDTH = 20
HEADER_HEIGHT = 40

# 색상
COLOR_PRIMARY = "#007e8e"
COLOR_BACKGROUND = "#fefefe"
COLOR_WHITE = "#ffffff"
COLOR_GRAY = "#cfcfcf"
COLOR_DARK_GRAY = "#7d7d7d"

# 하중 테이블 컬럼
LOAD_TABLE_COLUMNS = [
    'ID', 'floor', 'name', 'f1', 'd1', 't1', 'l1',
    'f2', 'd2', 't2', 'l2', 'f3', 'd3', 't3', 'l3',
    'f4', 'd4', 't4', 'l4', 'f5', 'd5', 't5', 'l5',
    'f6', 'd6', 't6', 'l6', 'SDL', 'Type', 'conthk',
    'conLoad', 'DL', 'Category', 'subcategory', 'LR',
    'LL', 'Service', 'Strength'
]

# 프로젝트 정보 필드
PROJECT_INFO_FIELDS = [
    'code', 'project', 'address', 'occupancy', 'area',
    'sfloor', 'bfloor', 'height', 'importance'
]
