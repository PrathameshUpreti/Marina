import json
from actions.searxng_search import searxng_search
from agent.llm_utils import llm_response, llm_stream_response
from config import Config
from agent import prompt


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
        result = self.call_agent(prompt.generate_search_queries_prompt(self.question))
        return json.loads(result)
    
    def identify_subtopics(self):
        """ Identifies subtopics and generates search queries for each. """
        result = self.call_agent(prompt.generate_subtopic_queries_prompt(self.question))
        try:
            return json.loads(result)
        except json.JSONDecodeError as e:
            print(f"Error parsing subtopics JSON: {e}")
            # Extract subtopics manually if JSON parsing fails
            subtopics = {}
            current_subtopic = None
            for line in result.split('\n'):
                if '"subtopic_' in line and ':' in line:
                    current_subtopic = line.strip().split(':')[0].strip().strip('"').strip()
                    subtopics[current_subtopic] = {"queries": []}
                elif '"title"' in line and current_subtopic and ':' in line:
                    subtopics[current_subtopic]["title"] = line.split(':')[1].strip().strip('"').strip(',')
                elif '"queries"' in line and current_subtopic and '[' in line:
                    queries_text = line.split('[')[1].split(']')[0]
                    queries = [q.strip().strip('"').strip(',').strip('"') for q in queries_text.split(',')]
                    subtopics[current_subtopic]["queries"] = queries
            
            return subtopics if subtopics else {"subtopic_1": {"title": "General Information", "queries": [self.question]}}

    def search_single_query(self, query):
        """ Runs the search for the given query. """
        return searxng_search(query, max_search_result=5)

    def run_search_summary(self, query):
        """ Runs the search summary for the given query.
        Args: query (str): The query to run the search summary for
        Returns: str: The search summary for the given query
        """
        responses = self.search_single_query(query)
        print(f"Searching for {query}")
        return responses
    


    def search_online(self):
        """ Conducts the search for the given question.
        Args: None
        Returns: str: The search results for the given question
        """
        if not self.search_summary:
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
       report_content = self.call_agent(report_type_func(self.question, research_data, ""))
       return report_content

       

    def write_report(self, report_type, extra_prompt=""):
        """ Writes the report for the given question.
        Args: 
            report_type (str): Type of report to generate
            extra_prompt (str): Additional instructions for the report
        Returns: 
            Generator: Yields the report content as it's generated
        """
        report_type_func = prompt.get_report_by_type(report_type)
        return self.call_agent(report_type_func(self.question, 
                                           self.search_online(),
                                            extra_prompt))


#########################################
import json
from actions.searxng_search import searxng_search
from agent.llm_utils import llm_response, llm_stream_response
from config import Config
from agent import prompt


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
        result = self.call_agent(prompt.generate_search_queries_prompt(self.question))
        return json.loads(result)
    
    
    def search_single_query(self, query):
        """ Runs the search for the given query. """
        return searxng_search(query, max_search_result=5)

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
       
            try:
                subtopic_result = self.call_agent(prompt.generate_subtopic_queries_prompt(self.question))
                print(f"Subtopic response length: {len(subtopic_result) if subtopic_result else 0}")
                print(f"First 100 characters: {subtopic_result[:100] if subtopic_result else 'Empty'}")
                
                subtopics = json.loads(subtopic_result)
            
                self.search_summary += f"\n\n=== SUBTOPIC EXPLORATION ===\n\n"
            
                for subtopic_id, subtopic_info in subtopics.items():
                    title = subtopic_info.get("title", subtopic_id)
                    self.search_summary += f"\n== SUBTOPIC: {title} ==\n\n"
                
               
                    for query in subtopic_info.get("queries", []):
                        search_result = self.run_search_summary(query)
                        self.search_summary += \
                            f"=Query=:\n{query}\n=Search Result=:\n{search_result}\n----------------\n"
            except Exception as e:
                print(f"Error in subtopic exploration: {e}")
            # Continue without subtopics if there's an error
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
        """ Writes the report for the given question.
        Args: 
            report_type (str): Type of report to generate
            extra_prompt (str): Additional instructions for the report
        Returns: 
            Generator: Yields the report content as it's generated
        """
        report_type_func = prompt.get_report_by_type(report_type)
        return self.call_agent(report_type_func(self.question, 
                                           self.search_online(),
                                            extra_prompt))







import json
from actions.searxng_search import searxng_search
from agent.llm_utils import llm_response, llm_stream_response
from config import Config
from agent import prompt
from scrapper.beautysoup import extract_clean_text
from scrapper.pyMupdf import is_pdf_url,extract_pdf_text,process_pdf_url
import requests


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
        result = self.call_agent(prompt.generate_search_queries_prompt(self.question))
        return json.loads(result)
    
    def search_single_query(self, query):
        """Runs the search for the given query and extracts clean text from each result."""
        raw_results = searxng_search(query, max_search_result=3)
        processed_results = []
        for result in raw_results:
            url = result.get('url')
            try:
                if is_pdf_url(url):
                    text = process_pdf_url(url)
                else:
                    response = requests.get(url, timeout=10)
                    html = response.text
                    text = extract_clean_text(html)
                
                result['clean_text'] = text[:3000] 
            except Exception as e:
                result['clean_text'] = f"Failed to extract: {e}"
            processed_results.append(result)  
        return processed_results

    
    
    
   # def search_single_query(self, query):
    #    """ Runs the search for the given query. """
     #   return searxng_search(query, max_search_result=5)

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
        enhanced_prompt = report_type_func(self.question, self.search_online(), extra_prompt) + """
    
    Please ensure your report:
    1. Thoroughly covers all subtopics identified in the research
    2. Provides in-depth analysis of each area
    3. Creates a comprehensive, well-structured document
    4. Includes specific examples and evidence from the research
    5. Aims for substantial depth in each section
    """
        return self.call_agent(enhanced_prompt)


