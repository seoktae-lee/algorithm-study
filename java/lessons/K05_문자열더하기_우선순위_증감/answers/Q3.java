// K05-Q3. x=5 에서 시작해 ++ 와 -- 만 사용해서 x를 6 → 7 → 6 으로 바꾸며 매번 출력하세요
//
// 기대 출력:
// 6
// 7
// 6
class Q3 {
    public static void main(String[] args) {
        int x = 5;
        x++;
        System.out.println(x);
        x++;
        System.out.println(x);
        x--;
        System.out.println(x);
    }
}
