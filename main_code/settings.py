"""All constants, day settings loading, trial video search, and checks; the day settings file overrides [A], [B], and [C] (advanced)."""

import copy
import os
import re

import cv2
import numpy as np

# ============================================================
# [A] Run values (day folder, trial number, and day settings file)
# ============================================================
DATA_ROOT = None
OUTPUT_DIR = None
RUN_NUMBER = None
TEST_RUN = False
TOP_VIDEO_DIR = 'Top'
FRONT_VIDEO_DIR = 'Front'
SETUP_DIR = 'setup'
DAY_SETTINGS_NAME = 'experiment_settings.yaml'

TOP_VIDEO_PATH = None
FRONT_VIDEO_PATH = None
TOP_MODEL_PATH = None
FRONT_MODEL_PATH = None
MANUAL_CALIB_TOP_PATH = None
MANUAL_CALIB_FRONT_PATH = None

RAW_EXCEL = None
FINAL_EXCEL = None
ANNOTATED_VIDEO_PATH = None
VERIFY_IMAGE_PATH = None

WATER_SURFACE_Z_CM = 67.0

TOP_TIME_OFFSET_SEC = 0.0
FRONT_TIME_OFFSET_SEC = 0.0

CALIB_TOP_VIDEO_PATH = None
CALIB_FRONT_VIDEO_PATH = None
CALIB_FRAME_INDEX = 0
CALIB_FRONT_USE_WALL_TRANSFORM = False
CALIB_FRONT_PICK_RIGHTMOST = True

# ============================================================
# [B] Equipment values (change only when the setup changes)
# ============================================================
EXPECTED_RESOLUTION = (1920, 1080)
EXPECTED_FPS = 59.94

MARKER_SIZE_CM = 15.0
ARUCO_DICT_TYPE = cv2.aruco.DICT_4X4_50

TOP_CAMERA_MODEL = "GoPro HERO13 Black"
FRONT_CAMERA_MODEL = "Insta360 Ace Pro 2"
K_MATRIX_TOP = np.array([
    [1.04157146e+03, 0.0, 9.49734448e+02],
    [0.0, 1.04797285e+03, 5.51602202e+02],
    [0.0, 0.0, 1.0],
], dtype=float)
DIST_COEFFS_TOP = np.array([
    [0.03618997, -0.04817693, -0.00320361, -0.00075223, 0.02632374]
], dtype=float)
K_MATRIX_FRONT = np.array([
    [734.42834248, 0.0, 958.12885964],
    [0.0, 738.92389777, 536.16766245],
    [0.0, 0.0, 1.0],
], dtype=float)
DIST_COEFFS_FRONT = np.array([
    [1.51047198e-02, -8.55712758e-03, -1.38100761e-03,
     1.74587731e-05, 5.72933769e-03]
], dtype=float)

R_FW = np.array([[1, 0, 0],
                 [0, 0, 1],
                 [0, -1, 0]], dtype=float)
t_FW = np.array([52.0, -15.5, -10]).reshape(3, 1)

N_AIR = 1.0
N_WATER = 1.333
FRONT_WALL_Y_CM = -11.6
INTERFACE_FRONT = None
INTERFACE_TOP = None

MOTOR_CENTER_IN_ID0_CM = np.array([-26.5, 28.0, 17.1], dtype=float)

TARGET_CLASS_NAMES = ('whitecube',)

# ============================================================
# [C] Algorithm constants (modify with caution: results change)
# ============================================================
HEADLESS = True
DATASET_IS_WET = True
ENABLE_REFRACTION = True
FPS_TOLERANCE = 0.10
STRICT_VIDEO_FORMAT = True
VERIFY_UNIFICATION = True

SYNC_OUTPUT_FPS = None
SYNC_METHOD = 'nearest_timestamp'
SYNC_MAX_ERROR_SEC = None
SYNC_MAX_ERROR_FRAME_FRACTION = 0.60

