import pandas as pd
from feature_engineering import build_player_features
from model import compute_impact_score

from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer

def interpret_linear_model():
    df = build_player_features()
    df["impact_score"] = compute_impact_score(df)

    X = df.select_dtypes(include=["int64", "float64"]).drop(columns=["impact_score"])
    y = df["impact_score"]

    feature_names = X.columns

    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)

    model = LinearRegression()
    model.fit(X_imputed, y)

    importance = pd.DataFrame({
        "feature": feature_names,
        "coefficient": model.coef_
    })

    importance["abs_coeff"] = importance["coefficient"].abs()
    importance = importance.sort_values(by="abs_coeff", ascending=False)

    print(importance.head(15))

if __name__ == "__main__":
    interpret_linear_model()
