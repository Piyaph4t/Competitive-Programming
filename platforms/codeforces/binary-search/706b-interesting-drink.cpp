#include <algorithm>
#include <iostream>
using namespace std;

int main() {
    int n, q;
    cin >> n;

    int shop[n];
    for (int& s : shop)
        cin >> s;
    cin >> q;
    sort(shop, shop + n);

    int m;
    while (q--) {
        int m;
        cin >> m;
        int* pos = upper_bound(shop, shop + n, m);

        cout << pos - shop << "\n";
    }
    return 0;
}
