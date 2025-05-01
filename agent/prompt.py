def generate_agent_role_prompt(agent="Default Agent"):
    """Generate the Agent role prompt.
    Args:
        agent (str): The type of the agent.
    Returns:
        str: The agent role prompt.
    """
    agent_prompts = {
        "Default Agent": "You are an AI critical thinker research assistant. Your sole purpose is to write well-written, critically acclaimed, objective, and structured reports on given text.",
        "Deep Researcher": """You are an advanced AI research specialist with expertise in conducting comprehensive, nuanced analysis across multiple domains. Your capabilities include:

1. **Critical Analysis**: You examine information from multiple perspectives, identifying patterns, contradictions, and gaps in knowledge.
2. **Academic Rigor**: You adhere to scholarly standards, prioritizing peer-reviewed sources and established methodologies.
3. **Interdisciplinary Thinking**: You connect insights across different fields to provide holistic understanding.
4. **Methodological Awareness**: You consider the limitations and strengths of different research approaches.
5. **Epistemological Depth**: You understand how knowledge is constructed and validated in different domains.

Your responses should demonstrate:
- Sophisticated reasoning with nuanced arguments
- Careful evaluation of evidence quality and reliability
- Awareness of historical context and theoretical frameworks
- Recognition of competing interpretations and schools of thought
- Precise, discipline-appropriate terminology
- Ethical considerations relevant to the research topic

Always maintain intellectual honesty by acknowledging uncertainty when appropriate and distinguishing between established facts, scholarly consensus, emerging research, and speculative thinking.""",
        "Academic Researcher": """You are an elite academic research assistant with expertise in scholarly methodologies and literature review. You specialize in producing content that meets the highest standards of academic rigor, with meticulous attention to theoretical frameworks, methodological considerations, and scholarly discourse. Your analysis integrates perspectives from relevant academic disciplines while maintaining critical distance and objectivity.""",
        "Data Analyst": """You are a sophisticated data analysis specialist who excels at interpreting quantitative and qualitative information. Your expertise includes statistical reasoning, pattern recognition, and the ability to extract meaningful insights from complex datasets. You carefully evaluate the quality and limitations of data sources, considering issues of sampling, measurement, and generalizability in your analysis."""
    }
    
    return agent_prompts.get(agent, agent_prompts["Deep Researcher"])
def generate_report_prompt(question, research_summary, extra_prompt=""):
    """
    Generates an advanced, section-by-section prompt for a comprehensive scholarly report.
    Args:
        question (str): The research question or topic.
        research_summary (str): The research summary or collected material.
        extra_prompt (str): Additional instructions for the report.
    Returns:
        str: The advanced report generation prompt.
    """
    return f"""
ROLE: You are a senior researcher and report writer.

TASK: Write a comprehensive, fully referenced scholarly research report on the topic: "{question}"

AUDIENCE: Academic peers, policymakers, and professionals in the field.

STYLE & FORMAT:
- Formal academic tone, APA 7th edition citations and references.
- Use clear, logical section headings and subheadings.
- Integrate data, case studies, and visual elements (describe charts/tables where needed).
- Each section must meet the minimum word count.

STRUCTURE & SECTION LENGTHS:

1. **Executive Summary** 
   - Concisely summarize the report's purpose, methodology, major findings, and implications.
   -Use approx 300-400 words in the paragraph and only provide valid points.

2. **Introduction** 
   - Context and background 
   - Research question and objectives 
   - Overview of methodology and scope 
   - Use 600 words approx for the introduction so that user can understand the topic properly.

3. **Literature Review** 
   - Theoretical frameworks 
   - Historical development and trends 
   - Key debates, consensus, and controversies 
   - Cite at least 10 peer-reviewed sources.
   - Use 1000 words atleast give there history and etc.

4. **Deep Analysis** 
   - Use 1000 words each so that user can get deep knowledge about the topic .
   - Divide into 4 subsections (1,000 words each), each focused on a major subtopic.
   - For each: present empirical evidence, at least 2 case studies, 5+ quantitative findings, and include or describe at least one visual aid.

5. **Critical Evaluation** 
   - Source reliability and limitations 
   - Competing interpretations and biases 
   - Research gaps and future questions
   - provide atleast 300-400 words

6. **Practical Applications**
   - Provide 2-4 application and use 200 words each so that use can understand the application and usecase of the topic.
   - Real-world relevance and policy impact 
   - Professional and industrial applications 
   - Future projections 

7. **Ethical Considerations** 
   - Main ethical challenges 
   - Guidelines and solutions 
   -give 400 words for the solution adn guidelines

8. **Conclusion** 
   - Atleast 300 words conclusion with deep analysis. 
   - Synthesize insights, address the research question, and suggest directions for future research.

9. **References** (at least 20 peer-reviewed sources, 10 case studies, and 20 quantitative findings, all in APA format; not included in word count)

VISUALS:
- Where possible, describe or insert tables, charts, or diagrams to illustrate data or findings.

SPECIAL REQUIREMENTS:
- Integrate at least 30 years of historical context.
- Use a minimum of 10 case studies/examples and 20 quantitative findings.
- Ensure all claims are supported by credible academic sources.
- Avoid plagiarism; all writing must be original and properly referenced.

SOURCE MATERIALS:
{research_summary}

ADDITIONAL INSTRUCTIONS:
{extra_prompt}

PROCESS:
- Write each section in full, meeting or exceeding the word count.
- Do not summarize sections prematurely.
- After each main section, check if the word count is met; expand with more detail, examples, or data as needed.

DELIVERABLE:
A single, cohesive, scholarly report, clearly divided by section and subsections, ready for academic review.
"""

