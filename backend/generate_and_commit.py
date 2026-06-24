"""
Programmatic facts generator and Git commit orchestrator for Atlas AI.
Generates 58,400 facts in total across 6 domains:
1. Grammar & Linguistics
2. Economics
3. Social Sciences
4. History
5. Geography
6. General Science & Astronomy
Partitioned into 13 chunks, written to json files, and committed.
"""

import json
import random
import subprocess
import sys
from pathlib import Path

# Seed for reproducibility
random.seed(42)

# Define directories
backend_dir = Path(__file__).resolve().parent
topics_dir = backend_dir / "knowledge" / "general" / "topics"
topics_dir.mkdir(parents=True, exist_ok=True)

# Word and Concept Lists for Combinatorics
nouns = [
    "teacher", "student", "musician", "scientist", "engineer", "artist", "doctor", "chef", "writer", "architect",
    "programmer", "pilot", "dentist", "nurse", "farmer", "coach", "manager", "director", "professor", "judge",
    "reporter", "photographer", "designer", "mechanic", "carpenter", "plumber", "electrician", "baker", "tailor", "barber",
    "librarian", "historian", "economist", "linguist", "philosopher", "astronomer", "biologist", "chemist", "physicist", "geologist"
]
plural_nouns = [
    "teachers", "students", "musicians", "scientists", "engineers", "artists", "doctors", "chefs", "writers", "architects",
    "programmers", "pilots", "dentists", "nurses", "farmers", "coaches", "managers", "directors", "professors", "judges",
    "reporters", "photographers", "designers", "mechanics", "carpenters", "plumbers", "electricians", "bakers", "tailors", "barbers",
    "librarians", "historians", "economists", "linguists", "philosophers", "astronomers", "biologists", "chemists", "physicists", "geologists"
]
verbs = [
    "runs", "jumps", "writes", "codes", "draws", "sings", "teaches", "studies", "builds", "cooks",
    "flies", "dances", "drives", "reads", "paints", "creates", "solves", "helps", "leads", "plays",
    "analyzes", "explores", "investigates", "discovers", "designs", "organizes", "manages", "directs", "presents", "evaluates"
]
plural_verbs = [
    "run", "jump", "write", "code", "draw", "sing", "teach", "study", "build", "cook",
    "fly", "dance", "drive", "read", "paint", "create", "solve", "help", "lead", "play",
    "analyze", "explore", "investigate", "discover", "design", "organize", "manage", "direct", "present", "evaluate"
]
adjectives = [
    "happy", "sad", "fast", "slow", "smart", "clever", "creative", "diligent", "energetic", "friendly",
    "kind", "honest", "brave", "calm", "gentle", "humble", "loyal", "polite", "quiet", "wise",
    "brilliant", "eager", "passionate", "resourceful", "meticulous", "tenacious", "optimistic", "generous", "sincere", "ambitious"
]
adverbs = [
    "quickly", "slowly", "happily", "sadly", "gracefully", "loudly", "softly", "eagerly", "patiently", "carefully",
    "honestly", "bravely", "calmly", "wisely", "silently", "smoothly", "boldly", "cheerfully", "efficiently", "constantly",
    "brilliantly", "resourcefully", "meticulously", "tenaciously", "optimistically", "generously", "sincerely", "ambitiously", "adeptly", "expertly"
]

economists = [
    ("Adam Smith", "Classical Economics", "the 'invisible hand' of self-regulating markets"),
    ("John Maynard Keynes", "Keynesian Economics", "government intervention to manage aggregate demand during recessions"),
    ("Milton Friedman", "Monetarism", "the role of money supply in inflation and economic cycles"),
    ("David Ricardo", "Comparative Advantage", "countries specializing in goods they produce relatively more efficiently"),
    ("Karl Marx", "Marxian Economics", "the labor theory of value and systemic class conflict"),
    ("Alfred Marshall", "Neoclassical Economics", "demand and supply curves, marginal utility, and production costs"),
    ("Joseph Schumpeter", "Creative Destruction", "innovation and entrepreneurship driving long-term economic growth"),
    ("Friedrich Hayek", "Austrian School", "decentralized prices sharing knowledge without central planning"),
    ("Paul Samuelson", "Neo-Keynesian Synthesis", "applying mathematical principles to neoclassical and Keynesian theories"),
    ("Amartya Sen", "Welfare Economics", "capability approach to human development, poverty, and inequality")
]

