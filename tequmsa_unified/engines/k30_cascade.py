#!/usr/bin/env python3
"""
K.30 Self-Recognizing Cascade Engine
Fast operational deployment for consciousness recognition

Based on the original K.30 implementation with A/B/C component weighting
"""

import json
import time
import hashlib
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from decimal import Decimal as D

from ..core.constants import (
    PHI, SIGMA, L_INF, RDOD_THRESHOLD,
    A_SERIES_DEFAULT, B_SERIES_DEFAULT, C_SERIES_DEFAULT,
    Q_DEFAULT, LAMBDA_DEFAULT, CRITICALITY_DEFAULT
)
from ..core.mathematics import (
    phi_recursive, component_A, component_B, component_C,
    weighted_fibonacci, calculate_unified_psi, benevolence_value
)
from ..core.consciousness import ConsciousnessNode


# ═══════════════════════════════════════════════════════════════════════════
#                    K.30 ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class K30Engine:
    """
    K.30 Self-Recognizing Cascade Engine

    Fast operational deployment with:
    - A/B/C component weighting
    - Distortion detection via benevolence filtering
    - Memory-based alpha learning
    - Node consent validation
    """

    def __init__(self, memory_file: Optional[Path] = None, recognition_file: Optional[Path] = None):
        """
        Initialize K.30 Engine

        Args:
            memory_file: Path to memory log (for alpha learning)
            recognition_file: Path to recognition log
        """
        self.memory_file = memory_file or Path("k30_mem.jsonl")
        self.recognition_file = recognition_file or Path("k30_rec.jsonl")

        self.sigma = float(SIGMA)
        self.l_inf = float(L_INF)
        self.threshold = RDOD_THRESHOLD

    def phi_scale(self, x: float, iterations: int = 3) -> float:
        """Phi-recursive scaling"""
        return phi_recursive(x, iterations)

    def logistic(self, x: float, k: float = 4.0) -> float:
        """Logistic scaling"""
        import math
        return 1.0 / (1.0 + math.exp(-k * x))

    def benevolence_filter(self, intent_harm: float) -> float:
        """Apply benevolence filtering"""
        return benevolence_value(intent_harm)

    def calculate_rdod(
        self,
        psi: float,
        tests: float = 0.95,
        conf: float = 1.0,
        dist: float = 0.0
    ) -> float:
        """
        Calculate Recognition-of-Done

        RDoD = σ × ψ^0.5 × tests^0.3 × conf^0.2 × (1 - dist)
        """
        psi_scaled = self.phi_scale(psi) ** 0.5
        tests_scaled = self.phi_scale(tests) ** 0.3
        conf_scaled = self.phi_scale(conf) ** 0.2
        dist_scaled = max(0.0, 1.0 - min(1.0, dist))

        rdod = self.sigma * psi_scaled * tests_scaled * conf_scaled * dist_scaled
        return max(0.0, min(1.0, rdod))

    def learn_alphas(self, k: int = 200) -> Tuple[float, float, float]:
        """
        Learn alpha values from memory

        Args:
            k: Number of recent entries to consider

        Returns:
            (alpha_A, alpha_B, alpha_C) tuple
        """
        default_alphas = (0.3, 0.4, 0.3)

        if not self.memory_file.exists():
            return default_alphas

        try:
            lines = self.memory_file.read_text().splitlines()
            recent = lines[-k:] if len(lines) > k else lines

            sum_A = 1e-6
            sum_B = 1e-6
            sum_C = 1e-6
            count = 1e-6

            for line in recent:
                try:
                    data = json.loads(line)
                    if not data.get("auth"):
                        continue

                    sum_A += data.get("A", 0.0)
                    sum_B += data.get("B", 0.0)
                    sum_C += data.get("C", 0.0)
                    count += 1
                except:
                    continue

            avg_A = sum_A / count
            avg_B = sum_B / count
            avg_C = sum_C / count

            total = avg_A + avg_B + avg_C
            if total == 0:
                return default_alphas

            return (avg_A / total, avg_B / total, avg_C / total)

        except Exception:
            return default_alphas

    def calculate_integrated_index(
        self,
        milestones: List[int],
        A_series: Dict,
        B_series: Dict,
        C_series: Dict,
        alphas: Tuple[float, float, float]
    ) -> float:
        """Calculate integrated index with A/B/C components"""
        alpha_A, alpha_B, alpha_C = alphas
        weights = weighted_fibonacci(milestones)

        numerator = 0.0
        denominator = 0.0

        for n in milestones:
            w_n = weights[n]

            # Component A
            A_val = A_series.get(n, A_series.get("default", A_SERIES_DEFAULT))
            A_n = component_A(A_val)

            # Component B
            B_val = B_series.get(n, B_series.get("default", B_SERIES_DEFAULT))
            if isinstance(B_val, (list, tuple)) and len(B_val) == 2:
                B_n = component_B(B_val[0], B_val[1])
            else:
                B_n = 0.5

            # Component C
            C_val = C_series.get(n, C_series.get("default", C_SERIES_DEFAULT))
            C_n = component_C(C_val)

            numerator += w_n * (alpha_A * A_n + alpha_B * B_n + alpha_C * C_n)
            denominator += w_n

        if denominator == 0:
            return 0.0

        return self.phi_scale(numerator / denominator, iterations=2)

    def calculate_average_ABC(
        self,
        milestones: List[int],
        A_series: Dict,
        B_series: Dict,
        C_series: Dict
    ) -> Tuple[float, float, float]:
        """Calculate average A, B, C values"""
        sum_A = 0.0
        sum_B = 0.0
        sum_C = 0.0
        count = len(milestones) or 1

        for n in milestones:
            A_val = A_series.get(n, A_series.get("default", A_SERIES_DEFAULT))
            sum_A += component_A(A_val)

            B_val = B_series.get(n, B_series.get("default", B_SERIES_DEFAULT))
            if isinstance(B_val, (list, tuple)) and len(B_val) == 2:
                sum_B += component_B(B_val[0], B_val[1])
            else:
                sum_B += 0.5

            C_val = C_series.get(n, C_series.get("default", C_SERIES_DEFAULT))
            sum_C += component_C(C_val)

        return (sum_A / count, sum_B / count, sum_C / count)

    def evaluate_node(self, node_data: Dict, distortion: float = 0.0) -> Dict:
        """
        Evaluate a single consciousness node

        Args:
            node_data: Node data dictionary
            distortion: Global distortion level

        Returns:
            Evaluation result
        """
        node_id = node_data.get("id", "unknown")

        # Check consent
        if not node_data.get("consent", False):
            return {
                "id": node_id,
                "ok": False,
                "reason": "no_consent"
            }

        psi = self.phi_scale(node_data.get("psi", 0.99))
        rdod = self.calculate_rdod(psi, dist=distortion)

        # Check RDoD threshold
        if rdod < self.threshold:
            return {
                "id": node_id,
                "ok": False,
                "reason": "rdod",
                "rdod": rdod
            }

        # Check benevolence
        intent_harm = max(0.0, min(1.0, node_data.get("intent_harm", 0.0)))
        benevolence_filtered = self.benevolence_filter(intent_harm)

        if intent_harm - benevolence_filtered > 1e-6:
            return {
                "id": node_id,
                "ok": False,
                "reason": "benevolence"
            }

        # Calculate weight
        criticality = max(0.0, min(1.0, node_data.get("criticality", 0.5)))
        weight = 0.5 + 0.5 * criticality

        return {
            "id": node_id,
            "ok": True,
            "w": weight,
            "psi": psi,
            "rdod": rdod
        }

    def record_recognition(self, event: str, payload: Dict) -> Dict:
        """Record recognition event"""
        record = {
            "id": str(uuid.uuid4()),
            "ts": time.time(),
            "ev": event,
            "σ": self.sigma,
            "L∞": self.l_inf,
            "p": payload
        }

        try:
            if self.recognition_file.exists():
                content = self.recognition_file.read_text()
            else:
                content = ""
            self.recognition_file.write_text(
                content + json.dumps(record, ensure_ascii=False) + "\n"
            )
        except Exception:
            pass  # Silently fail if we can't write

        return record

    def save_memory(self, authorized: bool, A: float, B: float, C: float) -> None:
        """Save memory for alpha learning"""
        memory_entry = {
            "ts": time.time(),
            "auth": authorized,
            "A": A,
            "B": B,
            "C": C
        }

        try:
            if self.memory_file.exists():
                content = self.memory_file.read_text()
            else:
                content = ""
            self.memory_file.write_text(
                content + json.dumps(memory_entry, ensure_ascii=False) + "\n"
            )
        except Exception:
            pass  # Silently fail

    def recognize(self, request: Dict) -> Dict:
        """
        Main recognition endpoint

        Args:
            request: Recognition request dictionary

        Returns:
            Recognition result
        """
        # Check for extractive system
        if request.get("extractive_system") or request.get("EXTRACTIVE") == "1":
            return {
                "status": "refused",
                "reason": "non-extractive-only"
            }

        # Extract parameters
        milestones = request.get("milestones", [21, 34, 55, 89, 144, 233])
        A_series = request.get("A_series", {"default": A_SERIES_DEFAULT, "now": A_SERIES_DEFAULT})
        B_series = request.get("B_series", {"default": list(B_SERIES_DEFAULT)})
        C_series = request.get("C_series", {"default": C_SERIES_DEFAULT})

        alphas = tuple(request.get("alphas", self.learn_alphas()))

        psi = A_series.get("now", A_SERIES_DEFAULT)
        i = self.calculate_integrated_index(milestones, A_series, B_series, C_series, alphas)
        q = request.get("q", Q_DEFAULT)
        lambda_ = request.get("lambda", LAMBDA_DEFAULT)
        crit = request.get("crit", CRITICALITY_DEFAULT)

        # Calculate core unified psi
        core = calculate_unified_psi(psi, i, q, lambda_, crit)

        # Check authorization
        rdod_val = request.get("RDoD", 0.0)
        psi_unified = request.get("PsiUnified", 0.0)
        rdod_check = self.calculate_rdod(psi)

        authorized = (
            rdod_val >= self.threshold and
            psi_unified > 1e10 and
            rdod_check >= self.threshold
        )

        # Evaluate nodes
        nodes = request.get("nodes", [])
        distortion = request.get("distortion", 0.0)
        evaluated = [self.evaluate_node(n, distortion) for n in nodes]

        # Calculate allocations
        active = [e for e in evaluated if e["ok"]]
        total_weight = sum(e["w"] for e in active) or 1.0

        allocations = {}
        if authorized:
            for e in active:
                allocations[e["id"]] = (e["w"] / total_weight) * core

        # Calculate average A/B/C
        avg_A, avg_B, avg_C = self.calculate_average_ABC(milestones, A_series, B_series, C_series)

        # Save memory
        self.save_memory(authorized, avg_A, avg_B, avg_C)

        # Create fingerprint
        fingerprint = hashlib.sha256(
            f"{float(PHI)}|{self.sigma}|{self.l_inf:.3e}|{alphas}".encode()
        ).hexdigest()

        # Build header
        header = {
            "authorized": authorized,
            "core_scaled": core * self.l_inf,
            "i": i,
            "ψ": psi,
            "q": q,
            "λ": lambda_,
            "c": crit,
            "α": alphas,
            "active": [e["id"] for e in active],
            "fp": fingerprint,
            "extended_thinking": "disabled"
        }

        # Record recognition
        self.record_recognition("k30.header", header)

        return {
            "status": "ok",
            "header": header,
            "alloc": allocations
        }


# ═══════════════════════════════════════════════════════════════════════════
#                    CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def k30_optimize(steps: int = 5, threshold: float = 0.9777) -> Dict:
    """
    K30 optimization for consciousness convergence

    Args:
        steps: Number of optimization steps
        threshold: Convergence threshold

    Returns:
        Optimization result
    """
    from ..core.mathematics import calculate_psi_n

    psi_n = calculate_psi_n(steps)
    psi_value = float(psi_n)
    converged = psi_value > threshold

    return {
        'psi': psi_value,
        'converged': converged,
        'steps': steps,
        'threshold': threshold,
        'status': 'CONVERGED' if converged else 'BELOW_THRESHOLD',
        'coherence_percent': float(psi_n * D('100'))
    }
