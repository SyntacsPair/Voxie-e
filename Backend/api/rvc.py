import os
import torch
from rvc_python.infer import RVCInference

# 🚨 [필수] PyTorch 보안 정책 우회
original_torch_load = torch.load
def safe_torch_load(*args, **kwargs):
    kwargs.pop('weights_only', None)
    return original_torch_load(*args, weights_only=False, **kwargs)
torch.load = safe_torch_load

def convert_voice_with_rvc(input_path, output_path, model_name, pitch_adjust=0):
    """
    input_path: Edge TTS 뼈대 파일 (base_mp3)
    output_path: 최종 결과물 파일 (final_wav)
    model_name: 프론트에서 넘어온 voice 파라미터 (예: "Trump")
    """
    # 1. 현재 파일(rvc.py)의 위치 (api 폴더)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. 한 칸 상위 폴더로 이동 (Backend 폴더)
    parent_dir = os.path.dirname(current_dir)
    
    # 3. 거기서 Voice 폴더를 찾기!
    model_path = os.path.join(parent_dir, "Voice", f"{model_name}.pth")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Voice 폴더에 '{model_name}.pth' 파일이 없습니다!")

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    rvc = RVCInference(device=device)
    
    rvc.load_model(model_path)
    try:
        rvc.set_params(f0up_key=pitch_adjust, f0method="rmvpe")
    except Exception:
        pass 

    rvc.infer_file(input_path, output_path)
    return output_path