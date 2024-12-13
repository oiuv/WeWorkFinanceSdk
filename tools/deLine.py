import sys


def delete_line(line_number, file_path='chatdata.jsonl'):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(file_path, 'w') as f:
        for i, line in enumerate(lines):
            if i != line_number - 1:
                f.write(line)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        line_number = int(sys.argv[1])
        delete_line(line_number)
    elif len(sys.argv) == 3:
        line_number = int(sys.argv[1])
        file_path = sys.argv[2]
        delete_line(line_number, file_path)
    else:
        print('Usage: python deLine.py line_number [file_path]')
