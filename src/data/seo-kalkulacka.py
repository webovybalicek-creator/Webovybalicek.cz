# Kalkulačka ceny webu /kalkulacka-ceny-webu/. ORIENTAČNÍ ceny – upravovat tady.
# Výsledek = základ + rozsah + jazyky + funkce + obsah, horní hranice = ×1,25; spěch = +15 %.
BASE = [("ai", "AI web", 20000, "Web na míru postavený s pomocí AI, hotový během dnů."),
        ("wordpress", "Prezentační web", 25000, "WordPress s Elementorem, obsah si spravujete sami."),
        ("eshop", "E-shop", 35000, "WooCommerce s platbami, dopravci a fakturací.")]
PAGES = [("Do 5 stránek", 0), ("6 až 10 stránek", 6000), ("11 až 20 stránek", 14000), ("Víc než 20 stránek", 25000)]
LANGS = [("Jen čeština", 0), ("2 jazyky", 6000), ("3 a více jazyků", 12000)]
FEATURES = [("Online rezervace", 6000), ("Blog nebo magazín", 3000), ("Prodej kurzů a členská sekce", 15000),
            ("Dárkové poukazy", 6000), ("Kalkulačka nebo konfigurátor", 10000), ("Napojení na jiný systém (CRM, ERP, API)", 8000)]
CONTENT = [("Texty připravíme my", 4000), ("Profesionální focení", 6000), ("Logo a vizuální identita", 8000)]
RUSH = 0.15
