import asyncio
import edge_tts

# (테스트용)
TEXT = """
드디어 지옥 같던 5일간의 도커 에러에서 벗어났다.
이제부터는 쾌적하고 깔끔한 내 컴퓨터에서, 
내가 원하는 목소리로 소설을 들을 것이다.
"""

# 기본 목소리 (한국어 여성 '선희')
VOICE = "ko-KR-SunHiNeural"
OUTPUT_FILE = "base_tts.mp3"

async def main():
    print("⏳ 기본 TTS(뼈대)를 생성하는 중입니다...")
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print(f"🎉 뼈대 완성! '{OUTPUT_FILE}' 파일이 만들어졌습니다.")

if __name__ == "__main__":
    asyncio.run(main())