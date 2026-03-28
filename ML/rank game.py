<<<<<<< HEAD
# """
# JEE Marks → Rank Predictor
# ==========================
# Combines:
#   - ML model (RandomForest): Marks → Percentile
#   - Formula-based logic:      Percentile → Rank
#
# Usage:
#     python marks_to_rank.py                  # interactive mode
#     python marks_to_rank.py --train          # retrain model from CSV
#     python marks_to_rank.py --marks 250      # predict for specific marks
# """
#
# import math
# import os
# import argparse
# import numpy as np
#
# # ──────────────────────────────────────────────
# # 1. STUDENT COUNT DATA  (model2.py logic)
# # ──────────────────────────────────────────────
#
# OFFICIAL_STUDENT_DATA = {
#     2022: 905000,
#     2023: 1113000,
#     2024: 1170000,
#     2025: 1200000,
# }
#
# GROWTH_RATE = 0.04
#
#
# def get_student_count(year: int) -> int:
#     """Return student count for a given year (official or estimated)."""
#     if year in OFFICIAL_STUDENT_DATA:
#         return OFFICIAL_STUDENT_DATA[year]
#
#     last_year = max(OFFICIAL_STUDENT_DATA.keys())
#     last_count = OFFICIAL_STUDENT_DATA[last_year]
#     years_after = year - last_year
#     return int(last_count * ((1 + GROWTH_RATE) ** years_after))
#
#
# def percentile_to_rank(percentile: float, year: int) -> int:
#     """Convert percentile to rank for a given exam year."""
#     if not (0 <= percentile <= 100):
#         raise ValueError("Percentile must be between 0 and 100.")
#     total = get_student_count(year)
#     rank = (100 - percentile) * total / 100
#     return math.ceil(rank)
#
#
# # ──────────────────────────────────────────────
# # 2. ML MODEL  (train_model1.py logic)
# # ──────────────────────────────────────────────
#
# MODEL_PATH = "model1_marks_to_percentile.pkl"
#
#
# def train_model(csv_path: str):
#     """Train RandomForest on Marks → Percentile and save it."""
#     import pandas as pd
#     from sklearn.model_selection import train_test_split
#     from sklearn.ensemble import RandomForestRegressor
#     from sklearn.metrics import mean_absolute_error, r2_score
#     import joblib
#
#     print(f"Loading data from: {csv_path}")
#     df = pd.read_csv(csv_path)
#
#     X = df[["Marks"]]
#     y = df["Percentile"]
#
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, random_state=42
#     )
#
#     model = RandomForestRegressor(n_estimators=300, random_state=42)
#     model.fit(X_train, y_train)
#
#     preds = model.predict(X_test)
#     print(f"  MAE : {round(mean_absolute_error(y_test, preds), 4)}")
#     print(f"  R²  : {round(r2_score(y_test, preds), 4)}")
#
#     import joblib
#     joblib.dump(model, MODEL_PATH)
#     print(f"Model saved → {MODEL_PATH}")
#     return model
#
#
# def load_model():
#     """Load saved model, or fall back to a simple linear approximation."""
#     if os.path.exists(MODEL_PATH):
#         import joblib
#         print(f"Loaded model from {MODEL_PATH}")
#         return joblib.load(MODEL_PATH)
#
#     # ── Fallback: polynomial approximation (no CSV needed) ──────────────
#     # Approximate JEE Main marks-percentile mapping (based on historical data)
#     # Max marks = 300
#     print("⚠  No trained model found. Using built-in polynomial approximation.")
#     print("   Run with --train <csv_path> to use your own data.\n")
#     return None
#
#
# # ──────────────────────────────────────────────
# # 3. FALLBACK APPROXIMATION (no model file)
# # ──────────────────────────────────────────────
#
# # Historical JEE Main reference points (marks → approx percentile)
# _MARKS_REF   = [0,  20,  40,  60,  80, 100, 120, 140, 160, 180, 200, 220, 250, 280, 300]
# _PCTILE_REF  = [1,   5,  10,  20,  35,  50,  65,  78,  87,  93,  97, 98.5, 99.3, 99.8, 100]
#
#
# def fallback_marks_to_percentile(marks: float) -> float:
#     """Piecewise-linear interpolation from historical reference data."""
#     marks = max(0, min(300, marks))
#     return float(np.interp(marks, _MARKS_REF, _PCTILE_REF))
#
#
# # ──────────────────────────────────────────────
# # 4. COMBINED PIPELINE
# # ──────────────────────────────────────────────
#
# def predict(marks: float, year: int = 2025, model=None) -> dict:
#     """
#     Full pipeline: Marks → Percentile → Rank
#
#     Returns a dict with marks, percentile, rank, and student count.
#     """
#     if marks < 0 or marks > 300:
#         raise ValueError("Marks must be between 0 and 300.")
#
#     # Step 1: Marks → Percentile
#     if model is not None:
#         import pandas as pd
#         percentile = float(model.predict(pd.DataFrame({"Marks": [marks]}))[0])
#         percentile = max(0.0, min(100.0, percentile))
#     else:
#         percentile = fallback_marks_to_percentile(marks)
#
#     # Step 2: Percentile → Rank
#     rank = percentile_to_rank(percentile, year)
#     total = get_student_count(year)
#
#     return {
#         "marks":      marks,
#         "percentile": round(percentile, 4),
#         "rank":       rank,
#         "year":       year,
#         "total_students": total,
#     }
#
#
# # ──────────────────────────────────────────────
# # 5. CLI / INTERACTIVE
# # ──────────────────────────────────────────────
#
# def print_result(result: dict):
#     print("\n" + "─" * 40)
#     print(f"  Marks          : {result['marks']}")
#     print(f"  Percentile     : {result['percentile']}")
#     print(f"  Estimated Rank : {result['rank']:,}")
#     print(f"  Year           : {result['year']}")
#     print(f"  Total Students : {result['total_students']:,}")
#     print("─" * 40 + "\n")
#
#
# def main():
#     parser = argparse.ArgumentParser(description="JEE Marks → Rank Predictor")
#     parser.add_argument("--train",  metavar="CSV",  help="Train model from CSV file (needs Marks, Percentile columns)")
#     parser.add_argument("--marks",  type=float,     help="Predict rank for given marks")
#     parser.add_argument("--year",   type=int, default=2025, help="Exam year (default: 2025)")
#     args = parser.parse_args()
#
#     model = None
#
#     if args.train:
#         model = train_model(args.train)
#     else:
#         model = load_model()
#
#     if args.marks is not None:
#         result = predict(args.marks, year=args.year, model=model)
#         print_result(result)
#         return
#
#     # Interactive mode
#     print("=" * 40)
#     print("  JEE Marks → Rank Predictor")
#     print("=" * 40)
#     print("Enter marks (0–300) to get predicted rank.")
#     print("Type 'quit' to exit.\n")
#
#     while True:
#         try:
#             raw = input("Enter marks: ").strip()
#             if raw.lower() in ("quit", "exit", "q"):
#                 break
#             marks = float(raw)
#
#             year_raw = input(f"Enter exam year (press Enter for {args.year}): ").strip()
#             year = int(year_raw) if year_raw else args.year
#
#             result = predict(marks, year=year, model=model)
#             print_result(result)
#
#         except ValueError as e:
#             print(f"  Error: {e}")
#         except KeyboardInterrupt:
#             break
#
#     print("Goodbye!")
#
#
# if __name__ == "__main__":
#     main()
import math
import os
import argparse
import numpy as np


