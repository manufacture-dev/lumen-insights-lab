"""Build Claude Code session transcripts (JSONL) from history/sessions.py.

    python3 -I history/build_history.py <out-dir>

Writes one <session-id>.jsonl per session, in the transcript format of
Claude Code 2.1.311, plus memory/ as the sessions left it. Ids and
timestamps are derived from the sessions, so a rebuild gives the same files.
"""
import json
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sessions import MEMORY, REPO, SESSIONS  # noqa: E402

VERSION = "2.1.311"
MODEL = "claude-opus-5-5"
NS = uuid.UUID("6f1c0e2a-4b7d-4c1e-9a55-0d1e5ab1c0de")
B32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZabcdefghijkmnopqrstuvwxyz"


def uid(*parts):
    """A deterministic id shaped like the random (version 4) ids Claude Code writes."""
    return str(uuid.UUID(bytes=uuid.uuid5(NS, "/".join(map(str, parts))).bytes, version=4))


def short(prefix, *parts):
    n = uuid.uuid5(NS, "/".join(map(str, parts))).int
    out = ""
    while len(out) < 24:
        n, r = divmod(n, len(B32))
        out += B32[r]
    return prefix + out


def stamp(t):
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"


def usage(out_tokens):
    return {"input_tokens": 2, "cache_creation_input_tokens": 600, "cache_read_input_tokens": 19800,
            "output_tokens": out_tokens, "output_tokens_details": {"thinking_tokens": 0},
            "server_tool_use": {"web_search_requests": 0, "web_fetch_requests": 0}, "service_tier": "standard",
            "cache_creation": {"ephemeral_1h_input_tokens": 600, "ephemeral_5m_input_tokens": 0},
            "inference_geo": "global", "iterations": [], "speed": "standard", "fallback_credit": None}


def tool_result_payload(name, inp, output, failed):
    if name == "Bash":
        return ("Error: " + output) if failed else {"stdout": output, "stderr": "", "interrupted": False,
                                                    "isImage": False, "noOutputExpected": False}
    if name == "Read":
        lines = output.count("\n") + 1
        return {"type": "text", "file": {"filePath": inp["file_path"], "content": output, "numLines": lines,
                                         "startLine": 1, "totalLines": lines}}
    if name == "Write":
        return {"type": "create", "filePath": inp["file_path"], "content": inp["content"], "structuredPatch": [],
                "originalFile": None, "userModified": False}
    return output


