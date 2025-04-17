from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.http import HttpRequest

from ads.utils import get_page_obj
from ads.models import Ad
from ads.views import get_ads_context


class PaginatorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        for i in range(1, 20):
            Ad.objects.create(
                title=f"Ad {i}",
                description=f"Description for ad {i}",
                condition='new',
                category='tech',
                image='images/test.jpg',
                user=self.user
            )

    def test_get_page_obj(self):
        request = HttpRequest()
        request.GET['page'] = '2'

        queryset = Ad.objects.all().order_by('created_at')
        page_obj = get_page_obj(request, queryset)
        self.assertEqual(page_obj.number, 2)
        self.assertEqual(len(page_obj.object_list), 9)
        self.assertEqual(page_obj.object_list[0].title, 'Ad 10')
        self.assertEqual(page_obj.object_list[8].title, 'Ad 18')


class GetAdsContextTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.ad1 = Ad.objects.create(
            title='My Tech Ad',
            description='Some description',
            condition='new',
            image='images/test1.jpg',
            category='tech',
            user=self.user1
        )

        self.ad2 = Ad.objects.create(
            title='Other Book Ad',
            description='Another description',
            condition='used',
            image='images/test2.jpg',
            category='book',
            user=self.user2
        )

    def test_general_ads_context(self):
        request = self.factory.get('/ads/', {'category': 'book'})
        request.user = self.user1
        context = get_ads_context(request)

        self.assertIn('form', context)
        self.assertIn('page_obj', context)
        self.assertIn('selected_categories', context)
        self.assertEqual(context['selected_categories'], ['book'])

        ads_in_page = context['page_obj'].object_list
        self.assertIn(self.ad2, ads_in_page)
        self.assertNotIn(self.ad1, ads_in_page)

    def test_user_specific_ads_context(self):
        request = self.factory.get('/my-ads/')
        request.user = self.user1
        context = get_ads_context(request, user_specific=True)

        ads_in_page = context['page_obj'].object_list
        self.assertIn(self.ad1, ads_in_page)
        self.assertNotIn(self.ad2, ads_in_page)
