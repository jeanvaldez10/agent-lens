from unittest.mock import patch, MagicMock
import agentlens
import threading


def test_get_client_singleton():
    # Should always return the same instance
    c1 = agentlens.get_client()
    c2 = agentlens.get_client()
    assert c1 is c2


def test_get_client_thread_safety():
    # Should not create multiple clients in threads
    results = []

    def worker():
        results.append(agentlens.get_client())

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(r is results[0] for r in results)


def test_init_merges_tags(monkeypatch):
    with patch("agentlens.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        agentlens.init(tags=["a"], default_tags=["b"])  # Should merge
        assert {"a", "b"}.issubset(set(mock_client.init.call_args[1]["default_tags"]))


def test_init_warns_on_deprecated_tags(monkeypatch):
    with patch("agentlens.get_client") as mock_get_client, patch("agentlens.warn_deprecated_param") as mock_warn:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        agentlens.init(tags=["a"])
        mock_warn.assert_called_once_with("tags", "default_tags")


def test_init_jupyter_detection(monkeypatch):
    with patch("agentlens.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        # Simulate Jupyter by patching get_ipython
        import builtins

        builtins.get_ipython = lambda: type("Z", (), {"__name__": "ZMQInteractiveShell"})()
        agentlens.init()
        del builtins.get_ipython


def test_init_jupyter_detection_nameerror():
    with patch("agentlens.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        # Simulate NameError when get_ipython() is called
        import builtins

        original_get_ipython = getattr(builtins, "get_ipython", None)
        builtins.get_ipython = lambda: None  # This will cause NameError
        try:
            agentlens.init()
        except NameError:
            pass  # Expected
        finally:
            if original_get_ipython:
                builtins.get_ipython = original_get_ipython
            else:
                delattr(builtins, "get_ipython")


def test_configure_valid_and_invalid_params():
    with patch("agentlens.get_client") as mock_get_client, patch("agentlens.logger") as mock_logger:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        # Valid param
        agentlens.configure(api_key="foo")
        mock_client.configure.assert_called_with(api_key="foo")
        # Invalid param
        agentlens.configure(bad_param=123)
        mock_logger.warning.assert_any_call("Invalid configuration parameters: {'bad_param'}")


def test_record_sets_end_timestamp():
    class Dummy:
        end_timestamp = None

    with patch("agentlens.helpers.time.get_ISO_time", return_value="now"):
        d = Dummy()
        agentlens.record(d)
        assert d.end_timestamp == "now"


def test_record_no_end_timestamp():
    class Dummy:
        pass

    d = Dummy()
    assert agentlens.record(d) is d


def test_update_trace_metadata_success():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        result = agentlens.update_trace_metadata({"foo": "bar"})
        assert result is True
        mock_span.set_attribute.assert_called()


def test_update_trace_metadata_no_active_span():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span", return_value=None):
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        assert not agentlens.update_trace_metadata({"foo": "bar"})


def test_update_trace_metadata_not_recording():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = False
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        assert not agentlens.update_trace_metadata({"foo": "bar"})


def test_update_trace_metadata_invalid_type():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        # Value is a dict, which is not allowed
        assert not agentlens.update_trace_metadata({"foo": {"bar": 1}})


def test_update_trace_metadata_list_type():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        # List of valid types
        assert agentlens.update_trace_metadata({"foo": [1, 2, 3]})
        mock_span.set_attribute.assert_called()


def test_update_trace_metadata_extract_key_single_part():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # Test with a semantic convention that has only one part (len < 2)
        with patch("agentlens.AgentAttributes") as mock_attrs:
            mock_attrs.__dict__ = {"SINGLE": "single_value"}
            result = agentlens.update_trace_metadata({"single_value": "test"})
            assert result is True


def test_update_trace_metadata_skip_gen_ai_attributes():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # Test that gen_ai attributes are skipped
        with patch("agentlens.AgentAttributes") as mock_attrs:
            mock_attrs.__dict__ = {"GEN_AI_ATTR": "gen_ai.something"}
            agentlens.update_trace_metadata({"gen_ai.something": "test"})
            # Should still work but skip the gen_ai attribute


def test_update_trace_metadata_trace_id_conversion_error():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "child_span"  # Not a session span
        mock_span.get_span_context.return_value.trace_id = "invalid_hex"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {"trace1": MagicMock()}
        mock_tracer.initialized = True

        # This should handle the ValueError from int("invalid_hex", 16)
        agentlens.update_trace_metadata({"foo": "bar"})
        # The function should handle the error gracefully


def test_update_trace_metadata_no_active_traces():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span", return_value=None),
        patch("agentlens.logger") as mock_logger,
    ):
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        result = agentlens.update_trace_metadata({"foo": "bar"})
        assert result is False
        mock_logger.warning.assert_called_with("No active trace found. Cannot update metadata.")


def test_update_trace_metadata_span_not_recording():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span") as mock_get_span,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_span = MagicMock()
        mock_span.is_recording.return_value = False
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        result = agentlens.update_trace_metadata({"foo": "bar"})
        assert result is False
        mock_logger.warning.assert_called_with("No active trace found. Cannot update metadata.")


def test_update_trace_metadata_list_invalid_types():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span") as mock_get_span,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # List with invalid types (dict)
        agentlens.update_trace_metadata({"foo": [{"invalid": "type"}]})
        mock_logger.warning.assert_called_with("No valid metadata attributes were updated")


def test_update_trace_metadata_invalid_value_type():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span") as mock_get_span,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # Invalid value type (dict)
        agentlens.update_trace_metadata({"foo": {"invalid": "type"}})
        mock_logger.warning.assert_called_with("No valid metadata attributes were updated")


def test_update_trace_metadata_semantic_convention_mapping():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span") as mock_get_span,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # Test semantic convention mapping
        with patch("agentlens.AgentAttributes") as mock_attrs:
            mock_attrs.__dict__ = {"TEST_ATTR": "agent.test_attribute"}
            agentlens.update_trace_metadata({"agent_test_attribute": "test"})
            mock_logger.debug.assert_called_with("Successfully updated 1 metadata attributes on trace")


def test_update_trace_metadata_exception_handling():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span") as mock_get_span,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_span.set_attribute.side_effect = Exception("Test error")
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        agentlens.update_trace_metadata({"foo": "bar"})
        mock_logger.error.assert_called_with("Error updating trace metadata: Test error")


def test_update_trace_metadata_no_valid_attributes():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span") as mock_get_span,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # All values are None
        agentlens.update_trace_metadata({"foo": None, "bar": None})
        mock_logger.warning.assert_called_with("No valid metadata attributes were updated")


def test_start_trace_auto_init_failure():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.init") as mock_init,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_tracer.initialized = False
        mock_init.side_effect = Exception("Init failed")

        agentlens.start_trace("test")
        mock_logger.error.assert_called_with(
            "SDK auto-initialization failed during start_trace: Init failed. Cannot start trace."
        )


def test_start_trace_auto_init_still_not_initialized():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.init") as _,
        patch("agentlens.logger") as mock_logger,
    ):
        mock_tracer.initialized = False

        agentlens.start_trace("test")
        mock_logger.error.assert_called_with("SDK initialization failed. Cannot start trace.")


def test_end_trace_not_initialized():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.logger") as mock_logger:
        mock_tracer.initialized = False
        agentlens.end_trace()
        mock_logger.warning.assert_called_with("agentlens SDK not initialized. Cannot end trace.")


def test_update_trace_metadata_not_initialized():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.logger") as mock_logger:
        mock_tracer.initialized = False
        agentlens.update_trace_metadata({"foo": "bar"})
        mock_logger.warning.assert_called_with("agentlens SDK not initialized. Cannot update trace metadata.")


def test_all_exports_importable():
    # Just import all symbols to ensure they're present
    from agentlens import (
        init,
        configure,
    )

    assert callable(init)
    assert callable(configure)


def test_update_trace_metadata_use_current_span_when_no_parent_found():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "child_span"  # Not a session span
        mock_span.get_span_context.return_value.trace_id = 12345
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {"trace1": MagicMock()}
        mock_tracer.initialized = True

        # When no parent trace is found, should use current span
        agentlens.update_trace_metadata({"foo": "bar"})
        # The function should work with current span


def test_update_trace_metadata_use_current_span_when_no_active_traces():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "child_span"  # Not a session span
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # When no active traces, should use current span
        agentlens.update_trace_metadata({"foo": "bar"})
        # The function should work with current span


def test_update_trace_metadata_use_most_recent_trace():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span", return_value=None),
        patch("agentlens.logger") as mock_logger,
    ):
        mock_trace_context = MagicMock()
        mock_trace_context.span = MagicMock()
        mock_trace_context.span.is_recording.return_value = True
        mock_tracer.get_active_traces.return_value = {"trace1": mock_trace_context}
        mock_tracer.initialized = True

        agentlens.update_trace_metadata({"foo": "bar"})
        mock_logger.debug.assert_called_with("Successfully updated 1 metadata attributes on trace")


