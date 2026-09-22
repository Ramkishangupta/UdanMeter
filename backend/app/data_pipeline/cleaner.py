import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple

class AirfareDataCleaner:
    """
    Data Cleaning & Outlier Removal Engine for MoSPI CPI Airfare Pipeline.
    Implements Modified Z-Score and Interquartile Range (IQR) bounds to purge
    anomalous price spikes, web scraping artifacts, and zero-fare glitches.
    """

    @staticmethod
    def detect_outliers_iqr(df: pd.DataFrame, fare_column: str = "total_fare") -> pd.DataFrame:
        """
        Interquartile Range (IQR) method:
        Q1 = 25th percentile, Q3 = 75th percentile, IQR = Q3 - Q1
        Lower Bound = Q1 - 1.5 * IQR
        Upper Bound = Q3 + 1.5 * IQR
        """
        if df.empty or len(df) < 4:
            df["is_outlier"] = False
            df["z_score"] = 0.0
            return df

        q1 = df[fare_column].quantile(0.25)
        q3 = df[fare_column].quantile(0.75)
        iqr = q3 - q1

        lower_bound = max(500.0, q1 - 1.5 * iqr) # Minimum realistic domestic fare ₹500
        upper_bound = q3 + 2.0 * iqr             # Upper bound cutoff

        # Calculate Modified Z-score (median based)
        median = df[fare_column].median()
        mad = np.median(np.abs(df[fare_column] - median))
        if mad == 0:
            mad = 1.0
        z_scores = 0.6745 * (df[fare_column] - median) / mad

        df["z_score"] = z_scores.round(2)
        df["is_outlier"] = (df[fare_column] < lower_bound) | (df[fare_column] > upper_bound) | (abs(z_scores) > 3.5)

        return df

    def clean_and_deduplicate_batch(self, raw_quotes: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
        """
        Cleans raw quote dictionary list, flags outliers per (route, advance_days) group,
        and deduplicates identical quotes.
        """
        if not raw_quotes:
            return [], 0

        df = pd.DataFrame(raw_quotes)

        # 1. Basic validation (Drop negative or zero fares)
        df = df[df["total_fare"] > 0]

        # 2. Outlier Detection grouped by (origin, destination, advance_days)
        cleaned_groups = []
        outlier_count = 0

        for (origin, dest, adv), group in df.groupby(["origin", "destination", "advance_days"]):
            group_cleaned = self.detect_outliers_iqr(group.copy(), "total_fare")
            outliers_in_group = group_cleaned["is_outlier"].sum()
            outlier_count += int(outliers_in_group)
            cleaned_groups.append(group_cleaned)

        if cleaned_groups:
            cleaned_df = pd.concat(cleaned_groups, ignore_index=True)
        else:
            cleaned_df = df.copy()
            cleaned_df["is_outlier"] = False
            cleaned_df["z_score"] = 0.0

        # 3. Filter out outliers for index calculation payload
        valid_records = cleaned_df.to_dict(orient="records")
        return valid_records, outlier_count

data_cleaner = AirfareDataCleaner()
