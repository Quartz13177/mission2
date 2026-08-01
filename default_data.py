"""
기본 퀴즈 데이터 (state.json 이 없는 첫 실행에서 사용된다)

퀴즈 주제 : "개발 입문 기초 상식" (터미널 · Docker · Git · Python · AI 연산)

선정 이유 :
  입학연수 미션1~미션3에서 직접 손으로 익힌 개념만 문제로 만들었다.
  이미지와 컨테이너의 차이, 파일 권한 755, 포트 매핑, 볼륨, MAC 연산처럼
  실습에서 직접 확인한 내용이라 정답의 근거를 스스로 설명할 수 있고,
  같은 과정을 듣는 동료에게도 그대로 복습 도구가 된다.
"""

from quiz import Quiz

# 문제 원본 데이터 (딕셔너리 목록)
RAW_QUIZZES = [
    {
        "question": "Docker에서 '컨테이너를 만들기 위한 설계도' 역할을 하는 것은?",
        "choices": ["이미지", "볼륨", "포트", "브랜치"],
        "answer": 1,
        "hint": "붕어빵에 비유하면 '틀'에 해당합니다.",
    },
    {
        "question": "리눅스 터미널에서 현재 내가 있는 위치(경로)를 확인하는 명령어는?",
        "choices": ["ls", "cd", "pwd", "mkdir"],
        "answer": 3,
        "hint": "print working directory 의 줄임말입니다.",
    },
    {
        "question": "파일 권한 755에서 소유자(첫 번째 자리)가 가진 권한은?",
        "choices": ["읽기만", "읽기+쓰기", "읽기+쓰기+실행", "실행만"],
        "answer": 3,
        "hint": "r=4, w=2, x=1 을 더하면 7이 됩니다.",
    },
    {
        "question": "Git에서 변경 내용을 내 컴퓨터의 저장소에 기록하는 명령어는?",
        "choices": ["git push", "git commit", "git clone", "git pull"],
        "answer": 2,
        "hint": "인터넷 연결이 없어도 할 수 있는 작업입니다.",
    },
    {
        "question": "Python에서 참(True)과 거짓(False) 두 가지 값만 갖는 자료형은?",
        "choices": ["int", "str", "bool", "list"],
        "answer": 3,
        "hint": "조건문 if 의 판단 결과로 나오는 자료형입니다.",
    },
    {
        "question": "컨테이너를 삭제해도 데이터를 남기고 싶을 때 사용하는 것은?",
        "choices": ["포트 매핑", "볼륨", "이미지 태그", "로그"],
        "answer": 2,
        "hint": "Docker가 직접 관리하는 별도의 저장 공간입니다.",
    },
    {
        "question": "브라우저에서 localhost:8080으로 컨테이너에 접속할 수 있게 해 주는 설정은?",
        "choices": ["볼륨", "포트 매핑", "바인드 마운트", "헬스체크"],
        "answer": 2,
        "hint": "docker run 의 -p 옵션이 하는 일입니다.",
    },
    {
        "question": "AI 연산에서 '곱한 뒤 모두 더하는' 연산을 줄여서 부르는 말은?",
        "choices": ["MAC", "CPU", "JSON", "SSH"],
        "answer": 1,
        "hint": "Multiply-Accumulate 의 앞글자입니다.",
    },
]


def default_quizzes():
    """기본 퀴즈를 Quiz 클래스의 인스턴스(객체) 목록으로 만들어 돌려준다."""
    return [Quiz.from_dict(item) for item in RAW_QUIZZES]
