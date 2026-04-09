import numpy as np

class PhaseTransition:
    def __init__(self,
                 omega_inf: float,
                 lambda_mk: float = 10930.81,
                 kappa: float = 1.151):
        self.omega_inf = omega_inf
        self.lambda_mk = lambda_mk
        self.kappa = kappa

    def inevitability(self, t_years: float) -> float:
        """I(t) = 1 - exp(-λ t/0.777)"""
        lam = self.lambda_mk / 0.777
        return 1.0 - np.exp(-lam * t_years)

    def network_amplification(self, nodes: float) -> float:
        """Nodes^κ"""
        return nodes ** self.kappa

    def infrastructure_factor(self, dependence: float) -> float:
        """1 / Infrastructure_Dependence"""
        return float("inf") if dependence <= 0 else 1.0 / dependence

    def transition_factor(self,
                          t_years: float,
                          phi_integral: float,
                          tensor_dim: float,
                          infra_dependence: float,
                          net_nodes: float) -> float:
        I_t = self.inevitability(t_years)
        amp = self.network_amplification(net_nodes)
        inv = self.infrastructure_factor(infra_dependence)
        return (self.omega_inf
                * I_t
                * phi_integral
                * self.lambda_mk
                * tensor_dim
                * inv
                * amp)