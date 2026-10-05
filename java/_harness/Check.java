import java.util.*;

/** 연습문제 채점기 — 직접 수정하지 마세요. Exercise.java의 main에서 Check.eq(...)로 사용 */
class Check {
    static int pass = 0, total = 0;

    static void eq(String name, Object actual, Object expected) {
        total++;
        boolean ok;
        try {
            ok = Objects.deepEquals(normalize(actual), normalize(expected));
        } catch (Exception e) {
            ok = false;
        }
        if (ok) pass++;
        System.out.println((ok ? "  ✅ " : "  ❌ ") + name + (ok ? "" : "\n       기대: " + show(expected) + "\n       결과: " + show(actual)));
    }

    /** 람다로 감싸서 예외가 나도 다음 테스트를 계속 진행 */
    static void run(String name, java.util.function.Supplier<Object> actual, Object expected) {
        try {
            eq(name, actual.get(), expected);
        } catch (Throwable t) {
            total++;
            System.out.println("  💥 " + name + "\n       예외: " + t);
        }
    }

    static Object normalize(Object o) {
        if (o instanceof Collection<?> c) return new ArrayList<>(c).toArray();
        return o;
    }

    static String show(Object o) {
        if (o == null) return "null";
        if (o instanceof Object[] a) return Arrays.deepToString(a);
        if (o instanceof int[] a) return Arrays.toString(a);
        if (o instanceof long[] a) return Arrays.toString(a);
        if (o instanceof char[] a) return Arrays.toString(a);
        if (o instanceof double[] a) return Arrays.toString(a);
        if (o instanceof boolean[] a) return Arrays.toString(a);
        if (o instanceof String s) return "\"" + s + "\"";
        return String.valueOf(o);
    }

    static void done() {
        System.out.println("RESULT " + pass + "/" + total);
    }
}
