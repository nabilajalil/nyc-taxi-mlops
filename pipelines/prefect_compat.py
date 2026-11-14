"""Temporary compatibility patch for Prefect and FastAPI."""

import inspect
import fastapi

_original_body = fastapi.Body

if "min_items" not in inspect.signature(_original_body).parameters:

    def compatible_body(
        *args,
        min_items=None,
        max_items=None,
        **kwargs,
    ):
        if min_items is not None:
            kwargs["min_length"] = min_items

        if max_items is not None:
            kwargs["max_length"] = max_items

        return _original_body(*args, **kwargs)

    fastapi.Body = compatible_body
