"""Input: read raw_N.xlsx and the calibration NPZ files."""

import cv2
import numpy as np
import pandas as pd

from .. import settings
from ..common.file_utils import _npz_value, reject_wall_transform


def _build_calib(R_cm, t_cm, K, dist, metadata=None):
    R_cm = np.asarray(R_cm, dtype=float).reshape(3, 3)
    t_cm = np.asarray(t_cm, dtype=float).reshape(3, 1)
    R_w, t_w = R_cm, t_cm

    rvec, _ = cv2.Rodrigues(R_w)
    calib = {
        'rvec': rvec,
        'tvec': t_w,
        'cam_matrix': np.asarray(K, dtype=float).reshape(3, 3),
        'dist_coeffs': np.asarray(dist, dtype=float).reshape(1, -1),
    }
    calib.update(metadata or {})
    return calib


def load_calib_top(path=None):
    if path is None:
        path = settings.MANUAL_CALIB_TOP_PATH
    try:
        data = np.load(path, allow_pickle=False)
        if 'R' not in data.files or 't' not in data.files:
            raise KeyError('NPZ must contain R and t')
        stored_model = str(_npz_value(data, ('camera_model',), settings.TOP_CAMERA_MODEL))
        metadata = {
            'camera_role': 'top',
            'camera_model': stored_model,
            'projection_mode': str(_npz_value(data, ('projection_mode',), 'unknown')),
            'intrinsic_rms_px': _npz_value(
                data, ('intrinsic_rms_px', 'rms', 'reprojection_rms_px'), np.nan
            ),
            'intrinsic_source': f'hardcoded: {settings.TOP_CAMERA_MODEL}',
        }
        calib = _build_calib(
            data['R'], data['t'], settings.K_MATRIX_TOP, settings.DIST_COEFFS_TOP,
            metadata=metadata,
        )
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'Top dry-calibration NPZ required: {path}') from exc
    except Exception as exc:
        raise RuntimeError(f'Failed to load top calibration NPZ: {path}: {exc}') from exc
    print(
        f"top calib: {path} | model={calib.get('camera_model', settings.TOP_CAMERA_MODEL)} | "
        f"intrinsic={calib.get('intrinsic_source', 'hardcoded')}"
    )
    return calib


def load_calib_front(path=None):
    if path is None:
        path = settings.MANUAL_CALIB_FRONT_PATH
    try:
        data = np.load(path, allow_pickle=False)
        if 'R' not in data.files or 't' not in data.files:
            raise KeyError('NPZ must contain R and t')
        reject_wall_transform(data, path)
        stored_model = str(_npz_value(data, ('camera_model',), settings.FRONT_CAMERA_MODEL))
        metadata = {
            'camera_role': 'front',
            'camera_model': stored_model,
            'projection_mode': str(_npz_value(data, ('projection_mode',), 'unknown')),
            'intrinsic_rms_px': _npz_value(
                data, ('intrinsic_rms_px', 'rms', 'reprojection_rms_px'), np.nan
            ),
            'intrinsic_source': f'hardcoded: {settings.FRONT_CAMERA_MODEL}',
        }
        calib = _build_calib(
            data['R'], data['t'], settings.K_MATRIX_FRONT, settings.DIST_COEFFS_FRONT,
            metadata=metadata,
        )
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'Front dry-calibration NPZ required: {path}') from exc
    except Exception as exc:
        raise RuntimeError(f'Failed to load front calibration NPZ: {path}: {exc}') from exc
    print(
        f"front calib: {path} | model={calib.get('camera_model', settings.FRONT_CAMERA_MODEL)} | "
        f"intrinsic={calib.get('intrinsic_source', 'hardcoded')}"
    )
    return calib


def read_raw_trajectory(raw_path):
    try:
        df = pd.read_excel(raw_path, sheet_name='Trajectory')
    except ValueError:
        df = pd.read_excel(raw_path)
    df = df[[c for c in df.columns if not str(c).startswith('｜')]].reset_index(drop=True)
    df = df.rename(columns=settings.LEGACY_RAW_COLUMNS)
    return df, set(df.columns)


def ensure_missing_reason(df):
    if 'Missing_Reason' in df.columns:
        df['Missing_Reason'] = df['Missing_Reason'].fillna('NONE').astype(str)
        return df

    reason = np.array(['NONE'] * len(df), dtype=object)
    has_meas = df[settings.RAW_MEAS_COLS].notna().all(axis=1).to_numpy()
    top_ok = df.get('Top_Status', pd.Series(['LOST'] * len(df))).eq('DETECTED').to_numpy()
    front_ok = df.get('Front_Status', pd.Series(['LOST'] * len(df))).eq('DETECTED').to_numpy()
    reason[(~has_meas) & (~top_ok) & (~front_ok)] = 'BOTH_MISSING'
    reason[(~has_meas) & (~top_ok) & front_ok] = 'TOP_MISSING'
    reason[(~has_meas) & top_ok & (~front_ok)] = 'FRONT_MISSING'
    reason[(~has_meas) & top_ok & front_ok] = 'TRIANGULATION_FAILED'
    if 'Meas_Status' in df.columns:
        status_map = {
            'REJECTED_JUMP': 'REJECTED_JUMP',
            'REJECTED_GATE': 'REJECTED_MAHALANOBIS',
            'REJECTED_MAHALANOBIS': 'REJECTED_MAHALANOBIS',
            'TENTATIVE_HOLD': 'TENTATIVE_HOLD',
            'REJECT_STREAK_RESET': 'REJECT_STREAK_RESET',
        }
        for status, mapped in status_map.items():
            mask = df['Meas_Status'].eq(status).to_numpy()
            reason[mask] = mapped
    df['Missing_Reason'] = reason
    return df
