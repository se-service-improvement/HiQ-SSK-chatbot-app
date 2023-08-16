from app import format_as_ndjson


def test_format_as_ndjson():
***REMOVED***obj = {"message": "I ❤️ 🐍 \n and escaped newlines"}
***REMOVED***assert format_as_ndjson(obj) == '{"message": "I ❤️ 🐍 \\n and escaped newlines"}\n'
