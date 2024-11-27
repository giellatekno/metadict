<script lang="ts">
    import { page } from "$app/stores";
    import { langname } from "$lib/langname.js";
    import { locale, t } from "svelte-intl-precompile";
    import { base } from "$app/paths";
    import { Accordion, AccordionItem} from "@skeletonlabs/skeleton"
    
    export let data;

    const { lang, lemma, article_id } = $page.params;
    const n_dicts = data.objs.length;

    let tr_langs: Array<string> = [];
    
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

<h5 class="h5 my-2">{$t("lookup-result", { values: { lemma: lemma, count: n_dicts } })}</h5>

<main class="w-full grid grid-cols-3 gap-5">
    <div class="flex flex-col w-3/4">
        <Accordion class="card">
            {#each sorted_tr_langs as tr_lang}
            <AccordionItem open>
                <svelte:fragment slot="summary">
                    <h6 class="h6"><b>{langname(lang, $locale)} → {langname(tr_lang, $locale)}</b></h6>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <nav class="list-nav">
                        {#each data.objs as [lemma, dictionary_name, article_id, lang2]}
                        {#if tr_lang === lang2}
                        <a href="{base}/lookup/{lang}/{lemma}/{article_id}">
                            {lemma} ({dictionary_name})
                        </a>
                        {/if}
                        {/each}
                    </nav>
                </svelte:fragment>
            </AccordionItem>
            {/each}
        </Accordion>
    </div>

    <div class="flex col-span-2">
        <slot/>
    </div>
</main>