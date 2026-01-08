import DYSteel.Section as Sec
import math

class Hsec :
    def __init__ (self, shape, Fy):
        self.phi = 0.9
        self.Sproperties = Sec.HSec(shape)
        self.Fy = Fy
        self.Zx = self.Sproperties.properties['Zx']
        self.Iy = self.Sproperties.properties['Iy']
        self.CW = self.Sproperties.properties['CW']
        self.Sx = self.Sproperties.properties['Sx']
        self.ry = self.Sproperties.properties['iy']
        self.J = self.Sproperties.properties['J']
        self.h0 = self.Sproperties.properties['H'] - self.Sproperties.properties['t2']
        self.Aw = self.Sproperties.properties['H'] * self.Sproperties.properties['t1']

        self.tw = self.Sproperties.properties['t1']
        self.h = self.Sproperties.properties['H']-self.Sproperties.properties['t2']*2-self.Sproperties.properties['r']
        self.w_slender = self.h / self.tw
    
    def Mp (self):
        return self.Fy * self.Zx * 10 ** -6
    
    def slender_flange(self):
        b = self.Sproperties.properties['B']/2
        t = self.Sproperties.properties['t2']
        self.f_lambda_p = 0.38 * (210000/self.Fy) ** (1/2)
        self.kc = 0
  
        if self.Sproperties.db == True: 
            self.f_lambda_r = 1.0 * (210000/self.Fy) ** (1/2)
        else:
            h = self.Sproperties.properties['H'] - self.Sproperties.properties['t2']*2
            tw = self.Sproperties.properties['t1']
            self.kc = 4 / ((h/tw)**(1/2))            
            if self.kc < 0.35 : self.kc = 0.35
            if self.kc > 0.76 : self.kc = 0.76

            check_web = self.slender_web(self.Fy)
            if check_web == 2 : FL = 0.5*self.Fy
            else : FL = 0.7*self.Fy
            self.f_lambda_r = 0.95 * (self.kc * 210000 / FL)

        self.f_selnder = b / t
        
        if self.f_selnder < self.f_lambda_p : return 0      
        elif self.f_selnder > self.f_lambda_r : return 2
        else : return 1

    def slender_web(self):
        lambda_p = 3.76 * (210000/self.Fy) ** (1/2)
        lambda_r = 5.70 * (210000/self.Fy) ** (1/2)

        if self.w_slender < lambda_p : return 0
        elif self.w_slender > lambda_r : return 2
        else : return 1
    
    def Mn_localbuck_flange(self):
        localbuck = self.slender_flange()

        lambda_p = self.f_lambda_p
        lambda_r = self.f_lambda_r
        f_slender = self.f_selnder

        if localbuck == 0 :
            return self.Mp()
        if localbuck == 1 :
            Mr = 0.7 * self.Fy * self.Sx * 10 ** -6
            return (self.Mp() - (self.Mp()-Mr)*(f_slender-lambda_p)/(lambda_r-lambda_p)) 
        if localbuck == 2 :
            Fcr = 0.9 * 210000 * self.kc / f_slender * 10 ** -6
            return Fcr * self.Sx
        
    def Mn_lateralBuck(self, Cb = 1.0, Lb = 0):
        Lb = Lb * 1000
        Lp = 1.76*self.ry*(210000/self.Fy)**(1/2)
        rts = ((self.Iy * self.CW)**(1/2) / self.Sx)**(1/2)
        JcSh = self.J * 1.0 / (self.Sx * self.h0)
        Lr = 1.95 * rts* 210000 / (0.7*self.Fy) * JcSh**(1/2) * (1+(1+6.76*((0.7*self.Fy/210000)/JcSh)**2)**(1/2))**(1/2)
        Fcr = Cb*math.pi**2 * 210000 / (Lb/rts)**2 * (1+0.078*JcSh * (Lb/rts)**2)**(1/2)
        print('Fcr = ',Fcr)
        Mn1 = Cb * (self.Mp()-(self.Mp()-0.7*self.Fy*self.Sx*10**-6)*(Lb-Lp)/(Lr-Lp))
        Mn2 = Fcr * self.Sx * 10**-6

        if Lb < Lp : Mn = self.Mp()
        elif Lb < Lr : Mn = min( Mn1 , self.Mp())
        else : Mn = min(Mn2, self.Mp())

        return Mn, self.Mp(),Mn1,Mn2,Lp,Lr
        
    def Vn(self, db = False):
        kv = 5                                                                   # plateGirder는 아직 반영 되지 않음
        if self.w_slender <= 1.1*(kv * 210000 / self.Fy)**(1/2): Cv = 1.0
        elif self.w_slender <= 1.37*(kv * 210000 / self.Fy)**(1/2): Cv = (1.1*(kv * 210000 / self.Fy)**(1/2))/self.w_slender
        else: Cv = 1.51*210000*kv / ((self.w_slender)**2 *self.Fy)

        if self.w_slender <= 2.24*( 210000 / self.Fy)**(1/2) and db == True : phi = 1.0
        else : phi = 0.9
        return 0.6 * self.Fy * self.Aw * Cv * 10 ** -3, phi
        


