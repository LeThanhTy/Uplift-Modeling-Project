"""Data Preprocessing Module"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklift.datasets import fetch_hillstrom


def load_data():
    """Load Hillstrom dataset from sklift"""
    data = fetch_hillstrom()
    X, y, t = data['data'], data['target'], data['treatment']
    return X, y, t


def explore_data(X, y, t):
    """Print data exploration statistics"""
    print("5 dòng đầu tiên của X:")
    print(X.head())
    
    print("\nKiểu dữ liệu của các cột trong X:")
    print(X.info())
    
    print("\nPhân phối của biến mục tiêu (y):")
    print(y.value_counts())
    
    print("\nPhân phối của biến điều trị (t):")
    print(t.value_counts())


def encode_features(X):
    """Apply One-Hot Encoding to categorical features"""
    categorical_cols = X.select_dtypes(include=['object']).columns
    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    
    print("\n5 dòng đầu tiên của X sau khi mã hóa:")
    print(X_encoded.head())
    
    print("\nSố lượng cột của X trước và sau mã hóa:")
    print(f"Trước mã hóa: {X.shape[1]} cột")
    print(f"Sau mã hóa: {X_encoded.shape[1]} cột")
    
    return X_encoded


def split_data(X, y, t, test_size=0.2, random_state=42):
    """Split data into train and test sets with stratification"""
    X_train, X_test, y_train, y_test, t_train, t_test = train_test_split(
        X, y, t, test_size=test_size, stratify=t, random_state=random_state
    )
    return X_train, X_test, y_train, y_test, t_train, t_test


def prepare_treatment_groups(X_train, y_train, t_train):
    """Separate treated and control groups for training"""
    treated_mask = (t_train == 'Womens E-Mail') | (t_train == 'Mens E-Mail')
    control_mask = (t_train == 'No E-Mail')
    
    X_train_treated = X_train[treated_mask]
    y_train_treated = y_train[treated_mask]
    X_train_control = X_train[control_mask]
    y_train_control = y_train[control_mask]
    
    return X_train_treated, y_train_treated, X_train_control, y_train_control


def convert_treatment_to_binary(t):
    """Convert treatment to binary format (1: Treated, 0: Control)"""
    return (t != 'No E-Mail').astype(int)