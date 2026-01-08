import pandas as pd

class WindLoad:

    '''
    KDS 41 12 00 풍하중 산정    
    Structural Type     1.1 : 밀폐형 건축구조물 -    한 벽면 틈새, 그 외 표면 밀폐
                        1.2 :                       마주보는 두 벽면 틈새, 그 외 표면 밀폐
                        1.3 :                       이웃하는 두 벽면 틈새, 그 외 표면 밀폐
                        1.4 :                       이웃하는 세 벽면 틈새, 그 외 표면 밀폐
                        1.5 :                       모든 표면(벽면 침 지붕) 틈새
                        1.6 :                       모든 벽면 틈새, 지붕 밀폐
                        1.7 :                       모든 표면(벽면 및 지붕) 밀폐                                            
                        2.1 : 부분밀폐형 건축물 -   탁월한 개구부 1 (표면 개구부 면적의 2배)
                        2.2 : 부분밀폐형 건축물 -   탁월한 개구부 2 (표면 개구분 면적의 3배)
                        2.3 : 윗면이 개방된 사일로, 굴뚝
                        3.0 : 개방형 건축구조물
    Lateral System      0 : 구조해석 값 이용
                        1 : 강구조 모멘트 저항골조
                        2 : 콘크리트 모멘트 저항골조
                        3 : 기타 수평하중저항 시스템을 가진 강구조 및 콘크리트 건축물
    '''

    def __init__(self, Lx : float, Ly : float, H : float, Vo : int = 28, KD : int = 1.0, KZT : float = 1.0 , WindCategory : str = 'C', Importance : str = '2', StructuralType : float = 1.6, LateralSystem : int = 3, nDx : float = 1, nDy : float = 1 ):

        StructuralTypeData = [
            [1.1, 0.7, -0.4],
            [1.2, 0.2, -0.4],
            [1.3, 0.2, -0.3],
            [1.4, 0, -0.6],
            [1.5, 0, -0.6],
            [1.6, 0, -0.4],
            [1.7, 0, -0.2],
            [2.1, 0.55, -0.55],
            [2.2, 0.7, -0.7],
            [2.3, -0.6, -0.6],
            [3.0, 0, 0]
        ]

        columns = ['구조물형식','Cpi1', 'Cpi2']
        self.df_structuraltype = pd.DataFrame(StructuralTypeData, columns=columns)

        
        self.__Lx = Lx
        self.__Ly = Ly
        self.__Vo = Vo
        self.__H = H
        self.__KD = KD
        self.__KZT = KZT
        self.__KZR, self.__alpha, self.__Zb = self.__WindCategory(WindCategory)
        self.__StructuralType = StructuralType
        self.__Cpi1, self.__Cpi2 = self.__Cpi_Wall()

        if Importance == '특': self.__Iw = 1.0
        if Importance == '1': self.__Iw = 1.0
        if Importance == '2': self.__Iw = 0.95
        if Importance == '3': self.__Iw = 0.9

        self.__VH = self.__DesignWindSpeed()
        self.__qH = self.__DesignWindPressure()
        self.__nDx, self.__nDy = self.__naturalFrequency(LateralSystem, nDx, nDy)

        self.__X_Cpe1, self.__X_Cpe2, self.__X_Cpe_side = self.__Cpe_Wall(B = Ly, D = Lx)
        self.__Y_Cpe1, self.__Y_Cpe2, self.__Y_Cpe_side = self.__Cpe_Wall(B = Lx, D = Ly)

    @property
    def kzr(self):
        return self.__KZR
    
    @property
    def Vh(self):
        return self.__VH
    
    @property
    def qH(self):
        return self.__qH
    
    @property
    def nDx(self):
        return self.__nDx
    
    @property
    def X_Cpe(self):
        return self.__X_Cpe1, self.__X_Cpe2, self.__X_Cpe_side

    @property
    def Y_Cpe(self):
        return self.__Y_Cpe1, self.__Y_Cpe2, self.__Y_Cpe_side
    
    @property
    def Cpi(self):
        return self.__Cpi1, self.__Cpi2

    def __DesignWindSpeed(self):
        return round(self.__Vo * self.__KD * self.__KZR * self.__KZT * self.__Iw,1)
    
    def __DesignWindPressure(self):
        return round(1 / 2 * 1.225 * self.__VH ** 2,1)
    
    def __WindCategory(self, WindCategory, z : float = 0):
        if z == 0: z = self.__H
        if WindCategory == 'A':
            Zb = 20
            alpha = 0.33
            if  z <= Zb: 
                return 0.58, alpha, Zb
            else:
                return 0.22 * z ** alpha, alpha, Zb
        elif WindCategory == 'B':
            Zb = 15
            alpha = 0.22
            if  z <= Zb: 
                return 0.81, alpha, Zb
            else:
                return 0.45 * z ** alpha, alpha, Zb
        elif WindCategory == 'C':
            Zb = 10
            alpha = 0.15
            if  z <= Zb: 
                return 1, alpha, Zb
            else:
                return 0.71 * z ** alpha, alpha, Zb
        elif WindCategory == 'D':
            Zb = 5
            alpha = 0.1
            if  z <= Zb: 
                return 1.13, alpha, Zb
            else:
                return 0.98 * z ** alpha, alpha, Zb
        else: return 1
    
    def __naturalFrequency(self, LateralSystem, nDx, nDy):
        if LateralSystem == 0:
            return nDx, nDy
        elif LateralSystem == 1:
            return 22.2 / (self.__H ** 0.8), 22.2 / (self.__H ** 0.8)            
        elif LateralSystem == 2:
            return 43.5 / (self.__H ** 0.9), 43.5 / (self.__H ** 0.9)
        elif LateralSystem == 3:
            return 75 / self.__H, 75 / self.__H 

    def __Cpe_Wall(self, D, B): # X방향 D=Ly, B=Lx
        if self.__H <= self.__Zb : kz = 1.0
        else : kz = 0.8 ** (2 * self.__alpha)
        
        DtoB = D / B
        if DtoB <=1:
            Cpe1 = 0.8
            Cpe2 = -0.5
        else:
            Cpe1 = 0.8 + 0.05 * kz
            Cpe2 = -0.35
        Cpe_side = -0.7

        return Cpe1, Cpe2, Cpe_side
    
    def __Cpi_Wall(self):
        filtered_row = self.df_structuraltype[self.df_structuraltype['구조물형식']== self.__StructuralType]
        return filtered_row['Cpi1'].values[0], filtered_row['Cpi2'].values[0]
    
    def X_WallWindLoad(self):
        '''
        출력 순서
        풍상벽1, 풍상벽2, 풍하벽1, 풍하벽2, 측벽
        '''
        X1_front_wall = self.__qH * (self.__X_Cpe1 - self.__Cpi1)
        X1_back_wall = self.__qH * (self.__X_Cpe2 - self.__Cpi1)
        X1_side_wall = self.__qH * (self.__X_Cpe_side - self.__Cpi1)
        X2_front_wall = self.__qH * (self.__X_Cpe1 - self.__Cpi2)
        X2_back_wall = self.__qH * (self.__X_Cpe2 - self.__Cpi2)
        X2_side_wall = self.__qH * (self.__X_Cpe_side - self.__Cpi2)

        return X1_front_wall, X1_back_wall, X1_side_wall, X2_front_wall, X2_back_wall, X2_side_wall
    
    def Y_WallWindLoad(self):
        '''
        출력 순서
        풍상벽1, 풍상벽2, 풍하벽1, 풍하벽2, 측벽
        '''
        Y1_front_wall = self.__qH * (self.__Y_Cpe1 - self.__Cpi1)
        Y1_back_wall = self.__qH * (self.__Y_Cpe2 - self.__Cpi1)
        Y1_side_wall = self.__qH * (self.__Y_Cpe_side - self.__Cpi1)
        Y2_front_wall = self.__qH * (self.__Y_Cpe1 - self.__Cpi2)
        Y2_back_wall = self.__qH * (self.__Y_Cpe2 - self.__Cpi2)
        Y2_side_wall = self.__qH * (self.__Y_Cpe_side - self.__Cpi2)

        return Y1_front_wall, Y1_back_wall, Y1_side_wall, Y2_front_wall, Y2_back_wall, Y2_side_wall


            



WLoad = WindLoad(Lx=24.47, Ly=11.80, H=7.85, Vo = 42, WindCategory='D',LateralSystem=1)
print(WLoad.qH)
print(WLoad.kzr)
print(WLoad.nDx)
print(WLoad.X_Cpe)
print(WLoad.Y_Cpe)
print(WLoad.Cpi)
print(WLoad.X_WallWindLoad())
print(WLoad.Y_WallWindLoad())
