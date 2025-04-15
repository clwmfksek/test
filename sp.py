import random
import json
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
from typing import List, Dict, Any, Tuple, Optional

# 상수 정의
FILE_PATH = 'manito_pairs.enc'
SALT = b'salt_123'  # 실제 운영 시에는 랜덤 salt 사용 권장

# 명단 데이터
names = [
    # 회장
    "신효환",
    
    # 부회장
    "성준영",
    
    # 학술부
    "손한솔", "권수현", "안재준", "이강민", "김영모", "강주영", "이은서",
    
    # 기획부
    "정연주", "김승현", "방지원", "유태규", "정율", "정민재", "강지원",
    
    # 총무부
    "강현진", "김수연", "한병헌", "박재관", "노혜륜",
    
    # 홈페이지관리부
    "윤진수", "김다인", "박선우", "박주영", "박준홍", "원종인", "장준혁",
    
    # 편집부
    "정민주", "김동원", "강성찬", "윤민재", "김승우"
]


def generate_key(password: str) -> bytes:
    """비밀번호로부터 암호화 키 생성"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def create_manito_pairs() -> List[Dict[str, str]]:
    """중복 없는 마니또 쌍 생성"""
    # 효율적인 마니또 쌍 생성 알고리즘
    shuffled_names = names.copy()
    
    # Fisher-Yates 셔플로 중복 없이 섞기
    random.shuffle(shuffled_names)
    
    # 자기 자신이 마니또가 되는 경우 처리
    for i in range(len(names)):
        if names[i] == shuffled_names[i]:
            # 다음 인덱스와 교환 (마지막 원소면 첫 원소와 교환)
            next_idx = (i + 1) % len(shuffled_names)
            shuffled_names[i], shuffled_names[next_idx] = shuffled_names[next_idx], shuffled_names[i]
    
    # 마니또 쌍 생성
    return [{"마니또": names[i], "대상": shuffled_names[i]} for i in range(len(names))]


def encrypt_data(data: Any, password: str) -> bytes:
    """데이터 암호화"""
    key = generate_key(password)
    f = Fernet(key)
    json_data = json.dumps(data, ensure_ascii=False).encode()
    return f.encrypt(json_data)


def decrypt_data(encrypted_data: bytes, password: str) -> Any:
    """데이터 복호화"""
    key = generate_key(password)
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())


def load_encrypted_file() -> Optional[bytes]:
    """암호화된 파일 로드"""
    try:
        if not os.path.exists(FILE_PATH):
            print(f"오류: {FILE_PATH} 파일이 존재하지 않습니다.")
            return None
        
        with open(FILE_PATH, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"파일 로드 중 오류 발생: {e}")
        return None


def encrypt_and_save_pairs(pairs: List[Dict[str, str]], password: str) -> bool:
    """마니또 쌍을 암호화하여 저장"""
    try:
        encrypted_data = encrypt_data(pairs, password)
        with open(FILE_PATH, 'wb') as file:
            file.write(encrypted_data)
        return True
    except Exception as e:
        print(f"암호화 및 저장 중 오류 발생: {e}")
        return False


def decrypt_and_show_pairs(password: str) -> None:
    """모든 마니또 쌍 보기(관리자용)"""
    encrypted_data = load_encrypted_file()
    if not encrypted_data:
        return
    
    try:
        pairs = decrypt_data(encrypted_data, password)
        print("\n=== 마니또 목록 ===")
        for pair in pairs:
            print(f"{pair['마니또']} -> {pair['대상']}")
    except Exception as e:
        print(f"비밀번호가 잘못되었거나 파일이 손상되었습니다: {e}")


def show_personal_manito(name: str, password: str) -> None:
    """개인 마니또 대상 확인"""
    encrypted_data = load_encrypted_file()
    if not encrypted_data:
        return
    
    try:
        pairs = decrypt_data(encrypted_data, password)
        
        # 딕셔너리로 변환하여 검색 효율 향상
        pairs_dict = {pair['마니또']: pair['대상'] for pair in pairs}
        
        if name in pairs_dict:
            print(f"\n{name}님의 마니또 대상은 {pairs_dict[name]}님 입니다.")
        else:
            print(f"\n{name}님은 명단에 없습니다.")
            
    except Exception as e:
        print(f"비밀번호가 잘못되었거나 파일이 손상되었습니다: {e}")


def print_name_list() -> None:
    """구성원 명단 출력"""
    print("\n=== 구성원 명단 ===")
    # 한 줄에 여러 이름을 출력하여 가독성 향상
    for i, name in enumerate(names, 1):
        print(f"{i:2d}. {name:<4}", end="\t")
        if i % 5 == 0:  # 5명씩 줄바꿈
            print()
    print()  # 마지막 줄바꿈


def check_file_exists() -> bool:
    """파일 존재 여부 확인"""
    exists = os.path.exists(FILE_PATH)
    if not exists:
        print(f"저장된 마니또 목록이 없습니다.")
    return exists


def main() -> None:
    """메인 함수"""
    menu_options = {
        "1": "마니또 추첨하기 (새로 생성)",
        "2": "마니또 목록 확인하기 (관리자용)",
        "3": "개인별 마니또 확인하기",
        "4": "종료"
    }
    
    while True:
        # 메뉴 출력
        print("\n=== 마니또 프로그램 ===")
        for key, value in menu_options.items():
            print(f"{key}. {value}")
        
        choice = input("선택해주세요: ")
        
        if choice == "1":
            pairs = create_manito_pairs()
            password = getpass.getpass("비밀번호를 설정하세요: ")
            if encrypt_and_save_pairs(pairs, password):
                print("마니또 추첨이 완료되었습니다. 암호화된 파일이 저장되었습니다.")
            
        elif choice == "2":
            if not check_file_exists():
                continue
            password = getpass.getpass("관리자 비밀번호를 입력하세요: ")
            decrypt_and_show_pairs(password)
            
        elif choice == "3":
            if not check_file_exists():
                continue
                
            print_name_list()
            name = input("\n본인의 이름을 입력하세요: ")
            if name in names:
                password = getpass.getpass("비밀번호를 입력하세요: ")
                show_personal_manito(name, password)
            else:
                print("잘못된 이름입니다.")
            
        elif choice == "4":
            print("프로그램을 종료합니다.")
            break
            
        else:
            print("잘못된 선택입니다. 1-4 사이의 숫자를 입력해주세요.")


if __name__ == "__main__":
    main()