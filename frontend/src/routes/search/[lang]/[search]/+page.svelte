<script lang="ts">
    import { t } from 'svelte-intl-precompile';
    import { base } from "$app/paths";
    
    // Data from +page.js load()
    export let data;
</script>

<p>
    {$t("search-result", { values: { count: data.objs.length } })}
</p>

<main>
    {#each data.objs as lemma}
        <span><a href="{base}/lookup/{data.lang}/{lemma}">{lemma}</a></span>
    {/each}
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        padding-left: 30px;
    }

    p {
        padding-left: 30px;
    }

    span {
        padding: 6px;
    }

    span > a {
        margin-left: 12px;
    }
</style>
