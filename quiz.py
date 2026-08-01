"""
Quiz 클래스 : "문제 한 개"를 담당하는 설계도.

문제 1개 = Quiz 객체 1개.
문제 내용, 선택지 4개, 정답 번호, 힌트를 하나로 묶어서 관리한다.
"""

from config import CHOICE_COUNT


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스."""

    def __init__(self, question, choices, answer, hint=""):
        """
        객체가 만들어질 때 자동으로 실행되는 메서드.
        self 는 "지금 만들어지고 있는 이 객체 자신"을 가리킨다.

        잘못된 데이터가 들어오면 여기서 걸러내므로,
        일단 만들어진 Quiz 객체는 항상 올바른 형태임이 보장된다.
        """
        question = str(question).strip()
        if not question:
            raise ValueError("문제 내용은 비어 있을 수 없습니다.")

        choices = [str(choice).strip() for choice in choices]
        if len(choices) != CHOICE_COUNT:
            raise ValueError("선택지는 정확히 %d개여야 합니다." % CHOICE_COUNT)
        for choice in choices:
            if not choice:
                raise ValueError("빈 선택지는 사용할 수 없습니다.")

        answer = int(answer)
        if answer < 1 or answer > CHOICE_COUNT:
            raise ValueError("정답 번호는 1~%d 사이여야 합니다." % CHOICE_COUNT)

        # 아래 4개가 이 객체의 '속성(attribute)'이다.
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = str(hint).strip()

    # ------------------------------------------------------------
    # 메서드 : 이 객체가 할 수 있는 일들
    # ------------------------------------------------------------
    def render(self, index=None):
        """화면에 출력할 문제 텍스트를 만들어 돌려준다."""
        if index is None:
            lines = [self.question]
        else:
            lines = ["[문제 %d] %s" % (index, self.question)]

        for number, choice in enumerate(self.choices, start=1):
            lines.append("  %d. %s" % (number, choice))
        return "\n".join(lines)

    def is_correct(self, number):
        """사용자가 입력한 번호가 정답인지 True / False 로 알려준다."""
        return int(number) == self.answer

    def answer_text(self):
        """정답 번호에 해당하는 선택지 글자를 돌려준다."""
        return self.choices[self.answer - 1]

    def has_hint(self):
        """이 문제에 힌트가 있는지 알려준다."""
        return self.hint != ""

    # ------------------------------------------------------------
    # JSON 파일로 저장하거나 불러오기 위한 변환 메서드
    # ------------------------------------------------------------
    def to_dict(self):
        """객체 → 딕셔너리 (JSON 으로 저장할 수 있는 형태)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리 → 객체 (JSON 에서 읽어온 데이터를 Quiz 로 되돌린다)"""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터가 딕셔너리 형태가 아닙니다.")
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", ""),
        )

    def __repr__(self):
        """디버깅할 때 객체를 알아보기 쉽게 출력해 주는 특별한 메서드."""
        return "Quiz(question=%r, answer=%d)" % (self.question, self.answer)
