<script lang="ts">
    import { t } from 'svelte-intl-precompile';
    import { base } from "$app/paths";
    import { Paginator, type PaginationSettings } from '@skeletonlabs/skeleton';

    // Data from +page.js load()
    export let data;

    let paginationSettings = {
        page: 0,
        limit: 10,
        size: data.objs.length,
        amounts: []
    } satisfies PaginationSettings;

    $: paginationSettings.size = data.objs.length;

    $: paginatedSource = data.objs.slice(
        paginationSettings.page * paginationSettings.limit,
        paginationSettings.page * paginationSettings.limit + paginationSettings.limit
    )
</script>

<h5 class="h5 my-2">{$t("search-result", { values: { count: data.objs.length } })}</h5>

<div class="card p-2 w-fit">

    <nav class="list-nav">
        {#each paginatedSource as lemma}
            <a href="{base}/lookup/{data.lang}/{lemma}">
                <span>{lemma}</span>
            </a>
        {/each}
    </nav>
    {#if data.objs.length > 10}
    <Paginator class="mt-2"
        bind:settings={paginationSettings}
        showPreviousNextButtons={true}
    />        
    {/if}
</div>