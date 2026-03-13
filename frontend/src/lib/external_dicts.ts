export const externalDicts: Record<string, { name: string; link: string }[]> = {
    deu: [
        {
            name: "Wiktionary (deu)",
            link: "https://de.wiktionary.org/wiki/{%string%}",
        },
    ],
    est: [
        {
            name: "Esti-soome suursõnaraamat",
            link: "https://arhiiv.eki.ee/dict/efi/index.cgi?Q={%string%}&F=M&C06=fi",
        },
        {
            name: "Sõnaveeb",
            link: "https://sonaveeb.ee/search/unif/dlall/dsall/{%string%}/1/est",
        },
        {
            name: "Wiktionary (est)",
            link: "https://et.wiktionary.org/wiki/{%string%}",
        },
    ],
    eng: [],
    fin: [
        {
            name: "Kielitoimiston sanakirja",
            link: "https://www.kielitoimistonsanakirja.fi/#/{%string%}",
        },
        {
            name: "Suomi–viro-suursanakirja",
            link: "https://arhiiv.eki.ee/dict/fie/index.cgi?Q={%string%}&F=M&C06=fi",
        },
        {
            name: "Wiktionary (fin)",
            link: "https://fi.wiktionary.org/wiki/{%string%}",
        },
    ],
    nob: [
        {
            name: "ordbøkene.no",
            link: "https://ordbokene.no/nob/bm,nn/{%string%}",
        },
        {
            name: "Davvi girji (nob-sme)",
            link: "https://533.davvi.no/ordbok_norsam.php?finn={%string%}",
        },
    ],
    sma: [],
    sme: [
        {
            name: "Davvi girji (sme-nob)",
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
