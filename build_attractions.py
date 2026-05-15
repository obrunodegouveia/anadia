#!/usr/bin/env python3
"""Generate /pt/atracoes/ hub + 5 topic sub-pages.

Each sub-page is a standalone HTML file sharing nav, footer, CSS and JS
with the main site. Content is unique Portuguese, focused on local SEO.
"""
import pathlib, html as html_mod, json

ROOT = pathlib.Path(__file__).parent
OUT  = ROOT / 'pt' / 'atracoes'

# ─── Page definitions ────────────────────────────────────────────────────
PAGES = {
    'index': {
        'slug': '',
        'title': 'Atrações de Anadia e Bairrada — Guia Completo | Vila Anadia',
        'description': 'Guia completo de Anadia e da Bairrada: vinhos, Termas da Curia, CAR Anadia, leitão à bairrada, e atrações a 1 hora — Coimbra, Aveiro, Buçaco e praias atlânticas.',
        'h1': 'Atrações de Anadia e Bairrada',
        'kicker': 'Guia turístico',
        'lead': 'Anadia, no centro de Portugal, é o coração da região vinícola da Bairrada. Em poucos quilómetros encontra caves históricas de espumante, termas centenárias, o principal centro de ciclismo do país, restaurantes de leitão à bairrada, e cidades como Coimbra e Aveiro a meia hora. Este guia reúne tudo o que pode visitar.',
        'sections': [
            ('hub', None),  # special: render the cards grid
        ],
    },

    'vinhos-bairrada': {
        'slug': 'vinhos-bairrada',
        'title': 'Vinhos da Bairrada — Caves e Quintas em Anadia | Vila Anadia',
        'description': 'Caves Aliança, Caves São João, Quinta do Encontro, Estação Vitivinícola: as caves e quintas históricas da Bairrada, em Anadia. Roteiro de provas e visitas.',
        'h1': 'Vinhos da Bairrada — Caves e Quintas',
        'kicker': 'Vinho · Bairrada',
        'lead': 'A Bairrada é uma das regiões vinícolas mais distintas de Portugal — famosa pelos espumantes pelo método clássico e pelos tintos da casta Baga. Várias das suas caves mais importantes estão em pleno concelho de Anadia, sobretudo nas freguesias de Sangalhos e São Lourenço do Bairro.',
        'sections': [
            ('text', '''<h2>A região demarcada da Bairrada</h2>
<p>A <a href="https://pt.wikipedia.org/wiki/Bairrada" target="_blank" rel="noopener">Região Demarcada da Bairrada</a> foi formalmente criada em 1979, mas as suas tradições vinícolas remontam ao século XVIII. Estende-se entre o oceano Atlântico e a Serra do Caramulo, abrangendo os concelhos de Anadia, Mealhada, Cantanhede, Oliveira do Bairro, Vagos, Águeda e parte de Coimbra. A casta Baga (tinta) e a Maria Gomes (branca) dominam as vinhas, em solos argilo-calcários únicos.</p>
<p>A <a href="https://www.bairrada.pt/" target="_blank" rel="noopener">Comissão Vitivinícola da Bairrada</a> (CVR) certifica produtores e mantém o portal oficial dos Vinhos da Bairrada — incluindo a Rota dos Vinhos com mais de uma dúzia de caves visitáveis.</p>'''),
            ('text', '''<h2>Caves Aliança e Aliança Underground Museum</h2>
<p>Em Sangalhos, freguesia de Anadia, as <strong>Caves Aliança</strong> são uma das maiores produtoras de espumante de Portugal — fundadas em 1927. Em 2010 inauguraram o impressionante <em>Aliança Underground Museum</em>, instalado nas galerias subterrâneas onde repousam milhões de garrafas. O museu reúne mais de 7 000 peças que vão desde arte africana, fósseis, minerais e cerâmica precolombiana até artefactos arqueológicos portugueses — uma das visitas mais surpreendentes da região.</p>
<p>Os bilhetes incluem prova de espumante. Visitas guiadas em português e inglês.</p>'''),
            ('text', '''<h2>Caves São João</h2>
<p>Fundadas em 1920 em São Lourenço do Bairro (Anadia), as <a href="https://www.cavessaojoao.com/" target="_blank" rel="noopener">Caves São João</a> são uma referência absoluta nos tintos da casta Baga de longa guarda. A casa mantém uma garrafeira histórica com vinhos de mais de 50 anos. Visita técnica e prova mediante marcação.</p>'''),
            ('text', '''<h2>Quinta do Encontro</h2>
<p>A <a href="https://www.quintadoencontro.pt/" target="_blank" rel="noopener">Quinta do Encontro</a>, em Sangalhos, é uma das quintas mais arquitetonicamente premiadas da Bairrada. Pertence ao grupo Niepoort e produz tintos modernos com a casta Baga reinterpretada. Provas guiadas, restaurante e enoturismo de excelência.</p>'''),
            ('text', '''<h2>Estação Vitivinícola da Bairrada</h2>
<p>A <strong>Estação Vitivinícola da Bairrada</strong>, em Anadia, foi fundada em 1887 e é a mais antiga estação de investigação vitivinícola de Portugal. Hoje afecta ao INIAV, mantém um papel central na investigação aplicada à viticultura. As instalações históricas são uma referência arquitetónica do século XIX.</p>'''),
            ('text', '''<h2>Roteiro de prova sugerido</h2>
<p>Um dia perfeito de enoturismo na Bairrada a partir de Vila Anadia:</p>
<ul>
  <li><strong>Manhã:</strong> Aliança Underground Museum (Sangalhos) — visita guiada com prova de espumante.</li>
  <li><strong>Almoço:</strong> Restaurante de leitão na Mealhada (10 min), acompanhado por espumante Bairrada.</li>
  <li><strong>Tarde:</strong> Quinta do Encontro — prova de tintos Baga e visita à arquitetura.</li>
  <li><strong>Fim de tarde:</strong> Caves São João — garrafeira histórica.</li>
</ul>'''),
        ],
    },

    'curia-termas': {
        'slug': 'curia-termas',
        'title': 'Termas da Curia, Anadia — Spa Histórico em Portugal | Vila Anadia',
        'description': 'Termas da Curia: estação termal histórica desde 1898, Curia Palace Hotel Art Nouveau e Parque da Curia. A 5 minutos de Vila Anadia.',
        'h1': 'Termas da Curia — Spa Histórico em Anadia',
        'kicker': 'Termas · Spa',
        'lead': 'A vila termal da Curia, freguesia de Anadia, é um dos destinos termais mais antigos e bonitos de Portugal. As suas águas medicinais começaram a ser exploradas em 1898 e atraem hoje visitantes para tratamentos de saúde e bem-estar — num enquadramento Art Nouveau preservado.',
        'sections': [
            ('text', '''<h2>Águas medicinais da Curia</h2>
<p>As <a href="https://www.termasdacuria.com/" target="_blank" rel="noopener">Termas da Curia</a> exploram águas hipossalinas, gasosas, bicarbonatadas-cálcicas, fortemente mineralizadas. Estão indicadas para problemas digestivos, do aparelho urinário e dermatológicos. Os primeiros estudos científicos das águas datam de 1898; a exploração comercial começou pouco depois e nunca mais parou.</p>
<p>As <a href="https://pt.wikipedia.org/wiki/Termas_da_Curia" target="_blank" rel="noopener">Termas da Curia</a> oferecem programas de uma manhã, pacotes de fim de semana e tratamentos de longa duração com prescrição médica.</p>'''),
            ('text', '''<h2>Curia Palace Hotel</h2>
<p>O <strong>Curia Palace Hotel</strong>, inaugurado em 1926, é um dos exemplos mais fotografados de arquitetura Art Nouveau em Portugal. Implantado em pleno parque das termas, com mais de 100 quartos, restaurante histórico, piscina exterior, court de ténis e salão de baile original. É hoje uma das opções de alojamento histórico mais procuradas da região.</p>'''),
            ('text', '''<h2>Parque da Curia</h2>
<p>O <strong>Parque da Curia</strong> tem cerca de 14 hectares de jardins, mata, lago navegável (com botes) e equipamentos desportivos — courts de ténis, mini-golfe, parque infantil, percursos pedestres. Aberto ao público todo o ano, é um excelente passeio para famílias.</p>'''),
            ('text', '''<h2>Quando visitar</h2>
<p>A época termal vai tipicamente de março a novembro. Os meses de verão (junho a setembro) são os mais movimentados, com programação cultural no parque e no hotel. Para quem procura tranquilidade, abril/maio e outubro são meses excelentes — clima ameno e menos visitantes.</p>'''),
        ],
    },

    'desporto-car-anadia': {
        'slug': 'desporto-car-anadia',
        'title': 'CAR Anadia — Centro de Alto Rendimento de Ciclismo | Vila Anadia',
        'description': 'Centro de Alto Rendimento de Anadia: velódromo nacional UCI, pista internacional de BMX, sede da Federação Portuguesa de Ciclismo. Em Sangalhos, Anadia.',
        'h1': 'CAR Anadia — Centro de Alto Rendimento de Ciclismo',
        'kicker': 'Desporto · Ciclismo',
        'lead': 'Anadia é, sem rival, a capital nacional do ciclismo de pista. O Centro de Alto Rendimento (CAR) de Anadia, em Sangalhos, é a sede da Federação Portuguesa de Ciclismo e a única infraestrutura do país com pista coberta homologada pela UCI.',
        'sections': [
            ('text', '''<h2>Velódromo Nacional de Sangalhos</h2>
<p>O Velódromo Nacional, integrado no CAR Anadia, é a única pista coberta de ciclismo em Portugal homologada pela <em>Union Cycliste Internationale</em> (UCI). Com 250 metros de extensão e bancada para mais de 2 000 espectadores, recebe regularmente provas internacionais — incluindo etapas da Taça das Nações UCI Júnior, campeonatos europeus e provas internas portuguesas.</p>'''),
            ('text', '''<h2>Pista Internacional de BMX</h2>
<p>O CAR inclui também uma pista internacional de BMX e zonas técnicas para preparação de atletas de elite. As infraestruturas são utilizadas pela seleção nacional, clubes portugueses e equipas estrangeiras em estágio.</p>'''),
            ('text', '''<h2>Federação Portuguesa de Ciclismo</h2>
<p>A <a href="https://www.fpciclismo.pt/" target="_blank" rel="noopener">Federação Portuguesa de Ciclismo</a> tem aqui a sua sede operacional. Calendário de provas, escolas de formação e seleções nacionais estão centralizadas em Anadia.</p>'''),
            ('text', '''<h2>Hospedagem para atletas e visitantes</h2>
<p>O concelho de Anadia oferece infraestrutura de alojamento que serve não só visitantes turísticos mas também equipas e atletas em concentração. Para quem invista em alojamento perto do CAR, a procura é constante ao longo do ano — ciclistas, treinadores, famílias e equipas técnicas.</p>'''),
        ],
    },

    'gastronomia-leitao': {
        'slug': 'gastronomia-leitao',
        'title': 'Leitão à Bairrada — Gastronomia de Anadia e Mealhada | Vila Anadia',
        'description': 'Leitão à Bairrada: a tradição gastronómica icónica de Anadia e Mealhada. Onde comer, harmonização com espumante Bairrada e Confraria do Leitão.',
        'h1': 'Leitão à Bairrada — A Gastronomia da Região',
        'kicker': 'Gastronomia',
        'lead': 'O Leitão à Bairrada é, talvez, o ícone gastronómico mais reconhecido do centro de Portugal. Anadia e a vizinha Mealhada concentram dezenas de restaurantes especializados — uma tradição que mistura técnica de forno a lenha, tempero próprio e harmonização perfeita com o espumante Bairrada local.',
        'sections': [
            ('text', '''<h2>O que é o Leitão à Bairrada</h2>
<p>O <a href="https://pt.wikipedia.org/wiki/Leit%C3%A3o_%C3%A0_Bairrada" target="_blank" rel="noopener">Leitão à Bairrada</a> é um leitão (porco bebé com cerca de 6-8 kg) assado inteiro em forno a lenha, temperado com uma pasta tradicional de pimenta, alho, sal e banha — segundo receitas guardadas há gerações. A pele fica estaladiça e dourada, a carne suculenta e perfumada. Servido em fatias com batata frita, salada e o tradicional molho de pimenta.</p>'''),
            ('text', '''<h2>Onde comer — Mealhada e Sangalhos</h2>
<p>A <a href="https://www.cm-mealhada.pt/" target="_blank" rel="noopener">Mealhada</a>, a 10 minutos de Anadia, é considerada a "capital portuguesa do leitão" — concentra dezenas de restaurantes em poucos quilómetros, todos especializados. Em Sangalhos (Anadia) e na Curia também há casas históricas dedicadas exclusivamente ao leitão.</p>
<p>Restaurantes recomendados (Mealhada e Anadia): Pedro dos Leitões, Mugasa, Hilário, Casa do Leitão, Os 3 Pastorinhos. Os preços rondam 18-25 € por pessoa.</p>'''),
            ('text', '''<h2>Harmonização — Espumante Bairrada</h2>
<p>O par perfeito é incontornável: leitão com espumante Bairrada. A acidez do espumante (frequentemente da casta Maria Gomes ou Baga vinificada em branco) corta a gordura do leitão e refresca o palato. Várias caves de Anadia produzem espumantes específicos para esta harmonização.</p>'''),
            ('text', '''<h2>Confraria do Leitão da Bairrada</h2>
<p>A <strong>Confraria Gastronómica do Leitão à Bairrada</strong> é a entidade que promove e certifica os restaurantes que respeitam a tradição. A sua chancela é uma garantia de qualidade e autenticidade — vale a pena procurá-la antes de escolher onde comer.</p>'''),
        ],
    },

    'cidades-praias': {
        'slug': 'cidades-praias',
        'title': 'Coimbra, Aveiro, Buçaco e Praias — Próximas de Anadia | Vila Anadia',
        'description': 'A 1 hora de Anadia: Coimbra (UNESCO), Aveiro (canais), Mata do Buçaco, Conímbriga romana, Costa Nova e Praia da Tocha.',
        'h1': 'Próximas de Anadia — Cidades, Praias e Património',
        'kicker': 'Excursões',
        'lead': 'Anadia é uma base ideal para explorar o centro de Portugal. Em menos de uma hora chega à universidade património mundial de Coimbra, aos canais de Aveiro, à floresta histórica do Buçaco, ao maior sítio romano do país (Conímbriga) e às praias atlânticas. Eis o que vale uma viagem de dia.',
        'sections': [
            ('text', '''<h2>Coimbra — ~30 minutos</h2>
<p>A cidade de <a href="https://www.cm-coimbra.pt/" target="_blank" rel="noopener">Coimbra</a> é uma das mais importantes capitais culturais de Portugal. A <a href="https://www.uc.pt/" target="_blank" rel="noopener">Universidade de Coimbra</a> — Alta e Sofia — está classificada como Património Mundial da UNESCO desde 2013. Imperdível: a Biblioteca Joanina (uma das mais belas do mundo), a Capela de São Miguel, o Pátio das Escolas e o tradicional Fado de Coimbra.</p>
<p>A cidade tem ainda a Sé Velha, o Mosteiro de Santa Cruz, a Quinta das Lágrimas e o Portugal dos Pequenitos — ideal para crianças.</p>'''),
            ('text', '''<h2>Aveiro — ~30 minutos</h2>
<p>Conhecida como a "Veneza portuguesa", <a href="https://www.cm-aveiro.pt/" target="_blank" rel="noopener">Aveiro</a> destaca-se pelos seus canais, moliceiros (barcos coloridos tradicionais), arquitetura Art Nouveau e ovos-moles (doce conventual icónico). A passeio de moliceiro pelos canais é obrigatório. A salina ainda em funcionamento, o Museu de Aveiro, a estação de comboios com painéis de azulejos e a Fábrica da Ciência completam o programa.</p>'''),
            ('text', '''<h2>Mata Nacional do Buçaco — ~20 minutos</h2>
<p>A <a href="https://pt.wikipedia.org/wiki/Mata_Nacional_do_Bu%C3%A7aco" target="_blank" rel="noopener">Mata Nacional do Buçaco</a> é uma floresta sagrada com mais de 700 espécies arbóreas plantadas pelos monges carmelitas a partir do século XVII. No seu coração ergue-se o impressionante <a href="https://pt.wikipedia.org/wiki/Pal%C3%A1cio_Hotel_do_Bu%C3%A7aco" target="_blank" rel="noopener">Palácio Hotel do Buçaco</a> em estilo neomanuelino — antiga residência real, hoje hotel de luxo. Imperdível: a Via Sacra, as fontes, o miradouro da Cruz Alta. Gerido pelo <a href="https://www.icnf.pt/" target="_blank" rel="noopener">ICNF</a>.</p>'''),
            ('text', '''<h2>Conímbriga — ~40 minutos</h2>
<p>O <strong>Sítio Arqueológico de Conímbriga</strong> é o maior sítio romano em Portugal — uma cidade luso-romana com mosaicos extraordinariamente bem preservados, termas, casas patrícias e muralhas. O museu monográfico contextualiza tudo. Visita altamente recomendada para quem se interessa por história ou arqueologia.</p>'''),
            ('text', '''<h2>Praia da Costa Nova — ~40 minutos</h2>
<p>A <a href="https://pt.wikipedia.org/wiki/Costa_Nova_do_Prado" target="_blank" rel="noopener">Costa Nova</a> é uma das praias mais fotografadas de Portugal — famosa pelos palheiros (casas de pescadores listradas em cores vivas). Praia atlântica extensa, ideal para passeios; restaurantes de marisco frescos, surf, e ria de Aveiro nas traseiras.</p>'''),
            ('text', '''<h2>Praia da Tocha — ~30 minutos</h2>
<p>A <strong>Praia da Tocha</strong> é uma alternativa mais tranquila à Costa Nova — ideal para famílias. Praia atlântica de areia branca, com palheiros típicos, dunas e restaurantes locais.</p>'''),
            ('text', '''<h2>Aeroportos</h2>
<p><strong>Aeroporto Francisco Sá Carneiro (Porto)</strong> — cerca de 1h por A1. <strong>Aeroporto Humberto Delgado (Lisboa)</strong> — cerca de 2h. Conexões internacionais diárias para toda a Europa, América e África.</p>'''),
        ],
    },
}

