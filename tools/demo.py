"""Print a short, reproducible demo from the preserved evidence archive."""
from pathlib import Path
import zipfile

from summarize_telemetry import summarize

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = 'ROG_G635LX_调校证据.zip'
MEMBER = 'tuning/baseline-auto-1/telemetry.csv'


def main():
    with zipfile.ZipFile(ROOT / ARCHIVE) as archive:
        result = summarize(archive.read(MEMBER).decode('utf-8-sig'))
    first = result['limit_segments'][0]
    print('Recorded G635LX telemetry | October 19, 2026 | UTC+8')
    print(f'Samples: {result["samples"]} over {result["sample_span_seconds"]:.3f} seconds')
    print(f'First limit segment: {first["limit_W"]:g} W across {first["samples"]} samples')
    limit = result['metrics']['limit_W']
    print(f'Recorded limit range: {limit["minimum"]:g}–{limit["maximum"]:g} W')
    print(f'CPU sample maximum: {result["metrics"]["cpu_C"]["maximum"]:g} °C')
    print('Whole-file sample statistics; not sustained-load or FPS results.')
    print('No hardware queries, setting changes, archive extraction, or network access.')


if __name__ == '__main__':
    main()
