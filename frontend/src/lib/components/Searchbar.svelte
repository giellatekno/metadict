<script lang="ts">
    import searchIcon from "$assets/search.svg";
    import { t, locale } from "svelte-intl-precompile";
    import { langname } from "$lib/langname";
    import { createEventDispatcher, onMount } from "svelte";

    export let search_input: HTMLInputElement;
    export let value = ""
    export let search_lang = "sme"

    const sami_letters = ["á", "č", "đ", "ŋ", "š", "ŧ", "ž"]

    const dispatch = createEventDispatcher()

    function on_enter_keydown(event:KeyboardEvent) {
        if (event.key !== "Enter" || value === "") return;
        dispatch("new-value", value)
    }

    function on_click() {
        if (value === "") return;
        dispatch("new-value", value)
    }
    onMount(() => {
        search_input.focus()
    })

    function on_sami_letter(letter: string) {
        value += letter
        search_input.focus()
    }

</script>

<div class="flex flex-wrap md:flex-initial">
    <div class="input-group input-group-divider rounded-2xl grid-cols-[auto_1fr_auto] w-full md:w-[42rem] h-12 md:h-16">
        <button class="input-group-shim" on:click={on_click}>
            <img src={searchIcon} alt="Search" width="25">
        </button>
        <input
        bind:this={search_input}
        type="search" 
        placeholder="{$t("search")}" 
        bind:value={value}
        on:keydown={on_enter_keydown}
        />
        <select
        name="searchlang" 
        id="searchlang" 
        bind:value={search_lang}>
            <option value="sme">{langname("sme", $locale)}</option>
            <option value="nob">{langname("nob", $locale)}</option>
            <option value="fin">{langname("fin", $locale)}</option>
        </select>
    </div>
    {#if search_lang === "sme"}        
        <div class="ml-[3.8rem] md:ml-5 my-3 w-fit grid grid-cols-7 gap-1">
            {#each sami_letters as letter}
                <button 
                class="px-2 py-1 outline outline-1 outline-primary-500 rounded hover:underline hover:bg-primary-500/15 "
                on:click = {() => on_sami_letter(letter)}>
                {letter}
                </button>
            {/each}
        </div>
    {/if}
</div>