# ─── HTML template ───────────────────────────────────────────────────────
HEAD_TMPL = '''<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#0f1b2d" />
  <link rel="canonical" href="https://vilaanadia.com/pt/atracoes/{slug_path}" />
  <link rel="alternate" hreflang="pt" href="https://vilaanadia.com/pt/atracoes/{slug_path}" />
  <link rel="alternate" hreflang="x-default" href="https://vilaanadia.com/" />

  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Vila Anadia" />
  <meta property="og:url" content="https://vilaanadia.com/pt/atracoes/{slug_path}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="https://vilaanadia.com/images/photo-44.jpg" />
  <meta property="og:locale" content="pt_PT" />

  <link rel="icon" href="data:image/svg+xml,&lt;svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22&gt;&lt;rect width=%2264%22 height=%2264%22 rx=%2212%22 fill=%22%230f1b2d%22/&gt;&lt;text x=%2232%22 y=%2244%22 font-family=%22Georgia%22 font-size=%2240%22 fill=%22%23fff%22 text-anchor=%22middle%22&gt;A&lt;/text&gt;&lt;/svg&gt;" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {headline_json},
    "description": {description_json},
    "inLanguage": "pt",
    "mainEntityOfPage": "https://vilaanadia.com/pt/atracoes/{slug_path}",
    "publisher": {{ "@type": "Organization", "name": "Vila Anadia", "url": "https://vilaanadia.com/" }},
    "image": "https://vilaanadia.com/images/photo-44.jpg"
  }}
  </script>
</head>
<body>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>

  <header class="nav" id="nav">
    <div class="container nav__inner">
      <a href="/pt/" class="nav__brand">
        <span class="nav__brand-mark">A</span>
        <span class="nav__brand-text">Vila&nbsp;Anadia</span>
      </a>
      <nav class="nav__links" aria-label="Principal">
        <a href="/pt/#highlights">Destaques</a>
        <a href="/pt/#investment">Investimento</a>
        <a href="/pt/#layout">Planta</a>
        <a href="/pt/alojamento-anadia/">Alojamento</a>
        <a href="/pt/atracoes/" class="is-active">Atrações</a>
      </nav>
      <button type="button" class="lang-trigger" id="langTrigger" aria-haspopup="dialog" aria-label="Escolher idioma">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20"/><path d="M12 2a15 15 0 0 0 0 20"/>
        </svg>
        <span class="lang-trigger__code" id="langTriggerCode">PT</span>
      </button>
      <a href="/pt/#contact" class="btn btn--primary nav__cta">Pedir Informação</a>
      <button class="nav__toggle" aria-label="Abrir menu" id="navToggle">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <section class="subpage-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/pt/">Vila Anadia</a>
        <span>›</span>
        <a href="/pt/atracoes/">Atrações</a>
        {breadcrumb_extra}
      </nav>
      <span class="kicker">{kicker}</span>
      <h1>{h1}</h1>
      <p class="subpage-hero__lead">{lead}</p>
    </div>
  </section>

  <section class="section">
    <div class="container subpage-content">
      {body}

      <div class="subpage-cta">
        <h3>Interessado no imóvel para investimento em Anadia?</h3>
        <p>Vila Anadia: imóvel de 393 m² para coliving e coworking — 8 quartos + T0 + T1 + T3 do proprietário.</p>
        <a href="/pt/" class="btn btn--primary">Ver Vila Anadia · €790.000</a>
      </div>

      {related}
    </div>
  </section>

  <footer class="footer">
    <div class="container footer__inner">
      <div>
        <a href="/pt/" class="nav__brand">
          <span class="nav__brand-mark">A</span>
          <span class="nav__brand-text">Vila&nbsp;Anadia</span>
        </a>
        <p class="footer__tag">Viva em Portugal. Gere rendimento. Um imóvel.</p>
      </div>
      <div class="footer__cols">
        <div>
          <h5>Atrações</h5>
          <a href="/pt/atracoes/">Guia completo</a>
          <a href="/pt/atracoes/vinhos-bairrada/">Vinhos da Bairrada</a>
          <a href="/pt/atracoes/curia-termas/">Termas da Curia</a>
        </div>
        <div>
          <h5>Mais</h5>
          <a href="/pt/atracoes/desporto-car-anadia/">CAR Anadia</a>
          <a href="/pt/atracoes/gastronomia-leitao/">Leitão à Bairrada</a>
          <a href="/pt/atracoes/cidades-praias/">Cidades & praias</a>
        </div>
        <div>
          <h5>Vila Anadia</h5>
          <a href="/pt/">Imóvel à venda</a>
          <a href="https://wa.me/351932855243" target="_blank" rel="noopener">WhatsApp (Daniel)</a>
        </div>
      </div>
    </div>
    <div class="container footer__base">
      <small>© <span id="year"></span> Vila Anadia. Informação indicativa — verifique a documentação completa antes da compra.</small>
    </div>
  </footer>

  <!-- Lang modal stripped — uses parent page's modal via JS -->
  <div class="lang-modal" id="langModal" role="dialog" aria-modal="true" aria-labelledby="langModalTitle">
    <div class="lang-modal__panel" role="document">
      <header class="lang-modal__head">
        <h2 class="lang-modal__title" id="langModalTitle">Escolher idioma</h2>
        <button type="button" class="lang-modal__close" id="langModalClose" aria-label="Fechar">×</button>
      </header>
      <div class="lang-modal__grid" id="langModalGrid">
        <button type="button" class="lang-option" data-lang="en"><span class="lang-option__flag" aria-hidden="true">🇬🇧</span><span class="lang-option__body"><span class="lang-option__native">English</span><span class="lang-option__sub">English</span></span></button>
        <button type="button" class="lang-option is-active" data-lang="pt"><span class="lang-option__flag" aria-hidden="true">🇵🇹</span><span class="lang-option__body"><span class="lang-option__native">Português</span><span class="lang-option__sub">Portuguese</span></span></button>
        <button type="button" class="lang-option" data-lang="de"><span class="lang-option__flag" aria-hidden="true">🇩🇪</span><span class="lang-option__body"><span class="lang-option__native">Deutsch</span><span class="lang-option__sub">German</span></span></button>
        <button type="button" class="lang-option" data-lang="fr"><span class="lang-option__flag" aria-hidden="true">🇫🇷</span><span class="lang-option__body"><span class="lang-option__native">Français</span><span class="lang-option__sub">French</span></span></button>
        <button type="button" class="lang-option" data-lang="es"><span class="lang-option__flag" aria-hidden="true">🇪🇸</span><span class="lang-option__body"><span class="lang-option__native">Español</span><span class="lang-option__sub">Spanish</span></span></button>
        <button type="button" class="lang-option" data-lang="ru"><span class="lang-option__flag" aria-hidden="true">🇷🇺</span><span class="lang-option__body"><span class="lang-option__native">Русский</span><span class="lang-option__sub">Russian</span></span></button>
        <button type="button" class="lang-option" data-lang="uk"><span class="lang-option__flag" aria-hidden="true">🇺🇦</span><span class="lang-option__body"><span class="lang-option__native">Українська</span><span class="lang-option__sub">Ukrainian</span></span></button>
        <button type="button" class="lang-option" data-lang="it"><span class="lang-option__flag" aria-hidden="true">🇮🇹</span><span class="lang-option__body"><span class="lang-option__native">Italiano</span><span class="lang-option__sub">Italian</span></span></button>
        <button type="button" class="lang-option" data-lang="pl"><span class="lang-option__flag" aria-hidden="true">🇵🇱</span><span class="lang-option__body"><span class="lang-option__native">Polski</span><span class="lang-option__sub">Polish</span></span></button>
        <button type="button" class="lang-option" data-lang="el"><span class="lang-option__flag" aria-hidden="true">🇬🇷</span><span class="lang-option__body"><span class="lang-option__native">Ελληνικά</span><span class="lang-option__sub">Greek</span></span></button>
        <button type="button" class="lang-option" data-lang="ja"><span class="lang-option__flag" aria-hidden="true">🇯🇵</span><span class="lang-option__body"><span class="lang-option__native">日本語</span><span class="lang-option__sub">Japanese</span></span></button>
        <button type="button" class="lang-option" data-lang="ar"><span class="lang-option__flag" aria-hidden="true">🇸🇦</span><span class="lang-option__body"><span class="lang-option__native">العربية</span><span class="lang-option__sub">Arabic</span></span></button>
        <button type="button" class="lang-option" data-lang="no"><span class="lang-option__flag" aria-hidden="true">🇳🇴</span><span class="lang-option__body"><span class="lang-option__native">Norsk</span><span class="lang-option__sub">Norwegian</span></span></button>
        <button type="button" class="lang-option" data-lang="sv"><span class="lang-option__flag" aria-hidden="true">🇸🇪</span><span class="lang-option__body"><span class="lang-option__native">Svenska</span><span class="lang-option__sub">Swedish</span></span></button>
        <button type="button" class="lang-option" data-lang="da"><span class="lang-option__flag" aria-hidden="true">🇩🇰</span><span class="lang-option__body"><span class="lang-option__native">Dansk</span><span class="lang-option__sub">Danish</span></span></button>
        <button type="button" class="lang-option" data-lang="nl"><span class="lang-option__flag" aria-hidden="true">🇳🇱</span><span class="lang-option__body"><span class="lang-option__native">Nederlands</span><span class="lang-option__sub">Dutch</span></span></button>
        <button type="button" class="lang-option" data-lang="hu"><span class="lang-option__flag" aria-hidden="true">🇭🇺</span><span class="lang-option__body"><span class="lang-option__native">Magyar</span><span class="lang-option__sub">Hungarian</span></span></button>
        <button type="button" class="lang-option" data-lang="bg"><span class="lang-option__flag" aria-hidden="true">🇧🇬</span><span class="lang-option__body"><span class="lang-option__native">Български</span><span class="lang-option__sub">Bulgarian</span></span></button>
        <button type="button" class="lang-option" data-lang="ro"><span class="lang-option__flag" aria-hidden="true">🇷🇴</span><span class="lang-option__body"><span class="lang-option__native">Română</span><span class="lang-option__sub">Romanian</span></span></button>
      </div>
    </div>
  </div>

  <button class="back-to-top" id="backToTop" aria-label="Topo">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
  </button>

  <script src="/script.js" defer></script>
</body>
</html>
'''

