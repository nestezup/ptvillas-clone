#!/bin/bash

# 이미지 다운로드
echo "이미지 다운로드 중..."
grep -o 'src="[^"]*"' hill_the-hill.html | sed 's/src="//g' | sed 's/"//g' | grep -E '\.(png|jpg|jpeg|gif|svg|webp)' | while read url; do
    if [[ $url == http* ]]; then
        filename=$(basename "$url" | cut -d'?' -f1)
        echo "다운로드 중: $url -> assets/images/$filename"
        curl -L -o "assets/images/$filename" "$url"
    fi
done

# CSS 배경 이미지 다운로드
echo "CSS 배경 이미지 다운로드 중..."
grep -o 'background-image:url([^)]*)' hill_the-hill.html | sed 's/background-image:url(//g' | sed 's/)//g' | sed 's/[\"'\'']//g' | while read url; do
    if [[ $url == http* ]]; then
        filename=$(basename "$url" | cut -d'?' -f1)
        echo "다운로드 중: $url -> assets/images/$filename"
        curl -L -o "assets/images/$filename" "$url"
    fi
done

# CSS 파일 다운로드
echo "CSS 파일 다운로드 중..."
grep -o 'href="[^"]*\.css[^"]*"' hill_the-hill.html | sed 's/href="//g' | sed 's/"//g' | while read url; do
    if [[ $url == http* ]]; then
        filename=$(basename "$url" | cut -d'?' -f1)
        echo "다운로드 중: $url -> assets/css/$filename"
        curl -L -o "assets/css/$filename" "$url"
    fi
done

# JS 파일 다운로드
echo "JS 파일 다운로드 중..."
grep -o 'src="[^"]*\.js[^"]*"' hill_the-hill.html | sed 's/src="//g' | sed 's/"//g' | while read url; do
    if [[ $url == http* ]]; then
        filename=$(basename "$url" | cut -d'?' -f1)
        echo "다운로드 중: $url -> assets/js/$filename"
        curl -L -o "assets/js/$filename" "$url"
    fi
done

echo "모든 리소스 다운로드 완료!"