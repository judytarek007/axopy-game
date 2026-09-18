import asyncio
import os
import random
import uuid
import flet as ft


def main(page: ft.Page):
  page.title = "AXOPY - Game to learn"
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.bgcolor = "#F4EEFF"

  client_id = str(uuid.uuid4())

  game_state = {
      "mode": "local",
      "current_player": "X",
      "my_symbol": "X",
      "is_my_turn": True,
      "room_code": None,
      "board_data": [],
  }

  questions = [
      {
          "q": "Which keyword is used to define a function in Python?",
          "ans": "def",
      },
      {
          "q": "Which keyword is used to send a value back from a function?",
          "ans": "return",
      },
      {
          "q": (
              "What keyword is used to create an anonymous (one-line) function?"
          ),
          "ans": "lambda",
      },
      {
          "q": (
              "What are the variables listed inside the function definition"
              " parentheses called?"
          ),
          "ans": "parameters",
      },
      {
          "q": (
              "What are the actual values passed to a function when it is"
              " called called?"
          ),
          "ans": "arguments",
      },
      {
          "q": (
              "What keyword is used as a placeholder for a function body that"
              " will be written later?"
          ),
          "ans": "pass",
      },
      {
          "q": (
              "What symbol is used before a parameter name to accept multiple"
              " positional arguments?"
          ),
          "ans": "*args",
      },
      {
          "q": (
              "What symbol is used before a parameter name to accept multiple"
              " keyword arguments?"
          ),
          "ans": "**kwargs",
      },
      {
          "q": (
              "What built-in function is used to view documentation or info"
              " about another function?"
          ),
          "ans": "help",
      },
      {"q": "What keyword is used to delete a function definition?", "ans": "del"},
      {
          "q": (
              "What built-in data type in Python is commonly used like an"
              " array to store items?"
          ),
          "ans": "list",
      },
  ]

  # تنبيه بسيط للأخطاء أو الحركات الخاطئة
  def show_alert(title_text):
    dlg = ft.AlertDialog(
        title=ft.Text(title_text, size=16, weight=ft.FontWeight.BOLD),
        bgcolor="#F4EEFF",
    )
    page.dialog = dlg
    dlg.open = True
    page.update()

  # شاشة مخصصة لنتائج الفوز أو التعادل تظهر بشكل واضح وجميل
  def show_game_over_screen(message_text):
    clear_view()

    title = ft.Text(
        "🏆 GAME OVER 🏆",
        size=26,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )

    msg = ft.Text(
        message_text,
        size=22,
        weight=ft.FontWeight.BOLD,
        color="#FF85A1",
        text_align=ft.TextAlign.CENTER,
    )

    btn_menu = ft.Button(
        content=ft.Text(
            "🏠 Return to Main Menu",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#FFB5A7",
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_main_menu(),
    )

    content = ft.Column(
        [
            title,
            ft.Container(height=20),
            msg,
            ft.Container(height=40),
            btn_menu,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    page.add(content)

  def clear_view():
    page.clean()

  def global_pubsub_listener(message):
    if isinstance(message, dict):
      if message.get("sender") == client_id:
        return

      if (
          game_state["mode"] == "online"
          and message.get("room") == game_state["room_code"]
      ):
        msg_type = message.get("type")
        if msg_type == "join_room" and game_state["my_symbol"] == "X":
          page.pubsub.send_all({
              "sender": client_id,
              "type": "start_game",
              "room": game_state["room_code"],
              "board": game_state["board_data"],
          })
          init_board_ui("online")
        elif msg_type == "start_game" and game_state["my_symbol"] == "O":
          game_state["board_data"] = message["board"]
          init_board_ui("online")
        elif msg_type == "move":
          idx = message["idx"]
          status = message["status"]
          game_state["board_data"][idx]["status"] = status
          if check_winner():
            show_game_over_screen(f"Congratulations Player {status}!")
            return
          if check_draw():
            show_game_over_screen("It's a Draw!")
            return
          game_state["is_my_turn"] = True
          init_board_ui("online")

  page.pubsub.subscribe(global_pubsub_listener)

  def show_welcome():
    clear_view()

    lbl_welcome = ft.Text(
        "✨ Welcome to our game ✨",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )
    title = ft.Text(
        "AXOPY 🎮",
        size=42,
        weight=ft.FontWeight.BOLD,
        color="#FF85A1",
        text_align=ft.TextAlign.CENTER,
    )

    btn_start = ft.Button(
        content=ft.Text(
            "🚀 START GAME", size=16, weight=ft.FontWeight.BOLD, color="#2C2C54"
        ),
        bgcolor="#FFB5A7",
        width=280,
        height=55,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_main_menu(),
    )

    footer = ft.Text(
        "Get ready to test your Python knowledge & tactics!",
        size=11,
        color="#3498DB",
        text_align=ft.TextAlign.CENTER,
    )

    content = ft.Column(
        [
            ft.Container(height=40),
            lbl_welcome,
            ft.Container(height=10),
            title,
            ft.Container(height=40),
            btn_start,
            ft.Container(height=60),
            footer,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(content)

  def show_main_menu():
    clear_view()

    title = ft.Text(
        "🎮 Main Menu",
        size=26,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )

    btn_local = ft.Button(
        content=ft.Text(
            "👥 Local Multiplayer (2P)",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#FFB5A7",
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: start_game("local"),
    )

    btn_ai = ft.Button(
        content=ft.Text(
            "🤖 Play vs Computer",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#9BF6FF",
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: start_game("ai"),
    )

    btn_online = ft.Button(
        content=ft.Text(
            "🌐 Online Multiplayer",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#FDFFB6",
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_online_menu(),
    )

    btn_back = ft.Button(
        content=ft.Text(
            "⬅ Back to Welcome",
            size=11,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#CAFFBF",
        width=200,
        height=40,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_welcome(),
    )

    content = ft.Column(
        [
            title,
            ft.Container(height=20),
            btn_local,
            ft.Container(height=10),
            btn_ai,
            ft.Container(height=10),
            btn_online,
            ft.Container(height=25),
            btn_back,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(content)

  def show_online_menu():
    clear_view()
    title = ft.Text(
        "🌐 Online Game Settings",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )
    desc = ft.Text(
        "Host a new game room or join an existing room code.",
        size=11,
        color="#3498DB",
        text_align=ft.TextAlign.CENTER,
    )

    btn_host = ft.Button(
        content=ft.Text(
            "🏠 Host Game",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#9BF6FF",
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: host_game(),
    )

    btn_join = ft.Button(
        content=ft.Text(
            "🔗 Join Game",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#FFB5A7",
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_join_screen(),
    )

    btn_back = ft.Button(
        content=ft.Text(
            "⬅ Back", size=12, weight=ft.FontWeight.BOLD, color="#2C2C54"
        ),
        bgcolor="#CAFFBF",
        width=180,
        height=40,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_main_menu(),
    )

    content = ft.Column(
        [
            title,
            ft.Container(height=10),
            desc,
            ft.Container(height=25),
            btn_host,
            ft.Container(height=15),
            btn_join,
            ft.Container(height=25),
            btn_back,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(content)

  def host_game():
    game_state["mode"] = "online"
    game_state["my_symbol"] = "X"
    game_state["is_my_turn"] = True

    room_code = str(random.randint(1000, 9999))
    game_state["room_code"] = room_code

    sample_count = min(9, len(questions))
    chosen_questions = random.sample(questions, sample_count)
    random.shuffle(chosen_questions)

    board = []
    for item in chosen_questions:
      board.append({"q": item["q"], "ans": item["ans"], "status": "available"})

    game_state["board_data"] = board
    show_waiting_screen(
        f"Room created! Code: {room_code}\nWaiting for opponent to join..."
    )

  def show_join_screen():
    clear_view()

    title = ft.Text(
        "🔗 Join Online Game",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )
    desc = ft.Text(
        "Enter the 4-digit room code provided by your friend.",
        size=12,
        color="#3498DB",
        text_align=ft.TextAlign.CENTER,
    )

    code_input = ft.TextField(
        label="Enter Room Code",
        width=260,
        height=50,
        text_align=ft.TextAlign.CENTER,
        border_radius=8,
        bgcolor="#FFFFFF",
    )

    def join_action(e):
      code = code_input.value.strip()
      if code != "":
        game_state["mode"] = "online"
        game_state["my_symbol"] = "O"
        game_state["is_my_turn"] = False
        game_state["room_code"] = code

        page.pubsub.send_all({
            "sender": client_id,
            "type": "join_room",
            "room": code,
        })
        init_board_ui("online")
      else:
        show_alert("Please enter a valid room code!")

    btn_connect = ft.Button(
        content=ft.Text(
            "🚀 Connect",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#9BF6FF",
        width=260,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=join_action,
    )

    btn_back = ft.Button(
        content=ft.Text(
            "⬅ Back", size=12, weight=ft.FontWeight.BOLD, color="#2C2C54"
        ),
        bgcolor="#CAFFBF",
        width=180,
        height=40,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_online_menu(),
    )

    content = ft.Column(
        [
            title,
            ft.Container(height=10),
            desc,
            ft.Container(height=25),
            code_input,
            ft.Container(height=20),
            btn_connect,
            ft.Container(height=15),
            btn_back,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    page.add(content)

  def show_waiting_screen(text):
    clear_view()
    lbl = ft.Text(
        text,
        size=16,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )

    btn_back = ft.Button(
        content=ft.Text(
            "Cancel", size=12, weight=ft.FontWeight.BOLD, color="#2C2C54"
        ),
        bgcolor="#FFB5A7",
        width=150,
        height=40,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_main_menu(),
    )

    content = ft.Column(
        [lbl, ft.Container(height=30), btn_back],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    page.add(content)

  def start_game(mode):
    game_state["mode"] = mode
    game_state["my_symbol"] = "X"
    game_state["is_my_turn"] = True
    game_state["current_player"] = "X"

    sample_count = min(9, len(questions))
    chosen_questions = random.sample(questions, sample_count)
    random.shuffle(chosen_questions)

    board = []
    for item in chosen_questions:
      board.append({"q": item["q"], "ans": item["ans"], "status": "available"})
    game_state["board_data"] = board
    init_board_ui(mode)

  def init_board_ui(mode):
    clear_view()

    status_text = (
        f"Player Turn: {game_state['current_player']}"
        if mode != "online"
        else f"Your Symbol: {game_state['my_symbol']} ({'Your Turn' if game_state['is_my_turn'] else 'Opponent Turn'})"
    )

    info_label = ft.Text(
        status_text,
        size=16,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )

    grid_rows = []
    for r in range(3):
      row_btns = []
      for c in range(3):
        idx = r * 3 + c
        item = game_state["board_data"][idx]

        btn_text = "Q"
        btn_bg = "#BDB2FF"
        btn_fg = "#2C2C54"
        font_size = 18
        weight = ft.FontWeight.BOLD

        if item["status"] in ("X", "O"):
          btn_text = item["status"]
          btn_bg = "#FFB5A7" if item["status"] == "X" else "#9BF6FF"
          font_size = 22
        elif item["status"] == "OPEN":
          btn_text = item["q"]
          btn_bg = "#FDFFB6"
          font_size = 9
          weight = ft.FontWeight.W_500

        b = ft.Button(
            content=ft.Text(
                btn_text,
                size=font_size,
                weight=weight,
                color=btn_fg,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=btn_bg,
            width=110,
            height=100,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=lambda e, i=idx: make_move(i),
        )
        row_btns.append(b)
      grid_rows.append(
          ft.Row(
              row_btns,
              alignment=ft.MainAxisAlignment.CENTER,
              spacing=6,
          )
      )

    back_btn = ft.Button(
        content=ft.Text(
            "🏠 Main Menu", size=12, weight=ft.FontWeight.BOLD, color="#2C2C54"
        ),
        bgcolor="#FFC6FF",
        width=160,
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: show_main_menu(),
    )

    content = ft.Column(
        [
            info_label,
            ft.Container(height=10),
            *grid_rows,
            ft.Container(height=15),
            back_btn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(content)

  def make_move(idx):
    if game_state["mode"] == "online" and not game_state["is_my_turn"]:
      show_alert("It's not your turn! Wait for your opponent.")
      return

    item = game_state["board_data"][idx]
    if item["status"] in ("X", "O"):
      show_alert("This cell is already occupied!")
      return

    show_question_screen(idx)

  def show_question_screen(idx):
    clear_view()
    item = game_state["board_data"][idx]
    is_open = item["status"] == "OPEN"
    title_text = (
        f"Cell {idx+1} Question (Open)" if is_open else "Python Question 💡"
    )

    title = ft.Text(
        title_text,
        size=22,
        weight=ft.FontWeight.BOLD,
        color="#8E44AD",
        text_align=ft.TextAlign.CENTER,
    )
    q_label = ft.Text(
        item["q"],
        size=16,
        weight=ft.FontWeight.W_500,
        color="#2C2C54",
        text_align=ft.TextAlign.CENTER,
    )

    ans_input = ft.TextField(
        label="Type your answer here...",
        width=320,
        text_align=ft.TextAlign.CENTER,
        border_radius=8,
    )

    def submit_answer(e):
      user_ans = ans_input.value
      if user_ans is None or user_ans.strip() == "":
        item["status"] = "OPEN"
        handle_turn_end(idx, "OPEN")
        return

      if user_ans.strip().lower() == item["ans"].lower():
        winner_symbol = (
            game_state["current_player"]
            if game_state["mode"] != "online"
            else game_state["my_symbol"]
        )
        item["status"] = winner_symbol

        if check_winner():
          if game_state["mode"] == "online":
            page.pubsub.send_all({
                "sender": client_id,
                "type": "move",
                "room": game_state["room_code"],
                "idx": idx,
                "status": winner_symbol,
            })
          show_game_over_screen(f"Congratulations Player {winner_symbol}!")
          return

        if check_draw():
          if game_state["mode"] == "online":
            page.pubsub.send_all({
                "sender": client_id,
                "type": "move",
                "room": game_state["room_code"],
                "idx": idx,
                "status": winner_symbol,
            })
          show_game_over_screen("It's a Draw!")
          return

        handle_turn_end(idx, winner_symbol)
      else:
        item["status"] = "OPEN"
        if check_draw():
          if game_state["mode"] == "online":
            page.pubsub.send_all({
                "sender": client_id,
                "type": "move",
                "room": game_state["room_code"],
                "idx": idx,
                "status": "OPEN",
            })
          show_game_over_screen("It's a Draw!")
          return

        handle_turn_end(idx, "OPEN")

    def skip_answer(e):
      item["status"] = "OPEN"
      handle_turn_end(idx, "OPEN")

    btn_submit = ft.Button(
        content=ft.Text(
            "✅ Submit Answer",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#9BF6FF",
        width=240,
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=submit_answer,
    )

    btn_skip = ft.Button(
        content=ft.Text(
            "⏭ Pass / Skip Question",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#2C2C54",
        ),
        bgcolor="#FFB5A7",
        width=240,
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=skip_answer,
    )

    content = ft.Column(
        [
            ft.Container(height=30),
            title,
            ft.Container(height=20),
            q_label,
            ft.Container(height=25),
            ans_input,
            ft.Container(height=20),
            btn_submit,
            ft.Container(height=10),
            btn_skip,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    page.add(content)

  def handle_turn_end(idx, status):
    if game_state["mode"] == "online":
      page.pubsub.send_all({
          "sender": client_id,
          "type": "move",
          "room": game_state["room_code"],
          "idx": idx,
          "status": status,
      })
      game_state["is_my_turn"] = False
      init_board_ui("online")
    elif game_state["mode"] == "ai":
      game_state["current_player"] = "O"
      init_board_ui("ai")
      page.run_task(ai_turn_delay)
    else:
      game_state["current_player"] = (
          "O" if game_state["current_player"] == "X" else "X"
      )
      init_board_ui("local")

  async def ai_turn_delay():
    await asyncio.sleep(0.8)
    available = [
        i
        for i, item in enumerate(game_state["board_data"])
        if item["status"] not in ("X", "O")
    ]
    if not available:
      return
    ai_choice = random.choice(available)
    item = game_state["board_data"][ai_choice]
    correct = random.choice([True, False])
    if correct:
      item["status"] = "O"
      if check_winner():
        show_game_over_screen("Congratulations Player O!")
        return
    else:
      item["status"] = "OPEN"
      show_alert("Computer made a mistake and the cell text is now visible!")

    if check_draw():
      show_game_over_screen("It's a Draw!")
      return

    game_state["current_player"] = "X"
    init_board_ui("ai")

  def check_winner():
    win_combos = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    board = game_state["board_data"]
    for a, b, c in win_combos:
      if (
          board[a]["status"] == board[b]["status"] == board[c]["status"]
      ) and board[a]["status"] in ("X", "O"):
        return True
    return False

  def check_draw():
    return not any(
        item["status"] in ("available", "OPEN")
        for item in game_state["board_data"]
    )

  show_welcome()


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 10000))

  if "PORT" in os.environ:
    ft.run(main, port=port, host="0.0.0.0")
  else:
    ft.run(main, port=port, host="127.0.0.1", view=ft.AppView.WEB_BROWSER)