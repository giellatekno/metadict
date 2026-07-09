<script lang="ts">
    import type { PageProps } from "./$types";
    import { m } from "$lib/paraglide/messages";
    import { langname } from "@giellatekno/langnames";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import SearchResultsTable from "$lib/components/SearchResultsTable.svelte";

    const locale = getLocale();

    let { data }: PageProps = $props();

    let allLemmas = $derived(data.lemmas ?? []);

    // Languages actually present in the result set (for the language filter)
    let langsPresent = $derived([...new Set(allLemmas.map((l) => l.lang))].sort());

    // --- filter state ---
    let filterText = $state("");
    let langFilter = $state("all");
    let pageSize = $state(20);

    let filtered = $derived.by(() => {
        const needle = filterText.trim().toLowerCase();
        return allLemmas.filter((l) => {
            if (langFilter !== "all" && l.lang !== langFilter) return false;
            if (needle && !l.lemma.toLowerCase().includes(needle)) return false;
            return true;
        });
    });
</script>

<div class="flex w-full flex-col items-center gap-4 sm:w-2/3 sm:min-w-124 xl:w-1/2">
    {#if allLemmas.length > 0}
        <!-- toolbar: result count, filter, language filter, hits per page -->
        <div class="flex w-full flex-wrap items-center gap-3">
            <div class="text-nowrap">
                {m.search_hits({ count: filtered.length })}
            </div>

            <input
                type="text"
                class="input min-w-40 flex-1"
                placeholder={m.search_filter_placeholder()}
                bind:value={filterText}
            />

            <select name="lang-filter" class="select w-fit" bind:value={langFilter}>
                <option value="all">{m.search_all_languages()}</option>
                {#each langsPresent as lang}
                    <option value={lang}>{langname(lang, locale)}</option>
                {/each}
            </select>

            <div class="flex flex-row items-center gap-2">
                <label for="hits-per-page">{m.search_hits_per_page()}</label>
                <select
                    name="hits-per-page"
                    class="select w-fit"
                    value={String(pageSize)}
                    onchange={(e) => (pageSize = Number(e.currentTarget.value))}
                >
                    <option value="20">20</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                </select>
            </div>
        </div>

        {#if filtered.length > 0}
            <SearchResultsTable lemmas={filtered} {pageSize} />
        {:else}
            <span class="text-lg">{m.search_no_filtered_results()}</span>
        {/if}
    {:else}
        <span class="text-lg">{m.search_no_results()}</span>
    {/if}
</div>
