<script lang="ts">
import "../app.css";
import { goto } from "$app/navigation";
import Profile from "$lib/components/Profile.svelte";
import { page } from "$app/stores";
import { base } from "$app/paths";
import { t, locale } from "svelte-intl-precompile";
import { env } from "$env/dynamic/public";
import { AppBar } from "@skeletonlabs/skeleton"
import SelectLocale from "$lib/components/SelectLocale.svelte";
import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
import { storePopup } from '@skeletonlabs/skeleton';
import infoIcon from "$assets/info.svg"
import Searchbar from "$lib/components/Searchbar.svelte";

storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });
			
let search_lang = "sme";

let redirect_uri = env.PUBLIC_API_ENDPOINT;
if (redirect_uri === undefined) {
    console.warn("routes/+layout.svelte: env.PUBLIC_API_ENDPOINT is undefined, using default value of 'http://localhost:3000'");
    redirect_uri = "http://localhost:3000";
}
redirect_uri = encodeURIComponent(redirect_uri + "/auth/callback");

type User = {
    gh_fullname: string,
    gh_avatar_url: string,
    restricted_dicts: boolean,
};
let user: User | undefined;
$: user = $page.data?.user;
async function on_new_value({ detail }: { detail: string }) {
    console.log(detail)
    const search_term = encodeURIComponent(detail);
    console.log(search_term)
    let url = `${base}/search/${search_lang}/${search_term}`;
    // fix for seemingly working in dev but not prod:
    // on dev base="", so the url starts with a "/", but on
    // prod, we have a base, starting with NOT a "/", so we need
    // to add it here, so that we don't go to a relative url
    if (!url.startsWith("/")) url = `/${url}`;
    console.log(url)
    await goto(url);
}
</script>

<svelte:head>
    <title>{$t("page-title")}</title>
</svelte:head> 

<AppBar background="bg-secondary-400" slotTrail="place-content-end">
    <a class="h2 font-medium" href="{base}/">{$t("page-title")}</a>
    
    <svelte:fragment slot="trail">
        <div class="flex items-center gap-10">
            {#if user}
            <Profile user="{user}"></Profile>
            {:else}
            <a class="btn variant-filled-tertiary" href="https://github.com/login/oauth/authorize?scope=read:user%20read:repo&amp;client_id=Iv1.f208b6793cca35ec&amp;redirect_uri={redirect_uri}">
                {$t("login")}
            </a>
            {/if}
            
            <SelectLocale/>
           
            <a href="{base}/about" class="btn variant-filled-tertiary">
                <img src={infoIcon} alt="Information" width="22"/>
                <span>Info</span>
            </a>           
        </div>
    </svelte:fragment>
</AppBar>

<div class="m-4 p-2">
    <label for="search-input" class="label">
        {$t("dictionary-form")} (%):
    </label>
    <div class="mt-2">
        <Searchbar on:new-value="{on_new_value}" bind:search_lang></Searchbar>
    </div>

    <div class="border bottom-1 w-full my-5"/>
    <slot/>    

</div>

