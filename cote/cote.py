#!/usr/bin/env python3
"""코테 기록 CLI (프로그래머스 Java)

  cote                    ★ 매일 이것만: 복습 + 새 문제 + (화·금) SQL을 순서대로 → 코드 복사 → Enter → 기록·GitHub 자동
  cote mock               📝 모의고사 (처음 보는 문제, 시간 제한) — 예정일이면 cote가 알려줌
  cote ext                외부 문제 기록 (백준·SWEA·LeetCode 등 처음 보는 문제)
  cote track [이름 on|off] 트랙 보기/켜기 (sql, samsung, boj)
  cote note [--all]       📘 핵심노트 PDF 발행 (복습 거친 문제 10개 모이면 cote가 먼저 물어봄) / --all 전체판만 재생성
  (자바 기초는 터미널에서 `java` — ~/dev/algorithm-study/java)

  cote today              오늘 분량 + 레벨 + 실전 정답률
  cote plan               앞으로 2주 복습 일정
  cote status [--json]    현재 위치 (루틴이 --json 사용)
  cote new|run|done|redo <번호>   수동 모드 (보통은 안 써도 됨)
"""
import csv, json, os, random, re, subprocess, sys, time
from datetime import date, datetime, timedelta, timezone

import notebook

ROOT = os.path.dirname(os.path.abspath(__file__))
RECORDS = os.path.join(ROOT, "records.csv")
MOCKS = os.path.join(ROOT, "mocks.csv")
EXT = os.path.join(ROOT, "ext.json")
FIELDS = ["date", "platform", "id", "title", "level", "kind", "result", "minutes", "note", "path"]
MOCK_FIELDS = ["date", "name", "format", "total", "solved", "minutes", "limit"]
RESULT = {"1": "✅", "2": "💡", "3": "❌"}
KST = timezone(timedelta(hours=9))
DIRS = {"programmers": "programmers", "sql": "sql", "ext": "ext"}


def today():
    return datetime.now(KST).date()


def load_cfg():
    with open(os.path.join(ROOT, "roadmap.json"), encoding="utf-8") as f:
        return json.load(f)


