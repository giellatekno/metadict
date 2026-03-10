<script lang="ts">
    import { getLocale } from "$lib/paraglide/runtime.js";
    import { m } from "$lib/paraglide/messages.js";
    import { langname } from "$lib/langname";
    import { onMount } from "svelte";
    import { ChevronDown, SearchIcon } from "lucide-svelte";
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";
    import { Accordion } from "@skeletonlabs/skeleton-svelte";
    import { slide } from "svelte/transition";

    let value = $state("");
    let search_lang = $state("sme");

    let search_input: HTMLInputElement;

    const extra_letters: Record<string, string[]> = {
        sme: ["á", "č", "đ", "ŋ", "š", "ŧ", "ž"],
        sma: ["ï", "æ", "ö"],
        fin: ["ä", "ö", "å"],
        nob: ["æ", "ø", "å"],
    };

    const search_langs = ["sme", "sma", "nob", "fin"] as const;

    // let target_langs = $state(["sme", "sma", "nob", "fin", "hist"]);

    // onMount(() => {
    //     const saved = localStorage.getItem("preferred_targets");
    //     if (saved) {
    //         try {
    //             target_langs = JSON.parse(saved);
    //         } catch (e) {
    //             console.error("Failed to parse languages", e);
    //         }
    //     }
    //     search_input.focus();
    // });

    // $effect(() => {
    //     localStorage.setItem("preferred_targets", JSON.stringify(target_langs));
    // });

    async function on_new_value(input: string) {
        await goto(
            resolve(`/search/${search_lang}/${encodeURIComponent(input)}`),
            { keepFocus: true },
        );
    }

    function on_enter_keydown(event: KeyboardEvent) {
        if (event.key !== "Enter" || value === "") return;
        on_new_value(value);
        search_input.focus();
    }

    function on_searchbutton_click() {
        if (value === "") return;
        on_new_value(value);
        search_input.focus();
    }

    onMount(() => {
        search_input.focus();
    });

    function on_extra_letter(letter: string) {
        value += letter;
        search_input.focus();
    }

    // function toggleTarget(lang: string) {
    //     if (target_langs.includes(lang)) {
    //         // Prevent deselecting everything (optional but recommended)
    //         if (target_langs.length > 1) {
    //             target_langs = target_langs.filter((l) => l !== lang);
    //         }
    //     } else {
    //         target_langs = [...target_langs, lang];
    //     }
    // }
</script>

<div class="flex w-2xl flex-col gap-2">
    <div class="grid w-fit grid-cols-7 gap-1.5">
        {#each extra_letters[search_lang] as letter}
            <button
                class="btn btn-sm md:btn-base preset-outlined-primary-500 w-4 md:w-8"
                onclick={() => on_extra_letter(letter)}
            >
                {letter}
            </button>
        {/each}
    </div>
    <div
        class="input-group preset-filled-tertiary-50-950 h-12 w-full grid-cols-[auto_1fr_auto] md:h-16 md:w-2xl"
    >
        <button class="ig-cell" onclick={on_searchbutton_click}>
            <SearchIcon class="size-6" />
        </button>
        <input
            class="ig-input text-lg"
            bind:this={search_input}
            type="search"
            placeholder={m.search_placeholder({ lang: search_lang })}
            bind:value
            onkeydown={on_enter_keydown}
        />
        <select
            class="ig-select"
            name="searchlang"
            id="searchlang"
            bind:value={search_lang}
            placeholder="Search language"
            onchange={() => {
                value = "";
                search_input.focus();
            }}
        >
            {#each search_langs as iso}
                <option value={iso}>{langname(iso, getLocale())}</option>
            {/each}
        </select>
    </div>
    <!-- <div class="flex flex-col"> -->
    <!--     <Accordion collapsible> -->
    <!--         <Accordion.Item value="1"> -->
    <!--             <h3> -->
    <!--                 <Accordion.ItemTrigger -->
    <!--                     class="preset-filled-surface-200-800 flex items-center justify-between font-bold" -->
    <!--                 > -->
    <!--                     Filter result languages -->
    <!--                     <Accordion.ItemIndicator class="group"> -->
    <!--                         <ChevronDown -->
    <!--                             class="h-5 w-5 transition group-data-[state=open]:rotate-180" -->
    <!--                         /> -->
    <!--                     </Accordion.ItemIndicator> -->
    <!--                 </Accordion.ItemTrigger> -->
    <!--             </h3> -->
    <!--             <Accordion.ItemContent -->
    <!--                 class="preset-outlined-surface-200-800 flex flex-wrap gap-2 rounded p-2" -->
    <!--             > -->
    <!--                 {#snippet element(attributes)} -->
    <!--                     {#if !attributes.hidden} -->
    <!--                         <div -->
    <!--                             {...attributes} -->
    <!--                             transition:slide={{ duration: 150 }} -->
    <!--                         > -->
    <!--                             {#each search_langs as iso} -->
    <!--                                 <button -->
    <!--                                     class="btn preset-outlined-primary-500 flex items-center text-sm" -->
    <!--                                     onclick={() => toggleTarget(iso)} -->
    <!--                                 > -->
    <!--                                     <input -->
    <!--                                         class="checkbox" -->
    <!--                                         type="checkbox" -->
    <!--                                         checked={target_langs.includes(iso)} -->
    <!--                                     /> -->
    <!--                                     <p> -->
    <!--                                         {langname(iso, getLocale())} -->
    <!--                                     </p> -->
    <!--                                 </button> -->
    <!--                             {/each} -->
    <!--                             <button -->
    <!--                                 class="btn preset-outlined-primary-500 flex items-center text-sm" -->
    <!--                                 onclick={() => toggleTarget("hist")} -->
    <!--                             > -->
    <!--                                 <input -->
    <!--                                     class="checkbox" -->
    <!--                                     type="checkbox" -->
    <!--                                     checked={target_langs.includes("hist")} -->
    <!--                                 /> -->
    <!--                                 <p>Historical dictionaries</p> -->
    <!--                             </button> -->
    <!--                         </div> -->
    <!--                     {/if} -->
    <!--                 {/snippet} -->
    <!--             </Accordion.ItemContent> -->
    <!--         </Accordion.Item> -->
    <!--     </Accordion> -->
    <!-- </div> -->
</div>