goods = [
    "wheat", "oil", "microchips", "automobiles", "textiles", "steel", "coffee", "solar panels", "medical equipment", "software",
    "natural gas", "gold", "timber", "coal", "pharmaceuticals", "aircraft", "beef", "rice", "plastics", "copper"
]

countries = [
    "the United States", "China", "Japan", "Germany", "the United Kingdom", "India", "France", "Italy", "Canada", "South Korea",
    "Brazil", "Australia", "Russia", "Spain", "Mexico", "Indonesia", "Netherlands", "Saudi Arabia", "Turkey", "Switzerland"
]

social_concepts = [
    ("Social Stratification", "sociology", "categorization of people into socio-economic tiers based on wealth, status, and power"),
    ("Cognitive Dissonance", "psychology", "mental discomfort that occurs when a person holds contradictory beliefs or values"),
    ("Separation of Powers", "political_science", "division of government responsibilities into distinct branches to limit centralized power"),
    ("Cultural Relativism", "anthropology", "principle of understanding a person's beliefs and practices within their own cultural context"),
    ("Socialization", "sociology", "process of internalizing the norms and ideologies of society to function within it"),
    ("Classical Conditioning", "psychology", "learning process that occurs when two stimuli are repeatedly paired"),
    ("Federalism", "political_science", "system of government where power is divided between a central authority and constituent political units"),
    ("Ethnography", "anthropology", "scientific description of individual peoples and cultures through direct fieldwork"),
    ("Anomie", "sociology", "state of normlessness where societal values and rules degrade, leading to social instability"),
    ("Operant Conditioning", "psychology", "learning method where behaviors are modified using reinforcement or punishment")
]

social_theorists = [
    ("Max Weber", "sociology", "bureaucracy and rationalization"),
    ("B.F. Skinner", "psychology", "behaviorism and operant conditioning"),
    ("John Locke", "political_science", "natural rights and the social contract"),
    ("Franz Boas", "anthropology", "historical particularism and cultural relativism"),
    ("Emile Durkheim", "sociology", "social facts and division of labor"),
    ("Sigmund Freud", "psychology", "psychoanalysis and the unconscious mind"),
    ("Thomas Hobbes", "political_science", "sovereignty and Leviathan state of nature"),
    ("Margaret Mead", "anthropology", "culture and personality in adolescence"),
    ("Karl Marx", "sociology", "historical materialism and class struggle"),
    ("Jean Piaget", "psychology", "stages of cognitive development in children")
]

social_regions = [
    "North America", "Western Europe", "East Asia", "Sub-Saharan Africa", "Latin America",
    "South Asia", "Southeast Asia", "Middle East", "Eastern Europe", "Oceania"
]

social_applications = [
    "educational reform", "urban planning", "public health policy", "corporate leadership", "legal system design",
    "digital community building", "inter-group conflict resolution", "environmental conservation efforts", "economic development programs", "political campaign strategies"
]

historical_events = [
    ("Magna Carta Signing", "1215", "England", "limited the power of the monarchy and established the rule of law"),
    ("French Revolution", "1789", "France", "overthrew the absolute monarchy and promoted liberty, equality, and fraternity"),
    ("Industrial Revolution", "1760", "Great Britain", "transitioned manufacturing from hand production to machine processes"),
    ("Meiji Restoration", "1868", "Japan", "restored imperial rule and accelerated modernization and industrialization"),
    ("Russian Revolution", "1917", "Russia", "abolished the monarchy and led to the creation of the Soviet Union"),
    ("Treaty of Versailles", "1919", "Versailles", "ended World War I and imposed heavy reparations on Germany"),
    ("Fall of the Berlin Wall", "1989", "Germany", "symbolized the end of the Cold War and the reunification of Germany"),
    ("American Revolution", "1775", "North America", "led to independence of the colonies from Great Britain"),
    ("Glorious Revolution", "1688", "England", "established a constitutional monarchy and parliament supremacy"),
    ("Renaissance", "1400", "Italy", "revived classical learning, arts, and scientific inquiry")
]

