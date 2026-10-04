#!/usr/bin/env python3
"""코테 기록 CLI (프로그래머스 Java)

  cote                    ★ 매일 이것만: 오늘 문제 열기 → 풀고 코드 복사 → Enter → 기록·GitHub 자동

  ./cote today            오늘 풀 문제 + 재풀이 + 레벨 게이지
  ./cote new 42576        문제 폴더 생성 (Solution.java + NOTE.md) + 브라우저로 문제 열기
  ./cote run 42576        로컬 실행 (Solution.main)
  ./cote done 42576       풀이 기록 → README 대시보드 갱신 → commit & push
  ./cote redo 42576       재풀이 기록 (해설 없이 다시 풀기)
  ./cote status [--json]  현재 위치 (루틴이 --json 사용)
"""
import csv, json, math, os, re, subprocess, sys, time
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
RECORDS = os.path.join(ROOT, "records.csv")
FIELDS = ["date", "platform", "id", "title", "level", "kind", "result", "minutes", "note", "path"]
RESULT = {"1": "✅", "2": "💡", "3": "❌"}
KST = timezone(timedelta(hours=9))


def today():
    return datetime.now(KST).date()


def load_cfg():
    with open(os.path.join(ROOT, "roadmap.json"), encoding="utf-8") as f:
        return json.load(f)


