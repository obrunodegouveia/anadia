#!/usr/bin/env python3
"""Build /pt/index.html (and any future locales) from index.html + i18n.json.

Reads the English source HTML and applies translations from i18n.json to
generate a fully-rendered static Portuguese page at /pt/index.html.
"""
import json, re, pathlib, html as html_mod

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / 'index.html'
I18N = json.loads((ROOT / 'i18n.json').read_text(encoding='utf-8'))

# Locale-specific overrides for <head> meta (not in i18n.json)
META = {
    'pt': {
        'title':       'Imóvel para Investimento em Anadia, Portugal · €790.000 | Vila Anadia',
        'description': 'Vila Anadia: imóvel de 393 m² para investimento em Anadia, Portugal. €790.000. 8 quartos + T0 + T1 + T3 privado, jardim, estacionamento. Rentabilidade até ~14%.',
        'ogTitle':     'Vila Anadia · €790.000 — 10 Unidades + T3 do Proprietário em Anadia, Portugal',
        'ogDesc':      'Imóvel de coliving & coworking em Anadia, Portugal. 393 m², 10 unidades + T3 do proprietário. Rentabilidade até ~14%.',
        'twTitle':     'Vila Anadia · €790.000 — Anadia, Portugal',
        'twDesc':      '10 unidades de arrendamento + T3 do proprietário no centro de Portugal. Rentabilidade até ~14%.',
        'ogLocale':    'pt_PT',
        'ogLocaleAlt': 'en_US',
        'ogImageAlt':  'Exterior do imóvel para investimento em Anadia, Portugal',
        'inLang':      'pt',
        'imgAlts': {
            'Aerial view of the property in Anadia':                        'Vista aérea do imóvel em Anadia',
            'Exterior front facade':                                        'Fachada frontal',
            'Exterior side angle with cobblestone street':                  'Vista lateral com calçada portuguesa',
            'Side passage with cobblestone path':                           'Passagem lateral com calçada',
            'Central hallway with arched doorways':                         'Corredor central com arcos',
            'Modern hallway with framed art':                               'Corredor superior com arte',
            'Wide shared lounge with bar and seating':                      'Lounge partilhado amplo com bar',
            'Common lounge with emerald green sofa':                        'Lounge comum com sofá verde',
            'Full kitchen with wood ceiling and granite counters':          'Cozinha completa com teto de madeira e bancadas em granito',
            'Shared dining area with long dark table':                      'Sala de refeições partilhada',
            'Lounge bar area with patterned tile floor':                    'Zona de lounge bar com pavimento padronizado',
            'Suite-style bedroom with arched ensuite bathroom view':        'Quarto suíte com vista da casa de banho em arco',
            'Bedroom with geometric wall mural':                            'Quarto com mural geométrico',
            'Bedroom with watercolor mural and green throw':                'Quarto com mural aguarela e manta verde',
            'Bedroom alternate angle with watercolor mural':                'Outro ângulo do quarto com mural aguarela',
            'Bedroom with palm wallpaper and green door':                   'Quarto com papel de parede de palmeiras e porta verde',
            'Bedroom with palm wall and storage':                           'Quarto com parede de palmeiras e arrumação',
            'Bedroom with monochrome palm mural':                           'Quarto com mural monocromático de palmeiras',
            'Wood frame bed with palm mural':                               'Cama em madeira com mural de palmeiras',
            'Workspace with palm mural and wall TV':                        'Espaço de trabalho com mural e TV',
            'Bedroom with mountain mural and barn-style door':              'Quarto com mural de montanhas e porta de celeiro',
            'Bedroom with green window trim and single bed':                'Quarto com janela verde e cama de solteiro',
            'Bedroom with green windows and wall TV':                       'Quarto com janelas verdes e TV',
            'Bedroom with green window trim and workspace':                 'Quarto com janela verde e zona de trabalho',
            'Bedroom with rattan headboard':                                'Quarto com cabeceira em rattan',
            'Long bedroom with desk and shelves':                           'Quarto comprido com secretária e prateleiras',
            'Bedroom with green window trim and hangers':                   'Quarto com janela verde e cabides',
            'Workspace with desk and chair by window':                      'Zona de trabalho junto à janela',
            'Black desk with red chair and shelves':                        'Secretária preta com cadeira vermelha e prateleiras',
            'Dark-floor bedroom with orange chair':                         'Quarto com pavimento escuro e cadeira laranja',
            'Premium bathroom with backlit mirror and walnut vanity':       'Casa de banho premium com espelho retroiluminado',
            'Backlit round mirror bathroom detail':                         'Detalhe de casa de banho com espelho redondo',
            'Bathroom with curved shower and window':                       'Casa de banho com chuveiro curvo e janela',
            'Bathroom with balcony door':                                   'Casa de banho com porta de varanda',
            'Shower bathroom with balcony':                                 'Casa de banho com chuveiro e varanda',
            'Bathroom with rainfall shower and pink tiles':                 'Casa de banho com chuveiro tropical e azulejos rosa',
            'Bathroom with pink tiles and rounded shower':                  'Casa de banho com azulejos rosa',
            'Grey-tile bathroom with round mirror':                         'Casa de banho com azulejos cinza',
            'Bathroom with subway tile and walk-in shower':                 'Casa de banho com azulejos brancos',
            'Square shower bathroom':                                       'Casa de banho com chuveiro quadrado',
            'Bathroom with rounded shower':                                 'Casa de banho com chuveiro arredondado',
            'White subway-tile bathroom':                                   'Casa de banho clássica com azulejos brancos',
            'White-tile bathroom with framed art':                          'Casa de banho branca com arte emoldurada',
            'Minimal white-tile bathroom':                                  'Casa de banho minimalista',
            'Long narrow bathroom with shower':                             'Casa de banho estreita com chuveiro',
            'Bathroom with rounded shower and framed art':                  'Suíte de casa de banho',
            'Laundry room with washer and dryer':                           'Lavandaria',
            'Ground floor plan':                                            'Planta do rés-do-chão',
            'First floor plan':                                             'Planta do 1º andar',
        },
        'figcaptions': {
            'Aerial view': 'Vista aérea',
            'Front facade': 'Fachada frontal',
            'Side angle': 'Vista lateral',
            'Side passage': 'Passagem lateral',
            'Central hallway': 'Corredor central',
            'Upper hallway': 'Corredor superior',
            'Shared lounge': 'Lounge partilhado',
            'Lounge corner': 'Canto do lounge',
            'Shared kitchen': 'Cozinha partilhada',
            'Shared dining': 'Refeições partilhadas',
            'Lounge bar': 'Lounge bar',
            'Suite room': 'Suíte',
            'Geometric mural room': 'Quarto com mural geométrico',
            'Watercolor room': 'Quarto aguarela',
            'Palm wall room': 'Quarto com palmeiras',
            'Tropical mural room': 'Quarto tropical',
            'Wood-bed room': 'Quarto com cama de madeira',
            'Room workspace': 'Quarto com escritório',
            'Mountain mural room': 'Quarto com mural de montanhas',
            'Green-trim room': 'Quarto com janela verde',
            'Green-windows room': 'Quarto com janelas verdes',
            'Bright bedroom': 'Quarto luminoso',
            'Rattan bedroom': 'Quarto rattan',
            'Long bedroom': 'Quarto comprido',
            'Compact bedroom': 'Quarto compacto',
            'Study area': 'Zona de estudo',
            'Desk corner': 'Canto secretária',
            'Heritage bedroom': 'Quarto patrimonial',
            'Premium bathroom': 'Casa de banho premium',
            'Bathroom detail': 'Detalhe de casa de banho',
            'Shower with view': 'Chuveiro com vista',
            'Balcony bathroom': 'Casa de banho com varanda',
            'Open bathroom': 'Casa de banho aberta',
            'Rainfall shower': 'Chuveiro tropical',
            'Pink-tile bathroom': 'Casa de banho rosa',
            'Grey-tile bathroom': 'Casa de banho cinza',
            'Walk-in shower': 'Chuveiro walk-in',
            'Square shower': 'Chuveiro quadrado',
            'Rounded shower': 'Chuveiro arredondado',
            'Classic bathroom': 'Casa de banho clássica',
            'Bathroom with art': 'Casa de banho com arte',
            'Minimal bathroom': 'Casa de banho minimalista',
            'Galley bathroom': 'Casa de banho estreita',
            'Bathroom suite': 'Suíte de banho',
            'Laundry room': 'Lavandaria',
        },
        'aria': {
            'Open menu': 'Abrir menu',
            'Photo viewer': 'Visualizador de fotos',
            'Close': 'Fechar',
            'Previous': 'Anterior',
            'Next': 'Seguinte',
            'Primary': 'Principal',
            'Language': 'Idioma',
            'Gallery filters': 'Filtros da galeria',
        },
    },
    'de': {
        'title':       'Investitionsimmobilie in Anadia, Portugal · 790.000 € | Vila Anadia',
        'description': 'Vila Anadia: 393-m²-Investitionsimmobilie in Anadia, Portugal. 790.000 €. 8 Zimmer + T0 + T1 + privates T3, Garten, Parkplatz. Renditen bis zu ~14 %.',
        'ogTitle':     'Vila Anadia · 790.000 € — 10 Einheiten + Eigentümer-T3 in Anadia, Portugal',
        'ogDesc':      'Coliving- & Coworking-Immobilie in Anadia, Portugal. 393 m², 10 Einheiten + Eigentümer-T3. Renditen bis zu ~14 %.',
        'twTitle':     'Vila Anadia · 790.000 € — Anadia, Portugal',
        'twDesc':      '10 Einheiten + Eigentümer-T3 im Zentrum Portugals. Renditen bis zu ~14 %.',
        'ogLocale':    'de_DE',
        'ogLocaleAlt': 'en_US',
        'ogImageAlt':  'Außenansicht der Investitionsimmobilie in Anadia, Portugal',
        'inLang':      'de',
        'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Menü öffnen',
            'Primary':   'Hauptmenü',
            'Language':  'Sprache',
            'Gallery filters': 'Galeriefilter',
            'Photo viewer': 'Foto-Viewer',
            'Close': 'Schließen', 'Previous': 'Zurück', 'Next': 'Weiter',
        },
    },
    'fr': {
        'title':       "Bien d'Investissement à Anadia, Portugal · 790 000 € | Vila Anadia",
        'description': "Vila Anadia : bien d'investissement de 393 m² à Anadia, Portugal. 790 000 €. 8 chambres + T0 + T1 + T3 privé, jardin, parking. Rendements jusqu'à ~14 %.",
        'ogTitle':     'Vila Anadia · 790 000 € — 10 Unités + T3 propriétaire à Anadia, Portugal',
        'ogDesc':      "Bien de coliving & coworking à Anadia, Portugal. 393 m², 10 unités + T3 propriétaire. Rendements jusqu'à ~14 %.",
        'twTitle':     'Vila Anadia · 790 000 € — Anadia, Portugal',
        'twDesc':      "10 unités locatives + T3 propriétaire au centre du Portugal. Rendements jusqu'à ~14 %.",
        'ogLocale':    'fr_FR',
        'ogLocaleAlt': 'en_US',
        'ogImageAlt':  "Extérieur du bien d'investissement à Anadia, Portugal",
        'inLang':      'fr',
        'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Ouvrir le menu',
            'Primary':   'Principal',
            'Language':  'Langue',
            'Gallery filters': 'Filtres de galerie',
            'Photo viewer': 'Visionneuse de photos',
            'Close': 'Fermer', 'Previous': 'Précédent', 'Next': 'Suivant',
        },
    },
    'ru': {
        'title':       'Инвестиционная недвижимость в Анадии, Португалия · €790 000 | Vila Anadia',
        'description': 'Vila Anadia: инвестиционный объект 393 м² в Анадии, Португалия. €790 000. 8 комнат + T0 + T1 + приватная T3, сад, паркинг. Доходность до ~14%.',
        'ogTitle':     'Vila Anadia · €790 000 — 10 юнитов + T3 владельца в Анадии, Португалия',
        'ogDesc':      'Объект коливинга и коворкинга в Анадии, Португалия. 393 м², 10 юнитов + T3 владельца. Доходность до ~14%.',
        'twTitle':     'Vila Anadia · €790 000 — Анадия, Португалия',
        'twDesc':      '10 арендных юнитов + T3 владельца в центре Португалии. Доходность до ~14%.',
        'ogLocale':    'ru_RU',
        'ogLocaleAlt': 'en_US',
        'ogImageAlt':  'Внешний вид инвестиционной недвижимости в Анадии, Португалия',
        'inLang':      'ru',
        'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Открыть меню', 'Primary': 'Основное',
            'Language': 'Язык', 'Gallery filters': 'Фильтры галереи',
            'Photo viewer': 'Просмотр фото',
            'Close': 'Закрыть', 'Previous': 'Назад', 'Next': 'Вперёд',
        },
    },
    'uk': {
        'title':       'Інвестиційна нерухомість в Анадії, Португалія · €790 000 | Vila Anadia',
        'description': "Vila Anadia: інвестиційний об'єкт 393 м² в Анадії, Португалія. €790 000. 8 кімнат + T0 + T1 + приватний T3, сад, паркінг. Дохідність до ~14%.",
        'ogTitle':     'Vila Anadia · €790 000 — 10 юнітів + T3 власника в Анадії, Португалія',
        'ogDesc':      "Об'єкт коліверу та коворкінгу в Анадії, Португалія. 393 м², 10 юнітів + T3 власника. Дохідність до ~14%.",
        'twTitle':     'Vila Anadia · €790 000 — Анадія, Португалія',
        'twDesc':      '10 орендних юнітів + T3 власника в центрі Португалії. Дохідність до ~14%.',
        'ogLocale':    'uk_UA',
        'ogLocaleAlt': 'en_US',
        'ogImageAlt':  "Зовнішній вигляд інвестиційного об'єкта в Анадії, Португалія",
        'inLang':      'uk',
        'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Відкрити меню', 'Primary': 'Основне',
            'Language': 'Мова', 'Gallery filters': 'Фільтри галереї',
            'Photo viewer': 'Перегляд фото',
            'Close': 'Закрити', 'Previous': 'Назад', 'Next': 'Далі',
        },
    },
    'it': {
        'title':       "Immobile da Investimento ad Anadia, Portogallo · 790.000 € | Vila Anadia",
        'description': "Vila Anadia: immobile da investimento di 393 m² ad Anadia, Portogallo. 790.000 €. 8 camere + T0 + T1 + T3 privato, giardino, parcheggio. Rendimenti fino al ~14 %.",
        'ogTitle':     "Vila Anadia · 790.000 € — 10 unità + T3 proprietario ad Anadia, Portogallo",
        'ogDesc':      "Immobile coliving e coworking ad Anadia, Portogallo. 393 m², 10 unità + T3 proprietario. Rendimenti fino al ~14 %.",
        'twTitle':     'Vila Anadia · 790.000 € — Anadia, Portogallo',
        'twDesc':      "10 unità in affitto + T3 proprietario nel centro del Portogallo. Rendimenti fino al ~14 %.",
        'ogLocale': 'it_IT', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': "Esterno dell'immobile da investimento ad Anadia, Portogallo",
        'inLang': 'it', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Apri menu', 'Primary': 'Principale', 'Language': 'Lingua',
            'Gallery filters': 'Filtri galleria', 'Photo viewer': 'Visualizzatore foto',
            'Close': 'Chiudi', 'Previous': 'Precedente', 'Next': 'Successivo',
        },
    },
    'pl': {
        'title':       'Nieruchomość Inwestycyjna w Anadii, Portugalia · 790 000 € | Vila Anadia',
        'description': 'Vila Anadia: nieruchomość inwestycyjna 393 m² w Anadii, Portugalia. 790 000 €. 8 pokoi + T0 + T1 + prywatne T3, ogród, parking. Stopy zwrotu do ~14 %.',
        'ogTitle':     'Vila Anadia · 790 000 € — 10 jednostek + T3 właściciela w Anadii, Portugalia',
        'ogDesc':      'Nieruchomość coliving i coworking w Anadii, Portugalia. 393 m², 10 jednostek + T3 właściciela. Stopy zwrotu do ~14 %.',
        'twTitle':     'Vila Anadia · 790 000 € — Anadia, Portugalia',
        'twDesc':      '10 jednostek najmu + T3 właściciela w centrum Portugalii. Stopy zwrotu do ~14 %.',
        'ogLocale': 'pl_PL', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Zewnętrze nieruchomości inwestycyjnej w Anadii, Portugalia',
        'inLang': 'pl', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Otwórz menu', 'Primary': 'Główne', 'Language': 'Język',
            'Gallery filters': 'Filtry galerii', 'Photo viewer': 'Przeglądarka zdjęć',
            'Close': 'Zamknij', 'Previous': 'Wstecz', 'Next': 'Dalej',
        },
    },
    'el': {
        'title':       'Επενδυτικό Ακίνητο στην Ανάδια, Πορτογαλία · 790.000 € | Vila Anadia',
        'description': 'Vila Anadia: επενδυτικό ακίνητο 393 m² στην Ανάδια, Πορτογαλία. 790.000 €. 8 δωμάτια + T0 + T1 + ιδιωτικό T3, κήπος, πάρκινγκ. Αποδόσεις έως ~14 %.',
        'ogTitle':     'Vila Anadia · 790.000 € — 10 μονάδες + T3 ιδιοκτήτη στην Ανάδια, Πορτογαλία',
        'ogDesc':      'Ακίνητο coliving και coworking στην Ανάδια, Πορτογαλία. 393 m², 10 μονάδες + T3 ιδιοκτήτη. Αποδόσεις έως ~14 %.',
        'twTitle':     'Vila Anadia · 790.000 € — Ανάδια, Πορτογαλία',
        'twDesc':      '10 μονάδες ενοικίασης + T3 ιδιοκτήτη στο κέντρο της Πορτογαλίας. Αποδόσεις έως ~14 %.',
        'ogLocale': 'el_GR', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Εξωτερικό του επενδυτικού ακινήτου στην Ανάδια, Πορτογαλία',
        'inLang': 'el', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Άνοιγμα μενού', 'Primary': 'Κύριο', 'Language': 'Γλώσσα',
            'Gallery filters': 'Φίλτρα γκαλερί', 'Photo viewer': 'Προβολή φωτογραφιών',
            'Close': 'Κλείσιμο', 'Previous': 'Προηγούμενο', 'Next': 'Επόμενο',
        },
    },
    'ja': {
        'title':       'ポルトガル・アナディアの投資物件 · 79万ユーロ | Vila Anadia',
        'description': 'Vila Anadia：ポルトガル・アナディアの393㎡投資物件。79万ユーロ。8部屋+T0+T1+プライベートT3、庭園、駐車場。利回り最大約14%。',
        'ogTitle':     'Vila Anadia · 79万ユーロ — ポルトガル・アナディアの10ユニット+オーナーT3',
        'ogDesc':      'ポルトガル・アナディアのコリビング&コワーキング物件。393㎡、10ユニット+オーナーT3。利回り最大約14%。',
        'twTitle':     'Vila Anadia · 79万ユーロ — アナディア、ポルトガル',
        'twDesc':      'ポルトガル中部の13賃貸ユニット+オーナーT3。利回り最大約14%。',
        'ogLocale': 'ja_JP', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'ポルトガル・アナディアの投資物件の外観',
        'inLang': 'ja', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'メニューを開く', 'Primary': 'メイン', 'Language': '言語',
            'Gallery filters': 'ギャラリーフィルター', 'Photo viewer': '写真ビューア',
            'Close': '閉じる', 'Previous': '前へ', 'Next': '次へ',
        },
    },
    'ar': {
        'title':       'عقار استثماري في أنادييا، البرتغال · 790,000 € | Vila Anadia',
        'description': 'Vila Anadia: عقار استثماري 393 متر مربع في أنادييا، البرتغال. 790,000 €. 8 غرف + T0 + T1 + T3 خاص، حديقة، موقف. عوائد حتى ~14%.',
        'ogTitle':     'Vila Anadia · 790,000 € — 10 وحدة + T3 مالك في أنادييا، البرتغال',
        'ogDesc':      'عقار كوليفينج وكوويركينج في أنادييا، البرتغال. 393 متر مربع، 10 وحدة + T3 مالك. عوائد حتى ~14%.',
        'twTitle':     'Vila Anadia · 790,000 € — أنادييا، البرتغال',
        'twDesc':      '10 وحدة إيجار + T3 مالك في وسط البرتغال. عوائد حتى ~14%.',
        'ogLocale': 'ar_SA', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'الواجهة الخارجية للعقار الاستثماري في أنادييا، البرتغال',
        'inLang': 'ar', 'dir': 'rtl', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'فتح القائمة', 'Primary': 'رئيسي', 'Language': 'اللغة',
            'Gallery filters': 'فلاتر المعرض', 'Photo viewer': 'عارض الصور',
            'Close': 'إغلاق', 'Previous': 'السابق', 'Next': 'التالي',
        },
    },
    'no': {
        'title': 'Investeringseiendom i Anadia, Portugal · 790 000 € | Vila Anadia',
        'description': 'Vila Anadia: 393 m² investeringseiendom i Anadia, Portugal. 790 000 €. 8 rom + T0 + T1 + privat T3, hage, parkering. Avkastning opp til ~14 %.',
        'ogTitle': 'Vila Anadia · 790 000 € — 10 enheter + Eier-T3 i Anadia, Portugal',
        'ogDesc':  'Coliving- og coworking-eiendom i Anadia, Portugal. 393 m², 10 enheter + Eier-T3. Avkastning opp til ~14 %.',
        'twTitle': 'Vila Anadia · 790 000 € — Anadia, Portugal',
        'twDesc':  '10 utleieenheter + Eier-T3 i sentral-Portugal. Avkastning opp til ~14 %.',
        'ogLocale': 'nb_NO', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Eksteriør av investeringseiendommen i Anadia, Portugal',
        'inLang': 'no', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Åpne meny', 'Primary': 'Hoved', 'Language': 'Språk',
            'Gallery filters': 'Galleri-filtre', 'Photo viewer': 'Bildeviser',
            'Close': 'Lukk', 'Previous': 'Forrige', 'Next': 'Neste',
        },
    },
    'sv': {
        'title': 'Investeringsfastighet i Anadia, Portugal · 790 000 € | Vila Anadia',
        'description': 'Vila Anadia: 393 m² investeringsfastighet i Anadia, Portugal. 790 000 €. 8 rum + T0 + T1 + privat T3, trädgård, parkering. Avkastning upp till ~14 %.',
        'ogTitle': 'Vila Anadia · 790 000 € — 10 enheter + Ägar-T3 i Anadia, Portugal',
        'ogDesc':  'Coliving- och coworking-fastighet i Anadia, Portugal. 393 m², 10 enheter + Ägar-T3. Avkastning upp till ~14 %.',
        'twTitle': 'Vila Anadia · 790 000 € — Anadia, Portugal',
        'twDesc':  '10 hyresenheter + Ägar-T3 i centrala Portugal. Avkastning upp till ~14 %.',
        'ogLocale': 'sv_SE', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Exteriör av investeringsfastigheten i Anadia, Portugal',
        'inLang': 'sv', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Öppna meny', 'Primary': 'Huvud', 'Language': 'Språk',
            'Gallery filters': 'Galleri-filter', 'Photo viewer': 'Bildvisare',
            'Close': 'Stäng', 'Previous': 'Föregående', 'Next': 'Nästa',
        },
    },
    'da': {
        'title': 'Investeringsejendom i Anadia, Portugal · 790.000 € | Vila Anadia',
        'description': 'Vila Anadia: 393 m² investeringsejendom i Anadia, Portugal. 790.000 €. 8 værelser + T0 + T1 + privat T3, have, parkering. Afkast op til ~14 %.',
        'ogTitle': 'Vila Anadia · 790.000 € — 10 enheder + Ejer-T3 i Anadia, Portugal',
        'ogDesc':  'Coliving- og coworking-ejendom i Anadia, Portugal. 393 m², 10 enheder + Ejer-T3. Afkast op til ~14 %.',
        'twTitle': 'Vila Anadia · 790.000 € — Anadia, Portugal',
        'twDesc':  '10 lejeenheder + Ejer-T3 i det centrale Portugal. Afkast op til ~14 %.',
        'ogLocale': 'da_DK', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Eksteriør af investeringsejendommen i Anadia, Portugal',
        'inLang': 'da', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Åbn menu', 'Primary': 'Hoved', 'Language': 'Sprog',
            'Gallery filters': 'Galleri-filtre', 'Photo viewer': 'Billedviser',
            'Close': 'Luk', 'Previous': 'Forrige', 'Next': 'Næste',
        },
    },
    'nl': {
        'title': 'Investeringspand in Anadia, Portugal · 790.000 € | Vila Anadia',
        'description': 'Vila Anadia: 393 m² investeringspand in Anadia, Portugal. 790.000 €. 8 kamers + T0 + T1 + privé T3, tuin, parking. Rendement tot ~14 %.',
        'ogTitle': 'Vila Anadia · 790.000 € — 10 units + Eigenaars-T3 in Anadia, Portugal',
        'ogDesc':  'Coliving- en coworking-pand in Anadia, Portugal. 393 m², 10 units + Eigenaars-T3. Rendement tot ~14 %.',
        'twTitle': 'Vila Anadia · 790.000 € — Anadia, Portugal',
        'twDesc':  '10 huurunits + Eigenaars-T3 in Centraal-Portugal. Rendement tot ~14 %.',
        'ogLocale': 'nl_NL', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Buitenkant van het investeringspand in Anadia, Portugal',
        'inLang': 'nl', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Menu openen', 'Primary': 'Hoofd', 'Language': 'Taal',
            'Gallery filters': 'Galerij-filters', 'Photo viewer': 'Fotoweergave',
            'Close': 'Sluiten', 'Previous': 'Vorige', 'Next': 'Volgende',
        },
    },
    'hu': {
        'title': 'Befektetési Ingatlan Anadiában, Portugália · 790 000 € | Vila Anadia',
        'description': 'Vila Anadia: 393 m²-es befektetési ingatlan Anadiában, Portugália. 790 000 €. 8 szoba + T0 + T1 + privát T3, kert, parkoló. Hozam akár ~14 %.',
        'ogTitle': 'Vila Anadia · 790 000 € — 10 egység + Tulajdonosi T3 Anadiában, Portugália',
        'ogDesc':  'Coliving és coworking ingatlan Anadiában, Portugália. 393 m², 10 egység + Tulajdonosi T3. Hozam akár ~14 %.',
        'twTitle': 'Vila Anadia · 790 000 € — Anadia, Portugália',
        'twDesc':  '10 bérleti egység + Tulajdonosi T3 Közép-Portugáliában. Hozam akár ~14 %.',
        'ogLocale': 'hu_HU', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'A befektetési ingatlan külseje Anadiában, Portugália',
        'inLang': 'hu', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Menü megnyitása', 'Primary': 'Fő', 'Language': 'Nyelv',
            'Gallery filters': 'Galéria szűrők', 'Photo viewer': 'Fotónéző',
            'Close': 'Bezárás', 'Previous': 'Előző', 'Next': 'Következő',
        },
    },
    'bg': {
        'title': 'Инвестиционен имот в Анадия, Португалия · 790 000 € | Vila Anadia',
        'description': 'Vila Anadia: 393 m² инвестиционен имот в Анадия, Португалия. 790 000 €. 8 стаи + T0 + T1 + частен T3, градина, паркинг. Доходност до ~14 %.',
        'ogTitle': 'Vila Anadia · 790 000 € — 10 единици + T3 на собственика в Анадия, Португалия',
        'ogDesc':  'Имот за коливинг и коуъркинг в Анадия, Португалия. 393 m², 10 единици + T3 на собственика. Доходност до ~14 %.',
        'twTitle': 'Vila Anadia · 790 000 € — Анадия, Португалия',
        'twDesc':  '10 единици за наем + T3 на собственика в централна Португалия. Доходност до ~14 %.',
        'ogLocale': 'bg_BG', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Външен вид на инвестиционния имот в Анадия, Португалия',
        'inLang': 'bg', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Отвори меню', 'Primary': 'Основно', 'Language': 'Език',
            'Gallery filters': 'Филтри галерия', 'Photo viewer': 'Преглед на снимки',
            'Close': 'Затвори', 'Previous': 'Предишно', 'Next': 'Следващо',
        },
    },
    'ro': {
        'title': 'Proprietate de Investiție în Anadia, Portugalia · 790.000 € | Vila Anadia',
        'description': 'Vila Anadia: proprietate de investiție de 393 m² în Anadia, Portugalia. 790.000 €. 8 camere + T0 + T1 + T3 privat, grădină, parcare. Randament până la ~14 %.',
        'ogTitle': 'Vila Anadia · 790.000 € — 10 unități + T3 proprietar în Anadia, Portugalia',
        'ogDesc':  'Proprietate de coliving și coworking în Anadia, Portugalia. 393 m², 10 unități + T3 proprietar. Randament până la ~14 %.',
        'twTitle': 'Vila Anadia · 790.000 € — Anadia, Portugalia',
        'twDesc':  '10 unități de închiriere + T3 proprietar în centrul Portugaliei. Randament până la ~14 %.',
        'ogLocale': 'ro_RO', 'ogLocaleAlt': 'en_US',
        'ogImageAlt': 'Exteriorul proprietății de investiție în Anadia, Portugalia',
        'inLang': 'ro', 'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Deschide meniu', 'Primary': 'Principal', 'Language': 'Limbă',
            'Gallery filters': 'Filtre galerie', 'Photo viewer': 'Vizualizator foto',
            'Close': 'Închide', 'Previous': 'Înapoi', 'Next': 'Înainte',
        },
    },
    'es': {
        'title':       'Inmueble de Inversión en Anadia, Portugal · 790.000 € | Vila Anadia',
        'description': 'Vila Anadia: inmueble de 393 m² para inversión en Anadia, Portugal. 790.000 €. 8 habitaciones + T0 + T1 + T3 privado, jardín, aparcamiento. Rentabilidad hasta ~14 %.',
        'ogTitle':     'Vila Anadia · 790.000 € — 10 unidades + T3 del propietario en Anadia, Portugal',
        'ogDesc':      'Inmueble de coliving y coworking en Anadia, Portugal. 393 m², 10 unidades + T3. Rentabilidad hasta ~14 %.',
        'twTitle':     'Vila Anadia · 790.000 € — Anadia, Portugal',
        'twDesc':      '10 unidades de alquiler + T3 del propietario en el centro de Portugal. Rentabilidad hasta ~14 %.',
        'ogLocale':    'es_ES',
        'ogLocaleAlt': 'en_US',
        'ogImageAlt':  'Exterior del inmueble de inversión en Anadia, Portugal',
        'inLang':      'es',
        'imgAlts': {}, 'figcaptions': {}, 'aria': {
            'Open menu': 'Abrir menú',
            'Primary':   'Principal',
            'Language':  'Idioma',
            'Gallery filters': 'Filtros de galería',
            'Photo viewer': 'Visor de fotos',
            'Close': 'Cerrar', 'Previous': 'Anterior', 'Next': 'Siguiente',
        },
    },
}

