import json
import connect

from pathlib import Path
from models import Author, Quote

from json.decoder import JSONDecodeError
from mongoengine.errors import ValidationError


class PathIsNotValidatedError(Exception):
    ...


def convert_json_to_data(path: Path):
    with open(path, encoding='utf-8') as file:
        data = json.load(file)

    if type(data) is list and data:
        for el in data:

            if type(el) is dict:

                if el.get('fullname'):
                    upload_authors_to_db(
                        el.get('fullname'),
                        el.get('born_date'),
                        el.get('born_location'),
                        el.get('description')
                    )
                elif el.get('tags'):
                    upload_quotes_to_db(
                        el.get('tags'),
                        el.get('author'),
                        el.get('quote')
                    )

            continue


def upload_authors_to_db(fullname, born_date, born_location, description):
    Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description).save()


def upload_quotes_to_db(tags, author, quote):
    authors = Author.objects(fullname=author)
    if authors:
        author_id = authors[0]
        Quote(tags=tags, author=author_id, quote=quote).save()


def validate_file(path: Path) -> bool:
    if path.is_file() and path.suffix == '.json':
        return True
    return False


def main():
    path = Path(input('Put the path to the JSON file:\n'
                      'EXAMPLE: C:\Some_User\Documents\data.json\n'
                      '>>> '))

    if validate_file(path):
        convert_json_to_data(path)
        print('\nDone!')
    else:
        raise PathIsNotValidatedError


if __name__ == '__main__':
    try:
        main()
    except PathIsNotValidatedError:
        print('The path is not valid!')
    except JSONDecodeError:
        print('The JSON file cannot be read!')
    except ValidationError:
        print('Data in the JSON file is not valid!')