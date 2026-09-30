#include <iostream>
using namespace std;
int main(){
   int n, k; cin >> n >>k ;
   int arr[n];

   for(int i=0;i<n;++i) cin >> arr[i];

   int left = 0;
   int right = 0;

   int curr_sum = 0;
   int num = 0;
   while(left <= right && right < n){
       if(curr_sum + arr[right] <= k){
            curr_sum += arr[right];
           ++right;
       }
       else {
           curr_sum -= arr[left++];
           if(curr_sum < 0) {
               right++;
               curr_sum = 0;
           }
       }
       if(curr_sum == k) {
           num++;
       }
       #ifdef DEBUG
       printf("Window [%d ... %d] => sum :%d\n",left , right, curr_sum);
       #endif
   }
    cout << num << "\n";
   return 0;
}
