import json
import random
import re
from pathlib import Path
import streamlit as st

# ---------------------------------------------------------------------------
# Page Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Static GK & GS Mastery — MCQ Fill in the Blanks",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).parent / "questions.json"

# ---------------------------------------------------------------------------
# Curated Exam-Grade Distractors (ensures realistic options even if an older
# questions.json without "options" is loaded)
# ---------------------------------------------------------------------------
BUILTIN_DISTRACTORS: dict[str, list[str]] = {
    # Physics
    "The SI unit of electric current is ____.": ["Volt", "Watt", "Coulomb"],
    "The SI unit of force is ____.": ["Joule", "Pascal", "Watt"],
    "The instrument used to measure atmospheric pressure is called a ____.": ["Hygrometer", "Anemometer", "Altimeter"],
    "Light travels fastest in ____.": ["Water", "Glass", "Diamond"],
    "The bending of light as it passes from one medium to another is called ____.": ["Reflection", "Diffraction", "Dispersion"],
    "The SI unit of electrical resistance is ____.": ["Ampere", "Volt", "Farad"],
    "The blue colour of the sky is primarily due to ____ of light.": ["Refraction", "Dispersion", "Diffraction"],
    "Sound waves cannot travel through a ____.": ["Solid", "Liquid", "Gas"],
    "The device used to convert mechanical energy into electrical energy is a ____.": ["Transformer", "Rectifier", "Electric motor"],
    "The SI unit of frequency is ____.": ["Decibel", "Newton", "Joule"],
    "Myopia (short-sightedness) is corrected using a ____ lens.": ["Convex", "Cylindrical", "Bifocal"],
    "The SI unit of power is ____.": ["Joule", "Newton", "Volt"],
    "A fuse wire is made of an alloy of tin and ____.": ["Copper", "Aluminium", "Zinc"],
    # Biology
    "The powerhouse of the cell is the ____.": ["Ribosome", "Golgi apparatus", "Lysosome"],
    "Deficiency of Vitamin C causes ____.": ["Rickets", "Beriberi", "Pellagra"],
    "The universal donor blood group is ____.": ["AB positive", "A positive", "B negative"],
    "The green pigment in plants responsible for photosynthesis is ____.": ["Carotene", "Xanthophyll", "Anthocyanin"],
    "The longest bone in the human body is the ____.": ["Tibia", "Humerus", "Fibula"],
    "Insulin is secreted by the ____ gland.": ["Thyroid", "Pituitary", "Adrenal"],
    "The largest organ of the human body is the ____.": ["Liver", "Heart", "Lungs"],
    "Deficiency of Vitamin D causes ____ in children.": ["Scurvy", "Goitre", "Beriberi"],
    "The functional unit of the kidney is the ____.": ["Neuron", "Alveolus", "Villus"],
    "Plants transport water from roots to leaves through ____ tissue.": ["Phloem", "Cambium", "Parenchyma"],
    "The normal resting pH of human blood is approximately ____.": ["6.8", "7.0", "8.2"],
    "Night blindness is caused by the deficiency of Vitamin ____.": ["B1", "C", "D"],
    "The smallest bone in the human body is the ____.": ["Malleus", "Incus", "Patella"],
    # Chemistry
    "The chemical symbol for Gold is ____.": ["Ag", "Gd", "Ga"],
    "The most abundant gas in Earth's atmosphere is ____.": ["Oxygen", "Carbon dioxide", "Argon"],
    "The pH value of pure neutral water at 25°C is ____.": ["5", "6", "8"],
    "Dry ice is the solid form of ____.": ["Nitrogen", "Ammonia", "Sulfur dioxide"],
    "The hardest naturally occurring substance is ____.": ["Quartz", "Corundum", "Topaz"],
    "Brass is an alloy of copper and ____.": ["Tin", "Nickel", "Lead"],
    "The acid present in vinegar is ____ acid.": ["Citric", "Formic", "Tartaric"],
    "The only metal that is liquid at room temperature is ____.": ["Gallium", "Cesium", "Sodium"],
    "Washing soda is chemically known as sodium ____.": ["Bicarbonate", "Hydroxide", "Chloride"],
    "Laughing gas is chemically known as ____ oxide.": ["Nitric", "Sulfur", "Carbon"],
    "The atomic number of an element equals the number of ____ in its nucleus.": ["Neutrons", "Nucleons", "Positrons"],
    "Rusting of iron is an example of ____.": ["Reduction", "Sublimation", "Neutralization"],
    # Indian Polity
    "The Constitution of India was adopted by the Constituent Assembly on 26 November ____.": ["1947", "1948", "1950"],
    "The Chairman of the Drafting Committee of the Indian Constitution was Dr. ____.": ["Rajendra Prasad", "S. Radhakrishnan", "K. M. Munshi"],
    "The minimum age to become a member of the Lok Sabha is ____ years.": ["18", "21", "30"],
    "The ex-officio Chairman of the Rajya Sabha is the ____ of India.": ["President", "Prime Minister", "Speaker"],
    "Fundamental Duties were added to the Constitution on the recommendation of the ____ Committee.": ["Sarkaria", "Mandal", "Balwant Rai Mehta"],
    "The concept of Directive Principles of State Policy (DPSP) was borrowed from the Constitution of ____.": ["USA", "Canada", "Australia"],
    "The ____ Schedule of the Indian Constitution contains the list of 22 recognized languages.": ["Seventh", "Ninth", "Eleventh"],
    "The Anti-Defection Law is contained in the ____ Schedule of the Indian Constitution.": ["Eighth", "Ninth", "Twelfth"],
    "The guardian and final interpreter of the Indian Constitution is the ____.": ["Parliament", "President", "Attorney General"],
    "A Money Bill can only be introduced in the ____.": ["Rajya Sabha", "Legislative Council", "Joint Sitting"],
    "The maximum gap between two sessions of Parliament cannot exceed ____ months.": ["3", "4", "12"],
    "The Comptroller and Auditor General (CAG) of India is appointed by the ____.": ["Prime Minister", "Chief Justice of India", "Speaker of Lok Sabha"],
    # Articles & Amendments
    "Article ____ of the Indian Constitution abolishes Untouchability.": ["14", "15", "18"],
    "Article ____ guarantees the Right to Life and Personal Liberty.": ["19", "20", "22"],
    "Dr. B. R. Ambedkar called Article ____ the 'Heart and Soul' of the Indian Constitution.": ["14", "21", "226"],
    "The ____ Constitutional Amendment Act (1976) is known as the 'Mini-Constitution'.": ["44th", "52nd", "73rd"],
    "The ____ Amendment Act lowered the voting age in India from 21 years to 18 years.": ["42nd", "52nd", "73rd"],
    "Panchayati Raj institutions were given constitutional status by the ____ Amendment Act, 1992.": ["42nd", "61st", "74th"],
    "The Goods and Services Tax (GST) was introduced by the ____ Constitutional Amendment Act, 2016.": ["99th", "100th", "102nd"],
    "Article ____ deals with the Uniform Civil Code for citizens.": ["40", "43", "48"],
    "Article ____ empowers Parliament to amend the Constitution.": ["352", "356", "360"],
    "The Right to Education (Article 21A) was inserted by the ____ Constitutional Amendment Act, 2002.": ["42nd", "73rd", "91st"],
    "Article ____ deals with the Election Commission of India.": ["280", "315", "338"],
    "Article ____ provides for the Finance Commission of India.": ["110", "312", "324"],
    "The ____ Amendment Act (1978) removed the Right to Property from Fundamental Rights and made it a legal right under Article 300A.": ["42nd", "52nd", "61st"],
    # National Parks
    "India's first National Park, established in 1936 as Hailey National Park, is ____ National Park.": ["Kaziranga", "Bandipur", "Kanha"],
    "Kaziranga National Park in Assam is famous for the ____.": ["Asiatic Lion", "Snow Leopard", "Sangai Deer"],
    "Gir National Park, the only natural habitat of the Asiatic Lion, is located in ____.": ["Rajasthan", "Madhya Pradesh", "Maharashtra"],
    "The world's only floating National Park, Keibul Lamjao, is situated in ____.": ["Assam", "Meghalaya", "Tripura"],
    "Sundarbans National Park, famous for Royal Bengal Tigers and mangroves, is in ____.": ["Odisha", "Assam", "Andhra Pradesh"],
    "The largest National Park in India by area is ____ National Park in Ladakh.": ["Dachigam", "Nanda Devi", "Desert"],
    "Dachigam National Park, famous for the Hangul (Kashmir Stag), is located in ____.": ["Himachal Pradesh", "Uttarakhand", "Ladakh"],
    "Silent Valley National Park is located in the Nilgiri Hills of ____.": ["Tamil Nadu", "Karnataka", "Goa"],
    "Ranthambore National Park is located in the state of ____.": ["Gujarat", "Madhya Pradesh", "Uttar Pradesh"],
    "Bandipur National Park is situated in the state of ____.": ["Kerala", "Tamil Nadu", "Andhra Pradesh"],
    "Simlipal National Park is located in ____.": ["Jharkhand", "Chhattisgarh", "West Bengal"],
    "Kanha National Park, which inspired Rudyard Kipling's 'The Jungle Book', is in ____.": ["Uttarakhand", "Maharashtra", "Rajasthan"],
    # All PM Yojanas
    "Pradhan Mantri Jan Dhan Yojana (PMJDY), launched on 28 August 2014, is India's flagship ____ inclusion mission.": ["Digital", "Agricultural", "Housing"],
    "Pradhan Mantri Ujjwala Yojana (PMUY) provides free ____ connections to women from BPL households.": ["Electricity", "Broadband", "Tap water"],
    "Under Ayushman Bharat (PM-JAY), eligible families receive health cover up to ₹____ lakh per family per year.": ["2", "3", "10"],
    "Under PM-KISAN (Pradhan Mantri Kisan Samman Nidhi), eligible farmer families receive ₹____ per year in three equal installments.": ["3000", "8000", "12000"],
    "Pradhan Mantri MUDRA Yojana provides collateral-free loans up to ₹10 lakh under three categories: Shishu, Kishore, and ____.": ["Vriddha", "Yuva", "Pragati"],
    "Beti Bachao Beti Padhao Yojana was launched on 22 January 2015 from Panipat, ____.": ["Punjab", "Rajasthan", "Uttar Pradesh"],
    "Swachh Bharat Mission was launched on 2 October ____.": ["2015", "2016", "2017"],
    "Atal Pension Yojana (APY) is open to Indian citizens aged between 18 and ____ years.": ["30", "50", "60"],
    "PM SVANidhi scheme provides micro-credit working capital loans to ____.": ["Marginal farmers", "Handloom weavers", "Dairy cooperatives"],
    "PM Vishwakarma Yojana, launched in September 2023, supports traditional ____ and craftspeople.": ["Fishermen", "Dairy farmers", "Folk artists"],
    "PM Surya Ghar: Muft Bijli Yojana aims to provide up to ____ units of free electricity per month via rooftop solar.": ["100", "200", "500"],
    "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY) offers a life insurance cover of ₹____ lakh.": ["1", "5", "10"],
    # Geography, Rivers & Dams
    "The longest river in India is the ____.": ["Yamuna", "Brahmaputra", "Godavari"],
    "The highest dam in India is the ____ Dam in Uttarakhand.": ["Bhakra Nangal", "Hirakud", "Sardar Sarovar"],
    "The longest dam in India is the ____ Dam built across the Mahanadi River.": ["Tehri", "Nagarjuna Sagar", "Mettur"],
    "The largest freshwater lake in India is ____ Lake in Jammu and Kashmir.": ["Dal", "Chilika", "Loktak"],
    "The river known as the 'Sorrow of Bihar' is the ____.": ["Damodar", "Gandak", "Son"],
    "The ____ Strait separates India from Sri Lanka.": ["Malacca", "Hormuz", "Sunda"],
    "The Tropic of Cancer passes through ____ Indian states.": ["6", "7", "9"],
    "The largest brackish water lagoon in India is ____ Lake in Odisha.": ["Pulicat", "Vembanad", "Kolleru"],
    "The longest river in Peninsular India (also called Dakshin Ganga) is the ____.": ["Krishna", "Kaveri", "Mahanadi"],
    "Nathu La pass connects Sikkim with ____.": ["Nepal", "Bhutan", "Myanmar"],
    # Awards, Dances & Orgs
    "The classical dance form Kuchipudi originated in the state of ____.": ["Tamil Nadu", "Odisha", "Karnataka"],
    "Kathakali is a classical dance form of ____.": ["Tamil Nadu", "Andhra Pradesh", "Manipur"],
    "The headquarters of the World Health Organization (WHO) is located in ____.": ["New York", "Paris", "Vienna"],
    "The headquarters of UNESCO is located in ____.": ["Geneva", "Rome", "London"],
    "India's highest civilian award is the ____.": ["Padma Vibhushan", "Padma Bhushan", "Param Vir Chakra"],
    "The Dronacharya Award is given for excellence in sports ____.": ["Journalism", "Administration", "Officiating"],
    "Bihu is the famous folk dance and harvest festival of ____.": ["Manipur", "Tripura", "Meghalaya"],
    "The Thomas Cup is associated with the sport of ____.": ["Tennis", "Table Tennis", "Squash"],
    "The Hornbill Festival is celebrated annually in the state of ____.": ["Mizoram", "Manipur", "Arunachal Pradesh"],
    "The International Court of Justice (ICJ) is headquartered at The Hague in the ____.": ["Switzerland", "Belgium", "Austria"],
    # History & Monuments
    "The Great Bath was discovered at the Indus Valley site of ____.": ["Harappa", "Lothal", "Kalibangan"],
    "Gautama Buddha delivered his first sermon at ____.": ["Bodh Gaya", "Lumbini", "Kushinagar"],
    "The Battle of Plassey was fought in the year ____.": ["1764", "1761", "1759"],
    "The founder of the Maurya Empire was ____.": ["Ashoka", "Bindusara", "Samudragupta"],
    "The Sun Temple at Konark was built by King ____ I of the Eastern Ganga dynasty.": ["Rajaraja", "Pulakeshin", "Krishnadevaraya"],
    "The Quit India Movement was launched by Mahatma Gandhi in August ____.": ["1930", "1920", "1945"],
    "The Ajanta and Ellora caves are located near Aurangabad (Chhatrapati Sambhajinagar) in ____.": ["Madhya Pradesh", "Karnataka", "Gujarat"],
    "The Indian National Congress was founded in 1885 in Bombay; its first President was ____.": ["Dadabhai Naoroji", "Surendranath Banerjee", "A. O. Hume"],
    "The Brihadeeswarar Temple at Thanjavur was built by ____.": ["Rajendra Chola I", "Narasimhavarman I", "Krishnadevaraya"],
    "The Jallianwala Bagh massacre took place on 13 April ____.": ["1917", "1921", "1922"],
}

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Jammu and Kashmir", "Ladakh",
]

