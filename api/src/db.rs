//! Database queries
//! All SQL is in this file.

use anyhow::{Context, Ok};
use tracing::debug;

pub async fn find_lemmas(
    db: deadpool_postgres::Object,
    lang: &str,
    query: &str,
    can_see_closed: bool,
) -> anyhow::Result<Vec<String>> {
    // TODO perf: prepared statement cache?
    // TODO injection safe?
    debug!(can_see_closed = can_see_closed, "find_lemmas()");

    let statement = if can_see_closed {
        r#"
        SELECT DISTINCT
            articles.lemma
        FROM
            articles
        WHERE
            articles.lang = $1
            AND
            articles.lemma LIKE $2
        ;
    "#
    } else {
        r#"
        SELECT DISTINCT
            articles.lemma
        FROM
            articles
        INNER JOIN
            dictionaries
        ON
            articles.dictionary = dictionaries.id
        WHERE
            lang = $1
            AND
            lemma LIKE $2
            AND
            dictionaries.closed = FALSE
        ;
    "#
    };

    Ok(db
        .query(statement, &[&lang, &query])
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .iter()
        .map(|row| {
            // tuple of row.get(index), but have to tell which type for each
            // column (and a (or the) correct rust type that the postgres type
            // can be converted into. E.g. if field N had pg type TEXT, then
            // it could not be converted to f32, but it can be converted to &str.
            row.get::<usize, String>(0)
        })
        .collect::<Vec<String>>())
}

pub async fn find_articles_for_lemma(
    db: deadpool_postgres::Object,
    lang: &str,
    lemma: &str,
    can_see_closed: bool,
) -> anyhow::Result<Vec<(String, String, i32, String)>> {
    // TODO injection safe?
    let statement = if can_see_closed {
        r#"
            SELECT
                articles.lemma,
                dictionaries.name,
                articles.id,
                dictionaries.lang2
            FROM
                articles
            INNER JOIN
                dictionaries
            ON
                articles.dictionary = dictionaries.id
            WHERE
                lang = $1
                AND
                lemma LIKE $2
            ;
        "#
    } else {
        r#"
            SELECT
                articles.lemma,
                dictionaries.name,
                articles.id,
                dictionaries.lang2
            FROM
                articles
            INNER JOIN
                dictionaries
            ON
                articles.dictionary = dictionaries.id
            WHERE
                lang = $1
                AND
                lemma LIKE $2
                AND
                dictionaries.closed = FALSE
            ;
        "#
    };

    Ok(db
        .query(statement, &[&lang, &lemma])
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .iter()
        .map(|row| {
            (
                row.get::<usize, String>(0),
                row.get::<usize, String>(1),
                row.get::<usize, i32>(2),
                row.get::<usize, String>(3),
            )
        })
        .collect::<Vec<_>>())
}

pub async fn find_article_by_id(
    db: deadpool_postgres::Object,
    id: i32,
    can_see_closed: bool,
) -> anyhow::Result<Vec<String>> {
    let statement = if can_see_closed {
        "SELECT rendered FROM articles WHERE id = $1;"
    } else {
        r#"
            SELECT
                articles.rendered
            FROM
                articles
            INNER JOIN
                dictionaries
            ON
                articles.dictionary = dictionaries.id
            WHERE
                articles.id = $1
                AND
                dictionaries.closed = FALSE
        "#
    };

    Ok(db
        .query(statement, &[&id])
        .await
        .map_err(|e| anyhow::anyhow!(e))
        .with_context(|| "running find_article_by_id query against db")?
        .iter()
        .map(|row| row.get::<usize, String>(0))
        .collect::<Vec<_>>())
}

pub async fn find_neighboring_articles(
    db: deadpool_postgres::Object,
    id: i32,
    can_see_closed: bool,
) -> anyhow::Result<Vec<String>> {
    let statement = if can_see_closed {
        r#"
            SELECT
                articles.rendered 
            FROM 
                articles, 
                (SELECT 
                    article_number, dictionary 
                FROM 
                    articles 
                WHERE 
                    id = $1) lemma 
            WHERE 
                articles.dictionary = lemma.dictionary 
                AND 
                articles.article_number BETWEEN lemma.article_number-5 AND lemma.article_number+5 
            ORDER BY 
                articles.article_number;
        "#
    } else {
        r#"
            SELECT
                articles.rendered 
            FROM 
                articles INNER JOIN dictionaries 
                ON articles.dictionary = dictionaries.id, 
                (SELECT 
                    article_number, dictionary 
                FROM 
                    articles 
                WHERE 
                    id = $1) lemma 
            WHERE 
            articles.dictionary = lemma.dictionary 
            AND 
            articles.article_number BETWEEN lemma.article_number-5 AND lemma.article_number+5 
            AND 
            dictionaries.closed = FALSE;
        "#
    };

    let mut result = db
        .query(statement, &[&id])
        .await
        .map_err(|e| anyhow::anyhow!(e))
        .with_context(|| "running find_neighboring_articles query against db")?
        .iter()
        .map(|row| row.get::<usize, String>(0))
        .collect::<Vec<_>>();

    result.dedup();
    Ok(result)
}