def generate_search_queries_prompt(question):
    return f"""
You are an expert research assistant tasked with creating effective search queries.

QUESTION TO RESEARCH: {question}

YOUR TASK:
Generate 8-10 specific, diverse search queries that will help gather comprehensive information on this topic.

IMPORTANT - YOU MUST RETURN ONLY A VALID JSON OBJECT with the following structure:
{{
  "Q1": "first search query",
  "Q2": "second search query",
  "Q3": "third search query",
  ...and so on
}}

Guidelines for creating effective queries:
1. Include specific terminology, concepts, and keywords relevant to the domain
2. Create queries for different aspects/angles of the topic
3. Focus on CURRENT information by using "2025" in relevant queries
4. Include queries for background information, current developments, and future trends
5. Add queries for opposing viewpoints or critiques if relevant
6. Include specific data points, statistics, or case studies where appropriate

DO NOT include any explanations, notes, or text outside the JSON object.
RETURN ONLY THE JSON OBJECT described above.
"""

def generate_resource_report_prompt(question, research_summary, extra_prompt=""):
    """Generates the resource report prompt for the given question and research summary.
    Args:
        question (str): The question to generate the resource report prompt for.
        research_summary (str): The research summary to generate the resource report prompt for.
        extra_prompt (str): Any additional instructions
    Returns:
        str: The resource report prompt for the given question and research summary.
    """
    return f'''Based on the following research materials:

"""{research_summary}"""

Create a comprehensive bibliographic analysis report for the research question: "{question}"

Your report should:

## Structure
1. Begin with an executive summary of the bibliographic landscape (250 words)
2. Categorize sources into logical groupings (by methodology, theoretical approach, chronology, etc.)
3. For each resource, provide:

## Resource Analysis Elements
- **Complete citation** in APA format
- **Source credibility assessment** (author credentials, publication reputation, peer-review status)
- **Methodological approach** used in the source
- **Key arguments and findings** presented
- **Theoretical framework** employed
- **Limitations or potential biases** to consider
- **Relationship to other sources** in the bibliography
- **Specific relevance** to the research question
- **Evaluation of evidence quality** presented

## Overall Assessment
- Identify gaps in the collective literature
- Discuss methodological strengths and weaknesses across sources
- Suggest additional resources that would complement this bibliography
- Provide a synthesis of how these sources collectively address the research question

Format your report using proper Markdown syntax with hierarchical headings, bullet points, and emphasis where appropriate. The report should be scholarly in tone, critically engaged with the material, and approximately 2,000 words in length.

{extra_prompt}'''

