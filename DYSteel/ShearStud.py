# 수평전단력 ###############################################
# KDS (4.6-19), (4.6-20)
# fck : 콘크리트 강도       MPa
# beff : 합성보의 유효폭    mm
# thk_con : 슬래브 두께     mm
# Fy :  강재 강도           MPa
# As :  강재 단면적         mm2
############################################################

def latral_shearforce(fck, beff, thk_con, Fy, As):
    V1 = 0.85 * fck * thk_con * beff    # 콘크리트 압괴
    V2 = Fy * As                        # 강재단면의 인장항복강도
    return min(V1, V2) / 1000           # 반환값 kN

# 스터드 직경과 높이 제한 ####################################
# 데크플레이트의 골에 설치되는 강재 전단연결재를 제외하고, 전단연결재의 측면 피복은 25 mm 이상이 되어야 한다. 
# 강재 전단연결재의 중심에서 전단력 방향에 있는 가장자리까지의 거리는 보통콘크리트에서는 200 mm 이상, 경량콘크리트에서는 250 mm 이상으로 한다. 
# [0] 강재보의 웨브 위에 위치하지 않는 경우, 전단연결재의 직경은 용접되는 플랜지 두께의 2.5배를 초과해서는 안 된다. 
# [1] 스터드 전단연결재의 중심 간 간격은 합성보의 길이방향으로는 스터드 전단연결재 직경의 6배 이상이 되어야 하며 
# [2] 직각방향으로는 직경의 4배 이상이 되어야 한다. 
# [3] 스터드 전단연결재의 중심 간 간격은 슬래브 총 두께의 8배 또는 900 mm를 초과할 수 없다.
# [4] 보통 콘크리트를 사용하는 경우, 전단력만 받는 스터드 전단연결재의 길이는 몸체직경의 5배 이상으로 한다.
# [5] 콘크리트 슬래브와 강재보를 연결하는 스터드는 직경이 19 mm 이하
# [6] 스터드 전단연결재의 상단 위로 13 mm 이상의 콘크리트피복이 있어야 한다.
# n : 스터드 열수
# dstud : 스터드 직경       mm
# lstud : 스터드 높이(길이) mm
# spacing : 스터드 간격     mm
# b : 플랜지 폭             mm
# tf : 플랜지 두께          mm
# thk_slab : 콘크리트 슬래브 두께 mm
############################################################

def check_stud(n, dstud, lstud, spacing, b, tf, thk_slab):
    ErrorCode = [0, 0, 0, 0, 0, 0, 0]
    if n != 1 and dstud > 2.5 * tf : ErrorCode[0] = 1
    if spacing < 6 * dstud : ErrorCode[1] = 1
    if n != 1 : 
        if (b - 100) / ( n - 1 ) < 4 * dstud : ErrorCode[2] = 1
    if spacing > 8 * max(thk_slab, 900) : ErrorCode[3] = 1 
    if lstud < 5 * dstud :  ErrorCode[4] = 1
    if dstud > 19 : ErrorCode[5] = 1
    if thk_slab - lstud < 13 : ErrorCode[6] = 1

    return ErrorCode

# 스터드 강도 ###############################################
# 여기서는 골데크를 사용하지 않는 것으로 한다.
# KDS (4.6-33)
# dstud : 스터드 직경       mm
# fck : 콘크리트 강도       MPa
# Fu : 스터드 인장강도      MPa
############################################################
# 반환값 : 스터드 1개 강도  kN
############################################################

def Capacity_stud(dstud, fck, Fu):
    Rg = 1.0
    Rp = 0.75
    A_sc = 3.14 * dstud ** 2 /4
    if fck < 40 : 
        fcu = fck + 4
    elif fck < 60 :
        fcu = fck + fck/10
    else :
        fcu = fck + 6
    
    Ec = 8500 * fcu ** (1/3)
    return min(0.5 * A_sc * (fck * Ec) ** (1/2), Rg * Rp * A_sc * Fu ) / 1000

# 전체 스터드 갯수와 전체 스터드 강도##########################
# n :   스터드 열수
# spacing : 스터드 간격      mm
# span : 보 경간            m
# Qn : 스터드 1개 강도      kN
# V : 수평전단력            kN
############################################################
# 반환값 : 전체 스터드 강도 ΣQn (kN), 합성률 (1 이하)
############################################################


def nStud(n, spacing, span, Qn, V):
    total_stud = int(span * 1000 / (spacing) / 2 * n )
    sigmaQn = Qn * total_stud
    ratio_composite = min (sigmaQn / V, 1) 
    return sigmaQn, ratio_composite
