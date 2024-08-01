<script lang="ts">
    import { t } from "svelte-intl-precompile";
    import Popup from "$lib/components/Popup.svelte";
    export let data;

    let showModal = false;

    let rendered: string | undefined;
    $: rendered = data.rendered

    let neighbors: Array<string> | undefined; 
    $: neighbors = data.neighbors

    let dictionary: Array<string> | undefined;
    $ : dictionary = data.dictionary
</script>

<div style="display: flex; flex-direction: column;">
    {#if neighbors && neighbors.length > 0}
        {#each neighbors as neighbor}
            {#if neighbor === rendered} 
                <div class="article">
                    {@html neighbor}
                </div>
            {:else}
                <div class="neighbor">
                    {@html neighbor}
                </div>
            {/if}
        {/each}
    {:else}
        <div class="single-article">
            {@html rendered}
        </div>
    {/if}
    <div>
        <button on:click={() => (showModal = true)}>
            <h5>{$t("about-dictionary")}</h5>        
        </button>
    </div>
</div>

{#if dictionary}
<Popup bind:showModal>
    <h2 slot="header">{dictionary[0]}</h2>
    {#if dictionary[1]}
        <h4>{$t("authors")}</h4>
        <p>{dictionary[1]}</p>
    {/if}
    {#if dictionary[2]}
        <h4>{$t("year-published")}</h4>
        <p>{dictionary[2]}</p>
    {/if}
    {#if dictionary[3]}
        <h4>ISBN</h4>
        <p>{dictionary[3]}</p>
    {/if}
    {#if !(dictionary[1] || dictionary[2] || dictionary[3])}
        <p>{$t("no-additional-info")}</p>
    {/if}
</Popup>
{/if}

<style>
    div.article {
        margin-right: 200px;
        border-top: 3px solid black;
        border-bottom: 3px solid black;
    }

    div.neighbor {
        margin-right: 200px;
        font-size: 0.8em;
    }

    div.single-article {
        margin-right: 200px;
    }

    button {
        background: none!important;
        border: none;
        padding: 0!important;
        color: blue;
        text-decoration: underline;
        cursor: pointer;
    }
</style>
