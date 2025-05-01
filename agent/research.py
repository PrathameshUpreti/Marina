import json
from actions.searxng_search import searxng_search
from agent.llm_utils import llm_response, llm_stream_response
from config import Config

from agent.prompt import generate_search_queries_prompt
from agent import prompt
from scrapper.beautysoup import extract_clean_text
from scrapper.pyMupdf import is_pdf_url,extract_pdf_text,process_pdf_url
import requests
import time

CFG = Config()

class Research:
    def __init__(self, question, agent, system_prompt, websocket=None, stream_output=None):
        self.question = question
        self.agent = agent
        self.websocket = websocket
        self.stream_output = stream_output
        self.visited_urls = set()
        self.search_summary = ""
        self.system_prompt = system_prompt
        self.subtopic_data = {}

    def call_agent(self, action):
        messages = [{
            "role": "system",
            "content": self.system_prompt,
        }, {
            "role": "user",
            "content": action,
        }]
        return llm_response(
            model=CFG.fast_llm_model,
            messages=messages,
        )

    def call_agent_stream(self, action):
        messages = [{
            "role": "system",
            "content": self.system_prompt,
        }, {
            "role": "user",
            "content": action,
        }]
        yield from llm_stream_response(
            model=CFG.fast_llm_model,
            messages=messages
        )

    def create_search_queries(self):
        """ Creates the search queries for the given question. """
        result = self.call_agent(generate_search_queries_prompt(self.question))
        
        try:
            # Try to parse as JSON first
            return json.loads(result)
        except json.JSONDecodeError:
            print("JSON parsing failed. Attempting to extract queries from text response.")
            
            # Fallback: Try to extract queries from text
            queries = {}
            query_count = 1
            
            # Look for patterns like "Q1", "Q2", etc.
            lines = result.split('\n')
            for line in lines:
                # Look for lines with Q1, Q2, etc. followed by content
                if ":" in line:
                    parts = line.split(":", 1)
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"').strip("'")
                    
                    # If it starts with Q followed by a number
                    if key.startswith("Q") and len(key) > 1 and key[1:].isdigit():
                        queries[key] = value
                        query_count += 1
            
            # If we couldn't extract any queries using the pattern matching
            if not queries:
                print("Could not extract structured queries, creating dynamic ones")
                queries = {
                    "Q1": f"General overview of {self.question} research trends",
                    "Q2": f"Historical development of {self.question} over past three decades",
                    "Q3": f"Quantitative analysis related to {self.question}",
                    "Q4": f"Case studies on practical applications of {self.question}",
                    "Q5": f"Ethical challenges in {self.question}",
                    "Q6": f"Ethical challenges in{self.question}",
                    "Q7": f"Case studies on practical applications of {self.question}",
                    "Q8": f"{self.question} future",
                    "Q9": f"{self.question} applications",
                    "Q10": f"{self.question} research",
                }
            
            return queries

    def search_single_query(self, query):
        """Runs the search for the given query and extracts clean text from each result."""
        raw_results = searxng_search(query, max_search_result=10)
        processed_results = []
        
        for result in raw_results:
            url = result.get('url')
            try:
                if is_pdf_url(url):
                    # Process PDF with our improved method
                    text = process_pdf_url(url, keep_file=False)
                    result['clean_text'] = text
                else:
                    # Handle regular HTML pages
                    response = requests.get(url, timeout=5)  # Reduced timeout
                    response.raise_for_status()
                    
                    html = response.text
                    text = extract_clean_text(html)
                    
                    # Truncate text if too long
                    if len(text) > 5000:
                        truncated_text = text[:5000]
                        last_period = truncated_text.rfind('.')
                        if last_period > 0:
                            text = truncated_text[:last_period+1]
                        else:
                            text = truncated_text
                    result['clean_text'] = text
            
            except requests.exceptions.Timeout:
                result['clean_text'] = f"Request timed out for: {url}"
            except requests.exceptions.RequestException as e:
                result['clean_text'] = f"Network error: {e}"
            except Exception as e:
                result['clean_text'] = f"Processing error: {e}"
            
            processed_results.append(result)
            # Add a delay between requests to reduce load
            time.sleep(1.0)
            
        return processed_results

    def run_search_summary(self, query):
        """ Runs the search summary for the given query.
        Args: query (str): The query to run the search summary for
        Returns: str: The search summary for the given query
        """
        responses = self.search_single_query(query)
        print(f"Searching for {query}")
        return responses
    
    def search_online(self):
        if not self.search_summary:
            self.search_summary += f"=== MAIN QUESTION: {self.question} ===\n\n"
            search_queries = self.create_search_queries()
            for _, query in search_queries.items():
                search_result = self.run_search_summary(query)
                self.search_summary += \
                f"=Query=:\n{query}\n=Search Result=:\n{search_result}\n================\n"
           
        return self.search_summary

    async def generate_research_report(self, task):
       """Generates a structured research report."""
       research_data = self.search_online()
       report_type_func = prompt.get_report_by_type(task) 
       enhanced_prompt = report_type_func(self.question, research_data, "") + """
    
       Please ensure your report:
       1. Thoroughly covers all subtopics identified in the research
       2. Provides in-depth analysis of each area
       3. Creates a comprehensive, well-structured document
       4. Includes specific examples and evidence from the research
       5. Aims for substantial depth in each section
       """
    
       report_content = self.call_agent(enhanced_prompt)
       return report_content

    def write_report(self, report_type, extra_prompt=""):
        report_type_func = prompt.get_report_by_type(report_type)
        research_data = self.search_online()
        
        # Limit the research data to prevent token limit errors
        # Estimate: 1 token ~= 4 characters for English text
        max_tokens = 150000  # Keep well under the 200k limit
        max_chars = max_tokens * 4
        
        if len(research_data) > max_chars:
            print(f"Truncating research data from {len(research_data)} chars to {max_chars} chars")
            # Try to cut at a logical boundary
            truncated_data = research_data[:max_chars]
            last_boundary = max(
                truncated_data.rfind("================\n"),
                truncated_data.rfind("=Search Result=:\n")
            )
            if last_boundary > max_chars * 0.75:  # Only use boundary if it's reasonably far in
                research_data = research_data[:last_boundary] + "\n[TRUNCATED DUE TO TOKEN LIMITS]"
            else:
                research_data = truncated_data + "\n[TRUNCATED DUE TO TOKEN LIMITS]"
        
        enhanced_prompt = report_type_func(self.question, research_data, extra_prompt) + """

Please ensure your report:
1. Thoroughly covers all subtopics identified in the research
2. Provides in-depth analysis of each area
3. Creates a comprehensive, well-structured document
4. Includes specific examples and evidence from the research
5. Aims for substantial depth in each section
"""
        return self.call_agent(enhanced_prompt)


