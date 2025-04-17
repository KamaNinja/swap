from ads.models import Ad, ExchangeProposal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


def generate_test_image():
    img_io = io.BytesIO()
    image = Image.new("RGB", (100, 100), "white")
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile('test.jpg', img_io.read(), content_type='image/jpeg')


class AdsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.ad = Ad.objects.create(
            title='Test Ad',
            description='Test Description',
            condition='new',
            category='tech',
            user=self.user,
            image=generate_test_image()
        )

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/index.html')

    def test_my_ads_requires_login(self):
        response = self.client.get(reverse('my_ads'))
        self.assertEqual(response.status_code, 302)

    def test_my_ads_authenticated(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('my_ads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/index.html')
        self.assertContains(response, self.ad.title)

    def test_ad_details_view(self):
        response = self.client.get(reverse('ad_details', args=[self.ad.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ad_details.html')
        self.assertContains(response, self.ad.title)

    def test_add_ad_requires_login(self):
        response = self.client.get(reverse('add_ad'))
        self.assertEqual(response.status_code, 302)

    def test_add_ad_post_valid(self):
        image = generate_test_image()
        data = {
            'title': 'New Ad',
            'description': 'Some description',
            'condition': 'used',
            'category': 'book',
            'image': image
        }
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('add_ad'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Объявление успешно добавлено.')
        self.assertTrue(Ad.objects.filter(title='New Ad').exists())

    def test_update_ad(self):
        data = {
            'title': 'Updated Title',
            'description': self.ad.description,
            'condition': self.ad.condition,
            'category': self.ad.category
        }
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('update_ad', args=[self.ad.pk]), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Объявление успешно обновлено.')
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Title')

    def test_delete_ad(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('delete_ad', args=[self.ad.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Объявление успешно удалено.')
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())


class ProposalViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.ad1 = Ad.objects.create(
            title='Ad 1',
            description='Desc 1',
            condition='new',
            image='image/test1.jpg',
            category='tech',
            user=self.user1
        )
        self.ad2 = Ad.objects.create(
            title='Ad 2',
            description='Desc 2',
            condition='used',
            image='image/test1.jpg',
            category='book',
            user=self.user2
        )

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Wanna trade?',
            status='pending'
        )

    def test_my_proposals_view(self):
        self.client.login(username='user1', password='pass')
        url = reverse('my_proposals')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/my_proposals.html')
        self.assertIn(self.proposal, response.context['outgoing'])

    def test_proposal_details_view(self):
        self.client.login(username='user1', password='pass')
        url = reverse('proposal_details', args=[self.proposal.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/proposal_details.html')
        self.assertContains(response, self.proposal.comment)

    def test_suggest_exchange_view_get(self):
        self.client.login(username='user1', password='pass')
        url = reverse('suggest_exchange', args=[self.ad2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/suggest_exchange.html')

    def test_suggest_exchange_view_post(self):
        self.client.login(username='user1', password='pass')
        url = reverse('suggest_exchange', args=[self.ad2.pk])
        data = {
            'ad_receiver': self.ad2.pk,
            'ad_sender': self.ad1.pk,
            'comment': 'Let’s trade!'
        }
        response = self.client.post(url, data, follow=True)
        self.assertContains(response, 'Предложение успешно отправлено.')
        self.assertTrue(ExchangeProposal.objects.filter(comment='Let’s trade!').exists())

    def test_exchange_action_accept(self):
        self.client.login(username='user2', password='pass')
        url = reverse('exchange_action', args=[self.proposal.pk])
        response = self.client.post(url, {'action': 'accept'}, follow=True)
        self.assertContains(response, 'Вы приняли предложение обмена.')
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'accepted')

    def test_exchange_action_reject(self):
        self.client.login(username='user2', password='pass')
        url = reverse('exchange_action', args=[self.proposal.pk])
        response = self.client.post(url, {'action': 'reject'}, follow=True)
        self.assertContains(response, 'Вы отклонили предложение обмена.')
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'rejected')

    def test_exchange_action_wrong_user(self):
        self.client.login(username='user1', password='pass')  # not receiver!
        url = reverse('exchange_action', args=[self.proposal.pk])
        response = self.client.post(url, {'action': 'accept'}, follow=True)
        self.assertContains(response, 'У вас нет прав для изменения этого предложения.')
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'pending')
