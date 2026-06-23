import numpy as np
import pandas as pd
from ..config import MISSION_DAYS

def regime(rate_mGy_day):
    if rate_mGy_day < 0.1:
        return 'very_low_model_forcing'
    if rate_mGy_day < 1.0:
        return 'low_model_forcing'
    if rate_mGy_day < 10.0:
        return 'moderate_model_forcing'
    if rate_mGy_day < 100.0:
        return 'high_model_forcing'
    return 'extreme_model_forcing'

def process_dose_forcing(dose_df: pd.DataFrame) -> pd.DataFrame:
    """Process total mission doses to calculate daily dose rates and forcing indices."""
    forcing = dose_df.copy().sort_values(['scenario', 'shield_mm_Al']).reset_index(drop=True)
    forcing['mission_days'] = MISSION_DAYS
    forcing['total_dose_rate_Gy_day'] = forcing['total_dose_Gy'] / forcing['mission_days']
    forcing['total_dose_rate_mGy_day'] = forcing['total_dose_rate_Gy_day'] * 1000.0
    forcing['electron_dose_rate_mGy_day'] = forcing['electron_dose_Gy'] * 1000.0 / forcing['mission_days']
    forcing['brems_dose_rate_mGy_day'] = forcing['brems_dose_Gy'] * 1000.0 / forcing['mission_days']
    forcing['trapped_proton_dose_rate_mGy_day'] = forcing['trapped_proton_dose_Gy'] * 1000.0 / forcing['mission_days']
    
    max_rate = forcing['total_dose_rate_mGy_day'].max()
    forcing['ros_forcing_index_log01'] = np.log1p(forcing['total_dose_rate_mGy_day']) / np.log1p(max_rate) if max_rate > 0 else 0.0
    
    forcing['forcing_regime_label'] = forcing['total_dose_rate_mGy_day'].apply(regime)
    forcing['recommended_use'] = np.where(
        forcing['scenario'].str.contains('VanAllen'),
        'stress-test / belt-crossing comparison, not a normal astronaut-habitat case',
        'baseline LEO comparison case'
    )
    
    return forcing[[
        'scenario', 'shield_mm_Al', 'mission_days',
        'total_dose_Gy', 'total_dose_rate_Gy_day', 'total_dose_rate_mGy_day',
        'electron_dose_rate_mGy_day', 'brems_dose_rate_mGy_day', 'trapped_proton_dose_rate_mGy_day',
        'ros_forcing_index_log01', 'forcing_regime_label', 'recommended_use'
    ]]
