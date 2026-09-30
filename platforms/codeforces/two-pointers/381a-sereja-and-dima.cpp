#include <iostream>
#include <vector>
using namespace std;
int main() {
    cin.tie(nullptr)->sync_with_stdio(0);
    int n;
    cin >> n;
    long long ans[2] = {0};
    vector<int> vec(n);
    for (int& x : vec)
        cin >> x;

    int i = 0, j = n - 1;
    int turn = 0;
    while (i <= j && j >= 0) {
        int pick;
        if (vec[i] > vec[j]) {
            pick = vec[i];
            i++;
        } else {
            pick = vec[j];
            j--;
        }
        ans[turn % 2] += pick;
        turn++;
    }
    cout << ans[0] << " " << ans[1] << "\n";
    return 0;
}
