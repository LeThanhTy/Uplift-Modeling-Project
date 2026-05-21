"""
Training Service - Wrapper around train module
Handles model training operations
"""

import sys
import os
import uuid
from typing import Dict, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from train import train_t_learner, train_causal_forest_dml
from preprocess import prepare_treatment_groups, convert_treatment_to_binary


class TrainingService:
    """Service for model training operations"""
    
    def __init__(self):
        """Initialize training service"""
        self.jobs = {}  # Store training job info
        self.models = {}  # Store trained models
        self.model_t = None
        self.model_c = None
        self.cf_dml = None
    
    def create_job(self, model_type: str, config: Dict[str, Any]) -> str:
        """
        Create a new training job
        Args:
            model_type: "t_learner" or "causal_forest"
            config: Model configuration dict
        Returns:
            job_id (str)
        """
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "id": job_id,
            "model_type": model_type,
            "config": config,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "progress": 0,
            "message": "Job created"
        }
        return job_id
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a training job
        Args:
            job_id: Job identifier
        Returns:
            dict with job status
        """
        if job_id not in self.jobs:
            return {
                "status": "error",
                "message": f"Job {job_id} not found"
            }
        return self.jobs[job_id]
    
    def train_t_learner_model(
        self, 
        job_id: str,
        X_train, 
        y_train, 
        t_train,
        random_state: int = 42
    ) -> Dict[str, Any]:
        """
        Train T-Learner model
        Args:
            job_id: Job identifier
            X_train: Training features
            y_train: Training target
            t_train: Training treatment
            random_state: Random seed
        Returns:
            dict with training result
        """
        try:
            if job_id not in self.jobs:
                return {
                    "status": "error",
                    "message": f"Job {job_id} not found"
                }
            
            # Update job status
            self.jobs[job_id]["status"] = "running"
            self.jobs[job_id]["progress"] = 10
            self.jobs[job_id]["message"] = "Preparing data..."
            
            # Prepare treatment groups
            X_train_treated, y_train_treated, X_train_control, y_train_control = \
                prepare_treatment_groups(X_train, y_train, t_train)
            
            self.jobs[job_id]["progress"] = 30
            self.jobs[job_id]["message"] = "Training models..."
            
            # Train models
            self.model_t, self.model_c = train_t_learner(
                X_train_treated, y_train_treated,
                X_train_control, y_train_control,
                random_state=random_state
            )
            
            self.jobs[job_id]["progress"] = 100
            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["message"] = "T-Learner training completed successfully"
            self.jobs[job_id]["model_type"] = "t_learner"
            
            return {
                "status": "success",
                "job_id": job_id,
                "message": "T-Learner training completed"
            }
        except Exception as e:
            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["message"] = str(e)
            return {
                "status": "error",
                "message": f"Training failed: {str(e)}"
            }
    
    def train_causal_forest_model(
        self,
        job_id: str,
        y_train,
        t_train,
        X_train,
        random_state: int = 42
    ) -> Dict[str, Any]:
        """
        Train CausalForestDML model
        Args:
            job_id: Job identifier
            y_train: Training target
            t_train: Training treatment
            X_train: Training features
            random_state: Random seed
        Returns:
            dict with training result
        """
        try:
            if job_id not in self.jobs:
                return {
                    "status": "error",
                    "message": f"Job {job_id} not found"
                }
            
            # Update job status
            self.jobs[job_id]["status"] = "running"
            self.jobs[job_id]["progress"] = 10
            self.jobs[job_id]["message"] = "Converting treatment to binary..."
            
            # Convert treatment to binary
            t_train_binary = convert_treatment_to_binary(t_train)
            
            self.jobs[job_id]["progress"] = 30
            self.jobs[job_id]["message"] = "Training CausalForestDML..."
            
            # Train model
            self.cf_dml = train_causal_forest_dml(
                y_train, t_train_binary, X_train,
                random_state=random_state
            )
            
            self.jobs[job_id]["progress"] = 100
            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["message"] = "CausalForestDML training completed successfully"
            self.jobs[job_id]["model_type"] = "causal_forest"
            
            return {
                "status": "success",
                "job_id": job_id,
                "message": "CausalForestDML training completed"
            }
        except Exception as e:
            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["message"] = str(e)
            return {
                "status": "error",
                "message": f"Training failed: {str(e)}"
            }
    
    def get_models(self) -> Dict[str, Any]:
        """
        Get trained models
        Returns:
            dict with model info
        """
        return {
            "t_learner": {
                "trained": self.model_t is not None and self.model_c is not None,
                "model_t": self.model_t,
                "model_c": self.model_c
            },
            "causal_forest": {
                "trained": self.cf_dml is not None,
                "model": self.cf_dml
            }
        }


# Global instance
training_service = TrainingService()
