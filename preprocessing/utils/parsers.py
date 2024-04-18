import xml.etree.ElementTree as ET
from utils.dataclasses import Article, Dictionary


def _parse_gt_dict(file, lang, dictionary_id):
    articles = []
    
    xml = ET.parse(file)
 
    for e in xml.iter("e"):
        l_node = e.find("lg/l")
        if l_node is None:
            print("<e> node has no <lg><l>")
            continue

        lemma = l_node.text.strip("\n\t ").replace("\n", " ")
        mgs = e.findall("mg")
        rendered = "<br>".join(ET.tostring(mg, encoding="unicode") for mg in mgs)
        rendered = rendered.replace("\n", "<br>").replace("\t", " ")

        a = Article(
            dictionary=dictionary_id,
            lemma=lemma,
            rendered=rendered,
            lang=lang,
        )

        articles.append(a)    
    
    return articles
    

def _parse_qvigstad(file, lang, dictionary_id):
    articles = []
    
    xml_file = ET.parse(file)

    for index, row in enumerate(xml_file.iter("row"), 1):
        
        lemma = row[1].text.strip().replace("\n", " ")
        pos = row[2].text.strip()

        mgs = [row[0], row[3], row[4], row[5]]
        rendered = "<br>".join(ET.tostring(mg, encoding="unicode") for mg in mgs)
        rendered = rendered.replace("\n", "<br>").replace("\t", " ")

        a = Article(
            dictionary=dictionary_id,
            lemma=lemma,
            rendered=rendered,
            lang=lang,
            pos=pos,
            article_number=index
        )

        articles.append(a)

    return articles


def parse_dictionary(dir_name, file, dictionary_id, ):
    
    match dir_name:
        case 'gt':
            name = file.name[3:-4]
            l1, l2 = name.split("-")
            d = Dictionary(
                id=dictionary_id,
                name=f"gt-{name}",
                lang1=l1,
                lang2=l2,
            )

            articles = _parse_gt_dict(file, l1, dictionary_id)


        case 'qvigstad':
            d = Dictionary(
                id=dictionary_id,
                name="Qvigstad-Kalfjord-sme-nob",
                lang1="sme",
                lang2="nob",
                is_ordered=True,
                author="Just Qvigstad",
                date_published="1889", 
            )
            articles = _parse_qvigstad(file, "sme", dictionary_id)

        case _:
            raise Exception(f"Parsing of \"{dir_name}\" dictionaries not implemented")
            

    return d, articles