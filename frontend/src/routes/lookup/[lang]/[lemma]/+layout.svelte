<script lang="ts">
    import { page } from "$app/stores";
    import { langname } from "$lib/langname";
    import { locale, t } from "svelte-intl-precompile";
    import { base } from "$app/paths";
    import { Accordion, AccordionItem} from "@skeletonlabs/skeleton"
    import externalLinkIcon from "$assets/external-link.svg";
    
    export let data;

    $: lang = $page.params.lang;
    $: lemma = $page.params.lemma;
    $: n_dicts = new Set(data.objs.map((item: Array<any>) => item[1])).size;
    
    let hist_dicts: Array<any> = [];
    
    $: if (data && data.objs.length > 0) {
        hist_dicts = data.objs.filter((item: Array<any>) => {
            return item[4] !== "" && Number(item[4].slice(-4)) < 1979;
        });
    }
    
    $: dicts = data.objs.filter((item: Array<any>) => {
        return !hist_dicts.includes(item)
    });

    $: tr_langs = Array.from(new Set(dicts.map((item: Array<any>) => item[3])));

    console.log(hist_dicts.length, dicts, tr_langs);
    

    // Sort list to show: xxx-sme, xxx-nob, xxx-other-langs
    $: sorted_tr_langs = [
        ...tr_langs.filter(elm => elm === "sme"),
        ...tr_langs.filter(elm => elm === "nob"),
        ...tr_langs.filter(elm => elm !== "sme" && elm !== "nob"),
    ];

    $: result_text = $t("lookup-result", { values: { lemma: lemma, count: n_dicts } })
</script>

<h5 class="h5 my-2">{result_text}</h5>

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
                        {#each dicts as [lemma, dictionary_name, article_id, lang2, _]}
                        {#if tr_lang === lang2}
                        <a href="{base}/lookup/{lang}/{lemma}/{article_id}">
                            {dictionary_name.length > 30 ? dictionary_name.slice(0, 30) + '...' : dictionary_name} ({lemma})
                        </a>
                        {/if}
                        {/each}
                    </nav>
                </svelte:fragment>
            </AccordionItem>
            {/each}

            {#if hist_dicts.length > 0}
            <AccordionItem open>
                <svelte:fragment slot="summary">
                    <h6 class="h6"><b>{$t("historical-dictionaries")}</b></h6>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <nav class="list-nav">
                        {#each hist_dicts as [lemma, dictionary_name, article_id, lang2, _]}
                        <a href="{base}/lookup/{lang}/{lemma}/{article_id}">
                            {dictionary_name.length > 30 ? dictionary_name.slice(0, 30) + '...' : dictionary_name} ({lemma})
                        </a>
                        {/each}
                    </nav>
                </svelte:fragment>
            </AccordionItem>
            {/if}
        </Accordion>
        {#if lang === "nob"}
            <div class="p-4 mt-10">
                <a class="btn variant-filled-primary" href={`https://ordbokene.no/nob/bm,nn/${lemma}`} target="_blank">
                    <span>
                        {$t("search-ordbokene", { values: { lemma: lemma } })}
                    </span>
                    <img src={externalLinkIcon} alt="External link" width="22"/>
                </a>
            </div>
        {/if}

    
    </div>

    <div class="flex col-span-2">
        <slot/>
    </div>
</main>