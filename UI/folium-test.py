import typing
from PyQt6 import QtCore
import folium
import io
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
import json

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folium")
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        map_osm = folium.Map(location=[37.566345, 126.977893])
        rfile = open('form\skorea_municipalities_geo_simple.json', 'r', encoding = 'utf-8').read()
        jsonData = json.loads(rfile)
        folium.GeoJson(jsonData, name='json_data').add_to(map_osm)

        map_osm.save('d:/map1.html')
        data = io.BytesIO()
        map_osm.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()

    sys.exit(app.exec())
    



