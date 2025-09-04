#!/bin/bash

echo "모든 페이지의 리소스 다운로드 시작..."

# 각 페이지 파일에서 리소스 추출 및 다운로드
for html_file in pages/*.html; do
    echo "처리 중: $html_file"
    
    # 이미지 다운로드
    echo "  - 이미지 다운로드 중..."
    grep -o 'src="[^"]*"' "$html_file" | sed 's/src="//g' | sed 's/"//g' | grep -E '\.(png|jpg|jpeg|gif|svg|webp)' | while read url; do
        if [[ $url == http* ]]; then
            filename=$(basename "$url" | cut -d'?' -f1)
            if [ ! -f "assets/images/$filename" ]; then
                echo "    다운로드: $url -> assets/images/$filename"
                curl -L -o "assets/images/$filename" "$url"
            fi
        fi
    done

    # leadconnectorhq 이미지들 다운로드
    grep -o 'src="https://images\.leadconnectorhq\.com/[^"]*"' "$html_file" | sed 's/src="//g' | sed 's/"//g' | while read url; do
        if [[ $url == *"u_https://assets.cdn.filesafe.space"* ]]; then
            filename=$(echo "$url" | sed 's/.*\/media\///g' | cut -d'?' -f1)
        elif [[ $url == *"u_https://firebasestorage.googleapis.com"* ]]; then
            filename=$(basename "$url" | cut -d'?' -f1)
        else
            filename=$(basename "$url" | cut -d'?' -f1)
        fi
        
        if [ ! -f "assets/images/$filename" ]; then
            echo "    다운로드: $url -> assets/images/$filename"
            curl -L -o "assets/images/$filename" "$url"
        fi
    done

    # CSS 배경 이미지 다운로드
    echo "  - CSS 배경 이미지 다운로드 중..."
    grep -o 'background-image:url([^)]*)' "$html_file" | sed 's/background-image:url(//g' | sed 's/)//g' | sed 's/[\"'\'']//g' | while read url; do
        if [[ $url == http* ]]; then
            filename=$(basename "$url" | cut -d'?' -f1)
            if [ ! -f "assets/images/$filename" ]; then
                echo "    다운로드: $url -> assets/images/$filename"
                curl -L -o "assets/images/$filename" "$url"
            fi
        fi
    done

    # CSS 파일 다운로드
    echo "  - CSS 파일 다운로드 중..."
    grep -o 'href="[^"]*\.css[^"]*"' "$html_file" | sed 's/href="//g' | sed 's/"//g' | while read url; do
        if [[ $url == http* ]]; then
            filename=$(basename "$url" | cut -d'?' -f1)
            if [ ! -f "assets/css/$filename" ]; then
                echo "    다운로드: $url -> assets/css/$filename"
                curl -L -o "assets/css/$filename" "$url"
            fi
        fi
    done

    # JS 파일 다운로드
    echo "  - JS 파일 다운로드 중..."
    grep -o 'src="[^"]*\.js[^"]*"' "$html_file" | sed 's/src="//g' | sed 's/"//g' | while read url; do
        if [[ $url == http* ]]; then
            filename=$(basename "$url" | cut -d'?' -f1)
            if [ ! -f "assets/js/$filename" ]; then
                echo "    다운로드: $url -> assets/js/$filename"
                curl -L -o "assets/js/$filename" "$url"
            fi
        fi
    done

    echo "  ✓ $html_file 리소스 처리 완료"
done

echo "모든 리소스 다운로드 완료!"
echo "최종 통계:"
echo "  이미지: $(ls assets/images/ | wc -l) 개"
echo "  CSS: $(ls assets/css/ | wc -l) 개"
echo "  JS: $(ls assets/js/ | wc -l) 개"