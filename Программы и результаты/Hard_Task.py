#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import jsonschema


@click.group()
@click.version_option(version="0.1.0")
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.option('-n', '--name', required=True, help="The human's name.")
@click.option('-s', '--surname', required=True, help="The human's surname.")
@click.option('-t', '--telephone', required=True, help="The human's telephone number.")
@click.option('-b', '--birthday', required=True, help="The human's birthday.")
def add(filename, name, surname, telephone, birthday):
    """Добавить запись о новом человеке."""
    people = load_people(filename)
    people.append({
        "name": name,
        "surname": surname,
        "telephone": telephone,
        "birthday": birthday
    })
    save_people(filename, people)


@cli.command()
@click.argument('filename')
def display(filename):
    """Вывести список всех людей."""
    people = load_people(filename)
    display_people(people)


@cli.command()
@click.argument('filename')
@click.option('-P', '--period', type=int, required=True, help="The needed month.")
def select(filename, period):
    """Выбрать людей по требуемому месяцу рождения."""
    people = load_people(filename)
    selected_people = select_people(people, period)
    display_people(selected_people)


def new_human(people, name, surname, telephone, happy_birthday):
    """Добавить данные о человеке."""
    people.append({
        "name": name,
        "surname": surname,
        "telephone": telephone,
        "birthday": happy_birthday
    })
    return people


def display_people(people):
    """Отобразить список людей."""
    if people:
        line = "├-{}-⫟-{}⫟-{}-⫟-{}-⫟-{}-┤".format(
            "-" * 5, "-" * 25, "-" * 25, "-" * 25, "-" * 18)
        # print(line)
        click.echo(line)
        # print("| {:^5} | {:^24} | {:^25} | {:^25} | {:^18} |".format(
        #     "№", "Name", "Surname", "Telephone", "Birthday"))
        click.echo("| {:^5} | {:^24} | {:^25} | {:^25} | {:^18} |".format(
            "№", "Name", "Surname", "Telephone", "Birthday"))

        # print(line)
        click.echo(line)
        for number, human in enumerate(people, 1):
            # print("| {:^5} | {:<24} | {:<25} | {:<25} | {:<18} |".format(number, human.get("name", ""), human.get("surname", ""),
            #                                                              human.get("telephone", ""), human.get("birthday", "")))
            click.echo("| {:^5} | {:<24} | {:<25} | {:<25} | {:<18} |".format(number, human.get("name", ""), human.get("surname", ""),
                                                                              human.get("telephone", ""), human.get("birthday", ""))
                       )
        # print(line)
        click.echo(line)
    else:
        # print("There are no people in list!")
        click.echo("There are no people in list!")


def select_people(people, month):
    """Выбрать людей, родившихся в требуемом месяце."""
    born = []
    for human in people:
        human_month = human.get("birthday").split(".")
        if month == int(human_month[1]):
            born.append(human)
    return born


def save_people(file_name, staff):
    """Сохранить всех людей в файл JSON."""
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """Загрузить всех людей из файла JSON."""

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "surname": {"type": "string"},
                "telephone": {"type": "string"},
                "birthday": {"type": "string"}
            },
            "required": ["name", "surname", "telephone", "birthday"]
        }
    }

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        loaded = json.load(fin)
    try:
        jsonschema.validate(loaded, schema)
        # print(">>> Data is obtained!")
        click.echo(">>> Data is obtained!")
        return loaded
    except jsonschema.exceptions.ValidationError as e:
        # print(">>> Data's structure is invalid. Please, check your JSON file.Error:")
        # print(e.message)  # Ошибка валидацци будет выведена на экран
        click.echo(click.style(
            f">>> Data's structure is invalid. Please, check your JSON file. Error: {e.message}", fg="red"))

# def load_people(file_name):
#     """Загрузить всех людей из файла JSON."""
#     if os.path.exists(file_name):
#         with open(file_name, "r", encoding="utf-8") as fin:
#             return json.load(fin)
#     else:
#         return []


if __name__ == "__main__":
    cli()
