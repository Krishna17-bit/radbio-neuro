import pandas as pd

def audit_effective_dose_nans(eff_audit_df: pd.DataFrame) -> dict:
    """Audit the effective dose dataframe for NaN outputs.
    Returns audit details showing which columns contain NaNs."""
    nan_count = eff_audit_df['usable_numeric_effective_dose'].isna().sum()
    any_usable = eff_audit_df['usable_numeric_effective_dose'].fillna(False).astype(bool).any()
    
    return {
        "nan_count": int(nan_count),
        "any_usable": bool(any_usable),
        "flag_unusable": not any_usable
    }

def check_calibration_domain(dose_rate_mGy_day: float) -> str:
    """Label dose rate based on proximity to the primary chronic biological validation domain (0.1 to 10.0 mGy/day)."""
    if 0.1 <= dose_rate_mGy_day <= 10.0:
        return 'near_primary_validation_domain'
    elif dose_rate_mGy_day > 10.0:
        return 'outside_primary_validation_domain_high_dose_rate'
    else:
        return 'outside_primary_validation_domain_low_dose_rate'
