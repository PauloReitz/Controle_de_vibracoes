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
        x = self.resultados["x"]

        self.ax.clear()
        [self.ax.plot(x[i, j], i + 1, ".") for i in range(len(x))]
        self.ax.set_xlim([-np.max(x) * 1.1, np.max(x) * 1.1])
        self.ax.set_ylim([0, 6])

    def animate2(self, j):
        x_nat = self.resultados["x_nat"]
        x = self.resultados["x"]
        k = self.cont

        self.ax.clear()
        [self.ax.plot(x_nat[k][i, j], i + 1, ".") for i in range(len(x))]
        self.ax.set_xlim([-np.max(x_nat) * 1.1, np.max(x_nat) * 1.1])
        self.ax.set_ylim([0, 6])

    def animar(self, op):
        x = self.resultados["x"]
        t_nat = self.resultados["t_nat"]
        fig, self.ax = plt.subplots(1, 1)

        if op == 1:
            self.cont = 0
            for k in range(5):
                self.cont = k
                ani2 = FuncAnimation(fig, self.animate2, frames=len(t_nat), interval=5, repeat=True)
                plt.show()
                ani2.save("freq"+str(k+1)+".gif")

        else:
            ani = FuncAnimation(fig, self.animate, frames=len(x[0]), interval=20, repeat=False)
            plt.show()
            ani.save("resposta.gif")


Animacao = Animation()
# Animacao.print_equacao()
# Animacao.plot_projetil()
# Animacao.animar(1)
# Animacao.animar(2)
