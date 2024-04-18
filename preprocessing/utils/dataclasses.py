#!/usr/bin/env python3

from dataclasses import dataclass, fields

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


@dataclass
class Dictionary:
    id: int
    name: str
    lang1: str
    lang2: str
    closed: bool = False
    is_ordered: bool = False
    author: str | None = None
    date_published: str | None = None
    isbn: str | None = None
    source: str | None = None

    def to_tsv_string(self):
        return dataclass_to_tsv_string(self)


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

