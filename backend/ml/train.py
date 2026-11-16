"""Train model dự đoán band overall từ CSV bài luận đã chấm.

Ví dụ:
    python -m ml.train --csv data/ielts_essays.csv --text-col Essay --label-col Overall

CSV cần ít nhất 2 cột: nội dung bài (text) và band (float 0-9).
Gợi ý dữ liệu: Kaggle "IELTS Writing Scored Essays Dataset".
"""
import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler

from .features import HandcraftedFeatures
from .scorer import round_band

DEFAULT_OUT = Path(__file__).parent / "artifacts" / "band_model.joblib"


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("features", FeatureUnion([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                                      max_features=20000, sublinear_tf=True)),
            ("hand", Pipeline([
                ("extract", HandcraftedFeatures()),
                ("scale", StandardScaler()),
            ])),
        ])),
        ("reg", Ridge(alpha=1.0)),
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--text-col", default="Essay")
    ap.add_argument("--label-col", default="Overall")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    df = pd.read_csv(args.csv).dropna(subset=[args.text_col, args.label_col])
    X = df[args.text_col].astype(str).tolist()
    y = df[args.label_col].astype(float).to_numpy()
    print(f"Loaded {len(X)} essays")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    pipe = build_pipeline()
    pipe.fit(X_train, y_train)

    pred = np.array([round_band(p) for p in pipe.predict(X_test)])
    mae = mean_absolute_error(y_test, pred)
    within_half = float(np.mean(np.abs(pred - y_test) <= 0.5))
    print(f"MAE: {mae:.3f} | lệch <= 0.5 band: {within_half:.1%}")

    pipe.fit(X, y)  # train lại trên toàn bộ dữ liệu trước khi lưu
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, args.out)
    print(f"Saved model -> {args.out}")


if __name__ == "__main__":
    main()
