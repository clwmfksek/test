# 마니또 추첨 프로그램

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## 소개

이 프로그램은 사용자 목록에서 랜덤으로 마니또 쌍을 생성하고, 암호화하여 관리할 수 있는 파이썬 기반 응용 프로그램입니다.

## 주요 기능

- **마니또 쌍 자동 생성**: Fisher-Yates 알고리즘을 사용한 공정한 무작위 배정
- **암호화 저장**: 비밀번호로 보호된 안전한 정보 저장 (Fernet 대칭 암호화 방식)
- **관리자 모드**: 전체 마니또 목록 확인 기능
- **개인 확인 모드**: 자신의 마니또 대상만 확인 가능

## 사용 방법

1. 프로그램 실행:
   ```bash
   python sp.py
   ```

2. 메뉴 선택:
   - `1`: 마니또 추첨하기 (새로 생성)
   - `2`: 마니또 목록 확인하기 (관리자용)
   - `3`: 개인별 마니또 확인하기
   - `4`: 종료

## 기술 스택

- **Python 3.6+**
- **cryptography**: 암호화 및 복호화
- **JSON**: 데이터 직렬화

## 시스템 요구사항

- Python 3.6 이상
- 필수 라이브러리: cryptography

## 설치 방법

1. 필요한 라이브러리 설치:
   ```bash
   pip install cryptography
   ```

2. 프로그램 다운로드:
   ```bash
   git clone https://github.com/clwmfksek/test.git
   cd test
   ```

## 보안 특징

- PBKDF2 키 생성을 통한 안전한 비밀번호 기반 암호화
- 암호화된 파일 형식으로 정보 보호
- 개인정보 보호를 위한 접근 제한

## 라이센스

MIT 라이센스에 따라 배포됩니다.

## 제작자

신효환