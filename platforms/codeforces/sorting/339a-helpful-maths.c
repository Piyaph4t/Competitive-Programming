#include <stdio.h>
#include <stdio.h>
#include <string.h>

int freq[4];
int main(){
    char c;
    while( (c = getchar()) != '\n' ){
        if (c == '+') ++freq[0];
        else ++freq[c - '0'];
    }
    for(int i=1;i<=3;i++){
        while(freq[i]--){
            putchar(i+'0');
            if(freq[0]--) putchar('+');
        }
    }
    return 0;
}
