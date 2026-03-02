import * as z from "zod";

export const User = z.object({
    gh_fullname: z.string(),
    gh_login_name: z.string(),
    gh_avatar_url: z.string(),
    restricted_dicts: z.boolean(),
});

export const LookupResponse = z.array(
    z.tuple([z.string(), z.string(), z.number(), z.string(), z.string()]),
);

export const SearchResponse = z.string().array();

export const ArticleResponse = z.string().array();

export const NeighborsResponse = z.string().array();

export const DictionaryResponse = z.array(
    z.tuple([z.string(), z.string(), z.string(), z.string()]),
);

export type UserType = z.infer<typeof User>;
export type LookupType = z.infer<typeof LookupResponse>;
export type SearchType = z.infer<typeof SearchResponse>;
export type ArticleType = z.infer<typeof ArticleResponse>;
export type DictionaryType = z.infer<typeof DictionaryResponse>;
