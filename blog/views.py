from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, MyUser, CommentPost, LikePost, FollowMyUser


# def func(post, comments, likes):
#     post.comments = comments[:5]
#     post.likes = likes[:3]
#     return post
#
#
# @login_required(login_url='login/')
# def home_view(request):
#     users = MyUser.objects.exclude(user=request.user)
#     my_user = MyUser.objects.filter(user=request.user).first()
#
#     followings = FollowMyUser.objects.filter(follower_id=my_user.id).values_list('following', flat=True)
#     users_view = users.exclude(id__in=followings)
#
#     posts = Post.objects.filter(author__in=followings)
#
#     # if len(users_view) > 0:
#     #     posts = Post.objects.filter(author=my_user)
#
#     context = {
#         'posts': map(lambda post: func(post, CommentPost.objects.filter(post_id=post.id),
#                                        LikePost.objects.filter(post_id=post.id)), posts),
#         'user': my_user,
#         'profiles': users_view,
#         'display_users': users_view
#
#     }
#
#     if request.method == 'POST':
#         data = request.POST
#         message = data['message']
#         post_id = data['post_id']
#         my_user = MyUser.objects.filter(user=request.user).first()
#         obj = CommentPost.objects.create(post_id=post_id, message=message, author=my_user)
#         obj.save()
#
#         return redirect('/#{}'.format(post_id))
#
#     return render(request, 'index.html', context=context)

def func(post, comments, likes):
    post.comments = comments[:5]
    post.likes = likes[:3]
    return post


@login_required(login_url='/login')
def home_view(request):
    users = MyUser.objects.exclude(user=request.user)
    user = MyUser.objects.filter(user=request.user).first()

    followings = FollowMyUser.objects.filter(follower=user).values_list('following_id', flat=True)
    display_users = users.exclude(id__in=followings)
    users_followed = MyUser.objects.filter(id__in=followings)
    posts = Post.objects.filter(author__in=users_followed)

    if len(users_followed) == 0:
        posts = Post.objects.filter(author=user)

    d = {
        'posts': map(lambda post: func(post, CommentPost.objects.filter(post_id=post.id),
                                       LikePost.objects.filter(post_id=post.id)), posts),
        'user': user,
        'profiles': MyUser.objects.all().exclude(user=request.user),
        'user_profile': MyUser.objects.filter(user=request.user),
        'display_users': display_users
    }

    if request.method == 'POST':
        data = request.POST
        message = data['message']
        post_id = data['post_id']
        my_user = MyUser.objects.filter(user=request.user).first()
        obj = CommentPost.objects.create(message=message, post_id=post_id, author=my_user)
        obj.save()
        return redirect('/#{}'.format(post_id))

    return render(request, 'index.html', context=d)


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')


def login_view(request):
    d = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        d['error'] = 'User or password incorrect'

    return render(request, 'signin.html', context=d)


def register_view(request):
    d = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        if User.objects.filter(username=username).exists():
            d['error'] = f'Username with this {username} already exists'
        elif password1 != password2:
            d['error'] = 'Passwords are not  same'
        else:
            user = User.objects.create(username=username, password=make_password(password1))
            user.save()
            my_user = MyUser.objects.create(user_id=user.id)
            my_user.save()
            return redirect('/login')
    return render(request, 'signup.html', context=d)


def setting_view(request):
    return render(request, 'setting.html')


@login_required(login_url='/login')
def profile_view(request, pk):
    my_user = MyUser.objects.filter(user=request.user).first()
    user = MyUser.objects.filter(id=pk).first()
    posts = Post.objects.filter(author_id=pk).all()
    post_count = posts.count()
    follower_count = FollowMyUser.objects.filter(follower_id=pk).count()
    following_count = FollowMyUser.objects.filter(following_id=pk).count()

    d = {
        'my_user': my_user,
        'user': user,
        'posts': posts,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
    }

    return render(request, 'profile.html', context=d)


@login_required(login_url='/login')
def upload_view(request):
    if request.method == 'POST':
        my_user = MyUser.objects.filter(user=request.user).first()
        post = Post.objects.create(image=request.FILES['image'], author=my_user)
        post.save()
        return redirect('/')
    return redirect('/')


@login_required(login_url='/login')
def upload_author_view(request):
    if request.method == 'POST' and 'profile_pic' in request.FILES:
        my_user = get_object_or_404(MyUser, user=request.user)
        if my_user.user == request.user:
            my_user.profile_pic = request.FILES['profile_pic']
            my_user.save()
            return redirect('/')
    return redirect('/')


@login_required(login_url='/login')
def like_view(request):
    post_id = request.GET.get('post_id')
    user = MyUser.objects.filter(user=request.user).first()
    post = Post.objects.filter(id=post_id).first()
    like_exists = LikePost.objects.filter(author=user, post_id=post_id)
    if like_exists.exists():
        like_exists.delete()
        post.like_count -= 1
        post.save(update_fields=['like_count'])

    else:
        obj = LikePost.objects.create(author=user, post_id=post_id)
        obj.save()
        post.like_count += 1
        post.save(update_fields=['like_count'])

    return redirect('/#{}'.format(post_id))


@login_required(login_url='/login')
def follow_view(request):
    profile_id = request.GET.get('profile_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    profile = MyUser.objects.filter(id=profile_id).first()
    follow_exists = FollowMyUser.objects.filter(follower=my_user, following_id=profile_id)
    if follow_exists.exists():
        follow_exists.delete()
        profile.follow_count -= 1
        profile.save(update_fields=['follow_count'])

    else:
        obj = FollowMyUser.objects.create(follower=my_user, following_id=profile_id)
        obj.save()
        profile.follow_count += 1
        profile.save(update_fields=['follow_count'])

    return redirect('/')


@login_required(login_url='/login')
def search_view(request):
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    posts = Post.objects.all()
    if query is not None and len(query) >= 1:
        posts = posts.filter(author__user__username__icontains=query)
    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context=context)
