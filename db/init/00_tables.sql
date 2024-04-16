-- An "article" is a

CREATE TABLE dictionaries (
    id SERIAL PRIMARY KEY,
    name text,

    -- is this flexible enough? could a dictionary have more target langs?
    lang1 text,
    lang2 text,
    author text
    -- other info about the dictionary
);

COPY dictionaries (name, lang1, lang2, author) FROM
    '/docker-entrypoint-initdb.d/data_dictionaries.txt';

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    lemma text,
    pos text,

    -- language
    lang text,
    dictionary integer REFERENCES dictionaries (id),

    -- rendered html of the article data
    rendered text
);

COPY articles (lemma, pos, lang, dictionary) FROM
    '/docker-entrypoint-initdb.d/data_articles.txt';
