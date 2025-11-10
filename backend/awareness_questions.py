# AI Awareness & Foundations Assessment Questions
# 25 questions across 5 domains
# Response categories: Early Awareness (1), Exploring Opportunities (2), Building Readiness (3), Ready to Progress (4)

AWARENESS_QUESTIONS_DATA = [
    {
        "code": "AU-01",
        "text": """How familiar are staff and leaders with what artificial intelligence (AI) actually is?""",
        "explanation": """Context: Understanding the basics of AI helps reduce confusion and fear. Many people associate AI only with automation or robotics, when in reality it also includes tools that analyse data, make predictions, or improve decision-making. This question assesses general familiarity with AI concepts across the organisation.""",
        "early_awareness": """Most people have little or no understanding of AI or what it can do.""",
        "exploring_opportunities": """Some individuals have heard of AI but misunderstand its purpose or potential.""",
        "building_readiness": """Staff and leaders have a basic understanding of AI concepts and examples.""",
        "ready_to_progress": """AI is widely understood as a tool to enhance—not replace—human decision-making.""",
        "domain_order": 1,
        "order": 1
    },
    {
        "code": "AU-02",
        "text": """How well does the organisation understand the potential benefits of AI for its work?""",
        "explanation": """Context: AI can help automate repetitive tasks, improve accuracy, and reveal new insights from data. Organisations at early stages often struggle to identify where AI might add value. This question explores whether your organisation has begun linking AI concepts to its mission or services.""",
        "early_awareness": """No understanding of AI benefits or relevance.""",
        "exploring_opportunities": """Some awareness of AI potential, but not connected to business goals.""",
        "building_readiness": """Clear examples identified where AI could improve efficiency or insight.""",
        "ready_to_progress": """Organisation actively explores potential AI use cases aligned to strategic goals.""",
        "domain_order": 1,
        "order": 2
    },
    {
        "code": "AU-03",
        "text": """How confident is the organisation in separating AI myths from realistic capabilities?""",
        "explanation": """Context: Public discussion of AI often mixes hype with fact. Early-stage organisations may believe AI can “think” or operate autonomously without limits. This question examines how well your organisation understands AI’s actual capabilities and limitations.""",
        "early_awareness": """Little awareness; AI often viewed as science fiction or fully autonomous.""",
        "exploring_opportunities": """Some understanding, but confusion or unrealistic expectations remain.""",
        "building_readiness": """Staff generally understand AI’s practical uses and limitations.""",
        "ready_to_progress": """Organisation promotes balanced, fact-based understanding of AI capabilities.""",
        "domain_order": 1,
        "order": 3
    },
    {
        "code": "AU-04",
        "text": """How open are leaders and staff to learning about AI and its implications?""",
        "explanation": """Context: Curiosity and openness are early indicators of readiness. Even without AI experience, a willingness to learn supports informed and responsible exploration. This question assesses cultural openness to new knowledge and experimentation.""",
        "early_awareness": """Staff show little interest or confidence in learning about AI.""",
        "exploring_opportunities": """Some curiosity exists, but few learning opportunities are provided.""",
        "building_readiness": """Leaders and teams express interest; learning sessions or discussions are encouraged.""",
        "ready_to_progress": """AI learning is part of ongoing professional development and curiosity is celebrated.""",
        "domain_order": 1,
        "order": 4
    },
    {
        "code": "AU-05",
        "text": """How clearly can staff and leaders explain how AI might impact their roles or services in the future?""",
        "explanation": """Context: Understanding how AI might change daily work helps organisations prepare and adapt. This question identifies whether staff and leaders have started thinking about how AI could influence workflows, service delivery, or skills needs.""",
        "early_awareness": """No discussion of AI’s impact on roles or services.""",
        "exploring_opportunities": """Some awareness, but perceptions are unclear or speculative.""",
        "building_readiness": """Staff and leaders can describe realistic potential changes or opportunities.""",
        "ready_to_progress": """Organisation actively plans for AI’s workforce impact through discussion and training.""",
        "domain_order": 1,
        "order": 5
    },
    {
        "code": "LV-01",
        "text": """How actively do leaders discuss or explore AI within the organisation’s strategic direction?""",
        "explanation": """Context: Leadership curiosity is vital in early stages of AI readiness. This question assesses whether executives or managers show interest in understanding AI’s potential impact and opportunities.""",
        "early_awareness": """AI has never been discussed at a leadership level.""",
        "exploring_opportunities": """AI occasionally mentioned but without direction or intent.""",
        "building_readiness": """Leadership shows interest and begins exploring AI’s relevance to strategy.""",
        "ready_to_progress": """Executives actively champion responsible AI exploration and learning initiatives.""",
        "domain_order": 2,
        "order": 1
    },
    {
        "code": "LV-02",
        "text": """How supportive are leaders of experimenting with small, low-risk digital or AI projects?""",
        "explanation": """Context: Early exploration builds understanding through experience. Leaders who support small experiments signal a culture of curiosity and innovation. This question evaluates whether such opportunities exist and are encouraged.""",
        "early_awareness": """No support for testing or experimentation with new technologies.""",
        "exploring_opportunities": """Occasional pilots or experiments occur informally.""",
        "building_readiness": """Leaders encourage small-scale, safe experimentation to explore AI potential.""",
        "ready_to_progress": """Innovation and pilot learning are embedded in leadership priorities and planning.""",
        "domain_order": 2,
        "order": 2
    },
    {
        "code": "LV-03",
        "text": """How well does the organisation connect AI exploration to its mission or community outcomes?""",
        "explanation": """Context: AI should serve real organisational goals, not just technological curiosity. This question assesses whether early discussions link AI potential to mission-driven or community-focused outcomes.""",
        "early_awareness": """No link between AI and organisational mission or service outcomes.""",
        "exploring_opportunities": """AI mentioned conceptually, but relevance unclear.""",
        "building_readiness": """Clear alignment between AI exploration and mission or public-service goals.""",
        "ready_to_progress": """AI principles directly tied to measurable outcomes that improve community or business value.""",
        "domain_order": 2,
        "order": 3
    },
    {
        "code": "LV-04",
        "text": """How willing is the organisation to invest time or resources in learning about AI responsibly?""",
        "explanation": """Context: Early investment doesn’t have to mean money—it can be time, training, or participation in shared learning networks. This question measures willingness to commit effort toward responsible exploration.""",
        "early_awareness": """No time or resources allocated to AI learning.""",
        "exploring_opportunities": """Minimal investment in learning opportunities; interest remains informal.""",
        "building_readiness": """Resources and time allocated for staff training or exploration.""",
        "ready_to_progress": """Investment in AI education and readiness embedded into planning cycles.""",
        "domain_order": 2,
        "order": 4
    },
    {
        "code": "LV-05",
        "text": """How confident are leaders in making informed decisions about adopting AI tools or vendors?""",
        "explanation": """Context: Understanding how to evaluate AI tools or vendors reduces risk. Many early-stage organisations rely on vendor claims without structured evaluation. This question gauges leadership’s confidence in assessing AI solutions critically.""",
        "early_awareness": """Leadership lacks knowledge or confidence to assess AI tools.""",
        "exploring_opportunities": """Some awareness, but decisions largely rely on vendor advice.""",
        "building_readiness": """Leadership seeks expert input and applies due diligence before adoption.""",
        "ready_to_progress": """AI procurement guided by clear evaluation criteria and ethical considerations.""",
        "domain_order": 2,
        "order": 5
    },
    {
        "code": "DR-01",
        "text": """How well does the organisation understand what data it has and where it’s stored?""",
        "explanation": """Context: Before exploring AI, organisations need basic data visibility. This question assesses awareness of what data exists, its location, and how it’s managed.""",
        "early_awareness": """Data is scattered or poorly understood; no central record of what exists.""",
        "exploring_opportunities": """Some understanding of key data sources but no consistent management.""",
        "building_readiness": """Data inventories or registers exist for major systems.""",
        "ready_to_progress": """Organisation maintains well-documented data assets ready for analysis or AI.""",
        "domain_order": 3,
        "order": 1
    },
    {
        "code": "DR-02",
        "text": """How reliable and accurate does the organisation consider its data to be?""",
        "explanation": """Context: AI relies on high-quality data. This question explores general confidence in data accuracy and completeness, even if formal governance doesn’t yet exist.""",
        "early_awareness": """Data accuracy is uncertain or inconsistent.""",
        "exploring_opportunities": """Some data considered reliable, but validation is irregular.""",
        "building_readiness": """Data quality monitored or checked in key systems.""",
        "ready_to_progress": """Consistent data-quality practices applied organisation-wide.""",
        "domain_order": 3,
        "order": 2
    },
    {
        "code": "DR-03",
        "text": """How easily can staff access the data they need to make decisions?""",
        "explanation": """Context: Data accessibility is a prerequisite for any future AI use. This question evaluates how easily information flows between teams and systems.""",
        "early_awareness": """Data is siloed and difficult to access.""",
        "exploring_opportunities": """Some data sharing occurs informally, but barriers remain.""",
        "building_readiness": """Staff can access data through authorised systems or shared repositories.""",
        "ready_to_progress": """Data accessibility and sharing supported by clear governance and secure platforms.""",
        "domain_order": 3,
        "order": 3
    },
    {
        "code": "DR-04",
        "text": """How secure and protected is organisational data from unauthorised access or misuse?""",
        "explanation": """Context: Data protection is essential even at early stages of digital transformation. This question assesses confidence in basic privacy and security controls.""",
        "early_awareness": """Data security not formally managed; risks largely unknown.""",
        "exploring_opportunities": """Basic protections (passwords, antivirus) exist, but no formal oversight.""",
        "building_readiness": """Clear data-protection practices in place (e.g., access control, encryption).""",
        "ready_to_progress": """Security is proactive, reviewed regularly, and aligned with best-practice standards.""",
        "domain_order": 3,
        "order": 4
    },
    {
        "code": "DR-05",
        "text": """How ready is the organisation’s technology infrastructure to support data analytics or AI exploration?""",
        "explanation": """Context: AI-readiness depends on having systems that can collect and process data efficiently. This question explores the perceived maturity of digital infrastructure.""",
        "early_awareness": """Technology systems outdated or unable to support analytics.""",
        "exploring_opportunities": """Some upgrades underway, but gaps remain.""",
        "building_readiness": """Systems modern, stable, and support data-driven projects.""",
        "ready_to_progress": """Scalable, secure infrastructure actively supports analytics and future AI experimentation.""",
        "domain_order": 3,
        "order": 5
    },
    {
        "code": "PS-01",
        "text": """How comfortable are staff using data or digital tools in their daily work?""",
        "explanation": """Context: Comfort with technology supports readiness for AI adoption. This question measures basic digital confidence rather than technical expertise.""",
        "early_awareness": """Staff have limited digital skills or confidence using data tools.""",
        "exploring_opportunities": """Staff use basic tools (e.g., spreadsheets) but struggle with more advanced systems.""",
        "building_readiness": """Staff generally confident using digital tools and basic data analysis.""",
        "ready_to_progress": """High digital literacy and openness to learning new technology.""",
        "domain_order": 4,
        "order": 1
    },
    {
        "code": "PS-02",
        "text": """How willing are staff to experiment with new tools or ways of working?""",
        "explanation": """Context: AI readiness begins with curiosity and adaptability. This question measures openness to testing new ideas and embracing change.""",
        "early_awareness": """Staff hesitant to try new tools or processes.""",
        "exploring_opportunities": """Some openness, but limited support for experimentation.""",
        "building_readiness": """Staff encouraged to test new digital tools responsibly.""",
        "ready_to_progress": """Continuous improvement culture where experimentation and feedback are valued.""",
        "domain_order": 4,
        "order": 2
    },
    {
        "code": "PS-03",
        "text": """How confident are managers in supporting their teams through technology change?""",
        "explanation": """Context: Managers play a key role in enabling safe innovation. This question assesses leadership readiness to guide teams through digital transformation.""",
        "early_awareness": """Managers lack confidence or guidance for supporting technology change.""",
        "exploring_opportunities": """Some managers lead small-scale initiatives but support varies.""",
        "building_readiness": """Managers trained and equipped to support digital or AI-related changes.""",
        "ready_to_progress": """Change management embedded in leadership development and planning.""",
        "domain_order": 4,
        "order": 3
    },
    {
        "code": "PS-04",
        "text": """How effectively does the organisation encourage staff to learn new skills related to technology or data?""",
        "explanation": """Context: Ongoing learning ensures the workforce evolves with digital transformation. This question assesses opportunities for continuous development.""",
        "early_awareness": """No structured training or learning opportunities available.""",
        "exploring_opportunities": """Occasional workshops or self-directed learning opportunities exist.""",
        "building_readiness": """Structured training and resources support skill development.""",
        "ready_to_progress": """Continuous learning culture embedded in workforce planning.""",
        "domain_order": 4,
        "order": 4
    },
    {
        "code": "PS-05",
        "text": """How confident are staff that AI or automation will support, not replace, their work?""",
        "explanation": """Context: Trust and reassurance are key to workforce readiness. This question examines perceptions of AI’s role—partner vs. threat.""",
        "early_awareness": """Staff fear AI will replace roles or reduce job security.""",
        "exploring_opportunities": """Some reassurance provided, but uncertainty remains.""",
        "building_readiness": """Communication emphasises AI as a support tool to enhance work.""",
        "ready_to_progress": """Staff trust AI initiatives as opportunities for growth and better outcomes.""",
        "domain_order": 4,
        "order": 5
    },
    {
        "code": "GT-01",
        "text": """How aware is the organisation of privacy and data-protection responsibilities?""",
        "explanation": """Context: Privacy protection underpins ethical technology use. This question explores whether staff understand basic privacy and compliance principles.""",
        "early_awareness": """Staff have limited awareness of privacy obligations.""",
        "exploring_opportunities": """Privacy awareness exists but practices are inconsistent.""",
        "building_readiness": """Privacy and data protection discussed in training or policy documents.""",
        "ready_to_progress": """Privacy culture embedded; staff actively consider data use and consent.""",
        "domain_order": 5,
        "order": 1
    },
    {
        "code": "GT-02",
        "text": """How does the organisation ensure technology and data are used responsibly and ethically?""",
        "explanation": """Context: Even without AI, responsible technology use is critical. This question assesses whether ethical thinking—fairness, transparency, and accountability—is part of daily operations.""",
        "early_awareness": """No consideration of ethics in technology decisions.""",
        "exploring_opportunities": """Some discussion, but no clear framework or policy.""",
        "building_readiness": """Ethical guidelines or informal principles influence technology decisions.""",
        "ready_to_progress": """Responsible-use principles documented and actively promoted.""",
        "domain_order": 5,
        "order": 2
    },
    {
        "code": "GT-03",
        "text": """How open is the organisation to being transparent about how it uses data or emerging technologies?""",
        "explanation": """Context: Transparency builds public trust. This question assesses willingness to share information about technology use and decision-making processes.""",
        "early_awareness": """No public or internal communication about data or technology use.""",
        "exploring_opportunities": """Some information shared reactively or when required.""",
        "building_readiness": """Organisation publishes general information about technology use and data handling.""",
        "ready_to_progress": """Proactive transparency embedded in communication and accountability practices.""",
        "domain_order": 5,
        "order": 3
    },
    {
        "code": "GT-04",
        "text": """How prepared is the organisation to identify and manage risks associated with new digital tools or AI?""",
        "explanation": """Context: Even early adopters need a basic understanding of risk. This question explores whether the organisation considers potential harms when testing or buying new tools.""",
        "early_awareness": """No process for identifying or managing technology risks.""",
        "exploring_opportunities": """Some awareness of risk, but actions are ad hoc or undocumented.""",
        "building_readiness": """Basic risk assessments performed before adopting new technologies.""",
        "ready_to_progress": """Consistent, proactive process for assessing and mitigating technology risks.""",
        "domain_order": 5,
        "order": 4
    },
    {
        "code": "GT-05",
        "text": """How confident is the organisation in its ability to adopt AI responsibly in the future?""",
        "explanation": """Context: Confidence in readiness reflects an understanding of both challenges and opportunities. This final question assesses overall perception of preparedness for responsible AI adoption.""",
        "early_awareness": """Organisation not confident; sees AI as too complex or risky.""",
        "exploring_opportunities": """Some confidence but acknowledges significant knowledge gaps.""",
        "building_readiness": """Feels generally ready to explore AI with proper guidance.""",
        "ready_to_progress": """Confident and intentional about pursuing AI responsibly and strategically.""",
        "domain_order": 5,
        "order": 5
    }
]
