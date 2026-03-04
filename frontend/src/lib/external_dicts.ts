export const externalDicts: Record<string, { name: string; link: string }[]> = {
    deu: [
        {
            name: "Wiktionary",
            link: "https://de.wiktionary.org/wiki/{%string%}",
        },
    ],
    est: [
        {
            name: "Sõnaveeb",
            link: "https://sonaveeb.ee/search/unif/dlall/dsall/{%string%}/1/est",
        },
        {
            name: "Wiktionary",
            link: "https://et.wiktionary.org/wiki/{%string%}",
        },
    ],
    // eng: [],
    fin: [
        {
            name: "Kielitoimiston sanakirja",
            link: "https://www.kielitoimistonsanakirja.fi/#/{%string%}",
        },
        {
            name: "Wiktionary",
            link: "https://fi.wiktionary.org/wiki/{%string%}",
        },
    ],
    nob: [
        {
            name: "ordbøkene.no",
            link: "https://ordbokene.no/nob/bm,nn/{%string%}",
        },
        {
            name: "Davvi girji",
            link: "https://533.davvi.no/ordbok_norsam.php?finn={%string%}",
        },
    ],
    sma: [],
    sme: [
        {
            name: "Davvi girji",
            link: "https://533.davvi.no/ordbok_samnor.php?finn={%string%}",
        },
    ],
    smj: [],
    smn: [],
    swe: [
        {
            name: "Svenska Akademiens ordböcker",
            link: "https://svenska.se/?q={%string%}",
        },
    ],
};