HUB_CARDS_HTML = '''      <div class="attractions__hub">
        <a class="hub-card" href="/pt/atracoes/vinhos-bairrada/">
          <h3>Vinhos da Bairrada</h3>
          <p>Caves Aliança, Caves São João, Quinta do Encontro — as caves históricas em Anadia.</p>
        </a>
        <a class="hub-card" href="/pt/atracoes/curia-termas/">
          <h3>Termas da Curia</h3>
          <p>Spa histórico desde 1898, Curia Palace Hotel Art Nouveau, Parque da Curia.</p>
        </a>
        <a class="hub-card" href="/pt/atracoes/desporto-car-anadia/">
          <h3>CAR Anadia · Ciclismo</h3>
          <p>Centro de Alto Rendimento, velódromo nacional UCI, sede da FPC.</p>
        </a>
        <a class="hub-card" href="/pt/atracoes/gastronomia-leitao/">
          <h3>Leitão à Bairrada</h3>
          <p>A gastronomia icónica da região: onde comer, harmonização, Confraria.</p>
        </a>
        <a class="hub-card" href="/pt/atracoes/cidades-praias/">
          <h3>Cidades & Praias</h3>
          <p>Coimbra, Aveiro, Buçaco, Conímbriga, Costa Nova — tudo a 1 hora.</p>
        </a>
      </div>'''

