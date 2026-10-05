"""📘 코테 핵심노트 — 망각곡선 복습을 한 번 이상 거친 문제를 유형별로 정리해 인쇄용 PDF로 발행

발행 조건: 아직 노트에 안 실린 문제 중 '복습(redo)을 1회 이상 한 문제'가 THRESHOLD개 모이면 (cote가 알려줌)
  cote note           조건과 상관없이 지금 모인 만큼 발행 (1문제 이상)
  cote note --all     지금까지의 모든 카드를 유형별로 다시 모은 전체판만 재생성

카드 내용은 로컬 `claude -p`가 내 코드·NOTE.md·풀이 기록을 읽고 작성 → notes/cards/<번호>.json (GitHub에 남음)
PDF는 Chrome headless로 렌더링 → notes/핵심노트_VolNN.pdf + notes/핵심노트_전체.pdf
"""
import glob, html, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
NOTES = os.path.join(ROOT, "notes")
CARDS = os.path.join(NOTES, "cards")
TYPES = os.path.join(NOTES, "types")
VOLUMES = os.path.join(NOTES, "volumes.json")
JAVA_LESSONS = os.path.join(REPO, "java", "lessons")
JAVA_RECORDS = os.path.join(REPO, "java", "records.csv")
THRESHOLD = 10
SKIP_TAGS = {"고득점Kit", "카카오"}
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
KST = timezone(timedelta(hours=9))
GITHUB = "https://github.com/seoktae-lee/algorithm-study/blob/main/cote/notes"


# ---------- 상태 ----------

def load_volumes():
    if not os.path.exists(VOLUMES):
        return []
    with open(VOLUMES, encoding="utf-8") as f:
        return json.load(f)


def published_ids():
    return {i for v in load_volumes() for i in v["ids"]}


def eligible(records):
    """복습을 1회 이상 거쳤고 아직 노트에 안 실린 문제 id (첫 풀이 순)"""
    done = published_ids()
    reviewed = {r["id"] for r in records if r["kind"] == "redo"}
    order = []
    for r in sorted(records, key=lambda x: x["date"]):
        if r["id"] in reviewed and r["id"] not in done and r["id"] not in order:
            order.append(r["id"])
    return order


def progress(records):
    return {"ready": len(eligible(records)), "threshold": THRESHOLD, "next_vol": len(load_volumes()) + 1}


# ---------- 카드 생성 (claude -p) ----------

def primary_type(p, card=None):
    tags = [t for t in p.get("tags", []) if t not in SKIP_TAGS]
    if tags:
        return tags[0]
    return (card or {}).get("type") or "기타"


def problem_files(path):
    d = os.path.join(ROOT, path) if path else None
    if not d or not os.path.isdir(d):
        return "", ""
    codes = sorted(glob.glob(os.path.join(d, "Solution*.java")) + glob.glob(os.path.join(d, "solution*.sql")))
    parts = []
    for c in codes:
        with open(c, encoding="utf-8") as f:
            parts.append(f"// ===== {os.path.basename(c)} =====\n{f.read()}")
    note = ""
    if os.path.exists(os.path.join(d, "NOTE.md")):
        with open(os.path.join(d, "NOTE.md"), encoding="utf-8") as f:
            note = f.read()
    return "\n\n".join(parts), note


def extract_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("JSON 없음")
    return json.loads(m.group(0))


def ask_claude(prompt):
    p = subprocess.run(["claude", "-p", prompt, "--model", "sonnet", "--allowedTools", "WebFetch"],
                       capture_output=True, text=True, timeout=600, cwd=ROOT)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[:300])
    return extract_json(p.stdout)


