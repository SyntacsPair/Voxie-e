from django.db import models
from django.contrib.auth.models import User # 장고 기본 유저

class Voice(models.Model):
    """
    목소리 옵션 관리 (Alloy, Echo 등)
    기획서 6번 API 명세의 GET /api/voices 대응
    """
    name = models.CharField(max_length=50, verbose_name="표시 이름") # 예: Alloy
    code = models.CharField(max_length=50, unique=True, verbose_name="API 코드") # 예: alloy
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Neutral')], verbose_name="성별")
    description = models.TextField(verbose_name="목소리 설명") # 예: 중성적, 균형잡힌 톤
    is_active = models.BooleanField(default=True, verbose_name="사용 가능 여부")

    def __str__(self):
        return self.name

class TTSGeneration(models.Model):
    """
    TTS 생성 요청 및 결과 히스토리
    기획서 3번 핵심 기능 & 6번 POST /api/generate 대응
    """
    STATUS_CHOICES = [
        ('PENDING', '대기중'),
        ('PROCESSING', '생성중'),
        ('COMPLETED', '완료'),
        ('FAILED', '실패'),
    ]

    # Phase 1은 비회원도 가능하므로 null=True 허용
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="요청자")
    
    # 목소리 옵션 연결 (목소리 정보가 바뀌어도 기록은 남아야 하므로 PROTECT 추천)
    voice = models.ForeignKey(Voice, on_delete=models.PROTECT, verbose_name="선택 목소리")
    
    text = models.TextField(verbose_name="입력 텍스트") # 500자 제한은 프론트/뷰에서 처리
    speed = models.FloatField(default=1.0, verbose_name="속도") # 0.5 ~ 2.0
    
    # 파일 저장 (media/tts/ 폴더에 저장됨)
    audio_file = models.FileField(upload_to='tts/', null=True, blank=True, verbose_name="생성된 오디오 파일")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="진행 상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")

    def __str__(self):
        return f"{self.text[:20]}... ({self.status})"