def load_records():
    if not os.path.exists(RECORDS):
        return []
    with open(RECORDS, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_problem(cfg, pid):
    for ph in cfg["phases"]:
        for p in ph["problems"]:
            if p["id"] == pid:
                return p, ph["key"]
    return None, None


def problem_dir(pid):
    base = os.path.join(ROOT, "programmers")
    for name in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        if name.split("_", 1)[0] == str(pid):
            return os.path.join(base, name)
    return None


def slug(title):
    return re.sub(r"[^\w가-힣\-]+", "_", title).strip("_")


def url(pid):
    return f"https://school.programmers.co.kr/learn/courses/30/lessons/{pid}"


# ---------- 진척도 계산 ----------

def best_status(records):
    """문제별 최종 상태: ✅ > 💡 > ❌"""
    rank = {"✅": 3, "💡": 2, "❌": 1}
    out = {}
    for r in records:
        pid = r["id"]
        if pid not in out or rank[r["result"]] > rank[out[pid]["result"]]:
            out[pid] = r
    return out


def xp_of(cfg, records):
    total = 0.0
    for r in best_status(records).values():
        base = cfg["xp"].get(str(r["level"]), 0)
        total += {"✅": base, "💡": base / 2, "❌": 0}[r["result"]]
    return total


def level_of(cfg, xp):
    a = cfg["level_anchors"]
    for (x0, l0), (x1, l1) in zip(a, a[1:]):
        if xp <= x1:
            return l0 + (l1 - l0) * (xp - x0) / (x1 - x0)
    return 100.0


def tier_of(cfg, lv):
    name = cfg["tiers"][0][1]
    for th, n in cfg["tiers"]:
        if lv >= th:
            name = n
    return name


def current_phase(cfg, d):
    for ph in cfg["phases"]:
        if ph["start"] <= d.isoformat() <= ph["end"]:
            return ph
    return cfg["phases"][0] if d.isoformat() < cfg["phases"][0]["start"] else cfg["phases"][-1]


def streak(records, d):
    days = {r["date"] for r in records}
    n, cur = 0, d
    if cur.isoformat() not in days:  # 오늘 아직 안 풀었으면 어제부터 센다
        cur -= timedelta(days=1)
    while cur.isoformat() in days:
        n += 1
        cur -= timedelta(days=1)
    return n


def week_range(d):
    start = d - timedelta(days=d.weekday())  # 월요일 시작
    return start, start + timedelta(days=6)


def due_redos(cfg, records, d):
    """💡/❌ 후 N일 지났고 아직 ✅로 안 바뀐 문제"""
    best = best_status(records)
    due = []
    for pid, r in best.items():
        if r["result"] == "✅":
            continue
        last = max(x["date"] for x in records if x["id"] == pid)
        when = date.fromisoformat(last) + timedelta(days=cfg["redo_after_days"])
        if when <= d:
            due.append({"id": int(pid), "title": r["title"], "level": int(r["level"]),
                        "last_result": r["result"], "due": when.isoformat(), "url": url(pid)})
    return sorted(due, key=lambda x: x["due"])


def next_new(cfg, records, d, n):
    tried = {r["id"] for r in records}
    ph = current_phase(cfg, d)
    order = [p for x in cfg["phases"][cfg["phases"].index(ph):] for p in x["problems"]]
    # 현재 페이즈 이전에 못 푼 문제가 남아 있으면 그것부터
    earlier = [p for x in cfg["phases"][:cfg["phases"].index(ph)] for p in x["problems"]]
    picks = [p for p in earlier + order if str(p["id"]) not in tried][:n]
    return [dict(p, url=url(p["id"])) for p in picks]


def status(cfg, records, d=None):
    d = d or today()
    xp = xp_of(cfg, records)
    lv = level_of(cfg, xp)
    ph = current_phase(cfg, d)
    ws, we = week_range(d)
    week_recs = [r for r in records if ws.isoformat() <= r["date"] <= we.isoformat()]
    today_recs = [r for r in records if r["date"] == d.isoformat()]
    best = best_status(records)
    by_level = {}
    for r in best.values():
        if r["result"] != "❌":
            by_level[r["level"]] = by_level.get(r["level"], 0) + 1
    nxt_target = next(((t, n) for t, n in cfg["targets"] if lv < t), None)
    all_ids = [p["id"] for x in cfg["phases"] for p in x["problems"]]
    done_ids = {int(k) for k, v in best.items() if v["result"] != "❌"}
    return {
        "date": d.isoformat(),
        "xp": round(xp, 1), "level": round(lv, 1), "tier": tier_of(cfg, lv),
        "next_target": {"level": nxt_target[0], "name": nxt_target[1]} if nxt_target else None,
        "targets": cfg["targets"],
        "solved_by_level": dict(sorted(by_level.items())),
        "roadmap_done": len([i for i in all_ids if i in done_ids]), "roadmap_total": len(all_ids),
        "streak_days": streak(records, d),
        "phase": {k: ph[k] for k in ("key", "name", "start", "end", "daily_min", "weekly_target", "focus")},
        "week": {"start": ws.isoformat(), "end": we.isoformat(), "done": len(week_recs), "target": ph["weekly_target"]},
        "today_done": [{k: r[k] for k in ("id", "title", "kind", "result", "minutes", "note")} for r in today_recs],
        "today_new": next_new(cfg, records, d, max(ph["daily_min"], 1)),
        "today_redo": due_redos(cfg, records, d),
    }


def bar(lv, width=30):
    filled = int(round(lv / 100 * width))
    return "█" * filled + "░" * (width - filled)


# ---------- README 대시보드 ----------

def render_readme(cfg, records):
    s = status(cfg, records)
    lines = [
        "# 코테 대시보드 (프로그래머스 · Java)",
        "",
        "> `cote.py`가 자동 생성하는 파일입니다. 직접 수정하지 마세요.",
        "",
        f"**Lv.{s['level']:.0f} / 100 · {s['tier']}** · XP {s['xp']} · 🔥 연속 {s['streak_days']}일",
        "",
        "```",
        f"[{bar(s['level'])}] {s['level']:.1f}",
        "```",
        "",
        "| 목표선 | 레벨 | 상태 |",
        "|---|---|---|",
    ]
    for t, n in cfg["targets"]:
        state = "✅ 도달" if s["level"] >= t else f"{t - s['level']:.1f} 남음"
        lines.append(f"| {n} | {t} | {state} |")
    lines += [
        "",
        f"- 현재 페이즈: **{s['phase']['key']} {s['phase']['name']}** ({s['phase']['start']} ~ {s['phase']['end']})",
        f"- 이번 주: {s['week']['done']} / {s['week']['target']}문제 (하루 최소 {s['phase']['daily_min']})",
        f"- 로드맵: {s['roadmap_done']} / {s['roadmap_total']}문제",
        f"- 레벨별 해결: " + ", ".join(f"Lv.{k} {v}개" for k, v in s["solved_by_level"].items()) if s["solved_by_level"] else "- 레벨별 해결: 아직 없음",
        "",
        "## 티어 기준 (자체 환산)",
        "",
        "| 레벨 | 티어 |",
        "|---|---|",
    ]
    tiers = cfg["tiers"]
    for i, (th, n) in enumerate(tiers):
        hi = tiers[i + 1][0] - 1 if i + 1 < len(tiers) else 100
        lines.append(f"| {th}–{hi} | {n} |")
    lines += ["", f"XP: Lv.0 0.5 · Lv.1 1 · Lv.2 3 · Lv.3 8 · Lv.4 15 · Lv.5 25 — {cfg['xp_rules']}", "",
              "## 풀이 기록", "", "| 날짜 | 문제 | Lv | 구분 | 결과 | 분 | 한 줄 기록 |", "|---|---|---|---|---|---|---|"]
    for r in reversed(records):
        link = f"[{r['id']} {r['title']}]({r['path']})" if r["path"] else f"{r['id']} {r['title']}"
        lines.append(f"| {r['date']} | {link} | {r['level']} | {'재풀이' if r['kind'] == 'redo' else '첫 풀이'} | {r['result']} | {r['minutes']} | {r['note']} |")
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------- 명령 ----------

def cmd_new(cfg, pid):
    p, _ = find_problem(cfg, pid)
    if problem_dir(pid):
        sys.exit(f"이미 있음: {problem_dir(pid)}")
    if not p:
        title = input("로드맵에 없는 문제예요. 제목: ").strip()
        level = int(input("레벨(0~5): ").strip())
        p = {"id": pid, "title": title, "level": level, "tags": []}
    d = os.path.join(ROOT, "programmers", f"{pid}_{slug(p['title'])}")
    os.makedirs(d)
    with open(os.path.join(ROOT, "_template", "Solution.java"), encoding="utf-8") as f:
        java = f.read()
    with open(os.path.join(d, "Solution.java"), "w", encoding="utf-8") as f:
        f.write(java)
    with open(os.path.join(ROOT, "_template", "NOTE.md"), encoding="utf-8") as f:
        note = f.read()
    note = (note.replace("{ID}", str(pid)).replace("{TITLE}", p["title"]).replace("{LEVEL}", str(p["level"]))
                .replace("{TAGS}", ", ".join(p["tags"]) or "-").replace("{URL}", url(pid)))
    with open(os.path.join(d, "NOTE.md"), "w", encoding="utf-8") as f:
        f.write(note)
    print(f"생성: {os.path.relpath(d, ROOT)}\n문제: {url(pid)}\n타이머 시작! 30~40분 고민 → 막히면 해설 → 덮고 다시 구현")
    if sys.platform == "darwin":
        subprocess.run(["open", url(pid)])  # 브라우저에서 문제 바로 열기


def cmd_run(pid):
    d = problem_dir(pid) or sys.exit(f"없음: {pid} (먼저 ./cote new {pid})")
    subprocess.run(["java", "Solution.java"], cwd=d)


def ask(prompt, valid=None):
    while True:
        v = input(prompt).strip()
        if not valid or v in valid:
            return v


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def cmd_record(cfg, pid, kind, minutes=None):
    d = problem_dir(pid)
    p, _ = find_problem(cfg, pid)
    if not d:
        sys.exit(f"없음: {pid} (먼저 ./cote new {pid})")
    if not p:
        m = re.search(r"Lv\.(\d)", open(os.path.join(d, "NOTE.md"), encoding="utf-8").read())
        p = {"id": pid, "title": os.path.basename(d).split("_", 1)[1].replace("_", " "), "level": int(m.group(1)) if m else 0}
    print(f"[{pid}] {p['title']} (Lv.{p['level']}) — {'재풀이' if kind == 'redo' else '첫 풀이'} 기록")
    res = RESULT[ask("결과? 1) ✅ 혼자 풀이  2) 💡 해설 참고  3) ❌ 미해결 : ", RESULT)]
    if minutes is None:
        minutes = ask("걸린 시간(분): ")
    else:
        print(f"걸린 시간: {minutes}분 (자동 측정)")
    note = ask("한 줄 기록 (핵심 아이디어 / 막힌 지점): ").replace("|", "/")
    rec = {"date": today().isoformat(), "platform": "programmers", "id": str(pid), "title": p["title"],
           "level": str(p["level"]), "kind": kind, "result": res, "minutes": minutes, "note": note,
           "path": os.path.relpath(d, ROOT)}
    new_file = not os.path.exists(RECORDS)
    with open(RECORDS, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        w.writerow(rec)
    records = load_records()
    render_readme(cfg, records)
    s = status(cfg, records)
    print(f"\nLv.{s['level']:.1f} {s['tier']} · XP {s['xp']} · 이번 주 {s['week']['done']}/{s['week']['target']} · 🔥 {s['streak_days']}일")

    prefix = "redo" if kind == "redo" else "solve"
    msg = f"{prefix}: PGS #{pid} {p['title']} {res} - {note}"
    git("add", ".")
    c = git("commit", "-m", msg)
    if c.returncode != 0:
        print(c.stdout + c.stderr)
        return
    push = git("push")
    print("GitHub push 완료 ✅" if push.returncode == 0 else f"push 실패 — 나중에 git push 해주세요\n{push.stderr}")
    if res != "✅":
        print(f"재풀이 예정: {(today() + timedelta(days=cfg['redo_after_days'])).isoformat()}")


def cmd_go(cfg):
    """하루 한 번 이것만: 오늘 문제 열기 → 풀기 → 코드 복사 → Enter → 기록·GitHub 자동"""
    s = status(cfg, load_records())
    if s["today_redo"]:
        pick, kind = s["today_redo"][0], "redo"
    elif s["today_new"]:
        pick, kind = s["today_new"][0], "first"
    else:
        sys.exit("로드맵 문제를 모두 풀었어요! 지원 기업 기출로 넘어가세요.")
    pid = pick["id"]
    done_today = len(s["today_done"])
    print(f"\n오늘 {done_today}문제 완료 · Lv.{s['level']:.1f} {s['tier']}")
    print(f"{'🔁 재풀이 (해설 없이!)' if kind == 'redo' else '🆕 새 문제'}: {pid} {pick['title']} (Lv.{pick['level']})\n")
    if problem_dir(pid):
        if sys.platform == "darwin":
            subprocess.run(["open", url(pid)])
        print(f"문제: {url(pid)}")
    else:
        cmd_new(cfg, pid)
    start = time.time()
    print("\n① 브라우저에서 문제를 풀고 제출하세요.")
    print("② 끝나면 프로그래머스 코드 창에서 ⌘A → ⌘C (코드 전체 복사)")
    input("③ 여기로 돌아와서 Enter ⏎ ")
    minutes = max(1, round((time.time() - start) / 60))
    code = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout if sys.platform == "darwin" else ""
    sol = os.path.join(problem_dir(pid), "Solution.java")
    if "solution" in code:
        with open(sol, "w", encoding="utf-8") as f:
            f.write(code if code.endswith("\n") else code + "\n")
        print("코드 저장 완료 ✅")
    else:
        print(f"⚠️ 클립보드에 코드가 없어서 저장 못 했어요. 나중에 {os.path.relpath(sol, ROOT)}에 붙여넣어 주세요.")
    cmd_record(cfg, pid, kind, minutes)
    print("\n오늘 몫 끝! 밤 11시에 노션 데브로그로 정리돼요. 한 문제 더 하려면 다시 cote")


def cmd_today(cfg, records):
    s = status(cfg, records)
    print(f"📅 {s['date']} · {s['phase']['key']} {s['phase']['name']}")
    print(f"[{bar(s['level'])}] Lv.{s['level']:.1f}/100 · {s['tier']} · 🔥 {s['streak_days']}일")
    if s["next_target"]:
        print(f"다음 목표선: {s['next_target']['name']} (Lv.{s['next_target']['level']})")
    print(f"이번 주 {s['week']['done']}/{s['week']['target']} · 오늘 완료 {len(s['today_done'])}/{s['phase']['daily_min']}")
    print(f"\n포커스: {s['phase']['focus']}\n")
    if s["today_redo"]:
        print("🔁 재풀이 (해설 없이):")
        for r in s["today_redo"]:
            print(f"   {r['id']} {r['title']} (Lv.{r['level']}, 지난 결과 {r['last_result']}) {r['url']}")
    print("🆕 새 문제:")
    for p in s["today_new"]:
        print(f"   {p['id']} {p['title']} (Lv.{p['level']} · {', '.join(p['tags'])}) {p['url']}")


def main():
    cfg = load_cfg()
    a = sys.argv[1:]
    if a and a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0] if a else "go"
    if cmd == "go":
        cmd_go(cfg)
        return
    if cmd == "today":
        cmd_today(cfg, load_records())
    elif cmd == "status":
        s = status(cfg, load_records())
        print(json.dumps(s, ensure_ascii=False, indent=1) if "--json" in a else
              f"Lv.{s['level']:.1f}/100 · {s['tier']} · XP {s['xp']} · 🔥 {s['streak_days']}일")
    elif cmd == "readme":
        render_readme(cfg, load_records())
    elif cmd in ("new", "run", "done", "redo") and len(a) > 1:
        pid = int(a[1])
        {"new": lambda: cmd_new(cfg, pid), "run": lambda: cmd_run(pid),
         "done": lambda: cmd_record(cfg, pid, "first"), "redo": lambda: cmd_record(cfg, pid, "redo")}[cmd]()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
