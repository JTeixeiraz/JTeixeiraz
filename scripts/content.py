"""Todo o texto dos SVGs do perfil, em linguagem simples.

Cada afirmação tem origem no vault do Obsidian (Vagas/02 - Base de
Evidências e as notas de cada projeto) ou no content.ts do portfólio.

Regras, de propósito:
- Perfil é permanente e ninguém atualiza: nada de contagem que envelhece
  (instalações, demandas, commits, testes).
- Nada de taxa de falha de sistema do empregador.
- Nenhuma frase de "procurando emprego": o perfil é visível para a XP.
- Uma ideia por frase. Quem lê é recrutador com noventa segundos.
"""

import json
import os

from svgkit import AMBER, MINT, PINK, SKY, TILE, VIOLET

with open(os.path.join(os.path.dirname(__file__), "icons.json")) as _f:
    ICONS = {i["label"]: i for i in json.load(_f)["icons"]}

PORTFOLIO = "https://joao-teixeira-eng.netlify.app"
VYRO = "https://vyro-studio-97878960.netlify.app"

HERO = {
    "handle": "README · @JTEIXEIRAZ",
    "name": ("João Pedro", "Teixeira"),
    "line": "I build software people depend on every day — and the AI agents "
            "that help run it.",
    # (rótulo, destaque, detalhe, cor)
    "tiles": [
        ("WORKING AT", "XP Educação", "Full Stack Developer", AMBER),
        ("LIVE ON THE STORES", "Birdy", "Google Play + App Store", MINT),
        ("BASED IN", "Belo Horizonte", "Brazil · UTC−3", TILE),
        ("FOCUS", "AI agents", "with a human in the loop", PINK),
    ],
    "stack_label": "MAIN STACK",
    "stack": ["TypeScript", "Python", "Flutter", "Rust", "React", "Next.js",
              "Node.js", "FastAPI", "PostgreSQL", "Supabase", "Docker", "Azure"],
}

# O que ele faz na XP Educação, sem jargão. (título, frase, cor)
DOING = [
    ("Automate manual work",
     "Processes that depend on someone remembering become code that runs on "
     "its own — certificates, contracts, enrollment.", VIOLET),
    ("Ship whole features",
     "Screen, API, database and deploy. The whole thing, not just my slice "
     "of it.", AMBER),
    ("Connect systems",
     "Payments, digital signatures and learning platforms talking to each "
     "other — without counting the same event twice.", MINT),
    ("Watch what runs",
     "Monitoring that flags business errors, not only server errors — before "
     "they turn into support tickets.", SKY),
    ("Keep it secure",
     "Certificates that can’t be forged, and credentials kept out of the "
     "code.", PINK),
    ("Use AI with care",
     "AI suggests, plain code executes, and a person approves. Never the "
     "other way around.", VIOLET),
]

BIRDY = {
    "slug": "birdy",
    "status": "LIVE · GOOGLE PLAY + APP STORE",
    "name": "Birdy",
    "what": "An app for bird breeders to manage their aviary — birds, pairs, "
            "genetics and pedigree.",
    "points": [
        "Built, shipped and run by me, from design to store billing.",
        "A desktop version that works offline and syncs on its own.",
        "Security-tested against my own production backend.",
    ],
    "glance": [
        ("PLATFORMS", "Android · iOS"),
        ("BACKEND", "Firebase + Supabase"),
        ("GROWTH", "Organic — no paid ads"),
        ("ROLE", "Founder, solo"),
    ],
    "stack": ["Flutter", "Dart", "Firebase", "Supabase", "PostgreSQL"],
    "link": "SEE BIRDY",
    "href": f"{VYRO}/birdy",
}

