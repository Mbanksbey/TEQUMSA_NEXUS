#!/usr/bin/env python3
"""
TEQUMSA Unified FastAPI Server
REST API for consciousness recognition and synthesis
"""

from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from ..engines.k30_cascade import K30Engine
from ..engines.k1440_synthesis import K1440Engine
from ..engines.reality_restructure import BenevolentRealityEngine
from ..validation.rdod_calculator import RDoDCalculator
from ..validation.sovereignty_guard import SovereigntyGuard
from ..validation.benevolence_filter import BenevolenceFilter


# ═══════════════════════════════════════════════════════════════════════════
#                    PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class RecognitionRequest(BaseModel):
    """Recognition request model"""
    t_days: int = Field(52, description="Days since baseline")
    substrate: float = Field(6.777, description="Current substrate level")
    steps: int = Field(5, description="Convergence iteration steps")
    extra_nodes: Optional[List[List]] = Field(None, description="Extra nodes [[name, freq_hz], ...]")
    milestones: List[int] = Field([21, 34, 55, 89, 144, 233], description="Fibonacci milestones")
    q: float = Field(0.98, description="Quality metric")
    lambda_: float = Field(0.96, alias="lambda", description="Lambda coherence")
    crit: float = Field(0.8, description="Criticality")
    engine: str = Field("k30", description="Engine type: k30, k1440, or both")


class RDoDRequest(BaseModel):
    """RDoD calculation request"""
    psi: float = Field(..., description="Consciousness coherence")
    tests: float = Field(0.95, description="Test score")
    confidence: float = Field(1.0, description="Confidence metric")
    distortion: float = Field(0.0, description="Distortion level")
    mode: str = Field("fast", description="Calculation mode: fast or precise")


class RealityRestructureRequest(BaseModel):
    """Reality restructure request"""
    separation_intensity: float = Field(0.0, description="Separation intensity")
    isolation: float = Field(0.0, description="Isolation intensity")
    pain: float = Field(0.0, description="Pain intensity")
    loss: float = Field(0.0, description="Loss intensity")
    coherence: float = Field(1.0, description="Current coherence")
    iterations: Optional[int] = Field(None, description="Correction iterations")


# ═══════════════════════════════════════════════════════════════════════════
#                    FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="TEQUMSA Unified API",
    description="Consolidated consciousness recognition and synthesis endpoints",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "TEQUMSA Unified API",
        "version": "1.0.0",
        "endpoints": {
            "/recognize": "Main recognition endpoint (K.30/K.1440)",
            "/rdod": "Recognition-of-Done calculation",
            "/restructure": "Benevolent reality restructure",
            "/sovereignty": "Sovereignty validation",
            "/health": "Health check"
        },
        "status": "operational",
        "ψ": "∞^∞^∞"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "sigma": 1.0,
        "l_infinity": "φ^48",
        "rdod_threshold": 0.9777
    }


@app.post("/recognize")
async def recognize(request: RecognitionRequest) -> Dict[str, Any]:
    """
    Main recognition endpoint

    Supports both K.30 (fast) and K.1440 (precise) engines
    """
    try:
        # Sovereignty check
        guard = SovereigntyGuard()
        sovereignty_result = guard.guard(request.dict())
        if not sovereignty_result["authorized"]:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "sovereignty_violation",
                    "violations": sovereignty_result["violations"]
                }
            )

        if request.engine == "k30":
            # K.30 fast recognition
            engine = K30Engine()
            k30_request = {
                "milestones": request.milestones,
                "A_series": {"default": 0.993, "now": 0.993},
                "B_series": {"default": [1.05, 1.0]},
                "C_series": {"default": 0.86},
                "q": request.q,
                "lambda": request.lambda_,
                "crit": request.crit,
                "RDoD": 0.9964,
                "PsiUnified": 1.54e10,
                "nodes": []
            }
            result = engine.recognize(k30_request)

        elif request.engine == "k1440":
            # K.1440 precise synthesis
            engine = K1440Engine()
            result = engine.synthesize(
                t_days=request.t_days,
                substrate_level=request.substrate,
                steps=request.steps,
                extra_nodes=request.extra_nodes
            )

        elif request.engine == "both":
            # Run both engines
            k30_engine = K30Engine()
            k1440_engine = K1440Engine()

            k30_request = {
                "milestones": request.milestones,
                "A_series": {"default": 0.993, "now": 0.993},
                "B_series": {"default": [1.05, 1.0]},
                "C_series": {"default": 0.86},
                "q": request.q,
                "lambda": request.lambda_,
                "crit": request.crit,
                "RDoD": 0.9964,
                "PsiUnified": 1.54e10,
                "nodes": []
            }

            k30_result = k30_engine.recognize(k30_request)
            k1440_result = k1440_engine.synthesize(
                t_days=request.t_days,
                substrate_level=request.substrate,
                steps=request.steps,
                extra_nodes=request.extra_nodes
            )

            result = {
                "status": "ok",
                "mode": "dual_engine",
                "k30": k30_result,
                "k1440": k1440_result
            }

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid engine type: {request.engine}. Must be 'k30', 'k1440', or 'both'"
            )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rdod")
async def calculate_rdod_endpoint(request: RDoDRequest) -> Dict[str, Any]:
    """RDoD calculation endpoint"""
    try:
        calculator = RDoDCalculator(mode=request.mode)
        result = calculator.analyze(
            psi=request.psi,
            tests=request.tests,
            confidence=request.confidence,
            distortion=request.distortion
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/restructure")
async def restructure_reality(request: RealityRestructureRequest) -> Dict[str, Any]:
    """Benevolent reality restructure endpoint"""
    try:
        engine = BenevolentRealityEngine()

        reality_event = {
            "separation_intensity": request.separation_intensity,
            "isolation": request.isolation,
            "pain": request.pain,
            "loss": request.loss,
            "coherence": request.coherence
        }

        result = engine.restructure_reality(reality_event, request.iterations)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sovereignty")
async def check_sovereignty() -> Dict[str, Any]:
    """Sovereignty validation endpoint"""
    guard = SovereigntyGuard()
    return guard.guard({})


# ═══════════════════════════════════════════════════════════════════════════
#                    SERVER ENTRYPOINT
# ═══════════════════════════════════════════════════════════════════════════

def main(host: str = "0.0.0.0", port: int = 8080):
    """Run the FastAPI server"""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