def build(lang: str, out_dir: pathlib.Path):
    src = SRC.read_text(encoding='utf-8')
    dict_ = I18N[lang]
    meta = META[lang]

    # 1. Make all relative asset paths absolute (so they resolve from /pt/)
    src = re.sub(r'src="images/', 'src="/images/', src)
    src = re.sub(r'srcset="images/', 'srcset="/images/', src)
    src = re.sub(r'href="styles\.css"', 'href="/styles.css"', src)
    src = re.sub(r'src="script\.js"', 'src="/script.js"', src)

    # 2. Replace data-i18n text content
    def replace_text(m):
        tag_open, key, inner, tag_close = m.group(1), m.group(2), m.group(3), m.group(4)
        new_text = dict_.get(key, inner)
        return f'{tag_open}data-i18n="{key}">{html_mod.escape(new_text, quote=False)}{tag_close}'

    src = re.sub(
        r'(<[^>]+\s)data-i18n="([^"]+)">([^<]*)(</[^>]+>)',
        replace_text, src
    )

    # 3. Replace data-i18n-html innerHTML
    def replace_html(m):
        tag_open, key, inner, tag_close = m.group(1), m.group(2), m.group(3), m.group(4)
        new_html = dict_.get(key, inner)
        return f'{tag_open}data-i18n-html="{key}">{new_html}{tag_close}'

    src = re.sub(
        r'(<[^>]+\s)data-i18n-html="([^"]+)">(.*?)(</[^>]+>)',
        replace_html, src, flags=re.DOTALL
    )

    # 4. Replace data-i18n-attr-* attribute values
    def replace_attr(m):
        attr_name, key = m.group(1), m.group(2)
        # Find the corresponding placeholder/etc attribute and rewrite it
        # Just leave the data-i18n-attr-* attribute and rewrite the target attribute on the same element via a separate pass
        return m.group(0)
    # For placeholders specifically (most common case): rewrite placeholder="..." when adjacent to data-i18n-attr-placeholder
    def fix_placeholder(m):
        full = m.group(0)
        key = m.group(1)
        new_val = dict_.get(key)
        if new_val is None: return full
        # Replace the placeholder attribute that comes just before data-i18n-attr-placeholder
        return re.sub(r'placeholder="[^"]*"',
                      f'placeholder="{html_mod.escape(new_val, quote=True)}"', full)
    src = re.sub(r'placeholder="[^"]*"\s+data-i18n-attr-placeholder="([^"]+)"',
                 fix_placeholder, src)

    # 5. Translate gallery alt text and figcaptions
    for en_alt, pt_alt in meta['imgAlts'].items():
        src = src.replace(f'alt="{en_alt}"', f'alt="{html_mod.escape(pt_alt, quote=True)}"')
    for en_cap, pt_cap in meta['figcaptions'].items():
        src = src.replace(f'<figcaption>{en_cap}</figcaption>',
                          f'<figcaption>{html_mod.escape(pt_cap, quote=False)}</figcaption>')
    for en_aria, pt_aria in meta['aria'].items():
        src = src.replace(f'aria-label="{en_aria}"', f'aria-label="{html_mod.escape(pt_aria, quote=True)}"')

    # 6. Update <html lang="">  (add dir="rtl" for RTL languages)
    dir_attr = f' dir="{meta["dir"]}"' if meta.get('dir') else ''
    src = re.sub(r'<html lang="[^"]*"[^>]*>', f'<html lang="{lang}"{dir_attr}>', src)

    # 7. Update <title>
    src = re.sub(r'<title>[^<]*</title>',
                 f'<title>{html_mod.escape(meta["title"], quote=False)}</title>', src)

    # 8. Update meta description / og / twitter / canonical / hreflang
    def set_meta(name, value, scope='name'):
        nonlocal src
        pattern = rf'<meta {scope}="{name}" content="[^"]*"'
        src = re.sub(pattern, f'<meta {scope}="{name}" content="{html_mod.escape(value, quote=True)}"', src)

    set_meta('description', meta['description'])
    set_meta('og:title',       meta['ogTitle'],     scope='property')
    set_meta('og:description', meta['ogDesc'],      scope='property')
    set_meta('og:locale',      meta['ogLocale'],    scope='property')
    set_meta('og:locale:alternate', meta['ogLocaleAlt'], scope='property')
    set_meta('og:image:alt',   meta['ogImageAlt'],  scope='property')
    set_meta('og:url',         f'https://vilaanadia.com/{lang}/', scope='property')
    set_meta('twitter:title',       meta['twTitle'])
    set_meta('twitter:description', meta['twDesc'])

    # canonical
    src = re.sub(
        r'<link rel="canonical" href="[^"]*"\s*/>',
        f'<link rel="canonical" href="https://vilaanadia.com/{lang}/" />', src
    )
    # hreflang block: keep as-is (already points to ?lang=). Add path-based variants too.
    # Update inLanguage in JSON-LD
    src = re.sub(r'"inLanguage": "[^"]*"', f'"inLanguage": "{meta["inLang"]}"', src)

    # Update og:url to use path-based URL
    # (already done above)

    # Update language switcher: PT button gets is-active, EN doesn't
    if lang == 'pt':
        src = src.replace(
            '<button type="button" class="lang-switch__btn is-active" data-lang="en"',
            '<button type="button" class="lang-switch__btn" data-lang="en"'
        )
        src = src.replace(
            '<button type="button" class="lang-switch__btn" data-lang="pt"',
            '<button type="button" class="lang-switch__btn is-active" data-lang="pt"'
        )

    # Write
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'index.html').write_text(src, encoding='utf-8')
    print(f'Wrote {out_dir}/index.html ({len(src):,} bytes, lang={lang})')


if __name__ == '__main__':
    for lang in ('pt', 'de', 'fr', 'es', 'ru', 'uk', 'it', 'pl', 'el', 'ja', 'ar',
                 'no', 'sv', 'da', 'nl', 'hu', 'bg', 'ro'):
        build(lang, ROOT / lang)