SAVE_ANNOTATED_VIDEO = True
ANNOTATED_VIDEO_SCALE = 0.5
ANNOTATED_VIDEO_FPS = None

TOP_ZONE_W_CM = 50.0
TOP_ZONE_H_CM = 50.0
FRONT_ZONE_W_CM = 50.0
FRONT_ZONE_ABOVE_CM = 25.0
FRONT_ZONE_BELOW_CM = 5.0

CONF_CUT = 0.4
YOLO_IMGSZ = 640

SIG_GATE_MEAS = np.array([0.12, 0.11, 0.27], dtype=float)
SIGMA_A_ONLINE = 0.10
GATE_CHI2 = 11.34

JUMP_LIMIT_CM_PER_FRAME = 2.0
JUMP_LIMIT_ABS_CM = 30.0

RAY_GAP_MAX_CM = 7.0

CONFIRM_N, CONFIRM_M = 10, 7
MAX_BOTH_LOST_FRAMES = 30
MAX_STEREO_NO_ACCEPT_FRAMES = 150
MAX_REJECT_STREAK = 10

HAMPEL_K = 15
HAMPEL_NSIGMA = 3.5
HAMPEL_ABS_FLOOR = np.array([0.50, 0.50, 0.30], dtype=float)

SIGMA_A_FALLBACK = np.array([0.030, 0.030, 0.025], dtype=float)

ANCHOR_SEARCH_INITIAL = 30
ANCHOR_SEARCH_EXTENDED = 60
ANCHOR_MODEL_MIN_POINTS = 3

HIDDEN_EPISODE_LINK_MAX = 60
HIDDEN_REACQUIRE_MIN_CONSECUTIVE_RAW = 5

HIDDEN_AXIS_MOTION_MODEL = 'CLEAN_LINEAR__INTERMITTENT_1D_KALMAN_RTS'
HIDDEN_HUBER_K = 1.345
HIDDEN_Q_SCALE_Z = 0.3
HIDDEN_Q_SCALE_Y = 0.03

HIDDEN_STD_STOP_Z_CM = 6.0
HIDDEN_STD_STOP_Y_CM = 2.0
HIDDEN_STD_STOP_THRESHOLDS_FINALIZED = True

V_MAX_Z = 0.50
V_MAX_Y = 0.10
V_MAX_X_FRONT_RAY = 0.10
FRONT_X_SANITY_MARGIN = 2.0

MAX_EXTRAP_LEN = 150
TOP_ZONE_MAX_EXTRAP_LEN = 300

ZONE_X_HALF = 25.0
ZONE_Y_HALF = 25.0
ZONE_Z_LOW = 0.0
ZONE_Z_HIGH = 25.0

ZONE_TRACK_CENTER_Z_FLOOR = 3.0

GRAB_MIN = 60

DISPLAY_ZONE_BRIDGE_MAX = 7
DISPLAY_ZONE_STABLE_SEARCH = 30
DISPLAY_ZONE_STABLE_MIN_POINTS_PER_SIDE = 3

SIG_RTS_RAW = np.array([0.12, 0.11, 0.27], dtype=float)
SIG_RTS_RECON_TOP = np.array([0.10, 0.10, 0.30], dtype=float)
SIG_RTS_RECON_FRONT = np.array([0.10, 0.10, 0.30], dtype=float)
SIG_RTS_RECON_TOP_FINALIZED = True
SIG_RTS_RECON_FRONT_FINALIZED = True

VEL_HALF_WINDOW = 5
VEL_MAX_NOISE_RATIO = 2.0
VEL_MAX_CENTER_OFFSET_FRAMES = 2.0
VEL_FALLBACK_FPS = 59.94
VEL_SOURCE_LABELS = ['OBSERVED', 'RAY_CONSTRAINED', 'MODEL_INTERP', 'MODEL_EXTRAP']
VEL_SLOW_PHASE_FLUCTUATION_NOTE = (
    'Slow-phase 3D speed fluctuation about 0.55–1.24 cm/s '
    '(upper bound estimated from 6 moving videos)'
)

