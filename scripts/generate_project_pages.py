#!/usr/bin/env python3

import html
import json
import re
import subprocess
import unicodedata
from pathlib import Path


ROOT = Path("/home/shepherd/workspace/cellweb")
PDF_DIR = ROOT / "pdfs"
PUBLICATIONS_FILE = ROOT / "publications" / "index.html"
PROJECTS_DIR = ROOT / "projects"
DATA_JS = PROJECTS_DIR / "projects-data.js"


AREA_META = {
    "llm": {
        "label": "Domain-Specialized Language Systems",
        "context": "This project sits in CELL's work on retrieval, domain specialization, and adaptive compression for language systems under strict deployment budgets.",
    },
    "gen-ai": {
        "label": "Generative AI for Systems and Media",
        "context": "This project reflects CELL's use of generative models to synthesize difficult-to-collect data, emulate system behavior, or accelerate emerging media workloads.",
    },
    "hd": {
        "label": "Brain-Inspired Hyperdimensional Computing",
        "context": "This project belongs to CELL's hyperdimensional computing line, where lightweight symbolic representations are used to build efficient, robust learning systems.",
    },
    "systems": {
        "label": "Efficient Systems and Accelerators",
        "context": "This project falls in CELL's systems thread, where accelerators, memory systems, and deployment-aware optimization are redesigned for practical efficiency.",
    },
}


