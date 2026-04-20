import fontforge
import os
import time
import random

class AntiLLM:
    def __init__(self, keyword="ASDFGHJKL"):
        self.keyword = keyword
        self.key_len = len(keyword)
        self.vig_base = 0xE000
        # 노이즈 대역 (기호 대역을 활용하여 데이터 오염 극대화)
        self.noise_ranges = list(range(0x2100, 0x214F)) + list(range(0x2190, 0x21FF))
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_file = "AntiLLM.ttf"

    def build_font(self, base_font_name="base_font.ttf"):
        input_path = os.path.join(self.current_dir, base_font_name)
        output_path = os.path.join(self.current_dir, self.font_file)

        if not os.path.exists(input_path):
            print(f"❌ 원본 폰트 없음: {input_path}")
            return False

        try:
            font = fontforge.open(input_path)
            
            # 1. 비즈네르 암호화 글리프 생성 (0xE000 대역)
            for code in range(32, 127):
                for i in range(self.key_len):
                    fake_uni = self.vig_base + ((code - 32) * self.key_len) + i
                    font.selection.select(code)
                    font.copy()
                    font.selection.select(fake_uni)
                    font.paste()

            # 2. 노이즈 대역 "완전 투명화" (핵심 수정 부분)
            print(f"{len(self.noise_ranges)}개의 노이즈를 유령 문자로 변환 중...")
            for uni in self.noise_ranges:
                # 공백(32)의 모양을 복사하여 기존 기호 모양을 지워버림
                font.selection.select(32)
                font.copy()
                if uni not in font:
                    font.createChar(uni)
                font.selection.select(uni)
                font.paste()
                
                # 너비와 여백을 0으로 만들어 시각적으로 제거
                font[uni].width = 0
                font[uni].left_side_bearing = 0
                font[uni].right_side_bearing = 0
                
                font[uni].vwidth = 0

            # 3. 메타데이터 설정 및 저장
            ts = int(time.time() % 100)
            font_name = f"AntiLLM_V4_{ts}"
            font.fontname = font.familyname = font.fullname = font_name
            font.generate(output_path)
            
            print(f"폰트 생성 완료: {output_path}")
            return font_name
        except Exception as e:
            print(f"에러: {e}")
            return False

    def encrypt(self, text):
        res = []
        for idx, c in enumerate(text):
            code = ord(c)
            if code in [10, 13]:
                res.append(c)
            elif 32 <= code <= 126:
                i = idx % self.key_len
                res.append(chr(self.vig_base + ((code - 32) * self.key_len) + i))
                # 랜덤 노이즈 1~3개 삽입
                for _ in range(random.randint(1, 3)):
                    res.append(chr(random.choice(self.noise_ranges)))
            else:
                res.append(c)
        return "".join(res)

    def decrypt(self, encrypted_text):
        noise_set = set(chr(n) for n in self.noise_ranges)
        filtered = [c for c in encrypted_text if c not in noise_set]
        res = []
        
        actual_idx = 0  # 수동 인덱스 도입
        for c in filtered:
            code = ord(c)
            if self.vig_base <= code < self.vig_base + (95 * self.key_len):
                i = actual_idx % self.key_len # 암호문일 때만 순서 계산
                original_ascii = (code - self.vig_base - i) // self.key_len + 32
                res.append(chr(int(original_ascii)))
                actual_idx += 1
            else:
                res.append(c)
        return "".join(res)

if __name__ == "__main__":
    system = AntiLLM(keyword="ASDFGHJKL")
    f_name = system.build_font("base_font.ttf")
    
    if f_name:
        original = 'print("Perfect Stealth Mode")'
        encrypted = system.encrypt(original)
        print(f"\n폰트 이름: {f_name}")
        print(f"\n[암호화 텍스트]\n{encrypted}")
        print(f"\n[복호화 검증] {'성공' if original == system.decrypt(encrypted) else '❌ 실패'}")