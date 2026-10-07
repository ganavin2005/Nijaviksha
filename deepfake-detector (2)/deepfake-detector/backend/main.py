import os
import random
import time
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="DeepScan Engine API", description="Backend for Deepfake Detection System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "DeepScan Engine Online"}

@app.post("/api/v1/analyze/media")
async def analyze_media_v1(file: UploadFile = File(...)):
    """
    Unified endpoint for scanning media payloads.
    Simulates advanced AI inference delays and returns deterministic results.
    """
    time.sleep(2.5) # Simulate heavy GPU inference
    
    filename = file.filename.lower()
    
    # Deterministic mock logic based on filename hints
    if 'real' in filename:
        score = random.uniform(85.0, 99.9)
        verdict = "AUTHENTIC"
        flags = []
    elif 'fake' in filename:
        score = random.uniform(5.0, 30.0)
        verdict = "AI_GENERATED"
        flags = random.sample(["temporal_inconsistency", "spectral_anomalies", "audio_desync", "facial_warp"], k=2)
    else:
        # Default randomizer if no 'real' or 'fake' keyword
        score = random.uniform(0.0, 100.0)
        verdict = "AUTHENTIC" if score > 50 else "AI_GENERATED"
        flags = random.sample(["temporal_inconsistency", "spectral_anomalies", "audio_desync", "facial_warp"], k=random.randint(1,3)) if score < 50 else []
        
    return JSONResponse({
        "status": "success",
        "filename": file.filename,
        "analysis": {
            "authenticity_score": round(score, 1),
            "verdict": verdict,
            "flags": flags
        }
    })

@app.get("/api/v1/vip/scan")
async def scan_vip_traffic():
    """
    Simulates a live security intercept on a VIP's active communication line.
    Usually returns safe/verified, but occasionally simulates a voice clone attack.
    """
    # 15% chance of detecting a deepfake voice clone
    is_threat = random.random() < 0.15
    
    if is_threat:
        auth_score = random.uniform(5.0, 30.0)
        risk_score = random.uniform(85.0, 99.0)
        status = "DEEPFAKE DETECTED"
    else:
        auth_score = random.uniform(92.0, 99.9)
        risk_score = random.uniform(0.1, 5.0)
        status = "AUTHENTIC"
        
    return JSONResponse({
        "status": "success",
        "data": {
            "authenticity_score": round(auth_score, 1),
            "artifact_risk": round(risk_score, 1),
            "verdict": status
        }
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
