# Metadictionary

Ei meta-ordbok er ei "ordbok over ordbøker". Den skal gi mulighet for å søke
opp et ord på et språk, og få tilbake alle ordboksartikler fra alle ordbøkene
om det oppslagsordet. Dette vil være et nyttig verktøy for ordboksforfattere.

Inkluderte ordbøker skal også kunne være på et annet språk, eller skrevet med
annen ortografi, slik at man enkelt skal kunne se hvordan et ord har blitt
brukt historisk.


Here we include historical dictionaries.

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

Datamengden er av noe størrelse, og vi ønsker å sørge for at søk og oppslag
går relativt kjapt. Kanskje kan dataen ligge i en database, for da kan vi
bruke databasen til å gjøre søk og oppslag. Alternativt må vi ha vårt eget
format, og vår egen måte å gjøre søk og oppslag i dataen vår på.

Fordeler med en database:
- Søk og oppslag gjøres av databasen
- Kan lagre ekstra data (f.eks kommentarer) uten å behøve å gjøre endringer
  i kildematriell, eller ha en ekstern plass å lagre slik data.

Ulemper med database:
- Rigid struktur (relasjonell database)
- Må hostes.

Alternativt lager vi en egen representasjon, noe ala digtdictionaries.
Fordeler med database er at søk og oppslagsfunksjonalitet er gjort for oss.



### Datastrukturer og data-representasjon

Giellateknos ordbøker er i vårt eget spesifikke XML-format. Andre ordbøker
er i andre formater. Vi må kunne lese alle type ordbøker. Jeg ser for meg at
vi velger et type format og/eller datalagringsverktøy, som koden opererer på.
Så, for hver ordbok, må vi da lage scripts som konverterer til metaordbokens
format.


### Grensesnitt

Det er et web-basert verktøy, og selv om ikke designet trenger å være så
estetisk flott, så er det nok kompleksitet til å bruke et rammeverk.
Alternativer her er Svelte, eller React.



### Autentisering

Prøve å bruke github. Login skjer via github, og vi får informasjon tilbake
fra github når brukeren har logget inn om brukeren er medlem av en organsisasjon
vi kontrollerer.

Da gir man tilgang ved å legge en github bruker til i en organsisasjon.
Evt opprette et eget repo, hvor man legger brukere til.


### norsk - samisk

Start ut med nds-ordbøkene: nob-sme, nob-fin
Alle ordbøker til  samisk
Einspråklege ordbøker på norsk, svensk, dansk


### Kjeldekode 

https://github.com/giellatekno/metadictionary.git

Vi vil ha python og javascript

Vi vurderer satni.org.

### Tilgang

Viss metaordboka skal vere på Azure må vi finne ut av tilgangssystemet.


## Ordbøker

- kunne vi få kjeldekoden av dg?
- Vi treng oversikt over **alle** fagordbøkene


https://giellalt.github.io/dicts/dicts.html
