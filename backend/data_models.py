"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel
from typing import List, Dict, Optional


# ==================== DATA MODELS ====================

class DataStatusResponse(BaseModel):
    """Response for data status check"""
    loaded: bool
    preprocessed: bool
    split: bool


class DataLoadResponse(BaseModel):
    """Response after loading data"""
    rows: int
    columns: int
    features: List[str]
    status: str


class DataExploreResponse(BaseModel):
    """Response for data exploration"""
    X_shape: tuple
    y_distribution: Dict
    t_distribution: Dict
    status: str


class PreprocessConfig(BaseModel):
    """Configuration for data preprocessing"""
    test_size: float = 0.2
    random_state: int = 42


class PreprocessResponse(BaseModel):
    """Response after preprocessing"""
    train_size: int
    test_size: int
    features: List[str]
    status: str


# ==================== MODEL TRAINING MODELS ====================

class ModelConfig(BaseModel):
    """Configuration for model training"""
    model_type: str  # "t_learner" or "causal_forest"
    random_state: int = 42


class TrainingJobResponse(BaseModel):
    """Response when starting training"""
    job_id: str
    status: str  # "started"
    message: str


class TrainingStatusResponse(BaseModel):
    """Response for training status"""
    job_id: str
    status: str  # "running", "completed", "failed"
    progress: float  # 0-100
    message: str


# ==================== PREDICTION MODELS ====================

class PredictionRequest(BaseModel):
    """Request for predictions"""
    data: List[List[float]]


class PredictionResponse(BaseModel):
    """Response with predictions"""
    predictions: List[float]
    status: str


# ==================== EVALUATION MODELS ====================

class MetricsResponse(BaseModel):
    """Response with evaluation metrics"""
    qini_coefficient: float
    uplift_at_10: float
    uplift_at_20: float
    total_customers: int
    target_customers: int
    net_economic_gain: float
    status: str


class QiniCurveResponse(BaseModel):
    """Response with Qini curve data"""
    customers: List[float]
    uplift: List[float]
    random: List[float]
    status: str


class DecileResponse(BaseModel):
    """Response with decile analysis"""
    deciles: List[int]
    uplift_values: List[float]
    conversion_rates_treated: List[float]
    conversion_rates_control: List[float]
    status: str


class StrategyComparisonResponse(BaseModel):
    """Response with strategy comparison"""
    strategies: List[str]
    gains: List[float]
    status: str


class DeploymentResponse(BaseModel):
    """Response with deployment recommendations"""
    send_mail_count: int
    ignore_count: int
    expected_gain: float
    status: str


# ==================== ERROR RESPONSE ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    status: str
    error: str
    detail: str


# ==================== GENERIC RESPONSE ====================

class SuccessResponse(BaseModel):
    """Generic success response"""
    status: str
    data: Dict
    message: str
