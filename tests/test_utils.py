import pytest
from backend.utils import format_as_ndjson, parse_multi_columns


@pytest.mark.asyncio
async def test_format_as_ndjson():
***REMOVED***async def dummy_generator():
***REMOVED***yield {"message": "test message\n"}

***REMOVED***async for event in format_as_ndjson(dummy_generator()):
***REMOVED***assert event == '{"message": "test message\\n"}\n'


@pytest.mark.asyncio
async def test_format_as_ndjson_exception():
***REMOVED***async def dummy_generator():
***REMOVED***raise Exception("test exception")
***REMOVED***yield {"message": "test message\n"}
***REMOVED***
***REMOVED***async for event in format_as_ndjson(dummy_generator()):
***REMOVED***assert event == '{"error": "test exception"}'

def test_parse_multi_columns():
***REMOVED***test_pipes = "col1|col2|col3"
***REMOVED***test_commas = "col1,col2,col3"
***REMOVED***test_single = "col1"
***REMOVED***assert parse_multi_columns(test_pipes) == ["col1", "col2", "col3"]
***REMOVED***assert parse_multi_columns(test_commas) == ["col1", "col2", "col3"]
***REMOVED***assert parse_multi_columns(test_single) == ["col1"]
