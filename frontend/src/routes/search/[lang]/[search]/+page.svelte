<script lang="ts">
    import { resolve } from "$app/paths";
    import { Pagination } from "@skeletonlabs/skeleton-svelte";
    import type { PageProps } from "./$types";
    import { m } from "$lib/paraglide/messages";
    import { ArrowLeftIcon, ArrowRightIcon } from "@lucide/svelte";
    import { LANG_COLORS } from "$lib/utils";
    import { goto } from "$app/navigation";

    let { data }: PageProps = $props();

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
            const target = shownLemmas[activeIndex];
            goto(
                resolve("/lookup/[lang]/[lemma]", {
                    lang: target.lang,
                    lemma: target.lemma,
                }),
                {
                    keepFocus: true,
                },
            );
        }
    }

    let pageSize = $state(20);

    let page = $state(1);

    let start = $derived((page - 1) * pageSize);
    let end = $derived(start + pageSize);
    let shownLemmas = $derived(data.lemmas ? data.lemmas.slice(start, end) : []);
    let n_results = $derived(data.lemmas ? data.lemmas.length : 0);
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="flex w-full flex-col items-center gap-4 sm:w-1/4 sm:min-w-124">
    {#if n_results > 0}
        <div class="flex w-full items-center justify-between">
            <div class="text-nowrap">
                {m.search_hits({ count: n_results })}
            </div>
            <div class="flex flex-row items-center gap-2">
                <label for="hits-per-page" class="">
                    {m.search_hits_per_page()}
                </label>
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
        {#if n_results}
            <div class="flex w-full flex-col gap-2">
                <div class="card bg-tertiary-50-950 w-full shadow-lg">
                    <div class="flex flex-col">
                        {#each shownLemmas as { lang, lemma }, i}
                            {@const isActive = activeIndex === i}
                            {@const rounded_style =
                                i === 0
                                    ? "rounded-t-xl rounded-b-none"
                                    : i === shownLemmas.length - 1
                                      ? "rounded-b-xl rounded-t-none"
                                      : "rounded-none"}
                            {#if i !== 0}
                                <hr class="hr border-primary-500" />
                            {/if}
                            <a
                                class="btn {isActive
                                    ? 'preset-filled-primary-500'
                                    : 'hover:preset-tonal'} justify-between py-3 {rounded_style}"
                                href={resolve("/lookup/[lang]/[lemma]", { lang, lemma })}
                            >
                                {lemma}
                                <span class="badge preset-filled {LANG_COLORS[lang]}">
                                    {lang.toUpperCase()}
                                </span>
                            </a>
                        {/each}
                    </div>
                </div>
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
                                    <Pagination.Ellipsis {index}>
                                        &#8230;
                                    </Pagination.Ellipsis>
                                {/if}
                            {/each}
                        {/snippet}
                    </Pagination.Context>
                    <Pagination.NextTrigger>
                        <ArrowRightIcon class="size-4" />
                    </Pagination.NextTrigger>
                </Pagination>
            {/if}
        {/if}
    {:else}
        <span class="text-lg">{m.search_no_results()}</span>
    {/if}
</div>
