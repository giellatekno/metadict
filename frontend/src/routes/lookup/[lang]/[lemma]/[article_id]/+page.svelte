<script lang="ts">
    import { page } from "$app/stores";
    export let data;

    let rendered: string | undefined;
    $: rendered = data.rendered

    let neighbors: Array<string> | undefined; 
    $: neighbors = data.neighbors
</script>

{#if neighbors && neighbors.length > 0}
    <div style="display: flex; flex-direction: column;">
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
    </div>
{:else}
    <div class="single-article">
        {@html rendered}
    </div>
{/if}


<!-- {#if rendered}
    <div class="article">
        {@html rendered}
    </div>
{/if} -->

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
</style>
