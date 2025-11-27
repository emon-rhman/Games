import curses
import random


# -----------------------
#   GAME CONFIG
# -----------------------
HEIGHT = 20
WIDTH = 40
SNAKE_SPEED = 300   # ← slow movement in ALL directions


# -----------------------
#   UTILITY FUNCTIONS
# -----------------------
def create_fruit(snake):
    while True:
        fruit = (random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2))
        if fruit not in snake:
            return fruit


def draw_border(stdscr):
    for x in range(WIDTH):
        stdscr.addstr(0, x, "#")
        stdscr.addstr(HEIGHT - 1, x, "#")
    for y in range(HEIGHT):
        stdscr.addstr(y, 0, "#")
        stdscr.addstr(y, WIDTH - 1, "#")


# -----------------------
#    MAIN GAME LOOP
# -----------------------
def run_game(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    stdscr.timeout(SNAKE_SPEED)  # slow speed

    # snake initial position
    snake = [(HEIGHT // 2, WIDTH // 2 + i) for i in range(3)]
    direction = (0, -1)
    fruit = create_fruit(snake)
    score = 0

    while True:
        stdscr.clear()
        draw_border(stdscr)

        # Draw fruit
        stdscr.addstr(fruit[0], fruit[1], "●")

        # Draw snake
        for y, x in snake:
            stdscr.addstr(y, x, "O")

        stdscr.addstr(0, 2, f" SCORE: {score} ")

        key = stdscr.getch()

        # Controls
        if key == curses.KEY_UP and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_DOWN and direction != (-1, 0):
            direction = (1, 0)
        elif key == curses.KEY_LEFT and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)

        # New head
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Wall collision
        if new_head[0] == 0 or new_head[0] == HEIGHT - 1 or \
           new_head[1] == 0 or new_head[1] == WIDTH - 1:
            return score

        # Self collision
        if new_head in snake:
            return score

        snake.insert(0, new_head)

        # Fruit collision
        if new_head == fruit:
            score += 1
            fruit = create_fruit(snake)
        else:
            snake.pop()


# -----------------------
#      MAIN MENU
# -----------------------
def main(stdscr):
    while True:
        stdscr.clear()
        curses.curs_set(0)

        stdscr.addstr(5, 12, "SNAKE GAME")
        stdscr.addstr(7, 8, "Press ENTER to start")
        stdscr.addstr(9, 8, "Press Q to quit")
        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord("\n"), curses.KEY_ENTER):
            score = run_game(stdscr)

            # Game Over Screen
            stdscr.clear()
            stdscr.addstr(7, 10, f"GAME OVER! SCORE: {score}")
            stdscr.addstr(9, 10, "Press ENTER to return to menu")
            stdscr.refresh()

            while True:
                key = stdscr.getch()
                if key in (ord("\n"), curses.KEY_ENTER):
                    break

        elif key in (ord("q"), ord("Q")):
            return


if __name__ == "__main__":
    curses.wrapper(main)
