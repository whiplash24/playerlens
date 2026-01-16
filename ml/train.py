from ml.feature_engineering import build_player_features
from ml.model import compute_impact_score

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.impute import SimpleImputer
import joblib
from pathlib import Path

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def train_and_save():
    df = build_player_features()
    df["impact_score"] = compute_impact_score(df)

    X = df.select_dtypes(include=["int64", "float64"]).drop(columns=["impact_score"])
    y = df["impact_score"]

    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_imputed, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("MAE:", mean_absolute_error(y_test, preds))
    print("R2:", r2_score(y_test, preds))

    joblib.dump(model, MODEL_DIR / "playerlens_model.pkl")
    joblib.dump(imputer, MODEL_DIR / "imputer.pkl")

    print("Model and imputer saved.")

if __name__ == "__main__":
    train_and_save()
