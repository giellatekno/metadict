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

    -- this dictionary is OCR Read, useful to inform users that it may not
    -- be 100% accurate
    is_ocr_read boolean,

    -- this dictionary is considered "historic", which makes it appear in
    -- the "historic" section on the left menu. what makes a dictionary
    -- "historic" is different for each source language (lang1), e.g.
    -- for sme, it's dictionaries published before 1979
    is_historic boolean,

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
    -- internal ordering in the dictionary. source dictionaries without
    -- a defined ordering will be alphabetizised
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
