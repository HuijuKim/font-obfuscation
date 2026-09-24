import fontforge
import os
import sys
import time

from endec import AntiLLMTool

# 사용법: ffpython build_font.py <원본 폰트.ttf> [출력 폰트.ttf]
# 키 길이, PUA 시작점, 노이즈 대역은 endec.py의 AntiLLMTool과 같은 값을 써야 한다.

def build_font(input_path, output_path, tool):
    if not os.path.exists(input_path):
        print(f"❌ 원본 폰트 없음: {input_path}")
        return False

    try:
        font = fontforge.open(input_path)

        # 1. 비즈네르 암호화 글리프 생성 (0xE000 대역)
        for code in range(32, 127):
            for i in range(tool.key_len):
                fake_uni = tool.vig_base + ((code - 32) * tool.key_len) + i
                font.selection.select(code)
                font.copy()
                font.selection.select(fake_uni)
                font.paste()

        # 2. 노이즈 대역 "완전 투명화"
        print(f"{len(tool.noise_ranges)}개의 노이즈를 유령 문자로 변환 중...")
        for uni in tool.noise_ranges:
            # 공백(32)의 모양을 복사하여 기존 기호 모양을 지워버림
            font.selection.select(32)
            font.copy()
            if uni not in font:
                font.createChar(uni)
            font.selection.select(uni)
            font.paste()

            # 너비와 여백을 없애 시각적으로 제거
            font[uni].left_side_bearing = 0
            font[uni].right_side_bearing = 0
            font[uni].vwidth = 0
            # 너비는 0이 아니라 1(1/2048 em)로 둔다. 고정폭 폰트(Consolas 등)에 폭 0 글리프가 있으면
            # FontForge가 TTF로 내보낼 때 모든 글리프 폭을 고정폭 값으로 덮어써서 노이즈가 공백으로 보인다.
            font[uni].width = 1

        # 3. 메타데이터 설정 및 저장 (중복 방지용 타임스탬프)
        ts = int(time.time() % 100)
        font_name = f"AntiLLM_V4_{ts}"
        font.fontname = font.familyname = font.fullname = font_name
        font.generate(output_path)

        print(f"폰트 생성 완료: {output_path} (폰트 이름: {font_name})")
        return font_name
    except Exception as e:
        print(f"에러: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: ffpython build_font.py <원본 폰트.ttf> [출력 폰트.ttf]")
        sys.exit(1)
    output = sys.argv[2] if len(sys.argv) > 2 else "AntiLLM.ttf"
    # FontForge는 한글 등이 섞인 상대 경로를 열지 못하므로 절대 경로로 넘긴다
    build_font(os.path.abspath(sys.argv[1]), os.path.abspath(output), AntiLLMTool(keyword="ASDFGHJKL"))
