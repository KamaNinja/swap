from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from ads.filters import build_ads_filters, build_proposal_filters
from ads.models import Ad, ExchangeProposal


class BuildAdsFiltersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='user', password='pass')

        self.ad1 = Ad.objects.create(
            title='iPhone 13',
            description='Новый телефон, ни разу не использовался',
            condition='new',
            category='tech',
            image='images/test1.jpg',
            user=self.user
        )

        self.ad2 = Ad.objects.create(
            title='Старый ноутбук',
            description='Использовался год',
            condition='used',
            category='tech',
            image='images/test2.jpg',
            user=self.user
        )

        self.ad3 = Ad.objects.create(
            title='Пальто зимнее',
            description='Теплое, удобное',
            condition='used',
            category='wear',
            image='images/test3.jpg',
            user=self.user
        )

    def test_search_bar_filter_by_title(self):
        request = self.factory.get('/ads', {'search_bar': 'iphone'})
        filters = build_ads_filters(request)
        ads = Ad.objects.filter(filters)
        self.assertIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)
        self.assertNotIn(self.ad3, ads)

    def test_search_bar_filter_by_description(self):
        request = self.factory.get('/ads', {'search_bar': 'Теплое'})
        filters = build_ads_filters(request)
        ads = Ad.objects.filter(filters)
        self.assertIn(self.ad3, ads)
        self.assertNotIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)

    def test_category_filter(self):
        request = self.factory.get('/ads', {'category': ['wear']})
        filters = build_ads_filters(request)
        ads = Ad.objects.filter(filters)
        self.assertIn(self.ad3, ads)
        self.assertNotIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)

    def test_condition_filter(self):
        request = self.factory.get('/ads', {'condition': 'new'})
        filters = build_ads_filters(request)
        ads = Ad.objects.filter(filters)
        self.assertIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)
        self.assertNotIn(self.ad3, ads)

    def test_combined_filters(self):
        request = self.factory.get('/ads', {
            'search_bar': 'ноутбук',
            'category': ['tech'],
            'condition': 'used'
        })
        filters = build_ads_filters(request)
        ads = Ad.objects.filter(filters)
        self.assertIn(self.ad2, ads)
        self.assertNotIn(self.ad1, ads)
        self.assertNotIn(self.ad3, ads)

    def test_combined_filters_no_match(self):
        request = self.factory.get('/ads', {
            'search_bar': 'пальто',
            'category': ['tech'],
            'condition': 'new'
        })
        filters = build_ads_filters(request)
        ads = Ad.objects.filter(filters)
        self.assertEqual(ads.count(), 0)


class ProposalFiltersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Пользователи
        self.sender_user = User.objects.create_user(username='sender', password='pass')
        self.receiver_user = User.objects.create_user(username='receiver', password='pass')

        # Объявления
        self.sender_ad = Ad.objects.create(
            title='Sender Ad',
            description='desc',
            condition='new',
            image='img.jpg',
            category='tech',
            user=self.sender_user
        )

        self.receiver_ad = Ad.objects.create(
            title='Receiver Ad',
            description='desc',
            condition='used',
            image='img.jpg',
            category='book',
            user=self.receiver_user
        )

        # Обмен
        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.sender_ad,
            ad_receiver=self.receiver_ad,
            comment='Let’s swap',
            status='pending'
        )

    def test_filter_by_sender_username(self):
        request = self.factory.get('/my_proposals/', {'ad_sender': 'sender'})
        filters = build_proposal_filters(request)
        proposals = ExchangeProposal.objects.filter(filters)
        self.assertEqual(list(proposals), [self.proposal])

    def test_filter_by_receiver_username(self):
        request = self.factory.get('/my_proposals/', {'ad_receiver': 'receiver'})
        filters = build_proposal_filters(request)
        proposals = ExchangeProposal.objects.filter(filters)
        self.assertEqual(list(proposals), [self.proposal])

    def test_filter_by_status(self):
        request = self.factory.get('/my_proposals/', {'status': ['pending']})
        filters = build_proposal_filters(request)
        proposals = ExchangeProposal.objects.filter(filters)
        self.assertEqual(list(proposals), [self.proposal])

    def test_combined_all_filters(self):
        request = self.factory.get('/my_proposals/', {
            'ad_sender': 'sender',
            'ad_receiver': 'receiver',
            'status': ['pending']
        })
        filters = build_proposal_filters(request)
        proposals = ExchangeProposal.objects.filter(filters)
        self.assertEqual(list(proposals), [self.proposal])

    def test_filter_with_wrong_status(self):
        request = self.factory.get('/my_proposals/', {'status': ['rejected']})
        filters = build_proposal_filters(request)
        proposals = ExchangeProposal.objects.filter(filters)
        self.assertEqual(len(proposals), 0)
