
def get_all_questions(tx, section_id: str = None):
    """
    Fetch all questions; if section_id is given, fetch questions only for that section.
    """
    if section_id:
        query = """
        MATCH (q:Question)-[:PART_OF]->(s:Section {id: $section_id})
        RETURN q ORDER BY q.text
        """
        result = tx.run(query, section_id=section_id)
    else:
        query = """
        MATCH (q:Question)
        RETURN q ORDER BY q.text
        """
        result = tx.run(query)
    return [record["q"] for record in result]

def get_question_by_id(tx, question_id: str):
    """
    Fetch a question node by its UUID.
    """
    query = "MATCH (q:Question {id: $question_id}) RETURN q"
    result = tx.run(query, question_id=question_id)
    return result.single()