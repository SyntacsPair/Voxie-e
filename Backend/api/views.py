import os
import tempfile
import asyncio
import uuid
import edge_tts
from django.http import FileResponse, StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .rvc import convert_voice_with_rvc

# =================================================================
# ⚙️ [백엔드 전용] 캐릭터별 하드코딩 설정
# =================================================================
CHARACTER_SETTINGS = {
    # 남성 캐릭터 (기본 여성 목소리에서 변조하므로 피치를 크게 내림)
    "Trump": {"base_voice": "ko-KR-SunHiNeural", "pitch": -12},
    "Zoro": {"base_voice": "ko-KR-SunHiNeural", "pitch": -12},
    "MJ": {"base_voice": "ko-KR-SunHiNeural", "pitch": -12}, # 마이클 잭슨 등 남성이라 가정
    
    # 소년 캐릭터 (약간만 내림)
    "Luffy": {"base_voice": "ko-KR-SunHiNeural", "pitch": -3},
    
    # 여성 캐릭터 (피치 변경 없음 또는 살짝 올림)
    "NELL": {"base_voice": "ko-KR-SunHiNeural", "pitch": 0},
    "Yandere": {"base_voice": "ko-KR-SunHiNeural", "pitch": 2}, # 얀데레 특유의 하이톤을 위해 살짝 높임
    
    # 기본값
    "default": {"base_voice": "ko-KR-SunHiNeural", "pitch": 0}
}

# =================================================================
# [Helper Function] Edge-TTS 비동기 실행기
# =================================================================
def generate_edge_tts(text, output_file, voice="ko-KR-SunHiNeural", speed=1.0):
    try:
        rate_percent = int((float(speed) - 1.0) * 100)
        rate_str = f"{rate_percent:+d}%" 
    except ValueError:
        rate_str = "+0%" 

    async def _generate():
        communicate = edge_tts.Communicate(text, voice, rate=rate_str)
        await communicate.save(output_file)
    
    asyncio.run(_generate())


# =================================================================
# [TTS Generate] 프론트엔드 구조 그대로, 백엔드에서 RVC 덮어씌우기
# =================================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def tts_generate(request):
    """ [POST] /api/v1/generate : 음성 생성 """
    text = request.data.get('text', '')
    
    # 🚨 프론트에서는 "Trump", "Luffy" 등의 코드를 'voice'로 보냄
    voice_model = request.data.get('voice', 'NELL_V11') 
    speed_val = request.data.get('speed', 1.0) 

    if not text:
        return Response({"error": "텍스트를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    # 💡 백엔드 몰래 설정 가져오기 (피치값, 뼈대 목소리 종류)
    char_config = CHARACTER_SETTINGS.get(voice_model, CHARACTER_SETTINGS["default"])
    base_tts_voice = char_config["base_voice"]
    pitch_val = char_config["pitch"]

    temp_dir = tempfile.gettempdir()
    unique_id = uuid.uuid4().hex 
    base_mp3 = os.path.join(temp_dir, f"base_{unique_id}.mp3")
    final_wav = os.path.join(temp_dir, f"final_{unique_id}.wav")

    try:
        # 1. Edge-TTS로 뼈대 생성 (char_config에서 지정된 베이스 목소리로!)
        generate_edge_tts(text, base_mp3, voice=base_tts_voice, speed=speed_val)

        # 2. RVC 변조 (프론트가 보낸 voice_model 이름으로 Voice 폴더에서 .pth 찾기)
        convert_voice_with_rvc(
            input_path=base_mp3,
            output_path=final_wav,
            model_name=voice_model,
            pitch_adjust=pitch_val
        )
        
        # 3. 임시 뼈대 삭제 (서버 용량 보호)
        if os.path.exists(base_mp3):
            os.remove(base_mp3)

        # 4. 프론트로 결과물 던져주기
        f = open(final_wav, 'rb')
        return FileResponse(f, content_type='audio/wav')

    except Exception as e:
        if os.path.exists(base_mp3): os.remove(base_mp3)
        if os.path.exists(final_wav): os.remove(final_wav)
        return Response({"error": f"음성 변환 실패: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =================================================================
# [System & Voice] 서버 상태 및 목소리 목록
# =================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "OK", "message": "Server is running smoothly."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def voice_list(request):
    """ [GET] /api/voices : 지원하는 캐릭터(RVC) 목록으로 프론트엔드에 뿌려줌 """
    data = [
        {"id": 1, "name": "트럼프 (Trump)", "code": "Trump", "gender": "Male", "desc": "강렬한 미국 전 대통령 음성", "img_url": "/static/trump.png"},
        {"id": 2, "name": "조로 (Zoro)", "code": "Zoro", "gender": "Male", "desc": "무심하고 시크한 검사 음성", "img_url": "/static/zoro.png"},
        {"id": 3, "name": "루피 (Luffy)", "code": "Luffy", "gender": "Male", "desc": "텐션 높은 애니메이션 주인공", "img_url": "/static/luffy.png"},
        {"id": 4, "name": "엠제이 (MJ)", "code": "MJ", "gender": "Male", "desc": "부드럽고 개성 있는 음성", "img_url": "/static/mj.png"},
        {"id": 5, "name": "넬 (NELL)", "code": "NELL", "gender": "Female", "desc": "차분하고 매력적인 여성 음성", "img_url": "/static/nell.png"},
        {"id": 6, "name": "얀데레 (Yandere)", "code": "Yandere", "gender": "Female", "desc": "집착이 느껴지는(?) 독특한 톤", "img_url": "/static/yandere.png"},
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