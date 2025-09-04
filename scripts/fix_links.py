#!/usr/bin/env python3
import re
import os

# HTML 파일 읽기
with open('hill_the-hill.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 이미지 src 변경 함수들
def replace_image_src(match):
    url = match.group(0).split('"')[1]
    filename = os.path.basename(url).split('?')[0]
    return f'src="assets/images/{filename}"'

def replace_leadconnector_src(match):
    url = match.group(0).split('"')[1]
    if 'u_https://assets.cdn.filesafe.space' in url:
        filename = url.split('/')[-1].split('?')[0]
        return f'src="assets/images/{filename}"'
    elif 'u_https://firebasestorage.googleapis.com' in url:
        filename = url.split('/')[-1].split('?')[0]
        return f'src="assets/images/{filename}"'
    else:
        filename = os.path.basename(url).split('?')[0]
        return f'src="assets/images/{filename}"'

def replace_background_image(match):
    url = match.group(0)
    if 'flags.png' in url:
        return 'background-image: url("assets/images/flags.png")'
    elif 'flags@2x.png' in url:
        return 'background-image: url("assets/images/flags@2x.png")'
    else:
        # URL에서 파일명 추출
        url_part = url.split('(')[1].split(')')[0].strip('"\'')
        filename = os.path.basename(url_part).split('?')[0]
        return f'background-image: url("assets/images/{filename}")'

def replace_css_href(match):
    url = match.group(0).split('"')[1]
    filename = os.path.basename(url).split('?')[0]
    return f'href="assets/css/{filename}"'

def replace_js_src(match):
    url = match.group(0).split('"')[1]
    filename = os.path.basename(url).split('?')[0]
    return f'src="assets/js/{filename}"'

# 패턴들을 순차적으로 적용
# 일반 이미지 src
content = re.sub(r'src="https://[^"]*\.(?:png|jpg|jpeg|gif|svg|webp)[^"]*"', replace_image_src, content)

# leadconnectorhq 이미지들 (복잡한 URL)
content = re.sub(r'src="https://images\.leadconnectorhq\.com/[^"]*"', replace_leadconnector_src, content)

# CSS background-image
content = re.sub(r'background-image:\s*url\(["\']?https://[^)]*["\']?\)', replace_background_image, content)

# CSS 파일
content = re.sub(r'href="https://[^"]*\.css[^"]*"', replace_css_href, content)

# JS 파일
content = re.sub(r'src="https://[^"]*\.js[^"]*"', replace_js_src, content)

# 특별한 경우들 직접 처리
content = re.sub(r'src="https://images\.leadconnectorhq\.com/[^"]*u_https://assets\.cdn\.filesafe\.space/[^/]*/media/([^"/?]*)[^"]*"', 
                r'src="assets/images/\1"', content)

content = re.sub(r'src="https://images\.leadconnectorhq\.com/[^"]*u_https://firebasestorage\.googleapis\.com/[^"]*/(map-[^"/?]*\.jpg)[^"]*"', 
                r'src="assets/images/\1"', content)

# 수정된 HTML 파일 저장
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML 파일이 index.html로 저장되었습니다. 모든 링크가 로컬 경로로 변경되었습니다.")