from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ChatAPI(APIView):
    def get(self, request):
        search = request.GET.get('search')
        users = User.objects.filter(username__icontains=search)
        data, no_message = [], []
        for user in users:
            if user == request.user:
                continue
            sends = request.user.chat.message_set.filter(to=user).order_by('-timestamp')
            gets = Message.objects.filter(chat=user.chat, to=request.user).order_by('-timestamp')

            if len(sends) != 0 and len(gets) != 0:
                if sends[0].timestamp > gets[0].timestamp:
                    message = sends[0].message
                    date_time = sends[0].timestamp
                    seen = True
                else:
                    message = gets[0].message
                    date_time = gets[0].timestamp
                    seen = gets[0].seen
            elif len(sends) != 0:
                message = sends[0].message
                date_time = sends[0].timestamp
                seen = True
            elif len(gets) != 0:
                message = gets[0].message
                date_time = gets[0].timestamp
                seen = gets[0].seen
            else:
                no_message.append([user.username, '', '', user.userprofile.avatar.url, user.id, ''])
                continue

            data.append([user.username, message, date_time, user.userprofile.avatar.url, user.id, seen])

        data.sort(key=lambda x : x[2], reverse=True)
        data.extend(no_message)
        return Response([data, request.user.chat.theme], status=status.HTTP_200_OK)

    def patch(self, request):
        chat = request.user.chat

        theme = request.data.get('change_to')
        chat.theme = theme
        chat.save()

        return Response(status=status.HTTP_200_OK)

@method_decorator(login_required, name='dispatch')
class MessageAPI(APIView):

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)

        # get conversation msg

        sends = request.user.chat.message_set.filter(to=user).order_by('timestamp')
        gets = Message.objects.filter(chat=user.chat, to=request.user).order_by('timestamp')


        gets.update(seen=True)

        sends_serializer = MessageSerializer(sends, many=True)
        gets_serializer = MessageSerializer(gets, many=True)
        # return
        return Response({
            'sends' : sends_serializer.data,
            'gets' : gets_serializer.data,
            'url' : user.userprofile.avatar.url
            }, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        message = Message.objects.create(
            message=request.data['message'],
            seen=False,
            chat=request.user.chat,
            to=user
        )

        message_serializer = MessageSerializer(message)

        return Response(message_serializer.data, status=status.HTTP_200_OK)

@method_decorator(login_required, name='dispatch')
class ChatIndexView(View):
    template_name = 'chat_index.html'

    def get(self, request):
        return render(request, self.template_name, {
            'theme' : request.user.chat.theme
        })
    
@login_required
def chat_detail(request, user_id):
    # Get the post owner (recipient)
    post_owner = get_object_or_404(User, id=user_id)

    # Ensure the current user is not the post owner
    if post_owner == request.user:
        return redirect('index')  # Redirect to the home page or another appropriate view

    # Render the chat interface
    return render(request, 'chats/chat_detail.html', {
        'post_owner': post_owner,
    })