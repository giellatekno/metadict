<script lang="ts">
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages.js";
    import { langname } from "$lib/langname";
    import { onMount } from "svelte";
    import { EllipsisIcon, SearchIcon, XIcon } from "lucide-svelte";
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";
    import { Dialog, Portal } from "@skeletonlabs/skeleton-svelte";
    import { saveSettings, settings } from "$lib/settings.svelte";
    import { SEARCH_LANGS, TARGET_LANGS } from "$lib/utils";
    import { browser } from "$app/environment";

    let value = $state("");

    let searchbox_elem: HTMLInputElement;

    let search_param: string = $derived.by(() => {
        if (Object.values(settings.selected_search_langs).every(Boolean))
            return "all";
        return Object.entries(settings.selected_search_langs)
            .filter(([_, v]) => v === true)
            .map(([k, _]) => k)
            .join(",");
    });

    onMount(() => {
        searchbox_elem.focus();
    });

    async function on_new_value(input: string) {
        await goto(
            resolve(`/search/${search_param}/${encodeURIComponent(input)}`),
            { keepFocus: true },
        );
    }

    function on_enter_keydown(event: KeyboardEvent) {
        if (event.key !== "Enter" || value === "") return;
        on_new_value(value);
        searchbox_elem.focus();
    }

    function on_searchbutton_click() {
        if (value === "") return;
        on_new_value(value);
        searchbox_elem.focus();
    }

    function toggleSearchLang(lang: string) {
        if (Object.keys(settings.selected_search_langs).includes(lang)) {
            settings.selected_search_langs[lang] =
                !settings.selected_search_langs[lang];
        }
        saveSettings();
    }

    function toggleTargetLang(lang: string) {
        if (Object.keys(settings.selected_target_langs).includes(lang)) {
            settings.selected_target_langs[lang] =
                !settings.selected_target_langs[lang];
        }
        saveSettings();
    }

    const isMac = $derived.by(() => {
        const ua = browser ? window.navigator.userAgent : "";
        return ua ? ua.includes("Mac") : false;
    });

    function on_ctrl_k(e: KeyboardEvent) {
        if (isMac) {
            if (e.metaKey && e.key === "k") {
                e.preventDefault();
                searchbox_elem.focus();
            }
        } else {
            if (e.ctrlKey && e.key === "k") {
                e.preventDefault();
                searchbox_elem.focus();
            }
        }
    }
    // animation for search settings dialig
    const animation =
        "transition transition-discrete opacity-0 translate-y-[100px] starting:data-[state=open]:opacity-0 starting:data-[state=open]:translate-y-[100px] data-[state=open]:opacity-100 data-[state=open]:translate-y-0";
</script>

<svelte:window onkeydown={on_ctrl_k} />

<div class="flex w-2xl flex-col gap-2">
    <div>
        <span class="flex items-center gap-1 opacity-80">
            {m.search_goto_1()}
            {#if isMac}
                <kbd class="kbd preset-filled-surface-300-700">⌘</kbd>
            {:else}
                <kbd class="kbd preset-filled-surface-300-700">ctrl</kbd>
            {/if}
            +
            <kbd class="kbd preset-filled-surface-300-700">K</kbd>
            {m.search_goto_2()}
        </span>
    </div>
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
    <div class="flex flex-col">
        <Dialog>
            <Dialog.Trigger
                class="preset-filled-surface-200-800 hover:preset-filled-surface-100-900 border-surface-200-800 flex items-center justify-between rounded-lg border px-4 py-2"
            >
                <span class="font-bold">SEARCH OPTIONS</span>
                <EllipsisIcon class="size-4" />
            </Dialog.Trigger>
            <Portal>
                <Dialog.Backdrop
                    class="bg-surface-50-950/50 fixed inset-0 z-50"
                />
                <Dialog.Positioner
                    class="fixed inset-0 z-50 flex items-center justify-center p-4"
                >
                    <Dialog.Content
                        class="card bg-tertiary-50-950 border-primary-500 w-full max-w-xl space-y-4 border-2 p-6 shadow-xl {animation}"
                    >
                        <header class="flex items-center justify-between">
                            <Dialog.Title class="h4 font-bold">
                                {m.search_options()}
                            </Dialog.Title>
                            <Dialog.CloseTrigger
                                class="hover:preset-tonal box-content rounded-md p-2"
                                title="Close"
                                aria-label="Close"
                            >
                                <XIcon class="size-6" />
                            </Dialog.CloseTrigger>
                        </header>
                        <Dialog.Description>
                            <div class="align-start grid grid-cols-2 gap-6">
                                <div class="flex flex-col gap-2">
                                    <span class="text-lg font-bold">
                                        {m.search_languages()}
                                    </span>
                                    <hr class="hr" />
                                    <div class="flex flex-col gap-2">
                                        {#each SEARCH_LANGS as iso}
                                            <button
                                                class="btn hover:preset-tonal flex justify-start"
                                                onclick={() =>
                                                    toggleSearchLang(iso)}
                                            >
                                                <input
                                                    class="checkbox"
                                                    type="checkbox"
                                                    bind:checked={
                                                        settings
                                                            .selected_search_langs[
                                                            iso
                                                        ]
                                                    }
                                                />
                                                <p>
                                                    {langname(iso, getLocale())}
                                                </p>
                                            </button>
                                        {/each}
                                    </div>
                                </div>
                                <div class="flex flex-col gap-2">
                                    <span class="text-lg font-bold">
                                        {m.target_languages()}
                                    </span>
                                    <hr class="hr" />
                                    <div class="flex flex-col gap-2">
                                        {#each TARGET_LANGS as iso}
                                            {#if iso !== "hst" && iso !== "ext"}
                                                <button
                                                    class="btn hover:preset-tonal flex justify-start"
                                                    onclick={() =>
                                                        toggleTargetLang(iso)}
                                                >
                                                    <input
                                                        class="checkbox"
                                                        type="checkbox"
                                                        bind:checked={
                                                            settings
                                                                .selected_target_langs[
                                                                iso
                                                            ]
                                                        }
                                                    />
                                                    <p>
                                                        {langname(
                                                            iso,
                                                            getLocale(),
                                                        )}
                                                    </p>
                                                </button>
                                            {/if}
                                        {/each}
                                        <button
                                            class="btn hover:preset-tonal flex justify-start"
                                            onclick={() =>
                                                toggleTargetLang("hst")}
                                        >
                                            <input
                                                class="checkbox"
                                                type="checkbox"
                                                bind:checked={
                                                    settings
                                                        .selected_target_langs[
                                                        "hst"
                                                    ]
                                                }
                                            />
                                            <p>{m.historical_dictionaries()}</p>
                                        </button>
                                        <button
                                            class="btn hover:preset-tonal flex justify-start"
                                            onclick={() =>
                                                toggleTargetLang("ext")}
                                        >
                                            <input
                                                class="checkbox"
                                                type="checkbox"
                                                bind:checked={
                                                    settings
                                                        .selected_target_langs[
                                                        "ext"
                                                    ]
                                                }
                                            />
                                            <p>{m.external_dictionaries()}</p>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </Dialog.Description>
                    </Dialog.Content>
                </Dialog.Positioner>
            </Portal>
        </Dialog>
    </div>
</div>
