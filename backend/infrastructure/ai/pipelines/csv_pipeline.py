import pandas as pd
import numpy as np
from shared.logger.logger import get_logger

logger = get_logger(__name__)


def profile_csv(file_path: str) -> dict:
    """
    Analyse un fichier CSV et retourne un profil complet.
    Utilisé par la tâche Celery après l'upload.
    """
    df = pd.read_csv(file_path)

    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": {},
        "missing_values": {},
        "sample": df.head(5).to_dict(orient="records"),
    }

    for col in df.columns:
        col_type = str(df[col].dtype)
        missing = int(df[col].isna().sum())
        missing_pct = round(missing / len(df) * 100, 2)

        col_info = {
            "type": col_type,
            "missing": missing,
            "missing_pct": missing_pct,
        }

        # Stats supplémentaires pour les colonnes numériques
        if df[col].dtype in [np.float64, np.int64]:
            col_info.update({
                "mean": round(float(df[col].mean()), 2),
                "std": round(float(df[col].std()), 2),
                "min": round(float(df[col].min()), 2),
                "max": round(float(df[col].max()), 2),
            })

        # Stats pour les colonnes texte
        elif df[col].dtype == object:
            col_info.update({
                "unique_count": int(df[col].nunique()),
                "top_values": df[col].value_counts().head(3).to_dict(),
            })

        profile["columns"][col] = col_info
        profile["missing_values"][col] = missing

    logger.info(f"Profiling terminé : {len(df)} lignes, {len(df.columns)} colonnes")
    return profile