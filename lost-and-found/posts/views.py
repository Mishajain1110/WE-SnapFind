from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, PostPictureForm
from django.http import JsonResponse
from .models import Post, PostPicture, AssetType, Comment
from django.views import View
from django.forms import formset_factory
from accounts.models import Reward, Badge
from .serializers import PostSerializer, AssetTypeSerializer, CommentSerializer
# from chats.models import ChatSession
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
# from .utils import compute_similarity
# from chats.models import Chat, Message
from .utils import find_similar_lost_posts
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
'''

def similar_posts_view(request, post_id):
    """
    View to display similar lost posts for a given found post.
    """
    # Get the newly created found post
    post = get_object_or_404(Post, id=post_id)

    # Find similar lost posts
    lost_posts = Post.objects.filter(type='lost')
    similar_posts = find_similar_lost_posts(post, lost_posts, threshold=0.7)

    # Render the similar posts template
    return render(request, 'posts/similar_posts.html', {
        'post': post,
        'similar_posts': similar_posts
    })'''
@login_required
def start_chat_with_owner(request, user_id):
    # Get the post owner or return 404 if not found
    post_owner = get_object_or_404(User, id=user_id)

    # Ensure the current user is not the post owner
    if post_owner == request.user:
        return redirect('detail')

    # Redirect to the chat interface with the post owner
    return redirect('chat_index')


class CommentAPI(APIView):

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).order_by("-create_at")
        serializer_comment = CommentSerializer(comments, many=True)
        return Response(serializer_comment.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)

        if request.user.is_authenticated:
            comment = Comment.objects.create(
                msg=request.data['msg'],
                user=request.user,
                post=post
            )
            reward, created = Reward.objects.get_or_create(user=request.user)
            # reward.points += 5  
            reward.save() 

            self.check_for_badges(reward)
        else:
            comment = Comment.objects.create(
                msg=request.data['msg'],
                post=post
            )
        serializer_comment = CommentSerializer(comment)
        return Response(serializer_comment.data, status=status.HTTP_200_OK)
    
    def check_for_badges(self, reward):
        if reward.points >= 0 and not reward.badges.filter(name="Newbie Badge").exists():
            newbie_badge = Badge.objects.get(name="Newbie Badge")
            reward.badges.add(newbie_badge)

        if reward.points >= 10 and not reward.badges.filter(name="Finder Badge").exists():
            finder_badge = Badge.objects.get(name="Finder Badge")
            reward.badges.add(finder_badge)

        if reward.points >= 50 and not reward.badges.filter(name="Active Contributor Badge").exists():
            active_contributor_badge = Badge.objects.get(name="Active Contributor Badge")
            reward.badges.add(active_contributor_badge)

        reward.save()


class PostAPI(APIView):

    def get(self, request):
        search_title = request.GET.get('search_title')
        search_location = request.GET.get('search_location')
        posts = Post.objects.filter(
            title__icontains=search_title, location__icontains=search_location)

        search_date = request.GET.get('search_date')
        if search_date != '':
            date_time = datetime.strptime(search_date, "%d/%m/%Y")
            posts = posts.filter(date_time__year=date_time.year,
                                 date_time__month=date_time.month, date_time__day=date_time.day)

        search_assetType = request.GET.get('search_assetType')
        if search_assetType != '-1':
            posts = posts.filter(
                assetType=AssetType.objects.get(id=search_assetType))

        search_type = request.GET.get('search_type')
        # search_type = 'lost'
        if search_type != '-1':
            posts = posts.filter(type=search_type)

        search_is_active = request.GET.get('search_is_active')
        if search_is_active != '-1':
            posts = posts.filter(is_active=bool(int(search_is_active)))

        posts = posts.order_by('-is_active', '-create_at')

        assetTypes = AssetType.objects.all()

        serializer_posts = PostSerializer(posts, many=True)
        serializer_assetTypes = AssetTypeSerializer(assetTypes, many=True)

        return Response([serializer_posts.data, serializer_assetTypes.data], status=status.HTTP_200_OK)

    def patch(self, request):
        post_id = request.data.get('post_id')
        post = Post.objects.get(id=post_id)

        post.is_active = False
        post.take_information = request.data.get('message')
        post.save()

        return Response({'post_id': post_id}, status=status.HTTP_200_OK)


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        losts = Post.objects.filter(type='lost')
        founds = Post.objects.filter(type='found')
        active = len(founds.filter(is_active=True))

        return render(request, self.template_name, {
            'losts': losts,
            'founds': founds,
            'active': active,
            'closed': len(founds) - active,
            'all': len(founds) + len(losts)
        })