MEAS_COLS = ['X_cm', 'Y_cm', 'Z_cm']
RAW_MEAS_COLS = ['Meas_X_cm', 'Meas_Y_cm', 'Meas_Z_cm']

RECOVERY_NONE = 'NONE'
RECOVERY_TOP_RAY = 'TOP_RAY'
RECOVERY_FRONT_RAY = 'FRONT_RAY'

RESULT_STATE_MAP = {
    'DETECTED': 'DETECTED',
    'DETECTED_ZONE': 'DETECTED',
    'SUB': 'RECOVERED',
    'SUB_ZONE': 'RECOVERED',
    'LOST': 'LOST',
    'GRAB': 'GRAB',
}

LEGACY_RAW_COLUMNS = {
    'Time_sec': 'Time_s',
    'Status_Top': 'Top_Status',
    'Status_Front': 'Front_Status',
    'Top_conf': 'Top_Conf',
    'Front_conf': 'Front_Conf',
    'Top_px_u': 'Top_U_px',
    'Top_px_v': 'Top_V_px',
    'Front_px_u': 'Front_U_px',
    'Front_px_v': 'Front_V_px',
    'Meas_X': 'Meas_X_cm',
    'Meas_Y': 'Meas_Y_cm',
    'Meas_Z': 'Meas_Z_cm',
    'Candidate_X': 'Candidate_X_cm',
    'Candidate_Y': 'Candidate_Y_cm',
    'Candidate_Z': 'Candidate_Z_cm',
    'Candidate_ON_X': 'Candidate_ON_X_cm',
    'Candidate_ON_Y': 'Candidate_ON_Y_cm',
    'Candidate_ON_Z': 'Candidate_ON_Z_cm',
    'Candidate_OFF_X': 'Candidate_OFF_X_cm',
    'Candidate_OFF_Y': 'Candidate_OFF_Y_cm',
    'Candidate_OFF_Z': 'Candidate_OFF_Z_cm',
    'Ray_s_Top_cm': 'Top_Ray_Dist_cm',
    'Ray_s_Front_cm': 'Front_Ray_Dist_cm',
    'Online_X': 'KF_X_cm',
    'Online_Y': 'KF_Y_cm',
    'Online_Z': 'KF_Z_cm',
    'KF_PosStd_X': 'KF_Std_X_cm',
    'KF_PosStd_Y': 'KF_Std_Y_cm',
    'KF_PosStd_Z': 'KF_Std_Z_cm',
}

RAW_SHEET_COLUMNS = {
    'Trajectory': [
        'Frame', 'Time_s', 'Top_Status', 'Front_Status', 'Top_Conf', 'Front_Conf',
        'Top_U_px', 'Top_V_px', 'Front_U_px', 'Front_V_px',
        'Meas_X_cm', 'Meas_Y_cm', 'Meas_Z_cm', 'Meas_Status', 'Missing_Reason', 'Ray_Gap_cm',
    ],
    'Triangulation': [
        'Frame', 'Candidate_X_cm', 'Candidate_Y_cm', 'Candidate_Z_cm',
        'Candidate_ON_X_cm', 'Candidate_ON_Y_cm', 'Candidate_ON_Z_cm',
        'Candidate_OFF_X_cm', 'Candidate_OFF_Y_cm', 'Candidate_OFF_Z_cm',
        'Geometry_Status_ON', 'Geometry_Status_OFF',
        'Top_Ray_Dist_cm', 'Front_Ray_Dist_cm', 'Ray_Gap_ON_cm', 'Ray_Gap_OFF_cm',
    ],
    'Online_Filter': [
        'Frame', 'Track_State', 'KF_Updated', 'KF_X_cm', 'KF_Y_cm', 'KF_Z_cm',
        'KF_Std_X_cm', 'KF_Std_Y_cm', 'KF_Std_Z_cm',
    ],
}

