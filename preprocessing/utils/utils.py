import os.path
from utils.dataclasses import Article, Dictionary

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
    '{dictionary.author}',
    '{dictionary.date_published}',
    '{dictionary.isbn}',
    '{dictionary.source}'
    );"""
    
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
        sql_statement += f"('{article.lemma}', $DICTIONARY$, '{article.rendered}', '{article.pos}', '{article.lang}', '{article.article_number}', '{article.additional_properties}'),\n"
    
    sql_statement = sql_statement[:-2] + ";"

    with open(f"sql_files/a-{filename}.sql", "w") as f:
        f.write(sql_statement)