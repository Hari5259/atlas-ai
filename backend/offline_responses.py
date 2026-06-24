"""Rich offline responses when knowledge search has no strong match."""

import re
from response_formatter import format_topics_list


def try_offline_response(prompt: str) -> str | None:
    t = prompt.lower().strip()
    if not t:
        return None

    handlers = [
        _topics_list,
        _physics,
        _chemistry,
        _biology,
        _programming,
        _cs_ml,
        _study,
        _history,
        _economics,
        _geography,
        _astronomy,
        _health,
        _philosophy,
        _environment,
    ]
    for handler in handlers:
        result = handler(t)
        if result:
            return result
    return None


def _topics_list(t: str) -> str | None:
    if re.search(r"\b(topics?|subjects?|what can you|capabilities|help with|know about)\b", t):
        topics = [
            "mathematics", "physics", "chemistry", "biology",
            "computer science", "programming", "networking", "cybersecurity",
            "history", "geography", "economics", "psychology", "astronomy",
            "environment", "health", "civics", "engineering", "philosophy",
            "literature", "arts", "study skills", "quick facts",
        ]
        return format_topics_list(topics)
    return None


def _physics(t: str) -> str | None:
    if not re.search(r"\b(physics|newton|force|velocity|momentum|energy|quantum)\b", t):
        return None
    if re.search(r"\b(newton|force|f=ma|acceleration)\b", t):
        return (
            "### *points to the blackboard* Newton's Laws\n\n"
            "**1st (Inertia):** An object stays at rest or uniform motion unless a net force acts.\n\n"
            "**2nd:** **F = m × a** — net force equals mass times acceleration.\n\n"
            "**3rd:** Every action has an equal and opposite reaction.\n\n"
            "**Kinetic energy:** KE = ½mv²\n\n"
            "*smiles and nods* Tell me which law or problem you'd like to work through. 📚"
        )
    return (
        "### *nods helpfully* Physics overview\n\n"
        "I can explain mechanics (forces, energy), electricity (Ohm's law), waves, and modern physics basics.\n\n"
        "*points to study board* Try: *Explain F=ma with an example* or *What is kinetic energy?* 🚀"
    )


def _chemistry(t: str) -> str | None:
    if not re.search(r"\b(chemistry|atom|molecule|reaction|bond|acid|ph|mole)\b", t):
        return None
    return (
        "### *gestures to molecular model* Chemistry essentials 🧪\n\n"
        "- **Atoms:** protons, neutrons, electrons; atomic number = protons\n"
        "- **Bonding:** ionic (transfer), covalent (sharing), metallic\n"
        "- **pH:** 0–14 scale; 7 = neutral\n"
        "- **Moles:** n = mass / molar mass; Avogadro = 6.022×10²³\n\n"
        "*smiles warmly* Ask about a specific reaction or concept for a deeper explanation."
    )


def _biology(t: str) -> str | None:
    if not re.search(r"\b(biology|cell|dna|gene|evolution|photosynthesis|respiration|organism)\b", t):
        return None
    if re.search(r"\b(photosynthesis|respiration|atp)\b", t):
        return (
            "### *taps diagram of cell metabolism* Energy in cells 🌿\n\n"
            "**Photosynthesis** (plants): 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\n"
            "**Cellular respiration:** C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + **ATP**\n\n"
            "*points to diagram* Photosynthesis stores energy; respiration releases it for cell work."
        )
    return (
        "### *nods friendly* Biology overview 🧬\n\n"
        "- **Cell theory** — all life is cellular\n"
        "- **DNA → RNA → protein** (central dogma)\n"
        "- **Evolution** by natural selection\n\n"
        "*smiles encouragingly* Want a quiz on any of these?"
    )


def _programming(t: str) -> str | None:
    if not re.search(r"\b(python|javascript|code|programming|function|variable|loop|debug)\b", t):
        return None
    return (
        "### *taps the computer screen* Programming tips 💻\n\n"
        "1. **Read errors carefully** — line number and message point to the fix\n"
        "2. **Break problems down** — solve one small piece at a time\n"
        "3. **Test edge cases** — empty input, zero, large values\n"
        "4. **Use meaningful names** — `student_count` not `x`\n\n"
        "*nods supportively* Share your language and problem for specific help."
    )


def _cs_ml(t: str) -> str | None:
    if not re.search(r"\b(algorithm|machine learning|neural|git|api|database|sql|big o)\b", t):
        return None
    if re.search(r"\b(big o|complexity|sort|search)\b", t):
        return (
            "### *points to complexity chart* Algorithm complexity (Big O) 📊\n\n"
            "| Notation | Meaning | Example |\n"
            "|----------|---------|--------|\n"
            "| O(1) | Constant | Hash lookup |\n"
            "| O(log n) | Logarithmic | Binary search |\n"
            "| O(n) | Linear | Single loop |\n"
            "| O(n log n) | Linearithmic | Merge sort |\n"
            "| O(n²) | Quadratic | Nested loops |\n"
        )
    return (
        "### *nods sagely* Computer science 🧠\n\n"
        "Algorithms, APIs, databases, Git, and ML fundamentals are in my knowledge base.\n\n"
        "*waves hand to suggest* Ask something specific like *Explain binary search* or *What is REST?*"
    )


