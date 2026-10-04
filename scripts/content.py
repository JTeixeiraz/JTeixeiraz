"""Todo o texto dos SVGs do perfil.

Cada afirmação aqui tem origem no vault do Obsidian (Vagas/02 - Base de
Evidências e as notas de cada projeto) ou no content.ts do portfólio.

Regras herdadas, de propósito:
- Perfil é permanente e ninguém atualiza: nada de contagem que envelhece
  (instalações, demandas, commits, testes). Mecanismo no lugar de número.
- Nada de taxa de falha de sistema do empregador.
- Nenhuma frase de "procurando emprego": o perfil é visível para a XP.
"""

from svgkit import width, wrap

EASE_IO = "cubic-bezier(.65,0,.35,1)"

PORTFOLIO = "https://joao-teixeira-eng.netlify.app"
VYRO = "https://vyro-studio-97878960.netlify.app"

HERO = {
    "role": "FULL STACK DEVELOPER · FORWARD DEPLOYED ENGINEER",
    "place": "BELO HORIZONTE, BR · UTC−3",
    "kicker": "XP EDUCAÇÃO · SOFTWARE ENGINEERING SQUAD",
    "name": "JOÃO PEDRO TEIXEIRA",
    "lines": ("SYSTEMS THAT", "CANNOT ", "GO DOWN"),
    "foot": "PYTHON · TYPESCRIPT · FLUTTER · RUST · AZURE · GOOGLE CLOUD",
    "foot_r": "FOUNDER · BIRDY",
    "alt": "João Pedro Teixeira — Systems that cannot go down",
    "desc": "Full Stack Developer and Forward Deployed Engineer in XP "
            "Educação's Software Engineering squad, Belo Horizonte, Brazil.",
}

# slug: (índice, título, nota à direita)
HEADS = {
    "craft": ("002", "THE CRAFT", "AT XP EDUCAÇÃO · 01 — 06"),
    "projects": ("003", "PROJECTS", "OWN PRODUCTS + FREELANCE · 01 — 05"),
    "boundary": ("004", "WHERE AUTOMATION STOPS", "THE BOUNDARY"),
    "tools": ("005", "TOOLS", "08 GROUPS"),
    "contact": ("006", "LET’S TALK", "PT · EN"),
}

CONTACT = {
    "lead": "If you have a system that needs to hold up under real users, "
            "write to me. I answer in Portuguese or English.",
    "line": "JOAOPEDROTEIXEIRAREIS@GMAIL.COM · BELO HORIZONTE, BR · UTC−3",
}

CRAFT = [
    ("I automate what depended on someone remembering",
     "Azure Functions in Python, on HTTP and timer triggers, that own the "
     "whole routine: generate, sign, send, verify.",
     "CASE — CERTIFICATE PIPELINE"),
    ("I deliver the whole feature, not my slice of it",
     "Screen, API, query, migration and deploy. When the rule is wrong in the "
     "database, a pretty interface fixes nothing.",
     "CASE — STUDENT ID CARD"),
    ("I make systems talk that were never built to",
     "Data contracts between platforms nobody designed together, with "
     "webhooks, retries and idempotency so an event never counts twice.",
     "CASE — CONTRACTS, LMS, PAYMENTS"),
    ("I instrument what nobody is watching",
     "A scheduled job fails silently while the dashboard stays green. I make "
     "a business error show up as an error, not a 200.",
     "CASE — AUTOMATION OBSERVABILITY"),
    ("I treat documents and credentials as attack surface",
     "If a certificate can be forged by knowing the format, it is worth "
     "nothing. The secret lives on the server, never in the shape of the code.",
     "CASE — AUTHENTICITY HASH + VALIDATOR"),
    ("I put AI agents into production on a leash",
     "A model classifies well and decides badly. It adds judgment; dispatch "
     "stays in deterministic code, behind human approval.",
     "CASE — SUSTENTABOT"),
]

