import connect
import sys

from models import Author, Quote


def name(arguments):
    author = Author.objects(fullname=arguments)

    if author:
        q = Quote.objects(author=author[0])
        return q
    return []

def tag(arguments):
    q = Quote.objects(tags=arguments)
    quotes = []

    for quote in q:
        quotes.append(quote)
    return quotes

def tags(arguments):
    tags_list = arguments.replace(' ', '').split(',')
    quotes = []

    for tag in tags_list:
        q = Quote.objects(tags=tag)

        for quote in q:
            quotes.append(quote)
    return quotes


def main():

    while True:
        user_input = input('------------------\n'
                           'Available commands: name, tag, tags, exit\n'
                                   'FORMAT -> command:argument\n'
                                   '>>> ')
        if user_input == 'exit':
            break

        try:
            command, arguments = user_input.split(':')
        except ValueError:
            print('Wrong format!')
            continue

        command, arguments = command.strip(), arguments.strip()

        match command:
            case 'name':
                result = name(arguments)
            case 'tag':
                result = tag(arguments)
            case 'tags':
                result = tags(arguments)

        print('------------------')
        for quote in result:
            print(f'Quote: {quote.quote}')

if __name__ == '__main__':
    main()