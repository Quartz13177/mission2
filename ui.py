"""
화면 출력 / 사용자 입력을 담당하는 도우미 함수 모음.

입력 검증(공백 제거, 숫자 변환 실패, 범위 밖, 빈 입력)을 이 파일에 모아 두었기 때문에
게임 로직(game.py)은 "무엇을 물어볼지"에만 집중할 수 있다.
"""

LINE = "-" * 40
DOUBLE_LINE = "=" * 40


def banner(title):
    """제목을 줄로 감싸서 출력한다."""
    print("")
    print(DOUBLE_LINE)
    print("   " + title)
    print(DOUBLE_LINE)


def divider():
    print(LINE)


def ask_int(prompt, min_value, max_value):
    """
    min_value ~ max_value 사이의 정수를 받을 때까지 계속 다시 물어본다.

    처리하는 잘못된 입력:
      - 빈 입력(그냥 Enter)
      - 숫자가 아닌 값(abc)
      - 범위를 벗어난 숫자(0, 9 등)
      - 앞뒤 공백(" 1 " → 1)
    """
    while True:
        text = input(prompt).strip()

        if text == "":
            print("⚠️  입력이 비어 있습니다. %d~%d 사이의 숫자를 입력하세요." % (min_value, max_value))
            continue

        try:
            value = int(text)
        except ValueError:
            print("⚠️  숫자만 입력할 수 있습니다. %d~%d 사이의 숫자를 입력하세요." % (min_value, max_value))
            continue

        if value < min_value or value > max_value:
            print("⚠️  %d~%d 범위의 숫자를 입력하세요. (입력값: %d)" % (min_value, max_value, value))
            continue

        return value


def ask_choice(prompt, min_value, max_value, extra_keys=()):
    """
    숫자 또는 정해진 글자(예: 힌트 'h')를 받는다.
    숫자를 입력하면 int 를, 정해진 글자를 입력하면 그 글자(소문자)를 돌려준다.
    """
    keys = tuple(str(key).lower() for key in extra_keys)

    while True:
        text = input(prompt).strip()

        if text == "":
            print("⚠️  입력이 비어 있습니다. %d~%d 사이의 숫자를 입력하세요." % (min_value, max_value))
            continue

        if text.lower() in keys:
            return text.lower()

        try:
            value = int(text)
        except ValueError:
            print("⚠️  숫자만 입력할 수 있습니다. %d~%d 사이의 숫자를 입력하세요." % (min_value, max_value))
            continue

        if value < min_value or value > max_value:
            print("⚠️  %d~%d 범위의 숫자를 입력하세요. (입력값: %d)" % (min_value, max_value, value))
            continue

        return value


def ask_text(prompt, allow_empty=False):
    """글자를 입력받는다. allow_empty=False 면 빈 입력을 허용하지 않는다."""
    while True:
        text = input(prompt).strip()
        if text == "" and not allow_empty:
            print("⚠️  내용을 입력해야 합니다.")
            continue
        return text


def ask_yes_no(prompt):
    """y / n 형태의 확인을 받는다."""
    while True:
        text = input(prompt).strip().lower()
        if text in ("y", "yes", "예", "네"):
            return True
        if text in ("n", "no", "아니오", "아니요"):
            return False
        print("⚠️  y(예) 또는 n(아니오) 으로 입력하세요.")