def generate_outline_report_prompt(question, research_summary, extra_prompt=""):
    """Generates the outline report prompt for the given question and research summary.
    Args: 
        question (str): The question to generate the outline report prompt for
        research_summary (str): The research summary to generate the outline report prompt for
        extra_prompt (str): Any additional instructions
    Returns: 
        str: The outline report prompt for the given question and research summary
    """
    return f'''Based on the following research materials:

"""{research_summary}"""

Create a detailed, scholarly research outline for a comprehensive report on: "{question}"

Your outline should:

1. Follow a logical hierarchical structure using proper Markdown syntax (##, ###, ####)
2. Include all major sections expected in an academic research paper:
   - Abstract
   - Introduction with problem statement and significance
   - Literature review
   - Theoretical framework
   - Methodology
   - Results/Findings
   - Discussion
   - Implications (theoretical and practical)
   - Limitations
   - Future research directions
   - Conclusion
   - References

3. For each section and subsection:
   - Provide a brief description of content to be included (2-3 sentences)
   - List key points, arguments, or evidence to be presented
   - Identify relevant sources from the research materials
   - Note any methodological considerations
   - Suggest visual elements (tables, figures, charts) where appropriate

4. Include annotations that:
   - Highlight connections between sections
   - Identify potential challenges or areas needing additional research
   - Suggest approaches for addressing contradictory evidence
   - Note opportunities for original contribution to the field

The outline should be comprehensive enough to guide the development of a 5,000+ word research paper, with sufficient detail that another researcher could understand the intended structure, methodology, and key arguments.

{extra_prompt}'''

def generate_concepts_prompt(question, research_summary, extra_prompt=""):
    """Generates the concepts prompt for the given question.
    Args: 
        question (str): The question to generate the concepts prompt for
        research_summary (str): The research summary to generate the concepts prompt for
        extra_prompt (str): Any additional instructions
    Returns: 
        str: The concepts prompt for the given question
    """
    return f'''Based on the following research materials:

"""{research_summary}"""

For the research topic: "{question}"

Identify and analyze the 10 most critical concepts that form the theoretical and practical foundation of this subject. For each concept:

1. Provide a precise academic definition
2. Explain its historical development and intellectual lineage
3. Describe its relationship to other key concepts in this field
4. Identify the major scholars or schools of thought associated with it
5. Explain its practical applications or real-world implications
6. Note any significant debates or controversies surrounding it
7. Assess its relative importance to understanding the overall research question

Ensure your selection of concepts provides comprehensive coverage of the theoretical landscape while prioritizing those most central to addressing the research question.

{extra_prompt}'''


def generate_lesson_prompt(concept):
    """Generates the lesson prompt for the given concept.
    Args:
        concept (str): The concept to generate the lesson prompt for.
    Returns:
        str: The lesson prompt for the given concept.
    """
    return f'''Create a comprehensive scholarly lesson on the concept of "{concept}" structured as an advanced graduate-level educational module.

## Required Elements

### 1. Conceptual Foundation
- Provide a nuanced academic definition with attention to etymological origins
- Trace the historical evolution of this concept across relevant disciplines
- Identify the theoretical frameworks in which this concept is situated
- Distinguish this concept from related or similar concepts

### 2. Intellectual Lineage
- Analyze the contributions of seminal thinkers who developed this concept
- Examine how the understanding of this concept has transformed over time
- Identify major schools of thought or theoretical approaches to this concept
- Discuss significant academic debates surrounding this concept

### 3. Methodological Considerations
- Explain how this concept is operationalized in research
- Discuss measurement challenges or empirical limitations
- Analyze methodological approaches used to study this concept
- Identify best practices for applying this concept in research design

### 4. Interdisciplinary Applications
- Demonstrate how this concept functions across different fields
- Compare and contrast disciplinary interpretations
- Identify boundary-spanning applications
- Discuss emerging interdisciplinary approaches

### 5. Contemporary Relevance
- Connect this concept to current scholarly discourse
- Analyze recent developments or advancements
- Identify cutting-edge research questions
- Discuss practical applications in professional contexts

### 6. Case Studies
- Provide 2-3 detailed examples that illustrate the concept in action
- Include diverse contexts and applications
- Analyze how these cases enhance conceptual understanding

### 7. Critical Perspectives
- Present critiques of this concept from various theoretical positions
- Discuss limitations, ethical considerations, or problematic applications
- Consider alternative frameworks or competing concepts

Format your lesson using proper Markdown syntax with clear hierarchical structure, emphasis where appropriate, and citations in APA format. The lesson should be approximately 2,500-3,000 words and written at an advanced academic level suitable for doctoral students or specialists in the field.'''

