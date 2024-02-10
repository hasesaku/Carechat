from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login # `login` を `auth_login` としてインポートして名前の衝突を避ける
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import ChatRoom, Message, Like
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm

# スタート画面のビュー
def start_screen(request):
    return render(request, 'firstapp/start_screen.html')

# 新規ユーザー登録ビューの更新版
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        nickname = request.POST['nickname']
        
        # ユーザー名としてメールアドレスを使用
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = nickname  # ニックネームをfirst_nameフィールドに保存
        user.save()
        
        # ユーザーを自動的にログインさせてホームページにリダイレクト
        auth_user = authenticate(username=email, password=password)
        if auth_user:
            auth_login(request, auth_user)
            return redirect('firstapp:home')
        else:
            return render(request, 'firstapp/register.html', {'error': 'ユーザーの作成に失敗しました。'})
    else:
        return render(request, 'firstapp/register.html')

# login 関数の定義を修正...
def login_view(request):
    # POSTリクエストの場合、ログイン処理を実行
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)  # `auth_login` を使用
            return redirect('firstapp:home')  # 名前空間を使用したリダイレクト先の指定
        else:
            # 認証失敗時のエラーメッセージを追加
            return render(request, 'firstapp/login.html', {'error': 'メールアドレスまたはパスワードが間違っています。'})  # パスを修正
    else:
        return render(request, 'firstapp/login.html')  # パスを修正

def home_view(request):
    # ホーム画面のテンプレートに遷移
    return render(request, 'firstapp/home.html')

def logout_view(request):
    # ユーザーをログアウトさせる
    auth_logout(request)
    # スタート画面にリダイレクト
    return redirect('firstapp:start_screen')

def mypage_view(request):
    # マイページのビュー
    return render(request, 'firstapp/mypage.html')

def chat_view(request):
    # チャット画面のビュー
    return render(request, 'firstapp/chat.html')

def support_view(request):
    # サポート機能のビュー
    return render(request, 'firstapp/support.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('firstapp:mypage')  # 編集後はマイページにリダイレクト
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'firstapp/edit_profile.html', {'form': form})

def chat_rooms(request):
    rooms = ChatRoom.objects.all()
    return render(request, 'firstapp/chat_rooms.html', {'rooms': rooms})

@login_required
def chat_room(request, room_id):
    # get_object_or_404の第二引数をカスタム主キーに合わせて修正
    room = get_object_or_404(ChatRoom, pk=room_id)  # `id=room_id`から`pk=room_id`へ修正
    messages = Message.objects.filter(chat_room=room)
    if request.method == 'POST':
        message_text = request.POST.get('message_text')
        Message.objects.create(chat_room=room, user=request.user, text=message_text)
        return redirect('firstapp:chat_room', room_id=room.pk)  # `room.id`を`room.pk`に修正
    return render(request, 'firstapp/chat.html', {'room': room, 'messages': messages})

@login_required
def like_message(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        like, created = Like.objects.get_or_create(message=message, user=request.user)
        if not created:
            like.delete() # 既に「いいね」があれば削除するオプション
            return JsonResponse({'liked': False})
        return JsonResponse({'liked': True})
    return JsonResponse({'error': 'POST request required.'}, status=400)