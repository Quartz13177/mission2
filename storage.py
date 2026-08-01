"""
Storage 클래스 : 파일(state.json) 저장/불러오기를 담당한다.

프로그램을 껐다 켜도 데이터가 남아 있게 하는 부분 = '데이터 영속성'.
JSON 은 "사람도 읽을 수 있는 데이터 저장 형식"이라 저장 결과를 눈으로 확인할 수 있다.
"""

import json
import os

from config import DATA_FILE, ENCODING, HISTORY_LIMIT
from default_data import default_quizzes
from quiz import Quiz


class Storage:
    """state.json 파일을 읽고 쓰는 역할만 담당하는 클래스."""

    def __init__(self, path=DATA_FILE):
        self.path = path

    # ------------------------------------------------------------
    # 불러오기
    # ------------------------------------------------------------
    def load(self):
        """
        파일에서 데이터를 읽어 딕셔너리로 돌려준다.

        어떤 문제가 생겨도 프로그램이 죽지 않도록,
        문제 상황마다 기본 퀴즈로 되돌리고 안내 메시지를 함께 돌려준다.
        """
        if not os.path.exists(self.path):
            return self._fallback("저장된 데이터가 없어 기본 퀴즈로 시작합니다.")

        try:
            with open(self.path, "r", encoding=ENCODING) as file:
                raw = json.load(file)
        except (ValueError, UnicodeDecodeError):
            # ValueError 는 json.JSONDecodeError 의 부모 - 파일 내용이 깨진 경우
            moved = self._move_broken_file()
            return self._fallback(
                "데이터 파일이 손상되어 기본 퀴즈로 복구했습니다. (손상 파일: %s)" % moved
            )
        except OSError as error:
            return self._fallback("데이터 파일을 읽지 못했습니다. (%s)" % error)

        if not isinstance(raw, dict):
            moved = self._move_broken_file()
            return self._fallback(
                "데이터 형식이 올바르지 않아 기본 퀴즈로 복구했습니다. (손상 파일: %s)" % moved
            )

        notes = []

        # 1) 퀴즈 목록 복원 - 한 문제가 깨져 있어도 나머지는 살린다.
        quizzes = []
        broken = 0
        for item in self._as_list(raw.get("quizzes")):
            try:
                quizzes.append(Quiz.from_dict(item))
            except (KeyError, TypeError, ValueError):
                broken += 1

        if broken:
            notes.append("형식이 잘못된 퀴즈 %d개를 건너뛰었습니다." % broken)

        if not quizzes:
            quizzes = default_quizzes()
            notes.append("불러올 퀴즈가 없어 기본 퀴즈를 사용합니다.")

        # 2) 최고 점수와 기록 복원
        best_score = self._as_int(raw.get("best_score"), 0)
        best_detail = self._as_detail(raw.get("best_detail"))
        history = self._as_history(raw.get("history"))

        notes.append(
            "저장된 데이터를 불러왔습니다. (퀴즈 %d개, 최고점수 %d점)"
            % (len(quizzes), best_score)
        )

        return {
            "quizzes": quizzes,
            "best_score": best_score,
            "best_detail": best_detail,
            "history": history,
            "notes": notes,
        }

    # ------------------------------------------------------------
    # 저장하기
    # ------------------------------------------------------------
    def save(self, quizzes, best_score, best_detail, history):
        """
        데이터를 JSON 파일로 저장한다. 성공하면 True.

        임시 파일에 먼저 쓰고 마지막에 이름을 바꾸기 때문에,
        저장 도중 프로그램이 멈춰도 기존 파일이 깨지지 않는다.
        """
        payload = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": int(best_score),
            "best_detail": {
                "correct": int(best_detail.get("correct", 0)),
                "total": int(best_detail.get("total", 0)),
            },
            "history": list(history)[-HISTORY_LIMIT:],
        }

        temp_path = self.path + ".tmp"
        try:
            with open(temp_path, "w", encoding=ENCODING) as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
                file.write("\n")
            os.replace(temp_path, self.path)
            return True
        except OSError as error:
            print("⚠️  저장에 실패했습니다. (%s)" % error)
            return False

    # ------------------------------------------------------------
    # 내부에서만 쓰는 도우미 메서드 (이름 앞의 _ 는 '내부용'이라는 관례)
    # ------------------------------------------------------------
    def _fallback(self, message):
        """문제가 생겼을 때 기본 퀴즈로 시작할 수 있게 기본 상태를 만들어 준다."""
        return {
            "quizzes": default_quizzes(),
            "best_score": 0,
            "best_detail": {"correct": 0, "total": 0},
            "history": [],
            "notes": [message],
        }

    def _move_broken_file(self):
        """손상된 파일을 .bak 으로 옮겨서 보관한다."""
        backup_path = self.path + ".bak"
        try:
            os.replace(self.path, backup_path)
            return backup_path
        except OSError:
            return "이동 실패"

    @staticmethod
    def _as_list(value):
        return value if isinstance(value, list) else []

    @staticmethod
    def _as_int(value, default):
        try:
            number = int(value)
        except (TypeError, ValueError):
            return default
        return number if number >= 0 else default

    @staticmethod
    def _as_detail(value):
        detail = {"correct": 0, "total": 0}
        if isinstance(value, dict):
            for key in detail:
                try:
                    detail[key] = max(0, int(value.get(key, 0)))
                except (TypeError, ValueError):
                    detail[key] = 0
        return detail

    @staticmethod
    def _as_history(value):
        records = []
        if not isinstance(value, list):
            return records
        for item in value:
            if isinstance(item, dict) and "score" in item:
                records.append(item)
        return records[-HISTORY_LIMIT:]
