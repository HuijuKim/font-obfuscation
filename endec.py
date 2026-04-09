import random

class AntiLLMTool:
    def __init__(self, keyword="ASDFGHJKL"):
        self.keyword = keyword
        self.key_len = len(keyword)
        self.vig_base = 0xE000
        # 폰트 빌드 시 설정했던 노이즈 대역과 반드시 일치해야 합니다.
        self.noise_ranges = list(range(0x2100, 0x214F)) + list(range(0x2190, 0x21FF))
        self.noise_set = set(chr(n) for n in self.noise_ranges)

    def encrypt(self, text):
        """원본 텍스트 -> 노이즈가 섞인 비즈네르 암호문"""
        res = []
        for idx, c in enumerate(text):
            code = ord(c)
            if code in [10, 13]: # 줄바꿈 보존
                res.append(c)
            elif 32 <= code <= 126:
                # 1. 비즈네르 암호화 적용
                i = idx % self.key_len
                res.append(chr(self.vig_base + ((code - 32) * self.key_len) + i))
                
                # 2. 랜덤 노이즈 삽입 (1~3개)
                for _ in range(random.randint(1, 3)):
                    res.append(chr(random.choice(self.noise_ranges)))
            else:
                res.append(c)
        return "".join(res)

    def decrypt(self, encrypted_text):
        """암호문 -> 노이즈 제거 후 원본 텍스트 복구"""
        # 1. 노이즈 대역에 포함된 모든 유령 문자 제거
        filtered = [c for c in encrypted_text if c not in self.noise_set]
        
        res = []
        for idx, c in enumerate(filtered):
            code = ord(c)
            # 암호화 대역 내 문자만 역산 수행
            if self.vig_base <= code < self.vig_base + (95 * self.key_len):
                i = idx % self.key_len
                original_ascii = (code - self.vig_base - i) // self.key_len + 32
                res.append(chr(original_ascii))
            else:
                res.append(c)
        return "".join(res)

# --- 실전 사용 예시 ---
if __name__ == "__main__":
    tool = AntiLLMTool(keyword="ASDFGHJKL")

    print("--- Anti-LLM 실전 변환기 모드 ---")
    print("1: 암호화 (Encrypt)")
    print("2: 복호화 (Decrypt)")
    choice = input("선택하세요: ")

    if choice == "1":
        print("\n암호화할 텍스트를 입력하세요 (입력 종료 후 Ctrl+Z(Windows) 또는 Ctrl+D(Unix) 입력):")
        import sys
        input_text = sys.stdin.read()
        if input_text.strip():
            result = tool.encrypt(input_text)
            print("\n[암호화 완료 - 아래 텍스트를 복사하세요]")
            print("-" * 40)
            print(result)
            print("-" * 40)
            
    elif choice == "2":
        print("\n복호화할 암호문을 붙여넣으세요 (입력 종료 후 Ctrl+Z 또는 Ctrl+D):")
        import sys
        input_text = sys.stdin.read()
        if input_text.strip():
            result = tool.decrypt(input_text)
            print("\n[복호화 완료 - 원본 코드]")
            print("-" * 40)
            print(result)
            print("-" * 40)