from .models import SubRubric


def bboard_context_processor(request):
    """Добавляет список рубрик и данные для коректного возврата пользователя в просматриваемую им часть списка
    объявлений в контекст"""
    context = {'rubrics': SubRubric.objects.all(), 'keyword': '', 'all': ''}
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != 1:
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context