OVERRIDES = {
    "Bit-Level_Semantics_Scalable_RAG_Retrieval_with_Neurosymbolic_Hyperdimensional_Computing.pdf": {
        "slug": "bit-level-semantics",
        "area": "llm",
        "tags": ["RAG Retrieval", "Hyperdimensional Computing"],
        "venue_short": "PACT 2025",
        "summary": "Binary hypervectors and HD-NSW make RAG retrieval scale to tens of millions of documents with dense-level quality at much lower memory cost.",
    },
    "a_diffusion_based_framework_for_configurable_and_realistic_multi_storage_trace_g.pdf": {
        "slug": "ditto-storage-traces",
        "area": "gen-ai",
        "tags": ["Diffusion Model", "Storage Systems"],
        "venue_short": "DAC 2025 LBR",
        "summary": "A diffusion model generates realistic, configurable multi-device storage traces so storage studies no longer depend on scarce hand-collected traces alone.",
        "title": "A Diffusion-Based Framework for Configurable and Realistic Multi-Storage Trace Generation",
    },
    "Late_Breaking_Results_Hyperdimensional_Regression_with_Fine-Grained_and_Scalable_Confidence-Based_Learning.pdf": {
        "slug": "hd-regression-confidence",
        "area": "hd",
        "tags": ["Regression", "Confidence-Based Learning"],
        "venue_short": "DATE 2025 LBR",
        "summary": "Confidence-aware HD regression adds fine-grained encoding and scalable uncertainty handling for more reliable continuous prediction.",
    },
    "Diffusion-Based Generative System Surrogates for Scalable Learning-Driven Optimization in Virtual Playgrounds.pdf": {
        "slug": "diffnest-system-surrogates",
        "area": "gen-ai",
        "tags": ["Diffusion Surrogate", "System Optimization"],
        "venue_short": "PACM MACS 2025",
        "summary": "Diffusion-generated surrogate traces let system optimization explore large design spaces without expensive data collection on physical hardware.",
    },
    "Late_Breaking_Results_Dynamically_Scalable_Pruning_for_Transformer-Based_Large_Language_Models.pdf": {
        "slug": "matryoshka-llm-pruning",
        "area": "llm",
        "tags": ["LLM Pruning", "Dynamic Runtime"],
        "venue_short": "DATE 2025 LBR",
        "summary": "Incremental submodels let a single pruned transformer adapt its runtime cost to changing latency and throughput budgets.",
    },
    "Hyperdimensional_Computing-Based_Federated_Learning_in_Mobile_Robots_Through_Synthetic_Oversampling.pdf": {
        "slug": "hd-federated-mobile-robots",
        "area": "hd",
        "tags": ["Federated Learning", "Mobile Robotics"],
        "venue_short": "ICRA 2025",
        "summary": "Synthetic oversampling strengthens hyperdimensional federated learning for mobile robots when local data are small, imbalanced, or privacy sensitive.",
    },
    "flexnerfer_a_multi_dataflow_adaptive_sparsity_aware_accelerator_for_on_device.pdf": {
        "slug": "flexnerfer",
        "area": "systems",
        "tags": ["NeRF Accelerator", "On-Device Rendering"],
        "venue_short": "ISCA 2025",
        "summary": "A multi-dataflow NeRF accelerator supports sparsity and precision scaling for efficient on-device 3D view synthesis.",
        "title": "FlexNeRFer: A Multi-Dataflow, Adaptive Sparsity-Aware Accelerator for On-Device NeRF Rendering",
    },
    "Efficient_Forward-Only_Training_for_Brain-Inspired_Hyperdimensional_Computing.pdf": {
        "slug": "forward-only-hdc-training",
        "area": "hd",
        "tags": ["Forward-Only", "HD Training"],
        "venue_short": "ICCD 2024",
        "summary": "Forward-only updates reduce the cost of HD training while preserving the lightweight learning behavior needed for edge deployment.",
    },
    "Advancing Hyperdimensional Computing Based on Trainable Encoding and Adaptive Training for Efficient.pdf": {
        "slug": "trainablehd",
        "area": "hd",
        "tags": ["Trainable Encoding", "Quantization"],
        "venue_short": "TODAES 2024",
        "summary": "TrainableHD replaces static encoders with trainable representations and adaptive optimization, pushing HDC closer to deep-learning-level accuracy.",
        "abstract": "TrainableHD revisits hyperdimensional computing by replacing fixed random encoders and static training rules with a trainable encoder, adaptive optimizers, and quantization-aware execution. The paper shows that these changes let HDC capture richer feature relationships, improve accuracy by up to 27.99% with no extra inference cost, and deliver strong speed and energy efficiency on low-power accelerators compared with deep learning baselines.",
        "title": "Advancing Hyperdimensional Computing Based on Trainable Encoding and Adaptive Training for Efficient and Accurate Learning",
    },
    "Brain-Inspired_Hyperdimensional_Computing_in_the_Wild_Lightweight_Symbolic_Learning_for_Sensorimotor_Controls_of_Wheeled_Robots.pdf": {
        "slug": "hdc-in-the-wild-robots",
        "area": "hd",
        "tags": ["Robotics", "Symbolic Control"],
        "venue_short": "ICRA 2024",
        "summary": "A robotic control stack uses lightweight symbolic learning to keep wheeled robots efficient and robust in real-world sensorimotor settings.",
    },
    "Towards_Forward-Only_Learning_for_Hyperdimensional_Computing.pdf": {
        "slug": "towards-forward-only-hdc",
        "area": "hd",
        "tags": ["Forward-Only", "Learning Rule"],
        "venue_short": "DATE 2024",
        "summary": "This work reframes HD learning around forward-only optimization to simplify training and improve practicality on resource-limited hardware.",
    },
    "Hierarchical_Distributed_and_Brain-Inspired_Learning_for_Internet_of_Things_Systems.pdf": {
        "slug": "edgehd-iot",
        "area": "hd",
        "tags": ["Edge Learning", "IoT Systems"],
        "venue_short": "ICDCS 2023",
        "summary": "EdgeHD distributes online learning across IoT hierarchies so edge systems can adapt continuously without centralizing all data.",
    },
    "Sidekick_Near_Data_Processing_for_Clustering_Enhanced_by_Automatic_Memory_Disaggregation.pdf": {
        "slug": "sidekick-cxl-clustering",
        "area": "systems",
        "tags": ["CXL", "Near-Data Processing"],
        "venue_short": "DAC 2023",
        "summary": "CXL-aware near-data processing and program-context-driven allocation accelerate clustering on disaggregated memory systems.",
        "title": "Sidekick: Near Data Processing for Clustering Enhanced by Automatic Memory Disaggregation",
        "authors": "Sanghoon Lee, Jongho Park, Minho Ha, Byung Il Koh, Kyoung Park, and Yeseong Kim",
        "venue_full": "2023 60th ACM/IEEE Design Automation Conference (DAC), IEEE, 2023",
        "citation": "Sanghoon Lee, Jongho Park, Minho Ha, Byung Il Koh, Kyoung Park, and Yeseong Kim. \"Sidekick: Near Data Processing for Clustering Enhanced by Automatic Memory Disaggregation,\" in 2023 60th ACM/IEEE Design Automation Conference (DAC), IEEE, 2023.",
    },
    "Comprehensive_Integration_of_Hyperdimensional_Computing_with_Deep_Learning_towards_Neuro-Symbolic_AI.pdf": {
        "slug": "neuro-symbolic-hdc-deep-learning",
        "area": "hd",
        "tags": ["Neuro-Symbolic AI", "Deep Learning"],
        "venue_short": "DAC 2023",
        "summary": "A neuro-symbolic pipeline combines HD computing with deep learning so symbolic efficiency and learned perception can reinforce each other.",
    },
    "Efficient_Hyperdimensional_Learning_with_Trainable_Quantizable_and_Holistic_Data_Representation.pdf": {
        "slug": "holistic-trainable-hdc",
        "area": "hd",
        "tags": ["Trainable Encoding", "Quantization"],
        "venue_short": "DATE 2023",
        "summary": "Trainable, quantizable, holistic data representations make HD learning both more accurate and easier to deploy on efficient hardware.",
        "title": "Efficient Hyperdimensional Learning with Trainable, Quantizable, and Holistic Data Representation",
        "authors": "Jiseung Kim, Hyunsei Lee, Mohsen Imani, and Yeseong Kim",
        "venue_full": "2023 Design, Automation & Test in Europe Conference & Exhibition (DATE), IEEE, 2023",
        "citation": "Jiseung Kim, Hyunsei Lee, Mohsen Imani, and Yeseong Kim. \"Efficient Hyperdimensional Learning with Trainable, Quantizable, and Holistic Data Representation,\" in 2023 Design, Automation & Test in Europe Conference & Exhibition (DATE), IEEE, 2023.",
    },
    "iltNet efficient deep learning inference on multi-chip accelerators using model partitioning.pdf": {
        "slug": "quiltnet",
        "area": "systems",
        "tags": ["Multi-Chip Inference", "Model Partitioning"],
        "venue_short": "DAC 2022",
        "summary": "Autoencoder-based model partitioning cuts inter-chip communication so larger neural networks can run efficiently across multiple accelerators.",
        "title": "QuiltNet: Efficient Deep Learning Inference on Multi-Chip Accelerators Using Model Partitioning",
    },
    "Algorithm-Hardware_Co-Design_for_Efficient_Brain-Inspired_Hyperdimensional_Learning_on_Edge.pdf": {
        "slug": "algorithm-hardware-hdc-edge",
        "area": "hd",
        "tags": ["Edge TPU", "Co-Design"],
        "venue_short": "DATE 2022",
        "summary": "An HDC pipeline reinterpreted as a hyper-wide neural network leverages CPUs and Edge TPUs together for fast edge learning.",
        "preferred_year": "2022",
        "award": "Best Paper Award",
        "title": "Algorithm-Hardware Co-Design for Efficient Brain-Inspired Hyperdimensional Learning on Edge",
    },
    "Online_Performance_and_Power_Prediction_for_Edge_TPU_via_Comprehensive_Characterization.pdf": {
        "slug": "edge-tpu-performance-power",
        "area": "systems",
        "tags": ["Performance Modeling", "Edge TPU"],
        "venue_short": "DATE 2022",
        "summary": "Comprehensive characterization turns Edge TPU behavior into predictive models for performance and power-aware deployment.",
    },
    "Massively_Parallel_Big_Data_Classification_on_a_Programmable_Processing_In-Memory_Architecture.pdf": {
        "slug": "pim-big-data-classification",
        "area": "systems",
        "tags": ["Processing in Memory", "Big Data"],
        "venue_short": "ICCAD 2021",
        "summary": "A programmable processing-in-memory architecture brings large-scale classification closer to data to reduce movement and increase throughput.",
    },
    "CascadeHD_Efficient_Many-Class_Learning_Framework_Using_Hyperdimensional_Computing.pdf": {
        "slug": "cascadehd",
        "area": "hd",
        "tags": ["Many-Class Learning", "HDC"],
        "venue_short": "DAC 2021",
        "summary": "A cascaded HDC framework scales many-class classification without giving up the efficiency that makes HD learning attractive.",
    },
    "Efficient_Brain-Inspired_Hyperdimensional_Learning_with_Spatiotemporal_Structured_Data.pdf": {
        "slug": "stemhd-spatiotemporal",
        "area": "hd",
        "tags": ["Spatiotemporal Data", "Accelerator"],
        "venue_short": "MASCOTS 2021",
        "summary": "STEM-HD preserves spatial and temporal structure in HDC encodings, improving accuracy and hardware efficiency for structured sensor data.",
        "abstract": "STEM-HD targets structured spatiotemporal data by explicitly encoding spatial and temporal relationships instead of treating all features as independent random positions. The work combines a new hyperdimensional encoding scheme with hardware-aware computation reuse, improving accuracy while reducing training time and energy for structured sensor workloads on efficient hardware.",
        "title": "Efficient Brain-Inspired Hyperdimensional Learning with Spatiotemporal Structured Data",
    },
    "Revisiting_HyperDimensional_Learning_for_FPGA_and_Low-Power_Architectures.pdf": {
        "slug": "revisiting-hdc-fpga",
        "area": "hd",
        "tags": ["FPGA", "Low-Power Systems"],
        "venue_short": "HPCA 2021",
        "summary": "This work rethinks HD learning for FPGA and low-power systems, exposing practical accelerator tradeoffs for edge-scale deployment.",
    },
    "DUAL_Acceleration_of_Clustering_Algorithms_using_Digital-based_Processing_In-Memory.pdf": {
        "slug": "dual-pim-clustering",
        "area": "systems",
        "tags": ["Clustering", "Digital PIM"],
        "venue_short": "MICRO 2020",
        "summary": "Digital processing-in-memory accelerates clustering by keeping data-intensive computation inside memory rather than paying repeated movement costs.",
    },
    "GenieHD_Efficient_DNA_Pattern_Matching_Accelerator_Using_Hyperdimensional_Computing.pdf": {
        "slug": "geniehd",
        "area": "hd",
        "tags": ["Bioinformatics", "Accelerator"],
        "venue_short": "DATE 2020",
        "summary": "A hyperdimensional accelerator makes DNA pattern matching faster and more efficient for large bioinformatics search workloads.",
        "award": "Best Paper Nomination",
        "title": "GenieHD: Efficient DNA Pattern Matching Accelerator Using Hyperdimensional Computing",
    },
}


