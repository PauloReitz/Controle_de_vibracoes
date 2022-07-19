###DADOS###

# Perfil da viga
larg_viga = 200 #mm
alt_viga = 150 #mm
esp_viga = 30 #mm

young = 186 #GPa
alt = 3.0 #m
massa = 20000 #kg
fator_amort = 0.1

m_proj = 10 #kg
velo = 800 #km/h

inertia = 2*(esp_viga*larg_viga**3)/12 + (alt_viga-2*esp_viga)*(esp_viga**3)/12 #mm
k_eq = 3*(young*(10**9))*(inertia*(10**(-12)))/(alt**3.0) * 4
c_eq = 2*fator_amort*np.sqrt(k_eq*massa)