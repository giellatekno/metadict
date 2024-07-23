import os.path
from utils.dataclasses import Article, Dictionary
import re

def get_gut_root():
    app_toml_path = os.path.expanduser("~/.config/gut/app.toml")
    with open(app_toml_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            try:
                k, v = line.split("=", maxsplit=1)
            except IndexError:
                continue
            k = k.strip()
            v = v.strip()
            if k != "root":
                continue

            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]

            return v


def dictionary_to_sql(dictionary: Dictionary, filename):
    sql_statement = f"""INSERT INTO 
    dictionaries (
        name,
        lang1,
        lang2,
        closed,
        is_ordered,
        author,
        date_published,
        isbn,
        source
    ) VALUES (
    '{dictionary.name}',
    '{dictionary.lang1}',
    '{dictionary.lang2}',
    {dictionary.closed},
    {dictionary.is_ordered},
    {f"'{dictionary.author}'" if dictionary.author else "NULL"},
    {f"'{dictionary.date_published}'" if dictionary.date_published else "NULL"},
    {f"'{dictionary.isbn}'" if dictionary.isbn else "NULL"},
    {f"'{dictionary.source}'" if dictionary.source else "NULL"}
    ) RETURNING id;"""

    with open(f"sql_files/d-{filename}.sql", "w") as f:
        f.write(sql_statement)

def articles_to_sql(articles:list[Article], filename):
    sql_statement = """INSERT INTO
    articles (
    lemma,
    dictionary,
    rendered,
    pos,
    lang,
    article_number,
    additional_properties
    ) VALUES """

    for article in articles:
        # Single quotes are escaped by doubeling them up in SQL
        sql_statement += f"""('{article.lemma.replace("'", "''")}',
        $DICTIONARY$,
        '{article.rendered.replace("'", "''")}',
        {f"'{article.pos}'" if article.pos else "NULL"},
        {f"'{article.lang}'" if article.lang else "NULL"},
        {article.article_number if article.article_number else "NULL"},
        {f"'{article.additional_properties}'" if article.additional_properties else "NULL"}),
        """

    last_comma = sql_statement.rfind(",")
    sql_statement = sql_statement[:last_comma] + ";"

    with open(f"sql_files/a-{filename}.sql", "w") as f:
        f.write(sql_statement)
