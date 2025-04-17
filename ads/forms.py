from django import forms

from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('title', 'description', 'condition', 'image', 'category')


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ('ad_receiver', 'ad_sender', 'comment')
        labels = {
            'ad_receiver': 'Я получаю',
            'ad_sender': 'Я отдаю',
            'comment': 'Комментарий'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)
        self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)


class FilterAdForm(forms.Form):
    search_bar = forms.CharField(
        max_length=55,
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск...'}),
    )
    category = forms.MultipleChoiceField(
        choices=Ad.CATEGORY_CHOICES,
        required=False,
        label='Категория',
        widget=forms.CheckboxSelectMultiple
    )
    condition = forms.ChoiceField(
        choices=[('', 'Любое')] + Ad.CONDITION_CHOICES,
        required=False,
        label='Состояние'
    )


class FilterProposalForm(forms.Form):
    ad_sender = forms.CharField(
        max_length=50,
        required=False,
        label='Отправитель',
        widget=forms.TextInput(attrs={'placeholder': 'Отправитель'})
    )
    ad_receiver = forms.CharField(
        max_length=50,
        required=False,
        label='Получатель',
        widget=forms.TextInput(attrs={'placeholder': 'Получатель'})
    )
    status = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ExchangeProposal.STATUS_CHOICES,
        required=False,
        label='Статус'
    )
