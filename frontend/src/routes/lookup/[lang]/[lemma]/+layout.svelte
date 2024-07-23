<script lang="ts">
    import { page } from "$app/stores";
    import { langname } from "$lib/langname.js";
    import { locale, t } from "svelte-intl-precompile";
    import { base } from "$app/paths";
    export let data;

    const { lang, lemma, article_id } = $page.params;
    const n_dicts = data.objs.length;

    let tr_langs: Array<string> = [];
    
    // Sort dicts by name so listing is consistent
    data.objs.sort((a: Array<any>, b: Array<any>) => {return a[1].localeCompare(b[1])})

    // Find all second langs of dicts
    data.objs.forEach((item: Array<any>) => {
        if (!tr_langs.includes(item[3])) {
            tr_langs.push(item[3])
        }
    });

    // Sort list to show: xxx-sme, xxx-nob, xxx-other-langs
    const sorted_tr_langs = [
        ...tr_langs.filter(elm => elm === "sme"),
        ...tr_langs.filter(elm => elm === "nob"),
        ...tr_langs.filter(elm => elm !== "sme" && elm !== "nob"),
    ];

</script>

<p>
    {$t("lookup-result", { values: { lemma: lemma, count: n_dicts } })}
</p>

<main class="container">
    <div class="k1">
        {#each sorted_tr_langs as tr_lang}
            <h4>{langname(lang, $locale)} - {langname(tr_lang, $locale)}</h4>
            {#each data.objs as [lemma, dictionary_name, article_id, lang2]}
                {#if tr_lang === lang2}
                    <span>
                        <a href="{base}/lookup/{lang}/{lemma}/{article_id}">
                            {lemma}
                        </a>
                        ({dictionary_name})
                    </span>
                {/if}
            {/each}
        {/each}
    </div>

    <div class="k2">
        <slot></slot>
    </div>
</main>


<style>
    main.container {
        width: 100vw;
        display: grid;
        grid-template-columns: 1fr 2fr;
    }

    div.k1 {
        display: flex;
        flex-direction: column;
        padding-left: 30px;
    }

    div.k2 {
        display: flex;
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
