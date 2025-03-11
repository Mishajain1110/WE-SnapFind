from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, MyPasswordChangeForm, EditProfileForm
from .models import Faculty, UserProfile, Reward, Badge
from posts.models import Post
from chats.models import Chat
from django.contrib.auth.models import User
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
@csrf_protect 
@require_POST 
def close_post(request):
    try:
        data = json.loads(request.body)
        post_id = data.get("post_id")
        finder_username = data.get("finder_username")
        found_post_id = data.get("found_post_id")

        if not post_id or not found_post_id:
            return JsonResponse({"error": "Invalid post ID"}, status=400)

        post_id = int(post_id)
        found_post_id = int(found_post_id)
        post = get_object_or_404(Post, id=post_id)
        post.is_active = False
        post.save()

        post2 = get_object_or_404(Post, id=found_post_id)
        post2.is_active = False
        post2.save()

        if finder_username:
            try:
                finder = User.objects.get(username=finder_username)
                reward, created = Reward.objects.get_or_create(user=finder)
                reward.points += 10
                reward.save()
            except User.DoesNotExist:
                return JsonResponse({"success": False, "message": "User not found!"})

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {
            'form': form,
            'facultys': Faculty.objects.all()
        })

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            faculty = Faculty.objects.get(
                id=request.POST.get('faculty')
            )

            try:
                picture = request.FILES['picture']
            except:
                picture = None

            userprofile = UserProfile.objects.create(
                user=user,
                faculty=faculty
            )

            if picture != None:
                userprofile.avatar = picture
                userprofile.save()

            Chat.objects.create(
                user=user
            )
            # login
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.template_name, {
                'form': form,
                'facultys': Faculty.objects.all()
            })


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        # if have next send it to save in input:hidden
        next_url = request.GET.get('next')
        return render(request, 'login.html', {
            'next_url': next_url
        })

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_url = request.POST.get('next_url')
        if user:
            login(request, user)
            if next_url != 'None':
                return redirect(next_url)
            else:
                return redirect('index')

        return render(request, 'login.html', {
            'next_url': next_url,
            'error': 'Incorrect username or password'
        })


class MyPostView(View):
    template_name = 'my_posts.html'

    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.filter(user=request.user).order_by(
                '-is_active', '-create_at')
            founds = Post.objects.filter(user=request.user, type='found')
            losts = Post.objects.filter(user=request.user, type='lost')
        else:
            posts = "key"
            founds = []
            losts = []
        return render(request, self.template_name, {
            'posts': posts,
            'founds': founds,
            'losts': losts,
            'closed': len(Post.objects.filter(user=request.user, is_active=False)) if request.user.is_authenticated else len(Post.objects.filter(is_active=False))
        })

    def post(self, request):
        key = request.POST.get('key')
        try:
            post = Post.objects.get(key=key)
            return render(request, self.template_name, {
                'posts': [post],
                'key': key
            })
        except:
            return render(request, self.template_name, {
                'posts': 'key',
                'key_error': 'No post found with this key'
            })


class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)
        founds = Post.objects.filter(user=user, type='found')
        losts = Post.objects.filter(user=user, type='lost')
        reward, created = Reward.objects.get_or_create(user=request.user)
        closed = 0
        for post in posts:
            if post.is_active == False:
                closed += 1
        context = {
            'user': user,
            'posts': posts,
            'closed': closed,
            'active': len(posts) - closed,
            'founds': founds,
            'losts': losts,
            'rewards': reward
        }
        return render(request, self.template_name, context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    template_name = 'change_password.html'

    def get(self, request):
        user = request.user
        form = MyPasswordChangeForm(user=user)

        return render(request, self.template_name, {
            'user': user,
            'form': form
        })

    def post(self, request):
        user = request.user
        form = MyPasswordChangeForm(data=request.POST, user=user)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, self.template_name, {
                'user': user,
                'form': form
            })


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    template_name = 'edit_profile.html'

    def get(self, request):
        user = request.user
        form = EditProfileForm(instance=user)
        faculty = Faculty.objects.all()

        return render(request, self.template_name, {
            'user': user,
            'form': form,
            'facultys': faculty
        })

    def post(self, request):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        form = EditProfileForm(request.POST, instance=user)

        userprofile.faculty = Faculty.objects.get(
            id=int(request.POST.get('faculty')))

        userprofile.save()

        try:
            picture = request.FILES['picture']
        except:
            picture = None

        if picture != None:
            userprofile.avatar = picture
            userprofile.save()

        if form.is_valid():
            form.save()
            return render(request, self.template_name, {
                'user': user,
                'form': form,
                'facultys': Faculty.objects.all(),
                'success': 'Profile updated successfully'
            })
        else:
            return render(request, self.template_name, {
                'user': user,
                'form': form,
                'facultys': Faculty.objects.all()
            })

@login_required
def rewards_view(request):
    reward, created = Reward.objects.get_or_create(user=request.user)
    upcoming_badges = Badge.objects.filter(points_required__gt=reward.points).order_by('points_required')[:4]
    top_users = Reward.objects.select_related('user').order_by('-points')[:5]
    print("hiiiiiiiiiii", top_users)
    context = {
        'rewards': reward,
        'upcoming_badges': upcoming_badges,
        'top_users': top_users,
    }

    return render(request, 'rewards.html', context)
