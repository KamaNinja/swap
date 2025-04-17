from django.db.models import Q


def build_ads_filters(request):
    """
    Создает фильтр для объявлений на основе параметров GET-запроса.
    Фильтрация включает:
    - Поиск по заголовку и описанию (search_bar)
    - Фильтрацию по категориям (category)
    - Фильтрацию по состоянию (condition)
    Args:
        request (HttpRequest): Объект запроса, содержащий параметры фильтрации.
    Returns:
        Q: Объект Q с накопленными условиями фильтрации.
    """
    filters = Q()

    search_bar = request.GET.get('search_bar', '').strip()
    if search_bar:
        filters &= (Q(title__icontains=search_bar) | Q(description__icontains=search_bar))

    categories = request.GET.getlist('category')
    if categories:
        filters &= Q(category__in=categories)

    condition = request.GET.get('condition', '')
    if condition:
        filters &= Q(condition=condition)

    return filters


def build_proposal_filters(request):
    """
    Создает фильтр для предложений на основе параметров GET-запроса.
    Фильтрация включает:
    - Отправителя объявления (ad_sender)
    - Получателя объявления (ad_receiver)
    - Статус предложения (status)
    Args:
        request (HttpRequest): Объект запроса, содержащий параметры фильтрации.
    Returns:
        Q: Объект Q с условиями фильтрации для модели предложений.
    """
    filters = Q()

    ad_sender = request.GET.get('ad_sender', '')
    if ad_sender:
        filters &= Q(ad_sender__user__username=ad_sender)

    ad_receiver = request.GET.get('ad_receiver', '')
    if ad_receiver:
        filters &= Q(ad_receiver__user__username=ad_receiver)

    status = request.GET.getlist('status')
    if status:
        filters &= Q(status__in=status)

    return filters
