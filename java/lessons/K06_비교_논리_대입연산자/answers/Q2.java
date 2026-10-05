// K06-Q2. str1과 str2의 '내용'이 같은지 출력하세요 (true가 나와야 함)
//
// 기대 출력:
// true
class Q2 {
    public static void main(String[] args) {
        String str1 = "hello";
        String str2 = new String("hello");
        System.out.println(str1.equals(str2));
    }
}