# ---------------------------------------------------------------------------
# Beautiful Custom CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    --accent: #6366f1;
    --accent-soft: rgba(99, 102, 241, 0.14);
    --success: #10b981;
    --success-soft: rgba(16, 185, 129, 0.15);
    --danger: #ef4444;
    --danger-soft: rgba(239, 68, 68, 0.15);
    --card-bg: rgba(255, 255, 255, 0.04);
    --card-border: rgba(148, 163, 184, 0.24);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 820px !important;
}

.hero-header {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #ec4899 100%);
    padding: 1.45rem 1.75rem;
    border-radius: 18px;
    color: #ffffff;
    margin-bottom: 1.2rem;
    box-shadow: 0 12px 30px -10px rgba(79, 70, 229, 0.45);
}
.hero-title {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 0.25rem 0;
}
.hero-sub {
    font-size: 0.92rem;
    opacity: 0.92;
    margin: 0;
}

.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.2rem;
}
.stat-pill {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 0.72rem 0.9rem;
    text-align: center;
    backdrop-filter: blur(8px);
}
.stat-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.7;
    font-weight: 600;
}
.stat-val {
    font-size: 1.25rem;
    font-weight: 800;
    margin-top: 0.15rem;
}

.q-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 1.65rem 1.75rem 1.45rem 1.75rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 10px 30px -15px rgba(15, 23, 42, 0.25);
}
.q-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.q-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: var(--accent-soft);
    color: #818cf8;
    border: 1px solid rgba(129, 140, 248, 0.35);
    padding: 0.3rem 0.78rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
}
.q-counter {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    opacity: 0.75;
    font-weight: 600;
}
.q-text {
    font-size: 1.26rem;
    line-height: 1.65;
    font-weight: 600;
    margin: 0.25rem 0 0.35rem 0;
}
.blank-highlight {
    display: inline-block;
    min-width: 92px;
    border-bottom: 3px dashed #818cf8;
    color: #818cf8;
    text-align: center;
    padding: 0 0.45rem;
    margin: 0 0.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
}
.blank-filled-ok {
    border-bottom: 3px solid var(--success);
    color: var(--success);
}
.blank-filled-bad {
    border-bottom: 3px solid var(--danger);
    color: var(--danger);
}