CARD_PROMPT = """너는 코딩테스트 복습 노트 편집자다. 아래 학생(석태, Java로 프로그래머스 준비)의 풀이를 보고
인쇄해서 반복해 볼 '문제 카드'를 만든다. 한국어, 짧고 정확하게. 학생의 기록(NOTE, 한 줄 기록, ❌/💡 이력)에 나온
실수를 우선 반영하고, 코드에 없는 내용을 지어내지 마라. 문제 원문을 복사하지 말 것(요약만). 필요하면 문제 링크를 WebFetch해도 된다.

[문제] {id} {title} (Lv.{level}) 유형 태그: {tags}
링크: {url}
[풀이 기록]
{history}
[NOTE.md]
{note}
[코드]
{code}

아래 JSON 하나만 출력 (설명·코드펜스 금지):
{{
 "type": "가장 핵심적인 알고리즘 유형 1개 (예: 해시, 스택, BFS, 그리디, DP, 구현, 문자열)",
 "summary": "문제 한 줄 요약 (40자 이내)",
 "signal": "문제에서 이 유형을 알아보는 신호 (1문장)",
 "idea": "핵심 아이디어 (1~2문장)",
 "concept": "필요한 핵심 개념 설명 (2~3문장, 왜 이 방법이 맞는지)",
 "steps": ["풀이 단계 3~5개, 각 25자 이내"],
 "code": "핵심 로직만 담은 Java 코드 조각 (최대 10줄, 학생 코드를 다듬은 것)",
 "pitfalls": ["실수·함정 1~3개 (학생 기록 우선)"],
 "complexity": "시간 O(..) / 공간 O(..)",
 "java": ["이 문제에서 쓴 Java 문법·API 1~3개 (예: getOrDefault, Arrays.sort)"]
}}"""

TYPE_PROMPT = """코딩테스트(Java) 복습 노트의 '유형 정리' 박스를 만든다. 유형: {type}
이 노트에 실린 이 유형의 문제: {titles}
한국어, 인쇄용으로 짧고 정확하게. 아래 JSON 하나만 출력 (설명·코드펜스 금지):
{{
 "concept": "이 유형의 핵심 개념 (2~3문장)",
 "when": ["이 유형을 의심할 신호 2~3개"],
 "template": "Java 기본 템플릿 코드 (최대 12줄)",
 "pitfalls": ["자주 하는 실수 2개"],
 "complexity": "대표 시간복잡도"
}}"""


def history_text(pid, records):
    rows = [r for r in records if r["id"] == pid]
    kind = {"first": "첫 풀이", "redo": "복습", "mock": "모의고사"}
    return "\n".join(f"- {r['date']} {kind.get(r['kind'], r['kind'])} {r['result']} {r['minutes']}분 — {r['note']}" for r in rows) or "-"


