"""Test cases for the exam util"""
from ddt import ddt, data, unpack
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
from django.test import SimpleTestCase
from factory.django import mute_signals

from exams.utils import (
    exponential_backoff,
    validate_profile
)
from profiles.factories import ProfileFactory
from search.base import MockedESTestCase


@ddt
class ExamBackoffUtilsTest(SimpleTestCase):
    """Tests for exam tasks"""
    @data(
        (5, 1, 5),
        (5, 2, 25),
        (5, 3, 125),
    )
    @unpack
    def test_exponential_backoff_values(self, base, retries, expected):  # pylint: disable=no-self-use
        """
        Test that exponential_backoff returns a power of settings.EXAMS_SFTP_BACKOFF_BASE
        """
        with self.settings(EXAMS_SFTP_BACKOFF_BASE=base):
            assert exponential_backoff(retries) == expected

    def test_exponential_backoff_invalid(self):  # pylint: disable=no-self-use
        """
        Test that exponential_backoff raises a configuration error if it gets an invalid value
        """
        with self.settings(EXAMS_SFTP_BACKOFF_BASE='NOT_AN_INT'):
            with self.assertRaises(ImproperlyConfigured):
                exponential_backoff(1)


@ddt
class ExamProfileValidationTests(MockedESTestCase):
    """Tests for exam utils validate_profile"""

    @classmethod
    def setUpTestData(cls):
        """
        Create a profile
        """
        super().setUpTestData()
        with mute_signals(post_save):
            cls.profile = ProfileFactory.create()

    def setUp(self):
        """
        refresh profile
        """
        super().setUp()
        self.profile.refresh_from_db()

    def test_exam_profile_validated(self):
        """
        test validate_profile when a field is empty
        """
        assert validate_profile(self.profile) is True

    @data('address', 'city', 'state_or_territory', 'country', 'phone_number')
    def test_when_field_is_blank(self, field):
        """
        test validate_profile when a field is empty
        """
        setattr(self.profile, field, '')
        self.profile.save()
        assert validate_profile(self.profile) is False

    @data('address', 'city', 'state_or_territory', 'country', 'phone_number')
    def test_when_field_is_invalid(self, field):
        """
        test validate_profile when a field is invalid
        """
        setattr(self.profile, field, '汉字')
        self.profile.save()
        assert validate_profile(self.profile) is False

    @data(
        ('AD', '通州区', True),
        ('AD', '', True),
        ('CA', '通州区', False),
        ('CA', '', False),
        ('US', '通州区', False),
        ('US', '', False)
    )
    @unpack
    def test_postal_code(self, country, postal_code, result):
        """
        when postal_code is (not) required and valid/invalid
        """
        self.profile.country = country
        self.profile.postal_code = postal_code
        self.profile.save()
        assert validate_profile(self.profile) is result

    @data(
        ('汉字', 'Andrew', True),
        ('', 'Andrew', True),
        ('汉字', '', False),
        ('', '', False)
    )
    @unpack
    def test_romanized_name(self, name, romanized_name, result):
        """
        test romanized name optional/required
        """
        self.profile.first_name = name
        self.profile.romanized_first_name = romanized_name
        self.profile.save()
        assert validate_profile(self.profile) is result

    @data('汉字', '')
    def test_user_email(self, email):
        """
        test invalid email
        """
        self.profile.user.email = email
        self.profile.user.save()
        assert validate_profile(self.profile) is False
