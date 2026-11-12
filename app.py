"""
Aplicación educativa en Streamlit
---------------------------------
- Fondo: #F0E7C7
- Menú lateral a la DERECHA con: Derechos, Videos, Forum
- Masonry de 2 columnas con 7 cartas (#AD6447), cada una con video y título abajo
- Header que se oculta al hacer scroll hacia abajo y reaparece al subir

Ejecutar:  streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Aprende y Participa",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

BG_COLOR = "#F0E7C7"
CARD_COLOR = "#AD6447"
TEXT_DARK = "#3B2A20"
TEXT_LIGHT = "#FFF8E7"

# ---------------------------------------------------------------------------
# Datos (reemplaza las URLs por tus propios videos .mp4)
# "ratio" varía la altura de cada video para lograr el efecto masonry.
# ---------------------------------------------------------------------------
VIDEOS = [
    {
        "title": "Introducción a los derechos humanos",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "ratio": "16 / 9",
    },
    {
        "title": "Derecho a la educación",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "ratio": "4 / 5",
    },
    {
        "title": "Igualdad y no discriminación",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "ratio": "1 / 1",
    },
    {
        "title": "Libertad de expresión",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "ratio": "16 / 9",
    },
    {
        "title": "Derecho a la salud",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "ratio": "3 / 4",
    },
    {
        "title": "Participación ciudadana",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        "ratio": "16 / 10",
    },
    {
        "title": "Cómo defender tus derechos",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
        "ratio": "1 / 1",
    },
]

DERECHOS = [
    ("Derecho a la educación", "Toda persona tiene derecho a recibir una educación gratuita y de calidad."),
    ("Derecho a la igualdad", "Todas las personas son iguales ante la ley y merecen el mismo trato."),
    ("Libertad de expresión", "Puedes expresar tus ideas y opiniones libremente y con respeto."),
    ("Derecho a la salud", "Tienes derecho a acceder a servicios de salud y a una vida saludable."),
    ("Derecho a la participación", "Puedes participar en las decisiones que afectan tu comunidad."),
    ("Derecho a la protección", "Toda persona debe ser protegida contra el abuso, la violencia y la explotación."),
]

# ---------------------------------------------------------------------------
# Estilos (CSS)
# ---------------------------------------------------------------------------
CSS = f"""
<style>
/* ---------- Fondo ---------- */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {{
    background-color: {BG_COLOR} !important;
}}

/* ---------- Ocultar header nativo de Streamlit ---------- */
[data-testid="stHeader"] {{
    display: none !important;
}}
#MainMenu, footer {{
    visibility: hidden;
}}

/* ---------- Sidebar a la DERECHA ---------- */
[data-testid="stAppViewContainer"] {{
    flex-direction: row-reverse !important;
}}
[data-testid="stSidebar"] {{
    background-color: {CARD_COLOR} !important;
    border-left: 3px solid {TEXT_DARK}22;
    border-right: none !important;
    padding-top: 72px;
}}
/* Se quita el botón de colapsar para mantener el menú siempre visible */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}
[data-testid="stSidebar"] * {{
    color: {TEXT_LIGHT} !important;
}}
[data-testid="stSidebar"] h2 {{
    font-weight: 800;
    letter-spacing: .5px;
}}
/* Radio como botones de menú */
[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 8px;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label {{
    background: #ffffff1a;
    border-radius: 12px;
    padding: 10px 14px;
    width: 100%;
    transition: background .2s ease, transform .2s ease;
    cursor: pointer;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
    background: #ffffff33;
    transform: translateX(-4px);
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {{
    background: {BG_COLOR};
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) * {{
    color: {TEXT_DARK} !important;
    font-weight: 700;
}}
/* Oculta el circulito del radio */
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {{
    display: none;
}}

/* ---------- Header con hide-on-scroll ---------- */
#app-header {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    background: {TEXT_DARK};
    color: {TEXT_LIGHT};
    box-shadow: 0 2px 10px #00000044;
    transition: transform .3s ease;
    font-family: "Segoe UI", system-ui, sans-serif;
}}
#app-header.header-hidden {{
    transform: translateY(-100%);
}}
#app-header .brand {{
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: .5px;
}}
#app-header .tagline {{
    font-size: .85rem;
    opacity: .8;
}}

/* Espacio para que el contenido no quede debajo del header */
[data-testid="stMainBlockContainer"],
.block-container {{
    padding-top: 90px !important;
    max-width: 1100px;
}}

/* ---------- Títulos ---------- */
h1, h2, h3 {{
    color: {TEXT_DARK} !important;
}}
.page-title {{
    font-size: 2rem;
    font-weight: 800;
    color: {TEXT_DARK};
    margin-bottom: 4px;
}}
.page-sub {{
    color: {TEXT_DARK};
    opacity: .75;
    margin-bottom: 24px;
}}

/* ---------- Masonry de 2 columnas ---------- */
.masonry {{
    column-count: 2;
    column-gap: 20px;
}}
.card {{
    background: {CARD_COLOR};
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 20px;
    break-inside: avoid;
    display: inline-block;
    width: 100%;
    box-shadow: 0 6px 16px #3b2a2033;
    transition: transform .2s ease, box-shadow .2s ease;
}}
.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 22px #3b2a2055;
}}
.card video {{
    display: block;
    width: 100%;
    object-fit: cover;
    background: #000;
}}
.card .card-title {{
    padding: 14px 16px;
    color: {TEXT_LIGHT};
    font-weight: 700;
    font-size: 1.05rem;
    font-family: "Segoe UI", system-ui, sans-serif;
}}
@media (max-width: 700px) {{
    .masonry {{ column-count: 1; }}
}}

