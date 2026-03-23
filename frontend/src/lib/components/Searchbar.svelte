<script lang="ts">
    import { m } from "$lib/paraglide/messages.js";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";
    import { settings } from "$lib/settings.svelte";
    import { SearchIcon } from "lucide-svelte";
    import SearchOptions from "./SearchOptions.svelte";
    import KeyboardShortcuts from "./KeyboardShortcuts.svelte";

    let value = $state("");

    let searchbox_elem: HTMLInputElement;

    let search_param = $derived.by(() => {
        if (settings.selected_search_langs.every((l) => l.enabled))
            return "all";

        const active = settings.selected_search_langs
            .filter((l) => l.enabled)
            .map((l) => l.iso);
        return active.join(",") || "none";
    });

    onMount(() => {
        searchbox_elem.focus();
    });

    async function on_new_value(input: string) {
        if (input.trim() !== "") {
            await goto(
                resolve(
                    `/search/${search_param}/${encodeURIComponent(input.trim())}`,
                ),
                { keepFocus: true },
            );
        }
    }

    function on_enter_keydown(event: KeyboardEvent) {
        if (event.key !== "Enter") return;
        on_new_value(value);
    }

    function on_searchbutton_click() {
        on_new_value(value);
    }

    function handleKeydown(e: KeyboardEvent) {
        if (!(e.target instanceof HTMLInputElement)) {
            if (((e.metaKey || e.ctrlKey) && e.key === "k") || e.key == "/") {
                e.preventDefault();
                searchbox_elem.focus();
            }
        }
    }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="flex w-2xl flex-col gap-2">
    <div
        class="input-group preset-filled-tertiary-50-950 h-12 w-full grid-cols-[auto_1fr_auto] md:h-16 md:w-2xl"
    >
        <div class="ig-cell">
            <SearchIcon class="size-6" />
        </div>
        <input
            class="ig-input text-lg"
            type="search"
            placeholder={m.search_placeholder()}
            bind:this={searchbox_elem}
            bind:value
            onkeydown={on_enter_keydown}
        />
        <button
            class="ig-btn preset-filled-primary-500"
            onclick={on_searchbutton_click}
        >
            {m.search()}
        </button>
    </div>
    <div class="flex justify-between">
        <SearchOptions />
        <KeyboardShortcuts />
    </div>
</div>