def build(session):
    sid = uid(session["slug"])
    t = datetime.fromisoformat(session["start"])
    common = {"userType": "external", "entrypoint": "cli", "cwd": REPO, "sessionId": sid, "version": VERSION,
              "gitBranch": session["branch"]}
    rows = [{"type": "mode", "mode": "normal", "sessionId": sid},
            {"type": "permission-mode", "permissionMode": "default", "sessionId": sid}]
    parent, prompt_id, prompt_index, turn_start, last_prompt = None, None, 0, t, ""
    tools_used, k = [], 0
    msg_id, block, request = None, 0, None

    def tick(seconds):
        nonlocal t
        t = t + timedelta(seconds=seconds)
        return stamp(t)

    def assistant(content, stop):
        nonlocal parent, k, block
        k += 1
        row = {"parentUuid": parent, "isSidechain": False,
               "message": {"model": MODEL, "id": msg_id, "type": "message", "role": "assistant", "content": [content],
                           "container": None, "stop_reason": stop, "stop_sequence": None, "stop_details": None,
                           "usage": usage(40 + 3 * len(json.dumps(content)) // 10), "diagnostics": None,
                           "context_management": None},
               "apiBlockIndex": block, "requestRef": request, "requestedModel": MODEL, "type": "assistant",
               "uuid": uid(sid, k), "timestamp": tick(6), "effort": "medium", "perTurnEffort": "medium",
               "session_id": sid, **common}
        block += 1
        parent = row["uuid"]
        rows.append(row)
        return row

    def new_request():
        nonlocal msg_id, block, request
        msg_id, block, request = short("msg_011", sid, k, "msg"), 0, uid(sid, k, "request")

    def close_turn():
        nonlocal k, parent
        if prompt_id is None:
            return
        k += 1
        row = {"parentUuid": parent, "isSidechain": False, "type": "system", "subtype": "turn_duration",
               "durationMs": int((t - turn_start).total_seconds() * 1000), "messageCount": k, "timestamp": tick(0),
               "uuid": uid(sid, k), "isMeta": False, **common}
        rows.append(row)
        parent = row["uuid"]

    for turn in session["turns"]:
        kind = turn[0]
        if kind == "user":
            close_turn()
            k += 1
            prompt_index += 1
            prompt_id, turn_start, last_prompt = uid(sid, k, "prompt"), t, turn[1]
            tick(45)
            row = {"parentUuid": parent, "isSidechain": False, "promptId": prompt_id, "type": "user",
                   "message": {"role": "user", "content": turn[1]}, "uuid": uid(sid, k), "timestamp": stamp(t),
                   "permissionMode": "default", "origin": {"kind": "human"}, "promptSource": "typed",
                   "turnOrigin": "human", "turnPosition": {"promptIndex": prompt_index, "turnIndex": 1}, **common}
            rows.append({"type": "file-history-snapshot", "messageId": row["uuid"],
                         "snapshot": {"messageId": row["uuid"], "trackedFileBackups": {}, "timestamp": stamp(t)},
                         "isSnapshotUpdate": False})
            rows.append(row)
            parent = row["uuid"]
            new_request()
        elif kind == "say":
            assistant({"type": "text", "text": turn[1]}, "end_turn")
            new_request()
        else:
            name, inp, output = turn[1], turn[2], turn[3]
            failed = kind == "tool!"
            tool_id = short("toolu_01", sid, k, "tool")
            call = assistant({"type": "tool_use", "id": tool_id, "name": name, "input": inp,
                              "caller": {"type": "direct"}}, "tool_use")
            if name not in tools_used:
                tools_used.append(name)
            k += 1
            row = {"parentUuid": parent, "isSidechain": False, "promptId": prompt_id, "type": "user",
                   "message": {"role": "user", "content": [{"tool_use_id": tool_id, "type": "tool_result",
                                                            "content": output, "is_error": failed}]},
                   "uuid": uid(sid, k), "timestamp": tick(2),
                   "toolUseResult": tool_result_payload(name, inp, output, failed),
                   **({"sandboxed": False} if name == "Bash" else {}),
                   "sourceToolAssistantUUID": call["uuid"],
                   "permissionDecision": {"decision": "accept", "source": "user", "reasonType": "prompt"},
                   "session_id": sid, **common}
            rows.append(row)
            parent = row["uuid"]
            new_request()
    close_turn()
    rows.append({"type": "last-prompt", "lastPrompt": last_prompt[:200], "leafUuid": parent, "sessionId": sid})
    rows.append({"type": "ai-title", "aiTitle": session["title"], "sessionId": sid})
    rows.append({"type": "tools-used", "tools": tools_used, "sessionId": sid})
    return sid, rows


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    memory = {}
    for session in SESSIONS:
        sid, rows = build(session)
        (out / f"{sid}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        for turn in session["turns"]:
            if turn[0] == "tool" and turn[1] == "Write" and turn[2]["file_path"].startswith(MEMORY):
                memory[Path(turn[2]["file_path"]).name] = turn[2]["content"]
        print(sid, session["start"][:10], session["who"], session["title"])
    if memory:
        (out / "memory").mkdir(exist_ok=True)
        index = ["- [Tickets in the tracker](tickets-in-tracker.md) — where tickets live\n"]
        for name, content in memory.items():
            (out / "memory" / name).write_text(content)
        (out / "memory" / "MEMORY.md").write_text("".join(index))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "projects")