RAW_EXCLUDED_COLUMNS = [
    'Sig_X', 'Sig_Y', 'Sig_Z', 'Tracker_Ref_Frame',
    'Top_Source_Frame', 'Front_Source_Frame', 'Top_Time_sec', 'Front_Time_sec',
    'Top_Sync_Time_sec', 'Front_Sync_Time_sec', 'Sync_Error_ms', 'Sync_Abs_Error_ms',
    'Sync_Status', 'Top_Frame_Reused', 'Front_Frame_Reused',
]

OUTPUT_FILES = {
    'RAW_EXCEL': ('raw', '.xlsx'),
    'FINAL_EXCEL': ('final', '.xlsx'),
    'ANNOTATED_VIDEO_PATH': ('video', '.mp4'),
    'VERIFY_IMAGE_PATH': ('setup', '.png'),
}
CONFIG_SNAPSHOT_NAME = 'config.yaml'


def _rebuild_derived():
    g = globals()
    g['INTERFACE_FRONT'] = {
        'axis': 1, 'value': FRONT_WALL_Y_CM,
        'normal_to_air': np.array([0.0, -1.0, 0.0]),
    }
    g['INTERFACE_TOP'] = {
        'axis': 2, 'value': WATER_SURFACE_Z_CM,
        'normal_to_air': np.array([0.0, 0.0, 1.0]),
    }
    for key, (stem, ext) in OUTPUT_FILES.items():
        if not OUTPUT_DIR:
            g[key] = None
        elif TEST_RUN:
            g[key] = os.path.join(OUTPUT_DIR, f'test_{stem}{ext}')
        elif RUN_NUMBER is not None:
            g[key] = os.path.join(OUTPUT_DIR, f'{stem}_{RUN_NUMBER}{ext}')
        else:
            g[key] = None


_rebuild_derived()

_DEFAULTS = {
    k: copy.deepcopy(v) for k, v in globals().items()
    if (k.isupper() or k == 't_FW') and not k.startswith('_')
}


_CONFIG_MAP = {
    ('experiment', 'data_root'): 'DATA_ROOT',
    ('inputs', 'top_video'): 'TOP_VIDEO_PATH',
    ('inputs', 'front_video'): 'FRONT_VIDEO_PATH',
    ('inputs', 'top_weights'): 'TOP_MODEL_PATH',
    ('inputs', 'front_weights'): 'FRONT_MODEL_PATH',
    ('inputs', 'calib_top_npz'): 'MANUAL_CALIB_TOP_PATH',
    ('inputs', 'calib_front_npz'): 'MANUAL_CALIB_FRONT_PATH',
    ('water', 'surface_z_cm'): 'WATER_SURFACE_Z_CM',
    ('sync', 'top_time_offset_sec'): 'TOP_TIME_OFFSET_SEC',
    ('sync', 'front_time_offset_sec'): 'FRONT_TIME_OFFSET_SEC',
    ('calibration', 'top_video'): 'CALIB_TOP_VIDEO_PATH',
    ('calibration', 'front_video'): 'CALIB_FRONT_VIDEO_PATH',
    ('calibration', 'frame_index'): 'CALIB_FRAME_INDEX',
    ('calibration', 'front_use_wall_transform'): 'CALIB_FRONT_USE_WALL_TRANSFORM',
    ('calibration', 'front_pick_rightmost'): 'CALIB_FRONT_PICK_RIGHTMOST',
    ('video', 'expected_resolution'): 'EXPECTED_RESOLUTION',
    ('video', 'expected_fps'): 'EXPECTED_FPS',
    ('video', 'save_annotated_video'): 'SAVE_ANNOTATED_VIDEO',
    ('models', 'target_class_names'): 'TARGET_CLASS_NAMES',
    ('cameras', 'top', 'model'): 'TOP_CAMERA_MODEL',
    ('cameras', 'top', 'K'): 'K_MATRIX_TOP',
    ('cameras', 'top', 'dist'): 'DIST_COEFFS_TOP',
    ('cameras', 'front', 'model'): 'FRONT_CAMERA_MODEL',
    ('cameras', 'front', 'K'): 'K_MATRIX_FRONT',
    ('cameras', 'front', 'dist'): 'DIST_COEFFS_FRONT',
    ('setup', 'marker_size_cm'): 'MARKER_SIZE_CM',
    ('setup', 'motor_center_in_id0_cm'): 'MOTOR_CENTER_IN_ID0_CM',
    ('setup', 'front_wall_y_cm'): 'FRONT_WALL_Y_CM',
    ('setup', 'front_wall_marker_R'): 'R_FW',
    ('setup', 'front_wall_marker_t'): 't_FW',
}

