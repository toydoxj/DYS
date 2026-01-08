"""페이지 모듈"""

from .info_page import InfoPage
from .gravity_load_page import GravityLoadPage
from .wind_load_page import WindLoadPage
from .earthquake_load_page import EarthquakeLoadPage
from .load_combination_page import LoadCombinationPage

__all__ = [
    'InfoPage',
    'GravityLoadPage',
    'WindLoadPage',
    'EarthquakeLoadPage',
    'LoadCombinationPage',
]
