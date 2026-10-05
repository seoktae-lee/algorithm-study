// K23-Q2. 입금 deposit(balance, amount)와 출금 withdraw(balance, amount) 메서드를 만드세요. 출금액이 잔액보다 크면 '잔액이 부족합니다.'를 출력하고 잔액을 그대로 돌려줍니다. 10000원에서 1000원 입금 → 20000원 출금 시도 → 2000원 출금 후 '최종 잔액: 9000' 출력
//
// 기대 출력:
// 잔액이 부족합니다.
// 최종 잔액: 9000
class Q2 {
    public static void main(String[] args) {
        int balance = 10000;
        balance = deposit(balance, 1000);
        balance = withdraw(balance, 20000);
        balance = withdraw(balance, 2000);
        System.out.println("최종 잔액: " + balance);
    }

    public static int deposit(int balance, int amount) {
        return balance + amount;
    }

    public static int withdraw(int balance, int amount) {
        if (amount > balance) {
            System.out.println("잔액이 부족합니다.");
            return balance;
        }
        return balance - amount;
    }
}
