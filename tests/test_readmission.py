import pandas as pd

from readmission import readmission_rate_by_age


def test_counts_and_rates():
    # ">30" and "NO" count as encounters, but not as 30-day readmissions
    df = pd.DataFrame({
        "age": ["[0-10)", "[0-10)", "[50-60)", "[50-60)", "[50-60)"],
        "readmitted": ["<30", "NO", "<30", ">30", "NO"],
    })
    expected = pd.DataFrame({
        "age_bracket": ["[0-10)", "[50-60)"],
        "encounters": [2, 3],
        "readmission_rate_30d": [1 / 2, 1 / 3],
    })
    pd.testing.assert_frame_equal(readmission_rate_by_age(df), expected)


def test_age_order():
    df = pd.DataFrame({"age": ["[90-100)", "[0-10)", "[10-20)"], "readmitted": ["NO", "NO", "NO"]})
    assert readmission_rate_by_age(df)["age_bracket"].tolist() == ["[0-10)", "[10-20)", "[90-100)"]
