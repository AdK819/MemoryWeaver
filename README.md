# 📖 MemoryWeaver — AI-Powered Scrapbook Chronicle

> Turn unstructured family notes and spoken memories into beautifully woven story chapters.

MemoryWeaver is an AI-powered multi-book chronicle that bridges generational memories into timeless heirloom chapters. Built with Streamlit, open-weight LLMs (`llama-3.3-70b-versatile` via Groq), and DevRelay agent session tracking.

![MemoryWeaver Scrapbook](https://placehold.co/800x450/271408/faebd7?text=MemoryWeaver+-+Scrapbook+Chronicle)

---

## ✨ Features

- **Multi-Book Workspaces**: Keep sensitive family history separate from casual trip memories (e.g. *Family Heritage Vault*, *Friends Trip Anthology*).
- **Scrapbook Desk Aesthetic**: Designed to feel like a wooden desk with a kraft paper pinboard, lined notebook paper, and grid paper notes.
- **Open-Weights AI**: Powered by `llama-3.3-70b-versatile` for empathetic, poetic chapter weaving.
- **End-User First**: Zero technical clutter or API key inputs exposed to end users.
- **DevRelay Integration**: Full agent session logging with embedded Liquid tags for DEV publishing.

---

## 🚀 Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AdK819/MemoryW.git
   cd MemoryW
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Groq API Key (Optional background key):**
   ```bash
   export GROQ_API_KEY="your-groq-api-key"
   # On Windows PowerShell:
   # $env:GROQ_API_KEY="your-groq-api-key"
   ```

4. **Launch the application:**
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **LLM Engine**: [Groq](https://groq.com/) with Llama-3.3-70B
- **Agent Logging & Publishing**: [DevRelay](https://devrelay.com/)
- **Styling**: Vintage Scrapbook CSS with Google Fonts (`Caveat`, `Patrick Hand`, `Special Elite`, `Crimson Pro`)

---

## 📜 License

MIT License — see the [LICENSE](LICENSE) file for details.
