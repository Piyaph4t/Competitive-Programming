#include <stdio.h>
const int max_n = 1e6 + 10;
#define max(a, b) ((a>b)?(a):(b))
int main(){
    
    char s[max_n];
    if( scanf("%s", s) != 1 )
        return -1;
    
    char *c = s; 
    int ans = 1;
    while(*c){
        char *sc = c;
        while(*c && *c == *(c+1))
            c++;
       ans = max(ans, (int)(c-sc) + 1);
       c++;
    }
    printf("%d\n",ans);
    return 0;
}
