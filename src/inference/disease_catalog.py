"""
Agricultural Knowledge Base and Disease Catalog.
Provides rich diagnostic details, symptoms, severity metrics, and
treatment recommendations (organic & chemical) for all 38 PlantVillage classes.
"""

from typing import Any, Dict, Optional
from src.constants import parse_class_name


DISEASE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "Apple___Apple_scab": {
        "disease_name": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "severity": "Moderate",
        "description": "A serious fungal disease affecting Malus species that attacks leaves, fruit, and twigs, causing premature defoliation and scarred fruit.",
        "symptoms": [
            "Olive-green to black velvety spots on upper leaf surfaces",
            "Yellowing around leaf spots leading to leaf drop",
            "Corky, scabby brown lesions on fruit"
        ],
        "organic_treatment": [
            "Apply liquid copper or sulfur sprays during early green tip stage",
            "Spray bio-fungicides containing Bacillus subtilis or neem extract",
            "Rake and destroy fallen leaves in autumn to eliminate overwintering spores"
        ],
        "chemical_treatment": [
            "Captan or Mancozeb applied preventively before rain events",
            "Myclobutanil or Difenoconazole for systemic curative action within 48 hours of infection"
        ],
        "prevention": [
            "Plant scab-resistant cultivars (e.g., Enterprise, Liberty, Freedom)",
            "Prune trees annually to enhance air circulation and speed leaf drying",
            "Avoid overhead irrigation"
        ]
    },
    "Apple___Black_rot": {
        "disease_name": "Black Rot (Frogeye Leaf Spot)",
        "scientific_name": "Botryosphaeria obtusa",
        "severity": "High",
        "description": "A devastating fungal disease that causes leaf spots, cankers on branches, and black mummified rot on fruit.",
        "symptoms": [
            "Small purple specks enlarging into 'frogeye' leaf spots with tan centers and purple margins",
            "Rotting fruit turning dark brown and eventually jet black, shriveling into hard mummies",
            "Sunken reddish-brown cankers on bark"
        ],
        "organic_treatment": [
            "Prune out dead wood, fire blight strikes, and cankers during dormancy",
            "Remove and burn all mummified fruits left hanging on branches",
            "Apply copper-based fungicides at bud break"
        ],
        "chemical_treatment": [
            "Captan, Thiophanate-methyl, or Fludioxonil applied from petal fall through harvest"
        ],
        "prevention": [
            "Maintain overall tree vigor with balanced fertilization",
            "Disinfect pruning shears between cuts with 70% alcohol",
            "Minimize mechanical damage to bark and fruit"
        ]
    },
    "Apple___Cedar_apple_rust": {
        "disease_name": "Cedar Apple Rust",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "severity": "Moderate",
        "description": "A heteroecious fungal disease requiring both apple trees and Eastern red cedar (juniper) to complete its lifecycle.",
        "symptoms": [
            "Bright yellow-orange or reddish spots on upper leaf surfaces in spring",
            "Small tube-like projections (aecia) protruding from the underside of leaves",
            "Early leaf yellowing and defoliation on susceptible varieties"
        ],
        "organic_treatment": [
            "Apply wettable sulfur sprays every 7-10 days starting from tight cluster through petal fall",
            "Remove nearby cedar gall hosts within a 1-mile radius if feasible"
        ],
        "chemical_treatment": [
            "Sterol-inhibiting fungicides (Myclobutanil, Fenbuconazole)",
            "Protective fungicides like Mancozeb"
        ],
        "prevention": [
            "Plant resistant apple varieties (e.g., Redfree, Pristine, William's Pride)",
            "Inspect nearby juniper trees and prune gelatinous orange galls in winter"
        ]
    },
    "Apple___healthy": {
        "disease_name": "Healthy Apple Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "The leaf shows vigorous chlorophyll distribution, healthy vascular structure, and no signs of fungal or bacterial lesions.",
        "symptoms": ["Normal vibrant green coloration, crisp margins, no spotting or discoloration."],
        "organic_treatment": ["No treatment required. Maintain regular watering and organic compost mulching."],
        "chemical_treatment": ["None required."],
        "prevention": ["Continue regular scouting, pest monitoring, and seasonal sanitation."]
    },
    "Blueberry___healthy": {
        "disease_name": "Healthy Blueberry Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Vigorous foliage with balanced soil pH (4.5 - 5.5) and no visible pathogens.",
        "symptoms": ["Smooth, deep green leaves with intact cuticle and zero chlorosis."],
        "organic_treatment": ["None required. Maintain acidic pine bark mulch."],
        "chemical_treatment": ["None required."],
        "prevention": ["Maintain acidic soil conditions and avoid waterlogged roots."]
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "disease_name": "Cherry Powdery Mildew",
        "scientific_name": "Podosphaera clandestina",
        "severity": "Moderate",
        "description": "A common fungal disease causing white powdery mycelial growth on young leaves, green shoots, and developing cherries.",
        "symptoms": [
            "White circular powdery patches on young expanding leaves",
            "Leaves becoming curled, distorted, or cupped upward",
            "Premature defoliation and poor fruit development"
        ],
        "organic_treatment": [
            "Spray potassium bicarbonate (e.g., MilStop) or dilute horticultural oils (1-2%)",
            "Apply sulfur-based fungicides preventively",
            "Neem oil spray early in the morning"
        ],
        "chemical_treatment": [
            "Quinoxyfen, Boscalid, or Pyraclostrobin alternating with DMI fungicides"
        ],
        "prevention": [
            "Prune dense canopies to promote maximum sunlight and airflow",
            "Avoid excessive nitrogen fertilization which produces susceptible tender tissue"
        ]
    },
    "Cherry_(including_sour)___healthy": {
        "disease_name": "Healthy Cherry Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Pest-free foliage exhibiting robust health and normal pigmentation.",
        "symptoms": ["Clear dark green foliage without spots or powdery coats."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Prune annually and inspect for shot-hole or mildew signs."]
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "disease_name": "Corn Gray Leaf Spot",
        "scientific_name": "Cercospora zeae-maydis",
        "severity": "High",
        "description": "One of the most destructive corn foliar diseases, thriving in warm humid climates and causing significant yield losses.",
        "symptoms": [
            "Small necrotic spots with halos that expand into long, rectangular grayish lesions bordered by leaf veins",
            "Lesions coalescing to blight entire leaves",
            "Stalk lodging due to premature leaf death"
        ],
        "organic_treatment": [
            "Plow under infected crop residue to accelerate fungal decomposition",
            "Apply copper hydroxide or Trichoderma harzianum bio-fungicides"
        ],
        "chemical_treatment": [
            "Strobilurin fungicides (Azoxystrobin) mixed with Triazoles (Propiconazole) applied at VT/R1 stage"
        ],
        "prevention": [
            "Plant gray leaf spot resistant corn hybrids",
            "Practice 2-year crop rotation with non-host crops like soybeans",
            "Manage residue with clean tilling where erosion permits"
        ]
    },
    "Corn_(maize)___Common_rust_": {
        "disease_name": "Corn Common Rust",
        "scientific_name": "Puccinia sorghi",
        "severity": "Moderate",
        "description": "Airborne rust fungus blown north annually, forming powdery brick-red pustules on leaves.",
        "symptoms": [
            "Small cinnamon-brown to reddish-brown oval pustules on both leaf surfaces",
            "Pustules rupture epidermal tissue releasing powdery spores",
            "Leaf tissue yellowing and drying out under severe pressure"
        ],
        "organic_treatment": [
            "Apply sulfur dust or bio-fungicides at early onset",
            "Ensure balanced potassium nutrition to enhance cell wall resistance"
        ],
        "chemical_treatment": [
            "Pyraclostrobin + Metconazole or Azoxystrobin applied when pustules first appear on lower canopy"
        ],
        "prevention": [
            "Utilize rust-resistant or tolerant hybrids (with Rp genes)",
            "Early planting to avoid high late-season spore counts"
        ]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "disease_name": "Northern Corn Leaf Blight",
        "scientific_name": "Setosphaeria turcica",
        "severity": "High",
        "description": "Severe foliar disease causing large cigar-shaped lesions, leading to extensive loss of photosynthetic area.",
        "symptoms": [
            "Long, elliptical, grayish-green or tan lesions (1-6 inches long)",
            "Lesions turning dark with olive-black fungal sporulation in damp weather",
            "Lower canopy leaves drying up resembling frost damage"
        ],
        "organic_treatment": [
            "Apply Bacillus pumilus or copper-based sprays early in the season",
            "Incorporate residue post-harvest"
        ],
        "chemical_treatment": [
            "Fungicides containing Pyraclostrobin, Trifloxystrobin, or Prothioconazole applied at tasseling"
        ],
        "prevention": [
            "Select hybrids with single-gene (Ht) or multigenic resistance",
            "Rotate crops annually with non-grass crops"
        ]
    },
    "Corn_(maize)___healthy": {
        "disease_name": "Healthy Corn Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Healthy maize foliage with uniform green pigmentation and strong vascular lines.",
        "symptoms": ["Long, uniform green leaves without streaks or pustules."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Maintain weed management and balanced N-P-K soil nutrition."]
    },
    "Grape___Black_rot": {
        "disease_name": "Grape Black Rot",
        "scientific_name": "Guignardia bidwellii",
        "severity": "High",
        "description": "Destructive vineyard fungal disease that attacks leaves, shoots, and turns ripening berries into shriveled hard black mummies.",
        "symptoms": [
            "Circular reddish-brown spots with dark borders and tiny black fruiting bodies (pycnidia)",
            "Young green shoots showing elongated black cankers",
            "Berries rotting, collapsing, and turning into hard black mummies"
        ],
        "organic_treatment": [
            "Prune and destroy infected cane mummies before bud break",
            "Apply copper soap and liquid lime sulfur early in the season"
        ],
        "chemical_treatment": [
            "Mancozeb, Ziram, or Tebuconazole applied from 1-inch shoot growth through 4 weeks post-bloom"
        ],
        "prevention": [
            "Canopy management (trellising, shoot positioning) to ensure rapid drying after rain",
            "Plant resistant cultivars"
        ]
    },
    "Grape___Esca_(Black_Measles)": {
        "disease_name": "Grape Esca (Black Measles)",
        "scientific_name": "Phaeomoniella chlamydospora & Fomitiporia mediterranea",
        "severity": "Critical",
        "description": "A complex vascular grapevine trunk disease that causes tiger-stripe leaf patterns and measles-like dark spots on berries.",
        "symptoms": [
            "'Tiger-striped' leaves with interveinal yellow and necrotic brown regions",
            "Dark purple or black speckles on berries ('measles')",
            "Sudden vine apoplexy (wilting and collapse in midsummer heat)"
        ],
        "organic_treatment": [
            "Apply Trichoderma-based wound protectants to pruning wounds immediately",
            "Remove dead vines and burn infected wood"
        ],
        "chemical_treatment": [
            "Paints or pastes containing Thiophanate-methyl on large pruning wounds"
        ],
        "prevention": [
            "Delay pruning until late winter when wound healing is rapid",
            "Sanitize pruning shears between vines"
        ]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "disease_name": "Grape Leaf Blight (Pseudocercospora / Isariopsis)",
        "scientific_name": "Pseudocercospora vitis",
        "severity": "Moderate",
        "description": "Foliar disease prevalent in late season under humid climates, causing premature senescence.",
        "symptoms": [
            "Irregular brown spots with dark purplish or black borders on mature leaves",
            "Yellow halo surrounding necrotic spots",
            "Leaf blight and early defoliation weakening vines for winter"
        ],
        "organic_treatment": [
            "Bordeaux mixture or copper hydroxide sprays post-bloom",
            "Sanitize vineyard floor by composting fallen leaves"
        ],
        "chemical_treatment": [
            "Chlorothalonil, Folpet, or Strobilurin sprays applied after bloom"
        ],
        "prevention": [
            "Ensure proper vine spacing and open canopy training",
            "Avoid excess nitrogen fertilization"
        ]
    },
    "Grape___healthy": {
        "disease_name": "Healthy Grape Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Vibrant, broad green vitis leaves without spots or fungal patinas.",
        "symptoms": ["Clear broad green leaves with intact serrated borders."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Standard seasonal canopy management and disease scouting."]
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "disease_name": "Citrus Greening (Huanglongbing - HLB)",
        "scientific_name": "Candidatus Liberibacter asiaticus",
        "severity": "Critical",
        "description": "Incurable, highly devastating bacterial disease vectored by the Asian citrus psyllid (Diaphorina citri).",
        "symptoms": [
            "Asymmetrical blotchy mottle leaf chlorosis crossing leaf veins",
            "Yellow shoots and leaf veins turning thick, corky, and raised",
            "Small, lopsided fruit that stays green at the bottom with bitter taste"
        ],
        "organic_treatment": [
            "Release parasitoid wasps (Tamarixia radiata) for biological psyllid control",
            "Apply foliar nutritional sprays (micronutrients: Zinc, Manganese, Boron) to sustain tree health",
            "Immediately remove and burn confirmed infected trees"
        ],
        "chemical_treatment": [
            "Insecticides targeting Asian citrus psyllid: Imidacloprid, Thiamethoxam, or Fenpropathrin",
            "Oxytetracycline trunk injections where permitted by regulatory bodies"
        ],
        "prevention": [
            "Use only certified disease-free nursery stock",
            "Aggressive psyllid monitoring with yellow sticky cards",
            "Strict quarantine enforcement"
        ]
    },
    "Peach___Bacterial_spot": {
        "disease_name": "Peach Bacterial Spot",
        "scientific_name": "Xanthomonas arboricola pv. pruni",
        "severity": "High",
        "description": "Bacterial infection causing angular leaf shot-holes, fruit pitting, and twig cankers under warm wet conditions.",
        "symptoms": [
            "Small angular, purple-brown water-soaked spots on leaves",
            "Centers of leaf spots drop out creating a 'shot-hole' appearance",
            "Deep, cracked pits and gummy exudates on fruit"
        ],
        "organic_treatment": [
            "Dormant copper sprays at late leaf fall and early bud break",
            "Bio-pesticides containing Bacillus amyloliquefaciens"
        ],
        "chemical_treatment": [
            "Oxytetracycline (Mycoshield) applied from petal fall through shuck split",
            "Low-rate copper compounds combined with mancozeb"
        ],
        "prevention": [
            "Select resistant cultivars (e.g., Candor, Biscoe, Harrow Diamond)",
            "Avoid overhead sprinkler irrigation",
            "Maintain windbreaks to reduce sand-blasting of leaf cuticles"
        ]
    },
    "Peach___healthy": {
        "disease_name": "Healthy Peach Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Glossy lanceolate leaves showing uniform green color with no lesions.",
        "symptoms": ["Slender, smooth lanceolate green foliage."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Routine winter pruning and dormant copper applications."]
    },
    "Pepper,_bell___Bacterial_spot": {
        "disease_name": "Pepper Bacterial Spot",
        "scientific_name": "Xanthomonas euvesicatoria",
        "severity": "High",
        "description": "Major bacterial disease causing defoliation, sunscald on exposed peppers, and unmarketable fruit.",
        "symptoms": [
            "Small, circular or irregular dark water-soaked leaf spots",
            "Spots turn brown with greasy appearance and slight yellow halo",
            "Severe leaf drop exposing fruit to sunburn"
        ],
        "organic_treatment": [
            "Fixed copper sprays mixed with Bacillus subtilis",
            "Hot water seed treatment (50°C for 25 minutes) before planting",
            "Destroy diseased plant residues after harvest"
        ],
        "chemical_treatment": [
            "Copper bactericides tank-mixed with Mancozeb (improves copper solubility)",
            "Actigard (Acibenzolar-S-methyl) for systemic acquired resistance"
        ],
        "prevention": [
            "Use certified pathogen-free seeds and resistant varieties",
            "Employ drip irrigation instead of overhead sprinklers",
            "Avoid working in fields when foliage is wet"
        ]
    },
    "Pepper,_bell___healthy": {
        "disease_name": "Healthy Bell Pepper Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Healthy capsicum foliage with rich green color and robust vigor.",
        "symptoms": ["Crisp, broad green leaves with no bacterial spots."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Maintain weed-free beds and balanced irrigation."]
    },
    "Potato___Early_blight": {
        "disease_name": "Potato Early Blight",
        "scientific_name": "Alternaria solani",
        "severity": "Moderate",
        "description": "Fungal disease characterized by 'target-board' concentric ring spots, typically starting on older lower foliage.",
        "symptoms": [
            "Small dark brown to black spots with concentric rings resembling a target board",
            "Yellow halo surrounding lesions on mature leaves",
            "Premature death of lower canopy vines"
        ],
        "organic_treatment": [
            "Apply copper soaps or Bordeaux mixture at 7-10 day intervals",
            "Bio-fungicides like Serenade (Bacillus subtilis)"
        ],
        "chemical_treatment": [
            "Chlorothalonil, Azoxystrobin, or Difenoconazole applied protectively"
        ],
        "prevention": [
            "Ensure 3-year crop rotation out of solanaceous crops",
            "Avoid overhead irrigation and irrigate early in the day",
            "Maintain optimal plant nutrition (nitrogen-deficient plants are more susceptible)"
        ]
    },
    "Potato___Late_blight": {
        "disease_name": "Potato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "severity": "Critical",
        "description": "The notorious water mold pathogen that caused the Irish Potato Famine; rapidly destroys foliage and rots tubers.",
        "symptoms": [
            "Water-soaked dark lesions spreading rapidly across leaves and stems",
            "White fuzzy mildew growth on undersides of leaves during high humidity",
            "Vines rapidly collapsing into brown-black slime with a distinctive pungent odor",
            "Dry, granular copper-brown rot inside tubers"
        ],
        "organic_treatment": [
            "Copper hydroxide or copper sulfate sprays applied before infection",
            "Immediately destroy infected foliage (vine kill) to protect tubers"
        ],
        "chemical_treatment": [
            "Cymoxanil, Mandipropamid, Dimethomorph, or Fluopicolide applied protectively",
            "Metalaxyl-M (where resistance has not developed)"
        ],
        "prevention": [
            "Plant only certified disease-free seed tubers",
            "Eliminate cull piles and volunteer potato plants",
            "Monitor weather disease forecasting models (e.g. Blitecast)"
        ]
    },
    "Potato___healthy": {
        "disease_name": "Healthy Potato Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Vigorous potato foliage with intact composite leaves and strong stem growth.",
        "symptoms": ["Vibrant green compound leaves without necrotic target spots."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Regular scouting and hill soil properly around developing tubers."]
    },
    "Raspberry___healthy": {
        "disease_name": "Healthy Raspberry Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Vigorous cane and leaf tissue without rust or cane blight lesions.",
        "symptoms": ["Bright green pinnate leaves with healthy white undersides."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Prune spent canes annually and trellis for maximum light."]
    },
    "Soybean___healthy": {
        "disease_name": "Healthy Soybean Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Healthy trifoliate leaves exhibiting normal green pigmentation and active nodulation.",
        "symptoms": ["Uniform green trifoliate leaves without rust, mildew or mosaic mottling."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Maintain weed management and standard scouting."]
    },
    "Squash___Powdery_mildew": {
        "disease_name": "Squash Powdery Mildew",
        "scientific_name": "Podosphaera xanthii",
        "severity": "Moderate",
        "description": "Airborne fungal disease covering cucurbit leaves with talcum powder-like fungal spores.",
        "symptoms": [
            "White, talcum-like powdery spots on both leaf surfaces and petioles",
            "Infected leaves turning yellow, then brown and papery",
            "Fruit exposed to sunburn due to lost foliage cover"
        ],
        "organic_treatment": [
            "Spray with 40% milk and 60% water solution in direct sunlight",
            "Potassium bicarbonate (MilStop) or horticultural neem oil spray",
            "Sulfur sprays applied preventively"
        ],
        "chemical_treatment": [
            "Myclobutanil, Quinoxyfen, or Triflumizole"
        ],
        "prevention": [
            "Plant resistant squash varieties",
            "Space plants generously to promote airflow",
            "Water roots directly using drip irrigation"
        ]
    },
    "Strawberry___Leaf_scorch": {
        "disease_name": "Strawberry Leaf Scorch",
        "scientific_name": "Diplocarpon earlianum",
        "severity": "Moderate",
        "description": "Fungal foliar disease causing numerous purple blotches that coalesce into scorch-like necrosis.",
        "symptoms": [
            "Small, irregular dark purple spots on upper leaf surfaces without light centers",
            "Spots enlarge and merge, making entire leaf appear burned/scorched",
            "Leaf margins curling upward and drying up"
        ],
        "organic_treatment": [
            "Remove and destroy infected older foliage after harvest renovation",
            "Apply copper soaps early in spring as new growth emerges"
        ],
        "chemical_treatment": [
            "Captan, Thiophanate-methyl, or Pyraclostrobin"
        ],
        "prevention": [
            "Plant on raised beds with straw mulch to prevent soil splashing",
            "Use drip tape rather than overhead sprinkler irrigation",
            "Renovate strawberry beds promptly after harvest"
        ]
    },
    "Strawberry___healthy": {
        "disease_name": "Healthy Strawberry Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Lush trifoliate strawberry leaves showing vigorous runnering and crown health.",
        "symptoms": ["Deep green trifoliate leaves with clean serrated margins."],
        "organic_treatment": ["None required."],
        "chemical_treatment": ["None required."],
        "prevention": ["Keep fruit elevated with pine needles or clean straw mulch."]
    },
    "Tomato___Bacterial_spot": {
        "disease_name": "Tomato Bacterial Spot",
        "scientific_name": "Xanthomonas vesicatoria",
        "severity": "High",
        "description": "Devastating bacterial disease in warm, wet climates attacking foliage, stems, and fruit.",
        "symptoms": [
            "Small, dark brown to black circular spots with greasy or water-soaked borders",
            "Spots on fruit begin as slightly raised blisters and turn dark brown and scabby",
            "Extensive leaf yellowing and blighting"
        ],
        "organic_treatment": [
            "Fixed copper sprays combined with Bacillus subtilis",
            "Soak seeds in 1.3% sodium hypochlorite or hot water (50°C for 25 min) prior to sowing"
        ],
        "chemical_treatment": [
            "Copper hydroxide mixed with Mancozeb",
            "Acibenzolar-S-methyl (Actigard) to activate plant defenses"
        ],
        "prevention": [
            "Use certified disease-free seeds and transplants",
            "Avoid handling plants when leaves are wet",
            "Rotate out of solanaceous crops for at least 2 years"
        ]
    },
    "Tomato___Early_blight": {
        "disease_name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "severity": "Moderate",
        "description": "Extremely prevalent fungus that creates characteristic concentric ring target spots on older foliage.",
        "symptoms": [
            "Brown-to-black spots with distinct concentric rings (target pattern)",
            "Yellowing of surrounding leaf tissue (chlorosis)",
            "Stem collar rot at ground level in seedlings"
        ],
        "organic_treatment": [
            "Prune bottom 12-18 inches of leaves to prevent soil splashing",
            "Apply copper-based fungicides or bio-fungicide Serenade",
            "Thoroughly mulch ground with straw or plastic film"
        ],
        "chemical_treatment": [
            "Chlorothalonil, Mancozeb, or Azoxystrobin applied every 7-10 days"
        ],
        "prevention": [
            "Stake and cage tomato plants to maximize airflow",
            "Water with drip irrigation at the base of plants",
            "Practice 3-year crop rotation"
        ]
    },
    "Tomato___Late_blight": {
        "disease_name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "severity": "Critical",
        "description": "Rapidly lethal oomycete pathogen capable of killing healthy tomato plants within days during cool, humid conditions.",
        "symptoms": [
            "Pale green to dark water-soaked greasy patches rapidly expanding on leaves",
            "White frosty fungal-like sporulation on the underside of leaves in high moisture",
            "Stems develop dark brown to black greasy lesions",
            "Firm, leathery, dark brown rot on green fruit"
        ],
        "organic_treatment": [
            "Preventive applications of copper fungicides before rainfall events",
            "Remove and bag heavily infected vines immediately—do not compost"
        ],
        "chemical_treatment": [
            "Chlorothalonil protectively; Curative fungicides: Mandipropamid, Dimethomorph, Cymoxanil"
        ],
        "prevention": [
            "Plant resistant hybrids (e.g., Mountain Magic, Defiant PhR, Iron Lady)",
            "Avoid overhead watering and ensure wide plant spacing",
            "Destroy volunteer tomato and potato plants near the garden"
        ]
    },
    "Tomato___Leaf_Mold": {
        "disease_name": "Tomato Leaf Mold",
        "scientific_name": "Passalora fulva",
        "severity": "Moderate",
        "description": "Fungal disease common in greenhouse and high-tunnel tomatoes with high humidity (>85%).",
        "symptoms": [
            "Pale green to yellowish indistinct spots on the upper leaf surface",
            "Olive-green to velvety brown mold growth on the corresponding lower surface",
            "Leaves turn yellow, curl, wither, and drop prematurely"
        ],
        "organic_treatment": [
            "Significantly increase ventilation and exhaust fan speed in greenhouses",
            "Apply copper soaps or potassium bicarbonate",
            "Prune lower foliage to open the canopy"
        ],
        "chemical_treatment": [
            "Chlorothalonil, Cyazofamid, or Boscalid"
        ],
        "prevention": [
            "Maintain greenhouse relative humidity below 80%",
            "Grow resistant tomato cultivars with Cf resistance genes",
            "Space plants adequately to prevent dense foliage crowding"
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "disease_name": "Tomato Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "severity": "Moderate",
        "description": "Common foliar fungal disease that causes severe lower leaf loss, exposing tomatoes to sunscald.",
        "symptoms": [
            "Numerous small (1/8 inch), circular spots with gray or white centers and dark brown margins",
            "Tiny black specks (pycnidia) visible inside the gray centers with a hand lens",
            "Lower leaves turn yellow, wither, and drop in rapid succession"
        ],
        "organic_treatment": [
            "Pick off and dispose of the lowest infected leaves as soon as spots appear",
            "Mulch heavily around the plant stem to prevent spores splashing from soil",
            "Apply liquid copper fungicide"
        ],
        "chemical_treatment": [
            "Chlorothalonil, Mancozeb, or Pyraclostrobin applied on a 7-day schedule"
        ],
        "prevention": [
            "Keep foliage dry with drip irrigation",
            "Allow 3 feet between plants for rapid evaporation",
            "Cleanly dispose of all nightshade crop debris at the end of the season"
        ]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "disease_name": "Tomato Two-Spotted Spider Mite",
        "scientific_name": "Tetranychus urticae",
        "severity": "High",
        "description": "Microscopic arachnid pests that pierce leaf cells in hot, dry conditions, causing stippling and webbing.",
        "symptoms": [
            "Fine pale yellow or bronze stippling (tiny dots) on the upper surface of leaves",
            "Fine silken webbing on undersides of leaves and leaf axils",
            "Leaves dry out, turn bronze or brown, and drop off"
        ],
        "organic_treatment": [
            "Release predatory mites (Phytoseiulus persimilis or Neoseiulus californicus)",
            "Spray insecticidal soap or neem oil thoroughly covering leaf undersides",
            "Blast undersides of leaves with a firm spray of water to knock down populations"
        ],
        "chemical_treatment": [
            "Miticide sprays: Bifenazate, Spiromesifen, or Abamectin (alternate classes to prevent resistance)"
        ],
        "prevention": [
            "Avoid excessive nitrogen fertilization",
            "Keep garden rows weed-free and mitigate dust along pathways",
            "Scout leaf undersides regularly during hot, dry spells"
        ]
    },
    "Tomato___Target_Spot": {
        "disease_name": "Tomato Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "severity": "Moderate",
        "description": "Fungal disease creating concentric target-like brown spots on leaves, stems, and sunken craters on fruit.",
        "symptoms": [
            "Small water-soaked pinpoint spots that expand into brown lesions with light brown centers and dark concentric rings",
            "Deep, crater-like brown lesions on green and ripe tomato fruit",
            "Progressive defoliation from bottom upward"
        ],
        "organic_treatment": [
            "Apply copper fungicides early in the morning",
            "Remove lower infected leaves to improve airflow",
            "Bio-fungicide treatments with Bacillus subtilis"
        ],
        "chemical_treatment": [
            "Fluopyram, Azoxystrobin + Difenoconazole, or Chlorothalonil"
        ],
        "prevention": [
            "Avoid overhead irrigation",
            "Stake and prune plants for enhanced canopy ventilation",
            "Rotate crops with non-solanaceous species"
        ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "disease_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "scientific_name": "Begomovirus (TYLCV)",
        "severity": "Critical",
        "description": "Devastating viral disease transmitted by the sweetpotato whitefly (Bemisia tabaci); causes extreme stunting and complete yield failure.",
        "symptoms": [
            "Severe upward cupping and curling of leaf margins",
            "Interveinal yellowing (chlorosis) especially on younger leaves",
            "Severe plant stunting, bushy erect appearance, and flower drop before fruit set"
        ],
        "organic_treatment": [
            "Install fine insect netting (50-mesh) in greenhouses and over row covers",
            "Hang yellow sticky traps to capture whiteflies",
            "Immediately pull up, bag, and destroy infected plants to prevent virus spread"
        ],
        "chemical_treatment": [
            "Target vector whiteflies with Dinotefuran, Acetamiprid, or Spirotetramat",
            "Note: Chemical sprays do NOT cure the virus once the plant is infected"
        ],
        "prevention": [
            "Plant TYLCV-resistant tomato varieties (e.g., Tycoon, Charger, Invictus)",
            "Control weeds like nightshade and mallow that harbor whiteflies",
            "Use reflective silver mulch to deter whiteflies from landing"
        ]
    },
    "Tomato___Tomato_mosaic_virus": {
        "disease_name": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tobamovirus (ToMV)",
        "severity": "High",
        "description": "Extremely persistent, mechanically transmitted virus that causes leaf mottling, deformation, and internal fruit browning.",
        "symptoms": [
            "Light and dark green mottling (mosaic pattern) on leaves",
            "Distorted, blistered, or strap-like 'shoestring' leaves",
            "Internal brown necrosis in fruit wall and uneven ripening"
        ],
        "organic_treatment": [
            "Wash hands and dip tools in 20% non-fat dry milk solution before handling plants",
            "Immediately remove and burn infected plants (do not compost)",
            "Strictly prohibit tobacco smoking/handling near tomato crops"
        ],
        "chemical_treatment": [
            "No chemical virucides exist. Disinfect stakes and trellis wires with 10% trisodium phosphate (TSP)"
        ],
        "prevention": [
            "Plant resistant tomato cultivars (labeled 'Tm' or 'ToMV')",
            "Disinfect pruning tools continuously with 70% ethanol or milk solution",
            "Purchase heat-treated or certified virus-free seed"
        ]
    },
    "Tomato___healthy": {
        "disease_name": "Healthy Tomato Leaf",
        "scientific_name": "N/A",
        "severity": "None",
        "description": "Vibrant, vigorously growing solanum lycopersicum foliage with healthy glandular hairs and strong photosynthetic capacity.",
        "symptoms": ["Aromatic, lush dark green compound leaves with crisp margins and zero spots."],
        "organic_treatment": ["None required. Maintain consistent watering and organic compost tea."],
        "chemical_treatment": ["None required."],
        "prevention": ["Prune bottom foliage, stake securely, and scout weekly for signs of blight."]
    }
}


def get_disease_details(class_name: str) -> Dict[str, Any]:
    """
    Retrieves the rich agricultural advisory details for a given class name.
    Falls back gracefully with parsed heuristics if the exact key is not found.
    """
    crop, condition, is_healthy = parse_class_name(class_name)

    if class_name in DISEASE_KNOWLEDGE_BASE:
        details = dict(DISEASE_KNOWLEDGE_BASE[class_name])
    else:
        details = {
            "disease_name": condition,
            "scientific_name": "Unknown",
            "severity": "None" if is_healthy else "Moderate",
            "description": f"Condition detected on {crop}: {condition}.",
            "symptoms": [f"Visual signs of {condition} observed on {crop} foliage."],
            "organic_treatment": ["Isolate plant and inspect for pest or fungal development."],
            "chemical_treatment": ["Consult local agricultural extension advisor."],
            "prevention": ["Maintain clean cultivation and sanitize pruning equipment."]
        }

    details["class_name"] = class_name
    details["crop"] = crop
    details["condition"] = condition
    details["is_healthy"] = is_healthy

    return details