BIRDY = {
    "slug": "birdy",
    "label": "OWN PRODUCT · GOOGLE PLAY & APP STORE",
    "name": "BIRDY",
    "summary": "Aviary management SaaS for exotic bird breeders. I built it, "
               "shipped it and run it — growing organically, with no paid "
               "acquisition.",
    "bullets": [
        "Hybrid backend: Firebase issues the JWT, Supabase validates it, and "
        "Row Level Security isolates every user’s data.",
        "A genetics engine shared by mobile and desktop: crossing simulator, "
        "pedigree and inbreeding coefficient.",
        "Local-first desktop client on its own sync engine: outbox queue, "
        "poison-pill tolerance, ancestry ordering for foreign keys.",
    ],
    "spec_title": "SPEC SHEET",
    "spec": [
        ("STATUS", "LIVE · ANDROID + IOS"),
        ("AUTH", "FIREBASE JWT · SUPABASE RLS"),
        ("BILLING", "SERVER-VALIDATED"),
        ("SYNC", "LOCAL-FIRST · OWN ENGINE"),
        ("AUDIT", "SELF-PENTESTED · 4 JWT FORGERY VECTORS BLOCKED"),
        ("GROWTH", "ORGANIC · NO PAID ADS"),
    ],
    "chips": ["FLUTTER", "RIVERPOD", "DRIFT", "FIREBASE", "SUPABASE",
              "POSTGRESQL", "PLAY BILLING"],
    "link": "SEE BIRDY",
    "href": f"{VYRO}/birdy",
}

CARDS = [
    {
        "slug": "lumi",
        "label": "OWN PRODUCT · CLOSED TESTING",
        "name": "LUMI",
        "summary": "A self-care app with an AI companion that runs a "
                   "consultation by conversation and builds the routine from "
                   "what it learns.",
        "bullets": [
            "The model chain lives in an Edge Function: the device knows no "
            "model name, and keys never leave the server.",
            "A fallback rule set by measurement — a 429 rotates the key, any "
            "other failure rotates the model.",
            "Structured JSON output as the injection defense: a reply that "
            "can only fill a closed schema cannot carry an instruction.",
        ],
        "chips": ["FLUTTER", "SUPABASE", "DENO", "POSTGRESQL", "CLOUDFLARE R2"],
        "link": "SEE LUMI",
        "href": f"{VYRO}/lumi",
    },
    {
        "slug": "postly",
        "label": "OPEN SOURCE · MIT",
        "name": "POSTLY",
        "summary": "A desktop app that runs a marketing department on your "
                   "machine: AI roles take turns on local models to research, "
                   "decide, produce, audit and publish.",
        "bullets": [
            "A middleware, not an LLM wrapper. Never two models resident: "
            "measure free memory, load the strongest that fits, answer, unload.",
            "Model tier follows the role — whoever decides must reason; whoever "
            "executes a finished brief need not.",
            "Shared context as a weighted graph, no database. Releases for "
            "Linux, macOS and Windows.",
        ],
        "chips": ["RUST", "TAURI V2", "REACT", "TYPESCRIPT", "OLLAMA"],
        "link": "VIEW REPOSITORY",
        "href": "https://github.com/JTeixeiraz/Postly",
    },
    {
        "slug": "induxai",
        "label": "FREELANCE · INDUSTRIAL ML API",
        "name": "INDUXAI",
        "summary": "Turned a cement-kiln prediction script into a "
                   "multi-tenant production API, consumed by the client’s own "
                   "SaaS.",
        "bullets": [
            "Numerical parity verified against the original pipeline: same "
            "input, same number.",
            "Docker image cut from 1.72 GB to 734 MB by removing CUDA the "
            "production model never touched.",
            "Scope stated in writing: deployment contracted, model training "
            "out of scope.",
        ],
        "chips": ["PYTHON", "FASTAPI", "XGBOOST", "DOCKER", "PYTEST"],
        "link": "READ MORE",
        "href": f"{PORTFOLIO}/#fora",
    },
    {
        "slug": "dcars",
        "label": "FREELANCE · WORKSHOP ERP",
        "name": "D’CARS BOX",
        "summary": "A bespoke desktop ERP for a mechanic’s workshop: quote, "
                   "work order, FIFO stock and payment in one loop.",
        "bullets": [
            "Answers what off-the-shelf tools don’t: which supplier sold the "
            "bad part.",
            "Runs fully offline on SQLite. The network is optional — updates, "
            "inspection photos, backups.",
            "Windows builds on every tag through GitHub Actions, with in-app "
            "auto-update.",
        ],
        "chips": ["FLUTTER DESKTOP", "RIVERPOD", "DRIFT", "SQLITE",
                  "GITHUB ACTIONS"],
        "link": "READ MORE",
        "href": f"{PORTFOLIO}/#fora",
    },
]