_PATH_KEYS = (
    'TOP_VIDEO_PATH', 'FRONT_VIDEO_PATH', 'TOP_MODEL_PATH', 'FRONT_MODEL_PATH',
    'MANUAL_CALIB_TOP_PATH', 'MANUAL_CALIB_FRONT_PATH',
    'CALIB_TOP_VIDEO_PATH', 'CALIB_FRONT_VIDEO_PATH',
)


def _coerce_like(name, value, default):
    if value is None:
        return None
    if isinstance(default, np.ndarray):
        arr = np.asarray(value, dtype=float)
        if arr.size != default.size:
            raise ValueError(f'{name}: expected {default.size} values, got {arr.size}.')
        return arr.reshape(default.shape)
    if isinstance(default, tuple):
        return tuple(value) if isinstance(value, (list, tuple)) else (value,)
    if isinstance(default, bool):
        return bool(value)
    if isinstance(default, float):
        return float(value)
    if isinstance(default, int) and not isinstance(default, bool):
        return int(value)
    return value


def _get_nested(cfg, keys):
    node = cfg
    for k in keys:
        if not isinstance(node, dict) or k not in node:
            return False, None
        node = node[k]
    return True, node


def _resolve_path(path):
    if path is None or str(path).strip() == '':
        return None
    path = os.path.expanduser(str(path))
    if os.path.isabs(path) or DATA_ROOT is None:
        return path
    return os.path.join(DATA_ROOT, path)


def reset_defaults():
    globals().update(copy.deepcopy(_DEFAULTS))
    _rebuild_derived()


def apply_config(cfg, trial=None):
    reset_defaults()
    g = globals()
    for keys, name in _CONFIG_MAP.items():
        found, value = _get_nested(cfg, keys)
        if found and value is not None:
            g[name] = _coerce_like(name, value, _DEFAULTS.get(name))

    for name, value in (cfg.get('advanced') or {}).items():
        if name not in _DEFAULTS:
            raise KeyError(f'advanced: unknown setting name: {name}')
        g[name] = _coerce_like(name, value, _DEFAULTS[name])

    for name in _PATH_KEYS:
        g[name] = _resolve_path(g[name])

    output_root = (cfg.get('outputs') or {}).get('output_root', 'result')
    if DATA_ROOT or os.path.isabs(str(output_root)):
        g['OUTPUT_DIR'] = _resolve_path(output_root)
    g['_VIDEO_CANDIDATES'] = {}
    if trial is not None:
        for role, folder in (('top', TOP_VIDEO_DIR), ('front', FRONT_VIDEO_DIR)):
            found = find_trial_videos(_resolve_path(folder), trial)
            g['_VIDEO_CANDIDATES'][role] = found
            g[f'{role.upper()}_VIDEO_PATH'] = found[0] if len(found) == 1 else None
        g['RUN_NUMBER'] = int(trial)
    else:
        g['RUN_NUMBER'] = trial_number(TOP_VIDEO_PATH)
    _rebuild_derived()


_VIDEO_CANDIDATES = {}


def find_trial_videos(folder, trial):
    if not folder or not os.path.isdir(folder):
        return []
    return [os.path.join(folder, n) for n in sorted(os.listdir(folder))
            if not n.startswith('.') and trial_number(n) == int(trial)]


def available_trials(data_root):
    folder = os.path.join(data_root, TOP_VIDEO_DIR)
    if not os.path.isdir(folder):
        return []
    return sorted({trial_number(n) for n in os.listdir(folder)
                   if not n.startswith('.') and trial_number(n) is not None})


