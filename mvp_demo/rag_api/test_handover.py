import importlib.util
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User
from . import views


class DateValidationTests(SimpleTestCase):
    def test_invalid_calendar_date_is_rejected(self):
        with self.assertRaises(ValueError):
            views.date_string_to_numeric('2024-13-45')

    def test_leap_day_is_a_real_date(self):
        self.assertEqual(views.date_string_to_numeric('2024-02-29'), 20240229)
        with self.assertRaises(ValueError):
            views.date_string_to_numeric('2023-02-29')


class SeedPasswordTests(TestCase):
    def test_fresh_seed_accounts_have_no_shared_placeholder(self):
        seeded = User.objects.filter(advisor__isnull=False)
        self.assertTrue(seeded.exists())
        for user in seeded:
            self.assertFalse(user.has_usable_password(), user.username)


class OCRDependencyTests(SimpleTestCase):
    def test_raw_ocr_does_not_load_chonkie_or_ollama_and_logs_timing(self):
        # Isolate the optional native OCR packages; no model downloads.
        path = Path(__file__).resolve().parents[1] / 'ocr_solution.py'
        fake = {'paddleocr': SimpleNamespace(PPStructureV3=object),
                'pymupdf': SimpleNamespace(Page=object), 'chonkie': None, 'ollama': None}
        with mock.patch.dict(sys.modules, fake):
            spec = importlib.util.spec_from_file_location('ocr_dependency_check', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / 'synthetic.pdf'
                source.write_bytes(b'%PDF-synthetic')
                ocr = module.OCR(Path(directory) / 'output')
                ocr.pipelineV3 = object()
                ocr.predictV3 = mock.Mock(return_value='Synthetic extracted text')
                self.assertEqual(ocr.output_document(source, cleanup=False), 'Synthetic extracted text')
                self.assertIn('cleanup=False', (ocr.output / 'ocr_log.txt').read_text())
