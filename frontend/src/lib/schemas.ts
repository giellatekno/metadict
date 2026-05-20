import * as z from "zod";

export const User = z.object({
    gh_fullname: z.string(),
    gh_login_name: z.string(),
    gh_avatar_url: z.string(),
    restricted_dicts: z.boolean(),
});

export const LookupResponse = z.array(
    z.object({
        article_id: z.number(),
        date_published: z.string(),
        dictionary_name: z.string(),
        dictionary_displayname: z.string(),
        is_historic: z.boolean(),
        is_ocr_read: z.boolean(),
        lang1: z.string(),
        lang2: z.string(),
        lemma: z.string(),
    }),
);

export const SearchResponse = z.array(
    z.object({
        lang: z.string(),
        lemma: z.string(),
    }),
);

export const ArticleResponse = z.object({
    article: z.object({
        article_number: z.number(),
        rendered: z.string(),
    }),
    dictionary_info: z.object({
        author: z.string(),
        date_published: z.string(),
        is_historic: z.boolean(),
        is_ocr_read: z.boolean(),
        isbn: z.string(),
        name: z.string(),
    }),
    neighbors: z.array(
        z.object({
            article_number: z.number(),
            rendered: z.string(),
        }),
    ),
});

export type UserType = z.infer<typeof User>;
export type LookupType = z.infer<typeof LookupResponse>;
export type SearchType = z.infer<typeof SearchResponse>;
export type ArticleType = z.infer<typeof ArticleResponse>;
