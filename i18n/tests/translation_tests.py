import unittest
import os
import os.path

from i18n import resource_loader
from i18n.translator import t
from i18n import translations
from i18n import config

RESOURCE_FOLDER = os.path.dirname(__file__) + os.sep + 'resources' + os.sep

class TestTranslationFormat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        resource_loader.init_loaders()
        config.set('load_path', [os.path.join(RESOURCE_FOLDER, 'translations')])
        translations.add('foo.hi', 'Hello %{name} !')
        translations.add('foo.hello', 'Salut %{name} !', locale='fr')

    def setUp(self):
        config.set('error_on_missing_translation', False)
        config.set('error_on_missing_placeholder', False)
        config.set('fallback', 'en')
        config.set('locale', 'en')

    def test_missing_translation(self):
        self.assertEqual(t('foo.inexistent'), 'foo.inexistent')

    def test_missing_translation_error(self):
        config.set('error_on_missing_translation', True)
        with self.assertRaises(KeyError):
            t('foo.inexistent')

    def test_basic_translation(self):
        self.assertEqual(t('foo.normal_key'), 'normal_value')

    def test_locale_change(self):
        config.set('locale', 'fr')
        self.assertEqual(t('foo.hello', name='Bob'), 'Salut Bob !')

    def test_fallback(self):
        config.set('fallback', 'fr')
        self.assertEqual(t('foo.hello', name='Bob'), 'Salut Bob !')

    def test_basic_placeholder(self):
        self.assertEqual(t('foo.hi', name='Bob'), 'Hello Bob !')

    def test_missing_placehoder(self):
        self.assertEqual(t('foo.hi'), 'Hello %{name} !')

    def test_missing_placeholder_error(self):
        config.set('error_on_missing_placeholder', True)
        with self.assertRaises(KeyError):
            t('foo.hi')
