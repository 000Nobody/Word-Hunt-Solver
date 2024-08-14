def get_words_dict():
    word_file = open("words.txt", "r")
    words = {}
    while True:
        word = word_file.readline()[0:-1]
        if not word:
            break
        if word[0] not in words.keys():
            words[word[0]] = [word]
        else:
            words[word[0]].append(word)

    return words


def get_board():
    board = input("Enter board letters: ").upper()
    if is_valid_board(board):
        return board


def is_valid_board(board):
    if len(board) != 16:
        print("Invalid Input")
        return False
    return True


def get_adjacent_cells(index):
    adjacent_cells = []

    left = (index % 4 != 0)
    right = (index % 4 != 3)
    top = (index >= 4)
    bottom = (index < 12)

    if top and left:
        adjacent_cells.append(index - 5)
    if top and right:
        adjacent_cells.append(index - 3)
    if top:
        adjacent_cells.append(index - 4)
    if left:
        adjacent_cells.append(index - 1)
    if right:
        adjacent_cells.append(index + 1)
    if bottom and left:
        adjacent_cells.append(index + 3)
    if bottom:
        adjacent_cells.append(index + 4)
    if bottom and right:
        adjacent_cells.append(index + 5)

    return adjacent_cells


def indexes_to_word(indexes, board):
    word = ""
    for index in indexes:
        word += board[index]

    return word


def solve(board, words):
    output = []
    for index in range(len(board)):
        possible_words = words[board[index]]
        solution = solve_adjacent_cells(board, index, possible_words)
        output.append(solution)

    return output


def solve_adjacent_cells(board, current_index, possible_words, word_indexes = []):
    output = {}

    current_word_indexes = word_indexes.copy()
    current_word_indexes.append(current_index)

    new_possible_words = []
    if len(current_word_indexes) >= 3:
        for word in possible_words:
            if word == indexes_to_word(current_word_indexes, board):
                output[word] = current_word_indexes
            elif word.startswith(indexes_to_word(current_word_indexes, board)):
                new_possible_words.append(word)
    else:
        new_possible_words = possible_words

    if len(new_possible_words) > 0:
        adjacent_cells = get_adjacent_cells(current_index)
        new_adjacent_cells = [cell for cell in adjacent_cells if cell not in current_word_indexes]
        for index in new_adjacent_cells:
            output.update(solve_adjacent_cells(board, index, new_possible_words, current_word_indexes))

    return output


def sort_answers(answers):
    output = []
    for solution_dict in answers:
        for key in solution_dict.keys():
            output.append(key)
    output = list(set(output))
    return sorted(output, key=len)


if __name__ == "__main__":
    words = get_words_dict()
    board = get_board()
    answers = solve(board, words)
    answer_words = sort_answers(answers)
    for word in answer_words:
        print(word)