def day_settings_path(data_root):
    return os.path.join(data_root, SETUP_DIR, DAY_SETTINGS_NAME)


def trial_number(path):
    if not path:
        return None
    stem = os.path.splitext(os.path.basename(str(path)))[0]
    found = re.findall(r'\d+', stem)
    return int(found[-1]) if found else None


def set_test_run(test):
    globals()['TEST_RUN'] = bool(test)
    _rebuild_derived()


def load_config_file(path):
    import yaml
    with open(path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f) or {}
    return cfg


def configure(config_path, make_output_dir=True, data_root=None, trial=None):
    cfg = load_config_file(config_path)
    if data_root:
        cfg.setdefault('experiment', {})['data_root'] = data_root
    apply_config(cfg, trial=trial)
    if make_output_dir and OUTPUT_DIR:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        save_snapshot(os.path.join(OUTPUT_DIR, CONFIG_SNAPSHOT_NAME))
    return cfg


SNAPSHOT_EXCLUDED = (
    'DATA_ROOT', 'OUTPUT_DIR', 'RUN_NUMBER', 'TEST_RUN',
    'TOP_VIDEO_DIR', 'FRONT_VIDEO_DIR', 'SETUP_DIR', 'DAY_SETTINGS_NAME',
    'TOP_VIDEO_PATH', 'FRONT_VIDEO_PATH', 'TOP_MODEL_PATH', 'FRONT_MODEL_PATH',
    'MANUAL_CALIB_TOP_PATH', 'MANUAL_CALIB_FRONT_PATH', 'CALIB_TOP_VIDEO_PATH', 'CALIB_FRONT_VIDEO_PATH',
    'RAW_EXCEL', 'FINAL_EXCEL', 'ANNOTATED_VIDEO_PATH', 'VERIFY_IMAGE_PATH',
    'OUTPUT_FILES', 'CONFIG_SNAPSHOT_NAME',
)


def snapshot():
    out = {}
    for k in _DEFAULTS:
        if k in SNAPSHOT_EXCLUDED:
            continue
        v = globals()[k]
        if isinstance(v, np.ndarray):
            v = v.tolist()
        elif isinstance(v, tuple):
            v = list(v)
        elif isinstance(v, dict):
            v = {kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv) for kk, vv in v.items()}
        out[k] = v
    return out


def save_snapshot(path):
    import yaml
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(snapshot(), f, allow_unicode=True, sort_keys=False)


REQUIRED_KEYS_BY_STAGE = {
    'calibration': ['DATA_ROOT'],
    'preprocessing': ['DATA_ROOT', 'TOP_VIDEO_PATH', 'FRONT_VIDEO_PATH',
               'TOP_MODEL_PATH', 'FRONT_MODEL_PATH',
               'MANUAL_CALIB_TOP_PATH', 'MANUAL_CALIB_FRONT_PATH'],
    'postprocessing': ['DATA_ROOT', 'TOP_VIDEO_PATH', 'FRONT_VIDEO_PATH',
                    'MANUAL_CALIB_TOP_PATH', 'MANUAL_CALIB_FRONT_PATH'],
}

FILES_BY_STAGE = {
    'calibration': [],
    'preprocessing': ['TOP_VIDEO_PATH', 'FRONT_VIDEO_PATH', 'TOP_MODEL_PATH', 'FRONT_MODEL_PATH',
               'MANUAL_CALIB_TOP_PATH', 'MANUAL_CALIB_FRONT_PATH'],
    'postprocessing': ['MANUAL_CALIB_TOP_PATH', 'MANUAL_CALIB_FRONT_PATH', 'RAW_EXCEL'],
}


