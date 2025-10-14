**AM AI SAFE**

AI Framework Assessment

for

**{{org.name}}**

{{assessment.date}}

**Automated Version**

**\**

**Table of Contents**

[1. Executive Summary [3](#executive-summary)](#executive-summary)

[2. Assessment Results [3](#assessment-results)](#assessment-results)

[Figure 1. {{org.name}} AI Maturity Heatmap\
[4](#_Toc210400669)](#_Toc210400669)

[3. Recommendations [4](#recommendations)](#recommendations)

[3.1. High Priority Recommendations [4](#_Toc210400671)](#_Toc210400671)

[Table 1. High Priority Recommendations\
[4](#_Toc210400672)](#_Toc210400672)

[3.2. Medium Priority Recommendations\
[4](#_Toc210400673)](#_Toc210400673)

[Table 2. Medium Priority Recommendations\
[5](#_Toc187324589)](#_Toc187324589)

[3.3. Low Priority Recommendations [5](#_Toc210400675)](#_Toc210400675)

[Table 3. Low Priority Recommendations\
[5](#_Toc187324590)](#_Toc187324590)

**\**

# Executive Summary {% raw %}{#executive-summary .Heading01}{% endraw %}

The objective of this assessment was to evaluate **{{org.name}}**'s AI
maturity across critical domains to identify strengths, weaknesses, and
opportunities for improvement in their use and governance of artificial
intelligence.

Using the AM AI SAFE framework, the assessment covered 11 key domains:

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

These domains encompass 88 targeted questions designed to provide a
comprehensive view of **{{org.name}}**'s AI capabilities and risks.

# Assessment Results {% raw %}{#assessment-results .Heading01}{% endraw %}

The results indicate that {{org.name}} has achieved an overall AI
maturity score of **{{overall.score}}%**, placing the organization
within the **{{overall.tier}}** AI Maturity category.

The heatmap below provides a visual representation of **{{org.name}}**'s
performance across the 11 domains and the corresponding 88 assessment
questions. Each cell in the heatmap represents the score for a specific
question, with colours indicating the level of performance:

- **Red**: Lowest scoring questions, indicating significant gaps that
  require immediate attention.

- **Orange**: Below-average performance, highlighting areas for
  improvement.

- **Yellow**: Moderate performance, reflecting foundational practices
  with room for growth.

- **Green**: High performance, demonstrating strong alignment with best
  practices.

The heatmap is organized as follows:

- Rows represent the 11 domains of the AM AI SAFE Framework.

- Columns represent the 8 questions associated with each domain, scored
  on a scale from 0 (lowest) to 3 (highest).

- After all answers have been collected, scores are calculated and
  heatmap arranged with domains sorted by total score in descending
  order, and individual answer scores arranged from left to right, with
  lowest scores to the left.

- This provides an intuitive view of your organization's overall AI
  maturity status from both a domain and individual control perspective
  and allows for prioritisation of recommendations.

{{heatmap_image}}

[]{%raw%}{#_Toc210400669 .anchor}{%endraw%}Figure 1. {{org.name}} AI Maturity Heatmap

# Recommendations {% raw %}{#recommendations .Heading01}{% endraw %}

Based on the findings of the AI Maturity Assessment, the following key
recommendations are proposed to help **{{org.name}}** enhance its AI
governance and achieve a higher level of AI maturity:

1.  []{%raw%}{#_Toc210400671 .anchor}{%endraw%}High Priority Recommendations

These High Priority actions recommended for **{{org.name}}** are in
response to the lowest '**Non-Ideal**' scoring questions from the AI
Maturity Assessment. These represent critical gaps that require urgent
attention to mitigate risks and align **{{org.name}}**'s AI practices
with best-in-class standards. Addressing these actions will strengthen
foundational aspects of AI governance and build momentum for broader
improvements.

+---------------+--------------------+-----------------------------------------+
| ## **Domain** | ## **Question ID** | ## **Recommendation**                   |
+===============+====================+=========================================+
| {% for action in actions.high %}{{ action.domain }} | {{ action.question_id }} | {{ action.text }}{% endfor %} |
+---------------+--------------------+-----------------------------------------+

: []{%raw%}{#_Toc210400672 .anchor}{%endraw%}Table 1. High Priority Recommendations

2.  []{%raw%}{#_Toc210400673 .anchor}{%endraw%}Medium Priority Recommendations

These Medium Priority recommendations focus on addressing gaps
identified in the set of '**Basic**' scoring questions from the AI
Maturity Assessment. These initiatives build on the immediate actions by
targeting areas that require moderate effort and investment but are
crucial for enhancing **{{org.name}}**'s AI maturity within the next
6--12 months.

+----------------+--------------------+-----------------------------------------+
| ## **Domain**  | ## **Question ID** | ## **Recommendation**                   |
+================+====================+=========================================+
| {% for action in actions.medium %}{{ action.domain }} | {{ action.question_id }} | {{ action.text }}{% endfor %} |
+----------------+--------------------+-----------------------------------------+

: []{%raw%}{#_Toc187324589 .anchor}{%endraw%}Table 2. Medium Priority Recommendations

3.  []{%raw%}{#_Toc210400675 .anchor}{%endraw%}Low Priority Recommendations

These Low Priority recommendations focus on addressing gaps identified
as '**Good**' scoring questions from the AI Maturity Assessment. These
initiatives are designed to drive sustained improvement and align
**{{org.name}}**'s AI practices with industry-leading standards over the
next 1--3 years. The long-term strategy emphasizes strategic
investments, cultural shifts, and innovative approaches to AI
governance.

+---------------+--------------------+-----------------------------------------+
| ## **Domain** | ## **Question ID** | ## **Recommendation**                   |
+===============+====================+=========================================+
| {% for action in actions.low %}{{ action.domain }} | {{ action.question_id }} | {{ action.text }}{% endfor %} |
+---------------+--------------------+-----------------------------------------+

: []{%raw%}{#_Toc187324590 .anchor}{%endraw%}Table 3. Low Priority Recommendations
