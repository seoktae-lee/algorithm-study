// K19-Q1. 상품 이름 배열과 가격 배열이 있을 때 가장 비싼 상품의 이름을 출력하세요
//
// 기대 출력:
// 가방
class Q1 {
    public static void main(String[] args) {
        String[] names = {"연필", "공책", "가방", "지우개"};
        int[] prices = {500, 1500, 25000, 300};
        int maxIndex = 0;
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] > prices[maxIndex]) {
                maxIndex = i;
            }
        }
        System.out.println(names[maxIndex]);
    }
}
