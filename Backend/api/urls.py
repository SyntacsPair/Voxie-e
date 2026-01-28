from django.urls import path
from . import views # 우리가 만든 뷰 (Mock)

# ★ 라이브러리에서 뷰만 쏙쏙 뽑아오기
from dj_rest_auth.views import (
    LoginView, LogoutView, UserDetailsView
)
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # ============================================
    # 1. TTS 기능 (우리가 만든 Mock View 연결)
    # ============================================
    path('tts/generate', views.tts_generate, name='tts_generate'),
    path('tts/voices', views.tts_voices, name='tts_voices'),

    path('tts/history', views.history_list, name='history_list'),
    path('tts/history/<int:history_id>', views.history_detail, name='history_detail'),
    path('tts/history/<int:history_id>/audio', views.history_download, name='history_download'),

    # ============================================
    # 2. User 기능 (라이브러리 View + 커스텀 URL 매핑)
    # ============================================
    
    # [회원가입] POST api/v1/users/signup
    path('users/signup', RegisterView.as_view(), name='user_signup'),

    # [로그인] POST api/v1/users/login
    path('users/login', LoginView.as_view(), name='user_login'),

    # [로그아웃] POST api/v1/users/logout
    path('users/logout', LogoutView.as_view(), name='user_logout'),

    # [토큰 재발급] POST api/v1/users/reissue
    path('users/reissue', TokenRefreshView.as_view(), name='token_reissue'),

    # [프로필 조회/수정] GET/PUT api/v1/users/me
    path('users/me', UserDetailsView.as_view(), name='user_profile'),

    # ============================================
    # 3. 중복 검사 (라이브러리에 없어서 우리가 만든 뷰 유지)
    # ============================================
    
    # [이메일 중복 검사] GET api/v1/users/email-availability
    path('users/email-availability', views.check_email, name='check_email'),

    # [닉네임 중복 검사] GET api/v1/users/nickname-availability
    path('users/nickname-availability', views.check_nickname, name='check_nickname'),
]