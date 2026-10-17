"""Run one trial (steps ①-⑭) or several trials in a row from the day folder."""

import re
import time
import traceback

import pandas as pd

from . import settings


def parse_trials(text):
    trials = set()
    for part in re.split(r'[,\s]+', str(text).strip()):
        if not part:
            continue
        m = re.fullmatch(r'(\d+)\s*[-~]\s*(\d+)', part)
        if m:
            a, b = sorted((int(m.group(1)), int(m.group(2))))
            trials.update(range(a, b + 1))
        elif part.isdigit():
            trials.add(int(part))
        else:
            raise ValueError(f'Cannot read "{part}". Use e.g. 2-10 or 2,4,7.')
    return sorted(trials)


def run_trial(day, trial):
    from .postprocessing import run_postprocessing as P
    from .preprocessing.run_preprocessing import run_preprocessing
    settings.configure(settings.day_settings_path(day), data_root=day, trial=trial)
    settings.check('preprocessing')
    run_preprocessing()
    ctx = P.step_load()
    for step in P.STEPS:
        ctx = step(ctx)
    return P.step_save(ctx)


def run_trials(day, trials, skip_existing=True):
    import os
    rows = []
    for i, trial in enumerate(trials, start=1):
        print(f'\n========== Trial {trial} ({i}/{len(trials)}) ==========')
        settings.configure(settings.day_settings_path(day), make_output_dir=False, data_root=day, trial=trial)
        if skip_existing and settings.FINAL_EXCEL and os.path.exists(settings.FINAL_EXCEL):
            print(f'Skipped: {settings.FINAL_EXCEL} already exists.')
            rows.append({'Trial': trial, 'Status': 'SKIPPED (final exists)', 'Minutes': 0.0, 'Error': ''})
            continue
        start = time.time()
        try:
            run_trial(day, trial)
            rows.append({'Trial': trial, 'Status': 'DONE', 'Minutes': round((time.time() - start) / 60, 1), 'Error': ''})
        except Exception as exc:
            traceback.print_exc()
            lines = [ln.strip().lstrip('- ') for ln in str(exc).splitlines() if ln.strip()]
            if len(lines) > 1 and lines[0].endswith(':'):
                lines = lines[1:]
            rows.append({'Trial': trial, 'Status': 'FAILED', 'Minutes': round((time.time() - start) / 60, 1),
                         'Error': '; '.join(lines)[:300]})
    summary = pd.DataFrame(rows, columns=['Trial', 'Status', 'Minutes', 'Error'])
    print('\n========== Batch summary ==========')
    print(summary.to_string(index=False))
    return summary
