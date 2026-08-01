"""
프로그램의 시작 파일.

실행 방법:
    python main.py

여기서는 "게임을 만들고 실행한다" 는 한 가지 일만 한다.
실제 동작은 game.py 의 QuizGame 클래스가 담당한다. (역할 분리)
"""

from game import QuizGame


def main():
    game = QuizGame()
    game.run()


# 이 파일을 직접 실행했을 때만 main() 을 호출한다.
# (다른 파일에서 import 할 때는 실행되지 않게 하는 파이썬의 관례)
if __name__ == "__main__":
    main()
