# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **reelos-creative-15s** skill (v2.0.0) - a ReelOS-branded 15-second creative video script generator. Users provide a protagonist image + creative intent, and the system generates a complete 15s video script with cut rhythm, voiceover placement, BGM suggestions, and a stronger ReelOS brand memory point.

**Dual Content Modes**:
- **Mode 1 (Pure Creative, default)**: Art, philosophy, emotion, culture - no product placement
- **Mode 2 (Brand Advertising)**: Natural product integration - only when user provides product/brand info

## Architecture

### Core Purpose

Generate professional ReelOS 15-second video scripts following a strict 3-line output format:

1. **画面**: One-paragraph cut-by-cut description with time markers (0-2s/2-5s/5-9s/9-12s/12-15s)
2. **旁白**: Core voiceover/tagline (Chinese: ≤22 chars, English: ≤15 words), or "无（纯视觉）"
3. **音乐**: Music style + BPM + drop point suggestions

### Mode Detection

```
IF user provides product/brand info → Mode 2 (Brand Ad)
ELSE → Mode 1 (Pure Creative, default)
```

**Mode 1 Rules**:
- NO product placement, NO brand info, NO commercial content
- Focus: art, philosophy, emotion, culture, festival atmosphere
- Voiceover: poetic, philosophical, emotional resonance

**Mode 2 Rules**:
- Natural product integration via visual metaphors
- Product info appears at 5-12s window
- Voiceover: can include brand name or core value proposition
- CTA at 12-15s if provided

### Time Structure

**Output format**: 0-2s / 2-5s / 5-9s / 9-12s / 12-15s (5 segments)

**Mode 1 emotional arc**:
- 0-3s: Visual impact, establish theme tone
- 3-8s: Core concept unfolds, visual metaphors
- 8-12s: Emotional/philosophical climax
- 12-15s: Sublimation, epiphany, lasting impression

**Mode 2 information arc**:
- 0-5s: Hook - visual impact to grab attention
- 5-9s: First product touchpoint (via visual metaphor)
- 9-12s: Product feature/philosophy deepened
- 12-15s: Brand reinforcement + voiceover + CTA

### Visual Language

- Dense cut rhythm (every 2-3 seconds)
- Rich camera movements: 特写(close-up), 推镜(push), 快切(fast cut), 旋转(rotate), 定格(freeze), 变焦(zoom), 环绕(orbit)
- Mode 2: Natural product integration via visual metaphors (not hard ads)

### Content Constraints

- No explicit/NSFW content
- No false promises ("guaranteed viral", "100% sales increase")
- Respect image subject dignity
- Avoid trademark/celebrity naming unless authorized
- Mode 1: Zero commercial/brand info
- Mode 2: Truthful product info, compliant with advertising regulations

## File Structure

```
reelos-creative-15s/
├── SKILL.md                  # Skill definition (main workflow)
├── README.md                 # User documentation (Chinese)
├── CLAUDE.md                 # This file - developer guide
├── .gitignore                # Git ignore rules
├── reference/                # Reference materials (relatively static)
│   ├── voice_design.md       # Voice design handbook (10 voice types)
│   ├── bgm_database.md       # BGM style database (8 music styles)
│   └── visual_effects.md     # Visual effects handbook (planned)
├── knowledge/                # Knowledge base (dynamically accumulated)
│   └── case_study.md         # Case study database
├── rules/                    # Rule libraries
│   ├── templates.md          # Cut templates (6 types)
│   ├── visual_elements.md    # Visual element library
│   └── bgm_guide.md          # BGM quick decision guide
├── examples/                 # Example scripts
│   ├── spring_festival.md    # Spring Festival cases
│   ├── fashion.md            # Fashion cases
│   └── fantasy.md            # Fantasy/Gaming cases
└── templates/                # Output templates
    ├── standard.md           # Standard version (3 lines)
    └── premium.md            # Premium version
```

## Working with This Skill

### Input Processing

**Required Parameters**:
```python
{
  "image": "Image file or description",
  "intent": "Creative direction (e.g., zen philosophy, travel memory, fashion dynamic)"
}
```

