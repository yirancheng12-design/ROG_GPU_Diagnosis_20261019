import csv
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class DiscoveryAssetsTests(unittest.TestCase):
    def test_chart_provenance_matches_source_and_assets(self):
        provenance = json.loads((ROOT / 'assets/preview-provenance.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(ROOT / provenance['archive']) as archive:
            raw = archive.read(provenance['member'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), provenance['source_sha256'])
        self.assertEqual(len(list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))), provenance['samples'])
        for name, digest in provenance['artifacts'].items():
            self.assertEqual(hashlib.sha256((ROOT / 'assets' / name).read_bytes()).hexdigest(), digest)
        png = (ROOT / 'assets/telemetry-preview.png').read_bytes()
        self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(list(struct.unpack('>II', png[16:24])), provenance['image_size'])
        self.assertLess(len(png), 1_000_000)

    def test_demo_runs_outside_repo_and_matches_readme_excerpt(self):
        with tempfile.TemporaryDirectory() as directory:
            run = subprocess.run([sys.executable, str(ROOT / 'tools/demo.py')], cwd=directory,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}, capture_output=True,
                text=True, encoding='utf-8', timeout=15, check=True)
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        for line in run.stdout.splitlines()[1:4]:
            self.assertIn(line, readme)
        self.assertIn('not sustained-load or FPS results', run.stdout)

    def test_growth_template_has_no_fabricated_measurements(self):
        text = (ROOT / 'docs/en/growth-log.csv').read_text(encoding='utf-8')
        reader = csv.DictReader(io.StringIO(text))
        self.assertIn('unique_visitors_14d', reader.fieldnames)
        self.assertEqual(list(reader), [])


if __name__ == '__main__':
    unittest.main()
