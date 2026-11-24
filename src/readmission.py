import pandas as pd


def readmission_rate_by_age(df: pd.DataFrame) -> pd.DataFrame:
    """Number of encounters and 30-day readmission rate per age bracket.

    Only "<30" counts as a 30-day readmission. Apply exclusions before calling.
    """
    readmitted_30d = df["readmitted"] == "<30"
    return (
        readmitted_30d.groupby(df["age"])
        .agg(encounters="size", readmission_rate_30d="mean")
        .reset_index(names="age_bracket")
    )
