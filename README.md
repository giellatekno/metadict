# Metadictionary

Ei meta-ordbok er ei "ordbok over ordbøker". Den skal gi mulighet for å søke
opp et ord på et språk, og få tilbake alle ordboksartikler fra alle ordbøkene
om det oppslagsordet. Dette vil være et nyttig verktøy for ordboksforfattere.

Inkluderte ordbøker skal også kunne være på et annet språk, eller skrevet med
annen ortografi, slik at man enkelt skal kunne se hvordan et ord har blitt
brukt historisk.


Ein nøkkel frå 

```
moderne samisk
 -> Bergsland-Ruong (kanskje ikkje så viktig)
 -> Konrad Nielsen (svært viktig)
 -> Friis
 -> Itkonen
 -> Leem
 -> norsk + dansk + svensk
 -> finsk
moderne norsk
 -> 1800-talsdansk, svensk, (1800-talssvensk?), finsk, tysk
```


### samisk - norsk

- Start ut med nds-ordbøkene?

    - sme-nob, sme-fin, sme-eng

    - ei anna ei

- Andre, eksisterande ordbøker
- Korpus (konkordans)
- Álgu

Arbeid:
- Samle og tilrettelegge alle
- Lage eit grensesnitt med passord
---

## Implementasjon

### Arkitektur

Et kjernebibliotek som inneholder funksjonaliteten. Et web api som bruker
biblioteket, som en front-end så representerer.


```
           -------------------------------
           |    ordboksmateriell         |
           -------------------------------
                   |
                   __ -->  |  genererer
                           |
           -------------------------------
           |       PostgreSQL            |
           -------------------------------
                        ^  aksesserer
                        |
           -------------------------------
           |    Kjernebibliotek          |
           -------------------------------
                       ^
                       |
           -------------------------------
           |        Web API              |
           -------------------------------
                       ^
                       |
           -------------------------------
           |        Webside              |
           -------------------------------
           
```


### Kjernebibliotek og hvordan data ligger lagret

Vi lagrer dataen i en PostgreSQL-database. Fordeler med dette er at søk og
oppslag tar databasen seg av å optimalisere. Vi har også muligheten for å kunne
lagre brukerdata (f.eks kommentarer) i en database. Ulempen er at strukturen
er relativt rigid, og forandring av denne krever en del innsats, om det skulle
bli nødvendig.

Alternativet er å bruke vårt eget format, men vi så ikke at vi hadde behov
for det, og da en database gjør jobben vår enklere, ble det valgt.



### Datastrukturer og data-representasjon

Giellateknos ordbøker er i vårt eget spesifikke XML-format. Andre ordbøker
er i andre formater. Vi må kunne lese alle type ordbøker. Jeg ser for meg at
vi velger et type format og/eller datalagringsverktøy, som koden opererer på.
Så, for hver ordbok, må vi da lage scripts som konverterer til metaordbokens
format.


### Grensesnitt

Websida har et enkelt design, og SvelteKit er rammeverket vi bruker.



### Autentisering

Brukere kan logge inn med Github. Om brukeren er medlem av et team vi
kontrollerer, vil brukeren også se de lukkede ordbøkene. Ellers sees bare de
åpne.


### norsk - samisk

Start ut med nds-ordbøkene: nob-sme, nob-fin
Alle ordbøker til  samisk
Einspråklege ordbøker på norsk, svensk, dansk


## Ordbøker

- kunne vi få kjeldekoden av dg?
- Vi treng oversikt over **alle** fagordbøkene


https://giellalt.github.io/dicts/dicts.html
