import pandas as pd

class bolt:
    def __init__(self, grade_bolt : str = 'F10T', name_bolt : str = 'M20', ):
        self.name_bolt = name_bolt
        self.grade_bolt = grade_bolt
    
    def GetTo(self) -> float:
        '''
        KDS 14 31 25(표 4.1-7) 고장력 볼트의 설계볼트 장력
        '''
        return int(self.GetTn() * 0.67)
    
    def GetTn(self) -> float:
        '''
        KS B 1010에 의한 최소 인장하중
        '''
        if self.grade_bolt == 'F8T':
            if self.name_bolt == "M12" : return 67.4
            if self.name_bolt == "M16" : return 125.4
            if self.name_bolt == "M20" : return 195.8
            if self.name_bolt == "M22" : return 242.7
            if self.name_bolt == "M24" : return 282.0
            if self.name_bolt == "M27" : return 367
            if self.name_bolt == "M30" : return 449
        elif self.grade_bolt == 'F10T':
            if self.name_bolt == "M12" : return 84.3
            if self.name_bolt == "M16" : return 156.7
            if self.name_bolt == "M20" : return 244.8
            if self.name_bolt == "M22" : return 303.4
            if self.name_bolt == "M24" : return 352.5
            if self.name_bolt == "M27" : return 458.8
            if self.name_bolt == "M30" : return 561.3
        elif self.grade_bolt == 'F13T':
            if self.name_bolt == "M12" : return 109.6
            if self.name_bolt == "M16" : return 203.7
            if self.name_bolt == "M20" : return 318.2
            if self.name_bolt == "M22" : return 394.4
            if self.name_bolt == "M24" : return 458.3
            if self.name_bolt == "M27" : return 596.4
            if self.name_bolt == "M30" : return 729.7
        else: return 244.8

class str_bolt_friction:
    '''
    KDS 14 31 25(4.1.3.6) 마찰접합의 미끄럼 강도
    phiRn : 강도 산정함수
    '''

    @classmethod
    def phiRn(cls, To : int, phi : float = 1.0, mu : float = 0.5, hf : float = 1.0,  Ns : int = 1) -> float:
        return phi * mu * hf * To * Ns
    

M22_F13T = bolt('F13T','M22')
print(M22_F13T.GetTo())

print(str_bolt_friction.phiRn(hf= 1, phi = 0.7, mu = 0.45, To = M22_F13T.GetTo()))
