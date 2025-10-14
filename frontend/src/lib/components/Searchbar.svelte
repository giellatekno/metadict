<script lang="ts">
    import searchIcon from "$assets/search.svg";
    import { t, locale } from "svelte-intl-precompile";
    import { langname } from "$lib/langname";
    import { onMount } from "svelte";

    interface Props {
        value?: string;
        search_lang?: string;
        on_new_value: Function;
    }

    let {
        value = $bindable(""),
        search_lang = $bindable("sme"),
        on_new_value,
    }: Props = $props();
    let search_input: HTMLInputElement;

    const extra_letters: { [id: string]: Array<string> } = {
        sme: ["á", "č", "đ", "ŋ", "š", "ŧ", "ž"],
        fin: ["ä", "ö", "å"],
        nob: ["æ", "ø", "å"],
    };

    function on_enter_keydown(event: KeyboardEvent) {
        if (event.key !== "Enter" || value === "") return;
        on_new_value(value);
    }

    function on_searchbutton_click() {
        if (value === "") return;
        on_new_value(value);
    }

    onMount(() => {
        search_input.focus();
    });

    function on_extra_letter(letter: string) {
        value += letter;
        search_input.focus();
    }
</script>

<div class="flex flex-wrap md:flex-initial">
    <div
        class="input-group input-group-divider rounded-2xl grid-cols-[auto_1fr_auto] w-full md:w-[42rem] h-12 md:h-16"
    >
        <button class="input-group-shim" onclick={on_searchbutton_click}>
            <img src={searchIcon} alt="Search" width="25" />
        </button>
        <input
            bind:this={search_input}
            type="search"
            placeholder={$t("search-placeholder")}
            bind:value
            onkeydown={on_enter_keydown}
        />
        <select name="searchlang" id="searchlang" bind:value={search_lang}>
            <option value="sme">{langname("sme", $locale)}</option>
            <option value="nob">{langname("nob", $locale)}</option>
            <option value="fin">{langname("fin", $locale)}</option>
        </select>
    </div>
    <div class="ml-[3.8rem] md:ml-5 my-3 w-fit grid grid-cols-7 gap-1">
        {#each extra_letters[search_lang] as letter}
            <button
                class="px-2 py-1 outline outline-1 outline-primary-500 rounded hover:underline hover:bg-primary-500/15"
                onclick={() => on_extra_letter(letter)}
            >
                {letter}
            </button>
        {/each}
    </div>
</div>