def check(stage):
    problems = []
    g = globals()
    for name in REQUIRED_KEYS_BY_STAGE[stage]:
        if name in ('TOP_VIDEO_PATH', 'FRONT_VIDEO_PATH') and _VIDEO_CANDIDATES:
            continue
        if g.get(name) in (None, ''):
            problems.append(f'{name} is empty (check experiment_settings.yaml).')
    for name in FILES_BY_STAGE[stage]:
        path = g.get(name)
        if path and not os.path.exists(path):
            hint = ''
            if name == 'RAW_EXCEL':
                hint = ' (run 02_run_trial first)'
            elif name.startswith('MANUAL_CALIB'):
                hint = ' (run 01_calibration first)'
            problems.append(f'{name} not found: {path}{hint}')
    if stage == 'calibration':
        for role in ('top', 'front'):
            path = g.get(f'CALIB_{role.upper()}_VIDEO_PATH') or g.get(f'{role.upper()}_VIDEO_PATH')
            if not path or not os.path.exists(path):
                problems.append(f'Calibration {role} video not found: {path} '
                                f'(calibration.{role}_video, or inputs.{role}_video if empty)')
    for role, found in _VIDEO_CANDIDATES.items():
        folder = TOP_VIDEO_DIR if role == 'top' else FRONT_VIDEO_DIR
        if not found:
            problems.append(f'No {role} video with trial number {RUN_NUMBER} in {folder}/')
        elif len(found) > 1:
            names = ', '.join(os.path.basename(f) for f in found)
            problems.append(f'Several {role} videos with trial number {RUN_NUMBER} in {folder}/: {names}')
    if stage in ('preprocessing', 'postprocessing') and TOP_VIDEO_PATH and FRONT_VIDEO_PATH:
        n_top, n_front = trial_number(TOP_VIDEO_PATH), trial_number(FRONT_VIDEO_PATH)
        if n_top is None or n_front is None:
            problems.append('Video file names must contain the trial number (e.g. Top/top1.mp4, Front/front1.mp4).')
        elif n_top != n_front:
            problems.append(f'Trial numbers differ: top {n_top}, front {n_front}.')
    if not (20.0 <= float(WATER_SURFACE_Z_CM) <= 150.0):
        problems.append(f'WATER_SURFACE_Z_CM={WATER_SURFACE_Z_CM}: check the water height above the floor [cm]')
    if K_MATRIX_TOP.shape != (3, 3) or K_MATRIX_FRONT.shape != (3, 3):
        problems.append('Camera K matrices must be 3x3.')
    if problems:
        msg = '\n'.join(f'  - {p}' for p in problems)
        raise RuntimeError(f'[{stage}] settings check failed:\n{msg}')
    print(f'[{stage}] settings check passed')


def print_summary(stage=None):
    rows = [
        ('Results folder', OUTPUT_DIR),
        ('Trial number', RUN_NUMBER),
        ('Top video', TOP_VIDEO_PATH),
        ('Front video', FRONT_VIDEO_PATH),
        ('Top YOLO weights', TOP_MODEL_PATH),
        ('Front YOLO weights', FRONT_MODEL_PATH),
        ('Top calibration NPZ', MANUAL_CALIB_TOP_PATH),
        ('Front calibration NPZ', MANUAL_CALIB_FRONT_PATH),
        ('Water height [cm]', WATER_SURFACE_Z_CM),
        ('Time offset top/front [s]', f'{TOP_TIME_OFFSET_SEC} / {FRONT_TIME_OFFSET_SEC}'),
        ('Motor center in ID0 [cm]', MOTOR_CENTER_IN_ID0_CM.tolist()),
    ]
    if stage == 'calibration':
        rows += [
            ('Calibration top video', CALIB_TOP_VIDEO_PATH or TOP_VIDEO_PATH),
            ('Calibration front video', CALIB_FRONT_VIDEO_PATH or FRONT_VIDEO_PATH),
            ('Calibration frame', CALIB_FRAME_INDEX),
            ('Front wall marker transform', CALIB_FRONT_USE_WALL_TRANSFORM),
        ]
    width = max(len(r[0]) for r in rows)
    for k, v in rows:
        print(f'{k:<{width}} : {v}')
