from pathlib import Path
import re
import struct
import textwrap
import unittest
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree

from tests.site_audit import parse_html


REPO_ROOT = Path(__file__).parents[1]
SITE_ROOT = REPO_ROOT / "site"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "pages.yml"
OG_IMAGE_URL = "https://jb-cho55.github.io/portfolio/assets/og-card.png"
CANONICALS = {
    "index.html": "https://jb-cho55.github.io/portfolio/",
    "artifacts/black-box/index.html": (
        "https://jb-cho55.github.io/portfolio/artifacts/black-box/"
    ),
    "artifacts/carmaker/index.html": (
        "https://jb-cho55.github.io/portfolio/artifacts/carmaker/"
    ),
    "artifacts/bootloader/index.html": (
        "https://jb-cho55.github.io/portfolio/artifacts/bootloader/"
    ),
}


def uncommented_yaml_lines(path):
    lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        quote = None
        escaped = False
        content = []
        for character in raw_line:
            if escaped:
                content.append(character)
                escaped = False
                continue
            if character == "\\" and quote == '"':
                content.append(character)
                escaped = True
                continue
            if character in {"'", '"'}:
                if quote == character:
                    quote = None
                elif quote is None:
                    quote = character
            if character == "#" and quote is None:
                break
            content.append(character)
        line = "".join(content).rstrip()
        if line.strip():
            lines.append(line)
    return lines


