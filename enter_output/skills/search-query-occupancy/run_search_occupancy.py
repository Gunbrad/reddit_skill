#!/usr/bin/env python3
"""
Run the SmartContent search-occupancy workflow end to end (Stage 3).

Usage:
    set PLANNER_SESSION=<cookie value>        (Windows cmd)
    export PLANNER_SESSION=<cookie value>     (bash)
    python run_search_occupancy.py --config run_config.json --out 03_search

The cookie is read ONLY from the PLANNER_SESSION env var. Never hard-code it.

run_config.json shape:
{
  "project_name": "Enter Pro",
  "project_id": "enter-pro",            // optional: reuse existing project; else created from name
  "product_brief_path": "01_product_brief/product_brief.md",  // optional, for project creation
  "posts_per_query": 10,
  "search_directions": [
    {"direction_id": "direction_001", "query": "..."},
    {"direction_id": "direction_002", "query": "..."}
  ],
  "topic_card_count": 12,
  "topic_supplemental_context": "...",   // optional
  "chosen_direction_ids": []             // optional: if set, only these get maps+cards downloaded
}

Only uses the Python standard library (urllib) so it runs anywhere Python 3 exists.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

BASE = "https://smartcontent.shifenglab.com"

def session():
    s = os.environ.get("PLANNER_SESSION")
    if not s:
        sys.exit("ERROR: set PLANNER_SESSION env var to the planner_session cookie value.")
    return s

def call(method, path, body=None, raw=False):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Cookie", f"planner_session={session()}")
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            content = r.read()
            return content if raw else json.loads(content or b"null")
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode(errors="replace")
        print(f"HTTP {e.code} on {method} {path}: {body_txt}", file=sys.stderr)
        raise

def write(path, content, mode="w"):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, mode, encoding=None if "b" in mode else "utf-8") as f:
        f.write(content)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default="03_search")
    ap.add_argument("--poll", type=int, default=10, help="run poll interval seconds")
    args = ap.parse_args()
    cfg = json.load(open(args.config, encoding="utf-8"))
    out = args.out

    me = call("GET", "/api/auth/me")
    print("auth ok:", me)

    pid = cfg.get("project_id")
    if not pid:
        brief = ""
        bp = cfg.get("product_brief_path")
        if bp and os.path.exists(bp):
            brief = open(bp, encoding="utf-8").read()
        proj = call("POST", "/api/search-occupancy/projects", {
            "name": cfg["project_name"], "product_brief": brief,
            "notes": cfg.get("notes", "search-occupancy run via skill script")})
        pid = proj["project_id"]
        print("created project:", pid)
    else:
        print("reusing project:", pid)

    run = call("POST", f"/api/search-occupancy/projects/{pid}/runs", {
        "posts_per_query": cfg.get("posts_per_query", 10),
        "search_directions": cfg["search_directions"]})
    rid = run["run_id"]
    print("created run:", rid)

    call("POST", f"/api/search-occupancy/projects/{pid}/runs/{rid}/prepare-all")
    print("prepare-all started; polling...")
    while True:
        st = call("GET", f"/api/search-occupancy/projects/{pid}/runs/{rid}")
        print(f"  stage={st.get('current_stage')} status={st.get('status')}")
        if st.get("status") in ("succeeded", "failed", "error"):
            break
        time.sleep(args.poll)

    summary = st.get("search_occupancy_map_summary") or {}
    dirs = summary.get("directions", [])
    success = [d["direction_id"] for d in dirs if d.get("status") == "success"]
    print("success directions:", success)
    print("failed directions:", [d["direction_id"] for d in dirs if d.get("status") != "success"])

    chosen = cfg.get("chosen_direction_ids") or success
    write(os.path.join(out, "run_status.json"), json.dumps(st, ensure_ascii=False, indent=2))

    for did in chosen:
        base = f"/api/search-occupancy/projects/{pid}/runs/{rid}"
        for kind, suffix, fn in [
            ("map_md",  f"/search-occupancy-maps/{did}/download/map_md",  f"maps/{did}.md"),
            ("map_json",f"/search-occupancy-maps/{did}/download/map_json",f"maps/{did}.json"),
            ("urls",    f"/search-urls/{did}/download/json",              f"materials/{did}/search_urls.json"),
            ("raw",     f"/search-materials/{did}/download/raw_posts_md", f"materials/{did}/raw_posts.md"),
        ]:
            try:
                write(os.path.join(out, fn), call("GET", base + suffix, raw=True), "wb")
                print("  downloaded", fn)
            except Exception as e:
                print("  skip", fn, e)
        # generate topic cards
        try:
            gen = call("POST", base + f"/directions/{did}/topic-cards/generate", {
                "count": cfg.get("topic_card_count", 12),
                "supplemental_context": cfg.get("topic_supplemental_context"),
                "overwrite": True})
            print(f"  generated {gen.get('generated_count')} cards for {did}")
            write(os.path.join(out, f"topic_cards/{did}.md"),
                  call("GET", base + f"/directions/{did}/download/topic_cards_md", raw=True), "wb")
            cards = call("GET", base + f"/directions/{did}/topic-cards")
            write(os.path.join(out, f"topic_cards/{did}.json"),
                  json.dumps(cards, ensure_ascii=False, indent=2))
        except Exception as e:
            print("  topic-card error", did, e)

    meta = {"project_id": pid, "run_id": rid,
            "direction_ids": [d["direction_id"] for d in cfg["search_directions"]],
            "success_direction_ids": success, "chosen_direction_ids": chosen,
            "posts_per_query": cfg.get("posts_per_query", 10)}
    write(os.path.join(out, "run_meta.json"), json.dumps(meta, ensure_ascii=False, indent=2))
    print("done. run_meta.json written. (cookie NOT stored)")

if __name__ == "__main__":
    main()
