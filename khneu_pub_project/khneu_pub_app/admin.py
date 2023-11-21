from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Faculty)
admin.site.register(Specialization)
admin.site.register(Favorite)
admin.site.register(Article)
admin.site.register(UserProfile)