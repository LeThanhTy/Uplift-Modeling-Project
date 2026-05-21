"""
Evaluation Service - Wrapper around evaluation module
Handles model evaluation and metrics calculation
"""

import sys
import os
from typing import Dict, Any, List
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation import (
    create_decile_analysis,
    calculate_qini_curve_data,
    calculate_uplift_at_k,
    calculate_qini_coefficient,
    compare_strategies,
    create_deployment_report
)
from preprocess import convert_treatment_to_binary


class EvaluationService:
    """Service for model evaluation"""
    
    def __init__(self):
        """Initialize evaluation service"""
        self.evaluation_results = {}
    
    def calculate_metrics(
        self,
        predictions_df,
        uplift_score,
        y_test,
        t_test,
        margin: float = 10,
        cost_email: float = 1
    ) -> Dict[str, Any]:
        """
        Calculate evaluation metrics
        Args:
            predictions_df: DataFrame with predictions
            uplift_score: Array of uplift scores
            y_test: Test targets
            t_test: Test treatments
            margin: Profit per conversion
            cost_email: Cost per email
        Returns:
            dict with metrics
        """
        try:
            # Convert treatment to binary
            treatment_binary = convert_treatment_to_binary(t_test)
            
            # Calculate Uplift@K
            uplift_at_10 = calculate_uplift_at_k(
                y_test, uplift_score, treatment_binary, 0.10
            )
            uplift_at_20 = calculate_uplift_at_k(
                y_test, uplift_score, treatment_binary, 0.20
            )
            
            # Qini curve data
            customers, uplift_model, uplift_random, _ = calculate_qini_curve_data(
                predictions_df, 'uplift_t_learner'
            )
            
            # Qini coefficient
            area_model, area_random, qini_coeff = calculate_qini_coefficient(
                customers, uplift_model, uplift_random
            )
            
            # Deployment info
            deployment_df, send_mail_count, ignore_count = create_deployment_report(
                predictions_df
            )
            
            # Total economic gain
            total_gain = predictions_df['net_economic_gain'].sum()
            
            metrics = {
                "status": "success",
                "qini_coefficient": float(qini_coeff),
                "uplift_at_10": float(uplift_at_10),
                "uplift_at_20": float(uplift_at_20),
                "area_under_curve": float(area_model),
                "total_customers": int(predictions_df.shape[0]),
                "target_customers": int(send_mail_count),
                "ignore_customers": int(ignore_count),
                "net_economic_gain": float(total_gain),
                "message": "Metrics calculated successfully"
            }
            
            self.evaluation_results = metrics
            return metrics
        except Exception as e:
            return {
                "status": "error",
                "message": f"Metrics calculation failed: {str(e)}"
            }
    
    def get_decile_analysis(
        self,
        predictions_df
    ) -> Dict[str, Any]:
        """
        Get decile analysis
        Args:
            predictions_df: DataFrame with predictions
        Returns:
            dict with decile analysis
        """
        try:
            decile_df, df_sorted = create_decile_analysis(
                predictions_df, 'uplift_t_learner'
            )
            
            return {
                "status": "success",
                "deciles": [int(x) for x in decile_df['Decile'].tolist()],
                "uplift_values": [float(x) for x in decile_df['Uplift thực tế'].tolist()],
                "conv_rate_treated": [
                    float(x)
                    for x in decile_df['Tỷ lệ chuyển đổi (Điều trị)'].tolist()
                ],
                "conv_rate_control": [
                    float(x)
                    for x in decile_df['Tỷ lệ chuyển đổi (Kiểm soát)'].tolist()
                ],
                "customer_counts": [
                    int(x)
                    for x in decile_df['Số lượng khách hàng'].tolist()
                ],
                "message": "Decile analysis completed"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Decile analysis failed: {str(e)}"
            }
    
    def get_qini_curve(
        self,
        predictions_df
    ) -> Dict[str, Any]:
        """
        Get Qini curve data
        Args:
            predictions_df: DataFrame with predictions
        Returns:
            dict with Qini curve data
        """
        try:
            customers, uplift, random, _ = calculate_qini_curve_data(
                predictions_df, 'uplift_t_learner'
            )
            
            return {
                "status": "success",
                "customers": [float(x) for x in customers.tolist()],
                "uplift": [float(x) for x in uplift.tolist()],
                "random": [float(x) for x in random.tolist()],
                "message": "Qini curve data retrieved"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Qini curve calculation failed: {str(e)}"
            }
    
    def get_strategy_comparison(
        self,
        predictions_df,
        margin: float = 10,
        cost_email: float = 1
    ) -> Dict[str, Any]:
        """
        Compare different strategies
        Args:
            predictions_df: DataFrame with predictions
            margin: Profit per conversion
            cost_email: Cost per email
        Returns:
            dict with strategy comparison
        """
        try:
            # Add is_treated column if not exists
            if 'is_treated' not in predictions_df.columns:
                predictions_df['is_treated'] = (
                    predictions_df['actual_treatment'] != 'No E-Mail'
                ).astype(int)
            
            comparison_df = compare_strategies(
                predictions_df, margin=margin, cost_email=cost_email
            )
            
            return {
                "status": "success",
                "strategies": comparison_df['Strategy'].tolist(),
                "gains": [
                    float(x)
                    for x in comparison_df['Net Economic Gain'].tolist()
                ],
                "message": "Strategy comparison completed"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Strategy comparison failed: {str(e)}"
            }
    
    def get_deployment_info(
        self,
        predictions_df
    ) -> Dict[str, Any]:
        """
        Get deployment recommendations
        Args:
            predictions_df: DataFrame with predictions
        Returns:
            dict with deployment info
        """
        try:
            deployment_df, send_mail, ignore = create_deployment_report(
                predictions_df
            )
            
            # Get top customers to target
            target_df = deployment_df[
                deployment_df['action'] == 'Send Mail'
            ].nlargest(10, 'net_economic_gain')
            
            return {
                "status": "success",
                "send_mail_count": int(send_mail),
                "ignore_count": int(ignore),
                "top_targets": [float(x) for x in target_df['net_economic_gain'].tolist()[:10]],
                "message": "Deployment information retrieved"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Deployment info retrieval failed: {str(e)}"
            }
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all calculated metrics
        Returns:
            dict with all metrics
        """
        return self.evaluation_results


# Global instance
evaluation_service = EvaluationService()
