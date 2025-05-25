


def fetch_all_questions(tx):
    query = """
        MATCH (q:Question)
        RETURN q.question_id AS question_id, q.text AS text
        ORDER BY q.text
    """
    result = tx.run(query)
    return [{"question_id": record["question_id"], "text": record["text"]} for record in result]