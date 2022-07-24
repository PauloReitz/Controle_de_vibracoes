import numpy as np

def pegar_dados_originais():
    return {"largura_viga": {"d": 200, "u": "mm"},  "altura_viga": {"d": 150, "u": "mm"}, "espessura_viga": {"d": 30, "u": "mm"}, "young": {"d": 186, "u": "GPa"}, "altura_andar": {"d": 3.0, "u": "m"}, "massa_andar": {"d": 20000, "u": "kg"}, "fator_amortecimento": {"d": 0.1, "u": "mm"}, "massa_projetil": {"d": 10, "u": "kg"}, "v_projetil": {"d": 800, "u": "km/h"}}

def pegar_cond_inicial():
    return {"x0": [0,0,0,0,0],  "xdot0": [0,0,0,1,0]}

def resultado_final(dados_problema, cond_inicial):
    larg_viga = dados_problema["largura_viga"]["d"]
    alt_viga = dados_problema["altura_viga"]["d"]
    esp_viga = dados_problema["espessura_viga"]["d"]
    young = dados_problema["young"]["d"]
    alt = dados_problema["altura_andar"]["d"]
    massa = dados_problema["massa_andar"]["d"]
    fator_amort = dados_problema["fator_amortecimento"]["d"]
    m_proj = dados_problema["massa_projetil"]["d"]
    velo = dados_problema["v_projetil"]["d"]

    velo_inicial = (velo / 3.6) * m_proj / (massa + m_proj)

    cont = 0
    for value in cond_inicial["xdot0"]:
        if value != 0:
            cond_inicial["xdot0"][cont] = velo_inicial
        else:
            pass
        cont += 1

    x0 = cond_inicial["x0"]
    xdot0 = cond_inicial["xdot0"]

    inertia = 2 * (esp_viga * larg_viga ** 3) / 12 + (alt_viga - 2 * esp_viga) * (esp_viga ** 3) / 12  # mm
    k_eq = 3 * (young * (10 ** 9)) * (inertia * (10 ** (-12))) / (alt ** 3.0) * 4
    c_eq = 2 * fator_amort * np.sqrt(k_eq * massa)

    # Equações do movimento
    m = np.array([[massa, 0, 0, 0, 0],
                  [0, massa, 0, 0, 0],
                  [0, 0, massa, 0, 0],
                  [0, 0, 0, massa, 0],
                  [0, 0, 0, 0, massa]])

    k = np.array([[2 * k_eq, -k_eq, 0, 0, 0],
                  [-k_eq, 2 * k_eq, -k_eq, 0, 0],
                  [0, -k_eq, 2 * k_eq, -k_eq, 0],
                  [0, 0, -k_eq, 2 * k_eq, -k_eq],
                  [0, 0, 0, -k_eq, k_eq]])

    c = np.array([[2 * c_eq, -c_eq, 0, 0, 0],
                  [-c_eq, 2 * c_eq, -c_eq, 0, 0],
                  [0, -c_eq, 2 * c_eq, -c_eq, 0],
                  [0, 0, -c_eq, 2 * c_eq, -c_eq],
                  [0, 0, 0, -c_eq, c_eq]])

    # Problema de autovalores e autovetores!!
    d = np.matmul(np.linalg.inv(k), m)
    aval, avet = np.linalg.eig(d)

    wn = np.sqrt(1 / aval)
    wd = np.apply_along_axis(lambda x: x * np.sqrt(1 - fator_amort ** 2), 0, wn)

    X = np.zeros((len(avet), len(avet)))
    for i in range(len(avet)):
        for j in range(len(avet[i])):
            X[i, j] = avet[i, j] / avet[0, j]

    X_norm = np.zeros((len(avet), len(avet)))
    for i in range(len(X)):
        for j in range(len(X[0])):
            X_norm[i, j] = X[i, j] / (np.linalg.norm(X[:, j]) * np.sqrt(massa))

    # calculando o q
    q0 = np.matmul(np.matmul(np.transpose(X_norm), m), x0)
    qdot0 = np.matmul(np.matmul(np.transpose(X_norm), m), xdot0)
    # qi(t) = Ai*exp(Bi*t)*sen(Ci*t)

    q, A, B, C = [0] * len(X), [0] * len(X), [0] * len(X), [0] * len(X)
    for i in range(len(X)):
        A[i] = qdot0[i] / wd[i]
        B[i] = -fator_amort * wd[i]
        C[i] = wd[i]

    # voltando para unidade fisica
    # xj(t) = Xji*Ai*exp(Bi*t)*sen(Ci*t) for i in range(5)

    t = np.linspace(0, 20, 1000)
    x = np.zeros((len(X), len(t)))
    for k in range(len(t)):
        for j in range(len(X)):
            x[j, k] = np.sum([X_norm[j, i] * A[i] * t[k] * np.exp(B[i] * t[k]) * np.sin(C[i] * t[k]) for i in range(len(X))])

    t_nat = np.linspace(0, 5, 1000)
    x_nat = np.zeros((5, len(X), len(t_nat)))
    for i in range(len((wn))):
        for k in range(len(t_nat)):
            for j in range(len(X)):
                x_nat[i][j, k] = X_norm[j, i] * np.cos(wn[i] * t_nat[k])

    return {"X": X, "X_norm": X_norm, "A": A, "B": B, "C": C, "x": x, "t": t, "x_nat": x_nat, "t_nat": t_nat}