**Optional Parameters**:
```python
{
  "tone": "cute|luxury|cool|epic|playful|hardcore|ethereal|dynamic|minimal",
  "festival": "Spring Festival|Valentine's|Black Friday|etc",
  "rhythm": "dynamic_fast_cut|smooth_progression|epic_burst|minimal_white_space",
  "aspect_ratio": "9:16|16:9",  # default: "9:16"
  "voiceover_must_include": "Specific voiceover content",
  "bpm": "Desired BPM (default: inferred from style)"
}
```

**Mode 2 Only (when user provides product info)**:
```python
{
  "product_info": "Product name / core selling points / brand philosophy",
  "integration_style": "natural|strong_exposure|metaphorical",
  "cta": "Try now|Click to generate|Learn more"
}
```

### Template Selection Logic

**6 Built-in Templates**:

1. **FESTIVAL_VIBES** (节日氛围) - Festival warmth
   - Elements: Festival symbols, cultural elements, atmosphere rendering
   - Rhythm: Fast cuts + dense festive elements
   - BGM: Guochao Electronic / Folk fusion 110-120 BPM
   - Suits: Spring Festival, Christmas, Valentine's, cultural expression

2. **FASHION_VISUAL** (时尚视觉) - Modern trendy
   - Elements: Dynamic rhythm, spotlights, neon, HUD lines, material close-ups
   - Rhythm: Beat-synced cuts + strong rhythm
   - BGM: House/Trap 120-130 BPM
   - Suits: Fashion, streetwear, youth culture

3. **EPIC_NARRATIVE** (史诗叙事) - Epic fantasy
   - Elements: Energy effects, shockwaves, particle bursts, slow-motion
   - Rhythm: Slow-motion + burst points
   - BGM: Epic Electronic / Cinematic 130-150 BPM
   - Suits: Fantasy, martial arts, grand narratives

4. **MINIMAL_ART** (极简艺术) - Premium minimal
   - Elements: White space, texture, micro-animations, geometric lines
   - Rhythm: Smooth progression + precise beats
   - BGM: Ambient/Minimal 90-110 BPM
   - Suits: Philosophy, zen, high-end, art films

5. **EMOTIONAL_CONNECT** (情感共鸣) - Emotional resonance
   - Elements: Character close-ups, emotional progression, story feel, memory atmosphere
   - Rhythm: Emotional curve progression
   - BGM: Piano/Guitar/Emotional Electronic 100-120 BPM
   - Suits: Human stories, emotional expression, nostalgia, warmth

6. **BRAND_AD** (品牌广告) - Brand advertising (Mode 2 only)
   - Elements: Product display + creative metaphor + info integration
   - Rhythm: Information-dense + clear structure
   - BGM: Clear rhythm 110-130 BPM
   - Suits: Product promotion, brand campaigns, marketing events

### Image Analysis Framework

```python
analysis = {
  "character_vibe": ["cute", "cool", "elegant", "traditional", "tech", "youthful"],
  "clothing_material": ["fabric_type", "color_palette"],
  "scene_atmosphere": ["indoor", "outdoor", "studio", "street", "nature"],
  "usable_camera_language": ["close-up", "push", "rotate", "freeze", "zoom"]
}
```

### Template Matching Algorithm

```python
def select_template(intent, image_analysis, mode):
    keywords = extract_keywords(intent)

    scores = {
        "FESTIVAL_VIBES": match_festival_keywords(keywords),
        "FASHION_VISUAL": match_fashion_keywords(keywords),
        "EPIC_NARRATIVE": match_epic_keywords(keywords),
        "MINIMAL_ART": match_minimal_keywords(keywords),
        "EMOTIONAL_CONNECT": match_emotional_keywords(keywords),
    }

    # Mode 2 only: consider BRAND_AD template
    if mode == 2:
        scores["BRAND_AD"] = match_brand_keywords(keywords)

    # Consider image analysis
    if "traditional_costume" in image_analysis:
        scores["EPIC_NARRATIVE"] += 20
    if "urban_night" in image_analysis:
        scores["FASHION_VISUAL"] += 20
    if "nature_sunset" in image_analysis:
        scores["EMOTIONAL_CONNECT"] += 20

    return get_template_or_mix(scores)
```

