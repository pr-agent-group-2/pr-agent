#Currently doing API calls - wrong !


import unittest
import asyncio
from unittest.mock import AsyncMock, patch
from pr_agent.tools.ticket_pr_compliance_check import extract_tickets, extract_and_cache_pr_tickets
from pr_agent.git_providers.github_provider import GithubProvider


class TestTicketCompliance(unittest.TestCase):

    @patch.object(GithubProvider, 'get_user_description', return_value="Fixes #1 and relates to #2")
    @patch.object(GithubProvider, '_parse_issue_url', side_effect=lambda url: ("WonOfAKind/KimchiBot", int(url.split('#')[-1])))
    @patch.object(GithubProvider, 'repo_obj')
    async def test_extract_tickets(self, mock_repo, mock_parse_issue_url, mock_user_desc):
        """
        Test extract_tickets() to ensure it extracts tickets correctly
        and fetches their content.
        """
        github_provider = GithubProvider()
        github_provider.repo = "WonOfAKind/KimchiBot"
        github_provider.base_url_html = "https://github.com"

        # Mock issue retrieval
        mock_issue = AsyncMock()
        mock_issue.number = 1
        mock_issue.title = "Sample Issue"
        mock_issue.body = "This is a test issue body."
        mock_issue.labels = ["bug", "high priority"]

        # Mock repo object
        mock_repo.get_issue.return_value = mock_issue

        tickets = await extract_tickets(github_provider)

        # Verify tickets were extracted correctly
        self.assertIsInstance(tickets, list)
        self.assertGreater(len(tickets), 0, "Expected at least one ticket!")

        # Verify ticket structure
        first_ticket = tickets[0]
        self.assertIn("ticket_id", first_ticket)
        self.assertIn("ticket_url", first_ticket)
        self.assertIn("title", first_ticket)
        self.assertIn("body", first_ticket)
        self.assertIn("labels", first_ticket)

        print("\n Test Passed: extract_tickets() successfully retrieved ticket info!")

    @patch.object(GithubProvider, 'get_user_description', return_value="Fixes #1 and relates to #2")
    @patch.object(GithubProvider, '_parse_issue_url', side_effect=lambda url: ("WonOfAKind/KimchiBot", int(url.split('#')[-1])))
    @patch.object(GithubProvider, 'repo_obj')
    async def test_extract_and_cache_pr_tickets(self, mock_repo, mock_parse_issue_url, mock_user_desc):
        """
        Test extract_and_cache_pr_tickets() to ensure tickets are extracted and cached correctly.
        """
        github_provider = GithubProvider()
        github_provider.repo = "WonOfAKind/KimchiBot"
        github_provider.base_url_html = "https://github.com"

        vars = {}  # Simulate the dictionary to store results

        # Mock issue retrieval
        mock_issue = AsyncMock()
        mock_issue.number = 1
        mock_issue.title = "Sample Issue"
        mock_issue.body = "This is a test issue body."
        mock_issue.labels = ["bug", "high priority"]

        # Mock repo object
        mock_repo.get_issue.return_value = mock_issue

        # Run function
        await extract_and_cache_pr_tickets(github_provider, vars)

        # Ensure tickets are cached
        self.assertIn("related_tickets", vars)
        self.assertIsInstance(vars["related_tickets"], list)
        self.assertGreater(len(vars["related_tickets"]), 0, "Expected at least one cached ticket!")

        print("\n Test Passed: extract_and_cache_pr_tickets() successfully cached ticket data!")

    @patch.object(GithubProvider, 'fetch_sub_issues', return_value={'sub-issue-1', 'sub-issue-2'})
    def test_fetch_sub_issues(self, mock_fetch):
        github_provider = GithubProvider()
        issue_url = "https://github.com/WonOfAKind/KimchiBot/issues/1"
        result = github_provider.fetch_sub_issues(issue_url)
        self.assertIsInstance(result, set)
        self.assertGreater(len(result), 0)

    @patch.object(GithubProvider, 'fetch_sub_issues', return_value=set())
    def test_fetch_sub_issues_with_no_results(self, mock_fetch):
        github_provider = GithubProvider()
        issue_url = "https://github.com/qodo-ai/pr-agent/issues/1499"
        result = github_provider.fetch_sub_issues(issue_url)
        self.assertIsInstance(result, set)
        self.assertEqual(len(result), 0)



if __name__ == "__main__":
    asyncio.run(unittest.main())





