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

def lif_differential(I, T_total):
    """LIF padrão usando equação diferencial"""
    n_steps = int(T_total / dt)
    u = np.zeros(n_steps)
    S = np.zeros(n_steps)
    u[0] = u_rest
    
    for i in range(1, n_steps):
        # Equação do LIF: tau_m * du/dt = -(u - u_rest) + R*I
        du = (-(u[i-1] - u_rest) + R * I) * dt / tau_m
        u[i] = u[i-1] + du
        
        # Disparo e reset
        if u[i] >= theta:
            return u
    
    return 0

def update_stdp(w, t_pre, t_post, A_plus=0.1, A_minus=0.12, tau_stdp=20.0):
    dt = t_post - t_pre
    if dt > 0:
        # Potencialização (LTP)
        dw = A_plus * np.exp(-dt / tau_stdp)
    else:
        # Depressão (LTD)
        dw = -A_minus * np.exp(dt / tau_stdp)
    return w + dw

