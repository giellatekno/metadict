import { browser } from "$app/environment";
import { SEARCH_OBJ, TARGET_OBJ } from "./utils";

interface SearchSettings {
    selected_search_langs: Record<string, boolean>;
    selected_target_langs: Record<string, boolean>;
}

const STORAGE_KEY = "user-search-settings";
const defaultValue: SearchSettings = {
    selected_search_langs: SEARCH_OBJ,
    selected_target_langs: TARGET_OBJ,
};

const saved = browser ? localStorage.getItem(STORAGE_KEY) : null;
const initial = saved ? JSON.parse(saved) : defaultValue;

export const settings = $state<SearchSettings>(initial);

export function saveSettings() {
    if (browser) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    }
}
