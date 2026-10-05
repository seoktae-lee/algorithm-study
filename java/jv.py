#!/usr/bin/env python3
"""자바 기초 CLI — ① 김영한의 자바 입문(인프런) K01~K23 → ② 코테용 Java L01~L24

  java                    ★ 매일 이것만: 카드 복습(망각곡선) → 오늘 회차(강의 3~4개 시청 → 연습문제 채점) → 기록·GitHub 자동
  java today              오늘 분량 + 진도
  java list               전체 회차 목록과 상태
  java cards [K3|L3]      카드만 복습 (예: java cards k3) — 기록 없이 연습용
  java skip K번호          이미 본 강의 회차까지 완료 처리 (예: java skip k6 → K01~K06)
  java status [--json]    현재 위치 (cote·루틴이 --json 사용)

  ※ 인자 없이(또는 today/list/cards/status/help) 치면 이 학습 CLI, `java Main.java`·`java -version` 등은 진짜 java (~/.zshrc 함수)
"""
import csv, json, os, re, shutil, subprocess, sys, time
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
LESSONS = os.path.join(ROOT, "lessons")
PRACTICE = os.path.join(ROOT, "practice")
RECORDS = os.path.join(ROOT, "records.csv")
FIELDS = ["date", "lesson", "title", "kind", "result", "score", "minutes", "note"]
KST = timezone(timedelta(hours=9))
CURVE = [1, 3, 7, 14, 30]       # 카드 복습 간격 (일). 80% 이상 맞히면 다음 간격, 아니면 1일부터
PASS_RATE = 0.8
TIME_LIMIT = 20             # 연습문제 채점 제한 시간(초)
JAVA = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8"]
GITHUB = "https://github.com/seoktae-lee/algorithm-study/blob/main/java/lessons"


def today():
    return datetime.now(KST).date()


# ---------- 레슨 읽기 ----------

def lessons():
    """lessons/{K,L}NN_제목/README.md → [{no, key, dir, title, course, units, cards, hints, cheat}]
    K = 인프런 강의 연동 회차(출력 비교형 QN.java), L = 코테용 레슨(Check 채점형 Exercise.java). K가 먼저"""
    out = []
    for name in sorted(os.listdir(LESSONS), key=lambda n: (n[0] != "K", n)):
        m = re.match(r"([KL])(\d+)_", name)
        if not m:
            continue
        with open(os.path.join(LESSONS, name, "README.md"), encoding="utf-8") as f:
            md = f.read()
        title = re.search(r"^# (.+)$", md, re.M).group(1).strip()
        title = re.sub(r"^[KL]\d+\.\s*", "", title)
        units = [{"title": t, "url": u, "min": int(mm) if mm else 0}
                 for t, u, mm in re.findall(r"^- \[(.+?)\]\((https://www\.inflearn\.com/[^)]+)\)(?: · (\d+)분)?", section(md, "🎬"), re.M)]
        out.append({"no": int(m.group(2)), "key": f"{m.group(1)}{int(m.group(2)):02d}", "dir": name, "title": title,
                    "course": m.group(1) == "K", "units": units,
                    "cards": parse_cards(section(md, "🃏")), "hints": section(md, "🧩").strip(),
                    "cheat": section(md, "📌").strip()})
    return out


