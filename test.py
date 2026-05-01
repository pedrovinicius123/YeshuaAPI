import numpy as np
import matplotlib.pyplot as plt

# 1. Configurações de tempo
dt = 0.1
t = np.arange(0, 100, dt)

# 2. Definição dos Kernels (Filtros)
def kernel_eta(s, tau_m=10):
    # Efeito do disparo (refração/reset)
    return -20 * np.exp(-s / tau_m)

def kernel_kappa(s, tau_m=10, R=1):
    # Resposta à corrente de entrada
    return (R / tau_m) * np.exp(-s / tau_m)

# Criando os vetores dos filtros
s_range = np.arange(0, 50, dt)
eta = kernel_eta(s_range)
kappa = kernel_kappa(s_range)

# 3. Estímulos de entrada
# Corrente constante
I = np.ones_like(t) * 25 
# Trem de pulsos (Spikes de entrada) - imagine um spike no tempo 20ms
S = np.zeros_like(t)
S[int(20/dt)] = 1/dt 

# 4. Implementação da Equação (Convolução)
# u(t) = (eta * S) + (kappa * I)
u_spikes = np.convolve(S, eta, mode='full')[:len(t)] * dt
u_current = np.convolve(I, kappa, mode='full')[:len(t)] * dt

u_rest = -50
u_total = u_rest + u_spikes + u_current

# Visualização
plt.figure(figsize=(10, 5))
plt.plot(t, u_total, label='u(t) SRM')
plt.axhline(u_rest, color='gray', linestyle='--', label='Repouso')
plt.title("Implementação via Convolução (Kernel)")
plt.legend()
plt.show()