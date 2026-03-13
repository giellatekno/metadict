//! Database queries
//! All SQL is in this file.

use crate::Language;
use anyhow::Context;
use itertools::Itertools;
use postgres_types::ToSql;
use tokio_postgres::types::private::BytesMut;

fn can_see_closed_sql(can_see_closed: bool) -> &'static str {
    if can_see_closed {
        ""
    } else {
        " AND dictionaries.closed = FALSE "
    }
}

#[derive(Debug, serde::Serialize)]
pub struct SearchRow {
    lang: String,
    lemma: String,
}

impl From<tokio_postgres::Row> for SearchRow {
    fn from(row: tokio_postgres::Row) -> Self {
        Self {
            lang: row.get("lang"),
            lemma: row.get("lemma"),
        }
    }
}

fn vec_language_to_sql(v: &[Language]) -> String {
    let mut out = String::from("(");
    let lasti = v.len() - 1;
    let mut i = 0;
    for lang in v.iter() {
        out.push_str(&format!("'{lang}'"));
        if i != lasti {
            out.push(',');
        }
        i += 1;
    }
    out.push(')');
    out
}

/// SQL for the /search endpoint. It finds all `(lang, lemma)` pairs such that the `lang`
/// is in the list of input `langs`, and only those where the `(lang, lemma)` pair has
/// a translation to any language given in `l2s`.
pub async fn search(
    db: deadpool_postgres::Object,
    langs: &[Language],
    query: &str,
    l2s: &[Language],
    can_see_closed: bool,
) -> anyhow::Result<Vec<SearchRow>> {
    Ok(db
        .query(
            &format!(
                r#"
        SELECT DISTINCT
            articles.lang AS lang,
            articles.lemma AS lemma
        FROM
            articles
        INNER JOIN
            dictionaries
        ON
            articles.dictionary = dictionaries.id
        WHERE
            articles.lang = ANY($1)
            AND
            LOWER(lemma) LIKE LOWER($2)
            AND
            dictionaries.lang2 = ANY($3)
            {}
        ORDER BY 
            articles.lemma
    "#,
                can_see_closed_sql(can_see_closed)
            ),
            &[&langs, &query, &l2s],
        )
        .await
        .map_err(|e| anyhow::anyhow!(e))
        .context("Running search query")?
        .into_iter()
        .map(SearchRow::from)
        .collect())
}

#[derive(serde::Serialize)]
pub struct Article {
    lemma: String,
    dictionary_name: String,
    article_id: i32,
    lang1: Language,
    lang2: Language,
    date_published: String,
    is_historic: bool,
    is_ocr_read: bool,
}

impl From<tokio_postgres::Row> for Article {
    fn from(row: tokio_postgres::Row) -> Self {
        Self {
            lemma: row.get("lemma"),
            dictionary_name: row.get("dictionary_name"),
            article_id: row.get("article_id"),
            lang1: row
                .get::<&str, String>("lang1")
                .parse()
                .expect("rust source code knows all language codes in database"),
            lang2: row
                .get::<&str, String>("lang2")
                .parse()
                .expect("rust source code knows all language codes in database"),
            date_published: row.get("date_published"),
            is_historic: row.get("is_historic"),
            is_ocr_read: row.get("is_ocr_read"),
        }
    }
}

pub async fn find_articles_for_lemma(
    db: deadpool_postgres::Object,
    langs: &[Language],
    lemma: &str,
    l2s: &[Language],
    can_see_closed: bool,
) -> anyhow::Result<Vec<Article>> {
    Ok(db
        .query(
            &format!(
                r#"
            SELECT
                articles.lemma AS lemma,
                dictionaries.name AS dictionary_name,
                articles.id AS article_id,
                dictionaries.lang1 AS lang1,
                dictionaries.lang2 AS lang2,
                COALESCE(dictionaries.date_published, '') AS date_published,
                dictionaries.is_historic AS is_historic,
                dictionaries.is_ocr_read AS is_ocr_read
            FROM
                articles
            INNER JOIN
                dictionaries
            ON
                articles.dictionary = dictionaries.id
            WHERE
                lang = ANY ($1)
                AND
                lemma LIKE $2
                AND
                dictionaries.lang2 = ANY ($3)
                {}
            ORDER BY 
                dictionaries.name, articles.id
        "#,
                can_see_closed_sql(can_see_closed)
            ),
            &[&langs, &lemma, &l2s],
        )
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .into_iter()
        .map(Article::from)
        .collect())
}