def _study(t: str) -> str | None:
    if not re.search(r"\b(study|exam|revision|pomodoro|flashcard|focus|learn how)\b", t):
        return None
    return (
        "### *points to a timer* Study smarter ⏱️\n\n"
        "- **Pomodoro:** 25 min focus, 5 min break\n"
        "- **Active recall:** test yourself, don't only re-read\n"
        "- **Spaced repetition:** review at 1d, 3d, 1w intervals\n"
        "- **Feynman:** explain the topic in simple words\n\n"
        "*smiles warmly* I can also quiz you on science or math topics — just ask!"
    )


def _history(t: str) -> str | None:
    if not re.search(r"\b(history|war|revolution|civilization|ancient|empire)\b", t):
        return None
    return (
        "### *gestures to historical timeline* History snapshot 📜\n\n"
        "- **Ancient:** Mesopotamia, Egypt, Greece, Rome, China\n"
        "- **Industrial Revolution (1760s+):** mechanization, urbanization\n"
        "- **20th century:** World Wars, Cold War, digital age\n\n"
        "*nods politely* Ask about a specific era or event for more detail."
    )


def _economics(t: str) -> str | None:
    if not re.search(r"\b(economics|gdp|inflation|supply|demand|market)\b", t):
        return None
    return (
        "### *points to supply/demand curves* Economics basics 📈\n\n"
        "- **Supply & demand** set equilibrium price\n"
        "- **GDP** = C + I + G + (X − M)\n"
        "- **Inflation:** rising price level; central banks use interest rates\n\n"
        "*smiles* Ask about a specific concept for examples."
    )


def _geography(t: str) -> str | None:
    if not re.search(r"\b(geography|continent|country|capital|river|mountain|climate)\b", t):
        return None
    return (
        "### *spins a globe* Geography highlights 🌍\n\n"
        "- **7 continents** — Asia largest by population\n"
        "- **Nile & Amazon** — among longest rivers\n"
        "- **Everest** — highest peak (8,849 m)\n"
        "- **Climate zones** — tropical, temperate, polar\n\n"
        "*nods friendly* Ask about a specific country or feature."
    )


def _astronomy(t: str) -> str | None:
    if not re.search(r"\b(space|planet|star|moon|sun|galaxy|universe|astronomy)\b", t):
        return None
    return (
        "### *points up to the stars* Astronomy snapshot 🌌\n\n"
        "- **8 planets** orbit the Sun\n"
        "- **Light speed** ≈ 3×10⁸ m/s\n"
        "- **Moon phases** — ~29.5 day cycle\n"
        "- **Big Bang** — universe ~13.8 billion years old\n\n"
        "*smiles excitedly* Ask about a specific planet or phenomenon."
    )


def _health(t: str) -> str | None:
    if not re.search(r"\b(health|nutrition|diet|sleep|exercise|immune|vitamin)\b", t):
        return None
    return (
        "### *nods healthily* Health & wellness 🍎\n\n"
        "- **Balanced diet** — carbs, protein, fats\n"
        "- **Sleep** — 7–9 hours for adults; aids memory\n"
        "- **Exercise** — 150 min/week moderate activity\n"
        "- **Hydration** — essential for focus and energy\n\n"
        "*smiles gently* This is educational info, not medical advice."
    )


def _philosophy(t: str) -> str | None:
    if not re.search(r"\b(philosophy|ethics|logic|socrates|plato|descartes|fallacy)\b", t):
        return None
    return (
        "### *strokes chin thoughtfully* Philosophy introduction 🤔\n\n"
        "- **Ethics** — right and wrong (utilitarianism, deontology)\n"
        "- **Logic** — valid reasoning, avoid fallacies\n"
        "- **Epistemology** — what we can know\n"
        "- **Socratic method** — learning through questions\n\n"
        "*nods slowly* Which branch interests you?"
    )


def _environment(t: str) -> str | None:
    if not re.search(r"\b(climate|environment|pollution|renewable|carbon|ecosystem|greenhouse)\b", t):
        return None
    return (
        "### *points to a recycling logo* Environment & climate 🌍\n\n"
        "- **Greenhouse effect** — CO₂ traps heat\n"
        "- **Renewables** — solar, wind, hydro\n"
        "- **Biodiversity** — variety of life on Earth\n"
        "- **Carbon footprint** — emissions from daily activities\n\n"
        "*smiles friendly* Ask about a specific environmental topic."
    )
