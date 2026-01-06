# AI System Maturity Assessment - Word Template Variables

Complete reference guide for all available template variables in DOCX report templates.

---

## Template System

The report uses **docxtpl** (Python-DOCX Template) which supports Jinja2 syntax.
- Use `{{ variable }}` for simple values
- Use `{% for item in list %} ... {% endfor %}` for loops
- Use `{% if condition %} ... {% endif %}` for conditionals

---

## 1. ORGANIZATION INFORMATION

### `{{org.name}}`
**Type:** String  
**Description:** The name of the organization being assessed  
**Example:** "Acme Corporation"

---

## 2. ASSESSMENT METADATA

### `{{assessment.date}}`
**Type:** Date String (YYYY-MM-DD)  
**Description:** The date when the assessment was completed  
**Example:** "2025-01-15"  
**Note:** Use `{{formatDate(assessment.date)}}` for formatted output (e.g., "15 January 2025")

### `{{assessment.version}}`
**Type:** String  
**Description:** The report version number  
**Example:** "1.0.0"

---

## 3. OVERALL SCORES

### `{{overall.score}}`
**Type:** Number (0-100)  
**Description:** Overall assessment score as a percentage  
**Example:** 75.5  
**Usage:** `{{overall.score}}%`

### `{{overall.tier}}`
**Type:** String  
**Description:** The maturity tier based on the overall score  
**Possible Values:** "Leading", "Established", "Developing", "Foundational"  
**Example:** "Established"

---

## 4. VISUALIZATIONS (IMAGES)

### `{{heatmap_image}}`
**Type:** InlineImage Object  
**Description:** Heatmap visualization showing scores across all domains and questions  
**Usage:** Place this placeholder where you want the heatmap image to appear  
**Note:** This is a pre-generated image object, not a URL

### `{{radar_chart_image}}`
**Type:** InlineImage Object  
**Description:** Radar chart showing domain performance  
**Usage:** Place this placeholder where you want the radar chart to appear  
**Note:** This is a pre-generated image object, not a URL

### `{{assets.heatmapUrl}}`
**Type:** String (Data URL)  
**Description:** Alternative heatmap reference (base64 encoded)  
**Usage:** For HTML-style templates or if inline image doesn't work

---

## 5. TOP STRENGTHS & GAPS

### `{{top_3_strengths}}`
**Type:** Array of Objects  
**Description:** The 3 highest-scoring domains  
**Structure:**
```
[
  {
    "domain": "Security",
    "percentage": "87.5%"
  },
  {
    "domain": "Privacy", 
    "percentage": "83.3%"
  },
  {
    "domain": "Transparency",
    "percentage": "79.2%"
  }
]
```

**Usage Example:**
```
{% for strength in top_3_strengths %}
{{ loop.index }}. {{ strength.domain }}: {{ strength.percentage }}
{% endfor %}
```

### `{{top_3_gaps}}`
**Type:** Array of Objects  
**Description:** The 3 lowest-scoring domains (areas needing most improvement)  
**Structure:**
```
[
  {
    "domain": "Explainability",
    "percentage": "45.8%"
  },
  {
    "domain": "Data Integrity",
    "percentage": "52.1%"
  },
  {
    "domain": "Fairness",
    "percentage": "58.3%"
  }
]
```

**Usage Example:**
```
{% for gap in top_3_gaps %}
{{ loop.index }}. {{ gap.domain }}: {{ gap.percentage }}
{% endfor %}
```

---

## 6. PRIORITIZED ACTIONS (RECOMMENDATIONS)

### `{{actions.high}}`
**Type:** Array of Objects  
**Description:** High priority recommendations (for questions scored 1/4 - Foundational)  
**Structure:**
```
[
  {
    "domain": "Fairness",
    "question_id": "FA-1",
    "text": "Implement regular bias audits..."
  },
  {
    "domain": "Transparency",
    "question_id": "TR-2", 
    "text": "Develop clear documentation..."
  }
]
```

**Usage Example:**
```
High Priority Actions:
{% for action in actions.high %}
{{ loop.index }}. [{{ action.question_id }}] {{ action.domain }}
   {{ action.text }}
{% endfor %}
```

### `{{actions.medium}}`
**Type:** Array of Objects  
**Description:** Medium priority recommendations (for questions scored 2/4 - Developing)  
**Structure:** Same as actions.high

