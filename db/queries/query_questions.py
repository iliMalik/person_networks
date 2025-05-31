from typing import List
from models.pyd_models import Question
from db.graph_driver import neo4j_driver
import pandas as pd
from db.queries.query_responses import responses_session_id
from utils.question_definitions import questions_df


def questions_get_all() -> List[Question]:
    query = """
            MATCH (q:Question)
            RETURN q.question_id AS question_id, q.question_text AS question_text
            ORDER BY q.text
        """

    with neo4j_driver.get_driver().session() as session:
        result = session.run(query)
        return [Question(question_id=record["question_id"], question_text=record["question_text"]) for record in result]


def get_question_sections() -> pd.DataFrame:
    """
    Fetch questions and their sections (allowing multiple sections per question).

    Returns:
        DataFrame with columns: question_id, section_id, section_name
    """
    query = """
    MATCH (s:Section)-[r:HAS_QUESTION]->(q:Question)
    RETURN q.question_id, s.section_id, s.section_name AS section_name
    """
    try:
        with neo4j_driver.get_driver().session() as session:
            result = session.run(query)
            data = [
                {
                    "question_id": str(record["q.question_id"]),
                    "section_id": str(record["s.section_id"]),
                    "section_name": record["section_name"]
                }
                for record in result
            ]
            df = pd.DataFrame(data, columns=["question_id", "section_id", "section_name"])

            return df
    except Exception as e:
        print(f"Error fetching question sections: {e}")
        return pd.DataFrame(columns=["question_id", "section_id", "section_name"])



def get_yes_Ids(session_id: str):
    # Get responses
    responses_list = responses_session_id(session_id)


    # Initialize data for DataFrame
    data = []

    for response in responses_list:
        for question_id, answer in response.answers.items():
            data.append({"question_id": question_id, "answer": answer})



    # Create DataFrame
    df_responses = pd.DataFrame(data)
    # df_responses = pd.DataFrame(data, columns=["question_id", "question_text", "answer"])

    # Merge with questions_df to get IDs
    df_merged = pd.merge(
        df_responses,
        questions_df[["ID", "question_id"]],
        on="question_id",
        how="left"
    )

    # Filter for YES responses and drop missing IDs
    yes_ids = df_merged[df_merged["answer"] == "YES"]["ID"].dropna().astype(int).tolist()

    return yes_ids

