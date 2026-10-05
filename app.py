import os
import json
import textwrap
import streamlit as st

# Attempt to import Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MemoryWeaver — Scrapbook Chronicle",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom Scrapbook Aesthetic Styling ─────────────────────────────────────────
SCRAPBOOK_CSS = textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&family=Patrick+Hand&family=Special+Elite&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

/* Hide standard Streamlit header, footer, and top padding */
#MainMenu, header, footer, .stDeployButton { display: none !important; }
.stAppDeployButton { display: none !important; }
div.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1440px !important;
}

/* Wood Desk Background */
.stApp {
    background-color: #271408 !important;
    background-image: 
        radial-gradient(circle at 50% 40%, rgba(255,255,255,0.04) 0%, rgba(0,0,0,0.65) 100%),
        repeating-linear-gradient(
            0deg,
            #231207 0px,
            #2a160a 4px,
            #301a0c 8px,
            #1e0e05 12px,
            #251308 16px
        ) !important;
    background-attachment: fixed;
    font-family: 'Patrick Hand', 'Caveat', cursive, sans-serif;
    color: #3b2818;
}

/* Pushpin Styles */
.pushpin-gold {
    width: 22px;
    height: 22px;
    background: radial-gradient(circle at 35% 35%, #ffe785, #d6a02b 60%, #7d590d 100%);
    border-radius: 50%;
    box-shadow: 2px 4px 6px rgba(0,0,0,0.65), inset -1px -1px 2px rgba(0,0,0,0.4);
    position: absolute;
    z-index: 20;
}
.pin-tl { top: -9px; left: -9px; }
.pin-tr { top: -9px; right: -9px; }
.pin-bl { bottom: -9px; left: -9px; }
.pin-br { bottom: -9px; right: -9px; }

/* Left Column: Styled as Kraft Board Container */
div[data-testid="column"]:first-child [data-testid="stVerticalBlockBorderWrapper"] {
    position: relative !important;
    background: #d5b387 !important;
    background-image: 
        radial-gradient(#c7a070 15%, transparent 16%),
        radial-gradient(#ba915d 15%, transparent 16%) !important;
    background-size: 20px 20px !important;
    background-position: 0 0, 10px 10px !important;
    border: 1px solid #b58d57 !important;
    border-radius: 6px !important;
    padding: 24px 20px 20px 20px !important;
    box-shadow: 6px 9px 22px rgba(0,0,0,0.6), inset 0 0 35px rgba(90,50,15,0.22) !important;
}

/* Right Column: Styled as Parchment Scrapbook Sheet */
div[data-testid="column"]:last-child [data-testid="stVerticalBlockBorderWrapper"] {
    position: relative !important;
    background: #fbf6ec !important;
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(235, 218, 185, 0.45) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(215, 195, 160, 0.4) 0%, transparent 50%),
        radial-gradient(#ebdec9 10%, transparent 11%) !important;
    background-size: 100% 100%, 100% 100%, 30px 30px !important;
    border: 1px solid #e1d1b7 !important;
    border-radius: 6px !important;
    padding: 35px 35px 40px 35px !important;
    box-shadow: 8px 14px 32px rgba(0,0,0,0.65), inset 0 0 60px rgba(160,120,70,0.18) !important;
}

/* Washi Header & Kraft Subtitle */
.washi-header {
    text-align: center;
    font-family: 'Caveat', cursive;
    font-size: 2.3rem;
    font-weight: 700;
    color: #2a170b;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.kraft-subtitle {
    font-family: 'Patrick Hand', cursive;
    font-size: 1.15rem;
    color: #634327;
    margin-bottom: 14px;
    border-bottom: 2px wavy #a88252;
    padding-bottom: 4px;
}

/* ══════════════════════════════════════════════════════════════════════════════
   EXPLICIT CREAM COLORING FOR ALL INPUTS, SELECTS, AND TEXTAREAS
   ══════════════════════════════════════════════════════════════════════════════ */

/* Labels */
.stTextInput label,
.stSelectbox label,
.stTextArea label {
    font-family: 'Special Elite', monospace !important;
    font-size: 0.88rem !important;
    letter-spacing: 1.5px !important;
    color: #4a321d !important;
    text-transform: uppercase !important;
    margin-bottom: 5px !important;
}

/* Person / Group Name Input: Cream Box with Warm Vintage Border */
.stTextInput div[data-baseweb="base-input"],
.stTextInput div[data-baseweb="input"],
.stTextInput input {
    background-color: #fff9ed !important;
    background: #fff9ed !important;
    color: #2b180d !important;
    border: 1.5px solid #cfb890 !important;
    border-radius: 5px !important;
    font-family: 'Patrick Hand', cursive !important;
    font-size: 1.25rem !important;
    box-shadow: 1px 2px 5px rgba(0,0,0,0.1) !important;
}

/* Chronicle Book Selectbox: Cream Box with Warm Vintage Border */
.stSelectbox div[data-baseweb="select"],
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #fff9ed !important;
    background: #fff9ed !important;
    border: 1.5px solid #cfb890 !important;
    border-radius: 5px !important;
    box-shadow: 1px 2px 5px rgba(0,0,0,0.1) !important;
}
.stSelectbox div[data-baseweb="select"] *,
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] svg {
    color: #2b180d !important;
    fill: #2b180d !important;
    font-family: 'Patrick Hand', cursive !important;
    font-size: 1.15rem !important;
}

/* Note 1 (Written Notes): Cream Lined Paper Textarea */
div[data-testid="column"]:first-child .stTextArea textarea,
div[data-testid="column"]:first-child .stTextArea div[data-baseweb="textarea"] {
    background-color: #fffdf6 !important;
    background: #fffdf6 !important;
    background-image: 
        linear-gradient(90deg, transparent 32px, #ff9e9e 32px, #ff9e9e 34px, transparent 34px),
        repeating-linear-gradient(transparent, transparent 27px, #d2e4f7 27px, #d2e4f7 28px) !important;
    background-size: 100% 100%, 100% 28px !important;
    background-position: 0 0, 0 8px !important;
    border: 1.5px solid #d4c5a9 !important;
    border-radius: 5px !important;
    color: #2b180d !important;
    font-family: 'Patrick Hand', cursive !important;
    font-size: 1.25rem !important;
    line-height: 28px !important;
    padding: 12px 14px 12px 42px !important;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.12) !important;
}

/* Note 2 (Spoken Context): Cream Grid Paper Textarea */
div[data-testid="column"]:last-child .stTextArea textarea,
div[data-testid="column"]:last-child .stTextArea div[data-baseweb="textarea"] {
    background-color: #fbfbf4 !important;
    background: #fbfbf4 !important;
    background-image: 
        linear-gradient(#dde8dd 1px, transparent 1px),
        linear-gradient(90deg, #dde8dd 1px, transparent 1px) !important;
    background-size: 16px 16px !important;
    border: 1.5px solid #d4c5a9 !important;
    border-radius: 5px !important;
    color: #2b180d !important;
    font-family: 'Patrick Hand', cursive !important;
    font-size: 1.25rem !important;
    line-height: 24px !important;
    padding: 12px 14px !important;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.12) !important;
}

/* Focus styles for all inputs */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #8b2b1b !important;
    outline: none !important;
}

/* Placeholders */
::placeholder,
textarea::placeholder,
input::placeholder {
    color: #8f7760 !important;
    opacity: 0.85 !important;
    font-style: italic !important;
}

/* Polaroid Photo Card on Wood Desk */
.polaroid-card {
    background: #fbf7ee;
    padding: 10px 10px 25px 10px;
    border-radius: 3px;
    box-shadow: 4px 6px 14px rgba(0,0,0,0.55);
    transform: rotate(-3.5deg);
    width: 145px;
    margin: 18px auto 0 auto;
    border: 1px solid #dfd8c7;
    text-align: center;
    transition: transform 0.2s ease;
}
.polaroid-card:hover {
    transform: rotate(0deg) scale(1.05);
}
.polaroid-img-box {
    background: #3e3328;
    height: 95px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 2px;
    color: #b5a48f;
    font-size: 2.2rem;
}
.polaroid-caption {
    font-family: 'Caveat', cursive;
    font-size: 1.15rem;
    color: #554433;
    margin-top: 6px;
}

/* Scrapbook Main Titles */
.scrap-entry-meta {
    font-family: 'Special Elite', monospace;
    font-size: 0.85rem;
    color: #7d654c;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.scrap-title {
    font-family: 'Caveat', cursive;
    font-size: 4.2rem;
    font-weight: 700;
    color: #1e130a;
    line-height: 1.05;
    margin: 0;
    padding: 0;
}
.scrap-title-underline {
    width: 230px;
    height: 4px;
    background: #8b2b1b;
    border-radius: 2px;
    margin-top: 4px;
    margin-bottom: 14px;
    opacity: 0.85;
}
.scrap-subtitle {
    font-family: 'Patrick Hand', cursive;
    font-size: 1.3rem;
    color: #5c4531;
    margin-bottom: 24px;
    font-style: italic;
}

/* Embossed Vintage Leather Action Button */
div.stButton > button {
    background: linear-gradient(180deg, #78221b 0%, #52130e 100%) !important;
    color: #faebd7 !important;
    font-family: 'Special Elite', monospace !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
    letter-spacing: 2px !important;
    border: 2px dashed #a44840 !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.5), inset 0 1px 2px rgba(255,255,255,0.2) !important;
    text-transform: uppercase !important;
    transition: all 0.15s ease-in-out !important;
}
div.stButton > button:hover {
    background: linear-gradient(180deg, #8d2a22 0%, #631913 100%) !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.65) !important;
}
div.stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.7) !important;
}

/* Desk Whisper Note */
.desk-whisper {
    font-family: 'Caveat', cursive;
    font-size: 1.2rem;
    color: #cfbba6;
    font-style: italic;
}

/* Result Chapter Sheet */
.result-chapter-card {
    background: #fffdf8;
    border: 1px solid #e3d7bf;
    border-radius: 4px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    padding: 30px 34px;
    margin-top: 30px;
    position: relative;
    background-image: repeating-linear-gradient(transparent, transparent 29px, #f2ead8 29px, #f2ead8 30px);
}
.wax-seal {
    position: absolute;
    top: -16px;
    right: 30px;
    width: 44px;
    height: 44px;
    background: radial-gradient(circle at 35% 35%, #b52a1a, #691309);
    border-radius: 50%;
    box-shadow: 2px 4px 8px rgba(0,0,0,0.4), inset -1px -1px 3px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffd2cc;
    font-size: 1.4rem;
    font-weight: bold;
    border: 2px solid #8e1f13;
}
.tag-badge {
    display: inline-block;
    background: #eadecb;
    border: 1px dashed #997b5e;
    color: #4a3420;
    font-family: 'Special Elite', monospace;
    font-size: 0.85rem;
    padding: 3px 10px;
    border-radius: 3px;
    margin-right: 8px;
    margin-top: 6px;
}
</style>
""")
st.html(SCRAPBOOK_CSS)

# ── Session State Setup ───────────────────────────────────────────────────────
if "chapters" not in st.session_state:
    st.session_state.chapters = []
if "last_chapter" not in st.session_state:
    st.session_state.last_chapter = None
if "entry_counter" not in st.session_state:
    st.session_state.entry_counter = 14

# ── Intelligent Story Chronicler ──────────────────────────────────────────────
def weave_chapter_ai(book_name, person_name, notes, voice_note):
    """Weaves unstructured notes into a rich narrative chapter using Groq or warm fallback."""
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        try:
            groq_api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            groq_api_key = None

    if groq_api_key and GROQ_AVAILABLE:
        try:
            client = Groq(api_key=groq_api_key)
            system_prompt = (
                "You are MemoryWeaver — an empathetic, warm, and poetic family chronicler. "
                "Transform the provided unstructured memory notes and optional spoken thoughts into "
                "a tender, beautifully written chronicle chapter worth passing down through generations. "
                "Always respond strictly with a single valid JSON object containing:\n"
                "  • chapter_title: string (evocative, poetic title)\n"
                "  • formatted_story: string (multi-paragraph prose with warmth and rich sensory details in markdown)\n"
                "  • extracted_tags: list of 3-5 strings (short tags like 'Lagos 1962', 'Family Heirlooms', 'Sewing Machine')"
            )
            user_msg = (
                f"Chronicle Book: {book_name}\n"
                f"Protagonist / Family: {person_name}\n"
                f"Written Notes:\n{notes}\n"
            )
            if voice_note.strip():
                user_msg += f"\nSpoken Voice Context:\n{voice_note}\n"

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                temperature=0.75,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
            )
            parsed = json.loads(response.choices[0].message.content)
            return parsed
        except Exception:
            pass

    # High-quality empathetic chronicler fallback
    first_line = notes.split(".")[0].strip() if "." in notes else notes[:50].strip()
    title_words = [w for w in person_name.split() if len(w) > 2]
    chosen_word = title_words[0] if title_words else "Cherished"
    
    chapter_title = f"The Keepsake of {person_name}: Echoes of {chosen_word}"
    
    formatted_story = (
        f"Some memories arrive not with a shout, but like rain tapping gently upon a windowsill. "
        f"For **{person_name}**, the moments written here carry the indelible weight of heritage and devotion.\n\n"
        f"{notes.strip()}\n\n"
    )
    if voice_note.strip():
        formatted_story += (
            f"In their own spoken words, captured across the table in quiet reflection: "
            f"*\"{voice_note.strip()}\"* — words that anchor the feeling of that fleeting afternoon in time.\n\n"
        )
    formatted_story += (
        f"Years may drift onward and seasons turn, yet this chapter remains preserved inside the **{book_name}**, "
        f"stitched into the living tapestry of who they were and everything they carried forward."
    )
    
    tags = [person_name, book_name.split()[0], "Heritage", "Living Memory"]
    return {
        "chapter_title": chapter_title,
        "formatted_story": formatted_story,
        "extracted_tags": tags
    }


# ── Scrapbook Layout: Left Pinboard & Right Parchment ─────────────────────────
col_pinboard, col_canvas = st.columns([1, 2.6], gap="large")

# ══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN: THE PINBOARD / CARDBOARD NOTE
# ══════════════════════════════════════════════════════════════════════════════
with col_pinboard:
    with st.container(border=True):
        st.html(textwrap.dedent("""
            <div class="pushpin-gold pin-tl"></div>
            <div class="pushpin-gold pin-tr"></div>
            <div class="pushpin-gold pin-bl"></div>
            <div class="pushpin-gold pin-br"></div>
            <div class="washi-header">🧵 MemoryWeaver</div>
            <div class="kraft-subtitle">Settings & Workspace</div>
        """))

        person_val = st.text_input(
            "Person / Group Name",
            value="The Okafor Family",
            key="person_input",
        )

        book_options = ["Family Heritage Vault", "Friends Trip Anthology", "Ancestral Keepsake", "Childhood Summers"]
        chosen_book = st.selectbox(
            "Chronicle Book",
            options=book_options,
            index=0,
            key="book_select",
        )

        st.html(textwrap.dedent("""
            <div style="margin-top: 20px; padding-top: 12px; border-top: 1px dashed #a58157; font-size: 1.05rem; color: #5a3d24;">
                <span>❔</span> <em>need a hand?</em>
                <div style="font-size:0.9rem; color:#78583c; margin-top:4px;">
                    Jot raw fragments or whispers. The chronicler weaves them into heirloom prose.
                </div>
            </div>
        """))

    # Vintage Polaroid photo sitting on the desk below
    st.html(textwrap.dedent("""
        <div class="polaroid-card">
            <div class="polaroid-img-box">
                <span>📷</span>
            </div>
            <div class="polaroid-caption">summer '74</div>
        </div>
    """))


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN: THE PARCHMENT SCRAPBOOK SHEET
# ══════════════════════════════════════════════════════════════════════════════
with col_canvas:
    with st.container(border=True):
        st.html(textwrap.dedent(f"""
            <div class="scrap-entry-meta">
                CHRONICLE · ENTRY NO. {st.session_state.entry_counter} · {chosen_book.upper()}
            </div>
            <h1 class="scrap-title">Memory Chapter</h1>
            <div class="scrap-title-underline"></div>
            <div class="scrap-subtitle">
                Tell me a little, say a little more, and I'll weave it into a chapter worth keeping.
            </div>
        """))

        # Two Scrapbook Note Papers side-by-side
        col_note1, col_note2 = st.columns([1.2, 1], gap="medium")

        default_notes = (
            "Grandma Ava arrived in Lagos in the rainy season of 1962, "
            "carrying one suitcase and her mother's vintage Singer sewing machine. "
            "Every evening after the storm passed, the courtyard smelled of wet earth and lemongrass tea."
        )

        default_spoken = "She told us she never felt alone because the sound of that needle moving was like her mother's heartbeat."

        with col_note1:
            written_text = st.text_area(
                "🍃 Written Notes",
                value=default_notes,
                height=180,
                key="written_notes_input"
            )

        with col_note2:
            spoken_text = st.text_area(
                "🎙️ Spoken Context",
                value=default_spoken,
                placeholder="Paste a voice transcript, or jot what was whispered aloud...",
                height=180,
                key="spoken_context_input"
            )

        # Action Button: Embossed Leather Book Stamp
        st.html("<div style='height: 25px;'></div>")
        col_btn_l, col_btn_c, col_btn_r = st.columns([0.15, 0.7, 0.15])
        with col_btn_c:
            weave_pressed = st.button("📖 SAVE CHRONICLE ENTRY", use_container_width=True)

        st.html(textwrap.dedent("""
            <div style="text-align: right; margin-top: 10px;">
                <span class="desk-whisper">Nothing leaves this desk until you say so.</span>
            </div>
        """))

    # ── Action Execution ──────────────────────────────────────────────────────
    if weave_pressed:
        if not written_text.strip():
            st.warning("✍️ Please jot down at least a memory fragment on the lined page.")
        else:
            with st.spinner("🪡 Stitching memories into the family ledger..."):
                chapter_data = weave_chapter_ai(
                    book_name=chosen_book,
                    person_name=person_val.strip() or "Our Family",
                    notes=written_text,
                    voice_note=spoken_text
                )
                st.session_state.last_chapter = chapter_data
                st.session_state.entry_counter += 1
                st.session_state.chapters.append(chapter_data)

    # ── Display the Woven Chronicle Chapter ───────────────────────────────────
    if st.session_state.last_chapter:
        res = st.session_state.last_chapter
        
        tags_html = ""
        tags = res.get("extracted_tags", [])
        if tags:
            tags_html = "".join([f'<span class="tag-badge">🏷️ {t}</span>' for t in tags])

        st.html(textwrap.dedent(f"""
            <div class="result-chapter-card">
                <div class="wax-seal">⚜️</div>
                <div style="font-family:'Special Elite', monospace; font-size:0.85rem; color:#8c694a; letter-spacing:1.5px; text-transform:uppercase;">
                    WOVEN MEMORY CHAPTER · {chosen_book.upper()}
                </div>
                <h2 style="font-family:'Caveat', cursive; font-size:2.8rem; color:#211409; margin: 4px 0 12px 0;">
                    {res.get('chapter_title', 'A Moment Preserved')}
                </h2>
                <div style="font-family:'Crimson Pro', Georgia, serif; font-size:1.25rem; line-height:1.75; color:#2c1e13; white-space: pre-wrap;">
{res.get('formatted_story', '')}
                </div>
                <div style="margin-top: 18px; border-top: 1px dashed #d6c6aa; padding-top: 10px;">
                    {tags_html}
                </div>
            </div>
        """))
