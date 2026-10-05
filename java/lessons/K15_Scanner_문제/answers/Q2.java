import java.util.*;

// K15-Q2. 상품 가격과 수량을 입력받아 '총 비용: 30000' 을 출력하세요
//
// 입력 (채점기가 자동으로 넣어 줌):
// 10000 3
//
// 기대 출력:
// 총 비용: 30000
class Q2 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int price = sc.nextInt();
        int quantity = sc.nextInt();
        System.out.println("총 비용: " + price * quantity);
    }
}
