class phi:
    '''
    KDS 14 20 10 4.2.3(2) 강도 감소 계수
    classmethod 함수로 구성됨.
    normal : 일반 Tie-bar
    spiral : 나선형 
    shear : 전단과 비틀림
    bearing : 지압
    pureconcrete : 무근콘크리트
    '''
    
    @classmethod
    def normal(cls, et : float, fy : int) -> float:
        '''
        일반적인 Tie-Bar
        '''
        Es = 200000
        ey = fy / Es
        limit_tension = max(0.005, 2.5 * ey) 

        if et <= ey:
            return 0.65
        elif et >= 2.5 * ey :
            return 0.85
        else:
            return 0.65 + 0.2 * (et - ey) / (limit_tension - ey)
        
    @classmethod
    def spiral(cls, et : float, fy : int) -> float:
        '''
        나선형 철근
        '''
        Es = 200000
        ey = fy / Es
        limit_tension = max(0.005, 2.5 * ey) 

        if et <= ey:
            return 0.7
        elif et >= 2.5 * ey :
            return 0.85
        else:
            return 0.7 + 0.15 * (et - ey) / (limit_tension - ey)
        
    @classmethod
    def shear(cls) -> float:
        '''
        전단
        '''
        return 0.75
    
    @classmethod
    def bearing(cls) -> float:
        '''
        지압
        '''
        return 0.65
    
    @classmethod
    def pureconcrete(cls) -> float:
        '''
        무근콘크리트
        '''
        return 0.55
        

print(phi.__doc__)