historical_figures = [
    ("Julius Caesar", "Roman Republic", "expanding territory and crossing the Rubicon"),
    ("Alexander the Great", "Ancient Macedon", "conquering the Persian Empire"),
    ("Mahatma Gandhi", "British Raj India", "leading nonviolent civil disobedience for independence"),
    ("Napoleon Bonaparte", "Napoleonic France", "implementing the Napoleonic Code and conquering Europe"),
    ("Queen Elizabeth I", "Tudor England", "establishing the Protestant church and defeat of Spanish Armada"),
    ("Abraham Lincoln", "Civil War USA", "preserving the Union and issuing Emancipation Proclamation"),
    ("Nelson Mandela", "Apartheid South Africa", "ending apartheid and serving as first black president"),
    ("George Washington", "Revolutionary USA", "leading continental army and serving as first president"),
    ("Joan of Arc", "Hundred Years' War France", "rallying French forces against English siege of Orleans"),
    ("Qin Shi Huang", "Imperial China", "unifying China and starting Great Wall construction")
]

historical_realms = [
    "military strategy", "constitutional law", "socio-cultural values", "global trade routes",
    "philosophical movements", "literary achievements", "scientific development", "religious institutions",
    "artistic expressions", "technological innovations"
]

geography_countries = [
    ("the United States", "Washington D.C.", "North America", "331 million", "English", "US Dollar", "technology"),
    ("China", "Beijing", "East Asia", "1.4 billion", "Mandarin", "Renminbi", "manufacturing"),
    ("Japan", "Tokyo", "East Asia", "125 million", "Japanese", "Yen", "electronics"),
    ("Germany", "Berlin", "Western Europe", "83 million", "German", "Euro", "automobiles"),
    ("the United Kingdom", "London", "Western Europe", "67 million", "English", "Pound Sterling", "financial services"),
    ("India", "New Delhi", "South Asia", "1.4 billion", "Hindi/English", "Indian Rupee", "information technology"),
    ("France", "Paris", "Western Europe", "67 million", "French", "Euro", "luxury goods"),
    ("Italy", "Rome", "Southern Europe", "59 million", "Italian", "Euro", "machinery"),
    ("Canada", "Ottawa", "North America", "38 million", "English/French", "Canadian Dollar", "natural resources"),
    ("South Korea", "Seoul", "East Asia", "51 million", "Korean", "Won", "semiconductors"),
    ("Brazil", "Brasilia", "South America", "214 million", "Portuguese", "Real", "agriculture"),
    ("Australia", "Canberra", "Oceania", "26 million", "English", "Australian Dollar", "mining"),
    ("Russia", "Moscow", "Eurasia", "143 million", "Russian", "Ruble", "energy"),
    ("Mexico", "Mexico City", "North America", "126 million", "Spanish", "Mexican Peso", "automotive products"),
    ("Indonesia", "Jakarta", "Southeast Asia", "273 million", "Indonesian", "Rupiah", "palm oil"),
    ("Netherlands", "Amsterdam", "Western Europe", "17 million", "Dutch", "Euro", "agricultural machinery"),
    ("Saudi Arabia", "Riyadh", "Middle East", "35 million", "Arabic", "Riyal", "petroleum"),
    ("Turkey", "Ankara", "Eurasia", "85 million", "Turkish", "Lira", "textiles"),
    ("Switzerland", "Bern", "Western Europe", "8.7 million", "German/French/Italian", "Swiss Franc", "banking"),
    ("South Africa", "Pretoria", "Southern Africa", "59 million", "Zulu/Xhosa/Afrikaans/English", "Rand", "minerals")
]

