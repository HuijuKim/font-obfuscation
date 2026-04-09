import fontforge
import os
import time

def generate_vigenere_pua(base_font_path, keyword):
    if not os.path.exists(base_font_path): return
    font = fontforge.open(base_font_path)
    
    # 0xE000: Private Use Area (가장 안전한 대역)
    base_addr = 0xE000 
    key_len = len(keyword)
    
    print(f"--- [비즈네르 PUA] 폰트 생성 시작 (키: {keyword}) ---")

    # ASCII 32(Space)부터 126(~)까지 모두 매핑
    for code in range(32, 127):
        for i in range(key_len):
            try:
                # 공식: 베이스 + (문자오프셋 * 키길이) + 현재 순서(i)
                fake_unicode = base_addr + ((code - 32) * key_len) + i
                
                font.selection.select(code)
                font.copy()
                font.selection.select(fake_unicode)
                font.paste()
                font[fake_unicode].glyphname = f"v_{code}_{i}"
            except:
                continue

    new_name = f"AntiLLM_Vig_Final_K{int(time.time()%100)}"
    font.fontname = font.familyname = font.fullname = new_name
    font.appendSFNTName('English (US)', 1, new_name)
    font.appendSFNTName('English (US)', 4, new_name)

    font.generate(os.path.join(os.path.dirname(base_font_path), "Vigenere_Final.ttf"))
    return new_name, base_addr, key_len

def encrypt_vigenere_final(text, base, key_len):
    res = []
    # 모든 문자(공백 포함)에 대해 인덱스를 엄격하게 적용
    for idx, c in enumerate(text):
        code = ord(c)
        if code in [10, 13]: # 개행만 보존
            res.append(c)
        elif 32 <= code <= 126:
            i = idx % key_len
            fake_code = base + ((code - 32) * key_len) + i
            res.append(chr(fake_code))
        else:
            res.append(c)
    return "".join(res)

if __name__ == "__main__":
    path = r"C:\path\to\base_font.ttf"
    kw = "ASDFGHJKL"
    name, b_addr, k_l = generate_vigenere_pua(path, kw)
    
    # 테스트 코드
    code_to_encrypt = 'print("Hello, Vigenere!")\nif True:\n    pass'
    print(f"\n[설치 폰트명: {name}]\n")
    print(encrypt_vigenere_final(code_to_encrypt, b_addr, k_l))