BOUNDARY = {
    "lead": "I run AI agents in production every day. The part that takes "
            "judgment is not getting a model to write code — it is deciding "
            "what it is not allowed to execute.",
    # (índice, papel, nome, descrição, é o portão humano?)
    "nodes": [
        ("01", "IN SLACK", "A request", "Someone asks for help in plain "
         "words, in a thread.", False),
        ("02", "THE MODEL SUGGESTS", "SustentaBot", "Interviews one question "
         "at a time, classifies urgency and impact, proposes a developer.",
         False),
        ("03", "CODE EXECUTES", "Routing", "Ordinary deterministic Python. No "
         "model sits in the dispatch path.", False),
        ("04", "A HUMAN DECIDES", "PM approval", "Nothing is sent until the "
         "product manager clicks.", True),
        ("05", "DISPATCH", "Developer DM", "Sent once — a double click or a "
         "Slack retry cannot send it twice.", False),
    ],
    "notes": [
        ("LIMITS STAY EXPLICIT",
         "A text-only model cannot see an attachment. The bot records the "
         "file, says it did not read it, and asks for a description instead "
         "of hallucinating."),
        ("GENERATED CODE IS A DRAFT",
         "On the InduxAI API, the final branch review caught an unhandled "
         "KeyError and incomplete NumPy serialization before merge."),
    ],
}

TOOLS = [
    ("FRONT", ["React", "Next.js", "TypeScript", "Tailwind", "TanStack Query",
               "Flutter", "Tauri"]),
    ("BACK", ["Python", "FastAPI", "Node.js", "Express", "Rust", "Django",
              "Flask", "C#", "Java"]),
    ("DATA", ["PostgreSQL", "MongoDB", "Cosmos DB", "Firestore", "SQLite",
              "CTEs", "RLS"]),
    ("CLOUD", ["Azure", "Google Cloud", "Firebase", "Supabase", "Pub/Sub",
               "Cloudflare R2"]),
    ("INFRA", ["Azure Functions", "Container Apps", "Azure DevOps", "Docker",
               "GitHub Actions", "Edge Functions", "RabbitMQ"]),
    ("ARCHITECTURE", ["event-driven", "idempotency", "retry with backoff",
                      "feature flags", "observability", "multi-tenant",
                      "local-first sync"]),
    ("AI", ["Claude API", "Gemini API", "NVIDIA NIM", "tool calling",
            "structured output", "RAG", "MCP", "subagents", "skills"]),
    ("CRAFT", ["TDD", "pytest", "code review", "Application Insights",
               "SOLID", "design patterns", "Scrum"]),
]

# (slug, rótulo, sólido?)
BUTTONS = [
    ("email", "SEND AN EMAIL", True),
    ("linkedin", "LINKEDIN", False),
    ("portfolio", "PORTFOLIO", False),
]


def wrap_title(t, size, maxw):
    return wrap(t, "title", size, maxw)


def wrap_sans(t, size, maxw):
    return wrap(t, "sans", size, maxw)


def wrap_mono(t, size, maxw):
    return wrap(t, "mono", size, maxw)


def alt_craft():
    return " ".join(f"{i:02d}. {t}. {b}" for i, (t, b, _) in enumerate(CRAFT, 1))


def alt_project(p):
    return f"{p['summary']} " + " ".join(p["bullets"])


def alt_boundary():
    steps = " → ".join(f"{n[2]} ({n[1].lower()})" for n in BOUNDARY["nodes"])
    return f"{BOUNDARY['lead']} {steps}."


def alt_tools():
    return "; ".join(f"{g}: {', '.join(i)}" for g, i in TOOLS)


__all__ = ["width"]
