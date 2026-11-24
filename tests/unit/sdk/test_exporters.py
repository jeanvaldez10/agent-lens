"""
Unit tests for AuthenticatedOTLPExporter.
"""

import unittest
from unittest.mock import Mock, patch

import requests
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExportResult
from opentelemetry.exporter.otlp.proto.http import Compression

from agentlens.sdk.exporters import AuthenticatedOTLPExporter
from agentlens.exceptions import agentlensApiJwtExpiredException, ApiServerException

# these are simple tests on a simple file, basically just to get test coverage


class TestAuthenticatedOTLPExporter(unittest.TestCase):
    """Tests for AuthenticatedOTLPExporter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.endpoint = "http://localhost:8000/v1/traces"
        self.jwt = "test-jwt-token"
        self.timeout = 30
        self.compression = Compression.Gzip
        self.custom_headers = {"X-Custom-Header": "test-value"}

    def test_initialization_with_required_params(self):
        """Test exporter initialization with required parameters."""
        exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

        # Verify the exporter was created successfully
        self.assertIsInstance(exporter, AuthenticatedOTLPExporter)
        self.assertEqual(exporter._endpoint, self.endpoint)

    def test_initialization_with_all_params(self):
        """Test exporter initialization with all parameters."""
        exporter = AuthenticatedOTLPExporter(
            endpoint=self.endpoint,
            jwt=self.jwt,
            headers=self.custom_headers,
            timeout=self.timeout,
            compression=self.compression,
        )

        # Verify the exporter was created successfully
        self.assertIsInstance(exporter, AuthenticatedOTLPExporter)
        self.assertEqual(exporter._endpoint, self.endpoint)

    def test_initialization_without_optional_params(self):
        """Test exporter initialization without optional parameters."""
        exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

        # Verify the exporter was created successfully
        self.assertIsInstance(exporter, AuthenticatedOTLPExporter)
        self.assertEqual(exporter._endpoint, self.endpoint)

    def test_export_success(self):
        """Test successful span export."""
        mock_spans = [Mock(spec=ReadableSpan), Mock(spec=ReadableSpan)]

        with patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter.export") as mock_export:
            mock_export.return_value = SpanExportResult.SUCCESS

            exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

            result = exporter.export(mock_spans)

            # Verify the result
            self.assertEqual(result, SpanExportResult.SUCCESS)

    def test_export_jwt_expired_exception(self):
        """Test export handling of JWT expired exception."""
        mock_spans = [Mock(spec=ReadableSpan)]

        with patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter.export") as mock_export:
            mock_export.side_effect = agentlensApiJwtExpiredException("Token expired")

            with patch("agentlens.sdk.exporters.logger") as mock_logger:
                exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

                result = exporter.export(mock_spans)

                # Verify failure result and logging
                self.assertEqual(result, SpanExportResult.FAILURE)
                mock_logger.warning.assert_called_once()

    def test_export_api_server_exception(self):
        """Test export handling of API server exception."""
        mock_spans = [Mock(spec=ReadableSpan)]

        with patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter.export") as mock_export:
            mock_export.side_effect = ApiServerException("Server error")

            with patch("agentlens.sdk.exporters.logger") as mock_logger:
                exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

                result = exporter.export(mock_spans)

                # Verify failure result and logging
                self.assertEqual(result, SpanExportResult.FAILURE)
                mock_logger.error.assert_called_once()

    def test_export_requests_exception(self):
        """Test export handling of requests exception."""
        mock_spans = [Mock(spec=ReadableSpan)]

        with patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter.export") as mock_export:
            mock_export.side_effect = requests.RequestException("Network error")

            with patch("agentlens.sdk.exporters.logger") as mock_logger:
                exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

                result = exporter.export(mock_spans)

                # Verify failure result and logging
                self.assertEqual(result, SpanExportResult.FAILURE)
                mock_logger.error.assert_called_once()

    def test_export_unexpected_exception(self):
        """Test export handling of unexpected exception."""
        mock_spans = [Mock(spec=ReadableSpan)]

        with patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter.export") as mock_export:
            mock_export.side_effect = ValueError("Unexpected error")

            with patch("agentlens.sdk.exporters.logger") as mock_logger:
                exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

                result = exporter.export(mock_spans)

                # Verify failure result and logging
                self.assertEqual(result, SpanExportResult.FAILURE)
                mock_logger.error.assert_called_once()

    def test_export_empty_spans_list(self):
        """Test export with empty spans list."""
        mock_spans = []

        with patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter.export") as mock_export:
            mock_export.return_value = SpanExportResult.SUCCESS

            exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

            result = exporter.export(mock_spans)

            # Verify the result
            self.assertEqual(result, SpanExportResult.SUCCESS)

    def test_clear_method(self):
        """Test clear method (should be a no-op)."""
        exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

        # Clear method should not raise any exception
        exporter.clear()

    def test_initialization_with_kwargs(self):
        """Test exporter initialization with additional kwargs."""
        exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt, custom_param="test_value")

        # Verify the exporter was created successfully
        self.assertIsInstance(exporter, AuthenticatedOTLPExporter)

    def test_headers_merging(self):
        """Test that custom headers are properly merged with authorization header."""
        custom_headers = {"X-Custom-Header": "test-value", "Content-Type": "application/json"}

        exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt, headers=custom_headers)

        # Verify the exporter was created successfully
        self.assertIsInstance(exporter, AuthenticatedOTLPExporter)

    def test_headers_protected_from_override(self):
        """Test that critical headers cannot be overridden by user-supplied headers."""
        # Attempt to override critical headers
        malicious_headers = {
            "Authorization": "Malicious-Auth malicious-token",
            "Content-Type": "text/plain",
            "User-Agent": "malicious-agent",
            "X-API-Key": "malicious-key",
            "X-Custom-Header": "test-value",  # This should be allowed
        }

        exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt, headers=malicious_headers)

        # Test the _prepare_headers method directly to verify protection
        prepared_headers = exporter._prepare_headers(malicious_headers)

        # Critical headers should not be overridden
        self.assertEqual(prepared_headers["Authorization"], f"Bearer {self.jwt}")
        self.assertNotEqual(prepared_headers.get("Content-Type"), "text/plain")
        self.assertNotEqual(prepared_headers.get("User-Agent"), "malicious-agent")
        self.assertNotIn("X-API-Key", prepared_headers)  # Should be filtered out

        # Non-critical headers should be allowed
        self.assertEqual(prepared_headers.get("X-Custom-Header"), "test-value")

        # Verify the exporter was created successfully
        self.assertIsInstance(exporter, AuthenticatedOTLPExporter)


class TestAuthenticatedOTLPExporterIntegration(unittest.TestCase):
    """Integration-style tests for AuthenticatedOTLPExporter."""

    def setUp(self):
        """Set up test fixtures."""
        self.endpoint = "http://localhost:8000/v1/traces"
        self.jwt = "test-jwt-token"

    def test_full_export_cycle(self):
        """Test a complete export cycle with multiple spans."""
        # Create mock spans
        mock_spans = [
            Mock(spec=ReadableSpan, name="span1"),
            Mock(spec=ReadableSpan, name="span2"),
            Mock(spec=ReadableSpan, name="span3"),
        ]

        with patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter.export") as mock_export:
            mock_export.return_value = SpanExportResult.SUCCESS

            # Create exporter
            exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt)

            # Export spans
            result = exporter.export(mock_spans)

            # Verify results
            self.assertEqual(result, SpanExportResult.SUCCESS)

            # Test clear method
            exporter.clear()  # Should not raise any exception

    def test_export_with_different_compression_types(self):
        """Test exporter with different compression types."""
        compression_types = [Compression.Gzip, Compression.Deflate, None]

        for compression in compression_types:
            with self.subTest(compression=compression):
                exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt, compression=compression)

                # Verify the exporter was created successfully
                self.assertIsInstance(exporter, AuthenticatedOTLPExporter)

    def test_export_with_different_timeouts(self):
        """Test exporter with different timeout values."""
        timeout_values = [10, 30, 60, None]

        for timeout in timeout_values:
            with self.subTest(timeout=timeout):
                exporter = AuthenticatedOTLPExporter(endpoint=self.endpoint, jwt=self.jwt, timeout=timeout)

                # Verify the exporter was created successfully
                self.assertIsInstance(exporter, AuthenticatedOTLPExporter)


# --- End-to-end tests through the real OTLP HTTP export path -------------------------------------
# These do not mock OTLPSpanExporter.export, so they catch breakage in how auth headers reach the
# wire when OpenTelemetry's exporter internals change between releases.

E2E_ENDPOINT = "https://otlp.example.test/v1/traces"


def _make_span():
    from opentelemetry.sdk.trace import TracerProvider

    provider = TracerProvider()
    span = provider.get_tracer("agentlens-test").start_span("e2e-span")
    span.end()
    return span


def test_e2e_export_sends_current_jwt(mock_req):
    mock_req.post(E2E_ENDPOINT, status_code=200)
    token = {"value": "first-token"}
    exporter = AuthenticatedOTLPExporter(
        endpoint=E2E_ENDPOINT, jwt_provider=lambda: token["value"], headers={"X-Custom": "yes"}
    )

    assert exporter.export([_make_span()]) == SpanExportResult.SUCCESS
    sent = mock_req.request_history[-1]
    assert sent.url == E2E_ENDPOINT
    assert sent.headers["Authorization"] == "Bearer first-token"
    assert sent.headers["X-Custom"] == "yes"
    assert sent.headers["Content-Type"] == "application/x-protobuf"

    # A rotated token is picked up on the next export without recreating the exporter
    token["value"] = "second-token"
    assert exporter.export([_make_span()]) == SpanExportResult.SUCCESS
    assert mock_req.request_history[-1].headers["Authorization"] == "Bearer second-token"


def test_e2e_export_user_cannot_override_authorization(mock_req):
    mock_req.post(E2E_ENDPOINT, status_code=200)
    exporter = AuthenticatedOTLPExporter(
        endpoint=E2E_ENDPOINT, jwt="real-token", headers={"Authorization": "Bearer attacker"}
    )

    assert exporter.export([_make_span()]) == SpanExportResult.SUCCESS
    assert mock_req.request_history[-1].headers["Authorization"] == "Bearer real-token"


def test_e2e_export_backs_off_after_401(mock_req):
    mock_req.post(E2E_ENDPOINT, status_code=401)
    exporter = AuthenticatedOTLPExporter(endpoint=E2E_ENDPOINT, jwt="bad-token")

    with patch("agentlens.sdk.exporters.logger") as mock_logger:
        assert exporter.export([_make_span()]) == SpanExportResult.FAILURE
        mock_logger.warning.assert_called_once()

    calls_after_first = len(mock_req.request_history)
    # Within the back-off window the exporter must not hit the endpoint again
    assert exporter.export([_make_span()]) == SpanExportResult.FAILURE
    assert len(mock_req.request_history) == calls_after_first


if __name__ == "__main__":
    unittest.main()
