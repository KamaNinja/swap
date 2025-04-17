from django.test import TestCase
from ads.models import Ad
from ads.forms import ExchangeProposalForm
from django.contrib.auth.models import User


class ExchangeProposalFormTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.ad1 = Ad.objects.create(
            title='Phone',
            description='Smartphone',
            condition='new',
            image='images/test1.jpg',
            category='tech',
            user=self.user1
        )

        self.ad2 = Ad.objects.create(
            title='Book',
            description='A good read',
            condition='used',
            image='images/test2.jpg',
            category='book',
            user=self.user2
        )

    def test_form_querysets(self):
        form = ExchangeProposalForm(user=self.user1)
        self.assertIn(self.ad2, form.fields['ad_receiver'].queryset)
        self.assertNotIn(self.ad1, form.fields['ad_receiver'].queryset)

        self.assertIn(self.ad1, form.fields['ad_sender'].queryset)
        self.assertNotIn(self.ad2, form.fields['ad_sender'].queryset)

    def test_valid_form(self):
        form_data = {
            'ad_sender': self.ad1.pk,
            'ad_receiver': self.ad2.pk,
            'comment': 'Давайте поменяемся!'
        }
        form = ExchangeProposalForm(data=form_data, user=self.user1)
        self.assertTrue(form.is_valid())

    def test_invalid_missing_fields(self):
        form_data = {
            'ad_sender': self.ad1.pk,
            'comment': 'Без получателя'
        }
        form = ExchangeProposalForm(data=form_data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('ad_receiver', form.errors)

    def test_invalid_sender_receiver_same_user(self):
        form_data = {
            'ad_sender': self.ad1.pk,
            'ad_receiver': self.ad1.pk,
            'comment': 'Хочу свой товар :)'
        }
        form = ExchangeProposalForm(data=form_data, user=self.user1)
        self.assertNotIn(self.ad1, form.fields['ad_receiver'].queryset)
