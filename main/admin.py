from django.contrib import admin
import datetime

from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, Comment
from .utilities import send_activation_notification
from .forms import SubRubricForm


def send_activation_notifications(model_admin, request, queryset):
    """Отправка писем с ссылкой для активации"""
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
        model_admin.message_user(request, 'Письма с оповещениями отправлены')


send_activation_notifications.short_description = 'Отправка писем с оповещениями об активации'


class NonactivatedFilter(admin.SimpleListFilter):
    """Фильтр для сортировки пользователей по их активации"""
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('no_activated', 'Не прошли'),
            ('three_days', 'Не прошли в течении более 3 дней'),
            ('week', 'Не прошли более недели')
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'no_activated':
            return queryset.filter(is_active=False, is_activated=False)
        elif val == 'three_days':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    """Редактор пользователей"""
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'), ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 'groups', 'user_permissions', ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


class SubRubricInline(admin.TabularInline):
    """Встроенный редактор подрубрик"""
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    """Редактор надрубрик"""
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)


class SubRubricAdmin(admin.ModelAdmin):
    """Редактор подрубрик"""
    form = SubRubricForm


class AdditionalImageInline(admin.TabularInline):
    """Встроенный редактор дополнительных иллюстраций"""
    model = AdditionalImage


class CommentInline(admin.TabularInline):
    """Встроенный редактор дополнительных иллюстраций"""
    model = Comment
    fields = ('author', 'content', 'is_active')


class BbAdmin(admin.ModelAdmin):
    """Редактор объявлений"""
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline, CommentInline,)


class CommentAdmin(admin.ModelAdmin):
    """Редактор комментариев"""
    list_display = ('bb', 'content', 'is_active', 'created_at')
    fields = (('bb', 'author'), 'content', 'is_active')


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Bb, BbAdmin)
admin.site.register(Comment, CommentAdmin)
