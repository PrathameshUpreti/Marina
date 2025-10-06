import sys
import asyncio
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.llm_search import llm_serch_function,get_llm
from agent.research import Research 


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type"]}})



@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "").strip()
    model_provider = data.get('model', 'openai') 

    if not query:
        return jsonify({"error": "Empty query"}), 400

    result = llm_serch_function(query,model_provider=model_provider)
    return jsonify({"response": result})

@app.route("/reason", methods=["POST"])
def reason():
    try:
        print("Headers:", request.headers)
        print("Data (raw):", request.data)
        data = request.get_json(silent=True)
        print("Parsed JSON:", data)
        if data is None:
            data = request.get_json(force=True)
            if data is None:
                return jsonify({"error": "Empty or invalid JSON in request body"}), 400
        query = data.get("query", "").strip()
        print("Query:", query)
        
        if not query:
            return jsonify({"error": "Empty query"}), 400

        try:
            research_agent = Research(question=query, agent="Default Agent", system_prompt="")
            search_results = research_agent.search_online()
            if not search_results:
                return jsonify({"error": "No search results found"}), 500
            
            report_type = "Research Report"
            try:
                report_content = research_agent.write_report(report_type, "")
                print("Report content:", report_content[:100] if report_content else "None")  # Print just the first 100 chars
            except Exception as e:
                print(f"Error generating report: {str(e)}")
                return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

            if not report_content:
                return jsonify({"error": "Failed to generate report content"}), 500

            return jsonify({"response": report_content})
        except Exception as e:
            print(f"Error in research process: {str(e)}")
            return jsonify({"error": f"Research error: {str(e)}"}), 500
    except Exception as e:
        print("Error in /reason endpoint:", str(e))
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)