# Optional local code context

New Claude and Codex chats can optionally use a local source-evidence helper.
In **New Chat**, check **Use local code context (optional)** before starting.
The checkbox starts unchecked each time and is never saved as a provider
preference. Other chats, terminal launches, child launches and existing sessions
do not inherit it. Changing model/account within the same open dialog preserves
the choice; switching to an unsupported provider clears it.

The helper finds candidate implementations and returns source with file paths,
line numbers, complete definitions where supported, and direct same-file
constants. It keeps ordinary provider tools and configured execution available.
The agent can expand evidence or use normal search automatically. There is no
new task-approval prompt, background service, network listener, model download
or modification of provider configuration.

This is experimental source assistance. It does **not** guarantee fewer tokens,
correct answers, complete dependency analysis, or that the provider will choose
to call it. Full task-level quality and savings require separate evaluation.

## Install on the agent's machine

Use Python 3.11+ in the environment containing that machine's `agent-orch`:

```sh
python -m pip install -e 'services/agent-orch[code-context]'
pentacle-code-context status --json
```

Run the install command from the Pentacle checkout root. The optional extra
installs Tree-sitter and JavaScript/TypeScript grammars. The base installation,
`python -m pip install -e services/agent-orch`, also installs the standalone
helper: Python definitions use the standard library, while unsupported or
missing language parsers produce explicitly incomplete lexical evidence.
There is no automatic installation at chat startup.

Both base and extra wheels contain the standalone entrypoint. Its runtime does
not import the daemon, subscription registry, sibling `_shared` source or private
configuration. Source in a project is parsed, never imported or executed.

Configure the target machine's existing `agent_orch_bin_dir` to the directory
containing **both** `agent-orch` and `pentacle-code-context` when necessary. This
also applies to SSH hosts; installing a helper on the web host alone does not
install it on an agent's machine. The daemon probes that exact target executable
for at most two seconds, without scanning source or starting a provider. Named
accounts use the existing allowlisted launch environment.

The New Chat option requires an updated daemon advertising `code_context_v1`.
With an older catalog the control is absent and normal spawning is unchanged.
The CLI also supports `agent-orch spawn --provider codex --code-context` with
the other ordinary spawn arguments. An explicit CLI opt-in to an old daemon is
refused before spawning. Scheduling, resume, handoff, custom command launches,
Gemini and Cursor are outside this fresh-session opt-in.

If the helper is missing, times out, or returns an incompatible capability
response, the chat still starts with normal tools and a fallback notice. A
successful `code_context.active` acknowledgment means advisory launch guidance
was supplied; it does not prove a model invocation. Switching the checkbox off
for the next chat needs no cleanup or migration. Existing native transcripts
may retain their earlier instructions; this is not a retroactive session switch.

## Direct use

These commands need no daemon, account credentials or generating model:

```sh
pentacle-code-context query --root /path/to/project --query 'How is a request validated?'
pentacle-code-context query --root /path/to/project --query validate_request
pentacle-code-context read --root /path/to/project --path src/requests.py --symbol validate_request
pentacle-code-context read --root /path/to/project --path src/requests.py --start 20 --end 60
pentacle-code-context search --root /path/to/project --query 'invalid_request'
```

An explicit root must be the exact Git worktree root. Without `--root`, only the
current directory's containing worktree is selected; the helper does not search
a workspace for repositories. Non-Git folders, the filesystem root, the user's
home directory, symlink root arguments and platforms lacking POSIX descriptor
relative/no-follow opens return unavailable. Linked Git worktrees are supported.

`query` uses exact identifiers or contextual file/unit lexical ranking. It
localizes up to 32 candidate files before extracting definitions. `read --symbol`
selects parsed functions/methods, including duplicate names if present;
`read --start --end` returns an explicit range of at most 1,000 lines.
`search` is bounded case-insensitive literal text search. JavaScript/JSX,
TypeScript/TSX and Python definitions have syntax-aware extraction when their
parsers work. Other admitted text uses clearly incomplete ranges.

Every result is a single JSON object with schema `pentacle.code-context.v1`:

- `status`: `candidates`, `partial`, `no_match`, or `unavailable`; capability
  status uses `ready`/`unavailable`.
