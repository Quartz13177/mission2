"""
퀴즈 풀기(출제 진행) 기능.

game.py 의 QuizGame 이 "상태 관리"를 담당한다면,
이 파일은 "한 판을 어떻게 진행할지"만 담당한다.

보너스 기능 포함:
  - 문제 순서 랜덤 섞기 (config.SHUFFLE_QUESTIONS)
  - 몇 문제를 풀지 선택
  - 힌트(h) 사용 시 점수 차감
"""

import random

import ui
from config import CHOICE_COUNT, HINT_PENALTY, SHUFFLE_QUESTIONS


def run_round(game):
    """
    퀴즈 한 판을 진행한다.

    game : QuizGame 객체. 문제 목록을 빌려오고, 결과를 돌려주기 위해 받는다.
    """
    # 퀴즈가 하나도 없는 경우를 먼저 처리한다.
    if not game.quizzes:
        print("")
        print("📭 등록된 퀴즈가 없습니다. 먼저 [2] 퀴즈 추가로 문제를 만들어 주세요.")
        return

    # 몇 문제를 풀지 고른다. (보너스 2: 문제 수 선택)
    total_available = len(game.quizzes)
    if total_available == 1:
        count = 1
    else:
        print("")
        count = ui.ask_int(
            "몇 문제를 풀까요? (1~%d): " % total_available, 1, total_available
        )

    # 원본 목록을 그대로 섞으면 저장된 순서까지 바뀌므로 복사본을 만들어 섞는다.
    selected = list(game.quizzes)
    if SHUFFLE_QUESTIONS:
        random.shuffle(selected)          # 보너스 1: 랜덤 출제
    selected = selected[:count]

    print("")
    print("📝 퀴즈를 시작합니다! (총 %d문제)" % len(selected))
    ui.divider()

    correct_count = 0
    hint_count = 0

    # 고른 문제를 하나씩 출제한다.
    for index, quiz in enumerate(selected, start=1):
        print("")
        print(quiz.render(index))

        # 정답을 입력받는다. 'h' 를 누르면 힌트를 보여주고 다시 물어본다.
        while True:
            answer = ui.ask_choice(
                "정답 입력 (1~%d, 힌트는 h): " % CHOICE_COUNT,
                1,
                CHOICE_COUNT,
                extra_keys=("h",),
            )
            if answer == "h":
                if quiz.has_hint():
                    hint_count += 1        # 보너스 3: 힌트 사용 횟수 기록
                    print("💡 힌트: %s (힌트 사용 -%d점)" % (quiz.hint, HINT_PENALTY))
                else:
                    print("💡 이 문제에는 준비된 힌트가 없습니다.")
                continue
            break

        # 채점은 Quiz 객체가 스스로 한다.
        if quiz.is_correct(answer):
            correct_count += 1
            print("✅ 정답입니다!")
        else:
            print(
                "❌ 오답입니다. 정답은 %d번 (%s) 입니다."
                % (quiz.answer, quiz.answer_text())
            )
        ui.divider()

    # 결과 처리(점수 계산·최고 점수 갱신·저장)는 QuizGame 에게 넘긴다.
    game.record_result(correct_count, len(selected), hint_count)
