<script lang="ts">
    import { AppBar } from "@skeletonlabs/skeleton-svelte";
    import Profile from "./Profile.svelte";
    import SelectLocale from "./SelectLocale.svelte";
    import LightSwitch from "./LightSwitch.svelte";
    import { t } from "svelte-intl-precompile";
    import { resolve } from "$app/paths";
    import { Info } from "lucide-svelte";

    interface Props {
        user:
            | {
                  gh_avatar_url: string;
                  gh_fullname: string;
                  restricted_dicts: boolean;
              }
            | undefined;
        redirect_uri: string;
    }

    let { user, redirect_uri }: Props = $props();
</script>

<AppBar>
    <AppBar.Toolbar class="grid grid-cols-[auto_auto] ">
        <AppBar.Headline class="flex justify-start m-4">
            <a class="text-4xl font-medium" href={resolve("/")}
                >{$t("page-title")}</a
            >
        </AppBar.Headline>
        <AppBar.Trail class="flex justify-end m-4 ">
            <div class="flex items-center gap-10">
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

                <SelectLocale />

                <a
                    href={resolve("/about")}
                    class="btn preset-filled-primary-500"
                >
                    <Info />
                    <span>Info</span>
                </a>
                <!-- <LightSwitch /> -->
            </div>
        </AppBar.Trail>
    </AppBar.Toolbar>
</AppBar>
<hr class="hr" />
