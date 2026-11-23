# Lokální stránky /tvorba-webu-<mesto>/ a rozcestník /kde-pusobime/.
# Každá lokalita musí mít vlastní obsah (ne jen vyměněný název) – Google jinak vyhodnotí stránky jako doorway.
# k = kicker, h = nadpis (*podtržení*), l = perex, why = 3× (nadpis, text), area = obce/čtvrti, refs = reference ze snímků,
# q = otázky a odpovědi. Náhledovku tvoří tools/og.py z meta["og"].

L = {
    "praha": dict(
        n="Praha", kde="v Praze", kw="Tvorba webů Praha",
        h="Tvorba webů *v Praze*",
        l="Weby a e-shopy pro pražské firmy, živnostníky a značky. Sídlíme kousek za Prahou, takže se rádi potkáme osobně, ať už na Letné, v Karlíně, nebo u vás v kanceláři.",
        md="Tvorba webů a e-shopů v Praze. Design na míru, AI zrychluje práci, kvalitu hlídá člověk. Osobní schůzka v Praze, prezentační web od 25 000 Kč.",
        why=[
            ("Osobní schůzka v Praze", "Na úvodní konzultaci za vámi přijedeme nebo se potkáme v kavárně. Do Prahy to máme z Říčan pár minut, další schůzky už běží hlavně online."),
            ("Pražský trh známe", "Pražské kavárny, studia, reality i developerské projekty soupeří o pozornost s desítkami podobných firem. Web proto stavíme tak, aby vás odlišil a přivedl poptávky."),
            ("Weby pro náročné obory", "Luxusní interiéry, gastro na Letné, móda nebo kongresy v Praze. Umíme vícejazyčné weby pro turisty i zahraniční klientelu."),
        ],
        area="Praha 1 až 22, Letná, Holešovice, Karlín, Vinohrady, Smíchov, Dejvice, Žižkov, Vršovice, Strašnice, Chodov, Jižní Město, Černý Most",
        refs=["zahradkyletna-cz", "maisondeluxeprague-com", "uhrdinu-cz", "homedesigner-cz", "ltc-congress-com", "jamiecollection-cz"],
        typy=["gastro", "zdravi", "reality", "developer", "vicejazycne", "eshop"],
        q=[
            ("Kolik stojí tvorba webu v Praze?", "Ceny máme stejné v Praze i mimo ni: AI web od 20 000 Kč, prezentační web na WordPressu od 25 000 Kč a e-shop od 35 000 Kč. Pražské agentury bývají dražší hlavně kvůli režii, my jsme malý tým bez drahé kanceláře."),
            ("Můžeme se potkat osobně?", "Ano. Úvodní schůzku rádi uděláme osobně kdekoli v Praze. Další konzultace pak běží online, aby vás to nestálo čas."),
            ("Umíte web v angličtině pro turisty a cizince?", "Ano, vícejazyčné weby stavíme běžně. Pro restaurace, ubytování a obchody v centru Prahy je angličtina často stejně důležitá jako čeština."),
            ("Jak rychle bude web hotový?", "AI web bývá hotový během dnů, prezentační web na WordPressu obvykle za 3 až 6 týdnů. Záleží hlavně na tom, jak rychle máme podklady."),
        ],
    ),
    "ricany": dict(
        n="Říčany", kde="v Říčanech", kw="Tvorba webů Říčany",
        h="Tvorba webů *v Říčanech*",
        l="Jsme z Říčan. Weby a e-shopy pro místní firmy, řemeslníky, obchody a služby. Stačí zavolat a potkáme se tady ve městě.",
        md="Tvorba webů a e-shopů v Říčanech. Místní tým, osobní schůzka, design na míru. Prezentační web od 25 000 Kč, AI web od 20 000 Kč.",
        why=[
            ("Jsme místní", "Webovybalicek sídlí v Říčanech. Na schůzku nemusíte nikam jezdit a když bude potřeba něco vyřešit rychle, jsme kousek."),
            ("Weby pro místní služby", "Řemeslníci, kadeřnictví, kliniky, školky nebo restaurace. Lidé z Říčan a okolí vás hledají v Googlu i na Mapách, web proto stavíme i na místní vyhledávání."),
            ("Správa bez starostí", "Po spuštění se o web staráme dál. Aktualizace, zálohy a drobné úpravy vyřešíme, aniž byste museli něco hledat."),
        ],
        area="Říčany, Radošovice, Kuří, Jažlovice, Strašín, Pacov, Voděrádky, Mukařov, Světice, Strančice, Mnichovice, Kamenice",
        refs=["kabinykravak-cz", "mmntshop-cz", "dorsen-cz", "zahradkyletna-cz"],
        typy=["remesla", "zdravi", "gastro", "rezervace", "firemni", "eshop"],
        q=[
            ("Kde se můžeme potkat?", "Přímo v Říčanech, u vás ve firmě nebo v kavárně na náměstí. Nebo online, jak vám to vyhovuje víc."),
            ("Pomůžete i s Google Mapami a Firemním profilem?", "Ano. Pro místní firmy je Firemní profil na Googlu často stejně důležitý jako web. Nastavíme ho a propojíme s webem."),
            ("Stavíte i pro malé živnostníky?", "Ano. Pro řemeslníka nebo jednu provozovnu bohatě stačí AI web od 20 000 Kč nebo menší prezentační web. Doporučíme, co dává smysl."),
            ("Postaráte se o web i po spuštění?", "Ano, správu webu nabízíme od 600 Kč měsíčně: aktualizace, zálohy, bezpečnost a drobné úpravy."),
        ],
    ),
    "praha-vychod": dict(
        n="Praha-východ", kde="v okrese Praha-východ", kw="Tvorba webů Praha-východ",
        h="Tvorba webů *Praha-východ*",
        l="Úvaly, Brandýs, Čelákovice, Mnichovice, Kostelec nad Černými lesy i další obce na východ od Prahy. Weby a e-shopy od lidí, kteří tu žijí.",
        md="Tvorba webů a e-shopů v okrese Praha-východ: Úvaly, Brandýs nad Labem, Čelákovice, Mnichovice, Kostelec. Osobní schůzka, design na míru.",
        why=[
            ("Celý okres máme za rohem", "Z Říčan to máme do Úval, Mnichovic, Kostelce i Brandýsu kousek. Úvodní schůzku uděláme u vás."),
            ("Firmy z regionu", "Stavební firmy, řemeslníci, kliniky, ubytování nebo farmy. Weby, které ukážou, co umíte, a přivedou zákazníky z okolí."),
            ("Místní vyhledávání", "Lidé hledají služby „v okolí“. Web proto připravujeme na dotazy s názvy obcí a propojujeme ho s Firemním profilem na Googlu."),
        ],
        area="Úvaly, Brandýs nad Labem-Stará Boleslav, Čelákovice, Mnichovice, Kostelec nad Černými lesy, Mukařov, Sulice, Jesenice u Prahy, Šestajovice, Klecany, Odolena Voda, Zeleneč, Škvorec",
        refs=["kabinykravak-cz", "dorint-cz", "bohdasin17-cz", "mmntshop-cz"],
        typy=["remesla", "ubytovani", "zdravi", "firemni", "rezervace", "eshop"],
        q=[
            ("Jezdíte na schůzky i mimo Prahu?", "Ano, okres Praha-východ máme z Říčan nejblíž. Na úvodní schůzku přijedeme za vámi."),
            ("Kolik stojí web pro firmu z okolí Prahy?", "AI web od 20 000 Kč, prezentační web od 25 000 Kč, e-shop od 35 000 Kč. Přesnou cenu pošleme po krátké konzultaci zdarma."),
            ("Pomůžete, aby nás lidé našli v okolí?", "Ano. Web připravíme na místní vyhledávání, nastavíme Firemní profil na Googlu a strukturovaná data s adresou a oblastí působnosti."),
        ],
    ),
    "praha-zapad": dict(
        n="Praha-západ", kde="v okrese Praha-západ", kw="Tvorba webů Praha-západ",
        h="Tvorba webů *Praha-západ*",
        l="Mníšek pod Brdy, Černošice, Řevnice, Dobřichovice, Jílové u Prahy i Roztoky. Weby a e-shopy pro firmy a živnostníky na západ a jih od Prahy.",
        md="Tvorba webů a e-shopů v okrese Praha-západ: Mníšek pod Brdy, Černošice, Řevnice, Dobřichovice, Jílové, Roztoky. Design na míru, osobní schůzka.",
        why=[
            ("Brdy a Povltaví známe", "V okolí Mníšku pod Brdy jsme doma. Rádi se potkáme osobně, ať už v Mníšku, Řevnicích, nebo v Černošicích."),
            ("Pro služby i turistiku", "Ubytování, restaurace u cyklostezek, řemeslníci, kliniky nebo spolky. Web, který ukáže, co nabízíte, a umí přijmout rezervaci."),
            ("Jeden partner na všechno", "Web, doména, e-maily, Firemní profil na Googlu i správa po spuštění. Nemusíte koordinovat několik dodavatelů."),
        ],
        area="Mníšek pod Brdy, Černošice, Řevnice, Dobřichovice, Všenory, Jíloviště, Štěchovice, Jílové u Prahy, Psáry, Jesenice, Hostivice, Rudná, Roztoky, Libčice nad Vltavou",
        refs=["bohdasin17-cz", "kabinykravak-cz", "zahradkyletna-cz", "dorsen-cz"],
        typy=["ubytovani", "gastro", "remesla", "neziskovky", "rezervace", "firemni"],
        q=[
            ("Potkáme se i v Mníšku nebo Řevnicích?", "Ano, v okolí Mníšku pod Brdy jsme často. Úvodní schůzku uděláme u vás nebo online."),
            ("Umíte rezervace pro ubytování a restaurace?", "Ano. Napojujeme rezervační systémy i vlastní formuláře, prodej poukazů a platby kartou."),
            ("Kolik stojí web?", "AI web od 20 000 Kč, prezentační web od 25 000 Kč, e-shop od 35 000 Kč. Nejdřív se zeptáme, co potřebujete, a pak pošleme přesnou nabídku."),
        ],
    ),
    "stredocesky-kraj": dict(
        n="Středočeský kraj", kde="ve Středočeském kraji", kw="Tvorba webů Středočeský kraj",
        h="Tvorba webů *ve Středočeském kraji*",
        l="Benešov, Kolín, Kutná Hora, Beroun, Mladá Boleslav, Kladno i Příbram. Weby a e-shopy pro firmy z celého kraje, s osobní schůzkou i bez ní.",
        md="Tvorba webů a e-shopů ve Středočeském kraji: Benešov, Kolín, Kutná Hora, Beroun, Kladno, Mladá Boleslav, Příbram. Design na míru, AI, správa.",
        why=[
            ("Kraj kolem Prahy", "Sídlíme v Říčanech, uprostřed kraje. Do Benešova, Kolína nebo Berouna se dostaneme rychle, zbytek spolupráce běží online."),
            ("Výroba, řemesla, cestovní ruch", "Středočeský kraj žije výrobou, stavebnictvím a turistikou. Stavíme weby, které ukážou zakázky, přivedou poptávky a umí rezervace."),
            ("Weby, které se najdou", "SEO, Firemní profil na Googlu a strukturovaná data pro vyhledávače i AI. Aby vás lidé z okolí našli dřív než konkurenci."),
        ],
        area="Benešov, Kolín, Kutná Hora, Beroun, Kladno, Mělník, Mladá Boleslav, Nymburk, Poděbrady, Příbram, Rakovník, Sedlčany, Vlašim, Neratovice, Slaný",
        refs=["continest-cz", "dorint-cz", "kabinykravak-cz", "bohdasin17-cz", "dorsen-cz"],
        typy=["remesla", "firemni", "ubytovani", "b2b", "nabor", "eshop"],
        q=[
            ("Pracujete pro firmy mimo Prahu?", "Ano, velkou část klientů máme mimo Prahu. Většina spolupráce běží online, na úvodní schůzku rádi přijedeme."),
            ("Umíte weby pro výrobní a stavební firmy?", "Ano. Prezentace zakázek, poptávkové formuláře, kalkulačky i B2B e-shopy pro velkoobchod."),
            ("Kolik stojí web?", "AI web od 20 000 Kč, prezentační web od 25 000 Kč, e-shop od 35 000 Kč. Přesnou cenu pošleme po krátké konzultaci zdarma."),
        ],
    ),
}
