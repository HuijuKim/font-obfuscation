import fontforge
import os
import time

# 1. 전범위 암호화 폰트 생성 함수
def generate_anti_llm_font(base_font_path, student_key):
    if not os.path.exists(base_font_path):
        print(f"에러: '{base_font_path}' 파일이 없습니다.")
        return None, None

    font = fontforge.open(base_font_path)
    # 안전한 유니코드 대역 (0x0500: 아르메니아 문자 근처)
    encryption_base = 0x0500 

    print(f"--- 폰트 생성 시작 (Key: {student_key}) ---")

    # ASCII 33(!)부터 126(~)까지 출력 가능 문자만 치환
    # 공백(32), 탭(9), 개행(10, 13)은 건드리지 않음
    for code in range(33, 127):
        try:
            fake_unicode = encryption_base + code + student_key
            
            # 모양 복사 및 이식
            font.selection.select(code)
            font.copy()
            font.selection.select(fake_unicode)
            font.paste()
            
            font[fake_unicode].glyphname = f"enc_{code}"
        except Exception:
            continue

    # 폰트 메타데이터 설정 (중복 방지용 타임스탬프)
    ts = int(time.time()) % 1000
    font_family = f"AntiLLM_K{student_key}_T{ts}"
    
    font.fontname = font_family
    font.familyname = font_family
    font.fullname = font_family
    font.appendSFNTName('English (US)', 1, font_family)
    font.appendSFNTName('English (US)', 4, font_family)

    output_path = os.path.join(os.path.dirname(base_font_path), "Student_A_Font.ttf")
    font.generate(output_path)
    
    print(f"--- 폰트 생성 완료: {font_family} ---")
    return font_family, encryption_base + student_key

# 2. 소스코드 텍스트 변환 함수 (개행/공백 보존)
def encrypt_text(source_text, offset):
    encrypted_chars = []
    for c in source_text:
        code = ord(c)
        # 공백, 탭, 개행 문자는 변환 없이 그대로 유지
        if code in [9, 10, 13, 32]:
            encrypted_chars.append(c)
        # 일반 출력 문자만 오프셋 적용
        elif 33 <= code <= 126:
            encrypted_chars.append(chr(code + offset))
        else:
            encrypted_chars.append(c)
    return "".join(encrypted_chars)

# --- 메인 실행부 ---
if __name__ == "__main__":
    # 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_font = os.path.join(current_dir, "base_font.ttf")
    
    # 1. 폰트 생성
    student_key = 14
    font_name, final_offset = generate_anti_llm_font(input_font, student_key)

    if font_name:
        # 2. 테스트용 코드 변환
        sample_code = """def hello_world():
    print("Anti-LLM System Activated!")
    if True:
        return 12345"""

        encrypted_result = encrypt_text(sample_code, final_offset)
        
        print("\n" + "="*50)
        print(f"1. 폰트 설치: Student_A_Font.ttf를 설치하세요.")
        print(f"2. 에디터 설정: 폰트를 '{font_name}'으로 변경하세요.")
        print(f"3. 아래 암호문을 복사해서 메모장에 붙여넣으세요.")
        print("="*50 + "\n")
        print(encrypted_result)
        print("\n" + "="*50)