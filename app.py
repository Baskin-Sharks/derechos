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

BG_COLOR = "#BFAE62"
CARD_COLOR = "#AD6447"
TEXT_DARK = "#3B2A20"
TEXT_LIGHT = "#FFF8E7"

NUM_CARDS = 7
# Alturas del espacio vacío de cada carta (px) -> efecto masonry
PLACEHOLDER_HEIGHTS = [220, 300, 260, 340, 240, 300, 220]

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
CSS = """
<style>
/* ---------- Fondo ---------- */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {
    background-color: __BG__ !important;
}

/* ---------- Ocultar header nativo de Streamlit ---------- */
[data-testid="stHeader"] { display: none !important; }
#MainMenu, footer { visibility: hidden; }

/* ---------- Header propio con hide-on-scroll ---------- */
#app-header {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 60px;
    z-index: 1000000;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px 0 28px;
    background: __DARK__;
    color: __LIGHT__;
    box-shadow: 0 2px 10px #00000044;
    transition: transform .3s ease;
    font-family: "Segoe UI", system-ui, sans-serif;
}
#app-header.header-hidden { transform: translateY(-100%); }
#app-header .brand { font-size: 1.2rem; font-weight: 800; letter-spacing: .5px; }

/* ---------- Botón hamburger (derecha) ---------- */
#hamburger {
    width: 44px; height: 44px;
    background: transparent;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 0;
}
#hamburger:hover { background: #ffffff22; }
#hamburger span {
    display: block;
    width: 24px; height: 3px;
    background: __LIGHT__;
    border-radius: 2px;
    transition: transform .25s ease, opacity .25s ease;
}
body.menu-open #hamburger span:nth-child(1) { transform: translateY(9px) rotate(45deg); }
body.menu-open #hamburger span:nth-child(2) { opacity: 0; }
body.menu-open #hamburger span:nth-child(3) { transform: translateY(-9px) rotate(-45deg); }

/* ---------- Side menu (drawer a la derecha) ---------- */
[data-testid="stSidebar"],
[data-testid="stSidebar"][aria-expanded="true"],
[data-testid="stSidebar"][aria-expanded="false"] {
    position: fixed !important;
    top: 0 !important;
    right: 0 !important;
    left: auto !important;
    height: 100vh !important;
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
    margin: 0 !important;
    z-index: 999999 !important;
    background-color: __CARD__ !important;
    border: none !important;
    box-shadow: -6px 0 18px #00000040;
    padding-top: 76px;
    transform: translateX(105%) !important;
    visibility: hidden;
    transition: transform .3s ease, visibility 0s linear .3s;
}
body.menu-open [data-testid="stSidebar"] {
    transform: translateX(0) !important;
    visibility: visible;
    transition: transform .3s ease, visibility 0s;
}
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

[data-testid="stSidebar"] * { color: __LIGHT__ !important; }
[data-testid="stSidebar"] h2 { font-weight: 800; letter-spacing: .5px; }

[data-testid="stSidebar"] div[role="radiogroup"] { gap: 8px; }
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background: #ffffff1a;
    border-radius: 12px;
    padding: 10px 14px;
    width: 100%;
    transition: background .2s ease, transform .2s ease;
    cursor: pointer;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: #ffffff33;
    transform: translateX(-4px);
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: __BG__;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) * {
    color: __DARK__ !important;
    font-weight: 700;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }

/* ---------- Contenido ---------- */
[data-testid="stMainBlockContainer"],
.block-container {
    padding-top: 90px !important;
    max-width: 1100px;
}
.page-title { font-size: 2rem; font-weight: 800; color: __DARK__; margin-bottom: 4px; }
.page-sub { color: __DARK__; opacity: .75; margin-bottom: 24px; }

/* ---------- Cartas del masonry ---------- */
[class*="st-key-card-"] {
    background: __CARD__;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 8px;
    box-shadow: 0 6px 16px #3b2a2033;
}
.placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    background: #ffffff1f;
    border: 2px dashed #fff8e7aa;
    border-radius: 12px;
    color: __LIGHT__;
    font-size: 2rem;
    margin-top: 6px;
}
.placeholder span { font-size: .95rem; opacity: .9; }

/* Uploader dentro de la carta */
[class*="st-key-card-"] [data-testid="stFileUploaderDropzone"] {
    background: #ffffff22;
    border: 2px dashed #fff8e7aa;
    border-radius: 12px;
}
[class*="st-key-card-"] [data-testid="stFileUploaderDropzone"] *,
[class*="st-key-card-"] [data-testid="stFileUploader"] small,
[class*="st-key-card-"] [data-testid="stFileUploaderFile"] * {
    color: __LIGHT__ !important;
}
[class*="st-key-card-"] [data-testid="stFileUploaderDropzone"] button {
    background: __DARK__;
    border: none;
    border-radius: 8px;
}
[class*="st-key-card-"] video {
    border-radius: 12px;
    width: 100%;
    margin-top: 6px;
}
/* Título en la parte inferior */
[class*="st-key-card-"] input {
    background: __LIGHT__ !important;
    color: __DARK__ !important;
    border-radius: 10px;
    font-weight: 700;
}

/* ---------- Derechos / Forum ---------- */
.rights-card, .post {
    background: __CARD__;
    color: __LIGHT__;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px #3b2a2033;
}
.rights-card h4 { margin: 0 0 6px 0; color: __LIGHT__ !important; }
.rights-card p { margin: 0; }
.post .author { font-weight: 800; margin-bottom: 4px; }

.stButton > button, .stFormSubmitButton > button {
    background: __CARD__;
    color: __LIGHT__;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: __DARK__;
    color: __LIGHT__;
}
</style>
"""

