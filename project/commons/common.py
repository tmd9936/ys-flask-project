import random
from string import digits, ascii_lowercase, ascii_uppercase
from .consts import ALLOWED_EXTENSIONS
import re # 정규식
import os # 시스템 명령 사용하기 위해서


# 파일이 유효한지 체크하는 함수
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

# 파일명을 random하게 생성해주는 함수
def rand_generator(length=8):
    char = ascii_lowercase + ascii_uppercase + digits
    return "".join(random.sample(char, length))


# 첨부파일을 적용할 때 secure_filename()의 함수를 사용해야 함.
# 그런데, 이함수는 파일명을 ascii로만 사용하기 때문에 한글파일은
# 사용상 문제가 된다. 따라서, 한글을 사용하기 위한 함수를 정의함.
def check_filename(filename):
    reg = re.compile("[^a-zA-Z0-9_.가-힣-]")
    for s in os.path.sep, os.path.altsep:
        if s:
            filename = filename.replace(s, '')
            # reg.sub('', '_'.join(filename.split()))는
            # [A-Za-z0-9_.가-힝-]을 제외한 문자가 있으면 공백으로 처리하라는 의미
            filename = str(reg.sub('', '_'.join(filename.split()))).strip("._")
        return filename