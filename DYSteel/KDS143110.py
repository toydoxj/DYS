import DYSteel.Section as Sec
import math

# Redefining the Material class using class methods to manage material properties
class Material:
    # Initializing a class variable with material properties
    materials = {
        "SS275": {"Fy": 275, "Fu": 485},
        "SM355": {"Fy": 355, "Fu": 490}
    }

    @classmethod
    def get_properties(cls, material_name):
        # Return the properties of the requested material
        return cls.materials.get(material_name, "Material not found")

# Using the class method to retrieve properties for SS275
SS275 = Material.get_properties("SS275")



'''' 
KDS 14 31 10
강구조 부재설계기준 (하중저항계수 설계법)
'''

class Mn:
    '''
    철골의 휨모멘트 산정 Class
    현재 - 강축 휨을 받는 2축대칭 H형강 또는 ㄷ형강 조밀단면 부재
    국부좌굴 X
    '''

    @classmethod
    def HShape(cls, Mat, Section, Lb, E : int = 210000, Cb : float = 1.0  ):
        '''
        KDS 14 31 10 (4.3.2.1.1.2)
        식 (4.3-2)
        '''
        SecObject = Sec.HSec(Section)
        SecProperties = SecObject.properties

        print(SecProperties)
        
        Fy = Material.get_properties(Mat)['Fy']
        ry = SecProperties['iy']
        Iy = SecProperties['Iy']
        Sx = SecProperties['Sx']
        Zx = SecProperties['Zx']
        J = SecProperties['J']
        Cw = SecProperties['CW']
        ho = SecProperties['H']- SecProperties['t2']

        rts = ((Iy*Cw)**(1/2) / Sx ) **(1/2)
        c = 1 # H형강인 경우에만 c=1임.

        Lp = 1.76*ry * (E/Fy)**(1/2)
        Lr = 1.95 * rts * ( E / (0.7*Fy)) * (( J * c ) / (Sx * ho)) **(1/2) * (1 + (1+6.76*((0.7*Fy /E)*(Sx * ho / (J *c)))**2)**(1/2))**(1/2)


        Mp = Fy * Zx * 10**-6
    

        if Lb <= Lp : 
            Mn = Mp
        elif Lb <= Lr :
            Mn = Cb * (Mp - (Mp - 0.7 * Fy * Sx * 10**-6) * (Lb - Lp) / (Lr - Lp))
            
        else:
            Fcr = Cb * 3.14**2 * 205000 / (Lb / rts)**2 * (1+0.078*J*c / (Sx * ho)*(Lb/rts)**2)**(1/2)
            Mn = Fcr * Sx 

        return min(Mn, Mp)
    
class Vn:
    '''
    철골의 휨모멘트 산정 Class
    현재 - 강축 휨을 받는 2축대칭 H형강 또는 ㄷ형강 조밀단면 부재
    국부좌굴 X
    '''

    @classmethod
    def HShape(cls, Mat, Section, Lb, E : int = 210000, Cb : float = 1.0  ):
        '''
        KDS 14 31 10 (4.3.2.1.1.2)
        식 (4.3-2)
        '''
        SecObject = Sec.HSec(Section)
        SecProperties = SecObject.properties

        print(SecProperties)
        
        Fy = Material.get_properties(Mat)['Fy']
        ry = SecProperties['iy']
        Iy = SecProperties['Iy']
        Sx = SecProperties['Sx']
        Zx = SecProperties['Zx']
        J = SecProperties['J']
        Cw = SecProperties['CW']
        ho = SecProperties['H']- SecProperties['t2']

        rts = ((Iy*Cw)**(1/2) / Sx ) **(1/2)
        c = 1 # H형강인 경우에만 c=1임.

        Lp = 1.76*ry * (E/Fy)**(1/2)
        Lr = 1.95 * rts * ( E / (0.7*Fy)) * (( J * c ) / (Sx * ho)) **(1/2) * (1 + (1+6.76*((0.7*Fy /E)*(Sx * ho / (J *c)))**2)**(1/2))**(1/2)


        Mp = Fy * Zx * 10**-6
    

        if Lb <= Lp : 
            Mn = Mp
        elif Lb <= Lr :
            Mn = Cb * (Mp - (Mp - 0.7 * Fy * Sx * 10**-6) * (Lb - Lp) / (Lr - Lp))
            
        else:
            Fcr = Cb * 3.14**2 * 205000 / (Lb / rts)**2 * (1+0.078*J*c / (Sx * ho)*(Lb/rts)**2)**(1/2)
            Mn = Fcr * Sx 

        return min(Mn, Mp)    
    
print(Mn.HShape('SS275', 'H-500x200x10/16',5))



