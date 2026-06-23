# RADBIO_NEURO_001 SPENVIS first-pass extraction

## What was extracted

The uploaded ZIP was readable. Most SPENVIS "txt" exports were actually PDF files saved with a `.txt` extension. I extracted text from those PDFs and generated machine-readable CSV summaries where possible.

## Main usable parsed output

1. `shieldose2_tissue_dose_by_shielding.csv`
   - Parsed from SHIELDOSE-2 tissue dose files.
   - Contains dose behind aluminium shielding for:
     - LEO ISS-like baseline
     - Van Allen/RBSP-like crossing
   - Units included:
     - rad over 180 days
     - Gy over 180 days

2. `leo_vs_vab_shieldose2_comparison.csv`
   - Direct scenario comparison at all shielding depths.
   - Includes VAB/LEO dose ratio.

3. `selected_shielding_depth_summary.csv`
   - Compact table at 1, 2, 5, 10, and 20 mm Al.

4. `effective_dose_output_audit.csv`
   - The SPENVIS effective-dose Monte Carlo output files were extracted, but the final effective-dose field is `NaN` in the available LEO 10k, LEO 100k, and VAB 10k outputs.
   - Therefore those effective-dose outputs should not be used yet as biological calibration values.
   - The Mulassis multilayer fluence outputs are present and can be inspected, but the final effective-dose conversion did not produce numeric Sv values.

## Important scientific interpretation

For the current workflow, use the SHIELDOSE-2 tissue absorbed dose tables as the primary quantitative dose layer. Treat the effective-dose Monte Carlo results as failed/incomplete until rerun with settings that produce non-NaN Sv outputs.

## Next modeling step

Use the SHIELDOSE-2 tissue dose table to construct a scenario-level dose forcing term:

- scenario
- shielding thickness
- total absorbed dose in Gy over 180 days
- dose rate in Gy/day
- component decomposition: electrons, bremsstrahlung, trapped protons

This can then feed the ROS/mitochondrial model. Effective dose / dose equivalent should be rerun or obtained through a better route before making biological risk claims about high-LET weighting.
