import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_query_db(asyn_test_client):
    """Test function for the db query endpoint using natural language"""

    test_question = "How many customers signed up yesterday?"
    mock_sql_query = (
        "SELECT COUNT(*) FROM customers WHERE signup_date = CURRENT_DATE - 1;"
    )
    mock_response_content = "42 customers signed up yesterday."

    mock_response = MagicMock()
    mock_response.content = mock_response_content

    with patch(
        "src.agent.controller.sql_chain", autospec=True
    ) as mock_sql_chain, patch(
        "src.agent.controller.response_chain", autospec=True
    ) as mock_response_chain:

        mock_sql_chain.invoke = MagicMock(return_value=mock_sql_query)
        mock_response_chain.invoke = MagicMock(return_value=mock_response)

        response = await asyn_test_client.post(
            "/agent/query", json={"question": test_question}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["answer"] == mock_response_content.strip()
        assert data["query"] == mock_sql_query

        mock_sql_chain.invoke.assert_called_once_with({"question": test_question})
        mock_response_chain.invoke.assert_called_once_with(
            {"question": test_question, "query": mock_sql_query}
        )


@pytest.mark.asyncio
async def test_query_db_internal_server_error(asyn_test_client):
    test_question = "Trigger an internal error"

    with patch("src.agent.controller.sql_chain") as mock_sql_chain:
        mock_sql_chain.invoke.side_effect = Exception("Something went wrong")

        response = await asyn_test_client.post(
            "/agent/query", json={"question": test_question}
        )

        assert response.status_code == 500
        assert response.json() == {"detail": "Something went wrong"}
