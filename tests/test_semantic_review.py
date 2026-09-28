"""Offline tests only: every Jev call uses a fake transport."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("semantic_review", ROOT / "scripts" / "semantic_review.py")
reviewer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reviewer)
FIXTURE = ROOT / "tests" / "fixtures" / "semantic_review.json"


def sample():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class FakeTransport:
    def __init__(self, choice="yes", confidence=0.96, noul=0.96, evidence=0.96):
        self.choice, self.confidence = choice, confidence
        self.noul, self.evidence = noul, evidence
        self.calls = []

    def __call__(self, request, api_key, timeout):
        self.calls.append(copy.deepcopy(request))
        answers = {}
        for key, question in request["questions"].items():
            if question["type"] == "noul":
                answers[key] = {"type": "noul", "noul": self.evidence if key.endswith("_evidence") else self.noul}
            else:
                probabilities = {option: 0.02 for option in question["criteria"]}
                probabilities[self.choice] = 0.96
                answers[key] = {"type": "choice", "choice": self.choice,
                                "confidence": self.confidence, "probabilities": probabilities}
        return {"model": reviewer.MODEL, "answers": answers,
                "usage": {"input_tokens": 400, "output_tokens": 30}}


def run_jev(data=None, transport=None, **options):
    return reviewer.review(sample() if data is None else data, mode="jev", allow_external=True,
                           environ={"TYPESAFE_API_KEY": "test-only-dummy"},
                           transport=transport or FakeTransport(), **options)


class SemanticReviewTests(unittest.TestCase):
    def test_local_never_reads_credentials_or_calls_network(self):
        class ForbiddenEnvironment(dict):
            def get(self, *args):
                raise AssertionError("local mode read environment")
        fake = FakeTransport()
        result = reviewer.review(sample(), environ=ForbiddenEnvironment(), transport=fake)
        self.assertEqual(result["status"], "local_checks_passed")
        self.assertEqual(result["semantic_review"], "not_performed")
        self.assertFalse(result["request_attempted"])
        self.assertFalse(fake.calls)

    def test_external_mode_needs_both_switches(self):
        fake = FakeTransport()
        result = reviewer.review(sample(), mode="jev", environ={"TYPESAFE_API_KEY": "dummy"}, transport=fake)
        self.assertEqual(result["code"], "external_not_allowed")
        self.assertFalse(fake.calls)
        local = reviewer.review(sample(), allow_external=True, transport=fake)
        self.assertEqual(local["provider"], "local")
        self.assertFalse(fake.calls)

    def test_missing_key_fails_instead_of_falling_back(self):
        fake = FakeTransport()
        for env in ({}, {"TYPESAFE_API_KEY": "  "}, {"JEV_API_KEY": "not-supported"}):
            result = reviewer.review(sample(), mode="jev", allow_external=True, environ=env, transport=fake)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["code"], "missing_api_key")
        self.assertFalse(fake.calls)

    def test_source_dialogue_and_speaker_are_exact(self):
        for field, value in (("text", "请坐吧。"), ("speaker", "B")):
            data = sample()
            data["deliverable"]["dialogue"][0][field] = value
            result = run_jev(data)
            self.assertEqual(result["status"], "failed")
            self.assertFalse(result["request_attempted"])
            self.assertIn("dialogue_changed", [issue["code"] for issue in result["checks"]])

    def test_missing_and_unsubstantiated_dialogue(self):
        data = sample()
        data["deliverable"]["dialogue"] = []
        self.assertEqual(reviewer.review(data)["checks"][0]["code"], "dialogue_missing")
        data = sample()
        data["deliverable"]["text"] = data["deliverable"]["text"].replace("坐吧。", "")
        self.assertIn("declared_dialogue_not_in_deliverable", [x["code"] for x in reviewer.review(data)["checks"]])
        data = sample()
        data["source"]["text"] = "没有这句对白。"
        self.assertEqual(reviewer.review(data)["checks"][0]["code"], "source_dialogue_not_in_source")

    def test_time_intervals_reject_nan_boolean_reverse_and_overrun(self):
        for start, end in ((float("nan"), 2), (True, 2), (2, 1), (-1, 2), (0, float("inf")), (0, 9), (0, 10**1000)):
            data = sample()
            data["deliverable"]["segments"][0].update(start_seconds=start, end_seconds=end)
            result = reviewer.review(data)
            self.assertEqual(result["status"], "failed", (start, end))
        data = sample()
        data["deliverable"]["dialogue"][0].pop("end_seconds")
        self.assertEqual(reviewer.review(data)["status"], "failed")

    def test_overlap_is_not_invented_as_a_failure(self):
        data = sample()
        data["deliverable"]["segments"].append({"start_seconds": 1, "end_seconds": 3})
        self.assertEqual(reviewer.review(data)["status"], "local_checks_passed")

    def test_invalid_inputs_are_rejected_without_network(self):
        cases = [None, {}, {**sample(), "image_url": "https://example.invalid/x.png"}]
        bad = sample()
        bad["observed_evidence"] = [{"id": "frame", "type": "image", "text": "not pixels"}]
        cases.append(bad)
        bad = sample()
        bad["source"]["text"] = "data:image/png;base64,private"
        cases.append(bad)
        bad = sample()
        bad["locked_facts"][0]["target"] = "absent"
        cases.append(bad)
        bad = sample()
        bad["locked_facts"] *= 13
        cases.append(bad)
        for data in cases:
            fake = FakeTransport()
            result = reviewer.review(data, mode="jev", allow_external=True,
                                     environ={"TYPESAFE_API_KEY": "dummy"}, transport=fake)
            self.assertEqual(result["status"], "failed")
            self.assertFalse(fake.calls)

    def test_quoted_location_must_be_real_and_unique(self):
        data = sample()
        data["locked_facts"][0]["excerpt"] = "not present"
        self.assertEqual(run_jev(data)["code"], "excerpt_not_in_target")
        data = sample()
        data["deliverable"]["text"] *= 2
        self.assertEqual(run_jev(data)["code"], "ambiguous_excerpt")

    def test_single_batch_independent_questions(self):
        data = sample()
        data["locked_facts"].append({"id": "weather", "text": "日间干燥", "target": "deliverable", "severity": "minor", "question_type": "noul"})
        fake = FakeTransport()
        result = run_jev(data, fake)
        self.assertEqual(result["status"], "no_issue_detected")
        self.assertEqual(len(fake.calls), 1)
        self.assertEqual(len(fake.calls[0]["questions"]), 3)
        self.assertNotIn("answers", fake.calls[0]["state"])
        self.assertEqual(result["usage"]["input_tokens"], 400)
        self.assertEqual(result["provider"], "typesafe")

    def test_unknown_low_confidence_and_minor_failures_require_review(self):
        for fake in (FakeTransport("insufficient_evidence"), FakeTransport("no", confidence=0.60)):
            self.assertEqual(run_jev(transport=fake)["status"], "review_required")
        data = sample()
        data["locked_facts"][0]["severity"] = "minor"
        self.assertEqual(run_jev(data, FakeTransport("no"))["status"], "review_required")

    def test_only_grounded_major_no_becomes_candidate_not_approval(self):
        result = run_jev(transport=FakeTransport("no"))
        self.assertEqual(result["status"], "candidate_repair")
        self.assertEqual(result["findings"][0]["location"], "/deliverable/text")
        self.assertEqual(len(result["findings"][0]["character_range"]), 2)
        data = sample()
        data["locked_facts"][0].pop("excerpt")
        self.assertEqual(run_jev(data, FakeTransport("no"))["status"], "review_required")

    def test_noul_unknown_guard_is_separate_from_no(self):
        data = sample()
        data["locked_facts"][0]["question_type"] = "noul"
        for evidence, noul, expected in ((0.2, 0.01, "review_required"), (0.98, 0.5, "review_required"), (0.98, 0.02, "candidate_repair"), (0.98, 0.98, "no_issue_detected")):
            self.assertEqual(run_jev(data, FakeTransport(noul=noul, evidence=evidence))["status"], expected)

    def test_observation_text_does_not_become_pixel_input(self):
        data = sample()
        data["observed_evidence"] = [{"id": "frame1", "type": "text", "text": "仅见一张静帧，无法确认车流是否运动。"}]
        data["locked_facts"][0].update(target="frame1")
        data["locked_facts"][0].pop("excerpt")
        fake = FakeTransport("insufficient_evidence")
        result = run_jev(data, fake)
        self.assertEqual(result["status"], "review_required")
        self.assertEqual(fake.calls[0]["state"]["checks"][0]["target_kind"], "text_observation")

    def test_errors_do_not_leak_key_input_or_provider_body(self):
        for status in (401, 403, 422, 429, 500, 529):
            def fail(*args):
                raise urllib.error.HTTPError(reviewer.ENDPOINT, status, "private-body", {}, io.BytesIO(b"private-provider-body"))
            result = run_jev(transport=fail)
            self.assertEqual(result["http_status"], status)
            self.assertEqual(result["status"], "failed")
            self.assertNotIn("private", json.dumps(result))
            self.assertNotIn("test-only-dummy", json.dumps(result))
        for error in (TimeoutError("private"), urllib.error.URLError("private")):
            def fail(*args):
                raise error
            self.assertEqual(run_jev(transport=fail)["code"], "transport_error")

    def test_refusal_malformed_wrong_model_and_invalid_probabilities(self):
        fake = FakeTransport()
        good = fake(reviewer.build_request(sample()), "dummy", 2)
        responses = [{"refusal": "private"}, {"error": "private"}, "not an object", {**good, "model": "another-model"}, {**good, "answers": {}}]
        for change in ({"confidence": float("nan")}, {"choice": "refuse"}, {"probabilities": {"yes": 2, "no": -1, "insufficient_evidence": 0}}):
            bad = copy.deepcopy(good)
            bad["answers"]["fact_0"].update(change)
            responses.append(bad)
        bad = copy.deepcopy(good)
        bad["usage"]["input_tokens"] = True
        responses.append(bad)
        for response in responses:
            result = run_jev(transport=lambda *args: response)
            self.assertEqual(result["status"], "failed")
            self.assertNotIn("private", json.dumps(result))

    def test_report_does_not_copy_private_text_or_identifier(self):
        data = sample()
        data["locked_facts"][0]["id"] = "private_case"
        result = run_jev(data)
        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(data["source"]["text"], serialized)
        self.assertNotIn(data["locked_facts"][0]["text"], serialized)
        self.assertNotIn("private_case", serialized)
        self.assertNotIn("test-only-dummy", serialized)

    def test_empty_review_and_oversize_never_send(self):
        data, fake = sample(), FakeTransport()
        data["locked_facts"] = []
        self.assertEqual(run_jev(data, fake)["status"], "review_required")
        self.assertFalse(fake.calls)
        data = sample()
        data["source"]["text"] += "x" * reviewer.MAX_REQUEST_BYTES
        self.assertEqual(run_jev(data, fake)["code"], "request_too_large")
        self.assertFalse(fake.calls)

    def test_cli_local_fixture(self):
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            code = reviewer.main(["--input", str(FIXTURE), "--mode", "local"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "local_checks_passed")

    def test_http_transport_uses_fixed_endpoint_and_disallows_redirect(self):
        payload = reviewer.build_request(sample())
        raw = json.dumps(FakeTransport()(payload, "dummy", 2)).encode()
        class Response(io.BytesIO):
            pass
        class Opener:
            def open(self, request, timeout):
                self.request, self.timeout = request, timeout
                return Response(raw)
        opener = Opener()
        with patch.object(reviewer.urllib.request, "build_opener", return_value=opener) as build:
            result = reviewer.http_transport(payload, "dummy", 3)
        self.assertEqual(opener.request.full_url, reviewer.ENDPOINT)
        self.assertEqual(opener.request.get_method(), "POST")
        self.assertEqual(opener.request.get_header("Authorization"), "Bearer dummy")
        self.assertEqual(json.loads(opener.request.data), payload)
        self.assertIsInstance(build.call_args.args[0], reviewer._NoRedirect)
        self.assertIsNone(reviewer._NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.invalid"))
        reviewer.validate_response(result, payload)

    def test_cli_invalid_json_and_oversize_do_not_echo_input(self):
        for raw in (b'{"secret":"private-invalid', b'x' * (reviewer.MAX_INPUT_BYTES + 1)):
            with patch.object(Path, "open", return_value=io.BytesIO(raw)), patch("sys.stdout", new_callable=io.StringIO) as output:
                code = reviewer.main(["--input", "unused.json", "--mode", "local"])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(output.getvalue())["status"], "failed")
            self.assertNotIn("private-invalid", output.getvalue())


if __name__ == "__main__":
    unittest.main()