FINE_SCOPE_CARD = {
    "area": "llm",
    "title": "FineScope: Precision Pruning for Domain-Specialized LLMs Using SAE-Guided Self-Data Cultivation",
    "authors": "Chaitali Bhattacharyya et al.",
    "lead_author": "Chaitali Bhattacharyya",
    "summary": "SAE-guided data curation makes pruning domain-aware, so compact language models keep more of the capacity that matters for specialized tasks.",
    "tags": ["LLM Pruning", "Sparse Autoencoders"],
    "venue_short": "ArXiv 2025",
    "page": "finescope.html",
}


def normalize(text):
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    normalized = normalized.lower().replace("&", " and ")
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return " ".join(normalized.split())


def parse_publications():
    raw = PUBLICATIONS_FILE.read_text(encoding="utf-8", errors="ignore")
    raw = raw[raw.index("Conference Papers") :]
    entries = []
    for match in re.finditer(r"<h2[^>]*>(.*?)</h2>\s*<ol>(.*?)</ol>", raw, flags=re.S):
        heading = html.unescape(re.sub(r"<[^>]+>", " ", match.group(1)))
        heading = " ".join(heading.split())
        if not any(ch.isdigit() for ch in heading):
            continue
        year = "".join(ch for ch in heading if ch.isdigit())
        items = re.findall(r"<li>(.*?)</li>", match.group(2), flags=re.S)
        for index, item in enumerate(items, 1):
            plain = html.unescape(re.sub(r"<[^>]+>", " ", item))
            plain = " ".join(plain.split())
            titles = re.findall(r'[“"]([^”"]+)[”"]', plain)
            title = titles[0].strip(" ,.") if titles else plain
            entries.append(
                {
                    "year": year,
                    "order": len(entries),
                    "index": index,
                    "title": title,
                    "citation": plain,
                }
            )
    return entries


