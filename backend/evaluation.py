"""Model Evaluation Module"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklift.metrics import uplift_at_k


def create_decile_analysis(df, uplift_col_name='uplift'):
    """Analyze uplift performance by deciles"""
    df_sorted = df.sort_values(by=uplift_col_name, ascending=False).reset_index(drop=True)
    
    df_sorted['decile'] = pd.qcut(
        df_sorted[uplift_col_name],
        q=10,
        labels=False,
        duplicates='drop'
    )
    
    uplift_ranking = []
    for decile in sorted(df_sorted['decile'].unique()):
        decile_df = df_sorted[df_sorted['decile'] == decile]
        
        treated_conversions = decile_df[
            (decile_df['actual_treatment'] != 'No E-Mail') & (decile_df['actual_target'] == 1)
        ].shape[0]
        treated_total = decile_df[decile_df['actual_treatment'] != 'No E-Mail'].shape[0]
        conv_rate_treated = treated_conversions / treated_total if treated_total > 0 else 0
        
        control_conversions = decile_df[
            (decile_df['actual_treatment'] == 'No E-Mail') & (decile_df['actual_target'] == 1)
        ].shape[0]
        control_total = decile_df[decile_df['actual_treatment'] == 'No E-Mail'].shape[0]
        conv_rate_control = control_conversions / control_total if control_total > 0 else 0
        
        actual_uplift = conv_rate_treated - conv_rate_control
        
        uplift_ranking.append({
            'Decile': decile,
            'Tỷ lệ chuyển đổi (Điều trị)': conv_rate_treated,
            'Tỷ lệ chuyển đổi (Kiểm soát)': conv_rate_control,
            'Uplift thực tế': actual_uplift,
            'Số lượng khách hàng': float(decile_df.shape[0])
        })
    
    return pd.DataFrame(uplift_ranking), df_sorted


def calculate_qini_curve_data(df, uplift_col_name):
    """Calculate Qini curve data for visualization"""
    df_sorted = df.sort_values(by=uplift_col_name, ascending=False).reset_index(drop=True)
    
    if 'is_treated' not in df_sorted.columns:
        df_sorted['is_treated'] = (df_sorted['actual_treatment'] != 'No E-Mail').astype(int)
    
    N_treated_total = df_sorted['is_treated'].sum()
    N_control_total = (1 - df_sorted['is_treated']).sum()
    
    cumulative_treated_conversions = []
    cumulative_control_conversions = []
    cumulative_customers = []
    
    cum_treated_conv = 0
    cum_control_conv = 0
    cum_cust = 0
    
    for index, row in df_sorted.iterrows():
        if row['is_treated'] == 1:
            cum_treated_conv += row['actual_target']
        else:
            cum_control_conv += row['actual_target']
        cum_cust += 1
        
        cumulative_treated_conversions.append(cum_treated_conv)
        cumulative_control_conversions.append(cum_control_conv)
        cumulative_customers.append(cum_cust)
    
    cumulative_treated_conversions = np.array(cumulative_treated_conversions)
    cumulative_control_conversions = np.array(cumulative_control_conversions)
    cumulative_customers = np.array(cumulative_customers)
    
    if N_control_total > 0:
        cumulative_uplift_model = cumulative_treated_conversions - \
                                  (cumulative_control_conversions * (N_treated_total / N_control_total))
    else:
        cumulative_uplift_model = cumulative_treated_conversions
    
    overall_conv_rate_treated = df_sorted[df_sorted['is_treated'] == 1]['actual_target'].mean()
    overall_conv_rate_control = df_sorted[df_sorted['is_treated'] == 0]['actual_target'].mean()
    overall_average_uplift = overall_conv_rate_treated - overall_conv_rate_control
    
    cumulative_uplift_random = cumulative_customers * \
                               (N_treated_total / (N_treated_total + N_control_total)) * \
                               overall_average_uplift
    
    return (
    cumulative_customers,
    cumulative_uplift_model,
    cumulative_uplift_random,
    float(overall_average_uplift)
)


def calculate_uplift_at_k(y_test, uplift_score, treatment_binary, k_percent):
    """Calculate Uplift@K metric"""
    uplift_k = uplift_at_k(
        y_true=y_test,
        uplift=uplift_score,
        treatment=treatment_binary,
        k=k_percent,
        strategy='overall'
    )
    return uplift_k


def calculate_qini_coefficient(cumulative_customers, cumulative_uplift_model, cumulative_uplift_random):
    """Calculate Qini coefficient and related metrics"""
    area_model = np.trapz(cumulative_uplift_model, cumulative_customers)
    area_random = np.trapz(cumulative_uplift_random, cumulative_customers)
    
    if area_random != 0 and area_model != 0:
        qini_coefficient = (area_model - area_random) / area_model
    else:
        qini_coefficient = 0
    
    return float(area_model), float(area_random), float(qini_coefficient)


def compare_strategies(df_sorted, margin=10, cost_email=1):
    """Compare economic gain across different strategies"""
    total_customers = len(df_sorted)
    
    overall_conv_rate_treated = df_sorted[df_sorted['is_treated'] == 1]['actual_target'].mean()
    overall_conv_rate_control = df_sorted[df_sorted['is_treated'] == 0]['actual_target'].mean()
    
    incremental_conversions_all = total_customers * (overall_conv_rate_treated - overall_conv_rate_control)
    gross_profit_all = incremental_conversions_all * margin
    total_cost_all = total_customers * cost_email
    net_gain_all = gross_profit_all - total_cost_all
    
    num_random_target = df_sorted['is_treated'].sum()
    incremental_conversions_random = num_random_target * (overall_conv_rate_treated - overall_conv_rate_control)
    gross_profit_random = incremental_conversions_random * margin
    total_cost_random = num_random_target * cost_email
    net_gain_random = gross_profit_random - total_cost_random
    
    net_gain_uplift = df_sorted['net_economic_gain'].sum()
    
    comparison_df = pd.DataFrame({
        'Strategy': ['Send to All (Adj.)', 'Random Targeting (Adj.)', 'Uplift Targeting'],
        'Net Economic Gain': [net_gain_all, net_gain_random, net_gain_uplift]
    })
    
    return comparison_df


def create_deployment_report(df_sorted):
    """Create deployment recommendations"""
    deployment_df = df_sorted.copy()
    deployment_df['action'] = deployment_df['net_economic_gain'].apply(
        lambda x: 'Send Mail' if x > 0 else 'Ignore'
    )
    
    send_mail_count = (deployment_df['action'] == 'Send Mail').sum()
    ignore_count = (deployment_df['action'] == 'Ignore').sum()
    
    return deployment_df, int(send_mail_count), int(ignore_count)