CREATE TABLE dictionaries (
    id SERIAL PRIMARY KEY,
    name text,

    -- is this flexible enough? could a dictionary have more than 1 source
    -- and/or target langs?
    lang1 text,
    lang2 text,

    -- Are the articles in the dictionary ordered, such that each article
    -- has a defined, numerical, id
    is_ordered boolean DEFAULT false,

    -- other info about the dictionary
    author text
    -- publishing date
    date_published text,
    -- If the dictionary is published as a book, this is the ISBN number
    isbn text,
    -- What is the source?
    source text,
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    lemma text,
    pos text,
    lang text,
    dictionary integer REFERENCES dictionaries (id),
    -- internal ordering in the dictionary, may be NULL
    article_number integer,
    -- additional properties, e.g. algu number, korp reference
    additional_properties json,
    -- rendered html of the article data
    rendered text
);


-- Generated data: Giellatekno dictionaries
COPY dictionaries (name, lang1, lang2, author) FROM
    '/docker-entrypoint-initdb.d/data_dictionaries.txt';

-- Generated data: Articles from all giellatekno dictionaries
COPY articles (lemma, pos, lang, dictionary) FROM
    '/docker-entrypoint-initdb.d/data_articles.txt';