def run_pdftotext(path, first_page_only=False):
    command = ["pdftotext"]
    if first_page_only:
        command.extend(["-f", "1", "-l", "1"])
    command.extend([str(path), "-"])
    return subprocess.check_output(command, text=True, encoding="utf-8", errors="ignore")


def clean_text(text):
    text = text.replace("\x0c", "\n")
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"\n+", "\n", text)
    text = text.strip()
    return text


def compact_spaces(text):
    text = clean_text(text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"^\d+\s+", "", text)
    return text.strip()


def sentence_split(text):
    text = compact_spaces(text)
    if not text:
        return []
    return [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment.strip()]


def trim_abstract(text):
    bad_markers = [
        "doi",
        "figure ",
        "copyright",
        "conference on",
        "memory (gb)",
        "published:",
        "citation in bibtex",
        "open access support",
        "authors' contact information",
    ]
    filtered = []
    for sentence in sentence_split(text):
        lowered = sentence.lower()
        if any(marker in lowered for marker in bad_markers):
            continue
        if len(sentence.split()) < 8:
            continue
        filtered.append(sentence)
    if not filtered:
        return compact_spaces(text)
    return " ".join(filtered[:5])


def extract_abstract(text):
    raw = clean_text(text)
    stop_patterns = [
        r"\n\s*(?:I\.|1\.?|1)\s*Introduction\b",
        r"\n\s*Introduction\b",
        r"\n\s*Keywords\b",
        r"\n\s*CCS Concepts\b",
        r"\n\s*Index Terms\b",
        r"\n\s*ACM Reference Format\b",
        r"\n\s*Authors[’'] Contact Information",
        r"\n\s*This work was supported",
    ]

    abstract_match = re.search(r"\b(?:Abstract|ABSTRACT)\s*[-:—]?\s*", raw)
    if abstract_match:
        tail = raw[abstract_match.end() :]
        end = len(tail)
        for pattern in stop_patterns:
            stop_match = re.search(pattern, tail, flags=re.I)
            if stop_match:
                end = min(end, stop_match.start())
        candidate = compact_spaces(tail[:end])
        if len(candidate.split()) >= 25:
            return candidate

    fallback = raw
    for pattern in stop_patterns:
        stop_match = re.search(pattern, fallback, flags=re.I)
        if stop_match:
            fallback = fallback[: stop_match.start()]
            break

    paragraphs = [
        compact_spaces(block)
        for block in re.split(r"\n\s*\n+", fallback)
        if len(compact_spaces(block).split()) >= 25
    ]
    paragraphs = [
        paragraph
        for paragraph in paragraphs
        if "doi.org" not in paragraph.lower()
        and "conference sponsors" not in paragraph.lower()
        and "citation in bibtex" not in paragraph.lower()
        and "published:" not in paragraph.lower()
        and "open access support" not in paragraph.lower()
    ]
    if not paragraphs:
        return ""

    def paragraph_score(paragraph):
        words = paragraph.split()
        penalty = 0
        if any(token.isupper() and len(token) > 3 for token in words[:12]):
            penalty += 40
        return len(words) - penalty

    paragraphs.sort(key=paragraph_score, reverse=True)
    return paragraphs[0]


