from langchain.tools import Tool

def get_code_snippet_single_input(query: str) -> str:
    """
    Accepts a single input string like:
    'file_path=app.py, line=27, context=5'
    and returns the code snippet around that line.
    """
    try:
        args = dict(
            part.strip().split("=")
            for part in query.split(",")
        )
        file_path = args["file_path"]
        line = int(args["line"])
        context = int(args.get("context", 5))

        with open(file_path) as f:
            lines = f.readlines()

        start = max(line - context - 1, 0)
        end = min(line + context, len(lines))
        snippet = "".join(lines[start:end])

        return f"File: {file_path}, Line: {line}\n```\n{snippet}\n```"

    except Exception as e:
        return f"Error parsing or reading code: {e}"

get_code_snippet = Tool(
    name="get_code_snippet",
    func=get_code_snippet_single_input,
    description="Get a code snippet from a file by specifying: file_path, line, context"
)
