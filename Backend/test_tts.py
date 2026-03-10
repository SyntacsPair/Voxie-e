import asyncio
import edge_tts
import torch
import tempfile
import os
from rvc_python.infer import RVCInference

# 🚨 [필수] PyTorch 2.6 보안 정책 우회
original_torch_load = torch.load
def safe_torch_load(*args, **kwargs):
    kwargs.pop('weights_only', None)
    return original_torch_load(*args, weights_only=False, **kwargs)
torch.load = safe_torch_load

# ==========================================
# ⚙️ 설정(Settings)
# ==========================================
TEXT = "고무고무~~총난타!!!"
VOICE = "ko-KR-SunHiNeural"
FINAL_AUDIO = "final_output.wav"    
MODEL_PATH = r"D:\Voxie-e\Backend\Voice\Luffy.pth"
# ==========================================

async def main():
    # 1. 윈도우/리눅스 어디서든 안전한 OS 임시 폴더에 파일 이름표만 미리 발급받습니다.
    # (프로젝트 폴더에는 아무것도 생기지 않습니다!)
    temp_fd, temp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(temp_fd) # 점유 락 해제

    try:
        print(f"\n⏳ [1/2] 뼈대 생성 중... (보이지 않는 임시 캐시 사용)")
        communicate = edge_tts.Communicate(TEXT, VOICE)
        await communicate.save(temp_path) # 👈 임시 경로에 저장
        
        print(f"\n⏳ [2/2] RVC 목소리 변조 시작... (모델: 루피)")
        rvc = RVCInference(device="cuda:0") 
        
        print("🧠 모델 장착 중...")
        rvc.load_model(MODEL_PATH)
        
        print("⚙️ 파라미터 세팅 중...")
        try:
            # 🚨 원본(여) -> 변조(남) 이므로 피치를 -12(한 옥타브) 깎아야 자연스럽습니다!
            rvc.set_params(f0up_key=-3, f0method="rmvpe")
        except Exception:
            pass 
            
        print("🎤 임시 파일을 읽어 음성 덮어씌우는 중...")
        rvc.infer_file(temp_path, FINAL_AUDIO) # 👈 임시 파일을 읽어서 최종 결과물 생성
        print(f"\n🎉 대성공! 우리 폴더에는 오직 '{FINAL_AUDIO}'만 깔끔하게 떨어졌습니다!")

    except Exception as e:
        print(f"\n❌ 작업 중 에러가 발생했습니다: {e}")
        
    finally:
        # 🚨 [핵심] 성공하든 중간에 에러가 나서 터지든, 이 finally 블록이 무조건 실행되어 임시 파일을 영원히 삭제합니다.
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())