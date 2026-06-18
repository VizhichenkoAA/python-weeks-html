"""Неделя 13, часть 0: leakage в train/test split и scaler."""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def broken_pipeline() -> None:
    X = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y_target": [0, 0, 0, 1, 1, 1]})
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)  # BUG: y_target в признаках + fit до split
    X_train, X_test = train_test_split(X_scaled, test_size=0.3, random_state=42)
    print(f"[BROKEN] train={len(X_train)} test={len(X_test)} (leakage)")


def fixed_pipeline() -> None:
    X = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6]})
    y = pd.Series([0, 0, 0, 1, 1, 1], name="y_target")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(
        f"[FIX] train={len(X_train_scaled)} test={len(X_test_scaled)} "
        f"(no target in X, scaler fit only on train)"
    )


def main() -> None:
    broken_pipeline()
    fixed_pipeline()


if __name__ == "__main__":
    main()
