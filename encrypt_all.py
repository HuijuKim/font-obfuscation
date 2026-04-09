import os
import random

class AntiLLMTool:
    def __init__(self, keyword="ASDFGHJKL"):
        self.keyword = keyword
        self.key_len = len(keyword)
        self.vig_base = 0xE000
        self.noise_ranges = list(range(0x2100, 0x214F)) + list(range(0x2190, 0x21FF))
        self.noise_set = set(chr(n) for n in self.noise_ranges)

    def encrypt(self, text):
        """원본 텍스트 -> 노이즈가 섞인 비즈네르 암호문"""
        res = []
        for idx, c in enumerate(text):
            code = ord(c)
            if code in [10, 13]:
                res.append(c)
            elif 32 <= code <= 126:
                i = idx % self.key_len
                res.append(chr(self.vig_base + ((code - 32) * self.key_len) + i))
                for _ in range(random.randint(1, 3)):
                    res.append(chr(random.choice(self.noise_ranges)))
            else:
                res.append(c)
        return "".join(res)

tool = AntiLLMTool(keyword="ASDFGHJKL")
current_dir = os.getcwd()

# 암호화할 파일 목록
files_to_encrypt = []

# problem*.md와 problem*.ml 파일들
for i in range(1, 16):
    files_to_encrypt.append(f"problem{i}.md")
    files_to_encrypt.append(f"problem{i}.ml")

# hw1.md도 포함
files_to_encrypt.append("hw1.md")

# 각 파일 암호화
for filename in files_to_encrypt:
    filepath = os.path.join(current_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encrypted_content = tool.encrypt(content)
        
        base_name = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]
        new_filename = f"{base_name}_enc{ext}"
        new_filepath = os.path.join(current_dir, new_filename)
        
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)
        
        print(f"✓ {filename} -> {new_filename}")
    else:
        print(f"✗ {filename} not found")

print(f"\n총 {len(files_to_encrypt)}개 파일 암호화 완료!")