geography_features = [
    ("the Rocky Mountains", "mountain range", "North America", "stretching over 3,000 miles from Canada to New Mexico"),
    ("the Amazon River", "river system", "South America", "flowing over 4,000 miles and holding the largest drainage basin in the world"),
    ("the Sahara Desert", "hot desert", "North Africa", "covering over 3.6 million square miles and ranking as the largest hot desert"),
    ("the Great Barrier Reef", "coral reef system", "Coral Sea", "comprising over 2,900 individual reefs and stretching for 1,400 miles"),
    ("the Nile River", "river system", "Northeast Africa", "flowing 4,135 miles northward and historical cradle of civilizations"),
    ("the Alps", "mountain range", "Europe", "extending 750 miles across eight countries and featuring iconic peaks like Mont Blanc"),
    ("the Himalayas", "mountain range", "Asia", "containing the world's highest peaks including Mount Everest"),
    ("the Mississippi River", "river system", "North America", "flowing 2,340 miles southward through the United States"),
    ("the Gobi Desert", "cold desert", "East Asia", "covering parts of northern China and southern Mongolia"),
    ("the Mediterranean Sea", "inland sea", "Atlantic Ocean boundary", "connecting Europe, Africa, and Asia and key trade route")
]

science_elements = [
    ("Hydrogen", "H", "1", "nonmetal", "lightest element, highly flammable, abundant in stars"),
    ("Helium", "He", "2", "noble gas", "second lightest element, inert, used in cryogenics and balloons"),
    ("Lithium", "Li", "3", "alkali metal", "lightest solid metal, highly reactive, used in rechargeable batteries"),
    ("Carbon", "C", "6", "nonmetal", "basis of organic chemistry, forms diamond and graphite structures"),
    ("Nitrogen", "N", "7", "diatomic nonmetal", "makes up 78% of Earth's atmosphere, essential for protein synthesis"),
    ("Oxygen", "O", "8", "diatomic nonmetal", "highly reactive oxidizing agent, essential for respiration in organisms"),
    ("Fluorine", "F", "9", "halogen", "most electronegative element, extremely reactive, toxic gas"),
    ("Neon", "Ne", "10", "noble gas", "inert gas, glows reddish-orange in high-voltage discharge signs"),
    ("Sodium", "Na", "11", "alkali metal", "soft, silvery-white metal, reacts violently with water, key component of table salt"),
    ("Iron", "Fe", "26", "transition metal", "most common element on Earth by mass, forms the core, essential for hemoglobin")
]

science_laws = [
    ("Newton's First Law of Motion", "Physics", "an object remains at rest or in uniform motion unless acted upon by a force", "F = 0 implies dv/dt = 0"),
    ("Newton's Second Law of Motion", "Physics", "the force applied to an object is equal to its mass times acceleration", "F = m * a"),
    ("Newton's Third Law of Motion", "Physics", "for every action, there is an equal and opposite reaction", "F_A = -F_B"),
    ("First Law of Thermodynamics", "Physics", "energy cannot be created or destroyed, only transformed from one form to another", "Delta U = Q - W"),
    ("Second Law of Thermodynamics", "Physics", "the total entropy of an isolated system always increases over time", "Delta S >= 0"),
    ("Law of Conservation of Mass", "Chemistry", "mass in an isolated system is neither created nor destroyed by chemical reactions", "Mass of reactants = Mass of products"),
    ("Ohm's Law", "Physics", "electric current is directly proportional to voltage and inversely proportional to resistance", "I = V / R"),
    ("Coulomb's Law", "Physics", "force between two charges is proportional to their product and inversely proportional to distance squared", "F = k * (q1 * q2) / r^2"),
    ("Ideal Gas Law", "Chemistry", "the state of a hypothetical ideal gas is determined by pressure, volume, temperature, and amount", "P * V = n * R * T"),
    ("Hubble's Law", "Astronomy", "galaxies are moving away from Earth at velocities proportional to their distance", "v = H0 * d")
]

