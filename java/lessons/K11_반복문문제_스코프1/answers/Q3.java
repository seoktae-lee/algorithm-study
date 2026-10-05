// K11-Q3. 스코프 컴파일 에러를 고쳐서 30이 출력되게 하세요 (x를 if 블록 밖에서 쓰고 있어요)
//
// 기대 출력:
// 30
class Q3 {
    public static void main(String[] args) {
        int m = 10;
        int x = 0;
        if (true) {
            x = 20;
        }
        System.out.println(m + x);
    }
}
