# Case Study: Documentation Assistant

## 1. Goal and Mission

This case study demonstrates how to build a helpful AI assistant that can answer questions about a codebase and generate documentation. The key challenge is providing the language model with the right context from a large and complex set of source files, while respecting token limits and minimizing noise.

**Mission:** To create an agent that can accurately answer questions like "How does the `User` class work?" or "Generate the markdown documentation for the `authentication.py` module."

## 2. Target Codebase (`src/example_code.py`)

For this case study, imagine the agent is operating on the following simple Python file.

```python
# src/example_code.py

class User:
    """
    Represents a user in the system.
    """
    def __init__(self, username: str, email: str):
        """
        Initializes a new User instance.

        Args:
            username: The user's chosen username.
            email: The user's email address.
        """
        self.username = username
        self.email = email
        self.is_active = True

    def deactivate(self):
        """
        Deactivates the user's account.
        """
        self.is_active = False
        print(f"User {self.username} has been deactivated.")

    def __repr__(self):
        return f"<User username='{self.username}' email='{self.email}'>"
```

## 3. Context Control Patterns Applied

-   **`Scope`**: We define which files are relevant, excluding build artifacts or dependencies.
-   **`Attention`**: We use heuristics (searching for class/function definitions) to focus on the most important parts of a file.
-   **`Boundaries`**: Clear markers separate the user's prompt, retrieved code, and system instructions.
-   **`Selection`**: A `SymbolicSearchTool` finds relevant code snippets.
-   **`Ordering`**: Snippets are ordered to place definitions before implementations.
-   **`Agents` & `Tools`**: An agentic workflow uses tools to find and read code.

## 4. Agent Workflow

The agent uses a ReAct-style loop (Reasoning + Acting) to answer the user's query.

```mermaid
flowchart TD
    A[User Query: "Document the User class"] --> B{Agent: Reason};
    B --> C[Act: Call SymbolicSearchTool.find_symbol("User")];
    C --> D{Observe: Get Code Snippet};
    D --> E{Agent: Reason - Have enough info?};
    E -- Yes --> F[Generate Final Documentation];
    E -- No --> G[Act: Call another tool (e.g., read_file)];
    G --> D;
```

### Step 1: Defining the Agent's Tools

First, we define the tools that the agent can use. The pseudo-code below is more detailed to show how such tools could be structured.

```python
# pseudo-code for agent tools

class Snippet:
    """A container for a piece of retrieved code."""
    def __init__(self, source_file: str, content: str, start_line: int):
        self.source_file = source_file
        self.content = content
        self.start_line = start_line
        self.tokens = len(content) // 4 # Heuristic token count

class FileSystemTool:
    """A tool for interacting with the file system."""
    def list_files(self, path: str) -> list[str]:
        """Lists files in a directory, respecting .gitignore."""
        # Implementation would use `glob` and ignore patterns.
        print(f"TOOL: Listing files in {path}...")
        return ["src/example_code.py"]

    def read_file(self, path: str, lines: tuple[int, int] = None) -> str:
        """Reads the content of a file."""
        # Implementation would read from the filesystem.
        print(f"TOOL: Reading file {path}...")
        with open(path, 'r') as f:
            return f.read()

class SymbolicSearchTool:
    """A tool for finding symbol definitions in the codebase."""
    def find_symbol(self, symbol: str) -> list[Snippet]:
        """Finds the definition of a class or function."""
        # Implementation would use ctags, tree-sitter, or an LSP.
        print(f"TOOL: Searching for symbol '{symbol}'...")
        # In our example, it finds the User class in example_code.py
        code = '''class User:
    """
    Represents a user in the system.
    """
    def __init__(self, username: str, email: str):
        # ... methods ...
'''
        return [Snippet(source_file="src/example_code.py", content=code, start_line=3)]
```

*Self-Correction: Initially, we might think a simple text search is enough. However, a symbolic search is much more precise and avoids noisy results from irrelevant comments or variable usages.*

### Step 2: Putting It All Together: A Walkthrough

Let's trace the agent's steps for the query: **"How does the `User` class work?"**

1.  **REASON**: The agent decides the best first step is to locate the `User` class definition.
2.  **ACT**: The agent calls `SymbolicSearchTool.find_symbol("User")`.
3.  **OBSERVE**: The tool returns a `Snippet` object containing the `User` class definition from `src/example_code.py`.

    **Tool Output (Snippet):**
    ```
    source_file: "src/example_code.py"
    content: `class User: ...`
    start_line: 3
    ```

4.  **REASON**: The agent now has the class definition. It determines this is sufficient to answer the user's question.
5.  **ACT (Final Response)**: The agent generates the final documentation, using the provided context.

    **Final Agent Response:**
    > The `User` class in `src/example_code.py` represents a user in the system. It is initialized with a `username` and `email`. It has methods to `deactivate()` the user's account.

## 5. Challenges and Solutions

-   **Challenge:** The model gets lost in large files.
    -   **Solution:** Use of the `Attention` primitive via the `SymbolicSearchTool`. Instead of feeding the whole file, we provide only the most relevant class or function definition.

-   **Challenge:** The model hallucinates documentation for code that doesn't exist.
    -   **Solution:** Strict `Validation`. The agent's reasoning is constrained so that it can only generate documentation for code snippets that have been explicitly retrieved from the codebase.

-   **Challenge:** Answers are inconsistent between similar queries.
    -   **Solution:** `Ordering` and `Boundaries`. By presenting the context in a consistent order and with clear boundaries, we create a more stable and predictable input for the model.
