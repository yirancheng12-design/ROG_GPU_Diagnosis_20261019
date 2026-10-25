"""Summarize recorded telemetry without querying or changing GPU hardware."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import io
import json
import math
from pathlib import Path
import statistics
import zipfile

FIELDS = ('power_W', 'limit_W', 'gpu_C', 'core_MHz', 'util_percent', 'cpu_C')


def summarize(text: str) -> dict:
    reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff')))
    required = {'timestamp', *FIELDS}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError('Missing columns: ' + ', '.join(sorted(required - set(reader.fieldnames or []))))
    values = {field: [] for field in FIELDS}
    segments, first, previous, samples = [], None, None, 0
    for line, row in enumerate(reader, 2):
        if None in row:
            raise ValueError(f'Row {line}: too many columns')
        try:
            # The historical source uses YYYY/MM/DD; ISO 8601 also works.
            timestamp = datetime.fromisoformat((row.get('timestamp') or '').replace('/', '-'))
            if previous is not None and timestamp <= previous:
                raise ValueError('timestamps must be strictly increasing with a consistent timezone')
        except (ValueError, TypeError) as exc:
            raise ValueError(f'Row {line}: invalid timestamp: {exc}') from exc
        numbers = {}
        for field in FIELDS:
            raw = (row.get(field) or '').strip()
            if raw in {'', 'N/A'}:
                numbers[field] = None
                continue
            try:
                value = float(raw)
                if not math.isfinite(value):
                    raise ValueError('not finite')
            except ValueError as exc:
                raise ValueError(f'Row {line}: invalid {field}') from exc
            numbers[field] = value
            values[field].append(value)
        label = timestamp.isoformat()
        if not segments or segments[-1]['limit_W'] != numbers['limit_W']:
            segments.append({'limit_W': numbers['limit_W'], 'first_sample': label,
                             'last_sample': label, 'samples': 0})
        segments[-1]['last_sample'] = label
        segments[-1]['samples'] += 1
        first = first or timestamp
        previous = timestamp
        samples += 1
    if not samples:
        raise ValueError('No samples: fill the template with actual measurements first')
    metrics = {field: {'available_samples': len(data), 'minimum': min(data) if data else None,
                      'maximum': max(data) if data else None,
                      'mean': statistics.fmean(data) if data else None} for field, data in values.items()}
    return {'samples': samples, 'first_sample': first.isoformat(), 'last_sample': previous.isoformat(),
            'sample_span_seconds': (previous - first).total_seconds(),
            'metrics': metrics, 'limit_segments': segments,
            'interpretation': 'Sample statistics only. Limit is not power draw. Gaps are not interpolated; '
                              'a segment spans recorded samples, not verified continuous operation. '
                              'No causal, FPS-gain, sustained-load, or stability claim is inferred.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--csv', type=Path, help='Recorded CSV using the documented columns')
    source.add_argument('--zip', type=Path, help='Read one CSV member directly, without extraction')
    parser.add_argument('--member', help='Exact CSV member name; required with --zip')
    args = parser.parse_args()
    if bool(args.zip) != bool(args.member):
        parser.error('--member must be supplied with --zip, and only with --zip')
    try:
        if args.zip:
            with zipfile.ZipFile(args.zip) as archive:
                raw = archive.read(args.member)
        else:
            raw = args.csv.read_bytes()
        print(json.dumps(summarize(raw.decode('utf-8-sig')), ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as exc:
        parser.exit(1, f'Error: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
