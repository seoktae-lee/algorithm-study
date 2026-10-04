#!/usr/bin/env python3
"""코테 기록 CLI (프로그래머스 Java)

  cote                    ★ 매일 이것만: 오늘 문제 열기 → 풀고 코드 복사 → Enter → 기록·GitHub 자동

  ./cote today            오늘 풀 문제 + 재풀이 + 레벨 게이지
  ./cote new 42576        문제 폴더 생성 (Solution.java + NOTE.md) + 브라우저로 문제 열기
  ./cote run 42576        로컬 실행 (Solution.main)
  ./cote done 42576       풀이 기록 → README 대시보드 갱신 → commit & push
  ./cote redo 42576       복습 기록 (망각곡선 1→3→7→14→30→60일, 보통은 cote가 알아서 띄움)
  ./cote plan             앞으로 2주 복습 일정
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


def problem_tags(cfg, pid):
    p, _ = find_problem(cfg, int(pid))
    return p["tags"] if p else []


def curve_for(cfg, level):
    return cfg["review_curve"].get(str(level), cfg["review_curve"]["3"])


def review_schedule(cfg, records):
    """망각곡선 복습 상태: stage = 다음 복습이 curve의 몇 번째 간격인지 (len이면 졸업)"""
    sched = {}
    for r in sorted(records, key=lambda x: x["date"]):
        pid, ok = r["id"], r["result"] == "✅"
        curve = curve_for(cfg, r["level"])
        st = sched.get(pid)
        if r["kind"] == "first" or st is None:
            stage = 0                      # 첫 풀이는 결과와 무관하게 1일 뒤부터
        else:
            stage = st["stage"] + 1 if ok else 0   # 성공 → 다음 간격, 실패 → 1일부터 다시
        due = (date.fromisoformat(r["date"]) + timedelta(days=curve[stage])).isoformat() if stage < len(curve) else None
        sched[pid] = {"id": int(pid), "title": r["title"], "level": int(r["level"]), "stage": stage,
                      "interval": curve[stage] if stage < len(curve) else None, "round": stage + 1, "rounds": len(curve),
                      "last": r["date"], "last_result": r["result"], "due": due}
    return sched


def review_queue(cfg, records, d):
    """오늘 복습할 문제 (우선순위: 실패한 것 → 간격 대비 많이 밀린 것 → 간격 짧은 것)"""
    due = []
    for x in review_schedule(cfg, records).values():
        if not x["due"] or x["due"] > d.isoformat() or x["last"] == d.isoformat():
            continue
        late = (d - date.fromisoformat(x["due"])).days
        quick = x["interval"] <= cfg["quick_review_max_interval"]
        mode = "빠른 회상 10분" if quick else "재풀이"
        reason = ("약점 재도전 · " if x["last_result"] != "✅" else "") + f"{x['interval']}일 차 {mode} ({x['round']}/{x['rounds']}회)"
        if late:
            reason += f" · {late}일 밀림"
        due.append(dict(x, reason=reason, quick=quick, late=late, url=url(x["id"]), tags=problem_tags(cfg, x["id"])))
    return sorted(due, key=lambda x: (x["last_result"] == "✅", -(x["late"] + 1) / x["interval"], x["interval"]))


def weak_tags(cfg, records, top=3):
    """💡·❌가 나온 유형 집계 → 약점 유형"""
    cnt = {}
    for r in records:
        if r["result"] != "✅":
            for t in problem_tags(cfg, r["id"]):
                if t not in ("고득점Kit", "카카오"):
                    cnt[t] = cnt.get(t, 0) + 1
    return [t for t, _ in sorted(cnt.items(), key=lambda x: -x[1])[:top]]


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
    sched = review_schedule(cfg, records)
    queue = review_queue(cfg, records, d)
    quick = [x for x in queue if x["quick"]]
    full = [x for x in queue if not x["quick"]]
    backlog = max(0, len(full) - ph["review_cap"])
    # 망각곡선 유지 우선: 재풀이가 밀려 있으면 새 문제는 하루 1개로 줄인다
    n_new = 1 if backlog else max(ph["daily_min"], 1)
    return {
        "date": d.isoformat(),
        "xp": round(xp, 1), "level": round(lv, 1), "tier": tier_of(cfg, lv),
        "next_target": {"level": nxt_target[0], "name": nxt_target[1]} if nxt_target else None,
        "targets": cfg["targets"],
        "solved_by_level": dict(sorted(by_level.items())),
        "roadmap_done": len([i for i in all_ids if i in done_ids]), "roadmap_total": len(all_ids),
        "streak_days": streak(records, d),
        "phase": {k: ph[k] for k in ("key", "name", "start", "end", "daily_min", "weekly_target", "review_cap", "focus")},
        "week": {"start": ws.isoformat(), "end": we.isoformat(), "done": len(week_recs), "target": ph["weekly_target"]},
        "today_done": [{k: r[k] for k in ("id", "title", "kind", "result", "minutes", "note")} for r in today_recs],
        "today_new": next_new(cfg, records, d, n_new),
        "today_redo": sorted(quick + full[:ph["review_cap"]], key=queue.index),
        "review_backlog": backlog,
        "review_rules": cfg["review_rules"],
        "mastered": sum(1 for x in sched.values() if x["due"] is None),
        "weak_tags": weak_tags(cfg, records),
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
        f"- 로드맵: {s['roadmap_done']} / {s['roadmap_total']}문제 · 복습 졸업 🎓 {s['mastered']}문제",
        f"- 오늘 복습: " + (", ".join(f"{r['id']} {r['title']}({r['reason']})" for r in s["today_redo"]) or "없음")
        + (f" · 밀린 복습 {s['review_backlog']}개" if s["review_backlog"] else ""),
        f"- 약점 유형: " + (", ".join(s["weak_tags"]) or "아직 없음"),
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
    lines += ["", f"복습 규칙: {cfg['review_rules']}"]
    lines += ["", f"XP: Lv.0 0.5 · Lv.1 1 · Lv.2 3 · Lv.3 8 · Lv.4 15 · Lv.5 25 — {cfg['xp_rules']}", "",
              "## 풀이 기록", "", "| 날짜 | 문제 | Lv | 구분 | 결과 | 분 | 한 줄 기록 |", "|---|---|---|---|---|---|---|"]
    for r in reversed(records):
        link = f"[{r['id']} {r['title']}]({r['path']})" if r["path"] else f"{r['id']} {r['title']}"
        lines.append(f"| {r['date']} | {link} | {r['level']} | {'복습' if r['kind'] == 'redo' else '첫 풀이'} | {r['result']} | {r['minutes']} | {r['note']} |")
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
    print(f"[{pid}] {p['title']} (Lv.{p['level']}) — {'복습' if kind == 'redo' else '첫 풀이'} 기록")
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

    nxt = review_schedule(cfg, records).get(str(pid))
    if nxt and nxt["due"]:
        print(f"다음 복습: {nxt['due']} (아침 메일에 🔁로 나와요)")
    elif nxt:
        print("🎓 졸업! 이 문제는 더 이상 복습하지 않아요")

    prefix = "redo" if kind == "redo" else "solve"
    msg = f"{prefix}: PGS #{pid} {p['title']} {res} - {note}"
    git("add", ".")
    c = git("commit", "-m", msg)
    if c.returncode != 0:
        print(c.stdout + c.stderr)
        return
    push = git("push")
    print("GitHub push 완료 ✅" if push.returncode == 0 else f"push 실패 — 나중에 git push 해주세요\n{push.stderr}")


def solve_one(cfg, pick, kind):
    """문제 하나: 브라우저 열기 → 타이머 → 코드 복사 → Enter → 기록·GitHub"""
    pid = pick["id"]
    if kind == "redo":
        print(f"\n🔁 복습 · {pid} {pick['title']} (Lv.{pick['level']}) — {pick['reason']}")
        if pick.get("quick"):
            print("   빠른 회상: 문제 읽고 1분간 접근을 말로 정리 → 10분 안에 코딩. 이전 코드·해설은 보지 않기")
        else:
            print("   이전 코드·해설 보지 말고 빈 화면에서 처음부터! (프로그래머스 '초기화' 버튼으로 코드 비우기)")
    else:
        print(f"\n🆕 새 문제 · {pid} {pick['title']} (Lv.{pick['level']} · {', '.join(pick.get('tags', []))})")
    if problem_dir(pid):
        print(f"문제: {url(pid)}")
        if sys.platform == "darwin":
            subprocess.run(["open", url(pid)])
    else:
        cmd_new(cfg, pid)
    start = time.time()
    print("\n① 브라우저에서 풀고 제출")
    print("② 프로그래머스 코드 창에서 ⌘A → ⌘C (코드 전체 복사)")
    input("③ 여기로 돌아와서 Enter ⏎ ")
    minutes = max(1, round((time.time() - start) / 60))
    code = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout if sys.platform == "darwin" else ""
    d = problem_dir(pid)
    # 첫 풀이는 Solution.java, 복습은 날짜별 파일로 따로 저장 (이전 풀이와 비교 가능)
    name = "Solution.java" if kind == "first" else f"Solution_{today().strftime('%Y%m%d')}.java"
    if "solution" in code:
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(code if code.endswith("\n") else code + "\n")
        print(f"코드 저장 완료 ✅ ({name})")
    else:
        print(f"⚠️ 클립보드에 코드가 없어서 저장 못 했어요. 나중에 {os.path.relpath(os.path.join(d, name), ROOT)}에 붙여넣어 주세요.")
    cmd_record(cfg, pid, kind, minutes)


def cmd_go(cfg):
    """하루 한 번 이것만: 오늘 분량(복습 + 새 문제)을 순서대로 진행"""
    s = status(cfg, load_records())
    redo = [(r, "redo") for r in s["today_redo"]]
    plan = redo[:1] + [(p, "first") for p in s["today_new"]] + redo[1:]
    if not plan:
        sys.exit("오늘 분량 끝! 더 하고 싶으면 내일 문제를 미리 봐도 돼요: ./cote today")
    print(f"\n📅 {s['date']} · Lv.{s['level']:.1f} {s['tier']} · 🔥 {s['streak_days']}일 · 오늘 완료 {len(s['today_done'])}개")
    print("오늘 분량 (⭐ = 바쁘면 이것만):")
    for i, (p, k) in enumerate(plan):
        tag = "🔁 복습" if k == "redo" else "🆕 새 문제"
        print(f"  {'⭐' if i == 0 else '  '} {tag} {p['id']} {p['title']} (Lv.{p['level']})" + (f" — {p['reason']}" if k == "redo" else ""))
    if s["review_backlog"]:
        print(f"  (밀린 복습 {s['review_backlog']}개는 내일 이후로 자동 배치)")
    for i, (p, k) in enumerate(plan):
        if i > 0:
            nxt = f"{'🔁 복습' if k == 'redo' else '🆕 새 문제'} {p['id']} {p['title']}"
            if input(f"\n다음: {nxt} — 계속할까요? (Enter=계속 / q=오늘은 여기까지) ").strip().lower() == "q":
                break
        solve_one(cfg, p, k)
        if i == 0:
            print("\n✅ 오늘 최소 분량 달성! 연속일 유지돼요.")
    print("\n오늘 끝! 밤 11시에 노션 데브로그로 정리돼요.")


def cmd_plan(cfg, records, days=14):
    """앞으로 N일 복습 일정 (망각곡선)"""
    sched = review_schedule(cfg, records)
    d0 = today()
    for i in range(days):
        d = (d0 + timedelta(days=i)).isoformat()
        items = [x for x in sched.values() if x["due"] and (x["due"] == d or (i == 0 and x["due"] < d))]
        if items:
            print(f"{d}: " + ", ".join(f"{x['id']} {x['title']}({x['interval']}일 차)" for x in items))
    print(f"🎓 졸업 {sum(1 for x in sched.values() if x['due'] is None)}문제")


def cmd_today(cfg, records):
    s = status(cfg, records)
    print(f"📅 {s['date']} · {s['phase']['key']} {s['phase']['name']}")
    print(f"[{bar(s['level'])}] Lv.{s['level']:.1f}/100 · {s['tier']} · 🔥 {s['streak_days']}일")
    if s["next_target"]:
        print(f"다음 목표선: {s['next_target']['name']} (Lv.{s['next_target']['level']})")
    print(f"이번 주 {s['week']['done']}/{s['week']['target']} · 오늘 완료 {len(s['today_done'])}/{s['phase']['daily_min']}")
    print(f"\n포커스: {s['phase']['focus']}\n")
    if s["today_redo"]:
        print("🔁 복습 (해설·이전 코드 없이):")
        for r in s["today_redo"]:
            print(f"   {r['id']} {r['title']} (Lv.{r['level']}, {r['reason']}) {r['url']}")
        if s["review_backlog"]:
            print(f"   + 밀린 복습 {s['review_backlog']}개")
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
    elif cmd == "plan":
        cmd_plan(cfg, load_records())
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