def yaml_block(lines, key, indent):
    header = f"{' ' * indent}{key}:"
    matches = [index for index, line in enumerate(lines) if line == header]
    if len(matches) != 1:
        raise AssertionError(
            f"Expected one YAML block named {key}, found {len(matches)}"
        )
    start = matches[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        current_indent = len(lines[index]) - len(lines[index].lstrip())
        if current_indent <= indent:
            end = index
            break
    return lines[start:end]


def flat_yaml_mapping(lines, child_indent):
    result = {}
    for line in lines[1:]:
        indent = len(line) - len(line.lstrip())
        if indent != child_indent:
            continue
        key, separator, value = line.strip().partition(":")
        if separator and value.strip():
            result[key] = value.strip()
    return result


def workflow_actions(job_lines):
    return {
        match.group(1)
        for line in job_lines
        if (match := re.fullmatch(r"\s+uses:\s*(\S+)", line))
    }


def numbered_markdown_steps(markdown, heading):
    section = markdown.split(heading, 1)[1]
    next_heading = re.search(r"(?m)^## ", section)
    if next_heading:
        section = section[: next_heading.start()]
    matches = list(re.finditer(r"(?m)^(\d+)\. .+$", section))
    numbers = [int(match.group(1)) for match in matches]
    if numbers != list(range(1, len(numbers) + 1)):
        raise AssertionError(f"Markdown steps are out of order: {numbers}")
    steps = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        steps[int(match.group(1))] = section[match.start() : end].strip()
    return steps


def powershell_code(step):
    blocks = re.findall(
        r"(?ms)^\s*```powershell\s*$\n(.*?)^\s*```\s*$",
        step,
    )
    return "\n".join(textwrap.dedent(block).strip() for block in blocks)


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.documents = {
            route: parse_html(SITE_ROOT / route) for route in CANONICALS
        }

    def test_pages_have_unique_titles_and_descriptions(self):
        titles = []
        descriptions = []
        for route, document in self.documents.items():
            with self.subTest(route=route):
                description_tags = [
                    attrs
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("name") == "description"
                ]
                self.assertTrue(document.title.strip())
                self.assertEqual(len(description_tags), 1)
                self.assertTrue(description_tags[0].get("content", "").strip())
                titles.append(document.title.strip())
                descriptions.append(description_tags[0]["content"].strip())
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_each_page_has_matching_canonical_and_open_graph_urls(self):
        open_graph_titles = []
        open_graph_descriptions = []
        for route, expected_url in CANONICALS.items():
            document = self.documents[route]
            with self.subTest(route=route):
                canonical = [
                    attrs.get("href")
                    for tag, attrs in document.tags
                    if tag == "link" and attrs.get("rel") == "canonical"
                ]
                og_url = [
                    attrs.get("content")
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("property") == "og:url"
                ]
                og_image = [
                    attrs.get("content")
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("property") == "og:image"
                ]
                og_title = [
                    attrs.get("content")
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("property") == "og:title"
                ]
                og_description = [
                    attrs.get("content")
                    for tag, attrs in document.tags
                    if tag == "meta" and attrs.get("property") == "og:description"
                ]
                self.assertEqual(canonical, [expected_url])
                self.assertEqual(og_url, [expected_url])
                self.assertEqual(og_image, [OG_IMAGE_URL])
                self.assertEqual(urlsplit(og_image[0]).scheme, "https")
                self.assertTrue(urlsplit(og_image[0]).netloc)
                self.assertEqual(len(og_title), 1)
                self.assertTrue(og_title[0].strip())
                self.assertEqual(og_title[0], document.title.strip())
                self.assertEqual(len(og_description), 1)
                self.assertTrue(og_description[0].strip())
                open_graph_titles.append(og_title[0])
                open_graph_descriptions.append(og_description[0])
        self.assertEqual(len(open_graph_titles), len(set(open_graph_titles)))
        self.assertEqual(
            len(open_graph_descriptions), len(set(open_graph_descriptions))
        )

    def test_json_ld_describes_person_and_authored_case_studies(self):
        home = self.documents["index.html"]
        self.assertEqual(len(home.json_ld), 1)
        self.assertEqual(home.json_ld[0].get("@type"), "Person")
        self.assertEqual(home.json_ld[0].get("name"), "조정빈")
        self.assertEqual(home.json_ld[0].get("url"), CANONICALS["index.html"])

        for route, canonical in CANONICALS.items():
            if route == "index.html":
                continue
            document = self.documents[route]
            with self.subTest(route=route):
                self.assertEqual(len(document.json_ld), 1)
                article = document.json_ld[0]
                self.assertEqual(article.get("@type"), "TechArticle")
                self.assertEqual(article.get("url"), canonical)
                self.assertEqual(
                    article.get("author"),
                    {"@type": "Person", "name": "조정빈"},
                )

    def test_discovery_files_publish_exactly_the_four_canonical_routes(self):
        sitemap = SITE_ROOT / "sitemap.xml"
        root = ElementTree.parse(sitemap).getroot()
        namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {
            node.text for node in root.findall("sitemap:url/sitemap:loc", namespace)
        }
        self.assertEqual(locations, set(CANONICALS.values()))

        robots = (SITE_ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /portfolio/", robots)
        self.assertIn(
            "Sitemap: https://jb-cho55.github.io/portfolio/sitemap.xml",
            robots,
        )
        self.assertTrue((SITE_ROOT / ".nojekyll").is_file())

    def test_open_graph_png_is_1200_by_630(self):
        image = SITE_ROOT / "assets" / "og-card.png"
        data = image.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(data[12:16], b"IHDR")
        self.assertEqual(struct.unpack(">II", data[16:24]), (1200, 630))

    def test_nested_404_resources_and_home_resolve_at_portfolio_root(self):
        document = parse_html(SITE_ROOT / "404.html")
        nested_missing_url = (
            "https://jb-cho55.github.io/portfolio/artifacts/missing/"
        )
        favicon = next(
            attrs["href"]
            for tag, attrs in document.tags
            if tag == "link" and attrs.get("rel") == "icon"
        )
        stylesheet = next(
            attrs["href"]
            for tag, attrs in document.tags
            if tag == "link" and attrs.get("rel") == "stylesheet"
        )
        home_links = [
            attrs["href"]
            for tag, attrs in document.tags
            if tag == "a"
            and (
                "identity" in attrs.get("class", "").split()
                or "text-link" in attrs.get("class", "").split()
            )
        ]
        self.assertEqual(
            urljoin(nested_missing_url, favicon),
            "https://jb-cho55.github.io/portfolio/assets/favicon.svg",
        )
        self.assertEqual(
            urljoin(nested_missing_url, stylesheet),
            "https://jb-cho55.github.io/portfolio/assets/css/site.css",
        )
        self.assertEqual(len(home_links), 2)
        self.assertEqual(
            {urljoin(nested_missing_url, href) for href in home_links},
            {"https://jb-cho55.github.io/portfolio/"},
        )


class DeploymentWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.lines = uncommented_yaml_lines(WORKFLOW)
        self.events = yaml_block(self.lines, "on", 0)
        self.global_permissions = yaml_block(self.lines, "permissions", 0)
        self.concurrency = yaml_block(self.lines, "concurrency", 0)
        self.jobs = yaml_block(self.lines, "jobs", 0)
        self.test_job = yaml_block(self.jobs, "test", 2)
        self.deploy_job = yaml_block(self.jobs, "deploy", 2)

    def test_only_main_push_can_reach_deploy_job(self):
        events = "\n".join(self.events)
        self.assertRegex(events, r"(?m)^  push:$")
        self.assertRegex(events, r"(?m)^    branches:$")
        self.assertRegex(events, r"(?m)^      - main$")
        self.assertNotRegex(events, r"(?m)^  pull_request:$")
        job_names = {
            match.group(1)
            for line in self.jobs[1:]
            if (match := re.fullmatch(r"  ([A-Za-z0-9_-]+):", line))
        }
        self.assertEqual(job_names, {"test", "deploy"})
        deploy = "\n".join(self.deploy_job)
        self.assertRegex(deploy, r"(?m)^    needs: test$")
        self.assertRegex(
            deploy,
            r"(?m)^    if: github\.event_name == 'push' && "
            r"github\.ref == 'refs/heads/main'$",
        )

    def test_expected_actions_and_site_artifact_are_in_the_correct_jobs(self):
        self.assertEqual(
            workflow_actions(self.test_job),
            {"actions/checkout@v7", "actions/setup-python@v7"},
        )
        self.assertIn(
            "run: python -B -m unittest discover -s tests -v",
            {line.strip() for line in self.test_job},
        )
        self.assertEqual(
            workflow_actions(self.deploy_job),
            {
                "actions/checkout@v7",
                "actions/configure-pages@v6",
                "actions/upload-pages-artifact@v5",
                "actions/deploy-pages@v5",
            },
        )
        deploy = "\n".join(self.deploy_job)
        self.assertRegex(
            deploy,
            r"(?ms)^\s+- name: Upload site artifact\s+"
            r"uses: actions/upload-pages-artifact@v5\s+"
            r"with:\s+path: site/$",
        )

    def test_workflow_uses_only_the_required_permissions(self):
        self.assertEqual(
            flat_yaml_mapping(self.global_permissions, 2),
            {"contents": "read"},
        )
        deploy_permissions = yaml_block(self.deploy_job, "permissions", 4)
        self.assertEqual(
            flat_yaml_mapping(deploy_permissions, 6),
            {
                "pages": "write",
                "id-token": "write",
                "contents": "read",
            },
        )

    def test_pages_deployments_are_not_cancelled_in_progress(self):
        self.assertEqual(
            flat_yaml_mapping(self.concurrency, 2).get("cancel-in-progress"),
            "false",
        )

    def test_readme_orders_push_before_pages_source_mutation(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        steps = numbered_markdown_steps(readme, "## 게시 절차")
        self.assertEqual(set(steps), {1, 2, 3, 4, 5, 6})
        capture = powershell_code(steps[1])
        remote_guard = powershell_code(steps[2])
        guarded_push = powershell_code(steps[3])
        pages_source = powershell_code(steps[4])

        self.assertRegex(capture, r"(?m)^\$releaseSha = git rev-parse HEAD$")
        self.assertIn("git ls-remote origin refs/heads/main", remote_guard)
        self.assertIn(
            '661b9d5186028318a1f181f4f7b0e8a822f1da63', remote_guard
        )
        self.assertRegex(remote_guard, r"\$remoteMain\s+-ne\s+\$expectedOldMain")
        self.assertIn(
            "git push --force-with-lease=refs/heads/main:"
            "661b9d5186028318a1f181f4f7b0e8a822f1da63 "
            "origin HEAD:refs/heads/main",
            guarded_push,
        )
        self.assertRegex(guarded_push, r"git rev-parse HEAD\) -ne \$releaseSha")
        self.assertIn(
            "gh api --method PUT repos/jb-cho55/portfolio/pages "
            "-f build_type=workflow",
            pages_source,
        )
        self.assertNotIn(
            "build_type=workflow",
            "\n".join(steps[index] for index in (1, 2, 3)),
        )

    def test_readme_binds_workflow_and_deployment_checks_to_release_sha(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        steps = numbered_markdown_steps(readme, "## 게시 절차")
        workflow_check = powershell_code(steps[5])
        deployment_check = powershell_code(steps[6])

        run_list = next(
            line for line in workflow_check.splitlines() if "gh run list" in line
        )
        self.assertIn("--commit $releaseSha", run_list)
        self.assertIn("--json databaseId,headSha", run_list)
        self.assertRegex(workflow_check, r"\$run\.headSha\s+-ne\s+\$releaseSha")
        self.assertIn("gh run watch $run.databaseId --exit-status", workflow_check)
        self.assertIn("gh run view $run.databaseId --log-failed", workflow_check)
        self.assertRegex(
            workflow_check,
            r'\$result\.status\s+-ne\s+"completed"',
        )
        self.assertIn("gh api repos/jb-cho55/portfolio/pages", deployment_check)
        deployed_routes = set(
            re.findall(
                r'https://jb-cho55\.github\.io/portfolio/(?:artifacts/(?:black-box|carmaker|bootloader)/)?',
                deployment_check,
            )
        )
        self.assertEqual(deployed_routes, set(CANONICALS.values()))


if __name__ == "__main__":
    unittest.main()
