import matplotlib.pyplot as plt
from matplotlib.animation import *
from problema_base import *

class Animation:
    def __init__(self):
        self.dados_problema = pegar_dados_originais()
        self.cond_inicial = pegar_cond_inicial()
        self.resultados = resultado_final(self.dados_problema, self.cond_inicial)

    def print_equacao(self):
        X = self.resultados["X"]
        X_norm = self.resultados["X_norm"]
        A = self.resultados["A"]
        B = self.resultados["B"]
        C = self.resultados["C"]

        for j in range(len(X)):
            print("\nx_", j+1, "(t)=", end="", sep="")
            for i in range(len(X)):
                print('%.4f'%(X_norm[j,i]*A[i]), "*exp(", '%.4f'%B[i], "t)*sen(", '%.4f'%C[i], "t)", end="", sep="")
                if i is not len(X)-1 and X_norm[j,i+1]*A[i+1] > 0:
                    print("+", end="", sep="")

    def plot_projetil(self):
        t = self.resultados["t"]
        x = self.resultados["x"]

        [plt.plot(t, i) for i in x]  # gráfico da resposta
        plt.show()

    def animate(self, j):
        x_nat = self.resultados["x_nat"]
        x = self.resultados["x"]
        k = self.cont

        self.ax.clear()
        [self.ax.plot(x_nat[k][i, j], 0, ".") for i in range(len(x))]
        self.ax.set_xlim([-0.01, np.max(x) * 1.1])
        self.ax.set_ylim([-0.04, 0.04])

    def animate2(self, j):
        x = self.resultados["x"]

        self.ax.clear()
        [self.ax.plot(x[i, j], 0, ".") for i in range(len(x))]
        self.ax.set_xlim([-0.01, np.max(x) * 1.1])
        self.ax.set_ylim([-0.04, 0.04])

    def animar(self, op):
        x = self.resultados["x"]
        x_nat = self.resultados["x_nat"]

        for j in range(len(x[0])):
            x[1][j] += 0.01
            x[2][j] += 0.02
            x[3][j] += 0.03
            x[4][j] += 0.04

        for k in range(5):
            for j in range(len(list(x_nat[0][0]))):
                x_nat[k][1][j] += 0.01
                x_nat[k][2][j] += 0.02
                x_nat[k][3][j] += 0.03
                x_nat[k][4][j] += 0.04

        t_nat = self.resultados["t_nat"]
        fig, self.ax = plt.subplots(1, 1)

        if op == 1:
            self.cont = 0
            for k in range(5):
                self.cont = k
                ani2 = FuncAnimation(fig, self.animate, frames=len(t_nat), interval=5, repeat=True)
                ani2.save("freq"+str(k+1)+".gif")

        if op == 2:
            ani = FuncAnimation(fig, self.animate2, frames=len(x[0]), interval=20, repeat=False)
            plt.show()
            ani.save("resposta.gif")

        else:
            pass

    def print_all(self):
        print(self.resultados)

Animacao = Animation()
# Animacao.print_equacao()
# Animacao.plot_projetil()
Animacao.animar(2)
# Animacao.print_all()