.option-grid div[data-testid="stButton"] > button {
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.85rem 1.1rem !important;
    border-radius: 14px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border: 1px solid var(--card-border) !important;
    transition: transform 0.12s ease, border-color 0.15s ease, box-shadow 0.15s ease !important;
}
.option-grid div[data-testid="stButton"] > button:hover:not(:disabled) {
    transform: translateY(-2px);
    border-color: #818cf8 !important;
    box-shadow: 0 6px 18px -8px rgba(99, 102, 241, 0.45);
}

.fb-box {
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin: 0.9rem 0 1rem 0;
    border-left: 5px solid;
    animation: fadeSlide 0.25s ease-out;
}
.fb-correct {
    background: var(--success-soft);
    border-left-color: var(--success);
}
.fb-wrong {
    background: var(--danger-soft);
    border-left-color: var(--danger);
}
.fb-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.25rem;
}
.fb-exp {
    font-size: 0.9rem;
    opacity: 0.92;
    line-height: 1.5;
}

@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.pinned-tag {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: #fff;
    margin-bottom: 0.35rem;
}

@media (max-width: 640px) {
    .stats-row { grid-template-columns: repeat(2, 1fr); }
    .q-text { font-size: 1.1rem; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Smart Type-Aware Distractor Engine (for imported Qs without custom options)
# ---------------------------------------------------------------------------
def _ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def generate_smart_distractors(q_obj: dict, sec_answers: list[str]) -> list[str]:
    q_text = q_obj.get("question", "")
    ans = str(q_obj.get("answer", "")).strip()

    # 1. Exact curated match from BUILTIN_DISTRACTORS
    if q_text in BUILTIN_DISTRACTORS:
        return [ans] + BUILTIN_DISTRACTORS[q_text][:3]

    # 2. Type-aware generation so distractors ALWAYS match the question format
    # Year (e.g., 1949, 2014, 1757)
    if re.fullmatch(r"(1[5-9]\d{2}|20[0-2]\d)", ans):
        yr = int(ans)
        offsets = [-5, -3, -2, -1, 1, 2, 3, 5]
        cands = [str(yr + d) for d in offsets if 1500 <= yr + d <= 2026]
        random.shuffle(cands)
        return [ans] + cands[:3]

    # Ordinal amendment / number (e.g., 42nd, 73rd, 101st)
    m_ord = re.fullmatch(r"(\d+)(st|nd|rd|th)", ans, re.IGNORECASE)
    if m_ord:
        num = int(m_ord.group(1))
        deltas = [-10, -4, -2, -1, 1, 2, 4, 8]
        cands = [_ordinal(num + d) for d in deltas if num + d > 0]
        random.shuffle(cands)
        return [ans] + cands[:3]

    # Plain integer (e.g., 5, 25, 300, 6000, Article 280)
    if re.fullmatch(r"\d+", ans):
        val = int(ans)
        if val <= 15:
            pool = [str(x) for x in range(max(1, val - 3), val + 6) if x != val]
        elif val <= 100:
            step = 5 if val % 5 == 0 else 2
            pool = [str(val + d * step) for d in (-3, -2, -1, 1, 2, 3) if val + d * step > 0]
        elif val <= 400:
            step = 10 if val % 10 == 0 else 4
            pool = [str(val + d * step) for d in (-4, -2, -1, 1, 2, 4) if val + d * step > 0]
        else:
            step = max(500, (val // 6 // 100) * 100)
            pool = [str(val + d * step) for d in (-2, -1, 1, 2, 3) if val + d * step > 0]
        random.shuffle(pool)
        return [ans] + pool[:3]

    # Decimal number (e.g., 7.4)
    if re.fullmatch(r"\d+\.\d+", ans):
        val = float(ans)
        cands = [f"{val + d:.1f}" for d in (-0.8, -0.4, 0.4, 0.8, 1.2) if val + d > 0]
        random.shuffle(cands)
        return [ans] + cands[:3]

    # Indian State / UT
    if ans in INDIAN_STATES:
        others = [s for s in INDIAN_STATES if s != ans]
        random.shuffle(others)
        return [ans] + others[:3]

    # Single vitamin letter (A, B, C, D, E, K)
    if ans in {"A", "B", "C", "D", "E", "K"}:
        others = [v for v in ["A", "B", "C", "D", "E", "K"] if v != ans]
        random.shuffle(others)
        return [ans] + others[:3]

    # Same-section non-numeric answers only (never mix numbers/letters with names)
    same_sec = [
        a for a in sec_answers
        if a != ans and not re.fullmatch(r"[\d\.]+", a) and len(a) > 1
    ]
    random.shuffle(same_sec)
    opts = [ans] + same_sec[:3]
    return opts


# ---------------------------------------------------------------------------
# Data Helpers
# ---------------------------------------------------------------------------
def load_data() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sections": []}


def save_data(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_question_pool(data: dict, section_id: str, shuffle: bool = True) -> list[dict]:
    pool = []
    for sec in data.get("sections", []):
        if section_id == "ALL" or sec["id"] == section_id:
            sec_answers = [q["answer"] for q in sec.get("questions", []) if q.get("answer")]
            for q in sec.get("questions", []):
                item = dict(q)
                item["section_name"] = f"{sec.get('icon', '📘')} {sec['name']}"
                opts = list(q.get("options", []))
                if len(opts) < 4:
                    opts = generate_smart_distractors(q, sec_answers)
                # Ensure answer is present and options are unique
                seen = set()
                clean_opts = []
                for o in ([q["answer"]] + opts):
                    if o not in seen:
                        seen.add(o)
                        clean_opts.append(o)
                clean_opts = clean_opts[:4]
                random.shuffle(clean_opts)
                item["shuffled_options"] = clean_opts
                pool.append(item)
    if shuffle or section_id == "ALL":
        random.shuffle(pool)
    return pool


def format_question_html(q_text: str, revealed_answer: str | None = None, is_ok: bool | None = None) -> str:
    if revealed_answer:
        cls = "blank-highlight blank-filled-ok" if is_ok else "blank-highlight blank-filled-bad"
        replacement = f"<span class='{cls}'>{revealed_answer}</span>"
    else:
        replacement = "<span class='blank-highlight'>________</span>"
    return re.sub(r"_{2,}", replacement, q_text)


# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = load_data()

if "active_section" not in st.session_state:
    st.session_state.active_section = "ALL"

if "shuffle_mode" not in st.session_state:
    st.session_state.shuffle_mode = True

if "pool" not in st.session_state:
    st.session_state.pool = build_question_pool(st.session_state.quiz_data, "ALL", shuffle=True)

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "attempted" not in st.session_state:
    st.session_state.attempted = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

if "last_correct" not in st.session_state:
    st.session_state.last_correct = None

if "wrong_list" not in st.session_state:
    st.session_state.wrong_list = []


def reset_quiz(section_id: str, shuffle: bool = True):
    st.session_state.active_section = section_id
    st.session_state.pool = build_question_pool(
        st.session_state.quiz_data, section_id, shuffle=shuffle
    )
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.attempted = 0
    st.session_state.streak = 0
    st.session_state.selected_option = None
    st.session_state.last_correct = None
    st.session_state.wrong_list = []


def handle_option_click(chosen: str, current_q: dict):
    if st.session_state.selected_option is not None:
        return
    st.session_state.selected_option = chosen
    st.session_state.attempted += 1
    if chosen == current_q["answer"]:
        st.session_state.last_correct = True
        st.session_state.score += 1
        st.session_state.streak += 1
    else:
        st.session_state.last_correct = False
        st.session_state.streak = 0
        st.session_state.wrong_list.append({
            "question": current_q["question"],
            "yours": chosen,
            "answer": current_q["answer"],
            "explanation": current_q.get("explanation", ""),
        })


# ---------------------------------------------------------------------------
# Sidebar: Pinned "All" + Sections
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📚 Sections")

    total_qs = sum(len(s.get("questions", [])) for s in st.session_state.quiz_data["sections"])

    st.markdown("<span class='pinned-tag'>📌 Pinned</span>", unsafe_allow_html=True)
    all_label = f"🎲 All Sections (Random Mix) · {total_qs}"
    if st.button(
        all_label,
        key="sec_btn_ALL",
        use_container_width=True,
        type="primary" if st.session_state.active_section == "ALL" else "secondary",
    ):
        reset_quiz("ALL", shuffle=True)
        st.rerun()

    st.markdown("---")
    st.caption("SUBJECT & STATIC GK SECTIONS")

    for sec in st.session_state.quiz_data["sections"]:
        q_count = len(sec.get("questions", []))
        btn_type = "primary" if st.session_state.active_section == sec["id"] else "secondary"
        if st.button(
            f"{sec.get('icon', '📘')} {sec['name']} · {q_count}",
            key=f"sec_btn_{sec['id']}",
            use_container_width=True,
            type=btn_type,
        ):
            reset_quiz(sec["id"], shuffle=st.session_state.shuffle_mode)
            st.rerun()

    st.markdown("---")
    shuffle_toggle = st.toggle("🔀 Shuffle questions", value=st.session_state.shuffle_mode)
    if shuffle_toggle != st.session_state.shuffle_mode:
        st.session_state.shuffle_mode = shuffle_toggle
        reset_quiz(st.session_state.active_section, shuffle=shuffle_toggle)
        st.rerun()

    if st.button("🔄 Restart Current Section", use_container_width=True):
        reset_quiz(st.session_state.active_section, shuffle=st.session_state.shuffle_mode)
        st.rerun()

# ---------------------------------------------------------------------------
# Main Area Tabs
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-header">
        <div class="hero-title">🧠 Static GK & General Science</div>
        <div class="hero-sub">Pick the one correct option for each blank, then hit Next!</div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_quiz, tab_manage = st.tabs(["🎯 Practice Quiz", "➕ Add Questions / New Section"])

with tab_quiz:
    pool = st.session_state.pool
    idx = st.session_state.q_index
    total = len(pool)

    accuracy = (
        f"{round((st.session_state.score / st.session_state.attempted) * 100)}%"
        if st.session_state.attempted > 0
        else "—"
    )
    st.markdown(
        f"""
        <div class="stats-row">
            <div class="stat-pill">
                <div class="stat-label">Score</div>
                <div class="stat-val">{st.session_state.score} / {st.session_state.attempted}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-label">Accuracy</div>
                <div class="stat-val">{accuracy}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-label">Streak</div>
                <div class="stat-val">🔥 {st.session_state.streak}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-label">Remaining</div>
                <div class="stat-val">{max(total - idx, 0)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if total == 0:
        st.info("No questions in this section yet. Switch to **Add Questions / New Section** to add some!")
    elif idx >= total:
        st.balloons()
        st.success(f"🎉 Section Complete! You scored **{st.session_state.score} out of {st.session_state.attempted}** ({accuracy}).")

        if st.session_state.wrong_list:
            with st.expander(f"📝 Review Missed Questions ({len(st.session_state.wrong_list)})", expanded=True):
                for item in st.session_state.wrong_list:
                    st.markdown(f"**Q:** {item['question']}")
                    st.markdown(f"- **Your choice:** `{item['yours']}`  |  **Correct:** `{item['answer']}`")
                    if item.get("explanation"):
                        st.caption(item["explanation"])
                    st.markdown("---")

        if st.button("🔁 Practice Again", type="primary", use_container_width=True):
            reset_quiz(st.session_state.active_section, shuffle=st.session_state.shuffle_mode)
            st.rerun()
    else:
        st.progress(idx / total)

        current_q = pool[idx]
        answered = st.session_state.selected_option is not None
        revealed = current_q["answer"] if answered else None
        q_html = format_question_html(
            current_q["question"],
            revealed_answer=revealed,
            is_ok=st.session_state.last_correct,
        )

        st.markdown(
            f"""
            <div class="q-card">
                <div class="q-meta">
                    <span class="q-badge">{current_q['section_name']}</span>
                    <span class="q-counter">Question {idx + 1} of {total}</span>
                </div>
                <div class="q-text">{q_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        options = current_q["shuffled_options"]
        labels = ["A", "B", "C", "D"]
        st.markdown('<div class="option-grid">', unsafe_allow_html=True)
        row1 = st.columns(2)
        row2 = st.columns(2)
        grid_cols = [row1[0], row1[1], row2[0], row2[1]]

        for i, opt in enumerate(options):
            prefix = f"{labels[i]}."
            btn_type = "secondary"
            display_label = f"{prefix}  {opt}"

            if answered:
                if opt == current_q["answer"]:
                    display_label = f"✅ {prefix}  {opt}"
                    btn_type = "primary"
                elif opt == st.session_state.selected_option:
                    display_label = f"❌ {prefix}  {opt}"

            with grid_cols[i]:
                if st.button(
                    display_label,
                    key=f"opt_{idx}_{i}",
                    use_container_width=True,
                    type=btn_type,
                    disabled=answered,
                ):
                    handle_option_click(opt, current_q)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if answered:
            exp_text = current_q.get("explanation", "")
            if st.session_state.last_correct:
                st.markdown(
                    f"""
                    <div class="fb-box fb-correct">
                        <div class="fb-title">✅ Correct! — {current_q['answer']}</div>
                        <div class="fb-exp">{exp_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="fb-box fb-wrong">
                        <div class="fb-title">❌ Incorrect — Correct Answer: {current_q['answer']}</div>
                        <div class="fb-exp">{exp_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.write("")
        nav_col1, nav_col2 = st.columns([3, 1])
        with nav_col1:
            next_label = "Finish & See Score 🏁" if idx + 1 == total else "Next Question ➡️"
            if st.button(
                next_label,
                key=f"next_{idx}",
                type="primary" if answered else "secondary",
                use_container_width=True,
            ):
                st.session_state.q_index += 1
                st.session_state.selected_option = None
                st.session_state.last_correct = None
                st.rerun()
        with nav_col2:
            if st.button("⏭️ Skip", key=f"skip_{idx}", use_container_width=True, disabled=answered):
                st.session_state.q_index += 1
                st.session_state.selected_option = None
                st.session_state.last_correct = None
                st.rerun()

with tab_manage:
    st.subheader("🆕 Create a New Section")
    with st.form("new_section_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            new_sec_name = st.text_input("Section Name", placeholder="e.g., Indian Economy, Space & ISRO")
        with c2:
            new_sec_icon = st.text_input("Emoji Icon", value="📘")
        new_sec_desc = st.text_input("Short Description", placeholder="Brief description of this section")
        create_sec = st.form_submit_button("Create Section", type="primary")

        if create_sec:
            if not new_sec_name.strip():
                st.error("Please enter a section name.")
            else:
                sec_id = re.sub(r"[^a-z0-9]+", "_", new_sec_name.strip().lower()).strip("_")
                existing_ids = {s["id"] for s in st.session_state.quiz_data["sections"]}
                if sec_id in existing_ids:
                    st.warning("A section with that name already exists.")
                else:
                    st.session_state.quiz_data["sections"].append({
                        "id": sec_id,
                        "name": new_sec_name.strip(),
                        "icon": new_sec_icon.strip() or "📘",
                        "description": new_sec_desc.strip(),
                        "questions": [],
                    })
                    save_data(st.session_state.quiz_data)
                    st.success(f"Section **{new_sec_name}** created!")
                    st.rerun()

    st.markdown("---")
    st.subheader("📄 Bulk Import from a Paper / Notes")
    st.caption(
        "Best format (4 custom options): `Question with ____ | Correct Answer | Wrong 1 | Wrong 2 | Wrong 3 | Optional Explanation`  \n"
        "Quick format (smart type-matched options): `Question with ____ | Correct Answer | Optional Explanation`"
    )

    sec_options = {s["name"]: s["id"] for s in st.session_state.quiz_data["sections"]}
    target_sec_name = st.selectbox("Target Section", list(sec_options.keys()))
    bulk_text = st.text_area(
        "Paste Questions",
        height=160,
        placeholder="The SI unit of pressure is ____. | Pascal | Newton | Joule | Watt | 1 Pascal = 1 N/m².",
    )
    if st.button("📥 Import Questions", type="primary"):
        lines = [ln.strip() for ln in bulk_text.splitlines() if ln.strip()]
        added = 0
        target_id = sec_options[target_sec_name]
        for ln in lines:
            parts = [p.strip() for p in ln.split("|")]
            if len(parts) >= 5:
                q_entry = {
                    "question": parts[0],
                    "answer": parts[1],
                    "options": parts[1:5],
                    "explanation": parts[5] if len(parts) >= 6 else "",
                }
            elif len(parts) >= 2 and parts[0] and parts[1]:
                q_entry = {
                    "question": parts[0],
                    "answer": parts[1],
                    "options": [],
                    "explanation": parts[2] if len(parts) >= 3 else "",
                }
            else:
                continue

            for s in st.session_state.quiz_data["sections"]:
                if s["id"] == target_id:
                    s["questions"].append(q_entry)
                    added += 1
                    break

        if added > 0:
            save_data(st.session_state.quiz_data)
            reset_quiz(st.session_state.active_section, shuffle=st.session_state.shuffle_mode)
            st.success(f"Added **{added}** question(s) to **{target_sec_name}**!")
            st.rerun()
        else:
            st.warning("No valid lines found. Use `Question | Answer | Opt2 | Opt3 | Opt4` or `Question | Answer`.")

    st.markdown("---")
    st.download_button(
        label="⬇️ Download Updated questions.json",
        data=json.dumps(st.session_state.quiz_data, indent=2, ensure_ascii=False),
        file_name="questions.json",
        mime="application/json",
    )