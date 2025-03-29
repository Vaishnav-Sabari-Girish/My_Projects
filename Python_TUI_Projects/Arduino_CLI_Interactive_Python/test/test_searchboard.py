from arduino_utils import list_arduino_boards, search_boards

sketch_file = list_arduino_boards()

board_name = str(input(("Enter Board Name: ")))

search_boards(board_name)
