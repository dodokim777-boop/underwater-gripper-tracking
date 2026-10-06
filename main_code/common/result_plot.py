"""Result plot: position by source (stereo, top-only, front-only), smoothed display line, work-zone and GRAB shading, speed."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


def _spans(ax, t, mask, color, alpha):
    mask = np.asarray(mask, dtype=bool)
    if not mask.any():
        return
    edges = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    dt = float(np.median(np.diff(t))) if len(t) > 1 else 0.0
    for start, stop in zip(edges[::2], edges[1::2]):
        ax.axvspan(t[start] - dt / 2, t[stop - 1] + dt / 2, color=color, alpha=alpha, lw=0)


def plot_result(sheets, title=None):
    res, aux = sheets['Result'], sheets['Plot_Aux']
    t = res['Time_s'].to_numpy(dtype=float)
    coord = res['Coord_Type'].fillna('').astype(str)
    groups = (
        ('Stereo (measured)', coord.eq('STEREO'), 'k'),
        ('Top-only recovered', coord.str.startswith('TOP'), 'tab:blue'),
        ('Front-only recovered', coord.str.startswith('FRONT'), 'tab:green'),
    )
    zone = aux['Display_In_Zone'].fillna(False).to_numpy(dtype=bool)
    grab = res['State'].eq('GRAB').to_numpy()

    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    for ax, axis in zip(axes, 'XYZ'):
        _spans(ax, t, zone, 'gold', 0.18)
        _spans(ax, t, grab, 'tab:red', 0.25)
        for label, mask, color in groups:
            ax.plot(t[mask], res.loc[mask, f'{axis}_cm'], '.', ms=2.5, color=color, label=label, zorder=3)
        ax.plot(aux['Time_s'], aux[f'{axis}_vis_cm'], '-', lw=2.0, color='tab:orange', alpha=0.45,
                label='Smoothed (display only)', zorder=2)
        ax.set_ylabel(f'{axis} [cm]')
        ax.grid(alpha=.3)
    _spans(axes[3], t, zone, 'gold', 0.18)
    _spans(axes[3], t, grab, 'tab:red', 0.25)
    axes[3].plot(t, res['Speed_3D_cm_s'], lw=.8, color='k')
    axes[3].set_ylabel('Speed 3D [cm/s]')
    axes[3].grid(alpha=.3)
    axes[3].set_xlabel('Time [s]')

    handles, labels = axes[0].get_legend_handles_labels()
    handles += [Patch(color='gold', alpha=0.4), Patch(color='tab:red', alpha=0.4)]
    labels += ['Work zone', 'GRAB']
    fig.legend(handles, labels, loc='lower center', ncol=6, markerscale=4, frameon=False)
    if title:
        fig.suptitle(title)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    plt.show()
    return fig