### Output Generation

**Fixed 3-Line Format**:

```markdown
画面：[Time-stamped one-paragraph cut description]

旁白：[Voiceover ≤22 Chinese chars / ≤15 English words, or "无（纯视觉）"]

音乐：[Style + BPM + drop point]
```

**画面 Requirements**:
- Must include time markers: 0-2s, 2-5s, 5-9s, 9-12s, 12-15s
- Rich camera language, dense visual changes every 2-3 seconds
- One-paragraph format for easy copy-paste
- Mode 1: Pure visual metaphors, zero brand info
- Mode 2: Product info naturally integrated via visual metaphors

**旁白 Requirements**:
- Chinese: ≤22 characters; English: ≤15 words
- Catchy rhythm, easy to remember
- Mode 1: Poetic / philosophical / emotional, no brand
- Mode 2: Can include brand name or core value proposition
- If no voiceover needed: "无（纯视觉）"

**音乐 Requirements**:
- Clear style (e.g., 禅意电子, 国潮, House, Trap, 史诗, Ambient, 钢琴)
- Clear BPM range
- Mark drop point (usually 10-12s)

### Version Tiers

**Standard (Default)**: 画面 + 旁白 + 音乐

**Premium (Optional)**: Standard + 字幕 + 音效 + 备选旁白

### Reference Materials

Consult these for enriched output:
- `reference/voice_design.md` - 10 voice types with matching matrices
- `reference/bgm_database.md` - 8 music styles with scene matching
- `rules/visual_elements.md` - Visual element library with camera language
- `rules/templates.md` - Detailed template structures with example sentence patterns
- `rules/bgm_guide.md` - BGM quick decision guide
- `knowledge/case_study.md` - Real-world case studies with deep analysis

## Safety & Compliance

### Content Filters

**Reject if**:
- Explicit/NSFW imagery or descriptions
- Hate speech or political mobilization
- False promises ("guaranteed viral", "100% sales increase")
- Celebrity/trademark without authorization

**Warning if**:
- Image contains recognizable brand logos → Suggest generic description
- Minors in image → Ensure family-friendly content only

## Error Handling

### Issue: Intent unclear
**Solution**: Provide 2-3 template options and ask user to choose

### Issue: Mode ambiguous (unclear if user wants product placement)
**Solution**: Default to Mode 1 (pure creative); ask if they want product integration

### Issue: Voiceover exceeds 22 chars
**Solution**:
1. Split into two lines
2. Use visual-only text animation
3. Offer 3 shorter alternatives

### Issue: Image analysis fails
**Solution**: Use generic template based on intent only, prompt "Upload image for customized visuals"

### Issue: Too many product points (Mode 2)
**Solution**: Prioritize by user-specified order. If not specified, select top 1-2 selling points for 5-12s integration.

## Best Practices

1. **Always include time markers** - 0-2s/2-5s/5-9s/9-12s/12-15s
2. **Match rhythm to BGM** - Cuts sync with beats
3. **Use active verbs** - 闪耀(flash), 炸开(explode), 旋转(spin)
4. **Visual metaphors over text** - Show don't tell
5. **Mode 1: Pure expression** - Zero commercial content
6. **Mode 2: Natural integration** - Weave product into story, not interrupt it
7. **Consult reference materials** - Use voice_design.md and bgm_database.md for enriched output

## Development Notes

- All outputs in Chinese for Chinese market
- English support via language parameter
- Template mixing encouraged for unique styles
- Keep one-paragraph format for easy copy-paste
- SKILL.md is the authoritative source for all design decisions

## Skill Invocation Triggers

Users invoke this skill by:
- Requesting video/ad script generation
- Asking for short video creative/script
- Providing creative brief + image
- Using `/reelos-creative-15s` command
