# Variables by step

Columns produced at each step. The code uses the same column names as the output Excel files.
"not written" marks working columns that stay inside the code. Constant values are in `main_code/settings.py`.

## Inputs

| Input | Where | Read by |
|---|---|---|
| Top and front videos (frame-aligned) | `Top/`, `Front/` in the day folder, found by trial number | `preprocessing/load_videos.py` |
| YOLO weights | `inputs.top_weights`, `inputs.front_weights` | `preprocessing/step01_detect_object.py` |
| Calibration NPZ (R, t) | `inputs.calib_top_npz`, `inputs.calib_front_npz` | `preprocessing/load_calibration.py`, `postprocessing/load_raw_excel.py` |
| Camera intrinsics (K, D) | `cameras.top`, `cameras.front` | same as above |

## Preprocessing → `raw_N.xlsx`

### ① Object detection — `step01_detect_object.py`

| Column | Sheet | Meaning |
|---|---|---|
| `Top_Status`, `Front_Status` | Trajectory | DETECTED / LOST |
| `Top_U_px`, `Top_V_px` | Trajectory | Top box center [px] |
| `Front_U_px`, `Front_V_px` | Trajectory | Front box center [px] |
| `Top_Conf`, `Front_Conf` | Trajectory | YOLO confidence |

### ② Ray generation and refraction — `common/refraction.py`

No output columns. Interfaces: water surface `Z = WATER_SURFACE_Z_CM`, front wall `Y = FRONT_WALL_Y_CM`.

### ③ Triangulation — `step03_triangulate.py`

| Column | Sheet | Meaning |
|---|---|---|
| `Candidate_ON_X/Y/Z_cm` | Triangulation | Refraction ON candidate |
| `Candidate_OFF_X/Y/Z_cm` | Triangulation | Refraction OFF candidate (comparison) |
| `Candidate_X/Y/Z_cm` | Triangulation | Candidate after the ray-gap gate |
| `Geometry_Status_ON/OFF` | Triangulation | VALID / FAILED / NOT_PAIRED |
| `Ray_Gap_cm` | Trajectory | Closest distance between the two rays |
| `Ray_Gap_ON_cm`, `Ray_Gap_OFF_cm` | Triangulation | Ray gap for ON / OFF |
| `Top_Ray_Dist_cm`, `Front_Ray_Dist_cm` | Triangulation | Ray length from the interface to the closest point |

### ④ Gating and track confirmation — `step04_gate_and_track.py`

| Column | Sheet | Meaning |
|---|---|---|
| `Meas_Status` | Trajectory | TRIANGULATED / NO_CANDIDATE / REJECTED_JUMP / REJECTED_MAHALANOBIS / TENTATIVE_HOLD / *_RESET |
| `Missing_Reason` | Trajectory | NONE / TOP_MISSING / FRONT_MISSING / BOTH_MISSING / RAY_GAP_EXCEEDED / TRIANGULATION_FAILED / REJECTED_* / TENTATIVE_HOLD |
| `Track_State` | Online_Filter | LOST / TENTATIVE / CONFIRMED |
| `KF_Updated` | Online_Filter | Filter updated in this frame |
| `KF_X/Y/Z_cm` | Online_Filter | Gate filter state |
| `KF_Std_X/Y/Z_cm` | Online_Filter | Gate filter position std |

### ⑤ Gripper-frame transform — `step05_to_gripper_frame.py`

| Column | Sheet | Meaning |
|---|---|---|
| `Meas_X/Y/Z_cm` | Trajectory | Accepted 3D position, origin = gripper (motor) center |

### Other raw columns

| Column | Sheet |
|---|---|
| `Frame`, `Time_s` | Trajectory |
| `Sig_*`, `Tracker_Ref_Frame`, `*_Source_Frame`, `*_Time_sec`, `*_Sync_*`, `Sync_*`, `*_Frame_Reused` | not written |

## Postprocessing → `final_N.xlsx`

### Input — `load_raw_excel.py`, `run_postprocessing.step_load`

| Column | Excel | Meaning |
|---|---|---|
| `Meas_X/Y/Z_cm` | not written | Stereo positions from the raw Excel, kept unchanged |
| `X_cm/Y_cm/Z_cm` | Result (after ⑩) | Working position: copy of `Meas_*_cm`, updated by ⑥ and ⑩ |

Raw Excel files with the earlier column names (`Time_sec`, `Status_Top`, `Top_px_u`, `Meas_X`, `Online_X`, …) are still read: the names are converted with `settings.LEGACY_RAW_COLUMNS`.

### ⑥ Outlier removal — `step06_remove_outliers.py`

