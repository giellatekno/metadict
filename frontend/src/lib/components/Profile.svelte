<script lang="ts">
    import { t } from "svelte-intl-precompile";
    export let user: {
        gh_avatar_url: string;
        gh_fullname: string;
        restricted_dicts: boolean;
    };
</script>

<span class="user">
    <img class="gh_avatar" src="{user.gh_avatar_url}" alt="Github user avatar" />
    <span class="name">{user.gh_fullname}</span>
    <span style="margin: 0 1em;">
        {#if user.restricted_dicts}
            <span style="color: green;">{$t("access")}</span>
        {:else}
            <span style="color: black;">{$t("noaccess")}</span>
        {/if}
    </span>
    <span><a href="/auth/logout">{$t("logout")}</a></span>
</span>

<style>
    span.user {
        display: inline-flex;
        align-items: center;
        gap: 0.8em;
    }

    img.gh_avatar {
        border-radius: 50%;
        height: 1.5em;
    }
</style>
