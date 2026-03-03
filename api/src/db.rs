//! Database queries
//! All SQL is in this file.

use anyhow::{Context, Ok};

pub async fn find_lemmas(
    db: deadpool_postgres::Object,
    lang: &str,
    query: &str,
    l2: Option<&[crate::Language]>,
    can_see_closed: bool,
) -> anyhow::Result<Vec<String>> {
    // TODO perf: prepared statement cache?
    // TODO injection safe?
    use itertools::Itertools;
    let can_see_closed = if !can_see_closed {
        " AND dictionaries.closed = FALSE "
    } else {
        ""
    };
    let lang2_filter = match l2 {
        Some(langs) => {
            langs
                .into_iter()
                .map(|lang| format!("'{lang}'"))
                .intersperse(String::from(","))
                .collect()
        }
        None => crate::LANGUAGES_STR_QUOTED_COMMA_SEPARATED.to_string(),
    };
    let statement = format!(r#"
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
            LOWER(lemma) LIKE LOWER($2)
            {can_see_closed}
            AND
            dictionaries.lang2 IN ({lang2_filter})
        ORDER BY 
            articles.lemma
    "#);

    Ok(db
        .query(&statement, &[&lang, &query])
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

#[derive(serde::Serialize)]
pub struct Article {
    lemma: String,
    dictionary_name: String,
    article_id: i32,
    lang2: crate::Language,
    date_published: String,
}

pub async fn find_articles_for_lemma(
    db: deadpool_postgres::Object,
    lang: &str,
    lemma: &str,
    can_see_closed: bool,
) -> anyhow::Result<Vec<Article>> {
    // TODO injection safe?
    let statement = if can_see_closed {
        r#"
            SELECT
                articles.lemma,
                dictionaries.name,
                articles.id,
                dictionaries.lang2,
                COALESCE(dictionaries.date_published, '')
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
            ORDER BY 
                dictionaries.name, articles.id
            ;
        "#
    } else {
        r#"
            SELECT
                articles.lemma,
                dictionaries.name,
                articles.id,
                dictionaries.lang2,
                COALESCE(dictionaries.date_published, '')
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
            ORDER BY 
                dictionaries.name, articles.id
            ;
        "#
    };

    Ok(db
        .query(statement, &[&lang, &lemma])
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .iter()
        .map(|row| {
            Article {
                lemma: row.get::<usize, String>(0),
                dictionary_name: row.get::<usize, String>(1),
                article_id: row.get::<usize, i32>(2),
                lang2: row.get::<usize, String>(3).parse()
                    .expect("language in database not in code"),
                date_published: row.get::<usize, String>(4),
            }
        })
        .collect::<Vec<Article>>())
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
                dictionaries.closed = FALSE
            ORDER BY
                articles.article_number;
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

pub async fn find_dictionary_by_article_id(
    db: deadpool_postgres::Object,
    id: i32,
    can_see_closed: bool,
) -> anyhow::Result<Vec<(String, String, String, String)>> {
    let statement = if can_see_closed {
        r#"
            SELECT 
                name, COALESCE(author, ''), COALESCE(date_published, ''), COALESCE(isbn, '') 
            FROM 
                dictionaries,
                (SELECT dictionary FROM articles WHERE id = $1) 
            WHERE 
                id = dictionary;
        "#
    } else {
        r#"
            SELECT 
                name, COALESCE(author, ''), COALESCE(date_published, ''), COALESCE(isbn, '') 
            FROM 
                dictionaries,
                (SELECT dictionary FROM articles WHERE id = $1) 
            WHERE 
                id = dictionary
                AND
                closed = FALSE;
        "#
    };

    Ok(db
        .query(statement, &[&id])
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .iter()
        .map(|row| {
            (
                row.get::<usize, String>(0),
                row.get::<usize, String>(1),
                row.get::<usize, String>(2),
                row.get::<usize, String>(3),
            )
        })
        .collect::<Vec<_>>())
}
