<script lang="ts">
    import { AppBar } from "@skeletonlabs/skeleton-svelte";
    import Profile from "./Profile.svelte";
    import SelectLocale from "./SelectLocale.svelte";
    import { t } from "svelte-intl-precompile";
    import { resolve } from "$app/paths";
    import { Info } from "lucide-svelte";

    interface Props {
        user?: {
            gh_avatar_url: string;
            gh_fullname: string;
            restricted_dicts: boolean;
        };
        redirect_uri: string;
    }

    let { user, redirect_uri }: Props = $props();
</script>

<AppBar>
    <AppBar.Toolbar class="grid-cols-[auto_auto] ">
        <AppBar.Headline>
            <a class="text-4xl font-medium" href={resolve("/")}
                >{$t("page-title")}</a
            >
        </AppBar.Headline>
        <AppBar.Trail>
            <div class="flex items-center gap-10">
                <SelectLocale />

                <a
                    href={resolve("/about")}
                    class="btn preset-filled-primary-400-600"
                >
                    <Info />
                    <span>Info</span>
                </a>
                {#if user}
                    <Profile {user}></Profile>
                {:else}
                    <a
                        class="btn btn-large preset-filled-primary-500"
                        href="https://github.com/login/oauth/authorize?scope=read:user%20read:repo&client_id=Iv1.f208b6793cca35ec&redirect_uri={redirect_uri}"
                    >
                        {$t("login")}
                    </a>
                {/if}
            </div>
        </AppBar.Trail>
    </AppBar.Toolbar>
</AppBar>
<hr class="hr" />
