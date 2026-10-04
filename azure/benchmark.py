"""Run the credit-card fraud benchmark on the Azure CPU VM."""
import argparse
import json
import platform
import statistics
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='creditcard.csv')
    parser.add_argument('--output', default='benchmark_result.json')
    args = parser.parse_args()
    start = time.perf_counter()
    data = pd.read_csv(args.data)
    load_seconds = time.perf_counter() - start
    if len(data) != 284807 or 'Class' not in data:
        raise ValueError('Expected the original 284,807-row Credit Card Fraud dataset')
    X = data.drop(columns='Class')
    y = data['Class']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)
    X_fit, X_valid, y_fit, y_valid = train_test_split(
        X_train, y_train, test_size=0.2, stratify=y_train, random_state=42)
    model = lgb.LGBMClassifier(
        n_estimators=1000, learning_rate=0.05, num_leaves=31,
        class_weight='balanced', random_state=42, n_jobs=2, verbosity=-1)
    start = time.perf_counter()
    model.fit(X_fit, y_fit, eval_set=[(X_valid, y_valid)], eval_metric='auc',
              callbacks=[lgb.early_stopping(50, first_metric_only=True), lgb.log_evaluation(50)])
    train_seconds = time.perf_counter() - start
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    one = X_test.iloc[:1]
    batch = X_test.iloc[:1000]
    model.predict_proba(one)
    model.predict_proba(batch)
    latencies = []
    for _ in range(100):
        start = time.perf_counter()
        model.predict_proba(one)
        latencies.append(time.perf_counter() - start)
    batch_times = []
    for _ in range(20):
        start = time.perf_counter()
        model.predict_proba(batch)
        batch_times.append(time.perf_counter() - start)
    result = {
        'dataset_rows': len(data), 'fraud_rows': int(y.sum()),
        'fit_rows': len(X_fit), 'validation_rows': len(X_valid), 'test_rows': len(X_test),
        'random_seed': 42, 'classification_threshold': 0.5,
        'load_data_seconds': load_seconds, 'training_seconds': train_seconds,
        'best_iteration': model.best_iteration_,
        'auc_roc': roc_auc_score(y_test, probabilities),
        'accuracy': accuracy_score(y_test, predictions),
        'f1_score': f1_score(y_test, predictions, zero_division=0),
        'precision': precision_score(y_test, predictions, zero_division=0),
        'recall': recall_score(y_test, predictions, zero_division=0),
        'inference_latency_1_row_ms': statistics.median(latencies) * 1000,
        'inference_latency_1_row_p95_ms': float(np.percentile(latencies, 95)) * 1000,
        'inference_throughput_1000_rows_per_second': 1000 / statistics.median(batch_times),
        'latency_repeats': 100, 'throughput_repeats': 20,
        'environment': {'python': platform.python_version(), 'lightgbm': lgb.__version__,
                        'sklearn': sklearn.__version__, 'machine': platform.machine(),
                        'threads': 2},
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    model.booster_.save_model('lightgbm_model.txt')


if __name__ == '__main__':
    main()