#[derive(serde::Serialize)]
pub struct FindArticleByIdRow {
    rendered: String,
    article_number: i32,
}

impl From<tokio_postgres::Row> for FindArticleByIdRow {
    fn from(row: tokio_postgres::Row) -> Self {
        Self {
            rendered: row.get("rendered"),
            article_number: row.get("article_number"),
        }
    }
}

pub async fn find_article_by_id(
    db: deadpool_postgres::Object,
    id: i32,
    can_see_closed: bool,
) -> anyhow::Result<FindArticleByIdRow> {
    Ok(db
        .query_one(
            &format!(
                r#"
            SELECT
                articles.rendered AS rendered,
                articles.article_number AS article_number
            FROM
                articles
            INNER JOIN
                dictionaries
            ON
                articles.dictionary = dictionaries.id
            WHERE
                articles.id = $1
                {}
        "#,
                can_see_closed_sql(can_see_closed)
            ),
            &[&id],
        )
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .into())
}

#[derive(serde::Serialize)]
pub struct NeighborRow {
    article_number: i32,
    rendered: String,
}

impl From<tokio_postgres::Row> for NeighborRow {
    fn from(row: tokio_postgres::Row) -> Self {
        Self {
            article_number: row.get("article_number"),
            rendered: row.get("rendered"),
        }
    }
}

pub async fn find_neighboring_articles(
    db: deadpool_postgres::Object,
    id: i32,
    can_see_closed: bool,
) -> anyhow::Result<Vec<NeighborRow>> {
    Ok(db
        .query(
            &format!(
                r#"
        SELECT
            articles.article_number AS article_number,
            articles.rendered AS rendered
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
            {}
        ORDER BY
            articles.article_number
    "#,
                can_see_closed_sql(can_see_closed)
            ),
            &[&id],
        )
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .into_iter()
        .map(NeighborRow::from)
        .dedup_by(|a, b| a.rendered == b.rendered)
        .collect())
}

#[derive(serde::Serialize)]
pub struct DictionaryRow {
    name: String,
    author: String,
    date_published: String,
    isbn: String,
    is_historic: bool,
    is_ocr_read: bool,
}

impl From<tokio_postgres::Row> for DictionaryRow {
    fn from(row: tokio_postgres::Row) -> Self {
        Self {
            name: row.get("name"),
            author: row.get("author"),
            date_published: row.get("date_published"),
            isbn: row.get("isbn"),
            is_historic: row.get("is_historic"),
            is_ocr_read: row.get("is_ocr_read"),
        }
    }
}

pub async fn find_dictionary_by_article_id(
    db: deadpool_postgres::Object,
    id: i32,
    can_see_closed: bool,
) -> anyhow::Result<DictionaryRow> {
    db.query_one(
        &format!(
            r#"
        SELECT
            name AS name,
            COALESCE(author, '') AS author,
            COALESCE(date_published, '') AS date_published,
            COALESCE(isbn, '') AS isbn,
            is_historic AS is_historic,
            is_ocr_read AS is_ocr_read
        FROM
            dictionaries,
            (SELECT dictionary FROM articles WHERE id = $1)
        WHERE
            id = dictionary
            {}
    "#,
            can_see_closed_sql(can_see_closed)
        ),
        &[&id],
    )
    .await
    .map_err(|e| anyhow::anyhow!(e))
    .map(DictionaryRow::from)
}