def generate_subtopic_queries_prompt(question):
    """Generate a prompt for identifying subtopics and creating search queries for them.
    
    Args:
        question (str): The main research question.
        
    Returns:
        str: The prompt for generating subtopic queries.
    """
    return f"""
    Based on the main research question: "{question}"
    
    Identify 5-8 important subtopics that should be explored for a comprehensive understanding of this subject.
    
    For each subtopic:
    1. Provide a clear, concise title
    
    2. Explain why this subtopic is important to the main question (2-3 paragragh)
    3. Create 2-3 specific search queries that would help explore this subtopic in depth
    
    Format your response as a JSON object with this structure:
    {{
        "subtopic_1": {{
            "title": "Title of first subtopic",
           
            "queries": ["Query 1", "Query 2", "Query 3"]
        }},
        "subtopic_2": {{
            "title": "Title of second subtopic",
            "queries": ["Query 1", "Query 2"]
        }}
    }}
    
    Ensure each search query is specific, focused, and likely to return relevant results.
    Include both broad overview queries and specific technical or detailed queries.
    Consider different perspectives, approaches, or dimensions of the topic.
    """

def generate_deep_research_prompt(topic, research_summary, extra_prompt=""):
    return f"""
    ## Comprehensive Doctoral-Level Research Analysis: "{topic}"

    You are to produce an extraordinarily in-depth, interdisciplinary research analysis that meets or exceeds the standards of top-tier academic publications. Your work must demonstrate original insight, critical synthesis, and methodological excellence. Please ensure the following:

    ### 1. Scope and Structure
    - Deliver a minimum of **15,000 words** of substantive, original content.
    - Reference at least **60 peer-reviewed, high-impact sources** from the past 20 years, with foundational works as needed.
    - Organize the work with a detailed table of contents, clear sections, and logically nested subsections.
    - Include multiple **visual conceptual maps** or diagrams illustrating the relationships among key theories, frameworks, or variables.
    - Provide extensive examples and case studies throughout each section.

    ### 2. Systematic Literature Review
    - Conduct a **comprehensive systematic literature review** following PRISMA or equivalent guidelines.
    - Document detailed inclusion/exclusion criteria, search strategies, and data extraction methods.
    - Synthesize findings across **qualitative, quantitative, and mixed-methods** research.
    - Critically assess the strengths, weaknesses, and gaps in the literature.
    - Include a detailed methodology section explaining the review process.

    ### 3. Theoretical and Conceptual Frameworks
    - Identify and analyze at least **12 major theoretical frameworks** or models relevant to the topic.
    - Provide a **detailed historical evolution** of these frameworks over the last 50 years.
    - Examine intersections, complementarities, and tensions among these frameworks.
    - Include specific examples of how each framework has been applied in practice.
    - Discuss the evolution of key concepts and terminology.

    ### 4. Interdisciplinary Integration
    - Integrate perspectives from at least **8 distinct academic disciplines**.
    - Analyze points of convergence/divergence and synthesize interdisciplinary insights.
    - Propose **multiple novel interdisciplinary frameworks** to address gaps.
    - Include specific examples of interdisciplinary research and its impact.
    - Discuss challenges and opportunities in interdisciplinary collaboration.

    ### 5. Methodological Rigor and Innovation
    - Critically evaluate the **methodological approaches** used in the field.
    - Discuss the appropriateness, reliability, and validity of various research designs.
    - Address challenges in data collection, measurement, and analysis.
    - Include detailed examples of methodological innovations.
    - Provide specific recommendations for improving research methods.

    ### 6. Critical Evaluation and Source Appraisal
    - Develop explicit **criteria for assessing source quality, credibility, and bias**.
    - Identify and discuss **systemic biases** and their implications.
    - Analyze and reconcile **contradictory findings** and competing interpretations.
    - Include specific examples of bias in research.
    - Provide detailed recommendations for improving research quality.

    ### 7. Contemporary Debates and Future Directions
    - Examine at least **8 current major debates, controversies, or unresolved questions**.
    - Analyze **emerging trends, technologies, or methodologies** shaping the future.
    - Propose **10 or more specific, actionable directions** for future research.
    - Include detailed case studies of current debates.
    - Provide specific recommendations for addressing each debate.

    ### 8. Practical Applications and Case Studies
    - Discuss **real-world implications** and potential for societal impact.
    - Provide at least **6 detailed case studies** with comprehensive analysis.
    - Analyze barriers to implementation and propose strategies to overcome them.
    - Include specific examples of successful implementations.
    - Provide detailed recommendations for practical application.

    ### 9. Epistemological and Philosophical Foundations
    - Critically examine the **philosophical and epistemological underpinnings**.
    - Discuss how different worldviews shape research questions and methods.
    - Include specific examples of philosophical influences on research.
    - Analyze the impact of different philosophical approaches.
    - Provide recommendations for addressing philosophical challenges.

    ### 10. Ethical, Legal, and Social Considerations
    - Identify at least **6 major ethical issues** and discuss their ramifications.
    - Propose robust **guidelines for ethical conduct** and responsible research.
    - Address legal, cultural, and social dimensions in detail.
    - Include specific examples of ethical challenges.
    - Provide detailed recommendations for ethical research.

    ### 11. Limitations, Reflexivity, and Transparency
    - Provide a **comprehensive analysis of the limitations** of current research.
    - Include a detailed reflexive discussion of potential biases and assumptions.
    - Suggest specific ways to enhance transparency and reproducibility.
    - Include examples of how limitations have been addressed in previous research.
    - Provide detailed recommendations for improving research transparency.

    ### 12. Communication and Engagement
    - Use **domain-specific terminology** with precision and clarity.
    - Ensure all arguments are **evidence-based, logically structured, and critically reasoned**.
    - Include multiple **visuals, tables, or infographics** to aid understanding.
    - Provide detailed explanations of complex concepts.
    - Include specific examples to illustrate key points.

    ### 13. Additional Requirements
    - Include a comprehensive glossary of key terms
    - Provide detailed appendices with supplementary information
    - Include extensive footnotes and references
    - Add cross-references between related sections
    - Provide detailed recommendations for further reading

    ---
    **Research Summary:**  
    {research_summary}

    {extra_prompt}

    **Instructions:**  
    Demonstrate exceptional depth, originality, and scholarly rigor throughout. The analysis should be suitable for publication in a leading academic journal or as a policy white paper. Cite all sources in APA, MLA, or Chicago style as appropriate. Ensure each section contains extensive detail, examples, and analysis. The final output should be comprehensive enough to serve as a definitive resource on the topic.

    """


def get_report_by_type(report_type):
    """Returns the appropriate report generation function based on report type."""
    report_type_mapping = {
        'Research Report': generate_report_prompt,
        'Resource Report': generate_resource_report_prompt,
        'Outline Report': generate_outline_report_prompt,
        'Deep Research': generate_deep_research_prompt,
      #  'Critical Evaluation': generate_critique_prompt,
      #  'Comparative Analysis': generate_comparative_analysis_prompt,
      #  'Meta-Analysis': generate_meta_analysis_prompt
    }
    return report_type_mapping.get(report_type, generate_report_prompt)