**Usage Example:**
```
Medium Priority Actions:
{% for action in actions.medium %}
{{ loop.index }}. [{{ action.question_id }}] {{ action.domain }}
   {{ action.text }}
{% endfor %}
```

### `{{actions.low}}`
**Type:** Array of Objects  
**Description:** Low priority recommendations (for questions scored 3/4 - Established)  
**Structure:** Same as actions.high

**Usage Example:**
```
Low Priority Actions:
{% for action in actions.low %}
{{ loop.index }}. [{{ action.question_id }}] {{ action.domain }}
   {{ action.text }}
{% endfor %}
```

**Note:** Questions scored 4/4 (Leading) are not included in recommendations as they represent best practice.

---

## 7. CONTENT SECTIONS (PRE-GENERATED TEXT)

### `{{executive_summary}}`
**Type:** String (Multi-paragraph text)  
**Description:** Comprehensive executive summary of the assessment results  
**Content Includes:**
- Overall maturity level and score
- Key strengths and weaknesses
- Strategic implications
- High-level recommendations  
**Length:** ~3-5 paragraphs

### `{{assessment_methodology}}`
**Type:** String (Multi-paragraph text)  
**Description:** Detailed explanation of the assessment methodology  
**Content Includes:**
- Assessment framework overview
- Scoring scale explanation (1-4: Foundational → Leading)
- 11 domain descriptions
- Question structure
- Best practices for assessment  
**Length:** ~4-6 paragraphs

### `{{domain_analysis}}`
**Type:** String (Multi-paragraph text)  
**Description:** Domain-by-domain detailed analysis  
**Content Includes:**
- Individual domain scores and maturity levels
- Score ranges and question counts
- Domain-specific insights
- Strengths and improvement opportunities per domain  
**Length:** ~10-15 paragraphs (varies by number of domains with answers)

### `{{key_findings}}`
**Type:** String (Multi-paragraph text)  
**Description:** Key findings and insights from the assessment  
**Content Includes:**
- Highest performing domain analysis
- Lowest performing domain analysis
- Distribution of maturity levels
- Critical gaps identified
- Strategic observations  
**Length:** ~4-6 paragraphs

### `{{implementation_roadmap}}`
**Type:** String (Multi-paragraph text)  
**Description:** Comprehensive implementation roadmap  
**Content Includes:**
- Phased approach (immediate, short-term, long-term)
- Quick wins identification
- Foundational improvements
- Advanced capabilities development
- Continuous improvement framework  
**Length:** ~5-7 paragraphs

---

## 8. HELPER FUNCTIONS

### `{{formatDate(date_string)}}`
**Type:** Function  
**Description:** Formats a date string to readable format  
**Input:** Date string in YYYY-MM-DD format  
**Output:** Formatted date like "15 January 2025"  
**Usage:** `{{formatDate(assessment.date)}}`

---

## 9. JINJA2 CONTROL STRUCTURES

### Loops
```
{% for action in actions.high %}
  {{ loop.index }}. {{ action.domain }}
  {{ action.text }}
{% endfor %}
```

**Loop Variables:**
- `loop.index` - Current iteration (1-indexed)
- `loop.index0` - Current iteration (0-indexed)
- `loop.first` - True if first iteration
- `loop.last` - True if last iteration
- `loop.length` - Total number of items

### Conditionals
```
{% if overall.score >= 75 %}
  Excellent performance!
{% elif overall.score >= 50 %}
  Good performance with room for improvement.
{% else %}
  Significant improvement needed.
{% endif %}
```

### Filters
```
{{ org.name|upper }}  # ACME CORPORATION
{{ overall.score|round(1) }}  # 75.5
{{ actions.high|length }}  # Number of high priority actions
```

---

## 10. COMPLETE EXAMPLE TEMPLATE

