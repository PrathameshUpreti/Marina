
@app.route("/reason", methods=["POST"])
def reason():
    try:
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
        data =request.get_json(force=True)
        if data is None:
            return jsonify({"error": "Invalid JSON format"}), 400
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Empty query"}), 400
        research_agent = Research(question=query, agent="Default Agent", system_prompt="")
        search_results = research_agent.search_online()
        if not search_results:
            return jsonify({"error": "No response from the model"}), 500
        report_type = "Research Report"
        report_generator = research_agent.write_report(report_type, "")
        report_content = ""

        for chunk in report_generator:
            report_content += chunk

        if not report_content:
            return jsonify({"error": "Failed to generate report content"}), 500

        return jsonify({"response": report_content})
    except Exception as e:
        print("Error in /reason endpoint:", str(e))
        return jsonify({"error": str(e)}), 500