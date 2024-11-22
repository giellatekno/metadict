<script lang="ts">
    import searchIcon from "$assets/search.svg";
    import { t, locale } from "svelte-intl-precompile";
    import { langname } from "$lib/langname";
    import { createEventDispatcher } from "svelte";


    let input;
    export let value = ""
    export let search_lang = "sme"

    const dispatch = createEventDispatcher();

    function on_enter_keydown(event:KeyboardEvent) {
        if (event.key !== "Enter") return;
        dispatch("new-value", value)
    }

    function on_click() {
        dispatch("new-value", value)
    }
</script>


<div class="input-group input-group-divider grid-cols-[auto_1fr_auto] w-2/6 h-16">
    <div class="input-group-shim">
        <button class="btn-icon btn-icon-lg !bg-transparent" on:click={on_click}>
            <img src={searchIcon} alt="Search" width="30">
        </button>
    </div>
    <input 
        bind:this={input}
        type="search" 
        placeholder="{$t("search")}" 
        bind:value 
        on:keydown={on_enter_keydown}
        />
    <select name="searchlang" id="searchlang" bind:value={search_lang}>
        <option value="sme">{langname("sme", $locale)}</option>
        <option value="nob">{langname("nob", $locale)}</option>
        <option value="fin">{langname("fin", $locale)}</option>
    </select>

</div>
