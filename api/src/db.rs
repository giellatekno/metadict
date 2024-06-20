//! Database queries
//! All SQL is in this file.

pub async fn find_lemmas(
    db: deadpool_postgres::Object,
    lang: &str,
    query: &str,
    can_see_closed: bool,
) -> anyhow::Result<Vec<String>> {
    // TODO prepared statement cache? Is that a thing?
    //let statement = match client.prepare(sql_query).await {
    //    Ok(statement) => statement,
    //    Err(e) => return format!("{}", e).into_response(),
    //};
    // TODO It could be possible that a lemma is only defined in a closed
    // dictionary, and in that case, we don't want to show that lemma at all
    // to a user who can't see closed dictionaries.
    // TODO is this injection safe?
    let statement = if can_see_closed {
        r#"
        SELECT DISTINCT
            articles.lemma
        FROM
            articles
        WHERE
            lang = $1
            AND
            lemma LIKE $2
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
) -> anyhow::Result<Vec<(String, String, i32)>> {
    // TODO is this injection safe?
    let statement = if can_see_closed {
        r#"
            SELECT
                articles.lemma,
                dictionaries.name,
                articles.id
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
                articles.id
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
            )
        })
        .collect::<Vec<_>>())
}

pub async fn find_article_by_id(
    db: deadpool_postgres::Object,
    id: i32,
    can_see_closed: bool,
) -> anyhow::Result<Vec<String>> {
    // TODO: Validate jwt, so it requires login to see closed articles!
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
                dicitionares.closed = FALSE
        "#
    };
    Ok(db
        .query(statement, &[&id])
        .await
        .map_err(|e| anyhow::anyhow!(e))?
        .iter()
        .map(|row| row.get::<usize, String>(0))
        .collect::<Vec<_>>())
}