def make_card(cfg, get_problem, pid, records):
    path = os.path.join(CARDS, f"{pid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    p = get_problem(cfg, pid) or {"id": pid, "title": pid, "level": "?", "tags": [], "url": ""}
    rec = next((r for r in records if r["id"] == pid), {})
    code, note = problem_files(rec.get("path", ""))
    card = ask_claude(CARD_PROMPT.format(id=pid, title=p["title"], level=p["level"], tags=", ".join(p.get("tags", [])) or "-",
                                         url=p.get("url", ""), history=history_text(pid, records),
                                         note=note or "(비어 있음)", code=code or "(코드 미저장)"))
    card.update({"id": pid, "title": p["title"], "level": p["level"], "url": p.get("url", ""), "tags": p.get("tags", [])})
    card["type"] = primary_type(p, card)
    os.makedirs(CARDS, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=1)
    return card


def make_type(t, titles):
    os.makedirs(TYPES, exist_ok=True)
    path = os.path.join(TYPES, re.sub(r"[^\w가-힣]+", "_", t) + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    box = ask_claude(TYPE_PROMPT.format(type=t, titles=", ".join(titles)))
    box["type"] = t
    with open(path, "w", encoding="utf-8") as f:
        json.dump(box, f, ensure_ascii=False, indent=1)
    return box


def build_cards(cfg, get_problem, ids, records):
    out, failed = [], []
    print(f"🧠 카드 작성 중 ({len(ids)}문제, 문제당 30초~1분 · 4개씩 동시에)…")

    def one(pid):
        try:
            return make_card(cfg, get_problem, pid, records)
        except Exception as e:
            failed.append((pid, str(e)))
            return None

    with ThreadPoolExecutor(4) as ex:
        for pid, card in zip(ids, ex.map(one, ids)):
            if card:
                out.append(card)
                print(f"   ✅ {pid} {card['title']} · {card['type']}")
    for pid, err in failed:
        print(f"   ⚠️ {pid} 카드 실패: {err} (다음 발행 때 다시 시도)")
    return out


# ---------- 자바 치트시트 ----------

def java_cheats(keys=None):
    """완료한 자바 레슨의 📌 핵심 요약. keys가 주어지면 그 레슨만"""
    done = set()
    if os.path.exists(JAVA_RECORDS):
        with open(JAVA_RECORDS, encoding="utf-8") as f:
            done = {line.split(",")[1] for line in f.read().splitlines()[1:] if line}
    out = []
    for d in sorted(os.listdir(JAVA_LESSONS)) if os.path.isdir(JAVA_LESSONS) else []:
        key = "L" + d[1:3]
        if key not in done or (keys is not None and key not in keys):
            continue
        with open(os.path.join(JAVA_LESSONS, d, "README.md"), encoding="utf-8") as f:
            md = f.read()
        title = re.search(r"^# (.+)$", md, re.M).group(1)
        m = re.search(r"^## 📌[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
        if m:
            out.append({"key": key, "title": title, "md": m.group(1).strip()})
    return out


# ---------- 렌더링 ----------

def e(s):
    return html.escape(str(s or ""))


def md_block(md):
    parts, pos = [], 0
    for m in re.finditer(r"```\w*\n(.*?)```", md, re.S):
        if md[pos:m.start()].strip():
            parts.append(f"<p>{e(md[pos:m.start()].strip())}</p>")
        parts.append(f"<pre>{e(m.group(1).rstrip())}</pre>")
        pos = m.end()
    if md[pos:].strip():
        parts.append(f"<pre>{e(md[pos:].strip())}</pre>")
    return "".join(parts)


CSS = """
@page { size: A4; margin: 14mm 13mm; }
* { box-sizing: border-box; }
body { font-family: "Apple SD Gothic Neo", "Pretendard", sans-serif; font-size: 9.6pt; line-height: 1.5; color: #1a1a1a; margin: 0; }
pre, code { font-family: Menlo, "D2Coding", monospace; font-size: 8.4pt; }
pre { background: #f5f5f2; border-left: 3px solid #bbb; padding: 5px 8px; margin: 4px 0; white-space: pre-wrap; word-break: break-all; }
h1 { font-size: 22pt; margin: 0 0 4px; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; page-break-after: always; }
.cover .sub { color: #555; font-size: 11pt; }
.toc { columns: 2; font-size: 9pt; margin-top: 18px; }
.toc div { break-inside: avoid; }
h2.type { font-size: 14pt; border-bottom: 2px solid #222; padding-bottom: 2px; margin: 0 0 6px; page-break-before: always; }
h2.type:first-of-type { page-break-before: auto; }
.typebox { border: 1.5px solid #222; border-radius: 4px; padding: 7px 10px; margin-bottom: 10px; break-inside: avoid; background: #fafaf7; }
.card { border: 1px solid #999; border-radius: 4px; padding: 7px 10px; margin-bottom: 9px; break-inside: avoid; }
.card h3 { font-size: 11pt; margin: 0 0 2px; }
.meta { color: #666; font-size: 8.4pt; margin-bottom: 4px; }
.row { margin: 2px 0; }
.lab { display: inline-block; min-width: 52px; font-weight: 700; color: #333; }
ol, ul { margin: 2px 0 2px 18px; padding: 0; }
.hist { color: #666; font-size: 8pt; border-top: 1px dashed #ccc; margin-top: 4px; padding-top: 3px; }
.check { float: right; font-size: 8.5pt; color: #888; }
.java h3 { font-size: 10.5pt; margin: 8px 0 2px; }
"""


def card_html(c, records):
    hist = [r for r in records if r["id"] == c["id"]]
    kind = {"first": "첫", "redo": "복습", "mock": "모의"}
    hline = " → ".join(f"{r['date'][5:]} {kind.get(r['kind'], r['kind'])} {r['result']}" for r in hist)
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs or [])
    return f"""<div class="card">
<span class="check">회독 ☐ ☐ ☐ ☐ ☐</span>
<h3>{e(c['id'])} {e(c['title'])}</h3>
<div class="meta">Lv.{e(c['level'])} · {e(', '.join(c.get('tags', [])) or c['type'])} · {e(c.get('summary'))}</div>
<div class="row"><span class="lab">신호</span>{e(c.get('signal'))}</div>
<div class="row"><span class="lab">아이디어</span><b>{e(c.get('idea'))}</b></div>
<div class="row"><span class="lab">개념</span>{e(c.get('concept'))}</div>
<div class="row"><span class="lab">풀이</span><ol>{li(c.get('steps'))}</ol></div>
<pre>{e(c.get('code'))}</pre>
<div class="row"><span class="lab">함정</span><ul>{li(c.get('pitfalls'))}</ul></div>
<div class="row"><span class="lab">복잡도</span>{e(c.get('complexity'))} &nbsp; <span class="lab">Java</span>{e(' · '.join(c.get('java', [])))}</div>
<div class="hist">내 기록: {e(hline)}</div>
</div>"""


def type_html(b):
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs or [])
    return f"""<div class="typebox">
<div class="row"><span class="lab">개념</span>{e(b.get('concept'))}</div>
<div class="row"><span class="lab">신호</span><ul>{li(b.get('when'))}</ul></div>
<pre>{e(b.get('template'))}</pre>
<div class="row"><span class="lab">실수</span><ul>{li(b.get('pitfalls'))}</ul></div>
<div class="row"><span class="lab">복잡도</span>{e(b.get('complexity'))}</div>
</div>"""


def group_by_type(cards):
    groups = {}
    for c in sorted(cards, key=lambda c: (int(c["level"]) if str(c["level"]).isdigit() else 9, c["id"])):
        groups.setdefault(c["type"], []).append(c)
    return dict(sorted(groups.items(), key=lambda kv: -len(kv[1])))


def render_html(title, subtitle, cards, types, cheats, records):
    groups = group_by_type(cards)
    toc = "".join(f"<div><b>{e(t)}</b> ({len(cs)}) — " + ", ".join(e(c["title"]) for c in cs) + "</div>" for t, cs in groups.items())
    body = [f"""<div class="cover"><h1>{e(title)}</h1><div class="sub">{e(subtitle)}</div>
<div class="sub">유형 {len(groups)}개 · 문제 {len(cards)}개{f' · 자바 치트시트 {len(cheats)}레슨' if cheats else ''}</div>
<div class="sub" style="margin-top:10px">보는 법: ① 유형 박스의 '신호'로 문제를 알아보는 감각 → ② 카드의 아이디어를 가리고 떠올려 보기 → ③ 함정 확인 → 오른쪽 위 ☐에 회독 체크</div>
<div class="toc">{toc}</div></div>"""]
    for t, cs in groups.items():
        body.append(f'<h2 class="type">{e(t)}</h2>')
        if t in types:
            body.append(type_html(types[t]))
        body += [card_html(c, records) for c in cs]
    if cheats:
        body.append('<h2 class="type">☕ 자바 치트시트</h2><div class="java">')
        for ch in cheats:
            body.append(f"<h3>{e(ch['title'])}</h3>{md_block(ch['md'])}")
        body.append("</div>")
    return f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{e(title)}</title><style>{CSS}</style></head><body>{''.join(body)}</body></html>"


def render_md(title, subtitle, cards, types, cheats, records, pdf_name):
    """GitHub·노션용 마크다운 (밤 루틴이 노션 페이지로 옮김)"""
    lines = [f"# {title}", "", f"> {subtitle}", "", f"🖨️ PDF: {GITHUB}/{pdf_name}", ""]
    for t, cs in group_by_type(cards).items():
        lines += [f"## {t}", ""]
        b = types.get(t)
        if b:
            lines += [f"**개념** {b.get('concept', '')}", "", "**신호** " + " / ".join(b.get("when", [])), "",
                      "```java", b.get("template", ""), "```", ""]
        for c in cs:
            lines += [f"### {c['id']} {c['title']} (Lv.{c['level']})", "", f"- **요약** {c.get('summary', '')}",
                      f"- **신호** {c.get('signal', '')}", f"- **아이디어** {c.get('idea', '')}", f"- **개념** {c.get('concept', '')}",
                      "- **풀이** " + " → ".join(c.get("steps", [])), "", "```java", c.get("code", ""), "```", "",
                      "- **함정** " + " / ".join(c.get("pitfalls", [])), f"- **복잡도** {c.get('complexity', '')}",
                      "- **Java** " + " · ".join(c.get("java", [])), ""]
    if cheats:
        lines += ["## ☕ 자바 치트시트", ""]
        for ch in cheats:
            lines += [f"### {ch['title']}", "", ch["md"], ""]
    return "\n".join(lines) + "\n"


def to_pdf(html_path, pdf_path):
    if not os.path.exists(CHROME):
        print("⚠️ Chrome이 없어 PDF 대신 HTML만 만들었어요 (브라우저에서 ⌘P로 PDF 저장)")
        return False
    p = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", "file://" + html_path], capture_output=True, text=True, timeout=180)
    return p.returncode == 0 and os.path.exists(pdf_path)


def write_edition(name, title, subtitle, cards, types, cheats, records):
    os.makedirs(NOTES, exist_ok=True)
    html_path = os.path.join(NOTES, f"{name}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(title, subtitle, cards, types, cheats, records))
    pdf_name = f"{name}.pdf"
    ok = to_pdf(html_path, os.path.join(NOTES, pdf_name))
    with open(os.path.join(NOTES, f"{name}.md"), "w", encoding="utf-8") as f:
        f.write(render_md(title, subtitle, cards, types, cheats, records, pdf_name))
    return os.path.join(NOTES, pdf_name if ok else f"{name}.html")


def all_cards():
    out = []
    for p in sorted(glob.glob(os.path.join(CARDS, "*.json"))):
        with open(p, encoding="utf-8") as f:
            out.append(json.load(f))
    return out


def types_for(cards):
    groups = group_by_type(cards)
    out = {}
    for t, cs in groups.items():
        try:
            out[t] = make_type(t, [c["title"] for c in cs])
        except Exception as ex:
            print(f"   ⚠️ 유형 박스 '{t}' 실패: {ex}")
    return out


def publish(cfg, get_problem, records, level_text, force=False):
    """새 볼륨 발행 → (pdf 경로, 볼륨 번호) 또는 None"""
    ids = eligible(records)
    if not ids or (len(ids) < THRESHOLD and not force):
        print(f"📘 아직 발행 조건 전이에요 ({len(ids)}/{THRESHOLD}). 지금 모인 만큼 만들려면 `cote note`")
        return None
    cards = build_cards(cfg, get_problem, ids, records)
    if not cards:
        return None
    vols = load_volumes()
    no = len(vols) + 1
    today = datetime.now(KST).date().isoformat()
    prev_java = {k for v in vols for k in v.get("java", [])}
    cheats = [c for c in java_cheats() if c["key"] not in prev_java]
    types = types_for(cards)
    name = f"핵심노트_Vol{no:02d}"
    first, last = min(r["date"] for r in records if r["id"] in {c["id"] for c in cards}), today
    path = write_edition(name, f"📘 코테 핵심노트 Vol.{no}", f"{first} ~ {last} · {level_text}", cards, types, cheats, records)
    vols.append({"vol": no, "date": today, "ids": [c["id"] for c in cards], "java": [c["key"] for c in cheats],
                 "pdf": f"notes/{name}.pdf", "md": f"notes/{name}.md"})
    with open(VOLUMES, "w", encoding="utf-8") as f:
        json.dump(vols, f, ensure_ascii=False, indent=1)
    rebuild_full(records, level_text)
    return path, no


def rebuild_full(records, level_text):
    cards = all_cards()
    if not cards:
        print("아직 카드가 없어요")
        return None
    published = published_ids()
    cards = [c for c in cards if c["id"] in published]
    today = datetime.now(KST).date().isoformat()
    return write_edition("핵심노트_전체", "📚 코테 핵심노트 전체판", f"~ {today} · {level_text} · Vol.1~{len(load_volumes())} 통합",
                         cards, types_for(cards), java_cheats(), records)
