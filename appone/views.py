from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, Conversation
from django.db.models import Count, Q
from .forms import UserForm, ProfileForm


@login_required
def conversations_list(request):
    user = request.user
    conversations = (
        Conversation.objects
        .filter(members=user)
        .annotate(message_count=Count('messages'))
    )

    convo_data = []
    used_user_ids = set()
    for convo in conversations:
        other_user = convo.members.exclude(id=user.id).first()
        if other_user:
            convo_data.append({
                'convo': convo,
                'other_user': other_user,
                'message_count': convo.message_count,
            })
            used_user_ids.add(other_user.id)

    users = User.objects.exclude(id=request.user.id).exclude(id__in=used_user_ids)

    return render(request, 'chat/conversations_list.html', {
        'conversations': convo_data,
        'users': users,
    })

# Список всех бесед пользователя\@login_required
# def conversations_list(request):
#     convos = request.user.conversations.all()
#     return render(request, 'chat/conversations_list.html', {'conversations': convos})

# Открытие или создание личной беседы с другим пользователем
@login_required
def open_conversation(request, username):
    other = get_object_or_404(User, username=username)
    if other == request.user:
        return redirect('chat:conversations_list')

    convo = Conversation.objects.filter(members=request.user).filter(members=other).first()
    if not convo:
        convo = Conversation.objects.create()
        convo.members.add(request.user, other)
        convo.save()

    return redirect('chat:conversation_detail', convo_id=convo.id)

@login_required
def conversation_detail(request, convo_id):
    convo = get_object_or_404(Conversation, id=convo_id)
    if request.user not in convo.members.all():
        return redirect('chat:conversations_list')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(conversation=convo, author=request.user, content=content)
        return redirect('chat:conversation_detail', convo_id=convo.id)

    messages = convo.messages.order_by('timestamp')
    other_user = convo.members.exclude(id=request.user.id).first()
    return render(request, 'chat/conversation.html', {
        'conversation': convo,
        'messages': messages,
        'other_user': other_user,
    })

# Регистрация
class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'chat/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat:conversations_list')
        return render(request, 'chat/signup.html', {'form': form})

# Вход
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'chat/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat:conversations_list')
        return render(request, 'chat/login.html', {'form': form})

# Выход
class LogoutConfirmationView(View):
    def get(self, request):
        return render(request, 'chat/logout_confirmation.html')

    def post(self, request):
        logout(request)
        return redirect('chat:login')

# Функция для удаления сообщения
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.author == request.user:
        message.delete()
    return redirect('chat:conversation_detail', convo_id=message.conversation.id)

# Функция для обновления сообщения
@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.author == request.user:
        if request.method == 'POST':
            message.content = request.POST.get('content')
            message.save()
            return redirect('chat:conversation_detail', convo_id=message.conversation.id)  # Редирект обратно в чат
        return render(request, 'edit_message.html', {'message': message})  # Шаблон для редактирования
    return redirect('chat:conversations_list')  # Если пользователь не автор сообщения, перенаправляем на список бесед



@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        uform = UserForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, instance=user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            return redirect('chat:profile')
    else:
        uform = UserForm(instance=user)
        pform = ProfileForm(instance=user.profile)
    return render(request, 'chat/profile.html', {'uform': uform, 'pform': pform})

@login_required
def users_list(request):
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)
    if query:
        users = users.filter(username__icontains=query)
    return render(request, 'chat/users_list.html', {'users': users, 'query': query})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'chat/user_detail.html', {'other_user': user})


@login_required
def settings_view(request):
    # Обработка формы "Задать вопрос"
    if request.method == 'POST':
        question = request.POST.get('question')
        # Здесь можно сохранить вопрос в модели или отправить на email
        request.session['msg_sent'] = True
        return redirect('chat:settings')

    msg_sent = request.session.pop('msg_sent', False)
    return render(request, 'chat/settings.html', {
        'msg_sent': msg_sent
    })