OFFICIAL_STUDENT_DATA = {
    2022: 905000,
    2023: 1113000,
    2024: 1170000,
    2025: 1200000,
}

GROWTH_RATE = 0.04


def get_student_count(year: int) -> int:
    """Return student count for a given year (official or estimated)."""
    if year in OFFICIAL_STUDENT_DATA:
        return OFFICIAL_STUDENT_DATA[year]

    last_year = max(OFFICIAL_STUDENT_DATA.keys())
    last_count = OFFICIAL_STUDENT_DATA[last_year]
    years_after = year - last_year
    return int(last_count * ((1 + GROWTH_RATE) ** years_after))


def percentile_to_rank(percentile: float, year: int) -> int:
    """Convert percentile to rank for a given exam year."""
    if not (0 <= percentile <= 100):
        raise ValueError("Percentile must be between 0 and 100.")
    total = get_student_count(year)
    rank = (100 - percentile) * total / 100
    return math.ceil(rank)


MODEL_PATH = "model1_marks_to_percentile.pkl"


def train_model(csv_path: str):
    """Train RandomForest on Marks → Percentile and save it."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, r2_score
    import joblib

    print(f"Loading data from: {csv_path}")
    df = pd.read_csv(csv_path)

    X = df[["Marks"]]
    y = df["Percentile"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=300, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"  MAE : {round(mean_absolute_error(y_test, preds), 4)}")
    print(f"  R²  : {round(r2_score(y_test, preds), 4)}")

    import joblib
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved → {MODEL_PATH}")
    return model


def load_model():
    """Load saved model, or fall back to a simple linear approximation."""
    if os.path.exists(MODEL_PATH):
        import joblib
        print(f"Loaded model from {MODEL_PATH}")
        return joblib.load(MODEL_PATH)

    # ── Fallback: polynomial approximation (no CSV needed) ──────────────
    # Approximate JEE Main marks-percentile mapping (based on historical data)
    # Max marks = 300
    print("⚠  No trained model found. Using built-in polynomial approximation.")
    print("   Run with --train <csv_path> to use your own data.\n")
    return None




_MARKS_REF = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 250, 280, 300]
_PCTILE_REF = [1, 5, 10, 20, 35, 50, 65, 78, 87, 93, 97, 98.5, 99.3, 99.8, 100]


def fallback_marks_to_percentile(marks: float) -> float:
    """Piecewise-linear interpolation from historical reference data."""
    marks = max(0, min(300, marks))
    return float(np.interp(marks, _MARKS_REF, _PCTILE_REF))



def predict(marks: float, year: int = 2025, model=None) -> dict:
    """
    Full pipeline: Marks → Percentile → Rank

    Returns a dict with marks, percentile, rank, and student count.
    """
    if marks < 0 or marks > 300:
        raise ValueError("Marks must be between 0 and 300.")


    if model is not None:
        import pandas as pd
        percentile = float(model.predict(pd.DataFrame({"Marks": [marks]}))[0])
        percentile = max(0.0, min(100.0, percentile))
    else:
        percentile = fallback_marks_to_percentile(marks)

    # Step 2: Percentile → Rank
    rank = percentile_to_rank(percentile, year)
    total = get_student_count(year)

    return {
        "marks": marks,
        "percentile": round(percentile, 4),
        "rank": rank,
        "year": year,
        "total_students": total,
    }



def print_result(result: dict):
    print(result['rank'])


def main():
    parser = argparse.ArgumentParser(description="JEE Marks → Rank Predictor")
    parser.add_argument("--train", metavar="CSV", help="Train model from CSV file (needs Marks, Percentile columns)")
    parser.add_argument("--marks", type=float, help="Predict rank for given marks")
    parser.add_argument("--year", type=int, default=2025, help="Exam year (default: 2025)")
    args = parser.parse_args()

    model = None

    if args.train:
        model = train_model(args.train)
    else:
        model = load_model()

    if args.marks is not None:
        result = predict(args.marks, year=args.year, model=model)
        print_result(result)
        return

    # Interactive mode
    print("=" * 40)
    print("  JEE Marks → Rank Predictor")
    print("=" * 40)
    print("Enter marks (0–300) to get predicted rank.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            raw = input("Enter marks: ").strip()
            if raw.lower() in ("quit", "exit", "q"):
                break
            marks = float(raw)

            year_raw = input(f"Enter exam year (press Enter for {args.year}): ").strip()
            year = int(year_raw) if year_raw else args.year

            result = predict(marks, year=year, model=model)
            print_result(result)

        except ValueError as e:
            print(f"  Error: {e}")
        except KeyboardInterrupt:
            break

    print("Goodbye!")


if __name__ == "__main__":
=======
# """
# JEE Marks → Rank Predictor
# ==========================
# Combines:
#   - ML model (RandomForest): Marks → Percentile
#   - Formula-based logic:      Percentile → Rank
#
# Usage:
#     python marks_to_rank.py                  # interactive mode
#     python marks_to_rank.py --train          # retrain model from CSV
#     python marks_to_rank.py --marks 250      # predict for specific marks
# """
#
# import math
# import os
# import argparse
# import numpy as np
#
# # ──────────────────────────────────────────────
# # 1. STUDENT COUNT DATA  (model2.py logic)
# # ──────────────────────────────────────────────
#
# OFFICIAL_STUDENT_DATA = {
#     2022: 905000,
#     2023: 1113000,
#     2024: 1170000,
#     2025: 1200000,
# }
#
# GROWTH_RATE = 0.04
#
#
# def get_student_count(year: int) -> int:
#     """Return student count for a given year (official or estimated)."""
#     if year in OFFICIAL_STUDENT_DATA:
#         return OFFICIAL_STUDENT_DATA[year]
#
#     last_year = max(OFFICIAL_STUDENT_DATA.keys())
#     last_count = OFFICIAL_STUDENT_DATA[last_year]
#     years_after = year - last_year
#     return int(last_count * ((1 + GROWTH_RATE) ** years_after))
#
#
# def percentile_to_rank(percentile: float, year: int) -> int:
#     """Convert percentile to rank for a given exam year."""
#     if not (0 <= percentile <= 100):
#         raise ValueError("Percentile must be between 0 and 100.")
#     total = get_student_count(year)
#     rank = (100 - percentile) * total / 100
#     return math.ceil(rank)
#
#
# # ──────────────────────────────────────────────
# # 2. ML MODEL  (train_model1.py logic)
# # ──────────────────────────────────────────────
#
# MODEL_PATH = "model1_marks_to_percentile.pkl"
#
#
# def train_model(csv_path: str):
#     """Train RandomForest on Marks → Percentile and save it."""
#     import pandas as pd
#     from sklearn.model_selection import train_test_split
#     from sklearn.ensemble import RandomForestRegressor
#     from sklearn.metrics import mean_absolute_error, r2_score
#     import joblib
#
#     print(f"Loading data from: {csv_path}")
#     df = pd.read_csv(csv_path)
#
#     X = df[["Marks"]]
#     y = df["Percentile"]
#
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, random_state=42
#     )
#
#     model = RandomForestRegressor(n_estimators=300, random_state=42)
#     model.fit(X_train, y_train)
#
#     preds = model.predict(X_test)
#     print(f"  MAE : {round(mean_absolute_error(y_test, preds), 4)}")
#     print(f"  R²  : {round(r2_score(y_test, preds), 4)}")
#
#     import joblib
#     joblib.dump(model, MODEL_PATH)
#     print(f"Model saved → {MODEL_PATH}")
#     return model
#
#
# def load_model():
#     """Load saved model, or fall back to a simple linear approximation."""
#     if os.path.exists(MODEL_PATH):
#         import joblib
#         print(f"Loaded model from {MODEL_PATH}")
#         return joblib.load(MODEL_PATH)
#
#     # ── Fallback: polynomial approximation (no CSV needed) ──────────────
#     # Approximate JEE Main marks-percentile mapping (based on historical data)
#     # Max marks = 300
#     print("⚠  No trained model found. Using built-in polynomial approximation.")
#     print("   Run with --train <csv_path> to use your own data.\n")
#     return None
#
#
# # ──────────────────────────────────────────────
# # 3. FALLBACK APPROXIMATION (no model file)
# # ──────────────────────────────────────────────
#
# # Historical JEE Main reference points (marks → approx percentile)
# _MARKS_REF   = [0,  20,  40,  60,  80, 100, 120, 140, 160, 180, 200, 220, 250, 280, 300]
# _PCTILE_REF  = [1,   5,  10,  20,  35,  50,  65,  78,  87,  93,  97, 98.5, 99.3, 99.8, 100]
#
#
# def fallback_marks_to_percentile(marks: float) -> float:
#     """Piecewise-linear interpolation from historical reference data."""
#     marks = max(0, min(300, marks))
#     return float(np.interp(marks, _MARKS_REF, _PCTILE_REF))
#
#
# # ──────────────────────────────────────────────
# # 4. COMBINED PIPELINE
# # ──────────────────────────────────────────────
#
# def predict(marks: float, year: int = 2025, model=None) -> dict:
#     """
#     Full pipeline: Marks → Percentile → Rank
#
#     Returns a dict with marks, percentile, rank, and student count.
#     """
#     if marks < 0 or marks > 300:
#         raise ValueError("Marks must be between 0 and 300.")
#
#     # Step 1: Marks → Percentile
#     if model is not None:
#         import pandas as pd
#         percentile = float(model.predict(pd.DataFrame({"Marks": [marks]}))[0])
#         percentile = max(0.0, min(100.0, percentile))
#     else:
#         percentile = fallback_marks_to_percentile(marks)
#
#     # Step 2: Percentile → Rank
#     rank = percentile_to_rank(percentile, year)
#     total = get_student_count(year)
#
#     return {
#         "marks":      marks,
#         "percentile": round(percentile, 4),
#         "rank":       rank,
#         "year":       year,
#         "total_students": total,
#     }
#
#
# # ──────────────────────────────────────────────
# # 5. CLI / INTERACTIVE
# # ──────────────────────────────────────────────
#
# def print_result(result: dict):
#     print("\n" + "─" * 40)
#     print(f"  Marks          : {result['marks']}")
#     print(f"  Percentile     : {result['percentile']}")
#     print(f"  Estimated Rank : {result['rank']:,}")
#     print(f"  Year           : {result['year']}")
#     print(f"  Total Students : {result['total_students']:,}")
#     print("─" * 40 + "\n")
#
#
# def main():
#     parser = argparse.ArgumentParser(description="JEE Marks → Rank Predictor")
#     parser.add_argument("--train",  metavar="CSV",  help="Train model from CSV file (needs Marks, Percentile columns)")
#     parser.add_argument("--marks",  type=float,     help="Predict rank for given marks")
#     parser.add_argument("--year",   type=int, default=2025, help="Exam year (default: 2025)")
#     args = parser.parse_args()
#
#     model = None
#
#     if args.train:
#         model = train_model(args.train)
#     else:
#         model = load_model()
#
#     if args.marks is not None:
#         result = predict(args.marks, year=args.year, model=model)
#         print_result(result)
#         return
#
#     # Interactive mode
#     print("=" * 40)
#     print("  JEE Marks → Rank Predictor")
#     print("=" * 40)
#     print("Enter marks (0–300) to get predicted rank.")
#     print("Type 'quit' to exit.\n")
#
#     while True:
#         try:
#             raw = input("Enter marks: ").strip()
#             if raw.lower() in ("quit", "exit", "q"):
#                 break
#             marks = float(raw)
#
#             year_raw = input(f"Enter exam year (press Enter for {args.year}): ").strip()
#             year = int(year_raw) if year_raw else args.year
#
#             result = predict(marks, year=year, model=model)
#             print_result(result)
#
#         except ValueError as e:
#             print(f"  Error: {e}")
#         except KeyboardInterrupt:
#             break
#
#     print("Goodbye!")
#
#
# if __name__ == "__main__":
#     main()
import math
import os
import argparse
import numpy as np


