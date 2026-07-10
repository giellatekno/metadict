<script lang="ts">
    import { resolve } from "$app/paths";
    import { goto } from "$app/navigation";
    import { Pagination } from "@skeletonlabs/skeleton-svelte";
    import {
        ArrowLeftIcon,
        ArrowRightIcon,
        ChevronsUpDownIcon,
        ChevronUpIcon,
        ChevronDownIcon,
    } from "@lucide/svelte";
    import { m } from "$lib/paraglide/messages";
    import { langname } from "@giellatekno/langnames";
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { LANG_COLORS } from "$lib/utils";
    import type { SearchType } from "$lib/schemas";

    const locale = getLocale();

    type ColKey = "lemma" | "lang";
    type SortDir = "asc" | "desc";

    let { lemmas, pageSize }: { lemmas: SearchType; pageSize: number } = $props();

    const columns: ColKey[] = ["lemma", "lang"];

    function columnLabel(col: ColKey) {
        return col === "lemma" ? m.search_column_lemma() : m.search_column_language();
    }

    // Sorting
    let sortKey = $state<ColKey>("lemma");
    let sortDir = $state<SortDir>("asc");

    function toggleSort(col: ColKey) {
        if (sortKey === col) {
            sortDir = sortDir === "asc" ? "desc" : "asc";
        } else {
            sortKey = col;
            sortDir = "asc";
        }
    }

    let sorted = $derived.by(() => {
        const dir = sortDir === "asc" ? 1 : -1;
        return [...lemmas].sort((a, b) => a[sortKey].localeCompare(b[sortKey]) * dir);
    });

    // Pagination
    let page = $state(1);
    let n_results = $derived(sorted.length);
    let n_pages = $derived(Math.max(1, Math.ceil(n_results / pageSize)));

    // Reset to first page whenever the visible set changes
    $effect(() => {
        lemmas;
        sortKey;
        sortDir;
        pageSize;
        page = 1;
    });

    // Clamp page if the result set shrinks below the current page
    $effect(() => {
        if (page > n_pages) page = n_pages;
    });

    let start = $derived((page - 1) * pageSize);
    let end = $derived(start + pageSize);
    let shownLemmas = $derived(sorted.slice(start, end));

    // Keyboard navigation over the current page
    let activeIndex = $state(-1);

    $effect(() => {
        if (page || shownLemmas) activeIndex = -1;
    });

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === "ArrowDown") {
            e.preventDefault();
            activeIndex = activeIndex < shownLemmas.length - 1 ? activeIndex + 1 : 0;
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            activeIndex = activeIndex > 0 ? activeIndex - 1 : shownLemmas.length - 1;
        } else if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && activeIndex !== -1) {
            e.preventDefault();
            gotoLemma(shownLemmas[activeIndex]);
        }
    }

    function gotoLemma(target: { lang: string; lemma: string }) {
        goto(
            resolve("/lookup/[lang]/[lemma]", {
                lang: target.lang,
                lemma: encodeURIComponent(target.lemma),
            }),
            { keepFocus: true },
        );
    }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="table-wrap card bg-tertiary-50-950 w-full max-w-xl shadow-lg">
    <table class="table">
        <thead>
            <tr class="preset-filled-surface-500">
                {#each columns as col}
                    <th class={col === "lang" ? "w-32" : ""}>
                        <button
                            type="button"
                            class="flex items-center gap-1"
                            onclick={() => toggleSort(col)}
                        >
                            {columnLabel(col)}
                            {#if sortKey === col}
                                {#if sortDir === "asc"}
                                    <ChevronUpIcon class="size-4" />
                                {:else}
                                    <ChevronDownIcon class="size-4" />
                                {/if}
                            {:else}
                                <ChevronsUpDownIcon class="size-4 opacity-40" />
                            {/if}
                        </button>
                    </th>
                {/each}
                <th class="w-8"></th>
            </tr>
        </thead>
        <tbody>
            {#each shownLemmas as row, i}
                {@const isActive = activeIndex === i}
                <tr
                    class="cursor-pointer {isActive
                        ? 'preset-filled-primary-100-900'
                        : ''}"
                    onclick={() => gotoLemma(row)}
                    onmouseenter={() => (activeIndex = i)}
                >
                    {#each columns as col}
                        <td class="align-middle">
                            {#if col === "lemma"}
                                <a
                                    href={resolve("/lookup/[lang]/[lemma]", {
                                        lang: row.lang,
                                        lemma: encodeURIComponent(row.lemma),
                                    })}
                                    onclick={(e) => e.stopPropagation()}
                                >
                                    {row.lemma}
                                </a>
                            {:else}
                                <span class="inline-flex items-center gap-2">
                                    <span
                                        class="size-2 rounded-full {LANG_COLORS[
                                            row.lang
                                        ]}"
                                    ></span>
                                    {langname(row.lang, locale)}
                                </span>
                            {/if}
                        </td>
                    {/each}
                    <td class="w-8 text-right align-middle">
                        {#if isActive}
                            <ArrowRightIcon class="inline size-4" />
                        {/if}
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>

{#if n_results > 10}
    <Pagination
        class="preset-filled-tertiary-50-950 flex w-fit min-w-1/2 justify-between"
        count={n_results}
        {pageSize}
        {page}
        onPageChange={(event) => (page = event.page)}
    >
        <Pagination.PrevTrigger>
            <ArrowLeftIcon class="size-4" />
        </Pagination.PrevTrigger>
        <Pagination.Context>
            {#snippet children(pagination)}
                {#each pagination().pages as page, index (page)}
                    {#if page.type === "page"}
                        <Pagination.Item {...page}>
                            {page.value}
                        </Pagination.Item>
                    {:else}
                        <Pagination.Ellipsis {index}>&#8230;</Pagination.Ellipsis>
                    {/if}
                {/each}
            {/snippet}
        </Pagination.Context>
        <Pagination.NextTrigger>
            <ArrowRightIcon class="size-4" />
        </Pagination.NextTrigger>
    </Pagination>
{/if}
