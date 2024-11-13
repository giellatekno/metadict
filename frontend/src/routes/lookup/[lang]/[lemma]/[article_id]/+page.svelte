<script lang="ts">
    import { t } from "svelte-intl-precompile";
    export let data;

    let rendered: string | undefined;
    $: rendered = data.rendered

    let neighbors: Array<string> | undefined; 
    $: neighbors = data.neighbors

    let dictionary: Array<string> | undefined;
    $ : dictionary = data.dictionary
</script>

<div class="grid grid-cols-5 gap-10 w-full">
    <div class="card col-span-3 p-5 w-full">
        {#if neighbors && neighbors.length > 0}
        {#each neighbors as neighbor}
        {#if neighbor === rendered} 
        <div class="p-1 border-y-2 bg-primary-500/10">
            {@html neighbor}
        </div>
        {:else}
        <div class="p-1 text-sm">
            {@html neighbor}
        </div>
        {/if}
        {/each}
        {:else}
        <div class="single-article">
            {@html rendered}
        </div>
        {/if}
    </div>

    {#if dictionary}
    <div class="card col-span-2 p-5 h-fit space-y-2">
        <h3 class="h3 font-medium">{dictionary[0]}</h3>
        {#if dictionary[1]}
        <div>
            <h4 class="h4">{$t("authors")}:</h4>
            <p>{dictionary[1]}</p>
        </div>
        {/if}
        {#if dictionary[2]}
        <div>
            <h4 class="h4">{$t("year-published")}:</h4>
            <p>{dictionary[2]}</p>
        </div>
        {/if}
        {#if dictionary[3]}
        <div>
            <h4 class="h4">ISBN:</h4>
            <p>{dictionary[3]}</p>
        </div>
        {/if}
        {#if !(dictionary[1] || dictionary[2] || dictionary[3])}
            <p>{$t("no-additional-info")}</p>
        {/if}
    </div>
    {/if}
</div>