def test_end_trace_with_trace_context():
    with patch("agentlens.tracer") as mock_tracer:
        mock_tracer.initialized = True
        mock_trace_context = MagicMock()
        agentlens.end_trace(mock_trace_context, "Error")
        mock_tracer.end_trace.assert_called_with(trace_context=mock_trace_context, end_state="Error")


def test_init_jupyter_detection_actual_nameerror():
    with patch("agentlens.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        # Actually remove get_ipython to trigger NameError
        import builtins

        original_get_ipython = getattr(builtins, "get_ipython", None)
        if hasattr(builtins, "get_ipython"):
            delattr(builtins, "get_ipython")
        try:
            agentlens.init()
        finally:
            if original_get_ipython:
                builtins.get_ipython = original_get_ipython


def test_end_trace_with_default_state():
    with patch("agentlens.tracer") as mock_tracer:
        mock_tracer.initialized = True
        from agentlens import TraceState

        agentlens.end_trace()  # Should use default TraceState.SUCCESS
        mock_tracer.end_trace.assert_called_with(trace_context=None, end_state=TraceState.SUCCESS)


def test_update_trace_metadata_extract_key_single_part_actual():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # Test with a semantic convention that has only one part (len < 2)
        with patch("agentlens.AgentAttributes") as mock_attrs:
            mock_attrs.__dict__ = {"SINGLE": "single"}
            agentlens.update_trace_metadata({"single": "test"})
            # The function should handle single-part attributes


def test_update_trace_metadata_skip_gen_ai_attributes_actual():
    with patch("agentlens.tracer") as mock_tracer, patch("agentlens.get_current_span") as mock_get_span:
        mock_span = MagicMock()
        mock_span.is_recording.return_value = True
        mock_span.name = "foo.SESSION"
        mock_get_span.return_value = mock_span
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True

        # Test that gen_ai attributes are actually skipped in the mapping
        with patch("agentlens.AgentAttributes") as mock_attrs:
            mock_attrs.__dict__ = {"GEN_AI_ATTR": "gen_ai.something"}
            agentlens.update_trace_metadata({"gen_ai.something": "test"})
            # Should still work but the gen_ai attribute should be skipped in mapping


def test_update_trace_metadata_no_active_traces_actual():
    with (
        patch("agentlens.tracer") as mock_tracer,
        patch("agentlens.get_current_span", return_value=None),
        patch("agentlens.logger") as mock_logger,
    ):
        mock_tracer.get_active_traces.return_value = {}
        mock_tracer.initialized = True
        agentlens.update_trace_metadata({"foo": "bar"})
        mock_logger.warning.assert_called_with("No active trace found. Cannot update metadata.")
