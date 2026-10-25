"""Optional maintainer tool: render the archived samples with matplotlib."""
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from summarize_telemetry import summarize

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = 'ROG_G635LX_调校证据.zip'
MEMBER = 'tuning/baseline-auto-1/telemetry.csv'


def main():
    with zipfile.ZipFile(ROOT / ARCHIVE) as archive:
        raw = archive.read(MEMBER)
    text = raw.decode('utf-8-sig')
    rows = list(csv.DictReader(io.StringIO(text)))
    summary = summarize(text)
    times = [datetime.fromisoformat(row['timestamp'].replace('/', '-')) for row in rows]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'svg.hashsalt': 'gpu-diagnostics'})
    figure = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor='#f5f8fc')
    figure.text(.065, .935, 'LAPTOP GPU DIAGNOSTICS', fontsize=11, weight='bold', color='#31566d')
    figure.text(.065, .825, '55W during standby. What changed after wake?', fontsize=23,
                weight='bold', color='#132b40')
    figure.text(.065, .765, 'A recorded G635LX / RTX 5090 Laptop case — inspect the samples, not just the target.',
                fontsize=12, color='#435c70')
    axis = figure.add_axes((.075, .22, .86, .48), facecolor='white')
    axis.scatter(times, [float(row['limit_W']) for row in rows], s=19, marker='s',
                 color='#bd5800', label='Effective power limit (W)', zorder=3)
    axis.scatter(times, [float(row['power_W']) for row in rows], s=15,
                 color='#007b83', label='Measured power draw (W)', zorder=2)
    wake = datetime(2026, 10, 19, 20, 12, 58)
    axis.axvline(wake, color='#5b6575', linestyle='--', linewidth=1)
    axis.text(wake, 202, ' Wake ~20:12:58', fontsize=10, color='#435c70')
    axis.set_ylim(0, 215)
    axis.set_ylabel('Watts')
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    axis.set_xlabel('Recorded sample time · October 19, 2026 · UTC+8', fontsize=10)
    axis.grid(axis='y', alpha=.16)
    axis.spines[['top', 'right']].set_visible(False)
    axis.legend(loc='upper left', frameon=False, fontsize=10)
    figure.text(.075, .105,
                f'{summary["samples"]} samples / {summary["sample_span_seconds"]:.3f}s   ·   '
                f'First {summary["limit_segments"][0]["samples"]} limit samples: 55W   ·   Read-only Python analysis',
                fontsize=11, color='#132b40', weight='bold')
    figure.text(.075, .055, 'Dots are samples, not proof of continuous operation. No FPS gain or stable 225W result is claimed.',
                fontsize=10, color='#435c70')
    assets = ROOT / 'assets'
    assets.mkdir(exist_ok=True)
    for suffix in ('png', 'svg'):
        figure.savefig(assets / f'telemetry-preview.{suffix}', dpi=100,
                       metadata={'Date': None} if suffix == 'svg' else {})
    svg = assets / 'telemetry-preview.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines()) + '\n',
                   encoding='utf-8', newline='\n')
    plt.close(figure)
    provenance = {'archive': ARCHIVE, 'member': MEMBER, 'source_sha256': hashlib.sha256(raw).hexdigest(),
                  'samples': summary['samples'], 'sample_span_seconds': summary['sample_span_seconds'],
                  'image_size': [1280, 640], 'plot': 'Individual recorded samples; no interpolation',
                  'generator': 'tools/render_preview.py',
                  'artifacts': {f'telemetry-preview.{ext}': hashlib.sha256((assets / f'telemetry-preview.{ext}').read_bytes()).hexdigest()
                                for ext in ('png', 'svg')}}
    (assets / 'preview-provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