```
AI SYSTEM MATURITY ASSESSMENT REPORT

Organization: {{org.name}}
Assessment Date: {{formatDate(assessment.date)}}
Report Version: {{assessment.version}}

EXECUTIVE SUMMARY
{{executive_summary}}

OVERALL RESULTS
Overall Maturity Score: {{overall.score}}%
Maturity Tier: {{overall.tier}}

TOP 3 STRENGTHS
{% for strength in top_3_strengths %}
{{ loop.index }}. {{ strength.domain }}: {{ strength.percentage }}
{% endfor %}

TOP 3 AREAS FOR IMPROVEMENT
{% for gap in top_3_gaps %}
{{ loop.index }}. {{ gap.domain }}: {{ gap.percentage }}
{% endfor %}

HEATMAP VISUALIZATION
{{heatmap_image}}

DOMAIN ANALYSIS
{{domain_analysis}}

HIGH PRIORITY RECOMMENDATIONS ({{actions.high|length}} items)
{% for action in actions.high %}
{{ loop.index }}. [{{ action.question_id }}] {{ action.domain }}
   {{ action.text }}
{% endfor %}

MEDIUM PRIORITY RECOMMENDATIONS ({{actions.medium|length}} items)
{% for action in actions.medium %}
{{ loop.index }}. [{{ action.question_id }}] {{ action.domain }}
   {{ action.text }}
{% endfor %}

KEY FINDINGS
{{key_findings}}

IMPLEMENTATION ROADMAP
{{implementation_roadmap}}
```

---

## NOTES

1. **Scoring Scale:** All assessments now use a 1-4 scale:
   - 1 = Foundational (0-25%)
   - 2 = Developing (26-50%)
   - 3 = Established (51-75%)
   - 4 = Leading (76-100%)

2. **Action Priority Mapping:**
   - Score 1 (Foundational) → High Priority
   - Score 2 (Developing) → Medium Priority
   - Score 3 (Established) → Low Priority
   - Score 4 (Leading) → Not included (best practice achieved)

3. **Domain List:** The 11 domains are:
   - Fairness
   - Transparency
   - Explainability
   - Accountability
   - Data Integrity
   - Reliability
   - Security
   - Privacy
   - Safety
   - Inclusivity
   - Sustainability

4. **Image Handling:** The `heatmap_image` and `radar_chart_image` variables are InlineImage objects that will automatically render in the Word document. Simply place the placeholder where you want the image to appear.

5. **Text Sections:** The pre-generated text sections (executive_summary, domain_analysis, etc.) are already formatted with proper paragraphs and can be inserted directly into the template.

---

## 10. SECTOR-SPECIFIC ACTION STEPS (NEW)

These variables provide sector/industry-specific recommendations based on the assessment's sector and question scores.

### `{{sector_name}}`
**Type:** String  
**Description:** The industry/sector of the assessed AI system  
**Example:** "Finance / Insurance"  
**Usage:** 
```
Assessment Sector: {{sector_name}}
```

### `{{sector_actions.high}}`
**Type:** Array of Objects  
**Description:** High-priority sector-specific action steps (for questions scoring 1)  
**Structure:**
```json
[
  {
    "domain": "Fairness",
    "question_id": "FA-1",
    "sector_action": "Deploy automated fairness monitoring tools to compare loan approval/rejection rates across protected characteristics...",
    "score": 1
  }
]
```
**Usage in template:**
```
{% for action in sector_actions.high %}
{{ loop.index }}. [{{ action.question_id }}] {{ action.domain }}
   {{ action.sector_action }}
{% endfor %}
```

### `{{sector_actions.medium}}`
**Type:** Array of Objects  
**Description:** Medium-priority sector-specific action steps (for questions scoring 2)  
**Structure:** Same as `sector_actions.high`

### `{{sector_actions.low}}`
**Type:** Array of Objects  
**Description:** Low-priority sector-specific action steps (for questions scoring 3)  
**Structure:** Same as `sector_actions.high`

### Available Sectors

The following sectors have predefined action steps:
- Local Government / Public Sector
- Education
- Healthcare
- Finance / Insurance
- Technology / Software
- Utilities / Critical Infrastructure
- Manufacturing
- Retail / Hospitality
- Consulting / Professional Services
- Not-for-profit / Charity
- Other

### Example Output

**For Finance / Insurance sector:**

```
HIGH PRIORITY SECTOR ACTIONS:

1. [FA-1] Fairness
   Deploy automated fairness monitoring tools to compare loan approval/rejection 
   rates across protected characteristics, triggering audits when disparities 
   exceed regulatory thresholds.

2. [TR-2] Transparency
   Create detailed model documentation repositories tracking data lineage, 
   preprocessing steps, algorithmic decisions, and version history with 
   comprehensive audit trails.

MEDIUM PRIORITY SECTOR ACTIONS:

1. [AC-4] Accountability
   Implement comprehensive complaint handling for AI-influenced decisions, with 
   dedicated specialists, documented procedures, and customer communication 
   templates.
```