def section(md, emoji):
    """'## {emoji} ...' 제목 아래부터 다음 '## '까지"""
    m = re.search(rf"^## {emoji}[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    return m.group(1) if m else ""


def parse_cards(text):
    cards, cur = [], None
    for line in text.splitlines():
        if line.startswith("- Q:"):
            cur = {"q": line[4:].strip(), "a": ""}
            cards.append(cur)
        elif cur is not None and line.strip().startswith("A:") and not cur["a"]:
            cur["a"] = line.strip()[2:].strip()
        elif cur is not None and cur["a"] and line.strip():
            cur["a"] += "\n" + line.strip()
    return cards


def find_lesson(ls, key):
    """'k3'·'K03' → K03, 'l3'·'3' → L03 (숫자만 쓰면 L)"""
    key = str(key).upper()
    track = key[0] if key[:1] in ("K", "L") else "L"
    no = key.lstrip("KL").lstrip("0") or "0"
    return next((l for l in ls if l["key"][0] == track and str(l["no"]) == no), None)


# ---------- 기록 ----------

def load_records():
    if not os.path.exists(RECORDS):
        return []
    with open(RECORDS, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_record(row):
    new = not os.path.exists(RECORDS)
    with open(RECORDS, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def schedule(records):
    """레슨별 망각곡선 상태. first(레슨 완료) → 1일 뒤, review 성공 → 다음 간격, 실패 → 1일부터"""
    st = {}
    for r in sorted(records, key=lambda x: x["date"]):
        k = r["lesson"]
        if r["kind"] == "skip":
            st[k] = {"lesson": k, "title": r["title"], "stage": len(CURVE), "due": None, "last": r["date"],
                     "interval": None, "exercise_ok": True, "skipped": True}
            continue
        if r["kind"] == "first" or k not in st:
            stage = 0
        elif r["kind"] == "review":
            stage = st[k]["stage"] + 1 if r["result"] == "✅" else 0
        else:
            continue
        exercise_ok = r["result"] == "✅" if r["kind"] == "first" else st.get(k, {}).get("exercise_ok", False)
        if r["kind"] == "review" and "연습문제 재도전 ✅" in r.get("note", ""):
            exercise_ok = True
        due = (date.fromisoformat(r["date"]) + timedelta(days=CURVE[stage])).isoformat() if stage < len(CURVE) else None
        st[k] = {"lesson": k, "title": r["title"], "stage": stage, "due": due, "last": r["date"],
                 "interval": CURVE[stage] if stage < len(CURVE) else None, "exercise_ok": exercise_ok}
    return st


def streak(records, d):
    days = {r["date"] for r in records if r["kind"] != "skip"}
    n, cur = 0, d
    if cur.isoformat() not in days:
        cur -= timedelta(days=1)
    while cur.isoformat() in days:
        n += 1
        cur -= timedelta(days=1)
    return n


def status(records=None, d=None):
    d = d or today()
    records = load_records() if records is None else records
    ls = lessons()
    st = schedule(records)
    done = [l for l in ls if l["key"] in st]
    nxt = next((l for l in ls if l["key"] not in st), None)
    due = sorted([x for x in st.values() if x["due"] and x["due"] <= d.isoformat() and x["last"] != d.isoformat()],
                 key=lambda x: (x["due"], x["lesson"]))
    today_recs = [r for r in records if r["date"] == d.isoformat()]
    new_done_today = any(r["kind"] == "first" for r in today_recs)
    return {
        "date": d.isoformat(),
        "done": len(done), "total": len(ls),
        "next_lesson": {"key": nxt["key"], "title": nxt["title"]} if nxt else None,
        "today_lesson": None if (new_done_today or not nxt) else {"key": nxt["key"], "title": nxt["title"],
                                                                 "minutes": sum(u["min"] for u in nxt["units"]) or None},
        "today_reviews": [{"key": x["lesson"], "title": x["title"], "interval": x["interval"]} for x in due],
        "today_done": [{k: r[k] for k in ("lesson", "title", "kind", "result", "score", "minutes")} for r in today_recs],
        "mastered": sum(1 for x in st.values() if x["due"] is None and not x.get("skipped")),
        "course": {"done": sum(1 for l in done if l["course"]), "total": sum(1 for l in ls if l["course"])},
        "streak_days": streak(records, d),
        "pending": bool(due) or (not new_done_today and nxt is not None),
    }


# ---------- 공통 ----------

def ask(prompt, valid=None):
    while True:
        v = input(prompt).strip().lower()
        if not valid or v in valid:
            return v


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


def commit_push(msg):
    git("add", "java")
    c = git("commit", "-m", msg)
    if c.returncode != 0:
        print(c.stdout + c.stderr)
        return
    push = git("push")
    print("GitHub push 완료 ✅" if push.returncode == 0 else f"push 실패 — 나중에 git push 해주세요\n{push.stderr}")


def open_url(u):
    if sys.platform == "darwin":
        subprocess.run(["open", u])


def open_editor(path):
    for cmd in (["code", "-r", path], ["open", "-t", path]):
        if shutil.which(cmd[0]):
            subprocess.run(cmd)
            return


def lesson_url(l):
    return f"{GITHUB}/{l['dir']}/README.md"


# ---------- 카드 복습 ----------

def quiz(l):
    cards = l["cards"]
    print(f"\n🃏 {l['key']} {l['title']} — 카드 {len(cards)}장 (머릿속으로 답 → Enter로 정답 확인 → 맞았는지 y/n)")
    right, missed = 0, []
    for i, c in enumerate(cards, 1):
        input(f"\n  Q{i}. {c['q'].replace('`', '')}\n     ⏎ ")
        print("     A. " + c["a"].replace("`", "").replace("\n", "\n        "))
        if ask("     맞았어? (y/n) ", {"y", "n"}) == "y":
            right += 1
        else:
            missed.append(i)
    ok = right / max(1, len(cards)) >= PASS_RATE
    print(f"\n  {right}/{len(cards)} " + ("✅ 통과 — 다음 복습 간격으로" if ok else "🔁 80% 미만 — 내일 다시 나와요"))
    return ok, right, len(cards), missed


# ---------- 연습문제 ----------

def practice_dir(l):
    return os.path.join(PRACTICE, l["dir"])


def course_questions(l):
    """K 회차의 문제 이름 [Q1, Q2, …] (기대 출력 QN.out 기준)"""
    d = os.path.join(LESSONS, l["dir"])
    return sorted((f[:-4] for f in os.listdir(d) if re.fullmatch(r"Q\d+\.out", f)), key=lambda q: int(q[1:]))


def prepare_course(l, fresh=False):
    """K 회차: practice/KNN_*/QN.java 준비. fresh면 이전 풀이를 first_YYYYMMDD/로 옮기고 새로"""
    d = practice_dir(l)
    qs = course_questions(l)
    if fresh and any(os.path.exists(os.path.join(d, f"{q}.java")) for q in qs):
        old = os.path.join(d, f"first_{today().strftime('%Y%m%d')}")
        os.makedirs(old, exist_ok=True)
        for q in qs:
            if os.path.exists(os.path.join(d, f"{q}.java")):
                os.rename(os.path.join(d, f"{q}.java"), os.path.join(old, f"{q}.java"))
    os.makedirs(d, exist_ok=True)
    for q in qs:
        target = os.path.join(d, f"{q}.java")
        if not os.path.exists(target):
            shutil.copy(os.path.join(LESSONS, l["dir"], f"{q}.java"), target)
    return [os.path.join(d, f"{q}.java") for q in qs]


def run_course(l):
    """QN.java를 하나씩 실행(입력 QN.in) → 출력이 QN.out과 같으면 통과 (줄 끝 공백 무시)"""
    norm = lambda t: "\n".join(x.rstrip() for x in t.strip("\n").split("\n"))
    ok = 0
    qs = course_questions(l)
    for q in qs:
        src = os.path.join(LESSONS, l["dir"], q)
        stdin = open(src + ".in", encoding="utf-8").read() if os.path.exists(src + ".in") else ""
        expected = norm(open(src + ".out", encoding="utf-8").read())
        try:
            p = subprocess.run([*JAVA, f"{q}.java"], cwd=practice_dir(l), input=stdin,
                               capture_output=True, text=True, timeout=TIME_LIMIT)
        except subprocess.TimeoutExpired:
            print(f"  ⏱ {q}: {TIME_LIMIT}초 안에 안 끝났어요 — 무한 루프인지 확인 (반복 변수 증가를 빠뜨렸나요?)")
            continue
        actual = norm(p.stdout)
        if p.returncode != 0 and not actual:
            err = p.stderr.strip()
            print(f"  💥 {q}: " + ("컴파일 에러" if "error:" in err else "실행 중 에러") + "\n       " +
                  (err[:1500] if len(err) < 1500 else err[:1500] + " …").replace("\n", "\n       "))
        elif actual == expected:
            ok += 1
            print(f"  ✅ {q}")
        else:
            print(f"  ❌ {q}\n       기대 출력:\n         " + expected.replace("\n", "\n         ") +
                  "\n       내 출력:\n         " + (actual or "(출력 없음)").replace("\n", "\n         "))
    return ok, len(qs)


def prepare_exercise(l, fresh=False):
    if l["course"]:
        return prepare_course(l, fresh)
    d = practice_dir(l)
    target = os.path.join(d, "Exercise.java")
    if fresh and os.path.exists(target):
        stamp = today().strftime("%Y%m%d")
        os.rename(target, os.path.join(d, f"Exercise_first_{stamp}.java"))
    os.makedirs(d, exist_ok=True)
    if not os.path.exists(target):
        shutil.copy(os.path.join(LESSONS, l["dir"], "Exercise.java"), target)
    shutil.copy(os.path.join(ROOT, "_harness", "Check.java"), os.path.join(d, "Check.java"))
    return target


def run_exercise(path):
    try:
        p = subprocess.run([*JAVA, os.path.basename(path)], cwd=os.path.dirname(path), capture_output=True, text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        print(f"  ⏱ {TIME_LIMIT}초 안에 안 끝났어요 — 무한 루프이거나 시간복잡도가 너무 커요 (코테였다면 시간 초과)")
        return 0, 1
    out = p.stdout + (("\n" + p.stderr) if p.stderr.strip() else "")
    m = re.search(r"RESULT (\d+)/(\d+)", p.stdout)
    shown = re.sub(r"RESULT \d+/\d+\n?", "", out).rstrip()
    print(shown if len(shown) < 4000 else shown[:4000] + "\n  …(생략)")
    if not m:
        return 0, 0
    return int(m.group(1)), int(m.group(2))


def exercise_loop(l, path):
    """Enter=채점, h=힌트, s=포기. 전부 통과하면 ✅, 힌트 보고 통과 💡, 포기 ❌"""
    answer = f"java/lessons/{l['dir']}/" + ("answers/" if l["course"] else "Answer.java")
    used_hint = False
    while True:
        v = ask("\n  Enter=채점  h=힌트  s=오늘은 포기 : ", {"", "h", "s"})
        if v == "h":
            used_hint = True
            print("\n" + (l["hints"] or "  (힌트 없음 — 레슨 README의 예제 코드를 다시 보세요)"))
            continue
        if v == "s":
            print(f"\n  정답 코드: {answer} — 읽어 보고 왜 그렇게 짜는지 이해하기 (다음 복습 때 다시 풀어요)")
            return "❌", "포기"
        print()
        ok, total = run_course(l) if l["course"] else run_exercise(path)
        if total and ok == total:
            return ("💡" if used_hint else "✅"), f"{ok}/{total}"
        print(f"\n  {ok}/{total} 통과 — 고치고 저장(⌘S)한 뒤 다시 Enter" if total else "\n  컴파일 에러 — 위 메시지의 줄 번호를 보고 고친 뒤 Enter")


def open_editor_files(paths):
    if shutil.which("code"):
        subprocess.run(["code", "-r", *paths])
    else:
        for p in paths:
            open_editor(p)


def do_course(l):
    """K 회차: 강의 시청 → Enter → QN.java 채우기 → 출력 비교 채점"""
    mins = sum(u["min"] for u in l["units"])
    print(f"\n🎬 {l['key']} {l['title']} — 강의 약 {mins}분")
    for i, u in enumerate(l["units"], 1):
        print(f"   {i}. {u['title']}" + (f" ({u['min']}분)" if u["min"] else " (퀴즈)"))
    print(f"   요약·링크 모음: {lesson_url(l)}")
    if l["units"]:
        open_url(l["units"][0]["url"])
    start = time.time()
    print("\n① 브라우저에서 첫 강의를 열었어요. 위 순서대로 보고, 예제는 꼭 직접 따라 치기")
    print("   (다음 강의는 인프런 화면의 '다음 수업' 또는 위 요약 페이지 링크)")
    if ask("② 다 봤으면 Enter → 연습문제 / q=오늘은 강의만 (기록 안 함) : ", {"", "q"}) == "q":
        print("   다음에 `java` 치면 이 회차부터 다시 시작해요")
        return False
    paths = prepare_exercise(l)
    open_editor_files(paths)
    print(f"\n③ VS Code에 연습문제 {len(paths)}개를 열었어요: {os.path.relpath(os.path.dirname(paths[0]), REPO)}/Q1~Q{len(paths)}.java")
    print("   각 파일 맨 위 주석의 '기대 출력'이 나오도록 TODO에 코드 쓰기 → 저장(⌘S) → 여기서 Enter")
    result, score = exercise_loop(l, None)
    minutes = max(1, round((time.time() - start) / 60))
    note = ask("\n한 줄 기록 (새로 안 것 / 헷갈린 것): ")
    append_record({"date": today().isoformat(), "lesson": l["key"], "title": l["title"], "kind": "first",
                   "result": result, "score": score, "minutes": minutes, "note": note.replace("|", "/")})
    render_readme()
    s = status()
    print(f"\n{result} {l['key']} 완료 · {minutes}분 · 강의 {s['course']['done']}/{s['course']['total']}회차 · 내일 카드 복습으로 다시 나와요")
    if result != "✅":
        print("   연습문제는 다음 카드 복습 때 새 파일로 한 번 더 풀어요")
    commit_push(f"java: {l['key']} {l['title']} {result} ({score}) - {note}")
    return True


def do_lesson(l):
    if l["course"]:
        return do_course(l)
    print(f"\n📖 {l['key']} {l['title']}")
    print(f"   개념: {lesson_url(l)}")
    open_url(lesson_url(l))
    path = prepare_exercise(l)
    print(f"   연습문제: {os.path.relpath(path, REPO)} (VS Code로 열었어요)")
    open_editor(path)
    start = time.time()
    print("\n① 브라우저에서 개념을 읽고 (예제 코드는 직접 쳐보기)")
    print("② VS Code에서 Exercise.java의 TODO 채우기 → 저장(⌘S)")
    print("③ 여기서 Enter → 자동 채점")
    result, score = exercise_loop(l, path)
    minutes = max(1, round((time.time() - start) / 60))
    note = ask("\n한 줄 기록 (새로 안 것 / 헷갈린 것): ")
    append_record({"date": today().isoformat(), "lesson": l["key"], "title": l["title"], "kind": "first",
                   "result": result, "score": score, "minutes": minutes, "note": note.replace("|", "/")})
    render_readme()
    s = status()
    print(f"\n{result} {l['key']} 완료 · {minutes}분 · 진도 {s['done']}/{s['total']} · 내일 카드 복습으로 다시 나와요")
    if result != "✅":
        print("   연습문제는 다음 카드 복습 때 새 파일로 한 번 더 풀어요")
    commit_push(f"java: {l['key']} {l['title']} {result} ({score}) - {note}")
    return True


def do_review(l, st):
    start = time.time()
    ok, right, total, missed = quiz(l)
    note = f"카드 {right}/{total}" + (f" · 틀린 카드 Q{', Q'.join(map(str, missed))}" if missed else "")
    redo_ok = None
    if not st.get("exercise_ok"):
        print(f"\n🔁 {l['key']} 연습문제 재도전 (지난번 💡/❌) — 이전 풀이는 " +
              ("first_날짜/ 폴더로" if l["course"] else "Exercise_first_*.java로") + " 옮겼어요")
        path = prepare_exercise(l, fresh=True)
        open_editor_files(path) if l["course"] else open_editor(path)
        r, score = exercise_loop(l, path)
        redo_ok = r == "✅"
        note = f"연습문제 재도전 {r} ({score}) · " + note
    minutes = max(1, round((time.time() - start) / 60))
    result = "✅" if ok and redo_ok is not False else "❌"
    append_record({"date": today().isoformat(), "lesson": l["key"], "title": l["title"], "kind": "review",
                   "result": result, "score": f"{right}/{total}", "minutes": minutes, "note": note})
    return result, note


# ---------- 명령 ----------

def cmd_go():
    records = load_records()
    s = status(records)
    ls = lessons()
    st = schedule(records)
    print(f"\n☕ {s['date']} · 자바 기초 {s['done']}/{s['total']} · 카드 졸업 🎓 {s['mastered']} · 🔥 {s['streak_days']}일")
    if not s["today_reviews"] and not s["today_lesson"]:
        print("오늘 자바 분량 끝! 👏  이제 `cote`로 오늘 문제 풀기")
        return
    if s["today_reviews"]:
        print("🔁 카드 복습: " + ", ".join(f"{r['key']} {r['title']}({r['interval']}일 차)" for r in s["today_reviews"]))
    if s["today_lesson"]:
        t = s["today_lesson"]
        print(f"{'🎬 오늘 강의' if t['key'][0] == 'K' else '📖 오늘 레슨'}: {t['key']} {t['title']} " +
              (f"(강의 {t['minutes']}분 + 연습 10분)" if t.get("minutes") else "(20~30분)"))
    reviewed = []
    for r in s["today_reviews"]:
        l = find_lesson(ls, r["key"])
        res, note = do_review(l, st[r["key"]])
        reviewed.append(f"{r['key']} {res}")
    if reviewed:
        render_readme()
        commit_push("java: 카드 복습 " + ", ".join(reviewed))
    if s["today_lesson"]:
        if reviewed and ask("\n이어서 오늘 레슨 할까요? (Enter=시작 / q=나중에) ", {"", "q"}) == "q":
            return
        if not do_lesson(find_lesson(ls, s["today_lesson"]["key"])):
            return
        nxt = status()["next_lesson"]
        if nxt and ask(f"\n여유 있으면 다음 회차 {nxt['key']} {nxt['title']}도? (y / Enter=오늘은 여기까지) ", {"", "y"}) == "y":
            do_lesson(find_lesson(lessons(), nxt["key"]))
    print("\n☕ 자바 끝! 이제 `cote`로 오늘 문제 풀기")


def cmd_list():
    st = schedule(load_records())
    for l in lessons():
        x = st.get(l["key"])
        mark = "⬜" if not x else ("⏭ 건너뜀" if x.get("skipped") else "🎓" if x["due"] is None else f"✅ 다음 복습 {x['due']}")
        if l["key"] == "K01":
            print("── 🎬 김영한의 자바 입문 (인프런) ──")
        if l["key"] == "L01":
            print("── 📖 코테용 Java ──")
        print(f"{l['key']} {l['title']:<34} {mark}")


def cmd_today():
    s = status()
    print(f"☕ {s['date']} · 자바 기초 {s['done']}/{s['total']} · 🎓 {s['mastered']} · 🔥 {s['streak_days']}일")
    for r in s["today_reviews"]:
        print(f"   🔁 {r['key']} {r['title']} ({r['interval']}일 차 카드 복습)")
    if s["today_lesson"]:
        t = s["today_lesson"]
        print(f"   {'🎬' if t['key'][0] == 'K' else '📖'} {t['key']} {t['title']}" + (f" (강의 {t['minutes']}분)" if t.get("minutes") else ""))
    if not s["pending"]:
        print("   오늘 분량 끝")


def cmd_skip(key):
    """이미 본 강의 회차까지 완료 처리 (카드 복습 없음). 예: java skip k6 → K01~K06"""
    ls = lessons()
    target = find_lesson(ls, key) if key else None
    if not target or not target["course"]:
        print("사용법: java skip K번호  (예: java skip k6 → K01~K06을 이미 본 것으로 처리)")
        return
    st = schedule(load_records())
    todo = [l for l in ls if l["course"] and l["no"] <= target["no"] and l["key"] not in st]
    if not todo:
        print("건너뛸 회차가 없어요")
        return
    print("완료 처리할 회차:\n" + "\n".join(f"   {l['key']} {l['title']}" for l in todo))
    if ask("진행할까요? (y/n) ", {"y", "n"}) != "y":
        return
    for l in todo:
        append_record({"date": today().isoformat(), "lesson": l["key"], "title": l["title"], "kind": "skip",
                       "result": "⏭", "score": "", "minutes": 0, "note": "이미 본 강의"})
    render_readme()
    nxt = status()["next_lesson"]
    print(f"⏭ {todo[0]['key']}~{todo[-1]['key']} 완료 처리 · 다음: {nxt['key']} {nxt['title']}" if nxt else "완료 처리")
    commit_push(f"java: {todo[0]['key']}~{todo[-1]['key']} 건너뜀 (이미 본 강의)")


def render_readme():
    records = load_records()
    s = status(records)
    st = schedule(records)
    lines = ["# 자바 기초 대시보드", "", "> `jv.py`가 자동 생성하는 파일입니다. 직접 수정하지 마세요.", "",
             f"**진도 {s['done']} / {s['total']}** (🎬 인프런 강의 {s['course']['done']}/{s['course']['total']}회차) · 카드 졸업 🎓 {s['mastered']} · 🔥 연속 {s['streak_days']}일", "",
             "터미널에서 `java` (인자 없이) → 카드 복습 → 오늘 회차(강의 시청 or 레슨 읽기) → 연습문제 자동 채점 → 기록·push", "",
             "① 🎬 K01~K23: [김영한의 자바 입문](https://www.inflearn.com/course/김영한의-자바-입문) 하루 강의 3~4개(약 30분) + 출력 비교형 연습문제",
             "② 📖 L01~L24: 코테용 Java (String·컬렉션·정렬·BFS…) — 강의 완주 후 자동으로 이어짐", "",
             "| 회차 | 제목 | 상태 | 다음 복습 |", "|---|---|---|---|"]
    for l in lessons():
        x = st.get(l["key"])
        state = "⬜" if not x else ("⏭ 건너뜀" if x.get("skipped") else "🎓 졸업" if x["due"] is None else f"{x['stage'] + 1}/{len(CURVE)}회차")
        lines.append(f"| {l['key']} | [{l['title']}](lessons/{l['dir']}/README.md) | {state} | {x['due'] if x and x['due'] else ''} |")
    lines += ["", f"복습: 카드 {int(PASS_RATE * 100)}% 이상 맞히면 {'→'.join(map(str, CURVE))}일 간격으로 늘어나고, 미만이면 1일부터 다시.",
              "연습문제를 💡/❌로 끝낸 레슨은 첫 카드 복습 때 연습문제도 새로 풉니다.", "",
              "## 학습 기록", "", "| 날짜 | 레슨 | 구분 | 결과 | 점수 | 분 | 기록 |", "|---|---|---|---|---|---|---|"]
    for r in reversed(records):
        lines.append(f"| {r['date']} | {r['lesson']} {r['title']} | {dict(first='학습', review='복습', skip='건너뜀').get(r['kind'], r['kind'])} | {r['result']} | {r['score']} | {r['minutes']} | {r['note']} |")
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    a = sys.argv[1:]
    cmd = a[0] if a else "go"
    if cmd in ("-h", "--help", "help"):
        print(__doc__)
    elif cmd == "go":
        cmd_go()
    elif cmd == "today":
        cmd_today()
    elif cmd == "list":
        cmd_list()
    elif cmd == "cards":
        ls = lessons()
        st = schedule(load_records())
        targets = [find_lesson(ls, a[1])] if len(a) > 1 else [l for l in ls if l["key"] in st]
        for l in filter(None, targets):
            quiz(l)
    elif cmd == "status":
        s = status()
        print(json.dumps(s, ensure_ascii=False, indent=1) if "--json" in a else
              f"자바 기초 {s['done']}/{s['total']} · 🎓 {s['mastered']} · 🔥 {s['streak_days']}일")
    elif cmd == "skip":
        cmd_skip(a[1] if len(a) > 1 else None)
    elif cmd == "readme":
        render_readme()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
