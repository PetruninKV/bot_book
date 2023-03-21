BOOK_PATH = 'book/book.txt'
# BOOK_PATH = '../book/book.txt'
PAGE_SIZE = 1050

book: dict = {}

def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    max_text = text[start:start + page_size]
    if len(max_text) < page_size:
        return (max_text, len(max_text))
    if max_text.endswith('!.') or max_text.endswith('?.') or max_text.endswith('..'):
        max_text = max_text.strip('!.').strip('?.').strip('..')
    punctuation = ',.!?:;'
    while max_text[-1] not in punctuation:
        max_text = max_text[:-1]
    return (max_text, len(max_text))


def prepare_book(path: str) -> None:
    start: int = 0
    num_str: int = 1
    page_size: int = PAGE_SIZE
    with open(path, 'r', encoding='utf-8') as text:
        text = text.read()
        finish = len(text)
        while start < finish:
            text_for_dict, len_text = _get_part_text(text, start, page_size)
            book[num_str] = text_for_dict.lstrip()
            # print(num_str)
            if num_str == 380:
                print(book[num_str])
            start += len_text
            num_str += 1
        

prepare_book(BOOK_PATH)