/* ---------- Derechos / Forum ---------- */
.rights-card {{
    background: {CARD_COLOR};
    color: {TEXT_LIGHT};
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px #3b2a2033;
}}
.rights-card h4 {{
    margin: 0 0 6px 0;
    color: {TEXT_LIGHT} !important;
}}
.rights-card p {{
    margin: 0;
}}
.post {{
    background: {CARD_COLOR};
    color: {TEXT_LIGHT};
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px #3b2a2033;
}}
.post .author {{
    font-weight: 800;
    margin-bottom: 4px;
}}
.stButton > button, .stFormSubmitButton > button {{
    background: {CARD_COLOR};
    color: {TEXT_LIGHT};
    border: none;
    border-radius: 10px;
    font-weight: 700;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    background: {TEXT_DARK};
    color: {TEXT_LIGHT};
}}
</style>
"""

HEADER_HTML = """
<div id="app-header">
    <span class="brand">📚 Aprende y Participa</span>
    <span class="tagline">Conoce tus derechos · Mira · Comparte</span>
</div>
"""

# JS que oculta el header al bajar y lo muestra al subir.
# Se ejecuta dentro de un iframe same-origin y accede al documento padre.
HIDE_ON_SCROLL_JS = """
<script>
(function () {
    const parentWin = window.parent;
    const doc = parentWin.document;

    function setup() {
        const header = doc.getElementById("app-header");
        if (!header) { return false; }
        if (parentWin.__hideOnScrollReady) { return true; }
        parentWin.__hideOnScrollReady = true;

        const targets = [
            doc.querySelector('[data-testid="stMain"]'),
            doc.querySelector('section.main'),
            doc.querySelector('[data-testid="stAppViewContainer"]'),
        ].filter(Boolean);

        let lastY = 0;
        const THRESHOLD = 8;

        function onScroll(e) {
            const el = e.target === doc ? doc.documentElement : e.target;
            const y = el.scrollTop || 0;
            if (Math.abs(y - lastY) < THRESHOLD) { return; }
            if (y > lastY && y > 60) {
                header.classList.add("header-hidden");     // bajando
            } else {
                header.classList.remove("header-hidden");  // subiendo
            }
            lastY = y;
        }

        targets.forEach(t => t.addEventListener("scroll", onScroll, { passive: true }));
        parentWin.addEventListener("scroll", onScroll, { passive: true });
        return true;
    }

    // Reintenta hasta que el header exista en el DOM
    let tries = 0;
    const timer = setInterval(function () {
        tries += 1;
        if (setup() || tries > 40) { clearInterval(timer); }
    }, 250);
})();
</script>
"""


# ---------------------------------------------------------------------------
# Vistas
# ---------------------------------------------------------------------------
def view_derechos() -> None:
    st.markdown('<div class="page-title">⚖️ Derechos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Conoce los derechos fundamentales que te protegen.</div>',
        unsafe_allow_html=True,
    )
    for titulo, texto in DERECHOS:
        st.markdown(
            f'<div class="rights-card"><h4>{titulo}</h4><p>{texto}</p></div>',
            unsafe_allow_html=True,
        )


def view_videos() -> None:
    st.markdown('<div class="page-title">🎬 Videos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Aprende con nuestra colección de videos educativos.</div>',
        unsafe_allow_html=True,
    )

    cards = ""
    for v in VIDEOS:
        cards += f"""
        <div class="card">
            <video controls preload="metadata" style="aspect-ratio: {v['ratio']};">
                <source src="{v['url']}" type="video/mp4">
                Tu navegador no soporta la reproducción de video.
            </video>
            <div class="card-title">{v['title']}</div>
        </div>
        """
    st.markdown(f'<div class="masonry">{cards}</div>', unsafe_allow_html=True)


def view_forum() -> None:
    st.markdown('<div class="page-title">💬 Forum</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Comparte tus preguntas y opiniones con la comunidad.</div>',
        unsafe_allow_html=True,
    )

    if "posts" not in st.session_state:
        st.session_state.posts = [
            {"autor": "Ana", "mensaje": "¿Dónde puedo aprender más sobre mis derechos como estudiante?"},
            {"autor": "Luis", "mensaje": "El video sobre igualdad me pareció muy claro. ¡Gracias!"},
        ]

    with st.form("nuevo_post", clear_on_submit=True):
        autor = st.text_input("Tu nombre")
        mensaje = st.text_area("Mensaje")
        enviar = st.form_submit_button("Publicar")

    if enviar:
        if autor.strip() and mensaje.strip():
            st.session_state.posts.insert(
                0, {"autor": autor.strip(), "mensaje": mensaje.strip()}
            )
            st.rerun()
        else:
            st.warning("Escribe tu nombre y un mensaje antes de publicar.")

    for p in st.session_state.posts:
        autor_html = (
            p["autor"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        mensaje_html = (
            p["mensaje"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        st.markdown(
            f'<div class="post"><div class="author">{autor_html}</div>{mensaje_html}</div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HEADER_HTML, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## Menú")
        pagina = st.radio(
            "Navegación",
            ["Derechos", "Videos", "Forum"],
            index=1,
            label_visibility="collapsed",
        )

    if pagina == "Derechos":
        view_derechos()
    elif pagina == "Videos":
        view_videos()
    else:
        view_forum()

    # Script de hide-on-scroll (iframe de altura 0)
    components.html(HIDE_ON_SCROLL_JS, height=0)


if __name__ == "__main__":
    main()