RELATED_HTML = '''      <aside class="related-pages">
        <h4>Continue a explorar</h4>
        <ul>
          {links}
        </ul>
      </aside>'''

# ─── Generate ────────────────────────────────────────────────────────────
def render_section(kind, content):
    if kind == 'hub':
        return HUB_CARDS_HTML
    if kind == 'text':
        return content
    return ''

def render_related(current_slug):
    items = []
    for key, p in PAGES.items():
        if key == 'index' or p['slug'] == current_slug:
            continue
        items.append(f'  <li><a href="/pt/atracoes/{p["slug"]}/">{p["h1"]}</a></li>')
    return RELATED_HTML.format(links='\n'.join(items)) if items else ''

OUT.mkdir(parents=True, exist_ok=True)

for key, p in PAGES.items():
    slug = p['slug']
    slug_path = f'{slug}/' if slug else ''
    out_dir = OUT / slug if slug else OUT
    out_dir.mkdir(parents=True, exist_ok=True)

    body_parts = [render_section(kind, content) for kind, content in p['sections']]
    body = '\n      '.join(body_parts)

    breadcrumb_extra = ''
    if slug:
        breadcrumb_extra = f'<span>›</span><span class="current">{html_mod.escape(p["h1"])}</span>'

    related = render_related(slug) if slug else ''

    html = HEAD_TMPL.format(
        title=html_mod.escape(p['title'], quote=True),
        description=html_mod.escape(p['description'], quote=True),
        slug_path=slug_path,
        kicker=html_mod.escape(p['kicker']),
        h1=html_mod.escape(p['h1']),
        lead=html_mod.escape(p['lead']),
        body=body,
        related=related,
        breadcrumb_extra=breadcrumb_extra,
        headline_json=json.dumps(p['title'], ensure_ascii=False),
        description_json=json.dumps(p['description'], ensure_ascii=False),
    )

    (out_dir / 'index.html').write_text(html, encoding='utf-8')
    print(f'Wrote {out_dir}/index.html')

print(f'\nGenerated {len(PAGES)} pages under /pt/atracoes/')
