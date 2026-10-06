"""Notebook prompts and forms: day folder, day settings file (create, edit, save), and trial number."""

import datetime
import html
import json
import os
import re

import ipywidgets as widgets
import yaml
from IPython.display import display

from .. import settings

LAST_DAY_FILE = '/content/drive/MyDrive/.underwater_gripper_last_day.txt'
VIDEO_EXTS = ('.mp4', '.mov', '.avi', '.mkv')

FILE_FIELDS = (
    ('calib_top_npz', 'Top calibration NPZ', ('.npz',), 'top', None),
    ('calib_front_npz', 'Front calibration NPZ', ('.npz',), 'front', None),
    ('top_weights', 'Top YOLO weights', ('.pt',), 'top', None),
    ('front_weights', 'Front YOLO weights', ('.pt',), 'front', None),
    ('top_video', 'Top calibration video', VIDEO_EXTS, 'top', 'calib'),
    ('front_video', 'Front calibration video', VIDEO_EXTS, 'front', 'calib'),
)


def _read_text(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except OSError:
        return ''


def ask_day_folder(memory_file=LAST_DAY_FILE):
    last = _read_text(memory_file)
    subdirs = (settings.TOP_VIDEO_DIR, settings.FRONT_VIDEO_DIR, settings.SETUP_DIR)
    while True:
        hint = f' [Enter: {last}]' if last else ''
        path = input(f'Day folder path{hint}: ').strip().strip('"').strip("'").rstrip('/') or last
        if not path:
            continue
        if not os.path.isdir(path):
            print(f'Folder not found: {path}')
            continue
        missing = [d for d in subdirs if not os.path.isdir(os.path.join(path, d))]
        if missing:
            print(f'Missing subfolders in {path}: {", ".join(missing)}')
            continue
        try:
            with open(memory_file, 'w', encoding='utf-8') as f:
                f.write(path)
        except OSError:
            pass
        print(f'Day folder: {path}')
        return path


def _ranges(numbers):
    parts, start, prev = [], None, None
    for n in numbers:
        if start is None:
            start = prev = n
        elif n == prev + 1:
            prev = n
        else:
            parts.append(f'{start}-{prev}' if prev > start else f'{start}')
            start = prev = n
    if start is not None:
        parts.append(f'{start}-{prev}' if prev > start else f'{start}')
    return ', '.join(parts)


def ask_trial(day):
    trials = settings.available_trials(day)
    if trials:
        print(f'Trials in {settings.TOP_VIDEO_DIR}/: {_ranges(trials)}')
    while True:
        found = re.findall(r'\d+', input('Trial number (e.g. 1 for t1 / f1): '))
        if found:
            return int(found[-1])
        print('Enter the trial number, e.g. 1.')


def _setup_files(day, exts):
    folder = os.path.join(day, settings.SETUP_DIR)
    return [f'{settings.SETUP_DIR}/{n}' for n in sorted(os.listdir(folder))
            if not n.startswith('.') and os.path.splitext(n)[1].lower() in exts]


def _guess(options, role, extra):
    other = 'front' if role == 'top' else 'top'
    hits = [o for o in options
            if role in os.path.basename(o).lower() and other not in os.path.basename(o).lower()
            and (extra is None or extra in os.path.basename(o).lower())]
    return hits[0] if len(hits) == 1 else None


def _set_value(text, key, value):
    pattern = re.compile(rf'^([ \t]*){re.escape(key)}:[ \t]*[^#\n]*?([ \t]*#.*)?$', re.M)
    if len(pattern.findall(text)) != 1:
        return None
    return pattern.sub(lambda m: f'{m.group(1)}{key}: {value}' + (f'  {m.group(2).strip()}' if m.group(2) else ''), text)


def _apply_values(text, values):
    for key, value in values.items():
        text = _set_value(text, key, value)
        if text is None:
            return None
    return text


def _get(cfg, *keys, default=None):
    node = cfg
    for k in keys:
        if not isinstance(node, dict) or k not in node:
            return default
        node = node[k]
    return node


def _pre(text):
    return widgets.HTML(f'<pre style="margin:0">{html.escape(text)}</pre>')


def _edit_full_file(path, day, template_path, view, calib):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    box = widgets.Textarea(value=text, continuous_update=False,
                           layout=widgets.Layout(width='100%', height='600px'))
    box.add_class('settings-editor')
    status = widgets.HTML('Changes are saved when you click outside the box.')
    back = widgets.Button(description='Back to summary')
    back.on_click(lambda _: _show_summary(path, day, template_path, view, calib))

    def save(change):
        try:
            yaml.safe_load(change['new'])
        except yaml.YAMLError as e:
            status.value = f'<b style="color:#d33">Not saved (YAML error):</b> {html.escape(str(e))}'
            return
        with open(path, 'w', encoding='utf-8') as f:
            f.write(change['new'])
        status.value = f'<b style="color:#2a2">Saved</b> {datetime.datetime.now():%H:%M:%S}'

    box.observe(save, names='value')
    view.children = [
        widgets.HTML('<style>.settings-editor textarea{font-family:monospace;font-size:13px}</style>'),
        box, status, back,
    ]


def _show_summary(path, day, template_path, view, calib, note=''):
    with open(path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f) or {}
    rows = [('Settings file', path),
            ('Water height [cm]', _get(cfg, 'water', 'surface_z_cm')),
            ('Motor center in ID0 [cm]', _get(cfg, 'setup', 'motor_center_in_id0_cm')),
            ('YOLO class names', _get(cfg, 'models', 'target_class_names'))]
    for key, label, _, _, _ in _fields(calib):
        section = 'calibration' if key.endswith('_video') else 'inputs'
        rows.append((label, _get(cfg, section, key)))
    width = max(len(r[0]) for r in rows)
    edit = widgets.Button(description='Edit settings')
    full = widgets.Button(description='Edit full file')
    edit.on_click(lambda _: _show_form(path, day, template_path, view, calib))
    full.on_click(lambda _: _edit_full_file(path, day, template_path, view, calib))
    text = '\n'.join(f'{k:<{width}} : {v}' for k, v in rows)
    text += (f'\n\n{note}' if note else '') + '\n\nSettings are ready. Run cell 1, or edit them with the buttons.'
    view.children = [_pre(text), widgets.HBox([edit, full])]


def _show_form(path, day, template_path, view, calib, intro=''):
    exists = os.path.exists(path)
    with open(path if exists else template_path, 'r', encoding='utf-8') as f:
        base = f.read()
    cfg = yaml.safe_load(base) or {}
    style = {'description_width': '190px'}
    wide = widgets.Layout(width='620px')

    water = widgets.Text(value=str(_get(cfg, 'water', 'surface_z_cm', default='')) if exists else '',
                         placeholder='required', description='Water height [cm]', style=style, layout=wide)
    motor = [widgets.FloatText(value=float(v), layout=widgets.Layout(width='110px'))
             for v in _get(cfg, 'setup', 'motor_center_in_id0_cm', default=[0.0, 0.0, 0.0])]
    motor_row = widgets.HBox([widgets.Label('Motor center X, Y, Z [cm]', layout=widgets.Layout(width='196px'))] + motor)
    classes = widgets.Text(value=', '.join(_get(cfg, 'models', 'target_class_names', default=[])),
                           description='YOLO class names', style=style, layout=wide)
    files = {}
    for key, label, exts, role, extra in _fields(calib):
        section = 'calibration' if key.endswith('_video') else 'inputs'
        options = _setup_files(day, exts)
        current = _get(cfg, section, key, default='')
        value = current if exists else (_guess(options, role, extra) or current)
        files[key] = (section, widgets.Combobox(value=value, options=options, ensure_option=False,
                                                description=label, style=style, layout=wide))
    video = widgets.Checkbox(value=bool(_get(cfg, 'video', 'save_annotated_video', default=True)),
                             description='Save annotated video (video_N.mp4)', indent=False,
                             layout=widgets.Layout(width='620px', margin='0 0 0 196px'))
    save = widgets.Button(description='Save', button_style='primary')
    status = widgets.HTML()

    def on_save(_):
        try:
            water_cm = float(water.value)
        except ValueError:
            status.value = '<b style="color:#d33">Enter the water height.</b>'
            return
        names = [c.strip() for c in classes.value.split(',') if c.strip()]
        if not names:
            status.value = '<b style="color:#d33">Enter at least one YOLO class name.</b>'
            return
        values = {
            'surface_z_cm': f'{water_cm:g}',
            'motor_center_in_id0_cm': '[' + ', '.join(f'{w.value:g}' for w in motor) + ']',
            'target_class_names': json.dumps(names, ensure_ascii=False),
            'save_annotated_video': 'true' if video.value else 'false',
        }
        for key, (_, box) in files.items():
            values[key] = json.dumps(box.value.strip(), ensure_ascii=False)
        text = _apply_values(base, values)
        if text is None:
            with open(template_path, 'r', encoding='utf-8') as f:
                text = _apply_values(f.read(), values)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        missing = [box.value for key, (_, box) in files.items()
                   if box.value and not os.path.exists(os.path.join(day, box.value)) and not key.endswith('_npz')]
        note = f'Saved {datetime.datetime.now():%H:%M:%S}.'
        if missing:
            note += ' Not found in the day folder: ' + ', '.join(missing)
        _show_summary(path, day, template_path, view, calib, note)

    save.on_click(on_save)
    header = (intro + '\n' if intro else '') + 'Settings file: ' + path + ('' if exists else ' (new)')
    view.children = [_pre(header), water, motor_row, classes] + [b for _, b in files.values()] + [video, save, status]


def _enable_colab_widgets():
    try:
        from google.colab import output
        output.enable_custom_widget_manager()
    except Exception:
        pass


def _fields(calib):
    return [f for f in FILE_FIELDS if calib or not f[0].endswith('_video')]


def day_settings(day, template_path, calibration=False):
    _enable_colab_widgets()
    path = settings.day_settings_path(day)
    view = widgets.VBox()
    display(view)
    if os.path.exists(path):
        _show_summary(path, day, template_path, view, calibration)
    else:
        _show_form(path, day, template_path, view, calibration,
                   intro='No settings file for this day yet. Fill in the form and click Save.')
    return path
