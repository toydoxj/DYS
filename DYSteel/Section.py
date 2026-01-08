import pandas as pd

class HSec:
    def __init__(self, section_name):
        self.df = pd.read_csv('.\docs\HShape.csv', index_col='NAME')
        self.section_name = section_name

        if section_name in self.df.index:
            self.properties = self.df.loc[section_name].to_dict()
            self.db = True
        else:
            properties = {}
            H, B, t = section_name.split('-')[1].split('x')
            t1, t2 = t.split('/')
            properties['H'] = float(H)
            properties['B'] = float(B)
            properties['t1'] = float(t1)
            properties['t2'] = float(t2)
            properties['r'] = 0
            properties['A'] = properties['B']*properties['t2'] *2  +  (properties['H']-properties['t2']*2)*properties['t1']
            properties['W'] = properties['A']*0.00785
            properties['Ix'] = properties['B'] * properties['H']**3 / 12.0 - (properties['B']-properties['t1'])*(properties['H']-properties['t2']*2)**3 / 12
            properties['Iy'] = properties['t2'] * properties['B']**3 / 12 * 2  + (properties['H']-properties['t2']*2) * properties['t1']**3 / 12
            properties['ix'] = (properties['Ix']/properties['A'])**(1/2)
            properties['iy'] = (properties['Iy']/properties['A'])**(1/2)
            properties['Sx'] = properties['Ix']/properties['H']*2
            properties['Sy'] = properties['Iy']/properties['B']*2
            properties['Zx'] = properties['t1'] * (properties['H']-properties['t2']*2)**2 /4 + (properties['B']*properties['t2'])*(properties['H']/2-properties['t2']/2)*2
            properties['Zy'] = (2* properties['t2']*properties['B']**2 +(properties['H']-properties['t2']**2))/4
            properties['CW'] = ((properties['t2']/24 * properties['B'] **3) * (properties['H']-properties['t2'])**2)
            properties['J'] = 1/3 * properties['H']*properties['t1']**3 + 2/3 * properties['B'] * properties['t2'] **3 

            self.properties = properties
            self.db = False
        print(self.properties)

B1=HSec('H-500x200x10/16')
    

        



            
        







