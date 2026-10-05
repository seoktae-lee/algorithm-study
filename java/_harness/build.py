#!/usr/bin/env python3
"""레슨 빌드: Answer.java(정답) → Exercise.java(빈칸) 생성 + 정답이 모든 테스트를 통과하는지 검증

Answer.java 표기:
    // ▼ answer
    ...정답 코드...
    // ▲ answer
    // TODO: return 0;        ← 빈칸 버전에 들어갈 기본 반환 (없으면 주석만)
    //> buggy code            ← 버그 고치기 레슨: 빈칸 대신 이 코드가 들어감
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS = os.path.join(ROOT, "lessons")


def to_exercise(src):
    out, lines, i = [], src.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "// ▼ answer":
            indent = line[: len(line) - len(line.lstrip())]
            while lines[i].strip() != "// ▲ answer":
                i += 1
            i += 1
            buggy, todo = [], None
            while i < len(lines) and (lines[i].strip().startswith("//>") or lines[i].strip().startswith("// TODO:")):
                s = lines[i].strip()
                if s.startswith("//>"):
                    buggy.append(lines[i].replace("//> ", "", 1).replace("//>", "", 1))
                else:
                    todo = s[len("// TODO:"):].strip()
                i += 1
            if buggy:
                out += buggy
            elif not todo and len(indent) <= 4:
                out.append(indent + "// (필요하면 여기에 도우미 메서드를 만드세요)")
            else:
                out.append(indent + "// TODO 여기를 채우세요")
                if todo:
                    out.append(indent + todo)
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def verify(lesson_dir, name):
    with tempfile.TemporaryDirectory() as t:
        shutil.copy(os.path.join(lesson_dir, name), os.path.join(t, "Exercise.java"))
        shutil.copy(os.path.join(ROOT, "_harness", "Check.java"), t)
        try:
            p = subprocess.run(["java", "Exercise.java"], cwd=t, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return (0, 0), "timeout"
        m = re.search(r"RESULT (\d+)/(\d+)", p.stdout)
        return (int(m.group(1)), int(m.group(2))) if m else (0, -1), p.stdout + p.stderr


def main():
    only = sys.argv[1:]
    bad = 0
    for name in sorted(os.listdir(LESSONS)):
        if only and not any(name.startswith(o) for o in only):
            continue
        d = os.path.join(LESSONS, name)
        with open(os.path.join(d, "Answer.java"), encoding="utf-8") as f:
            src = f.read()
        with open(os.path.join(d, "Exercise.java"), "w", encoding="utf-8") as f:
            f.write(to_exercise(src))
        (ok, total), log = verify(d, "Answer.java")
        (eok, etotal), elog = verify(d, "Exercise.java")
        good = total > 0 and ok == total and etotal >= 0 and eok < max(etotal, 1)
        bad += not good
        print(f"{'✅' if good else '❌'} {name}: 정답 {ok}/{total} · 빈칸 {eok}/{etotal} (컴파일 {'OK' if etotal >= 0 else '실패'})")
        if not good:
            print(log[-3000:])
            if etotal < 0:
                print(elog[-2000:])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
