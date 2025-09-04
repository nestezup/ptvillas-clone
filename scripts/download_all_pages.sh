#!/bin/bash

# pages 디렉터리 생성
mkdir -p pages

echo "모든 서브 페이지 다운로드 시작..."

# 각 URL에서 페이지 다운로드
while read url; do
    # URL에서 페이지 이름 추출
    page_name=$(basename "$url")
    echo "다운로드 중: $url -> pages/${page_name}.html"
    
    # HTML 다운로드
    curl -L -o "pages/${page_name}.html" "$url"
    
    echo "✓ ${page_name}.html 다운로드 완료"
    
done < all_urls.txt

echo "모든 페이지 다운로드 완료!"
echo "다운로드된 페이지들:"
ls -la pages/