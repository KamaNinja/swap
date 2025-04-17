from django.core.paginator import Paginator

from ads.filters import build_ads_filters
from ads.forms import FilterAdForm
from ads.models import Ad


def get_page_obj(request, queryset, per_page=9):
    """
    Возвращает объект пагинации для переданного запроса.
    Args:
      request (HttpRequest): Объект запроса, содержащий параметр страницы.
      queryset (QuerySet): Набор данных, подлежащий пагинации.
      per_page (int, optional): Количество элементов на страницу. По умолчанию 9.
    Returns:
        Page: Объект текущей страницы с элементами из queryset.
      """
    paginator = Paginator(queryset, per_page)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return page_obj


def get_ads_context(request, user_specific=False):
    """
    Формирует контекст для отображения объявлений с учетом фильтров и пагинации.
    Args:
        request (HttpRequest): Объект запроса с параметрами фильтрации и пагинации.
        user_specific (bool, optional): Флаг, указывающий, нужно ли выводить только объявления текущего пользователя.
        По умолчанию False (выводятся все объявления).
    Returns:
        dict: Словарь с контекстом, содержащим форму фильтрации, объект пагинации и выбранные категории.
    """
    form = FilterAdForm(request.GET or None)
    filters = build_ads_filters(request)

    if user_specific:
        ads = Ad.objects.filter(user=request.user).filter(filters).select_related('user')
    else:
        ads = Ad.objects.filter(filters).select_related('user')

    selected_categories = request.GET.getlist('category')
    page_obj = get_page_obj(request, ads, 9)
    context = {
        'form': form,
        'page_obj': page_obj,
        'selected_categories': selected_categories
    }
    return context
