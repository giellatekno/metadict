export type User = {
    gh_fullname: string;
    gh_login_name: string;
    gh_avatar_url: string;
    restricted_dicts: boolean;
};

// NOTE: Maybe use a schema validation library like zod to verify json responses?
export type LookupResponse = [string, string, number, string, string][];
export type SearchResponse = string[];
export type ArticleResponse = string[];
export type NeighborsResponse = string[];
export type DictionaryResponse = [string, string, string, string][];