- `evidence`: relative `path`, 1-based `start`/`end`, captured full-file `sha256`,
  original `excerpt`, `symbol`, `unit_complete` and dependency boundaries.
  Parsed definitions may include `supporting_constants` with their own ranges.
- `scan`, `limitations`, `capture_ms`, and `fallback` describe actual bounds and
  further source reads. Resource failures may return a smaller unavailable
  envelope instead of a partial capture.

Check the evidence and limitations even when the command exits zero. Usable
partial responses and no-match responses exit zero; invalid or unavailable
requests exit two. `--help` prints human-readable usage. No source/code body is
included in diagnostic exceptions. Rank scores are not correctness probabilities.

`unit_complete` describes a selected definition's source extent, not whether an
answer has sufficient evidence. Imports, enclosing state, closures, decorators,
configuration and dynamic calls may require further reads. Parser errors or
missing/incompatible grammars return lexical fallback, never a false complete
definition. Oversized units return a locator and an explicit range-expansion
request; they are not cut and labeled complete.

For multi-term questions, a conservative token-overlap heuristic returns only
small locators when no candidate has enough overlap. This `weak_match` state
avoids sending unrelated bodies; it is not calibrated confidence and can reject
useful candidates. Use native search or a precise identifier/read to continue.

## Scope, freshness and resource bounds

Each invocation enumerates Git tracked and untracked nonignored paths, hashes
captured bytes and creates only an in-memory index. There is no disk source
cache or watcher. Changes with preserved size/mtime, new files, renames and
deletions are seen on the next invocation. Before emission, selected bytes,
root identity, ignore rules and membership are checked again. Changed evidence
is suppressed. This is a checked capture, not an atomic repository snapshot.

Admission and direct reads share the same checks. Files and intermediate path
components are opened without following symlinks; nonregular files, submodule
directories and nested repository traversal are excluded. Git plumbing runs
without shell expansion, with repository fsmonitor/hooks disabled and bounded
time/output. Project files cannot shadow parser imports in the isolated worker.

Built-in excluded directory names are `.git`, `.hg`, `.svn`, `node_modules`,
`vendor`, `dist`, `build`, `release`, `coverage`, `__pycache__`, `.cache`, `.venv`,
`venv`, `.tox`, `.next`, `.claude`, `.codex`, `.gemini`, `.cursor`, `.ssh`, `.aws`,
`.azure`, `.kube`, `.gnupg` and `.pentacle-stream-tokens`. Credential-related
filename components (`credential[s]`, `secret[s]`, `token[s]`, separated by `.`,
`_` or `-`), `.env`/`.env.*`, SSH private-key names, `.netrc`, `.npmrc`, `.pypirc`,
and `.pem`/`.key`/`.p12`/`.pfx`/`.keystore` files are excluded even if tracked.
Examples/templates are not exempt. Binary/non-UTF8 content is excluded. This
is conservative path filtering, not detection of every secret embedded in code.

Only common source/config/document text extensions are admitted. Ordinary tests
and docs remain eligible; dependencies/generated trees do not. Add root-local
`.pentacle-context-ignore` exclusions using one pattern per line: `#` comments,
case-sensitive wildcard matching of root-relative POSIX paths, basename patterns
without `/`, or a root-prefix directory ending in `/`. `*` follows Python
`fnmatch` semantics, including matching `/` in full paths. Negation is rejected;
this file cannot undo built-in exclusions. Git ignore rules apply to tracked
files too.

Limits are 5,000 source files, 32 MiB admitted bytes, 1 MiB per file, 2 MiB Git
listing output, two seconds per Git operation, and ten seconds for the owned
worker process group. Candidate selection, parser/scan limits and skipped files
are reported explicitly. The soft source response target is 6 KiB; one coherent
definition with constants can exceed it through a 48 KiB source ceiling. The
encoded JSON response ceiling is 384 KiB, accounting for escaping and metadata.
Queries are at most 4,096 characters, symbols 200, relative paths 1,000, root
arguments 4,096, hits 1–12 and the encoded worker request 16 KiB. Native parser
hangs are bounded by terminating only the helper's owned process group.

This first version rebuilds an index per invocation and has different startup,
latency and resource characteristics from a persistent retrieval worker.
Graphify and semantic rerankers are not required or integrated in this version.