def title_tokens(title):
    return set(normalize(title).split())


def choose_entry(pdf_name, override, entries, first_page_text):
    preferred_year = override.get("preferred_year")
    year_hints = set(re.findall(r"20\d{2}", first_page_text))
    pdf_tokens = title_tokens(Path(pdf_name).stem)

    best = None
    best_score = (-1, -1, -1, -999)
    for entry in entries:
        if preferred_year and entry["year"] != preferred_year:
            continue
        overlap = len(pdf_tokens & title_tokens(entry["title"]))
        ratio = int(1000 * overlap / max(len(title_tokens(entry["title"])), 1))
        year_match = 1 if entry["year"] in year_hints else 0
        score = (year_match, overlap, ratio, -entry["order"])
        if score > best_score:
            best_score = score
            best = entry
    return best


def split_authors_and_venue(citation, title):
    title_pattern = re.escape(title)
    parts = re.split(title_pattern, citation, maxsplit=1, flags=re.I)
    if len(parts) == 2:
        authors = parts[0]
        venue = parts[1]
    else:
        authors = citation
        venue = ""
    authors = authors.replace("“", "").replace('"', "").strip(" ,.")
    venue = venue.replace("”", "").replace('"', "").strip(" ,.")
    return authors, venue


def lead_author(authors):
    authors = authors.replace(" and ", ", ")
    return authors.split(",")[0].strip()