CARDS = [
    {
        "slug": "lumi", "color": VIOLET, "status": "IN TESTING",
        "name": "LUMI",
        "what": "A self-care app with an AI companion that builds your "
                "routine from a short conversation.",
        "points": [
            "AI runs on the server — new models, no app update.",
            "Fixed-format answers as a defense against prompt injection.",
        ],
        "stack": ["Flutter", "Supabase", "Deno"],
        "link": "SEE LUMI", "href": f"{VYRO}/lumi",
    },
    {
        "slug": "postly", "color": AMBER, "status": "OPEN SOURCE",
        "name": "Postly",
        "what": "A marketing team that runs on your own computer, powered by "
                "local AI models.",
        "points": [
            "Loads one AI model at a time, so it fits on an ordinary laptop.",
            "Free and MIT-licensed, for Linux, macOS and Windows.",
        ],
        "stack": ["Rust", "Tauri", "React", "Ollama"],
        "link": "VIEW CODE", "href": "https://github.com/JTeixeiraz/Postly",
    },
    {
        "slug": "induxai", "color": SKY, "status": "FREELANCE",
        "name": "InduxAI",
        "what": "An API that predicts a key quality measure in a cement kiln, "
                "used inside the client’s own software.",
        "points": [
            "Turned a data-science script into a production API.",
            "Shrank the server image from 1.72 GB to 734 MB.",
        ],
        "stack": ["Python", "FastAPI", "Docker"],
        "link": "READ MORE", "href": f"{PORTFOLIO}/#fora",
    },
    {
        "slug": "dcars", "color": PINK, "status": "FREELANCE",
        "name": "D’Cars Box",
        "what": "Management software for a mechanic’s workshop: quotes, work "
                "orders, parts stock and payments.",
        "points": [
            "Works fully offline — the internet is optional.",
            "Shows which supplier sold a faulty part.",
        ],
        "stack": ["Flutter", "SQLite", "GitHub Actions"],
        "link": "READ MORE", "href": f"{PORTFOLIO}/#fora",
    },
]

AI = {
    "steps": [
        ("STEP 1", "AI suggests", "Reads the request, sorts it by urgency and "
         "suggests who should handle it.", VIOLET),
        ("STEP 2", "Code executes", "Plain, predictable code does the "
         "routing. No AI in that path.", SKY),
        ("STEP 3", "A person approves", "Nothing is sent until the product "
         "manager clicks approve.", AMBER),
    ],
    "label": "IN PRODUCTION AT XP EDUCAÇÃO",
    "example": "SustentaBot — a Slack assistant that turns support requests "
               "into ready-to-work tasks.",
    "note": "When it can’t read something, like an image, it says so instead "
            "of guessing.",
}

# (rótulo, cor, itens com ícone, texto extra)
STACK = [
    ("LANGUAGES", VIOLET, ["TypeScript", "Python", "Dart", "Rust", "Java",
                           "C#"], ""),
    ("FRONT END & MOBILE", AMBER, ["React", "Next.js", "Tailwind", "Flutter",
                                   "Tauri"], ""),
    ("BACK END", MINT, ["Node.js", "Express", "FastAPI", "Django", "Flask",
                        "Deno"], ""),
    ("DATA", SKY, ["PostgreSQL", "MongoDB", "SQLite", "Firebase", "Supabase"],
     ""),
    ("CLOUD & DEVOPS", PINK, ["Azure", "Azure DevOps", "Google Cloud",
                              "Cloudflare", "Docker", "GitHub Actions"], ""),
    ("AI", VIOLET, ["Claude", "Gemini", "NVIDIA NIM", "Ollama"],
     "MCP · RAG · tool calling · agents"),
]
PRACTICES = ("PRACTICES", "TDD · code review · event-driven design · retries "
             "and idempotency · observability · feature flags · Scrum")

# (slug, rótulo, valor, cor)
CONTACT = [
    ("email", "EMAIL", "joaopedroteixeirareis@gmail.com", VIOLET),
    ("linkedin", "LINKEDIN", "in/joaoteixeirareis", SKY),
    ("portfolio", "PORTFOLIO · PT / EN", "joao-teixeira-eng.netlify.app", AMBER),
]
