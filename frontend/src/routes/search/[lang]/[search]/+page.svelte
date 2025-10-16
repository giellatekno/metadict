<script lang="ts">
    import { t } from "svelte-intl-precompile";
    import { resolve } from "$app/paths";
    import { Pagination } from "@skeletonlabs/skeleton-svelte";
    import type { PageProps } from "./$types";
    import { page as pagestate } from "$app/state";
    import { ArrowLeftIcon, ArrowRightIcon } from "lucide-svelte";

    let { data }: PageProps = $props();

    const PAGE_SIZE = 10;

    let page = $state(1);

    const start = $derived((page - 1) * PAGE_SIZE);
    const end = $derived(start + PAGE_SIZE);
    const lemmas = $derived(data.lemmas.slice(start, end));
</script>

<h5 class="h5 my-2">
    {$t("search-result", { values: { count: data.lemmas.length } })}
</h5>
<div class="card py-2 w-1/4 bg-surface-100-900 border border-surface-200-800">
    <div class="flex flex-col gap-2">
        {#each lemmas as lemma}
            <a
                class="btn mx-2 hover:preset-tonal justify-start"
                href={resolve(`/lookup/${pagestate.params.lang}/${lemma}`)}
            >
                {lemma}
            </a>
            {#if !(lemma === lemmas[-1])}
                <hr class="hr border-surface-200-800" />
            {/if}
        {/each}
    </div>
    {#if data.lemmas.length > 10}
        <Pagination
            class="w-full justify-center flex gap-2 mt-2"
            count={data.lemmas.length}
            pageSize={PAGE_SIZE}
            {page}
            onPageChange={(event) => (page = event.page)}
        >
            <Pagination.PrevTrigger
                class="btn btn-sm preset-filled-surface-500"
            >
                <ArrowLeftIcon size={24} />
            </Pagination.PrevTrigger>
            <Pagination.Context>
                {#snippet children(pagination)}
                    {#each pagination().pages as page, index (page)}
                        {#if page.type === "page"}
                            <Pagination.Item
                                {...page}
                                class="btn btn-sm preset-filled-surface-500"
                            >
                                {page.value}
                            </Pagination.Item>
                        {:else}
                            <Pagination.Ellipsis
                                {index}
                                class="btn btn-sm preset-filled-surface-500"
                            >
                                &#8230;
                            </Pagination.Ellipsis>
                        {/if}
                    {/each}
                {/snippet}
            </Pagination.Context>
            <Pagination.NextTrigger
                class="btn btn-sm preset-filled-surface-500"
            >
                <ArrowRightIcon size={24} />
            </Pagination.NextTrigger>
        </Pagination>
    {/if}
</div>
