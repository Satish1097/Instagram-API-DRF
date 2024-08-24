from django.contrib import admin
from .models import Post,Profile,Comment,like,Story,Follow

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(like)
admin.site.register(Story)
admin.site.register(Follow)