class CreateView(View):
    template_name = 'create.html'
    PictureFormSet = formset_factory(PostPictureForm, extra=0)

    def get(self, request):
        form = PostForm()
        formset = self.PictureFormSet()
        return render(request, self.template_name, {
            'form': form,
            'formset': formset
        })

    def post(self, request):
        form = PostForm(request.POST)
        if (datetime.now() < datetime.strptime(request.POST.get("date_time"), '%d/%m/%Y %H:%M')):
            return render(request, self.template_name, {
                'form': form,
                'formset': self.PictureFormSet(),
                'key_error': 'Please select a date that is current or in the past only.'
            })
        formset = self.PictureFormSet(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.user = request.user
                if post.type == 'found':  
                    reward, created = Reward.objects.get_or_create(user=request.user)
                    # reward.points += 10  
                    reward.save()
                    self.check_for_badges(reward)
            else:
                post.key = request.POST.get('key')
                if (len(post.key) < 6):
                    return render(request, self.template_name, {
                        'form': form,
                        'formset': self.PictureFormSet(),
                        'key_error': 'Please enter a key with at least 6 characters.'
                    })
                for i in Post.objects.all():
                    if i.key == post.key:
                        return render(request, self.template_name, {
                            'form': form,
                            'formset': self.PictureFormSet(),
                            'key_error': 'This key already exists in the system.'
                        })
            post.save()
            if request.POST.get('form-TOTAL_FORMS') != '0':
                for picture in formset:
                    if picture.is_valid():
                        picture = picture.save(commit=False)
                        picture.post = post
                        picture.save() 

                # Check for similar lost posts if the new post is a "found" item
            if post.type == 'found':
                lost_posts = Post.objects.filter(type='lost')
                similar_posts = find_similar_lost_posts(post, lost_posts, threshold=0.7)

                # Pass the similar posts to the template or handle as needed
                return render(request, 'similar_posts.html', {
                    'post': post,
                    'similar_posts': similar_posts
                })

                # Pass the similar posts to the template or handle as needed
               
                       
            return redirect('detail', post_id=post.id)
        else:
            return render(request, self.template_name, {
                'form': form,
                'formset': self.PictureFormSet()
            })
        
    def check_for_badges(self, reward):
        if reward.points >= 0 and not reward.badges.filter(name="Newbie Badge").exists():
            newbie_badge = Badge.objects.get(name="Newbie Badge")
            reward.badges.add(newbie_badge)

        if reward.points >= 10 and not reward.badges.filter(name="Finder Badge").exists():
            finder_badge = Badge.objects.get(name="Finder Badge")
            reward.badges.add(finder_badge)

        if reward.points >= 50 and not reward.badges.filter(name="Active Contributor Badge").exists():
            active_contributor_badge = Badge.objects.get(name="Active Contributor Badge")
            reward.badges.add(active_contributor_badge)

        reward.save()


class DetailView(View):
    template_name = 'detail1.html'

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        return render(request, self.template_name, {
            'post': post
        })

class EditPostView(View):
    template_name = 'edit_post.html'
    PictureFormSet = formset_factory(PostPictureForm, extra=0)

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        form = PostForm(instance=post)

        if request.user.is_authenticated:
            if request.user != post.user:  # If logged in and editing a post that was not created by the user
                return redirect('index')
        elif post.key == None:  # If not logged in and trying to edit a post created by a logged-in user
            return redirect('index')

        formset = self.PictureFormSet()

        return render(request, self.template_name, {
            'form': form,
            'post': post,
            'pictures': post.postpicture_set.all(),
            'formset': formset,
            'anonymous': True if post.user == None else False,
        })

    def post(self, request, post_id):

        post = Post.objects.get(id=post_id)
        form = PostForm(request.POST, instance=post)

        formset = self.PictureFormSet(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)

            if post.user == None and request.POST.get('key') != post.key:
                return render(request, self.template_name, {
                    'form': form,
                    'post': post,
                    'pictures': post.postpicture_set.all(),
                    'formset': formset,
                    'anonymous': True if post.user == None else False,
                    'key_error': 'Incorrect key'
                })

            post.save()

            # If there are deleted images (JS will set the value of input:hidden to 0)
            for picture in post.postpicture_set.all():
                value = request.POST.get(f'{picture.id}')
                if value == '0':
                    picture.delete()

            if request.POST.get('form-TOTAL_FORMS') != '0':
                for picture in formset:
                    if picture.is_valid():
                        picture = picture.save(commit=False)
                        picture.post = post
                        picture.save()

            return render(request, self.template_name, {
                'form': form,
                'post': post,
                'pictures': post.postpicture_set.all(),
                'formset': formset,
                'anonymous': True if post.user == None else False,
                'success': 'Post information has been successfully edited.'
            })
        else:
            return render(request, self.template_name, {
                'form': form,
                'post': post,
                'pictures': post.postpicture_set.all(),
                'formset': formset,
                'anonymous': True if post.user == None else False,
            })


@login_required
def delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.key is None and post.user != request.user:
        return redirect('index')
    elif post.key is not None:
        key = request.GET.get('key')
        if post.key != key:
            return redirect('index')

    post.is_active = False  
    post.save()

    closed_count = Post.objects.filter(user=request.user, is_active=False).count()
    return redirect('my_posts')

