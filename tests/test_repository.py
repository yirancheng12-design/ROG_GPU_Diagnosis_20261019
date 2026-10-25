from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('verify_repository', Path(__file__).resolve().parents[1] / 'tools/verify_repository.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


def entry(path, raw, **extra):
    return {'path': path, 'bytes': len(raw), 'sha256': verify.sha256(raw), **extra}


def zip_fixture(name='evidence/result.json'):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        archive.writestr(name, b'{"result": "recorded"}')
    raw = stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        info = archive.infolist()[0]
        member = {'path': info.filename, 'bytes': info.file_size, 'crc32': f'{info.CRC:08x}',
                  'sha256': verify.sha256(archive.read(info))}
    return raw, [member]


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_original_hash_change_is_rejected(self):
        (self.root / 'report.txt').write_bytes(b'changed')
        errors = verify.verify_evidence(self.root, {'files': [entry('report.txt', b'original')]})
        self.assertTrue(any('changed' in error for error in errors))

    def test_missing_original_is_rejected(self):
        self.assertTrue(verify.verify_evidence(self.root, {'files': [entry('missing.txt', b'data')]}))

    def test_valid_zip_is_read_without_extraction(self):
        raw, members = zip_fixture()
        (self.root / 'data.zip').write_bytes(raw)
        self.assertEqual(verify.verify_evidence(self.root, {'files': [entry('data.zip', raw, members=members)]}), [])
        self.assertFalse((self.root / 'evidence').exists())

    def test_member_inventory_change_is_rejected(self):
        raw, members = zip_fixture()
        (self.root / 'data.zip').write_bytes(raw)
        members[0]['sha256'] = '0' * 64
        self.assertTrue(verify.verify_evidence(self.root, {'files': [entry('data.zip', raw, members=members)]}))

    def test_invalid_zip_is_rejected(self):
        raw = b'not a ZIP file'
        (self.root / 'bad.zip').write_bytes(raw)
        self.assertTrue(verify.verify_evidence(self.root, {'files': [entry('bad.zip', raw, members=[])]}))

    def test_unsafe_zip_paths_are_rejected_without_extraction(self):
        for name in ('../outside.txt', '/absolute.txt', 'C:/outside.txt', '..\\outside.txt'):
            with self.subTest(name=name):
                raw, members = zip_fixture(name)
                (self.root / 'data.zip').write_bytes(raw)
                errors = verify.verify_evidence(self.root, {'files': [entry('data.zip', raw, members=members)]})
                self.assertTrue(any('Unsafe ZIP' in error for error in errors))

    def test_links_handle_unicode_spaces_and_missing_targets(self):
        (self.root / 'README.md').write_text('# Home\n[report](%E6%8A%A5%E5%91%8A%20one.txt)\n', encoding='utf-8')
        (self.root / 'CONTRIBUTING.md').write_text('# Contributing\n', encoding='utf-8')
        (self.root / '报告 one.txt').write_text('source', encoding='utf-8')
        self.assertEqual(verify.verify_markdown(self.root), [])
        (self.root / 'README.md').write_text('# Home\n[missing](missing.txt)\n', encoding='utf-8')
        self.assertTrue(any('Broken local link' in error for error in verify.verify_markdown(self.root)))

    def test_link_cannot_escape_repository(self):
        (self.root / 'README.md').write_text('# Home\n[escape](../outside.txt)\n', encoding='utf-8')
        (self.root / 'CONTRIBUTING.md').write_text('# Contributing\n', encoding='utf-8')
        self.assertTrue(any('escapes' in error for error in verify.verify_markdown(self.root)))

    def test_coverage_distinguishes_archive_path_from_same_basename(self):
        html = '<a href="tuning/final-state.json">archived</a><a href="final-state.json">missing</a>'
        (self.root / 'report.html').write_text(html, encoding='utf-8')
        manifest = {'files': [entry('report.html', html.encode()),
                              {'path': 'data.zip', 'members': [{'path': 'tuning/final-state.json'}]}]}
        coverage = verify.coverage_text(self.root, manifest)
        self.assertIn('`tuning/final-state.json` | archive member', coverage)
        self.assertIn('`final-state.json` | not published', coverage)

    def test_csv_invalid_digest_is_rejected(self):
        path = self.root / 'inventory.csv'
        path.write_text('File,Bytes,SHA256\na.json,1,invalid\n', encoding='utf-8')
        self.assertTrue(verify.verify_csvs(self.root, {'files': [{'path': path.name}]}))


class PublishedEvidenceTests(unittest.TestCase):
    def test_published_snapshot_and_docs_pass(self):
        manifest = json.loads((verify.ROOT / verify.MANIFEST).read_text(encoding='utf-8'))
        self.assertEqual(verify.verify_evidence(verify.ROOT, manifest), [])
        self.assertEqual(verify.verify_markdown(verify.ROOT), [])
        self.assertEqual(verify.verify_csvs(verify.ROOT, manifest), [])
        self.assertEqual((verify.ROOT / verify.COVERAGE).read_text(encoding='utf-8'), verify.coverage_text(verify.ROOT, manifest))

    def test_pre_restart_write_is_not_live_225w_or_a_stress_test(self):
        with zipfile.ZipFile(verify.ROOT / '225W新路线重启前证据_20261019.zip') as archive:
            result = json.loads(archive.read('power225-research-followup/apply-max225-20261019-234340-result.json').decode('utf-8-sig'))
        self.assertTrue(result['RegistryReadbackMatches'])
        self.assertEqual(result['TargetMaxWatts'], 225)
        self.assertTrue(result['LiveCurrentStill175'])
        self.assertTrue(result['LiveMaxStill175'])
        self.assertTrue(result['RestartRequired'])
        self.assertFalse(result['StressTestStarted'])
        self.assertFalse(result['FirmwareFlashed'])


if __name__ == '__main__':
    unittest.main()
