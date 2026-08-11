#!/usr/bin/env python3

from dataclasses import dataclass, fields
from textwrap import dedent


def pyobj_to_psql_data(obj):
    if obj is None:
        return "\\N"
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, int):
        return str(obj)
    else:
        raise TypeError("unhandled type of obj", type(obj))


def dataclass_to_tsv_string(dcls_inst):
    strings = []
    for field in fields(dcls_inst):
        value = getattr(dcls_inst, field.name)
        stringified = pyobj_to_psql_data(value)
        strings.append(stringified)

    return "\t".join(strings)


def to_sqlval(val):
    if val is None:
        return "NULL"
    elif isinstance(val, str):
        # single quotes are escaped in SQL text by doubling them
        return "'" + val.replace("'", "''") + "'"
    elif isinstance(val, int):
        return str(val)
    else:
        # otherwise, quote the stringify item
        return "'" + str(val) + "'"


@dataclass
class Dictionary:
    id: int
    slug: str
    name: str
    lang1: str
    lang2: str
    displayname: str | None = None
    closed: bool = False
    is_ocr_read: bool = False
    is_historic: bool = False
    author: str | None = None
    date_published: str | None = None
    isbn: str | None = None
    source: str | None = None

    def to_tsv_string(self):
        return dataclass_to_tsv_string(self)

    def to_sql(self):
        return dedent(f"""
            INSERT INTO
            dictionaries (
                slug,
                name,
                lang1,
                lang2,
                displayname,
                closed,
                is_ocr_read,
                is_historic,
                author,
                date_published,
                isbn,
                source
            ) VALUES (
                {to_sqlval(self.slug)},
                {to_sqlval(self.name)},
                {to_sqlval(self.lang1)},
                {to_sqlval(self.lang2)},
                {to_sqlval(self.displayname)},
                {to_sqlval(self.closed)},
                {to_sqlval(self.is_ocr_read)},
                {to_sqlval(self.is_historic)},
                {to_sqlval(self.author)},
                {to_sqlval(self.date_published)},
                {to_sqlval(self.isbn)},
                {to_sqlval(self.source)}
            ) RETURNING id;""")


@dataclass
class Article:
    # id: int
    lemma: str
    dictionary: int
    rendered: str
    pos: str | None = None
    lang: str | None = None
    article_number: int | None = None
    additional_properties: str | None = None

    def to_tsv_string(self):
        return dataclass_to_tsv_string(self)

    def to_sql(self):
        # The $DICTIONARY$ will be replaced later
        return dedent(f"""
            (
                {to_sqlval(self.lemma)},
                $DICTIONARY$,
                {to_sqlval(self.rendered)},
                {to_sqlval(self.pos)},
                {to_sqlval(self.lang)},
                {to_sqlval(self.article_number)},
                {to_sqlval(self.additional_properties)}
            )""")
