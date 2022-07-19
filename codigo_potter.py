import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Dados
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

#Condições iniciais
x0 = [0,0,0,0,0]
velo_inicial = (velo/3.6)*m_proj/(massa+m_proj)
xdot0 = [0,0,0,velo_inicial,0]

#Equações do movimento
m = np.array([[massa, 0, 0, 0, 0],
             [0, massa, 0, 0, 0],
             [0, 0, massa, 0, 0],
             [0, 0, 0, massa, 0],
             [0, 0, 0, 0, massa]])

k = np.array([[2*k_eq,  -k_eq,  0,       0,     0],
              [-k_eq,   2*k_eq, -k_eq,   0,     0],
              [0,       -k_eq,  2*k_eq,  -k_eq, 0],
              [0,       0,      -k_eq,   2*k_eq,-k_eq],
              [0,       0,      0,       -k_eq, k_eq]])

c = np.array([[2*c_eq,  -c_eq,  0,       0,      0],
              [-c_eq,   2*c_eq, -c_eq,   0,      0],
              [0,       -c_eq,  2*c_eq,  -c_eq,  0],
              [0,       0,      -c_eq,   2*c_eq, -c_eq],
              [0,       0,      0,       -c_eq,  c_eq]])

# Problema de autovalores e autovetores!!
d = np.matmul(np.linalg.inv(k) , m)
aval, avet = np.linalg.eig(d)

wn = np.sqrt(1/aval)
wd = np.apply_along_axis(lambda x : x*np.sqrt(1-fator_amort**2), 0, wn)

X = np.zeros((len(avet),len(avet)))
for i in range(len(avet)):
    for j in range(len(avet[i])):
       X[i, j] = avet[i, j]/avet[0, j]

X_norm = np.zeros((len(avet),len(avet)))
for i in range(len(X)):
    for j in range(len(X[0])):
        X_norm[i,j] = X[i,j]/np.linalg.norm(X[:,j])

#calculando o q
q0 = np.matmul(np.matmul(np.transpose(X_norm),m),x0)
qdot0 = np.matmul(np.matmul(np.transpose(X_norm),m),xdot0)
# qi(t) = Ai*exp(Bi*t)*sen(Ci*t)
q, A, B, C = [0]*len(X), [0]*len(X), [0]*len(X), [0]*len(X)
for i in range(len(X)):
    A[i] = qdot0[i]/wd[i]
    B[i] = -fator_amort*wd[i]
    C[i] = wd[i]

# voltando para unidade fisica
# xj(t) = Xji*Ai*exp(Bi*t)*sen(Ci*t) for i in range(5)

# for j in range(len(X)):
#     print("\nx_", j+1, "(t)=", end="", sep="")
#     for i in range(len(X)):
#         print('%.4f'%(X_norm[j,i]*A[i]), "*exp(", '%.4f'%B[i], "t)*sen(", '%.4f'%C[i], "t)", end="", sep="")
#         if i is not len(X)-1 and X_norm[j,i+1]*A[i+1] > 0:
#             print("+", end="", sep="")
#descomentar para printar as respostas algébricas de x

t = np.linspace(0, 20, 1000)
x = np.zeros((len(X), len(t)))
for k in range(len(t)):
    for j in range(len(X)):
        x[j, k] = np.sum([X_norm[j,i]*A[i]*t[k]*np.exp(B[i]*t[k])*np.sin(C[i]*t[k]) for i in range(len(X))])

#plotagem - projetil

[plt.plot(t, i) for i in x] #gráfico da resposta

fig, ax = plt.subplots(1, 1)

def animate(j):
    ax.clear()
    [ax.plot(x[i, j], i + 1, ".") for i in range(len(x))]
    ax.set_xlim([-300, 300])
    ax.set_ylim([0, 6])

ani = FuncAnimation(fig, animate, frames=len(x[0]), interval=20, repeat=False)
plt.show()
ani.save("resposta.gif")
#descomentar esses comentários para salvar gif da resposta

#plotagem - frequencias naturais
t_nat = np.linspace(0, 5, 1000)
x_nat = np.zeros((5, len(X), len(t_nat)))
for i in range(len((wn))):
    for k in range(len(t_nat)):
        for j in range(len(X)):
            x_nat[i][j, k] = X_norm[j,i]*np.cos(wn[i]*t_nat[k])

def animate2(j):
    ax2.clear()
    [ax2.plot(x_nat[k][i, j], i + 1, ".") for i in range(len(x))]
    ax2.set_xlim([-np.max(x_nat)*1.1, np.max(x_nat)*1.1])
    ax2.set_ylim([0, 6])

fig2, ax2 = plt.subplots(1, 1)
# for k in range(5):
#     ani2 = FuncAnimation(fig2, animate2, frames=len(t_nat), interval=5, repeat=True)
#     ani2.save("freq"+str(k+1)+".gif")
#     #plt.show()
#     print(k) #descomentar para salvar gifs dos modos de vibração
