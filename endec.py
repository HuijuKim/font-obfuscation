import random
import sys

class AntiLLMTool:
    def __init__(self, keyword="ASDFGHJKL"):
        self.keyword = keyword
        self.key_len = len(keyword)
        self.vig_base = 0xE000
        self.noise_ranges = list(range(0x2100, 0x214F)) + list(range(0x2190, 0x21FF))
        self.noise_set = set(chr(n) for n in self.noise_ranges)

    def encrypt(self, text):
        res = []
        actual_idx = 0 
        for c in text:
            code = ord(c)
            if 32 <= code <= 126:
                i = actual_idx % self.key_len
                res.append(chr(self.vig_base + ((code - 32) * self.key_len) + i))
                for _ in range(random.randint(1, 3)):
                    res.append(chr(random.choice(self.noise_ranges)))
                actual_idx += 1
            else:
                res.append(c)
        return "".join(res)

    def decrypt(self, encrypted_text):
        filtered = [c for c in encrypted_text if c not in self.noise_set]
        res = []
        for c in filtered:
            code = ord(c)
            if self.vig_base <= code < self.vig_base + (95 * self.key_len):
                # 키 순번(0 ~ key_len-1)은 몫에 영향을 주지 않으므로 순번을 몰라도 복호화된다.
                # 순번을 세는 방식이 암호화 쪽과 다르면 글자가 한 칸씩 밀리던 문제를 없앤다.
                original_ascii = (code - self.vig_base) // self.key_len + 32
                res.append(chr(original_ascii))
            else:
                res.append(c)
        return "".join(res)

if __name__ == "__main__":
    tool = AntiLLMTool(keyword="ASDFGHJKL")
    print("1: 암호화 / 2: 복호화")
    choice = input("선택: ")
    if choice in ["1", "2"]:
        print("텍스트 입력 후 Ctrl+Z(Win) 또는 Ctrl+D(Mac) 입력:")
        data = sys.stdin.read()
        if choice == "1":
            print("\n[암호화 결과]\n" + tool.encrypt(data))
        else:
            print("\n[복호화 결과]\n" + tool.decrypt(data))