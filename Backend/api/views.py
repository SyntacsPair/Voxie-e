import os
import tempfile
import asyncio
import edge_tts
from django.http import FileResponse, StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# =================================================================
# [Helper Function] Edge-TTS 비동기 실행기 (Speed 파라미터 추가!)
# =================================================================
def generate_edge_tts(text, output_file, voice="ko-KR-SunHiNeural", speed=1.0):
    """ 동기(Sync) 장고 뷰에서 비동기(Async) edge-tts를 실행하기 위한 헬퍼 함수 """
    
    # 프론트엔드의 1.0, 1.5 같은 배수를 edge-tts용 퍼센트 문자열(+50%, -20% 등)로 자동 변환
    try:
        rate_percent = int((float(speed) - 1.0) * 100)
        rate_str = f"{rate_percent:+d}%" # 예: +50%, -20%, +0%
    except ValueError:
        rate_str = "+0%" # 숫자가 아닌 이상한 값이 오면 기본 속도로 방어

    async def _generate():
        communicate = edge_tts.Communicate(text, voice, rate=rate_str)
        await communicate.save(output_file)
    
    asyncio.run(_generate())


# =================================================================
# [TTS Generate] Edge-TTS 실제 연동 (Speed 파라미터 추가!)
# =================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def tts_generate(request):
    """ [POST] /api/v1/generate : 음성 생성 """
    text = request.data.get('text', '')
    voice_code = request.data.get('voice', 'ko-KR-SunHiNeural') 
    
    # 프론트에서 넘어온 speed 값 (안 보내면 기본값 1.0)
    speed_val = request.data.get('speed', 1.0) 
    
    if not text:
        return Response({"error": "텍스트를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    temp_dir = tempfile.gettempdir()
    output_mp3 = os.path.join(temp_dir, f"output_edge_{os.getpid()}.mp3")

    try:
        # 1. Edge-TTS로 MP3 파일 저장 (speed 전달)
        generate_edge_tts(text, output_mp3, voice=voice_code, speed=speed_val)

        # 2. 프론트엔드로 파일 전송
        f = open(output_mp3, 'rb')
        return FileResponse(f, content_type='audio/mpeg')

    except Exception as e:
        return Response({"error": f"Edge-TTS 변환 실패: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =================================================================
# [System & Voice] 서버 상태 및 목소리 목록 (명세서 1순위)
# =================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """ [GET] /health : 서버 상태 확인 """
    return Response({"status": "OK", "message": "Server is running smoothly."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def voice_list(request):
    """ [GET] /api/voices : Edge-TTS 지원 목소리 목록 """
    data = [
        {"id": 1, "name": "선희 (SunHi)", "code": "ko-KR-SunHiNeural", "gender": "Female", "desc": "차분한 한국어 여성 음성", "img_url": "/static/sunhi.png"},
        {"id": 2, "name": "인준 (InJoon)", "code": "ko-KR-InJoonNeural", "gender": "Male", "desc": "안정적인 한국어 남성 음성", "img_url": "/static/injoon.png"},
        {"id": 3, "name": "아리아 (Aria)", "code": "en-US-AriaNeural", "gender": "Female", "desc": "자연스러운 미국 영어", "img_url": "/static/aria.png"},
        {"id": 4, "name": "가이 (Guy)", "code": "en-US-GuyNeural", "gender": "Male", "desc": "신뢰감 있는 미국 영어", "img_url": "/static/guy.png"},
    ]
    return Response({"count": len(data), "results": data}, status=status.HTTP_200_OK)


 # 더미) 스트리밍 응답 (실제 Edge-TTS 스트리밍이 아니므로 더미 데이터 반환)
@api_view(['POST'])
@permission_classes([AllowAny])
def tts_generate_stream(request):
    """ [POST] /api/generate/stream : 음성 생성 스트리밍 """
    def dummy_stream():
        yield b"dummy audio byte stream"
    return StreamingHttpResponse(dummy_stream(), content_type="audio/mpeg")


# =================================================================
# [History] 기록 관리 (# 더미) (명세서 3순위)
# =================================================================
# 더미) 히스토리 목록 조회 및 저장
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def history_list(request):
    """ [GET/POST] /api/history : 히스토리 목록 조회 및 저장  """
    if request.method == 'GET':
        data = [
            {"id": 102, "text": "안녕하세요, 선희입니다.", "voice_name": "선희 (SunHi)", "status": "COMPLETED", "created_at": "2026-02-23T14:30:00Z", "audio_url": "https://sample-videos.com/audio/mp3/crowd-cheering.mp3"},
            {"id": 101, "text": "반갑습니다, 인준입니다.", "voice_name": "인준 (InJoon)", "status": "PROCESSING", "created_at": "2026-02-23T14:28:00Z", "audio_url": None}
        ]
        return Response({"count": 2, "next": None, "previous": None, "results": data})
    
    elif request.method == 'POST':
        return Response({"message": "기록이 저장되었습니다.", "id": 103}, status=status.HTTP_201_CREATED)

# 더미) 히스토리 상세 조회 및 삭제
@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
def history_detail(request, history_id):
    """ [GET/DELETE] /api/history/{id} : 히스토리 상세 조회 및 삭제  """
    if request.method == 'GET':
        return Response({
            "id": history_id,
            "text": f"상세 조회한 텍스트 내용입니다. (ID: {history_id})",
            "voice": {"code": "ko-KR-SunHiNeural", "name": "선희 (SunHi)"},
            "status": "COMPLETED",
            "created_at": "2026-02-23T14:30:00Z"
        })
    elif request.method == 'DELETE':
        return Response({"message": f"히스토리 {history_id}번이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# 더미) 히스토리 오디오 다운로드 (실제 파일이 없으므로 더미 응답)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_download(request, history_id):
    """ [GET] /api/history/{id}/download : 오디오 다운로드  """
    return Response({"message": "다운로드 링크 제공"}, status=status.HTTP_200_OK)


# =================================================================
# [User] 이메일 & 닉네임 중복 검사
# =================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def check_email(request):
    email = request.query_params.get('email', None)
    if not email: return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists(): return Response({"is_available": False, "message": "이미 사용 중인 이메일입니다."}, status=status.HTTP_200_OK)
    return Response({"is_available": True, "message": "사용 가능한 이메일입니다."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request):
    nickname = request.query_params.get('nickname', None)
    if not nickname: return Response({"message": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=nickname).exists(): return Response({"is_available": False, "message": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_200_OK)
    return Response({"is_available": True, "message": "멋진 닉네임이네요!"}, status=status.HTTP_200_OK)