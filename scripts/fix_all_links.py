#!/usr/bin/env python3
import re
import os
import glob

def fix_links_in_file(file_path, output_path):
    """개별 HTML 파일의 링크를 로컬 경로로 수정"""
    print(f"처리 중: {file_path} -> {output_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미지 src 변경 함수들
    def replace_image_src(match):
        url = match.group(0).split('"')[1]
        filename = os.path.basename(url).split('?')[0]
        return f'src="../assets/images/{filename}"'

    def replace_leadconnector_src(match):
        url = match.group(0).split('"')[1]
        if 'u_https://assets.cdn.filesafe.space' in url:
            filename = url.split('/')[-1].split('?')[0]
            return f'src="../assets/images/{filename}"'
        elif 'u_https://firebasestorage.googleapis.com' in url:
            filename = url.split('/')[-1].split('?')[0]
            return f'src="../assets/images/{filename}"'
        else:
            filename = os.path.basename(url).split('?')[0]
            return f'src="../assets/images/{filename}"'

    def replace_background_image(match):
        url = match.group(0)
        if 'flags.png' in url:
            return 'background-image: url("../assets/images/flags.png")'
        elif 'flags@2x.png' in url:
            return 'background-image: url("../assets/images/flags@2x.png")'
        else:
            url_part = url.split('(')[1].split(')')[0].strip('"\'')
            filename = os.path.basename(url_part).split('?')[0]
            return f'background-image: url("../assets/images/{filename}")'

    def replace_css_href(match):
        url = match.group(0).split('"')[1]
        filename = os.path.basename(url).split('?')[0]
        return f'href="../assets/css/{filename}"'

    def replace_js_src(match):
        url = match.group(0).split('"')[1]
        filename = os.path.basename(url).split('?')[0]
        return f'src="../assets/js/{filename}"'

    def replace_internal_link(match):
        """내부 페이지 링크를 로컬 경로로 변경"""
        url = match.group(0).split('"')[1]
        page_name = os.path.basename(url)
        return f'href="{page_name}.html"'

    # 패턴들을 순차적으로 적용
    # 내부 페이지 링크 (ptvillas.co.kr 도메인)
    content = re.sub(r'href="https://ptvillas\.co\.kr/([^"]*)"', replace_internal_link, content)
    
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

    # 수정된 HTML 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {output_path} 저장 완료")

# 메인 페이지 수정 (이미 있는 index.html 사용)
print("=== 메인 페이지 수정 ===")
fix_links_in_file('hill_the-hill.html', 'index.html')

# 서브 페이지들 수정
print("\n=== 서브 페이지들 수정 ===")
for html_file in glob.glob('pages/*.html'):
    base_name = os.path.basename(html_file).replace('.html', '')
    output_file = f'{base_name}.html'
    
    # 메인 페이지와 중복되는 경우 건너뛰기
    if base_name == 'hill_the-hill':
        continue
        
    fix_links_in_file(html_file, output_file)

print(f"\n=== 작업 완료 ===")
print("생성된 파일들:")
html_files = glob.glob('*.html')
for html_file in sorted(html_files):
    size = os.path.getsize(html_file) // 1024
    print(f"  {html_file} ({size}KB)")

print(f"\n총 {len(html_files)}개 HTML 파일이 생성되었습니다.")
print("assets 폴더와 함께 전체 웹사이트가 로컬에서 동작합니다.")