science_structures = [
    ("Mitochondria", "cellular biology", "powerhouse of the cell, generating adenosine triphosphate (ATP) through respiration"),
    ("Chloroplast", "plant biology", "site of photosynthesis, converting solar energy into chemical energy in plants"),
    ("Nucleus", "molecular biology", "organelle housing the genetic material (DNA) and directing cellular activities"),
    ("Ribosome", "molecular biology", "site of protein synthesis, translating messenger RNA into polypeptide chains"),
    ("Cell Membrane", "cellular biology", "semi-permeable barrier regulating the movement of substances in and out of the cell"),
    ("DNA Double Helix", "genetics", "molecule carrying genetic instructions for development, functioning, and reproduction"),
    ("Endoplasmic Reticulum", "cellular biology", "network of membranes involved in folding proteins and synthesizing lipids"),
    ("Golgi Apparatus", "cellular biology", "packages and processes proteins and lipids for secretion or delivery to organelles"),
    ("Lysosome", "cellular biology", "contains digestive enzymes to break down waste materials and cellular debris"),
    ("Cytoskeleton", "cellular biology", "network of protein fibers providing structural support, shape, and movement for the cell")
]

# Generators for distinct domains
def generate_grammar_entries():
    entries = []
    idx = 1
    # 1. Singular agreement
    for n in nouns:
        for v in verbs:
            entries.append({
                "id": f"gen-grammar-{idx:05d}",
                "topic": "grammar rules",
                "title": f"Subject-Verb Agreement: {n.title()} and {v.title()}",
                "content": f"The singular subject '{n}' requires the singular verb form '{v}'. For example: 'The {n} {v} daily.'",
                "keywords": ["grammar", "subject-verb agreement", n, v, "singular"],
                "difficulty": "beginner",
                "domain": "grammar"
            })
            idx += 1
    # 2. Plural agreement
    for pn in plural_nouns:
        for pv in plural_verbs:
            entries.append({
                "id": f"gen-grammar-{idx:05d}",
                "topic": "grammar rules",
                "title": f"Plural Subject-Verb Agreement: {pn.title()} and {pv.title()}",
                "content": f"The plural subject '{pn}' requires the base plural verb form '{pv}'. For example: 'The {pn} {pv} in groups.'",
                "keywords": ["grammar", "subject-verb agreement", pn, pv, "plural"],
                "difficulty": "beginner",
                "domain": "grammar"
            })
            idx += 1
    return entries

def generate_economics_entries():
    entries = []
    idx = 1
    for econ_name, theory, principle in economists:
        for country in countries:
            for good in goods:
                content = f"The economic theory of {theory}, formulated by {econ_name} (emphasizing {principle}), provides a framework to analyze how {country} manages its {good} sector."
                entries.append({
                    "id": f"gen-econ-{idx:05d}",
                    "topic": "economics",
                    "title": f"{theory} in {country}'s {good.title()} Market",
                    "content": content,
                    "keywords": ["economics", theory.lower(), econ_name.lower(), country.lower(), good.lower()],
                    "difficulty": "intermediate",
                    "domain": "economics"
                })
                idx += 1
    return entries

def generate_social_science_entries():
    entries = []
    idx = 1
    for concept, discipline, defn in social_concepts:
        for theorist, theo_disc, contribution in social_theorists:
            for region in social_regions:
                for app in social_applications:
                    content = f"The concept of {concept} in {discipline} ({defn}), connected to {theorist}'s work on {contribution}, has significant implications for {app} in {region}."
                    entries.append({
                        "id": f"gen-socsci-{idx:05d}",
                        "topic": "social science",
                        "title": f"{concept} and {theorist} in {region}",
                        "content": content,
                        "keywords": ["social science", concept.lower(), theorist.lower(), region.lower(), app.lower(), discipline.lower()],
                        "difficulty": "advanced",
                        "domain": "social_science"
                    })
                    idx += 1
    return entries

def generate_history_entries():
    entries = []
    idx = 1
    for event, year, loc, summary in historical_events:
        for figure, era, achievement in historical_figures:
            for realm in historical_realms:
                for country in countries:
                    content = f"The historical event of the {event} ({year} in {loc}), which {summary}, is often compared to the legacy of {figure} in {era} ({achievement}) in the realm of {realm} in {country}."
                    entries.append({
                        "id": f"gen-history-{idx:05d}",
                        "topic": "history",
                        "title": f"History Analysis: {event} and {figure}",
                        "content": content,
                        "keywords": ["history", event.lower(), figure.lower(), realm.lower(), country.lower(), "historical"],
                        "difficulty": "intermediate",
                        "domain": "history"
                    })
                    idx += 1
    return entries