| Column | Excel | Meaning |
|---|---|---|
| `X_cm/Y_cm/Z_cm` | — | Outliers set to NaN |
| `Outlier_Flag` | Debug | Outlier frame |
| `Missing_Reason` | not written | HAMPEL_OUTLIER for outlier frames |

### ⑦ Anchor snapshot — `step07_freeze_anchors.py`

| Column | Excel | Meaning |
|---|---|---|
| `Anchor_Raw_X/Y/Z`, `Anchor_Raw_Valid` | Debug | Stereo positions after step ⑥, never updated |

### ⑧ Process noise — `step08_estimate_noise.py`

| Value | Excel | Meaning |
|---|---|---|
| `sigma_a` (3 axes) | Summary `Sigma_a_*_cm_per_frame2` | Process noise for step ⑬ |

### ⑨ Recovery mode — `step09_classify_recovery.py`

| Column | Excel | Meaning |
|---|---|---|
| `Recovery_Mode` | Debug | NONE / TOP_RAY (front missing) / FRONT_RAY (top missing) |
| `Recovery_Run_ID` | Plot_Aux | Segment number of one recovery mode |
| `State2` | Debug | DETECTED / SUB / LOST before GRAB labeling (updated in ⑩) |
| `Top_Zone_Supported` | Debug | Top ray passes the work-zone box (Z 3–25 cm) |

### ⑩ Single-view recovery — `step10_recover_missing.py`, `step10_hidden_axis_model.py`

| Column | Excel | Meaning |
|---|---|---|
| `X_cm/Y_cm/Z_cm` | Result | Recovered positions filled in (pre-smoothing final position) |
| `Filled_Type` | Debug | Recovery method per frame; converted to `Coord_Type` in ⑭ |
| `Hidden_Axis_Std_cm` | Result | Std of the estimated axis (blank for STEREO and NONE in Result) |
| `Z_Floor_Applied` | Result | Z fixed at the 3 cm floor |
| `Hidden_Stop_Reason` | Debug | NO_RAW_ANCHOR / STATE_INIT_FAILED / POSTERIOR_STD_LIMIT / MAX_EXTRAP_LEN / RAY_GEOMETRY_FAILURE / FRONT_X_SANITY / RAY_OR_SANITY_FAILURE |
| `Recovery_Applied`, `Hidden_Axis_*`, `Anchor_Left/Right_*`, `Hidden_Episode_ID` | Debug | Recovery diagnostics |

### ⑪ Work zone and GRAB — `step11_zone_and_grab.py`

| Column | Excel | Meaning |
|---|---|---|
| `Coord_State` | Debug | DETECTED(_ZONE) / SUB(_ZONE) / LOST / GRAB; mapped to `State` in ⑭ |
| `In_Zone` | Result | Work-zone flag on pre-smoothing positions |
| `Grab_*` | Debug | GRAB evidence |

### ⑫ Display zone — `step12_display_zone.py`

| Column | Excel | Meaning |
|---|---|---|
| `In_Zone_PreRTS` | not written | Frozen copy of `In_Zone` used to check that later steps do not change it |
| `Display_In_Zone` | Plot_Aux | Plot shading only |
| `Display_Zone_*` | Debug | Bridging diagnostics |

### ⑬ RTS smoothing — `step13_smooth_rts.py`

| Column | Excel | Meaning |
|---|---|---|
| `X_rts/Y_rts/Z_rts` | Debug | RTS output |
| `X_vis_cm/Y_vis_cm/Z_vis_cm` | Plot_Aux | Plot positions (RTS for stereo, recovered values elsewhere) |
| `Vis_Std_X/Y/Z_cm` | Plot_Aux | Plot position std |
| `In_Zone_Final` | Debug | Work-zone flag on plot positions |

### ⑭ Velocity — `step14_velocity.py`

| Column | Excel |
|---|---|
| `Vx/Vy/Vz_cm_s`, `Speed_3D_cm_s` | Result |
| `Vx/Vy/Vz_Source`, `Speed_3D_Source` | Result |
| `Vx/Vy/Vz_obs_cm_s`, `Speed_3D_obs_cm_s` | Result |
| `V_Noise_Ratio`, `V_obs_Noise_Ratio` | Result |
| `State`, `Coord_Type` | Result |
| `V_N_Used`, `V_obs_N_Used` | Debug |

## Intermediate columns

These columns appear only in the Debug sheet (or not at all) and keep their own names: `State2` (⑨–⑩), `Coord_State` (⑪), `Filled_Type` (⑩), `In_Zone_PreRTS` (⑫), `In_Zone_Final` (⑬).
