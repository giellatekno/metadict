export type User = {
    gh_fullname: string;
    gh_login_name: string;
    gh_avatar_url: string;
    restricted_dicts: boolean;
};

export type DictionaryEntries = [string, string, number, string, string][];
