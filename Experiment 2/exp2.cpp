#include <bits/stdc++.h>
using namespace std;

double getPow(double x, int n) {
    if(n == 0) return 1;
    if(n == 1) return x;

    double half = getPow(x, n/2);
    if(n % 2) {
        return half * half * x;
    } else {
        return half * half;
    }
}

double myPow(double x, int n) {
    if(n < 0) {
        return (1/getPow(x, n));
    } else {
        return getPow(x, n);
    }
}

int main() {
    int n = 10;
    int x = 2;

    cout<<myPow(x, n)<<endl;
    return 0;
}