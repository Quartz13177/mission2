"""
QuizGame 클래스 : 게임 전체를 관리하는 '사회자' 역할.

- 어떤 퀴즈들이 있는지(quizzes), 최고 점수가 몇 점인지(best_score)를 들고 있고
- 메뉴 표시 / 퀴즈 추가 / 목록 / 점수 확인 / 삭제 / 저장을 메서드로 나눠서 수행한다.

퀴즈 풀기 기능은 별도 브랜치(feature/play-quiz)에서 개발할 예정이다.
"""

import ui
from config import CHOICE_COUNT
from quiz import Quiz
from storage import Storage

MENU_ITEMS = (
    "1. 퀴즈 풀기",
    "2. 퀴즈 추가",
    "3. 퀴즈 목록",
    "4. 점수 확인",
    "5. 퀴즈 삭제",
    "6. 종료",
)
MENU_MIN = 1
MENU_MAX = 6


class QuizGame:
    """게임 진행 전체를 관리하는 클래스."""

    def __init__(self, storage=None):
        # 속성(attribute) : 이 게임이 기억해야 하는 정보들
        self.storage = storage if storage is not None else Storage()
        self.quizzes = []
        self.best_score = 0
        self.best_detail = {"correct": 0, "total": 0}
        self.history = []

    # ------------------------------------------------------------
    # 저장 / 불러오기
    # ------------------------------------------------------------
    def load(self):
        """Storage 에게 데이터를 요청해서 내 속성에 담는다."""
        state = self.storage.load()
        self.quizzes = state["quizzes"]
        self.best_score = state["best_score"]
        self.best_detail = state["best_detail"]
        self.history = state["history"]
        for note in state["notes"]:
            print("📂 " + note)

    def save(self):
        """현재 상태를 Storage 에게 넘겨 파일로 저장한다."""
        return self.storage.save(
            self.quizzes, self.best_score, self.best_detail, self.history
        )

    # ------------------------------------------------------------
    # 메인 루프
    # ------------------------------------------------------------
    def show_menu(self):
        print("")
        print(ui.DOUBLE_LINE)
        for item in MENU_ITEMS:
            print(item)
        print(ui.DOUBLE_LINE)

    def run(self):
        """프로그램의 시작점. 메뉴를 반복해서 보여준다."""
        ui.banner("🎯 나만의 퀴즈 게임 🎯")
        self.load()

        while True:
            try:
                self.show_menu()
                choice = ui.ask_int("선택: ", MENU_MIN, MENU_MAX)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    self.delete_quiz()
                else:
                    print("")
                    print("💾 데이터를 저장하고 종료합니다.")
                    self.save()
                    print("👋 안녕히 가세요!")
                    break

            except (KeyboardInterrupt, EOFError):
                # Ctrl+C 를 눌러도, 입력이 갑자기 끊겨도 '비정상 종료'하지 않는다.
                print("")
                print("")
                print("⚠️  입력이 중단되었습니다. 지금까지의 데이터를 저장하고 안전하게 종료합니다.")
                self.save()
                break

    # ------------------------------------------------------------
    # 1. 퀴즈 풀기 (feature/play-quiz 브랜치에서 구현 예정)
    # ------------------------------------------------------------
    def play_quiz(self):
        print("")
        print("🚧 퀴즈 풀기 기능은 아직 준비 중입니다.")

    # ------------------------------------------------------------
    # 2. 퀴즈 추가
    # ------------------------------------------------------------
    def add_quiz(self):
        print("")
        print("📌 새로운 퀴즈를 추가합니다. (중간에 Ctrl+C 를 누르면 취소됩니다)")

        question = ui.ask_text("문제를 입력하세요: ")

        choices = []
        for number in range(1, CHOICE_COUNT + 1):
            choices.append(ui.ask_text("선택지 %d: " % number))

        answer = ui.ask_int("정답 번호 (1-%d): " % CHOICE_COUNT, 1, CHOICE_COUNT)
        hint = ui.ask_text("힌트 (없으면 그냥 Enter): ", allow_empty=True)

        try:
            new_quiz = Quiz(question, choices, answer, hint)
        except ValueError as error:
            print("⚠️  퀴즈를 만들 수 없습니다: %s" % error)
            return

        self.quizzes.append(new_quiz)
        if self.save():
            print("✅ 퀴즈가 추가되었습니다! (현재 총 %d개)" % len(self.quizzes))
        else:
            print("⚠️  퀴즈는 추가되었지만 파일 저장에 실패했습니다.")

    # ------------------------------------------------------------
    # 3. 퀴즈 목록
    # ------------------------------------------------------------
    def list_quizzes(self):
        print("")
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return

        print("📋 등록된 퀴즈 목록 (총 %d개)" % len(self.quizzes))
        ui.divider()
        for index, quiz in enumerate(self.quizzes, start=1):
            mark = " 💡" if quiz.has_hint() else ""
            print("[%d] %s%s" % (index, quiz.question, mark))
        ui.divider()
        print("* 정답은 표시하지 않습니다. 💡 표시는 힌트가 있는 문제입니다.")

    # ------------------------------------------------------------
    # 4. 점수 확인
    # ------------------------------------------------------------
    def show_score(self):
        print("")
        if self.best_detail["total"] == 0 and self.best_score == 0:
            print("📊 아직 퀴즈를 풀지 않았습니다. [1] 퀴즈 풀기로 도전해 보세요!")
            return

        print(
            "🏆 최고 점수: %d점 (%d문제 중 %d문제 정답)"
            % (self.best_score, self.best_detail["total"], self.best_detail["correct"])
        )

        if self.history:
            print("")
            print("🕘 최근 기록")
            ui.divider()
            for record in self.history[-5:][::-1]:
                print(
                    "%s | %d문제 중 %d개 정답 | %d점"
                    % (
                        record.get("played_at", "-"),
                        record.get("total", 0),
                        record.get("correct", 0),
                        record.get("score", 0),
                    )
                )
            ui.divider()

    # ------------------------------------------------------------
    # 5. 퀴즈 삭제 (보너스 4)
    # ------------------------------------------------------------
    def delete_quiz(self):
        print("")
        if not self.quizzes:
            print("📭 삭제할 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        number = ui.ask_int(
            "삭제할 퀴즈 번호 (1~%d): " % len(self.quizzes), 1, len(self.quizzes)
        )
        target = self.quizzes[number - 1]

        if not ui.ask_yes_no("'%s' 를 정말 삭제할까요? (y/n): " % target.question):
            print("취소했습니다.")
            return

        self.quizzes.pop(number - 1)
        if self.save():
            print("🗑️  삭제했습니다. (현재 총 %d개)" % len(self.quizzes))
        else:
            print("⚠️  삭제했지만 파일 저장에 실패했습니다.")
