<script lang="ts">
    import { t, locale } from "svelte-intl-precompile";
    import { langname } from "$lib/langname";
    import { onMount } from "svelte";
    import { SearchIcon } from "lucide-svelte";

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
    <!-- <div class="input-group grid-cols-[auto_1fr_auto]"> -->
    <div
        class="input-group rounded-2xl grid-cols-[auto_1fr_auto] w-full md:w-2xl h-12 md:h-16"
    >
        <button class="ig-cell" onclick={on_searchbutton_click}>
            <SearchIcon size={16} />
        </button>
        <input
            class="ig-input"
            bind:this={search_input}
            type="search"
            placeholder={$t("search-placeholder")}
            bind:value
            onkeydown={on_enter_keydown}
        />
        <select
            class="ig-select"
            name="searchlang"
            id="searchlang"
            bind:value={search_lang}
        >
            <option value="sme">{langname("sme", $locale)}</option>
            <option value="nob">{langname("nob", $locale)}</option>
            <option value="fin">{langname("fin", $locale)}</option>
        </select>
    </div>
    <div class="ml-[3.8rem] md:ml-5 my-3 w-fit grid grid-cols-7 gap-1">
        {#each extra_letters[search_lang] as letter}
            <button
                class="px-2 py-1 outline-solid outline-1 outline-primary-500 rounded-sm hover:underline hover:bg-surface-100-900"
                onclick={() => on_extra_letter(letter)}
            >
                {letter}
            </button>
        {/each}
    </div>
</div>