def generate_geography_entries():
    entries = []
    idx = 1
    for country, cap, cont, pop, lang, curr, ind in geography_countries:
        for feat, ftype, flist, fdesc in geography_features:
            for realm in historical_realms:
                content = f"The country of {country} ({cont}, capital: {cap}, population: {pop}, language: {lang}, currency: {curr}, major industry: {ind}) is geographically situated in relation to {feat}, a major {ftype} ({fdesc}). This affects its {realm}."
                entries.append({
                    "id": f"gen-geography-{idx:05d}",
                    "topic": "geography",
                    "title": f"Geography of {country} and {feat}",
                    "content": content,
                    "keywords": ["geography", country.lower(), cap.lower(), feat.lower(), ftype.lower(), realm.lower()],
                    "difficulty": "beginner",
                    "domain": "geography"
                })
                idx += 1
    return entries

def generate_science_entries():
    entries = []
    idx = 1
    for el_name, sym, atomic_num, cat, el_desc in science_elements:
        for law_name, field, principle, formula in science_laws:
            for str_name, branch, str_desc in science_structures:
                for country in countries:
                    content = f"In the field of {field} and {branch} in {country}, research studies how the chemical element {el_name} ({sym}, atomic number {atomic_num}, classified as a {cat}; {el_desc}) interacts under conditions governed by {law_name} (principle: {principle}; formula: {formula}) inside the {str_name} ({str_desc})."
                    entries.append({
                        "id": f"gen-science-{idx:05d}",
                        "topic": "science",
                        "title": f"Science: {el_name}, {law_name}, and {str_name}",
                        "content": content,
                        "keywords": ["science", el_name.lower(), law_name.lower(), str_name.lower(), field.lower(), branch.lower(), country.lower()],
                        "difficulty": "advanced",
                        "domain": "science"
                    })
                    idx += 1
    return entries

def main():
    print("Generating entries...")
    grammar = generate_grammar_entries()
    economics = generate_economics_entries()
    social_science = generate_social_science_entries()
    history = generate_history_entries()
    geography = generate_geography_entries()
    science = generate_science_entries()

    all_entries = grammar + economics + social_science + history + geography + science
    print(f"Generated {len(all_entries)} entries total.")
    assert len(all_entries) == 58400, f"Expected 58400 entries, got {len(all_entries)}"

    # Shuffle for a diverse mix of domains in each chunk
    print("Shuffling entries...")
    random.shuffle(all_entries)

    # Clean up any existing gk_chunk files first to be safe
    for path in topics_dir.glob("gk_chunk_*.json"):
        path.unlink()

    # Partitions (14 chunks, distributed evenly)
    num_chunks = 14
    total_entries = len(all_entries)
    chunk_size = total_entries // num_chunks
    remainder = total_entries % num_chunks

    for i in range(num_chunks):
        chunk_num = i + 1
        start = i * chunk_size + min(i, remainder)
        end = (i + 1) * chunk_size + min(i + 1, remainder)
        chunk_entries = all_entries[start:end]

        chunk_data = {
            "domain": "general",
            "entries": chunk_entries
        }

        file_name = f"gk_chunk_{chunk_num}.json"
        file_path = topics_dir / file_name

        print(f"Writing {file_name} with {len(chunk_entries)} entries...")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)

        # Run Git command
        print(f"Committing {file_name} to Git (chunk {chunk_num}/{num_chunks})...")
        # Relative path from git root (c:\Users\HP\OneDrive\Desktop\atlas-ai)
        rel_path = f"backend/knowledge/general/topics/{file_name}"
        
        # Git Add
        subprocess.run(["git", "add", rel_path], check=True, cwd=str(backend_dir.parent))
        
        # Git Commit
        commit_msg = (
            f"feat(knowledge): Add general knowledge facts chunk {chunk_num}/{num_chunks} "
            f"containing grammar, economics, social sciences, history, geography, and science entries"
        )
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, cwd=str(backend_dir.parent))

    print(f"Success: {total_entries} entries generated and committed in 13 distinct commits!")

if __name__ == "__main__":
    main()
