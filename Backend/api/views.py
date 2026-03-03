import os
import subprocess
import time
import io # <--- 추가됨
from gtts import gTTS # <--- 추가됨
from django.http import FileResponse # <--- 추가됨
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User  # ★ DB 조회용 임포트

# =================================================================
# [Part 1] TTS Generation (구글 TTS 적용됨)
# =================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def tts_generate(request):
    """
    [POST] Google TTS를 이용한 음성 생성
    - gTTS 라이브러리 사용 (크로스 플랫폼 지원)
    """
    text = request.data.get('text', '')
    if not text:
        return Response({"error": "텍스트를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        tts = gTTS(text=text, lang='ko')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return FileResponse(audio_buffer, content_type='audio/mpeg', filename='tts_output.mp3')

    except Exception as e:
        print(f"❌ TTS Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =================================================================
# [Part 2] History & Voices (Mock 데이터 유지)
# =================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def tts_voices(request):
    """
    [GET] 목소리 목록 조회
    API: /api/v1/tts/voices
    """
    data = [
        {"id": 1, "name": "SunHi", "code": "ko-KR-SunHiNeural", "gender": "Female", "lang": "한국어", "desc": "한국어 여성 음성"},
        {"id": 2, "name": "InJoon", "code": "ko-KR-InJoonNeural", "gender": "Male", "lang": "한국어", "desc": "한국어 남성 음성"},
        {"id": 3, "name": "Aria", "code": "en-US-AriaNeural", "gender": "Female", "lang": "English", "desc": "영어 여성 음성"},
        {"id": 4, "name": "Guy", "code": "en-US-GuyNeural", "gender": "Male", "lang": "English", "desc": "영어 남성 음성"},
    ]
    return Response({"count": len(data), "results": data})

@api_view(['GET'])
@permission_classes([AllowAny])
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

@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def history_download(request, history_id):
    """
    [GET] 오디오 다운로드
    API: /api/v1/tts/history/{id}/audio
    """
    return Response({"message": "다운로드 링크 제공"}, status=status.HTTP_200_OK)


# =================================================================
# [Part 3] User 관련 (★ DB 조회 유지)
# =================================================================

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