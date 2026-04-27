# Metadictionary

Ei metaordbok er ei "ordbok over ordbøker". Den skal gi mulighet for å søke
opp et ord på et språk, og få tilbake alle ordboksartikler fra alle ordbøkene
om det oppslagsordet. Dette vil være et nyttig verktøy for ordboksforfattere.

Inkluderte ordbøker skal også kunne være på et annet språk, eller skrevet med
annen ortografi, slik at man enkelt skal kunne se hvordan et ord har blitt
brukt historisk.

Innholdet til metaordboka ligger i [`dictionaries-closed`](https://github.com/giellatekno/dictionaries-closed) repositoriet (krever tilgang).

---

## Repo-struktur

```
metadict/
├── api/            # Rust/Axum web-API
├── db/             # PostgreSQL-oppsett og init-skript
├── frontend/       # SvelteKit-webside
├── preprocessing/  # Python-skript for å parse ordbøker og generere SQL
└── ocr_cleanup/    # Python-skript for opprydding av OCR-skannede ordbøker
```

Se README i hver undermappe for detaljer.

---

## Tech stack

| Lag            | Teknologi                                                      |
|----------------|----------------------------------------------------------------|
| Frontend       | Svelte 5 + SvelteKit, TypeScript, Tailwind CSS, Skeleton UI, Paraglide (i18n) |
| API            | Rust, Axum, Tokio                                              |
| Database       | PostgreSQL                                                     |
| Autentisering  | GitHub OAuth                                                   |
| Preprocessing  | Python                                                         |

---

## Arkitektur

```
            -------------------------------
            |      ordboksmateriell       |
            -------------------------------
                         |
                         |  genererer
                         v
            -------------------------------
            |       PostgreSQL            |
            -------------------------------
                         ^  aksesserer
                         |
            -------------------------------
            |      Kjernebibliotek        |
            -------------------------------
                         ^
                         |
            -------------------------------
            |         Web API             |
            -------------------------------
                         ^
                         |
            -------------------------------
            |         Webside             |
            -------------------------------

```

Brukere kan logge inn med GitHub. Medlemmer av et kontrollert team får tilgang
til lukkede ordbøker. Andre ser bare åpne ordbøker.

---

## Kom i gang

Se [Install.md](Install.md) for oppsett av utviklingsmiljø.
