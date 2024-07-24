CREATE TABLE dictionaries (
    id SERIAL PRIMARY KEY,
    name text,

    -- is this flexible enough? could a dictionary have more than 1 source
    -- and/or target langs?
    lang1 text,
    lang2 text,

    -- Dictionary is closed to the public, and only logged in users can see
    -- contents from it
    closed boolean,

    -- Are the articles in the dictionary ordered, such that each article
    -- has a defined, numerical, id
    is_ordered boolean DEFAULT false,

    -- other info about the dictionary
    author text,
    -- publishing date
    date_published text,
    -- If the dictionary is published as a book, this is the ISBN number
    isbn text,
    -- What is the source?
    source text
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    lemma text,
    dictionary integer REFERENCES dictionaries (id),
    -- rendered html of the article data
    rendered text,
    pos text,
    lang text,
    -- internal ordering in the dictionary, may be NULL
    article_number integer,
    -- additional properties, e.g. algu number, korp reference
    additional_properties json
);


-- Previously used to load data into the database on creation.
-- We now use the insert_dictionaries.py script with the generated
-- .sql files found in preprocessing/ instead.

-- -- Generated data: Giellatekno dictionaries
-- COPY dictionaries FROM PROGRAM 
--     'gzip -cd /docker-entrypoint-initdb.d/data_dictionaries.txt';
-- 
-- -- Generated data: Articles from all giellatekno dictionaries
-- COPY articles(lemma, dictionary, rendered, pos, lang, article_number, additional_properties) FROM
--     PROGRAM
--     'gzip -cd /docker-entrypoint-initdb.d/data_articles.txt';
