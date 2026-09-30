#include <bits/stdc++.h>
using namespace std;

#define drawX(size, count) ((size) * (count) - count)
void fill_col(vector<string> &s, int col) {
  for (int i = 0; i < s.size(); ++i)
    s[i][col] = 'x';
}
void fill_row(vector<string> &s, int row, int start, int stop) {
  while (start <= stop) {
    s[row][start++] = 'x';
  }
}

void send_signal(vector<pair<int, int>> &interval, vector<string> &signal,
                 int &size) {
  int index = 0;
  if (interval[0].first == 0)
    fill_col(signal, 0);
  for (int i = 0; i < interval.size(); ++i) {
    int state = interval[i].first;
    int count = interval[i].second;

    int state_row = 0;
    if (state == 0)
      state_row = size - 1;

    fill_row(signal, state_row, index, index + drawX(size, count));
    index += drawX(size, count);
    if (i != interval.size() - 1)
      fill_col(signal, index);
  }
}

string ascii_to_binary(int c) {
  string bin = "";
  while (c) {
    bin.push_back((char)((c % 2) + '0'));
    c /= 2;
  }
  reverse(bin.begin(), bin.end());
  return string(8 - bin.length(), '0') + bin;
}
int main() {
  int size;
  string digit = "", input;
  cin >> input >> size;

  // clean data convert character to binary.
  for (int i = 0; i < input.length(); ++i) {
    if (input[i] != '1' && input[i] != '0') {
      digit += ascii_to_binary(input[i]);
    } else
      digit.push_back(input[i]);
  }
  vector<pair<int, int>> interval;
  int i = 0;
  for (size_t i = 0; i < digit.size();) {
    const char value = digit[i];
    size_t start = i;

    while (i < digit.size() && digit[i] == value) {
      ++i;
    }
    interval.emplace_back(value - '0', i - start);
  }

  vector<string> signal(size, string(digit.length() * (size-1) + 1, '_'));
  send_signal(interval, signal, size);

  // print signals.
  for (vector<string>::iterator c = signal.begin(); c != signal.end(); c++)
    cout << *c << "\n";
  return 0;
}
