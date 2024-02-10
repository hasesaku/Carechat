from django.urls import path
from . import views
from .views import mypage_view, chat_view, support_view
from .views import edit_profile

app_name = 'firstapp'  # 名前空間の名前を設定

urlpatterns = [
    path('', views.start_screen, name='start_screen'),  # ホームページのURLを追加
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # `login`ビューへのパスを修正
    path('home/', views.home_view, name='home'),  # ホーム画面のURLパターンを追加
    path('edit_profile/', edit_profile, name='edit_profile'),
    # path('chat/', views.chat_view, name='chat'),
    path('chat/', views.chat_rooms, name='chat_rooms'),  # チャットルーム一覧ビューへのパス
    path('chat_rooms/', views.chat_rooms, name='chat_rooms'),
    path('chat_room/<int:room_id>/', views.chat_room, name='chat_room'),  # 修正: chat_rooms/を追加して区別    path('like_message/', views.like_message, name='like_message'),
    # 他のURLパターン...
]

urlpatterns += [
    path('mypage/', mypage_view, name='mypage'),
    # path('chat/', chat_view, name='chat'),
    path('support/', support_view, name='support'),
    # ログアウト機能のURLを追加
    path('logout/', views.logout_view, name='logout'),
]