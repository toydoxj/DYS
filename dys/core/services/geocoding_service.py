"""지오코딩 서비스 (Google Maps API)"""

import os
from typing import Tuple, Optional
from PyQt6.QtWidgets import QMessageBox

try:
    import googlemaps
    GOOGLEMAPS_AVAILABLE = True
except ImportError:
    GOOGLEMAPS_AVAILABLE = False


class GeocodingService:
    """지오코딩 서비스 클래스
    
    Google Maps Geocoding API를 사용하여 주소를 좌표로 변환합니다.
    API 키는 환경 변수나 설정 파일에서 로드합니다.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        지오코딩 서비스 초기화
        
        Args:
            api_key: Google Maps API 키 (None이면 환경 변수에서 로드)
        """
        self.api_key = api_key or self._load_api_key()
        self.client = None
        
        if GOOGLEMAPS_AVAILABLE and self.api_key:
            try:
                self.client = googlemaps.Client(key=self.api_key)
            except Exception as e:
                print(f"Google Maps API 클라이언트 초기화 실패: {e}")
                self.client = None
    
    def _load_api_key(self) -> Optional[str]:
        """
        API 키 로드
        
        우선순위:
        1. 환경 변수 GOOGLE_MAPS_API_KEY
        2. .env 파일
        3. config/api_key.txt (로컬 개발용, .gitignore에 포함)
        
        Returns:
            Optional[str]: API 키 또는 None
        """
        # 환경 변수에서 로드
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if api_key:
            return api_key
        
        # .env 파일에서 로드
        try:
            from pathlib import Path
            env_file = Path(__file__).parent.parent.parent.parent / '.env'
            if env_file.exists():
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('GOOGLE_MAPS_API_KEY='):
                            return line.split('=', 1)[1].strip()
        except Exception:
            pass
        
        # 로컬 설정 파일에서 로드 (개발용)
        try:
            from pathlib import Path
            api_key_file = Path(__file__).parent.parent.parent.parent / 'config' / 'api_key.txt'
            if api_key_file.exists():
                with open(api_key_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except Exception:
            pass
        
        return None
    
    def is_available(self) -> bool:
        """
        서비스 사용 가능 여부 확인
        
        Returns:
            bool: 사용 가능하면 True
        """
        return GOOGLEMAPS_AVAILABLE and self.client is not None
    
    def geocode(self, address: str) -> Tuple[Optional[float], Optional[float]]:
        """
        주소를 좌표로 변환 (지오코딩)
        
        Args:
            address: 주소 문자열
            
        Returns:
            Tuple[Optional[float], Optional[float]]: (위도, 경도) 또는 (None, None)
        """
        if not self.is_available():
            return None, None
        
        if not address or not address.strip():
            return None, None
        
        try:
            geocode_result = self.client.geocode(address)
            
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                lat = location['lat']
                lng = location['lng']
                return lat, lng
            else:
                return None, None
                
        except Exception as e:
            # API 키 오류, 할당량 초과 등
            error_msg = self._parse_error_message(e)
            print(f"Google Maps API 오류: {error_msg}")
            return None, None
            
        except Exception as e:
            print(f"지오코딩 오류: {str(e)}")
            return None, None
    
    def _parse_error_message(self, error: Exception) -> str:
        """
        에러 메시지 파싱
        
        Args:
            error: 예외 객체
            
        Returns:
            str: 사용자 친화적인 에러 메시지
        """
        error_str = str(error)
        
        if 'API key' in error_str or 'INVALID_REQUEST' in error_str:
            return "API 키가 유효하지 않습니다. 설정을 확인해주세요."
        elif 'OVER_QUERY_LIMIT' in error_str:
            return "API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
        elif 'REQUEST_DENIED' in error_str:
            return "API 요청이 거부되었습니다. API 키 권한을 확인해주세요."
        elif 'ZERO_RESULTS' in error_str:
            return "검색 결과가 없습니다."
        else:
            return f"API 오류: {error_str}"
    
    def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        """
        좌표를 주소로 변환 (역지오코딩)
        
        Args:
            lat: 위도
            lng: 경도
            
        Returns:
            Optional[str]: 주소 문자열 또는 None
        """
        if not self.is_available():
            return None
        
        try:
            reverse_result = self.client.reverse_geocode((lat, lng))
            
            if reverse_result:
                return reverse_result[0]['formatted_address']
            else:
                return None
                
        except Exception as e:
            print(f"역지오코딩 오류: {str(e)}")
            return None
