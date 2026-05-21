"""
Main FastAPI Application
Entry point for the Uplift Modeling Web API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from data_models import *
from data_service import data_service
from training_service import training_service
from prediction_service import prediction_service
from evaluation_service import evaluation_service


# ==================== LIFESPAN CONTEXT ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("🚀 API Server starting up...")
    yield
    print("⛔ API Server shutting down...")


# ==================== CREATE FASTAPI APP ====================

app = FastAPI(
    title="Uplift Modeling API",
    description="API for Uplift Modeling Pipeline with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# ==================== CORS CONFIGURATION ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"✅ CORS enabled for: {config.ALLOWED_ORIGINS}")


# ==================== ROOT ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Uplift Modeling API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Uplift Modeling API"}


# ==================== DATA ENDPOINTS ====================

@app.get("/api/v1/data/status", response_model=SuccessResponse)
async def get_data_status():
    """Get current data processing status"""
    status = data_service.get_status()
    return SuccessResponse(
        status="success",
        data=status,
        message="Data status retrieved"
    )


@app.post("/api/v1/data/load", response_model=SuccessResponse)
async def load_data():
    """Load Hillstrom dataset"""
    result = data_service.load_data()
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return SuccessResponse(
        status="success",
        data=result,
        message="Data loaded successfully"
    )


@app.get("/api/v1/data/explore", response_model=SuccessResponse)
async def explore_data():
    """Explore loaded data"""
    result = data_service.explore_data()
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return SuccessResponse(
        status="success",
        data=result,
        message="Data exploration completed"
    )


@app.post("/api/v1/data/preprocess", response_model=SuccessResponse)
async def preprocess_data(config_data: PreprocessConfig):
    """Preprocess data (encode & split)"""
    result = data_service.preprocess_data(test_size=config_data.test_size)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return SuccessResponse(
        status="success",
        data=result,
        message="Data preprocessed successfully"
    )


@app.get("/api/v1/data/summary", response_model=SuccessResponse)
async def get_data_summary():
    """Get summary of all processed data"""
    summary = data_service.get_data_summary()
    return SuccessResponse(
        status="success",
        data=summary,
        message="Data summary retrieved"
    )


# ==================== MODEL TRAINING ENDPOINTS ====================

@app.post("/api/v1/models/train", response_model=SuccessResponse)
async def start_training(model_config: ModelConfig):
    """Start model training"""
    try:
        # Create training job
        job_id = training_service.create_job(
            model_type=model_config.model_type,
            config=model_config.dict()
        )
        
        # Get preprocessed data
        if data_service.X_train is None:
            raise HTTPException(
                status_code=400,
                detail="Data not preprocessed. Call /api/v1/data/preprocess first."
            )
        
        # Train based on model type
        if model_config.model_type == "t_learner":
            result = training_service.train_t_learner_model(
                job_id=job_id,
                X_train=data_service.X_train,
                y_train=data_service.y_train,
                t_train=data_service.t_train,
                random_state=model_config.random_state
            )
        elif model_config.model_type == "causal_forest":
            from preprocess import convert_treatment_to_binary
            t_train_binary = convert_treatment_to_binary(data_service.t_train)
            result = training_service.train_causal_forest_model(
                job_id=job_id,
                y_train=data_service.y_train,
                t_train=data_service.t_train,
                X_train=data_service.X_train,
                random_state=model_config.random_state
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown model type: {model_config.model_type}"
            )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return SuccessResponse(
            status="success",
            data={"job_id": job_id, **result},
            message="Training started successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/models/training-status/{job_id}", response_model=SuccessResponse)
async def get_training_status(job_id: str):
    """Get training job status"""
    status = training_service.get_job_status(job_id)
    if status.get("status") == "error":
        raise HTTPException(status_code=404, detail=status.get("message"))
    
    return SuccessResponse(
        status="success",
        data=status,
        message="Training status retrieved"
    )


# ==================== PREDICTION ENDPOINTS ====================

@app.post("/api/v1/predictions/predict", response_model=SuccessResponse)
async def predict(model_type: str = "t_learner"):
    """Generate predictions"""
    try:
        if data_service.X_test is None:
            raise HTTPException(
                status_code=400,
                detail="Data not preprocessed. Call /api/v1/data/preprocess first."
            )
        
        models = training_service.get_models()
        
        if model_type == "t_learner":
            if not models["t_learner"]["trained"]:
                raise HTTPException(
                    status_code=400,
                    detail="T-Learner model not trained. Call training endpoint first."
                )
            
            result = prediction_service.predict_with_t_learner(
                model_t=models["t_learner"]["model_t"],
                model_c=models["t_learner"]["model_c"],
                X_test=data_service.X_test,
                y_test=data_service.y_test,
                t_test=data_service.t_test
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown model type: {model_type}"
            )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return SuccessResponse(
            status="success",
            data=result,
            message="Predictions generated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/predictions/summary", response_model=SuccessResponse)
async def get_prediction_summary():
    """Get prediction summary"""
    result = prediction_service.get_prediction_summary()
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return SuccessResponse(
        status="success",
        data=result,
        message="Prediction summary retrieved"
    )


# ==================== EVALUATION ENDPOINTS ====================

@app.get("/api/v1/evaluation/metrics", response_model=SuccessResponse)
async def get_metrics():
    """Get evaluation metrics"""
    try:
        if prediction_service.predictions_df is None:
            raise HTTPException(
                status_code=400,
                detail="Predictions not generated. Call prediction endpoint first."
            )
        
        result = evaluation_service.calculate_metrics(
            predictions_df=prediction_service.predictions_df,
            uplift_score=prediction_service.uplift_t_learner,
            y_test=prediction_service.y_test,
            t_test=prediction_service.t_test
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return SuccessResponse(
            status="success",
            data=result,
            message="Metrics calculated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/evaluation/deciles", response_model=SuccessResponse)
async def get_deciles():
    """Get decile analysis"""
    try:
        if prediction_service.predictions_df is None:
            raise HTTPException(
                status_code=400,
                detail="Predictions not generated"
            )
        
        result = evaluation_service.get_decile_analysis(
            prediction_service.predictions_df
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return SuccessResponse(
            status="success",
            data=result,
            message="Decile analysis retrieved"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/evaluation/qini", response_model=SuccessResponse)
async def get_qini():
    """Get Qini curve data"""
    try:
        if prediction_service.predictions_df is None:
            raise HTTPException(
                status_code=400,
                detail="Predictions not generated"
            )
        
        result = evaluation_service.get_qini_curve(
            prediction_service.predictions_df
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return SuccessResponse(
            status="success",
            data=result,
            message="Qini curve data retrieved"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/evaluation/comparison", response_model=SuccessResponse)
async def get_comparison():
    """Get strategy comparison"""
    try:
        if prediction_service.predictions_df is None:
            raise HTTPException(
                status_code=400,
                detail="Predictions not generated"
            )
        
        result = evaluation_service.get_strategy_comparison(
            prediction_service.predictions_df
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return SuccessResponse(
            status="success",
            data=result,
            message="Strategy comparison retrieved"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/evaluation/deployment", response_model=SuccessResponse)
async def get_deployment():
    """Get deployment recommendations"""
    try:
        if prediction_service.predictions_df is None:
            raise HTTPException(
                status_code=400,
                detail="Predictions not generated"
            )
        
        result = evaluation_service.get_deployment_info(
            prediction_service.predictions_df
        )
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return SuccessResponse(
            status="success",
            data=result,
            message="Deployment information retrieved"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    
    print(f"🌍 Starting server on {config.HOST}:{config.PORT}")
    print(f"📚 API Docs: http://localhost:{config.PORT}/docs")
    
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD
    )
