from django.contrib import admin

from blog.models import MyUser, Post, CommentPost, LikePost, FollowMyUser

admin.site.register(MyUser)
admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(LikePost)
admin.site.register(FollowMyUser)
