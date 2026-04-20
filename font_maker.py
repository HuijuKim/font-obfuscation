import fontforge
import os
import time

class AntiLLM:
    def __init__(self, keyword="ASDFGHJKL"):
        self.keyword = keyword
        self.key_len = len(keyword)
        self.vig_base = 0xE000
        self.noise_ranges = list(range(0x2100, 0x214F)) + list(range(0x2190, 0x21FF))

    def get_font_path(self, font_name):
        # 1. 현재 작업 폴더 확인
        if os.path.exists(font_name):
            return os.path.abspath(font_name)
        
        # 2. 윈도우 기본 폰트 폴더 확인
        win_font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', font_name)
        if os.path.exists(win_font_path):
            return win_font_path
            
        return None

    def build_font(self, base_font_name="consola.ttf"):
        input_path = self.get_font_path(base_font_name)
        
        if not input_path:
            print(f"❌ 폰트 파일을 찾을 수 없습니다: {base_font_name}")
            print("💡 해결책: 콘솔라 폰트 파일을 현재 파이썬 파일과 같은 폴더에 복사해 두세요.")
            return False

        ts = time.strftime("%H%M")
        font_id = f"AntiLLM_{ts}"
        output_path = os.path.join(os.getcwd(), f"{font_id}.ttf")

        try:
            # 폰트 열기
            font = fontforge.open(input_path)
            font.encoding = "UnicodeFull"
            
            print(f"🛠️ {font_id} 빌드 시작... (Source: {input_path})")

            for code in range(32, 127):
                orig_width = font[code].width
                for i in range(self.key_len):
                    fake_uni = self.vig_base + ((code - 32) * self.key_len) + i
                    font.selection.select(code)
                    font.copy()
                    font.selection.select(fake_uni)
                    font.paste()
                    font[fake_uni].width = orig_width

            # 노이즈 대역 처리
            for uni in self.noise_ranges:
                if uni not in font: font.createChar(uni)
                font.selection.select(32); font.copy()
                font.selection.select(uni); font.paste()
                font[uni].width = 0 

            font.fontname = font_id
            font.familyname = font_id
            font.fullname = font_id
            
            font.generate(output_path)
            print(f"✅ 생성 성공: {output_path}")
            return True
        except Exception as e:
            print(f"❌ 폰트 생성 에러: {e}")
            return False

if __name__ == "__main__":
    # 키워드는 반드시 ASDFGHJKL (9글자) 유지
    AntiLLM(keyword="ASDFGHJKL").build_font("consola.ttf")