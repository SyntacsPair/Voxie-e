import os
import subprocess
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# =================================================================
# [Part 1] TTS Generation (Piper - KSS 모델 적용)
# =================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def tts_generate(request):
    text = request.data.get('text', '')
    if not text:
        return Response({"error": "텍스트를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    # 서버 내부 경로 (수정 금지)
    model_path = "/app/voice/KSS/KSS.onnx"
    output_wav = f"/tmp/output_{os.getpid()}.wav"

    try:
        # 모델 있는지 확인
        if not os.path.exists(model_path):
             return Response({"error": f"모델 파일이 없습니다: {model_path}"}, status=500)

        # Piper 실행 (리눅스 명령어)
        cmd = f'echo "{text}" | piper --model {model_path} --output_file {output_wav}'
        subprocess.run(cmd, shell=True, check=True)

        # 결과 전송
        f = open(output_wav, 'rb')
        return FileResponse(f, content_type='audio/wav')

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# =================================================================
# [Part 2] History & Voices (Mock 데이터 유지)
# =================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def tts_voices(request):
    """
    [GET] 목소리 목록 조회
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
@permission_classes([IsAuthenticated])
def history_detail(request, history_id):
    """
    [GET/DELETE] 히스토리 상세 조회 및 삭제
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
        return Response({
            "message": f"히스토리 {history_id}번이 삭제되었습니다.",
            "deleted_id": history_id
        }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_download(request, history_id):
    """
    [GET] 오디오 다운로드
    """
    return Response({"message": "다운로드 링크 제공"}, status=status.HTTP_200_OK)


# =================================================================
# [Part 3] User 관련
# =================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def check_email(request):
    """
    [GET] 이메일 중복 검사
    """
    email = request.query_params.get('email', None)
    
    if not email:
        return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"is_available": False, "message": "이미 사용 중인 이메일입니다."}, status=status.HTTP_200_OK)
    
    return Response({"is_available": True, "message": "사용 가능한 이메일입니다."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request):
    """
    [GET] 닉네임(ID) 중복 검사
    """
    nickname = request.query_params.get('nickname', None)
    
    if not nickname:
        return Response({"message": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=nickname).exists():
        return Response({"is_available": False, "message": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_200_OK)
    
    return Response({"is_available": True, "message": "멋진 닉네임이네요!"}, status=status.HTTP_200_OK)