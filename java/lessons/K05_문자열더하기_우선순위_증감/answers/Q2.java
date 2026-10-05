// K05-Q2. price=1000원짜리를 count=3개 사고 delivery=2500원 배송비를 낼 때 총액을 '총액: 5500원' 형태로 출력하세요
//
// 기대 출력:
// 총액: 5500원
class Q2 {
    public static void main(String[] args) {
        int price = 1000;
        int count = 3;
        int delivery = 2500;
        int total = price * count + delivery;
        System.out.println("총액: " + total + "원");
    }
}
