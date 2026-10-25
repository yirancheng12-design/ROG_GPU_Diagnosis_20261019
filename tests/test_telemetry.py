import csv
import importlib.util
import io
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('telemetry', ROOT / 'tools/summarize_telemetry.py')
telemetry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(telemetry)
HEADER = 'timestamp,power_W,limit_W,gpu_C,core_MHz,util_percent,cpu_C\n'


class TelemetryTests(unittest.TestCase):
    def test_draw_and_limit_are_separate(self):
        result = telemetry.summarize(HEADER + '2026-10-19T20:00:00+08:00,40,175,50,1000,10,60\n'
                                     + '2026-10-19T20:00:01+08:00,60,175,52,1200,20,70\n')
        self.assertEqual(result['metrics']['power_W']['mean'], 50)
        self.assertEqual(result['metrics']['limit_W']['mean'], 175)
        self.assertEqual(result['sample_span_seconds'], 1)
        self.assertEqual(result['samples'], 2)

    def test_missing_limit_breaks_segment_and_remains_unknown(self):
        result = telemetry.summarize(HEADER + '2026/10/19 20:00:00,40,55,50,1000,10,60\n'
                                     + '2026/10/19 20:00:01,,N/A,,,,\n'
                                     + '2026/10/19 20:00:02,50,55,51,1100,20,65\n')
        self.assertEqual([s['limit_W'] for s in result['limit_segments']], [55, None, 55])
        self.assertEqual(result['metrics']['limit_W']['available_samples'], 2)

    def test_empty_template_is_not_fabricated_data(self):
        template = (ROOT / 'docs/en/telemetry-template.csv').read_text(encoding='utf-8')
        self.assertEqual(list(csv.DictReader(io.StringIO(template))), [])
        with self.assertRaisesRegex(ValueError, 'No samples'):
            telemetry.summarize(template)

    def test_invalid_numbers_are_rejected(self):
        for raw in ('NaN', 'inf', '-inf', 'not-a-number'):
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, 'invalid power_W'):
                telemetry.summarize(HEADER + f'2026-10-19T20:00:00,{raw},175,50,1000,10,60\n')

    def test_bad_timestamps_and_order_are_rejected(self):
        for second in ('2026-10-19T20:00:00', '2026-10-19T19:59:59', 'invalid', '2026-10-19T20:00:01+08:00'):
            with self.subTest(second=second), self.assertRaisesRegex(ValueError, 'timestamp'):
                telemetry.summarize(HEADER + '2026-10-19T20:00:00,40,175,50,1000,10,60\n'
                                     + f'{second},50,175,51,1100,20,65\n')

    def test_missing_columns_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Missing columns'):
            telemetry.summarize('timestamp,power_W\n2026-10-19T20:00:00,40\n')

    def test_extra_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'too many columns'):
            telemetry.summarize(HEADER + '2026-10-19T20:00:00,40,175,50,1000,10,60,unexpected\n')

    def test_real_archive_statistics_match_independent_calculation(self):
        with zipfile.ZipFile(ROOT / 'ROG_G635LX_调校证据.zip') as archive:
            text = archive.read('tuning/baseline-auto-1/telemetry.csv').decode('utf-8-sig')
        result = telemetry.summarize(text)
        rows = list(csv.DictReader(io.StringIO(text)))
        self.assertEqual(result['samples'], len(rows))
        self.assertEqual(result['samples'], 107)
        self.assertEqual(result['limit_segments'][0]['limit_W'], 55)
        self.assertEqual(result['limit_segments'][0]['samples'], 57)
        self.assertAlmostEqual(result['sample_span_seconds'], 98.627)
        self.assertEqual(sum(segment['samples'] for segment in result['limit_segments']), len(rows))
        self.assertAlmostEqual(result['metrics']['power_W']['mean'], sum(float(row['power_W']) for row in rows) / len(rows))
        self.assertEqual(result['metrics']['cpu_C']['maximum'], 104)


if __name__ == '__main__':
    unittest.main()
