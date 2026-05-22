import { browser } from "$app/environment";
import { SEARCH_OPTIONS, TARGET_OPTIONS } from "./utils";

export interface LangConfig {
    iso: string;
    enabled: boolean;
}

interface SearchSettings {
    selected_search_langs: LangConfig[];
    selected_target_langs: LangConfig[];
}

const STORAGE_KEY = "user-search-settings";

function reconcile(defaultOptions: string[], savedConfigs: LangConfig[]) {
    if (!savedConfigs || !Array.isArray(savedConfigs)) {
        return defaultOptions.map((iso) => ({ iso, enabled: true }));
    }

    const validSaved = savedConfigs.filter((s) => defaultOptions.includes(s.iso));

    defaultOptions.forEach((iso) => {
        if (!validSaved.find((s) => s.iso === iso)) {
            validSaved.push({ iso, enabled: true });
        }
    });

    return validSaved;
}

function getInitialSettings(): SearchSettings {
    const raw = browser ? localStorage.getItem(STORAGE_KEY) : null;
    let parsed = null;

    try {
        parsed = raw ? JSON.parse(raw) : null;
    } catch {
        parsed = null;
    }

    return {
        selected_search_langs: reconcile(SEARCH_OPTIONS, parsed?.selected_search_langs),
        selected_target_langs: reconcile(TARGET_OPTIONS, parsed?.selected_target_langs),
    };
}
export const settings = $state<SearchSettings>(getInitialSettings());

if (browser) {
    $effect.root(() => {
        $effect(() => {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
        });
    });
}
