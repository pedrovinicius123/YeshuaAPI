import numpy as np

# --- 1. Parâmetros do Modelo ---
tau_m = 10.0      # Constante de tempo (ms)
R = 1.0           # Resistência de membrana
u_rest = -70.0    # Potencial de repouso (mV)
theta = -50.0     # Limiar de disparo (threshold)
u_reset = -65.0   # Potencial de reset após disparo
dt=0.1

# 2. Definição dos Kernels (Filtros)
def kernel_eta(s, tau_m=10):
    # Efeito do disparo (refração/reset)
    return -20 * np.exp(-s / tau_m)

def kernel_kappa(s, tau_m=10, R=1):
    # Resposta à corrente de entrada
    return (R / tau_m) * np.exp(-s / tau_m)

def calc_delta_t_neuron(S, I, rng, t):
    eta = kernel_eta(rng)
    kappa = kernel_kappa(rng)

    u_spikes = np.convolve(S, eta, mode='full')[:len(t)] * dt
    u_current = np.convolve(I, kappa, mode='full')[:len(t)] * dt

    u_rest = -50
    u_total = u_rest + u_spikes + u_current 
    return u_total
