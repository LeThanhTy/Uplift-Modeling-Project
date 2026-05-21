"""Model Training Module"""

from xgboost import XGBClassifier
from econml.dml import CausalForestDML
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier


def train_t_learner(X_train_treated, y_train_treated, X_train_control, y_train_control, random_state=42):
    """Train T-Learner models (separate models for treated and control groups)"""
    model_t = XGBClassifier(random_state=random_state)
    model_t.fit(X_train_treated, y_train_treated)
    
    model_c = XGBClassifier(random_state=random_state)
    model_c.fit(X_train_control, y_train_control)
    
    print("Hoàn thành huấn luyện T-Learner (XGBoost).")
    return model_t, model_c


def train_causal_forest_dml(y_train, t_train_binary, X_train, random_state=42):
    """Train CausalForestDML model for causal effect estimation"""
    model_y = GradientBoostingRegressor(
        n_estimators=100, max_depth=4, min_samples_leaf=5, random_state=random_state
    )
    model_t = GradientBoostingRegressor(
        n_estimators=100, max_depth=4, min_samples_leaf=5, random_state=random_state
    )
    
    cf_dml = CausalForestDML(
        model_y=model_y,
        model_t=model_t,
        n_estimators=1000,
        min_samples_leaf=10,
        max_depth=10,
        random_state=random_state
    )
    
    cf_dml.fit(y_train, t_train_binary, X=X_train)
    
    print("Hoàn thành huấn luyện và dự đoán CausalForestDML.")
    return cf_dml