CSS = (
    CSS.replace("__BG__", BG_COLOR)
    .replace("__CARD__", CARD_COLOR)
    .replace("__DARK__", TEXT_DARK)
    .replace("__LIGHT__", TEXT_LIGHT)
)

HEADER_HTML = """
<div id="app-header">
    <span class="brand">📚 Aprende y Participa</span>
    <button id="hamburger" aria-label="Abrir menú" type="button">
        <span></span><span></span><span></span>
    </button>
</div>
"""

# JS: hamburger (abrir/cerrar menú) + hide-on-scroll del header.
# Corre en un iframe same-origin y trabaja sobre el documento padre.
BEHAVIOR_JS = """
<script>
(function () {
    const parentWin = window.parent;
    const doc = parentWin.document;

    /* ---------- Hamburger menu ---------- */
    if (!parentWin.__menuReady) {
        parentWin.__menuReady = true;

        doc.addEventListener("click", function (e) {
            const t = e.target;
            const isBurger = t.closest && t.closest("#hamburger");
            const inSidebar = t.closest && t.closest('[data-testid="stSidebar"]');

            if (isBurger) {
                doc.body.classList.toggle("menu-open");
            } else if (inSidebar) {
                // al elegir una opción del menú, se cierra
                if (t.closest("label")) {
                    setTimeout(function () { doc.body.classList.remove("menu-open"); }, 250);
                }
            } else {
                doc.body.classList.remove("menu-open");   // clic fuera del menú
            }
        });
    }

    /* ---------- Hide-on-scroll ---------- */
    function setupScroll() {
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
            const h = doc.getElementById("app-header");
            if (!h) { return; }
            if (y > lastY && y > 60) {
                h.classList.add("header-hidden");      // bajando
            } else {
                h.classList.remove("header-hidden");   // subiendo
            }
            lastY = y;
        }

        targets.forEach(function (t) { t.addEventListener("scroll", onScroll, { passive: true }); });
        parentWin.addEventListener("scroll", onScroll, { passive: true });
        return true;
    }

    let tries = 0;
    const timer = setInterval(function () {
        tries += 1;
        if (setupScroll() || tries > 40) { clearInterval(timer); }
    }, 250);
})();
</script>
"""


# ---------------------------------------------------------------------------
# Vistas
# ---------------------------------------------------------------------------
def render_card(index: int) -> None:
    """Carta vacía: subir video + título en la parte inferior."""
    with st.container(key=f"card-{index}"):
        video = st.file_uploader(
            f"Video {index + 1}",
            type=["mp4", "mov", "webm", "m4v"],
            key=f"video_{index}",
            label_visibility="collapsed",
        )
        if video is not None:
            st.video(video)
        else:
            height = PLACEHOLDER_HEIGHTS[index % len(PLACEHOLDER_HEIGHTS)]
            st.markdown(
                f'<div class="placeholder" style="height:{height}px;">🎬'
                f"<span>Carta vacía · sube un video</span></div>",
                unsafe_allow_html=True,
            )
        st.text_input(
            f"Título {index + 1}",
            key=f"title_{index}",
            placeholder="Escribe un título…",
            label_visibility="collapsed",
        )


def view_videos() -> None:
    st.markdown('<div class="page-title">🎬 Videos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-sub">Sube un video y ponle título a cada carta.</div>',
        unsafe_allow_html=True,
    )

    # Masonry de 2 columnas: cartas 1,3,5,7 a la izquierda y 2,4,6 a la derecha.
    # Al variar la altura de cada carta, las columnas quedan escalonadas.
    col_left, col_right = st.columns(2, gap="medium")
    for i in range(NUM_CARDS):
        with (col_left if i % 2 == 0 else col_right):
            render_card(i)


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


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


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
        st.markdown(
            f'<div class="post"><div class="author">{_esc(p["autor"])}</div>'
            f'{_esc(p["mensaje"])}</div>',
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

    # Comportamiento: hamburger + hide-on-scroll (iframe de altura 0)
    components.html(BEHAVIOR_JS, height=0)


if __name__ == "__main__":
    main()
