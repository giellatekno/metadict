<script lang="ts">
    import { t } from "svelte-intl-precompile";
    import { resolve } from "$app/paths";
    import { Paginator, type PaginationSettings } from "@skeletonlabs/skeleton";
    import type { PageProps } from "./$types";
    import { page } from "$app/state";

    let { data }: PageProps = $props();

    let paginationSettings = $state({
        page: 0,
        limit: 10,
        size: data.lemmas.length,
        amounts: [],
    } satisfies PaginationSettings);

    $effect(() => {
        paginationSettings.size = data.lemmas.length;
    });

    let paginatedSource = $derived(
        data.lemmas.slice(
            paginationSettings.page * paginationSettings.limit,
            paginationSettings.page * paginationSettings.limit +
                paginationSettings.limit,
        ),
    );
</script>

<h5 class="h5 my-2">
    {$t("search-result", { values: { count: data.lemmas.length } })}
</h5>

{#if paginationSettings.size !== 0}
    <div class="card p-2 w-fit">
        <nav class="list-nav">
            {#each paginatedSource as lemma}
                <a href={resolve(`/lookup/${page.params.lang}/${lemma}`)}>
                    <span>{lemma}</span>
                </a>
            {/each}
        </nav>
        {#if data.lemmas.length > 10}
            <Paginator
                class="mt-2"
                bind:settings={paginationSettings}
                showPreviousNextButtons={true}
            />
        {/if}
    </div>
{/if}
