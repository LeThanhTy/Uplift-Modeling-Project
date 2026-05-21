"""
Prediction Service - Wrapper around predict module
Handles prediction generation
"""

import sys
import os
from typing import Dict, Any, List
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from predict import (
    predict_t_learner as predict_t_learner_func,
    predict_causal_forest_dml as predict_causal_forest_dml_func,
    create_prediction_dataframe,
    add_economic_features
)


class PredictionService:
    """Service for prediction operations"""
    
    def __init__(self):
        """Initialize prediction service"""
        self.X_test = None
        self.y_test = None
        self.t_test = None
        self.uplift_t_learner = None
        self.uplift_cf_dml = None
        self.predictions_df = None
    
    def predict_with_t_learner(
        self,
        model_t,
        model_c,
        X_test,
        y_test,
        t_test,
        margin: float = 10,
        cost_email: float = 1
    ) -> Dict[str, Any]:
        """
        Generate predictions using T-Learner
        Args:
            model_t: Treated group model
            model_c: Control group model
            X_test: Test features
            y_test: Test target
            t_test: Test treatment
            margin: Profit per conversion
            cost_email: Cost per email
        Returns:
            dict with predictions
        """
        try:
            # Store data
            self.X_test = X_test
            self.y_test = y_test
            self.t_test = t_test
            
            # Generate predictions
            self.uplift_t_learner = predict_t_learner_func(
                model_t, model_c, X_test
            )
            
            # Create prediction dataframe
            self.predictions_df = create_prediction_dataframe(
                X_test, y_test, t_test,
                self.uplift_t_learner,
                np.zeros(len(X_test))  # Placeholder for CF predictions
            )
            
            # Add economic features
            self.predictions_df = add_economic_features(
                self.predictions_df,
                uplift_col_name='uplift_t_learner',
                margin=margin,
                cost_email=cost_email
            )
            
            return {
                "status": "success",
                "predictions_count": len(self.uplift_t_learner),
                "uplift_mean": float(np.mean(self.uplift_t_learner)),
                "uplift_std": float(np.std(self.uplift_t_learner)),
                "uplift_min": float(np.min(self.uplift_t_learner)),
                "uplift_max": float(np.max(self.uplift_t_learner)),
                "message": "T-Learner predictions generated"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Prediction failed: {str(e)}"
            }
    
    def predict_with_causal_forest(
        self,
        cf_dml,
        X_test,
        y_test,
        t_test,
        margin: float = 10,
        cost_email: float = 1
    ) -> Dict[str, Any]:
        """
        Generate predictions using CausalForestDML
        Args:
            cf_dml: Causal forest model
            X_test: Test features
            y_test: Test target
            t_test: Test treatment
            margin: Profit per conversion
            cost_email: Cost per email
        Returns:
            dict with predictions
        """
        try:
            # Store data
            self.X_test = X_test
            self.y_test = y_test
            self.t_test = t_test
            
            # Generate predictions
            self.uplift_cf_dml = predict_causal_forest_dml_func(cf_dml, X_test)
            
            return {
                "status": "success",
                "predictions_count": len(self.uplift_cf_dml),
                "uplift_mean": float(np.mean(self.uplift_cf_dml)),
                "uplift_std": float(np.std(self.uplift_cf_dml)),
                "uplift_min": float(np.min(self.uplift_cf_dml)),
                "uplift_max": float(np.max(self.uplift_cf_dml)),
                "message": "CausalForestDML predictions generated"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Prediction failed: {str(e)}"
            }
    
    def get_prediction_summary(self) -> Dict[str, Any]:
        """
        Get summary of predictions
        Returns:
            dict with prediction summary
        """
        if self.predictions_df is None:
            return {
                "status": "error",
                "message": "No predictions generated yet"
            }
        
        return {
            "status": "success",
            "total_predictions": len(self.predictions_df),
            "positive_uplift": int((self.uplift_t_learner > 0).sum()),
            "negative_uplift": int((self.uplift_t_learner < 0).sum()),
            "customers_to_target": int(
                (self.predictions_df['net_economic_gain'] > 0).sum()
            ),
            "total_economic_gain": float(
                self.predictions_df['net_economic_gain'].sum()
            ),
            "message": "Prediction summary retrieved"
        }


# Global instance
prediction_service = PredictionService()
