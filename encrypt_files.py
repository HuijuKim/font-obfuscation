import os
import sys

from endec import ObfuscationTool

# 사용법: python encrypt_files.py 파일1 [파일2 ...]
# 각 파일의 암호화본을 같은 폴더에 "이름_enc.확장자"로 저장한다.

tool = ObfuscationTool(keyword="ASDFGHJKL")

if len(sys.argv) < 2:
    print("사용법: python encrypt_files.py 파일1 [파일2 ...]")
    sys.exit(1)

for filepath in sys.argv[1:]:
    if not os.path.exists(filepath):
        print(f"✗ {filepath} not found")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    base_name, ext = os.path.splitext(filepath)
    new_filepath = f"{base_name}_enc{ext}"

    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(tool.encrypt(content))

    print(f"✓ {filepath} -> {new_filepath}")
