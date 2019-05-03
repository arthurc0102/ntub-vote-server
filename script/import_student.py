import re
import os
import django

from argparse import ArgumentParser, ArgumentTypeError

from pathlib import Path


# Django setup, this must done before you import your models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

STD_NO_PATTERN = \
    '(?P<night>[N|n]?)' \
    '(?P<year>[0-9]{2,3})' \
    '(?P<system>[1-9])' \
    '(?P<department>[1-9A-Za-z])' \
    '(?P<class>[0-9]?)' \
    '(?P<no>[0-9]{2})'


def file_type(file_path):
    file = Path(file_path)

    if not file.is_file():
        raise ArgumentTypeError(f'{file_path} is not a file.')

    if file.suffix != '.csv':
        raise ArgumentTypeError(f'{file_path} is not a csv file.')

    return file


def parse_args():
    parser = ArgumentParser(description='NTUB Vote student import tool.')

    parser.add_argument(dest='group', help='Group name', type=str)
    parser.add_argument(dest='file', help='CSV file', type=file_type)
    parser.add_argument(
        '-t', '--title',
        help='CSV file include data',
        action='store_true',
    )

    return parser.parse_args()


def validate_std_no(std_no):
    return re.compile(STD_NO_PATTERN).match(std_no)


def insert_data(group, data):
    from app.school.models import Group, Student

    group, _ = Group.objects.get_or_create(name=group)

    for std_no in data:
        std, _ = Student.objects.get_or_create(std_no=std_no)
        std.groups.add(group)
        std.save()


def main():
    args = parse_args()

    data = []
    with open(args.file, 'r') as f:
        data = f.read().split()

        if args.title:
            data = data[1:]

    assert len(data) > 0, 'No data.'

    for i, std_no in enumerate(data):
        if validate_std_no(std_no):
            continue

        print(f'Fail!!! {std_no} isn\'t valid.')
        data.pop(i)

    insert_data(args.group, data)


if __name__ == '__main__':
    main()