def save_cfg(cfg):
    with open(os.path.join(ROOT, "roadmap.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)


def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_csv(path, fields, row):
    new_file = not os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new_file:
            w.writeheader()
        w.writerow(row)


def load_records():
    return load_csv(RECORDS)


def load_ext():
    if not os.path.exists(EXT):
        return {}
    with open(EXT, encoding="utf-8") as f:
        return json.load(f)


def slug(title):
    return re.sub(r"[^\w가-힣\-]+", "_", title).strip("_")


def pgs_url(pid):
    return f"https://school.programmers.co.kr/learn/courses/30/lessons/{pid}"


# ---------- 문제 찾기 (로드맵 · 모의고사 풀 · SQL 트랙 · 외부 문제) ----------

def get_problem(cfg, pid):
    """id(문자열)로 문제 정보 찾기 → {id, title, level, tags, platform, url, phase}"""
    pid = str(pid)
    for ph in cfg["phases"]:
        for p in ph["problems"]:
            if str(p["id"]) == pid:
                return dict(p, id=pid, platform="programmers", url=pgs_url(pid), phase=ph["key"])
    mock = cfg["mock"]
    for p in mock["pool"] + [q for s in mock["official_sets"] for q in s["problems"]]:
        if str(p["id"]) == pid:
            return dict(p, id=pid, tags=[], platform="programmers", url=pgs_url(pid), phase="모의고사")
    for p in cfg["tracks"]["sql"]["problems"]:
        if str(p["id"]) == pid:
            return dict(p, id=pid, tags=["SQL"], platform="sql", url=pgs_url(pid), phase="SQL")
    ext = load_ext()
    if pid in ext:
        return dict(ext[pid], id=pid, tags=[], platform="ext", phase="외부")
    return None


def problem_dir(pid, platform="programmers"):
    base = os.path.join(ROOT, DIRS[platform])
    for name in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        if name.split("_", 1)[0] == str(pid):
            return os.path.join(base, name)
    return None


def make_dir(p):
    """문제 폴더 생성: 코드 템플릿 + NOTE.md"""
    d = problem_dir(p["id"], p["platform"])
    if d:
        return d
    d = os.path.join(ROOT, DIRS[p["platform"]], f"{p['id']}_{slug(p['title'])}")
    os.makedirs(d)
    code_name = "solution.sql" if p["platform"] == "sql" else "Solution.java"
    if p["platform"] != "sql":
        with open(os.path.join(ROOT, "_template", "Solution.java"), encoding="utf-8") as f:
            java = f.read()
        with open(os.path.join(d, code_name), "w", encoding="utf-8") as f:
            f.write(java)
    with open(os.path.join(ROOT, "_template", "NOTE.md"), encoding="utf-8") as f:
        note = f.read()
    note = (note.replace("{ID}", p["id"]).replace("{TITLE}", p["title"]).replace("{LEVEL}", str(p["level"]))
                .replace("{TAGS}", ", ".join(p.get("tags", [])) or "-").replace("{URL}", p["url"]))
    with open(os.path.join(d, "NOTE.md"), "w", encoding="utf-8") as f:
        f.write(note)
    return d


def open_url(u):
    if sys.platform == "darwin":
        subprocess.run(["open", u])


def java_status():
    """자바 기초 CLI(java/jv.py)의 오늘 상태 — 없거나 실패하면 None"""
    jv = os.path.join(os.path.dirname(ROOT), "java", "jv.py")
    if not os.path.exists(jv):
        return None
    try:
        p = subprocess.run([sys.executable, jv, "status", "--json"], capture_output=True, text=True, timeout=20)
        return json.loads(p.stdout)
    except Exception:
        return None


# ---------- 진척도 계산 ----------

def algo(records):
    """레벨·복습 계산 대상 (SQL 트랙은 별도 집계)"""
    return [r for r in records if r["platform"] != "sql"]


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
    for r in best_status(algo(records)).values():
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


# ---------- 망각곡선 복습 ----------

def curve_for(cfg, level):
    return cfg["review_curve"].get(str(level), cfg["review_curve"]["3"])


def review_schedule(cfg, records):
    """망각곡선 복습 상태: stage = 다음 복습이 curve의 몇 번째 간격인지 (len이면 졸업)"""
    sched = {}
    for r in sorted(algo(records), key=lambda x: x["date"]):
        pid, ok = r["id"], r["result"] == "✅"
        curve = curve_for(cfg, r["level"])
        st = sched.get(pid)
        if r["kind"] != "redo" or st is None:
            stage = 0                      # 첫 풀이·모의고사는 결과와 무관하게 1일 뒤부터
        else:
            stage = st["stage"] + 1 if ok else 0   # 성공 → 다음 간격, 실패 → 1일부터 다시
        due = (date.fromisoformat(r["date"]) + timedelta(days=curve[stage])).isoformat() if stage < len(curve) else None
        sched[pid] = {"id": pid, "title": r["title"], "level": int(r["level"]), "platform": r["platform"], "stage": stage,
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
        p = get_problem(cfg, x["id"]) or {}
        due.append(dict(x, reason=reason, quick=quick, late=late, url=p.get("url", pgs_url(x["id"])), tags=p.get("tags", [])))
    return sorted(due, key=lambda x: (x["last_result"] == "✅", -(x["late"] + 1) / x["interval"], x["interval"]))


def weak_tags(cfg, records, top=3):
    """💡·❌가 나온 유형 집계 → 약점 유형"""
    cnt = {}
    for r in algo(records):
        if r["result"] != "✅":
            for t in (get_problem(cfg, r["id"]) or {}).get("tags", []):
                if t not in ("고득점Kit", "카카오"):
                    cnt[t] = cnt.get(t, 0) + 1
    return [t for t, _ in sorted(cnt.items(), key=lambda x: -x[1])[:top]]


def next_new(cfg, records, d, n):
    tried = {r["id"] for r in records}
    ph = current_phase(cfg, d)
    i = cfg["phases"].index(ph)
    # 이전 페이즈에 못 푼 문제가 남아 있으면 그것부터
    order = [p for x in cfg["phases"][:i] + cfg["phases"][i:] for p in x["problems"]]
    picks = [p for p in order if str(p["id"]) not in tried][:n]
    return [dict(p, id=str(p["id"]), platform="programmers", url=pgs_url(p["id"])) for p in picks]


# ---------- 모의고사 · 실전 정답률 ----------

def mock_schedule(cfg, d):
    active = [s for s in cfg["mock"]["schedule"] if s["from"] <= d.isoformat()]
    return active[-1] if active else None


def next_mock(cfg, d):
    """다음 모의고사 날짜와 형식 (일정 시작 전이면 첫 예정일)"""
    sch = mock_schedule(cfg, d) or cfg["mock"]["schedule"][0]
    mocks = load_csv(MOCKS)
    last = max((m["date"] for m in mocks), default=None)
    nxt = date.fromisoformat(sch["from"])
    if last:
        nxt = max(nxt, date.fromisoformat(last) + timedelta(days=sch["every_days"]))
    fmt = cfg["mock"]["formats"][sch["format"]]
    return {"date": nxt.isoformat(), "due": nxt <= d, "format": sch["format"], "minutes": fmt["minutes"],
            "count": len(fmt["levels"]), "every_days": sch["every_days"], "done": len(mocks)}


def pick_mock(cfg, d, fmt_name):
    """공식 기출 세트(해금일 이후, 전부 미공개일 때) 우선, 아니면 풀에서 레벨별 무작위 출제"""
    tried = {r["id"] for r in load_records()}
    for s in cfg["mock"]["official_sets"]:
        if s["not_before"] <= d.isoformat() and not any(str(p["id"]) in tried for p in s["problems"]):
            return s["name"], [dict(p, id=str(p["id"])) for p in s["problems"]], s["minutes"]
    fmt = cfg["mock"]["formats"][fmt_name]
    official_ids = {str(p["id"]) for s in cfg["mock"]["official_sets"] for p in s["problems"]}
    left = [dict(p, id=str(p["id"])) for p in cfg["mock"]["pool"] if str(p["id"]) not in tried | official_ids]
    rnd = random.Random(d.isoformat())
    rnd.shuffle(left)
    picks = []
    for lv in fmt["levels"]:
        if not left:
            break
        best = min(left, key=lambda p: abs(p["level"] - lv))  # 해당 레벨이 소진되면 가장 가까운 레벨
        picks.append(best)
        left.remove(best)
    return f"{fmt_name} 모의고사", sorted(picks, key=lambda p: p["level"]), fmt["minutes"]


def readiness(cfg, records):
    """처음 보는 문제(모의고사·외부 첫 풀이)로 본 레벨별 실전 정답률과 지원 라인 판정"""
    rc = cfg["readiness"]
    firsts = {}
    for r in sorted(algo(records), key=lambda x: x["date"]):
        if r["id"] not in firsts and (r["kind"] == "mock" or r["platform"] == "ext"):
            firsts[r["id"]] = r
    by = {}
    for r in sorted(firsts.values(), key=lambda x: x["date"]):
        box = rc["time_box"].get(str(r["level"]), 120)
        ok = r["result"] == "✅" and (r["kind"] == "mock" or int(r["minutes"] or 999) <= box)
        by.setdefault(str(r["level"]), []).append(ok)
    stats = {lv: {"n": len(v[-10:]), "acc": round(sum(v[-10:]) / len(v[-10:]), 2)} for lv, v in sorted(by.items())}
    verdicts = []
    for c in rc["criteria"]:
        parts, met = [], True
        for lv, need in c["need"].items():
            s = stats.get(lv)
            if not s or s["n"] < 3:
                met = False
                parts.append(f"Lv.{lv} 표본 부족({s['n'] if s else 0}/3)")
            else:
                met &= s["acc"] >= need
                parts.append(f"Lv.{lv} {s['acc']:.0%}/{need:.0%}")
        verdicts.append({"name": c["name"], "met": met, "detail": " · ".join(parts)})
    return {"by_level": stats, "verdicts": verdicts}


# ---------- 트랙 (SQL · 삼성 · 백준) ----------

def tracks_today(cfg, records, d):
    out = []
    tried = {r["id"] for r in records}
    for key, t in cfg["tracks"].items():
        if not t["enabled"] or d.weekday() not in t["weekdays"] or t.get("start", "") > d.isoformat():
            continue
        if key == "sql":
            if any(r["platform"] == "sql" and r["date"] == d.isoformat() for r in records):
                continue
            left = [p for p in t["problems"] if str(p["id"]) not in tried]
            if left:
                p = left[0]
                out.append({"track": key, "id": str(p["id"]), "title": p["title"], "level": p["level"],
                            "url": pgs_url(p["id"]), "platform": "sql", "tags": ["SQL"]})
        else:
            out.append({"track": key, "title": t["name"], "url": t.get("url"), "why": t["why"]})
    return out


def sql_progress(cfg, records):
    done = {r["id"] for r in records if r["platform"] == "sql" and r["result"] == "✅"}
    return {"done": len(done), "total": len(cfg["tracks"]["sql"]["problems"])}


# ---------- 상태 ----------

def status(cfg, records, d=None):
    d = d or today()
    xp = xp_of(cfg, records)
    lv = level_of(cfg, xp)
    ph = current_phase(cfg, d)
    ws, we = week_range(d)
    week_recs = [r for r in records if ws.isoformat() <= r["date"] <= we.isoformat()]
    today_recs = [r for r in records if r["date"] == d.isoformat()]
    best = best_status(algo(records))
    by_level = {}
    for r in best.values():
        if r["result"] != "❌":
            by_level[r["level"]] = by_level.get(r["level"], 0) + 1
    nxt_target = next(((t, n) for t, n in cfg["targets"] if lv < t), None)
    all_ids = [str(p["id"]) for x in cfg["phases"] for p in x["problems"]]
    done_ids = {k for k, v in best.items() if v["result"] != "❌"}
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
        "today_done": [{k: r[k] for k in ("id", "title", "platform", "kind", "result", "minutes", "note")} for r in today_recs],
        "today_new": next_new(cfg, records, d, n_new),
        "today_redo": sorted(quick + full[:ph["review_cap"]], key=queue.index),
        "review_backlog": backlog,
        "review_rules": cfg["review_rules"],
        "mastered": sum(1 for x in sched.values() if x["due"] is None),
        "weak_tags": weak_tags(cfg, records),
        "tracks_today": tracks_today(cfg, records, d),
        "sql_progress": sql_progress(cfg, records),
        "mock": next_mock(cfg, d),
        "readiness": readiness(cfg, records),
        "milestones": cfg["milestones"],
        "notebook": notebook.progress(records),
        "java": java_status(),
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
        f"- 로드맵: {s['roadmap_done']} / {s['roadmap_total']}문제 · 복습 졸업 🎓 {s['mastered']}문제 · SQL {s['sql_progress']['done']} / {s['sql_progress']['total']}",
        "- 레벨별 해결: " + (", ".join(f"Lv.{k} {v}개" for k, v in s["solved_by_level"].items()) or "아직 없음"),
        "- 오늘 복습: " + (", ".join(f"{r['id']} {r['title']}({r['reason']})" for r in s["today_redo"]) or "없음")
        + (f" · 밀린 복습 {s['review_backlog']}개" if s["review_backlog"] else ""),
        "- 약점 유형: " + (", ".join(s["weak_tags"]) or "아직 없음"),
        f"- 📘 핵심노트: 발행 {s['notebook']['next_vol'] - 1}권 · 다음 Vol.{s['notebook']['next_vol']}까지 {s['notebook']['ready']} / {s['notebook']['threshold']}문제 ([notes/](notes/))",
        (f"- ☕ 자바 기초: {s['java']['done']} / {s['java']['total']}레슨 · 카드 졸업 {s['java']['mastered']} ([java/](../java/README.md))" if s.get("java") else "- ☕ 자바 기초: -"),
        "",
        "## 실전 정답률 (처음 보는 문제 기준)",
        "",
        f"> {cfg['readiness']['about']}",
        "",
        "| 지원 라인 | 판정 | 근거 |",
        "|---|---|---|",
    ]
    for v in s["readiness"]["verdicts"]:
        lines.append(f"| {v['name']} | {'✅ 준비됨' if v['met'] else '⏳ 아직'} | {v['detail']} |")
    m = s["mock"]
    lines += ["", f"다음 모의고사: **{m['date']}** ({m['format']}, {m['count']}문제 {m['minutes']}분) · 지금까지 {m['done']}회", ""]
    mocks = load_csv(MOCKS)
    if mocks:
        lines += ["| 날짜 | 모의고사 | 결과 | 시간 |", "|---|---|---|---|"]
        for x in reversed(mocks):
            lines.append(f"| {x['date']} | {x['name']} | {x['solved']} / {x['total']} | {x['minutes']} / {x['limit']}분 |")
        lines.append("")
    lines += ["## 마일스톤", ""] + [f"- {x['date']}: {x['what']}" for x in cfg["milestones"]]
    lines += ["", "## 티어 기준 (자체 환산)", "", "| 레벨 | 티어 |", "|---|---|"]
    tiers = cfg["tiers"]
    for i, (th, n) in enumerate(tiers):
        hi = tiers[i + 1][0] - 1 if i + 1 < len(tiers) else 100
        lines.append(f"| {th}–{hi} | {n} |")
    lines += ["", f"복습 규칙: {cfg['review_rules']}"]
    lines += ["", f"XP: Lv.0 0.5 · Lv.1 1 · Lv.2 3 · Lv.3 8 · Lv.4 15 · Lv.5 25 — {cfg['xp_rules']}", "",
              "## 풀이 기록", "", "| 날짜 | 문제 | Lv | 구분 | 결과 | 분 | 한 줄 기록 |", "|---|---|---|---|---|---|---|"]
    kind_name = {"redo": "복습", "first": "첫 풀이", "mock": "모의고사"}
    for r in reversed(records):
        title = f"{r['id']} {r['title']}" + (" (SQL)" if r["platform"] == "sql" else "")
        link = f"[{title}]({r['path']})" if r["path"] else title
        lines.append(f"| {r['date']} | {link} | {r['level']} | {kind_name.get(r['kind'], r['kind'])} | {r['result']} | {r['minutes']} | {r['note']} |")
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------- 기록 공통 ----------

def ask(prompt, valid=None):
    while True:
        v = input(prompt).strip()
        if not valid or v in valid:
            return v


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def commit_push(msg):
    git("add", ".")
    c = git("commit", "-m", msg)
    if c.returncode != 0:
        print(c.stdout + c.stderr)
        return
    push = git("push")
    print("GitHub push 완료 ✅" if push.returncode == 0 else f"push 실패 — 나중에 git push 해주세요\n{push.stderr}")


def write_record(cfg, p, kind, result, minutes, note):
    d = problem_dir(p["id"], p["platform"])
    append_csv(RECORDS, FIELDS, {"date": today().isoformat(), "platform": p["platform"], "id": p["id"], "title": p["title"],
                                 "level": str(p["level"]), "kind": kind, "result": result, "minutes": str(minutes),
                                 "note": note.replace("|", "/"), "path": os.path.relpath(d, ROOT) if d else ""})


def cmd_record(cfg, pid, kind, minutes=None):
    p = get_problem(cfg, pid)
    if not p:
        sys.exit(f"모르는 문제: {pid}")
    if not problem_dir(p["id"], p["platform"]):
        sys.exit(f"없음: {pid} (먼저 cote new {pid})")
    print(f"[{p['id']}] {p['title']} (Lv.{p['level']}) — {'복습' if kind == 'redo' else '첫 풀이'} 기록")
    res = RESULT[ask("결과? 1) ✅ 혼자 풀이  2) 💡 해설 참고  3) ❌ 미해결 : ", RESULT)]
    if minutes is None:
        minutes = ask("걸린 시간(분): ")
    else:
        print(f"걸린 시간: {minutes}분 (자동 측정)")
    note = ask("한 줄 기록 (핵심 아이디어 / 막힌 지점): ")
    write_record(cfg, p, kind, res, minutes, note)
    records = load_records()
    render_readme(cfg, records)
    s = status(cfg, records)
    print(f"\nLv.{s['level']:.1f} {s['tier']} · XP {s['xp']} · 이번 주 {s['week']['done']}/{s['week']['target']} · 🔥 {s['streak_days']}일")
    if p["platform"] != "sql":
        nxt = review_schedule(cfg, records).get(p["id"])
        if nxt and nxt["due"]:
            print(f"다음 복습: {nxt['due']} (아침 메일에 🔁로 나와요)")
        elif nxt:
            print("🎓 졸업! 이 문제는 더 이상 복습하지 않아요")
    prefix = {"redo": "redo", "first": "solve"}[kind]
    tag = {"programmers": "PGS", "sql": "SQL", "ext": "EXT"}[p["platform"]]
    commit_push(f"{prefix}: {tag} #{p['id']} {p['title']} {res} - {note}")


def grab_code(p, kind):
    """클립보드 코드를 풀이 파일로 저장 (복습은 날짜별 파일로 따로)"""
    code = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout if sys.platform == "darwin" else ""
    d = problem_dir(p["id"], p["platform"])
    stamp = "" if kind == "first" else f"_{today().strftime('%Y%m%d')}"
    name = f"solution{stamp}.sql" if p["platform"] == "sql" else f"Solution{stamp}.java"
    looks_ok = ("select" in code.lower()) if p["platform"] == "sql" else ("solution" in code or "class" in code)
    if looks_ok:
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            f.write(code if code.endswith("\n") else code + "\n")
        print(f"코드 저장 완료 ✅ ({name})")
    else:
        print(f"⚠️ 클립보드에 코드가 없어서 저장 못 했어요. 나중에 {os.path.relpath(os.path.join(d, name), ROOT)}에 붙여넣어 주세요.")


def solve_one(cfg, pick, kind):
    """문제 하나: 브라우저 열기 → 타이머 → 코드 복사 → Enter → 기록·GitHub"""
    p = get_problem(cfg, pick["id"])
    if kind == "redo":
        print(f"\n🔁 복습 · {p['id']} {p['title']} (Lv.{p['level']}) — {pick['reason']}")
        if pick.get("quick"):
            print("   빠른 회상: 문제 읽고 1분간 접근을 말로 정리 → 10분 안에 코딩. 이전 코드·해설은 보지 않기")
        else:
            print("   이전 코드·해설 보지 말고 빈 화면에서 처음부터! (프로그래머스 '초기화' 버튼으로 코드 비우기)")
    elif p["platform"] == "sql":
        print(f"\n🗄️ SQL · {p['id']} {p['title']} (Lv.{p['level']}) — 정처기 실기·SQLD 같이 대비")
    else:
        tags = ", ".join(p.get("tags", []))
        print(f"\n🆕 새 문제 · {p['id']} {p['title']} (Lv.{p['level']}" + (f" · {tags})" if tags else ")"))
    make_dir(p)
    print(f"문제: {p['url']}")
    open_url(p["url"])
    start = time.time()
    print("\n① 브라우저에서 풀고 제출")
    print("② 코드 창에서 ⌘A → ⌘C (코드 전체 복사)")
    input("③ 여기로 돌아와서 Enter ⏎ ")
    minutes = max(1, round((time.time() - start) / 60))
    grab_code(p, kind)
    cmd_record(cfg, p["id"], kind, minutes)


# ---------- 명령 ----------

def cmd_go(cfg):
    """하루 한 번 이것만: 오늘 분량(복습 + 새 문제 + 트랙)을 순서대로 진행"""
    s = status(cfg, load_records())
    redo = [(r, "redo") for r in s["today_redo"]]
    sql = [(t, "first") for t in s["tracks_today"] if t["track"] == "sql"]
    reminders = [t for t in s["tracks_today"] if t["track"] != "sql"]
    plan = redo[:1] + [(p, "first") for p in s["today_new"]] + sql + redo[1:]
    print(f"\n📅 {s['date']} · Lv.{s['level']:.1f} {s['tier']} · 🔥 {s['streak_days']}일 · 오늘 완료 {len(s['today_done'])}개")
    m = s["mock"]
    if m["due"]:
        print(f"📝 모의고사 날이에요! 시간 될 때 `cote mock` ({m['count']}문제 {m['minutes']}분, 주말 추천)")
    elif (date.fromisoformat(m["date"]) - today()).days <= 3:
        print(f"📝 모의고사 예정: {m['date']} ({m['count']}문제 {m['minutes']}분)")
    for t in reminders:
        print(f"🧩 {t['title']}: {t['why']} → {t['url']}")
    j = s.get("java")
    if j and j["pending"]:
        what = ([f"카드 복습 {len(j['today_reviews'])}개"] if j["today_reviews"] else []) + \
               ([f"{j['today_lesson']['key']} {j['today_lesson']['title']}"] if j["today_lesson"] else [])
        print(f"☕ 자바 기초 ({j['done']}/{j['total']}): 오늘 {' + '.join(what)} → 터미널에 `java`")
    nb = s["notebook"]
    if nb["ready"]:
        print(f"📘 핵심노트 Vol.{nb['next_vol']}: {nb['ready']}/{nb['threshold']}문제 모임" + (" — 발행 가능!" if nb["ready"] >= nb["threshold"] else ""))
    if not plan:
        print("오늘 분량 끝! 👏")
        offer_notebook(cfg)
        return
    print("오늘 분량 (⭐ = 바쁘면 이것만):")
    icon = lambda p, k: "🔁 복습" if k == "redo" else ("🗄️ SQL" if p.get("platform") == "sql" else "🆕 새 문제")
    for i, (p, k) in enumerate(plan):
        print(f"  {'⭐' if i == 0 else '  '} {icon(p, k)} {p['id']} {p['title']} (Lv.{p['level']})" + (f" — {p['reason']}" if k == "redo" else ""))
    if s["review_backlog"]:
        print(f"  (밀린 재풀이 {s['review_backlog']}개는 내일 이후로 자동 배치, 새 문제는 1개로 줄였어요)")
    for i, (p, k) in enumerate(plan):
        if i > 0 and input(f"\n다음: {icon(p, k)} {p['id']} {p['title']} — 계속할까요? (Enter=계속 / q=오늘은 여기까지) ").strip().lower() == "q":
            break
        solve_one(cfg, p, k)
        if i == 0:
            print("\n✅ 오늘 최소 분량 달성! 연속일 유지돼요.")
    print("\n오늘 끝! 밤 11시에 노션 데브로그로 정리돼요.")
    offer_notebook(cfg)


def level_text(cfg, records):
    s = status(cfg, records)
    return f"Lv.{s['level']:.0f} {s['tier']}"


def offer_notebook(cfg):
    """복습 거친 문제가 기준 수만큼 모이면 핵심노트 발행 제안"""
    records = load_records()
    nb = notebook.progress(records)
    if nb["ready"] < nb["threshold"]:
        return
    if ask(f"\n📘 복습을 거친 문제 {nb['ready']}개가 모였어요. 핵심노트 Vol.{nb['next_vol']} PDF를 만들까요? (3~5분) (y/n) ", {"y", "n"}) == "y":
        cmd_note(cfg, [])


def cmd_note(cfg, args):
    records = load_records()
    lv = level_text(cfg, records)
    if "--all" in args:
        path = notebook.rebuild_full(records, lv)
        msg = "note: 핵심노트 전체판 재생성"
    else:
        res = notebook.publish(cfg, get_problem, records, lv, force=True)
        if not res:
            return
        path, no = res
        msg = f"note: 📘 핵심노트 Vol.{no} 발행"
    if not path:
        return
    print(f"\n📘 완성: {os.path.relpath(path, ROOT)} (전체판: notes/핵심노트_전체.pdf)")
    open_url(path)
    render_readme(cfg, records)
    commit_push(msg)
    print("밤 11시 루틴이 노션 마스터 페이지 아래에 같은 내용을 페이지로 올려요. 인쇄는 열린 PDF에서 ⌘P")


def cmd_mock(cfg):
    """처음 보는 문제로 시간 재고 실전 연습"""
    d = today()
    m = next_mock(cfg, d)
    if not m["due"] and ask(f"다음 예정일은 {m['date']}예요. 지금 미리 볼까요? (y/n) ", {"y", "n"}) == "n":
        return
    name, probs, limit = pick_mock(cfg, d, m["format"])
    if not probs:
        sys.exit("모의고사 풀이 소진됐어요. 백준·기업 기출을 `cote ext`로 풀어 주세요.")
    end = datetime.now(KST) + timedelta(minutes=limit)
    print(f"\n📝 {name} · {len(probs)}문제 · 제한 {limit}분 (종료 {end:%H:%M})")
    print("   실전처럼: 유형 힌트 없음, 해설·검색 금지, 자동완성 없이 프로그래머스 에디터에서만")
    for i, p in enumerate(probs, 1):
        print(f"   {i}. {p['url'] if 'url' in p else pgs_url(p['id'])}")
    input("\n준비되면 Enter ⏎ (모든 문제가 열리고 타이머 시작) ")
    for p in probs:
        open_url(pgs_url(p["id"]))
    start = time.time()
    input(f"\n⏱ 시작! {end:%H:%M}까지. 다 끝냈거나 시간이 다 되면 Enter ⏎ ")
    minutes = max(1, round((time.time() - start) / 60))
    print(f"\n걸린 시간 {minutes}분 / {limit}분" + (" ⚠️ 시간 초과분은 실전이면 0점이에요" if minutes > limit else ""))
    solved = 0
    for i, p in enumerate(probs, 1):
        info = get_problem(cfg, p["id"])
        r = ask(f"{i}. {info['title']} (Lv.{info['level']}) — 1) 통과  2) 부분 점수/시간 초과  3) 못 풂 : ", {"1", "2", "3"})
        res = "✅" if r == "1" else "❌"
        solved += r == "1"
        make_dir(info)
        write_record(cfg, info, "mock", res, minutes, f"{name} {i}번" + (" 부분 점수" if r == "2" else ""))
    append_csv(MOCKS, MOCK_FIELDS, {"date": d.isoformat(), "name": name, "format": m["format"], "total": len(probs),
                                     "solved": solved, "minutes": minutes, "limit": limit})
    records = load_records()
    render_readme(cfg, records)
    rd = readiness(cfg, records)
    print(f"\n결과 {solved} / {len(probs)} · 못 푼 문제는 내일부터 망각곡선 복습으로 다시 나와요")
    for v in rd["verdicts"]:
        print(f"   {'✅' if v['met'] else '⏳'} {v['name']}: {v['detail']}")
    commit_push(f"mock: {name} {solved}/{len(probs)} ({minutes}/{limit}분)")


def cmd_ext(cfg):
    """외부 문제(백준·SWEA·LeetCode 등) 처음 보는 문제 풀이"""
    src = {"1": ("boj", "백준"), "2": ("swea", "SWEA"), "3": ("leet", "LeetCode"), "4": ("etc", "기타")}
    k, src_name = src[ask("출처? 1) 백준  2) SWEA  3) LeetCode  4) 기타 : ", src)]
    num = ask("문제 번호/ID: ")
    title = ask("제목: ")
    level = int(ask("체감 레벨 (프로그래머스 기준 1~5): ", {"1", "2", "3", "4", "5"}))
    u = f"https://www.acmicpc.net/problem/{num}" if k == "boj" else ask("문제 URL: ")
    pid = f"{k}-{slug(num)}"
    ext = load_ext()
    ext[pid] = {"title": f"[{src_name}] {title}", "level": level, "url": u}
    with open(EXT, "w", encoding="utf-8") as f:
        json.dump(ext, f, ensure_ascii=False, indent=1)
    solve_one(cfg, {"id": pid}, "first")


def cmd_track(cfg, args):
    if len(args) >= 2 and args[0] in cfg["tracks"] and args[1] in ("on", "off"):
        cfg["tracks"][args[0]]["enabled"] = args[1] == "on"
        save_cfg(cfg)
        commit_push(f"chore: {args[0]} 트랙 {args[1]}")
    for key, t in cfg["tracks"].items():
        days = "".join("월화수목금토일"[w] for w in t["weekdays"])
        print(f"{'🟢' if t['enabled'] else '⚪'} {key:8} {t['name']} ({days}) — {t['why']}")
    print("\n켜기/끄기: cote track samsung on")


def cmd_plan(cfg, records, days=14):
    """앞으로 N일 복습 일정 (망각곡선)"""
    sched = review_schedule(cfg, records)
    d0 = today()
    for i in range(days):
        d = (d0 + timedelta(days=i)).isoformat()
        items = [x for x in sched.values() if x["due"] and (x["due"] == d or (i == 0 and x["due"] < d))]
        if items:
            print(f"{d}: " + ", ".join(f"{x['id']} {x['title']}({x['interval']}일 차)" for x in items))
    m = next_mock(cfg, d0)
    print(f"📝 다음 모의고사 {m['date']} · 🎓 졸업 {sum(1 for x in sched.values() if x['due'] is None)}문제")


def cmd_today(cfg, records):
    s = status(cfg, records)
    print(f"📅 {s['date']} · {s['phase']['key']} {s['phase']['name']}")
    print(f"[{bar(s['level'])}] Lv.{s['level']:.1f}/100 · {s['tier']} · 🔥 {s['streak_days']}일")
    if s["next_target"]:
        print(f"다음 목표선: {s['next_target']['name']} (Lv.{s['next_target']['level']})")
    print(f"이번 주 {s['week']['done']}/{s['week']['target']} · 오늘 완료 {len(s['today_done'])}/{s['phase']['daily_min']} · SQL {s['sql_progress']['done']}/{s['sql_progress']['total']}")
    print("실전 정답률: " + " · ".join(f"{'✅' if v['met'] else '⏳'} {v['name']}" for v in s["readiness"]["verdicts"]))
    print(f"\n포커스: {s['phase']['focus']}\n")
    if s["today_redo"]:
        print("🔁 복습 (해설·이전 코드 없이):")
        for r in s["today_redo"]:
            print(f"   {r['id']} {r['title']} (Lv.{r['level']}, {r['reason']}) {r['url']}")
        if s["review_backlog"]:
            print(f"   + 밀린 재풀이 {s['review_backlog']}개")
    print("🆕 새 문제:")
    for p in s["today_new"]:
        print(f"   {p['id']} {p['title']} (Lv.{p['level']} · {', '.join(p['tags'])}) {p['url']}")
    for t in s["tracks_today"]:
        print(f"{'🗄️ SQL' if t['track'] == 'sql' else '🧩'} {t.get('id', '')} {t['title']} {t['url']}")
    m = s["mock"]
    print(f"📝 다음 모의고사: {m['date']}" + (" ← 오늘!" if m["due"] else ""))
    j = s.get("java")
    if j:
        todo = [f"{r['key']} 카드 복습" for r in j["today_reviews"]] + ([f"{j['today_lesson']['key']} {j['today_lesson']['title']}"] if j["today_lesson"] else [])
        print(f"☕ 자바 기초 {j['done']}/{j['total']}: " + (", ".join(todo) + " → `java`" if todo else "오늘 끝"))
    nb = s["notebook"]
    print(f"📘 핵심노트 Vol.{nb['next_vol']}: {nb['ready']}/{nb['threshold']}문제")


def cmd_new(cfg, pid):
    p = get_problem(cfg, pid)
    if not p:
        title = input("로드맵에 없는 문제예요. 제목: ").strip()
        level = int(input("레벨(0~5): ").strip())
        p = {"id": str(pid), "title": title, "level": level, "tags": [], "platform": "programmers", "url": pgs_url(pid)}
    d = make_dir(p)
    print(f"생성: {os.path.relpath(d, ROOT)}\n문제: {p['url']}")
    open_url(p["url"])


def main():
    cfg = load_cfg()
    a = sys.argv[1:]
    if a and a[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd = a[0] if a else "go"
    records = load_records()
    if cmd == "go":
        cmd_go(cfg)
    elif cmd == "mock":
        cmd_mock(cfg)
    elif cmd == "ext":
        cmd_ext(cfg)
    elif cmd == "track":
        cmd_track(cfg, a[1:])
    elif cmd == "note":
        cmd_note(cfg, a[1:])
    elif cmd == "today":
        cmd_today(cfg, records)
    elif cmd == "plan":
        cmd_plan(cfg, records)
    elif cmd == "status":
        s = status(cfg, records)
        print(json.dumps(s, ensure_ascii=False, indent=1) if "--json" in a else
              f"Lv.{s['level']:.1f}/100 · {s['tier']} · XP {s['xp']} · 🔥 {s['streak_days']}일")
    elif cmd == "readme":
        render_readme(cfg, records)
    elif cmd == "new" and len(a) > 1:
        cmd_new(cfg, a[1])
    elif cmd == "run" and len(a) > 1:
        d = problem_dir(a[1]) or sys.exit(f"없음: {a[1]}")
        subprocess.run(["java", "Solution.java"], cwd=d)
    elif cmd in ("done", "redo") and len(a) > 1:
        cmd_record(cfg, a[1], "first" if cmd == "done" else "redo")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
