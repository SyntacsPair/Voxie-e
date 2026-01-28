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
    [POST] Piper TTS를 이용한 고품질 AI 음성 생성
    - 모델: ko_KR-onnuri-medium (오픈소스 한국어 모델)
    - 파일: .onnx (AI모델) + .json (설정파일) 사용
    """
    text = request.data.get('text', '')
    if not text:
        return Response({"error": "텍스트를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    # 1. 모델 파일이 저장될 경로 설정
    model_dir = "/app/piper_models"
    model_name = "ko_KR-onnuri-medium"
    onnx_path = f"{model_dir}/{model_name}.onnx"
    json_path = f"{model_dir}/{model_name}.onnx.json"
    output_wav = f"/tmp/output_{os.getpid()}.wav" # 임시 결과 파일

    try:
        # 2. 모델 파일이 없으면 자동으로 다운로드 (최초 1회만 실행됨)
        if not os.path.exists(onnx_path):
            print("🚀 모델 파일이 없습니다. 다운로드를 시작합니다...")
            os.makedirs(model_dir, exist_ok=True)
            
            # (1) .onnx 파일 다운로드 (약 60MB)
            subprocess.run(
                f"curl -L -o {onnx_path} https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ko/ko_KR/onnuri/medium/ko_KR-onnuri-medium.onnx",
                shell=True, check=True
            )
            # (2) .json 파일 다운로드 (설정 파일)
            subprocess.run(
                f"curl -L -o {json_path} https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ko/ko_KR/onnuri/medium/ko_KR-onnuri-medium.onnx.json",
                shell=True, check=True
            )
            print("✅ 모델 다운로드 완료!")

        # 3. Piper 실행 (리눅스 명령어)
        # echo "텍스트" | piper --model 모델파일 --output_file 결과파일
        cmd = f'echo "{text}" | piper --model {onnx_path} --output_file {output_wav}'
        subprocess.run(cmd, shell=True, check=True)

        # 4. 생성된 WAV 파일을 읽어서 응답으로 전송
        f = open(output_wav, 'rb')
        return FileResponse(f, content_type='audio/wav')

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

@api_view(['GET', 'DELETE'])
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