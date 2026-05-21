"""Prediction Module"""

import pandas as pd
import numpy as np


def predict_t_learner(model_t, model_c, X_test):
    """Generate uplift predictions using T-Learner"""
    p_t = model_t.predict_proba(X_test)[:, 1]
    p_c = model_c.predict_proba(X_test)[:, 1]
    uplift_score = p_t - p_c
    return uplift_score


def predict_causal_forest_dml(cf_dml, X_test):
    """Generate uplift predictions using CausalForestDML"""
    uplift_score_cf_dml = cf_dml.effect(X_test).flatten()
    return uplift_score_cf_dml


def create_prediction_dataframe(X_test, y_test, t_test, uplift_score_t_learner, 
                                uplift_score_cf_dml):
    """Create a comprehensive DataFrame with predictions and actual values"""
    uplift_results_df = X_test.copy()
    uplift_results_df['actual_target'] = y_test
    uplift_results_df['actual_treatment'] = t_test
    uplift_results_df['uplift_t_learner'] = uplift_score_t_learner
    uplift_results_df['uplift_causal_forest_dml'] = uplift_score_cf_dml
    
    return uplift_results_df


def add_economic_features(df, uplift_col_name='uplift', margin=10, cost_email=1):
    """Add economic gain calculations to the prediction dataframe"""
    df = df.copy()
    df['economic_gain'] = df[uplift_col_name] * margin - cost_email
    df['net_economic_gain'] = df['economic_gain'].apply(lambda x: max(0, x))
    
    return df