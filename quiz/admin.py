from django.contrib import admin
from.models import Question,Result,Course,schoo_dashbored
# Register your models here.
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
# admin.site.register(Course)
@admin.register(schoo_dashbored)
class School_dashbord_admin(admin.ModelAdmin):
    list_display = ['School_name','Phone_Number','city']