OFFICIAL_STUDENT_DATA = {
    2022: 905000,
    2023: 1113000,
    2024: 1170000,
    2025: 1200000,
}

GROWTH_RATE = 0.04


def get_student_count(year: int) -> int:
    """Return student count for a given year (official or estimated)."""
    if year in OFFICIAL_STUDENT_DATA:
        return OFFICIAL_STUDENT_DATA[year]

    last_year = max(OFFICIAL_STUDENT_DATA.keys())
    last_count = OFFICIAL_STUDENT_DATA[last_year]
    years_after = year - last_year
    return int(last_count * ((1 + GROWTH_RATE) ** years_after))


def percentile_to_rank(percentile: float, year: int) -> int:
    """Convert percentile to rank for a given exam year."""
    if not (0 <= percentile <= 100):
        raise ValueError("Percentile must be between 0 and 100.")
    total = get_student_count(year)
    rank = (100 - percentile) * total / 100
    return math.ceil(rank)


MODEL_PATH = "model1_marks_to_percentile.pkl"


def train_model(csv_path: str):
    """Train RandomForest on Marks → Percentile and save it."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, r2_score
    import joblib

    print(f"Loading data from: {csv_path}")
    df = pd.read_csv(csv_path)

    X = df[["Marks"]]
    y = df["Percentile"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=300, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"  MAE : {round(mean_absolute_error(y_test, preds), 4)}")
    print(f"  R²  : {round(r2_score(y_test, preds), 4)}")

    import joblib
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved → {MODEL_PATH}")
    return model


def load_model():
    """Load saved model, or fall back to a simple linear approximation."""
    if os.path.exists(MODEL_PATH):
        import joblib
        print(f"Loaded model from {MODEL_PATH}")
        return joblib.load(MODEL_PATH)

    # ── Fallback: polynomial approximation (no CSV needed) ──────────────
    # Approximate JEE Main marks-percentile mapping (based on historical data)
    # Max marks = 300
    print("⚠  No trained model found. Using built-in polynomial approximation.")
    print("   Run with --train <csv_path> to use your own data.\n")
    return None




_MARKS_REF = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 250, 280, 300]
_PCTILE_REF = [1, 5, 10, 20, 35, 50, 65, 78, 87, 93, 97, 98.5, 99.3, 99.8, 100]


def fallback_marks_to_percentile(marks: float) -> float:
    """Piecewise-linear interpolation from historical reference data."""
    marks = max(0, min(300, marks))
    return float(np.interp(marks, _MARKS_REF, _PCTILE_REF))



def predict(marks: float, year: int = 2025, model=None) -> dict:
    """
    Full pipeline: Marks → Percentile → Rank

    Returns a dict with marks, percentile, rank, and student count.
    """
    if marks < 0 or marks > 300:
        raise ValueError("Marks must be between 0 and 300.")


    if model is not None:
        import pandas as pd
        percentile = float(model.predict(pd.DataFrame({"Marks": [marks]}))[0])
        percentile = max(0.0, min(100.0, percentile))
    else:
        percentile = fallback_marks_to_percentile(marks)

    # Step 2: Percentile → Rank
    rank = percentile_to_rank(percentile, year)
    total = get_student_count(year)

    return {
        "marks": marks,
        "percentile": round(percentile, 4),
        "rank": rank,
        "year": year,
        "total_students": total,
    }



def print_result(result: dict):
    print(result['rank'])


def main():
    parser = argparse.ArgumentParser(description="JEE Marks → Rank Predictor")
    parser.add_argument("--train", metavar="CSV", help="Train model from CSV file (needs Marks, Percentile columns)")
    parser.add_argument("--marks", type=float, help="Predict rank for given marks")
    parser.add_argument("--year", type=int, default=2025, help="Exam year (default: 2025)")
    args = parser.parse_args()

    model = None

    if args.train:
        model = train_model(args.train)
    else:
        model = load_model()

    if args.marks is not None:
        result = predict(args.marks, year=args.year, model=model)
        print_result(result)
        return

    # Interactive mode
    print("=" * 40)
    print("  JEE Marks → Rank Predictor")
    print("=" * 40)
    print("Enter marks (0–300) to get predicted rank.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            raw = input("Enter marks: ").strip()
            if raw.lower() in ("quit", "exit", "q"):
                break
            marks = float(raw)

            year_raw = input(f"Enter exam year (press Enter for {args.year}): ").strip()
            year = int(year_raw) if year_raw else args.year

            result = predict(marks, year=year, model=model)
            print_result(result)

        except ValueError as e:
            print(f"  Error: {e}")
        except KeyboardInterrupt:
            break

    print("Goodbye!")


if __name__ == "__main__":
>>>>>>> d8506cd368c11c7a9642b8de967055ae8e9d1d84
    main()