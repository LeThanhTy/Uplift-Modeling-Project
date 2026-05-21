"""
Data Service - Wrapper around preprocess module
Handles data loading, exploration, and preprocessing
"""

import sys
import os

# Add parent directory to path so we can import preprocess module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocess import (
    load_data as preprocess_load_data,
    explore_data as preprocess_explore_data,
    encode_features as preprocess_encode_features,
    split_data as preprocess_split_data,
    prepare_treatment_groups,
    convert_treatment_to_binary
)

import pandas as pd
from typing import Tuple, Dict, Any


class DataService:
    """Service for data operations"""
    
    def __init__(self):
        """Initialize data service"""
        self.X = None
        self.y = None
        self.t = None
        self.X_encoded = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.t_train = None
        self.t_test = None
        self.features = None
    
    def load_data(self) -> Dict[str, Any]:
        """
        Load Hillstrom dataset
        Returns: dict with data info
        """
        try:
            self.X, self.y, self.t = preprocess_load_data()
            self.features = list(self.X.columns)
            
            return {
                "status": "success",
                "rows": len(self.X),
                "columns": self.X.shape[1],
                "data": self.X.head(20).to_dict(orient="records"),
                "features": self.features,
                "message": "Data loaded successfully"
            }
            
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to load data: {str(e)}"
            }
    
    def explore_data(self) -> Dict[str, Any]:
        """
        Explore data statistics
        Returns: dict with data exploration info
        """
        try:
            if self.X is None:
                return {
                    "status": "error",
                    "message": "Data not loaded. Call load_data() first."
                }
            
            return {
                "status": "success",
                "X_shape": [
                    int(self.X.shape[0]),
                    int(self.X.shape[1])
                ],
                "X_columns": [str(col) for col in self.X.columns.tolist()],
                "y_distribution": {
                    str(k): int(v)
                    for k, v in self.y.value_counts().to_dict().items()
                },
                "t_distribution": {
                    str(k): int(v)
                    for k, v in self.t.value_counts().to_dict().items()
                },
                "X_dtypes": {
                    str(col): str(dtype)
                    for col, dtype in self.X.dtypes.items()
                },
                
                "message": "Data exploration complete"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to explore data: {str(e)}"
            }
    
    def preprocess_data(self, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Encode features and split data
        Args: test_size (float): Proportion of test data
        Returns: dict with preprocessing info
        """
        try:
            if self.X is None:
                return {
                    "status": "error",
                    "message": "Data not loaded. Call load_data() first."
                }
            
            # Encode features
            self.X_encoded = preprocess_encode_features(self.X)
            
            # Split data
            (self.X_train, self.X_test, 
             self.y_train, self.y_test, 
             self.t_train, self.t_test) = preprocess_split_data(
                self.X_encoded, self.y, self.t,
                test_size=test_size
            )
            
            self.features = list(self.X_train.columns)
            
            return {
                "status": "success",
                "train_size": len(self.X_train),
                "test_size": len(self.X_test),
                "features": len(self.features),
                "feature_names": self.features,
                "message": "Data preprocessed successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to preprocess data: {str(e)}"
            }
    
    def get_status(self) -> Dict[str, bool]:
        """
        Get current data processing status
        Returns: dict with status flags
        """
        return {
            "loaded": self.X is not None,
            "encoded": self.X_encoded is not None,
            "split": self.X_train is not None
        }
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary of all loaded/processed data
        Returns: dict with data summary
        """
        summary = {
            "raw_data": {
                "loaded": self.X is not None,
                "rows": len(self.X) if self.X is not None else 0,
                "columns": self.X.shape[1] if self.X is not None else 0
            },
            "preprocessed_data": {
                "encoded": self.X_encoded is not None,
                "rows": len(self.X_encoded) if self.X_encoded is not None else 0,
                "columns": self.X_encoded.shape[1] if self.X_encoded is not None else 0
            },
            "split_data": {
                "split": self.X_train is not None,
                "train_rows": len(self.X_train) if self.X_train is not None else 0,
                "test_rows": len(self.X_test) if self.X_test is not None else 0
            }
        }
        return summary


# Global instance
data_service = DataService()