def build_contributions(summary, abstract, area_key):
    sentences = []
    for sentence in sentence_split(abstract):
        lowered = sentence.lower()
        if "authors contact information" in lowered or "copyright" in lowered:
            continue
        if sentence not in sentences:
            sentences.append(sentence)
    if len(sentences) >= 3:
        bullets = [sentences[0], sentences[1], sentences[-1]]
    else:
        bullets = sentences[:3]
    if not bullets:
        bullets.append(summary)
    while len(bullets) < 3:
        if len(bullets) == 1:
            bullets.append(AREA_META[area_key]["context"])
        else:
            bullets.append("The project combines algorithm design with efficiency-aware deployment choices that matter in practical systems.")
    labels = ["Core Idea", "Design Move", "Practical Impact"]
    return list(zip(labels, bullets[:3]))


def build_context(area_key, tags):
    focus = ", ".join(tags[:-1]) + (" and " + tags[-1] if len(tags) > 1 else tags[0])
    return f"{AREA_META[area_key]['context']} The page highlights the paper through the lens of {focus}."


def render_page(project):
    contributions_html = "\n".join(
        f"""      <div class="contribution-card reveal">
        <h3>{html.escape(label)}</h3>
        <p>{html.escape(text)}</p>
      </div>"""
        for label, text in project["contributions"]
    )

    snapshot_html = f"""      <div class="snapshot-card reveal">
        <div class="snapshot-label">Research Thread</div>
        <div class="snapshot-value">{html.escape(AREA_META[project["area"]]["label"])}</div>
      </div>
      <div class="snapshot-card reveal">
        <div class="snapshot-label">Venue</div>
        <div class="snapshot-value">{html.escape(project["venue_short"])}</div>
      </div>
      <div class="snapshot-card reveal">
        <div class="snapshot-label">Selected Focus</div>
        <div class="snapshot-value">{html.escape(", ".join(project["tags"]))}</div>
      </div>"""

    citation_text = project["citation"]
    title = html.escape(project["title"])
    summary = html.escape(project["summary"])
    authors = html.escape(project["authors"])
    abstract = html.escape(project["abstract"])
    venue = html.escape(project["venue_short"])
    context = html.escape(project["context"])
    award_html = (
        f'<div class="hero-meta"><strong>Note</strong> {html.escape(project["award"])}</div>'
        if project.get("award")
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | CELL Project Page</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="project-style.css">
</head>
<body data-area="{project["area"]}">
<button class="theme-btn" id="themeBtn"><span id="themeLabel">Light</span></button>

<section class="hero">
  <div class="hero-inner">
    <div class="hero-label">CELL Project Page · {venue}</div>
    <h1 class="hero-title">{title}</h1>
    <p class="hero-subtitle">{summary}</p>
    <div class="hero-meta"><strong>Authors</strong> {authors}</div>
    {award_html}
    <div class="button-row">
      <a class="btn btn-primary" href="../projectpage.html#project-pages">Back to Project Pages</a>
      <a class="btn btn-secondary" href="#abstract">Read Abstract</a>
      <a class="btn btn-secondary" href="#citation">Cite</a>
    </div>
  </div>
</section>

<nav>
  <a class="nav-link active" href="#abstract">Abstract</a>
  <a class="nav-link" href="#snapshot">Snapshot</a>
  <a class="nav-link" href="#contributions">Contributions</a>
  <a class="nav-link" href="#citation">Citation</a>
</nav>

<section id="abstract">
  <div class="section-kicker">Abstract</div>
  <h2 class="section-title">What the paper is doing.</h2>
  <div class="abstract-box reveal">
    <p>{abstract}</p>
  </div>
</section>

<hr class="divider">

<section id="snapshot">
  <div class="section-kicker">Snapshot</div>
  <h2 class="section-title">How this project fits inside CELL.</h2>
  <p class="section-intro">{html.escape(project["summary"])}</p>
  <div class="snapshot-grid">
{snapshot_html}
  </div>
  <div class="context-box reveal">
    <h3>Why it matters</h3>
    <p>{context}</p>
  </div>
</section>

<hr class="divider">

<section id="contributions">
  <div class="section-kicker">Contributions</div>
  <h2 class="section-title">Three takeaways from the work.</h2>
  <div class="contributions-grid">
{contributions_html}
  </div>
</section>

<hr class="divider">

<section id="citation">
  <div class="section-kicker">Citation</div>
  <h2 class="section-title">Reference entry.</h2>
  <div class="citation-box reveal">
    <button class="copy-btn" data-copy-target="citation-text">Copy</button>
    <p class="citation-text" id="citation-text">{html.escape(citation_text)}</p>
  </div>
</section>

<footer>
  <p><a href="../projectpage.html#project-pages">Project Pages</a> · <a href="https://cell.postech.ac.kr" target="_blank">CELL Lab @ POSTECH</a></p>
</footer>

<script src="project.js"></script>
</body>
</html>
"""


def render_data_js(cards):
    return "window.CELL_PROJECTS = " + json.dumps(cards, indent=2, ensure_ascii=False) + ";\n"


def build_projects():
    entries = parse_publications()
    projects = []

    for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
        override = OVERRIDES.get(pdf_path.name)
        if not override:
            continue

        first_page_text = run_pdftotext(pdf_path, first_page_only=True)
        entry = choose_entry(pdf_path.name, override, entries, first_page_text)
        if not entry:
            raise RuntimeError(f"Could not match publication entry for {pdf_path.name}")

        title = override.get("title", entry["title"])
        citation = override.get("citation", entry["citation"])
        authors, venue_full = split_authors_and_venue(citation, title)
        authors = override.get("authors", authors)
        venue_full = override.get("venue_full", venue_full or entry["year"])

        pdf_text = run_pdftotext(pdf_path)
        abstract = override.get("abstract", extract_abstract(pdf_text))
        if not abstract:
            abstract = override["summary"]
        abstract = trim_abstract(abstract)

        project = {
            "slug": override["slug"],
            "area": override["area"],
            "tags": override["tags"],
            "venue_short": override["venue_short"],
            "venue_full": venue_full,
            "summary": override["summary"],
            "title": title,
            "authors": authors,
            "lead_author": lead_author(authors),
            "abstract": compact_spaces(abstract),
            "citation": citation,
            "year": entry["year"],
            "order": entry["order"],
            "award": override.get("award"),
        }
        project["context"] = build_context(project["area"], project["tags"])
        project["contributions"] = build_contributions(project["summary"], project["abstract"], project["area"])
        projects.append(project)

    projects.sort(key=lambda item: item["order"])
    return projects


def write_outputs(projects):
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

    for project in projects:
        page_path = PROJECTS_DIR / f"{project['slug']}.html"
        page_path.write_text(render_page(project), encoding="utf-8")

    cards = [FINE_SCOPE_CARD]
    for project in projects:
        cards.append(
            {
                "area": project["area"],
                "title": project["title"],
                "authors": project["authors"],
                "leadAuthor": project["lead_author"],
                "summary": project["summary"],
                "tags": project["tags"],
                "venue_short": project["venue_short"],
                "page": f"projects/{project['slug']}.html",
                "award": project.get("award"),
            }
        )

    DATA_JS.write_text(render_data_js(cards), encoding="utf-8")


def main():
    projects = build_projects()
    write_outputs(projects)
    print(f"Generated {len(projects)} project pages and {DATA_JS.name}.")


if __name__ == "__main__":
    main()
