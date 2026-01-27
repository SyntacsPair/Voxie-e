import time
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User  # ★ DB 조회용 임포트

# =================================================================
# [Part 1] TTS & History (아직 기능 구현 전이라 Mock 데이터 유지)
# =================================================================

@api_view(['POST'])
@permission_classes([AllowAny]) # 나중에 IsAuthenticated로 변경 필요
def tts_generate(request):
    """
    [POST] TTS 음성 생성 요청
    API: /api/v1/tts/generate
    """
    # 프론트 로딩바 테스트를 위한 1초 딜레이
    time.sleep(1)
    
    return Response({
        "id": 101,
        "status": "PENDING",
        "message": "음성 생성이 요청되었습니다.",
        "estimated_time": "5 seconds"
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def tts_voices(request):
    """
    [GET] 목소리 목록 조회
    API: /api/v1/tts/voices
    """
    data = [
        {"id": 1, "name": "Alloy", "code": "alloy", "gender": "Neutral", "desc": "다목적, 중성적", "img_url": "/static/alloy.png"},
        {"id": 2, "name": "Echo", "code": "echo", "gender": "Male", "desc": "부드러운 중저음", "img_url": "/static/echo.png"},
        {"id": 3, "name": "Fable", "code": "fable", "gender": "British", "desc": "영국식 억양", "img_url": "/static/fable.png"},
        {"id": 4, "name": "Onyx", "code": "onyx", "gender": "Male", "desc": "깊고 중후한 톤", "img_url": "/static/onyx.png"},
        {"id": 5, "name": "Nova", "code": "nova", "gender": "Female", "desc": "차분하고 여성적", "img_url": "/static/nova.png"},
        {"id": 6, "name": "Shimmer", "code": "shimmer", "gender": "Female", "desc": "맑고 깨끗한 톤", "img_url": "/static/shimmer.png"},
    ]
    return Response({"count": len(data), "results": data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_list(request):
    """
    [GET] 히스토리 목록 조회
    API: /api/v1/tts/history
    """
    data = [
        {
            "id": 102,
            "text": "안녕하세요, 반가워요.",
            "voice_name": "Alloy",
            "status": "COMPLETED",
            "created_at": "2026-01-27 14:30:00",
            "audio_url": "https://sample-videos.com/audio/mp3/crowd-cheering.mp3"
        },
        {
            "id": 101,
            "text": "이것은 긴 텍스트 테스트입니다.",
            "voice_name": "Echo",
            "status": "PROCESSING",
            "created_at": "2026-01-27 14:28:00",
            "audio_url": None
        }
    ]
    return Response({
        "count": 15,
        "next": "http://api.../history?page=2",
        "previous": None,
        "results": data
    })

@api_view(['GET', 'DELETE']) # ★ DELETE 메서드 추가됨!
@permission_classes([IsAuthenticated])
def history_detail(request, history_id):
    """
    [GET/DELETE] 히스토리 상세 조회 및 삭제
    API: /api/v1/tts/history/{id}
    """
    # 1. 상세 조회
    if request.method == 'GET':
        return Response({
            "id": history_id,
            "text": f"상세 조회한 텍스트 내용입니다. (ID: {history_id})",
            "voice": {"code": "alloy", "name": "Alloy"},
            "speed": 1.0,
            "status": "COMPLETED",
            "audio_url": "https://sample-videos.com/audio/mp3/crowd-cheering.mp3",
            "created_at": "2026-01-27 14:30:00"
        })
    
    # 2. 삭제 (DELETE)
    elif request.method == 'DELETE':
        # 실제 DB 삭제 로직은 나중에: TtsGeneration.objects.get(id=history_id).delete()
        return Response({
            "message": f"히스토리 {history_id}번이 삭제되었습니다.",
            "deleted_id": history_id
        }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_download(request, history_id):
    """
    [GET] 오디오 다운로드
    API: /api/v1/tts/history/{id}/audio
    """
    return Response({"message": "다운로드 링크 제공"}, status=status.HTTP_200_OK)


# =================================================================
# [Part 2] User 관련 (★ 진짜 DB 조회 로직 구현됨)
# =================================================================
# ※ 주의: 로그인, 회원가입, 로그아웃, 토큰재발급, 프로필조회는 
#    urls.py에서 dj-rest-auth 라이브러리와 직접 연결했으므로 여기엔 코드가 없어야 합니다!
#    (중복 작성 시 헷갈림 방지)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_email(request):
    """
    [GET] 이메일 중복 검사 (Real DB)
    API: /api/v1/users/email-availability?email=...
    """
    email = request.query_params.get('email', None)
    
    if not email:
        return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    # 실제 DB 조회
    if User.objects.filter(email=email).exists():
        return Response({"is_available": False, "message": "이미 사용 중인 이메일입니다."}, status=status.HTTP_200_OK)
    
    return Response({"is_available": True, "message": "사용 가능한 이메일입니다."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request):
    """
    [GET] 닉네임(ID) 중복 검사 (Real DB)
    API: /api/v1/users/nickname-availability?nickname=...
    """
    nickname = request.query_params.get('nickname', None)
    
    if not nickname:
        return Response({"message": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    # 실제 DB 조회 (auth_user 테이블의 username 컬럼 확인)
    if User.objects.filter(username=nickname).exists():
        return Response({"is_available": False, "message": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_200_OK)
    
    return Response({"is_available": True, "message": "멋진 닉네임이네요!"}, status=status.HTTP_200_OK)