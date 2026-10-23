#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <array>
#include <algorithm>
#include <set>
using namespace std;
struct H{int rec,pos,mm,amb;};
int main(int argc,char**argv){string p=argv[1];ifstream in(p+"/rank_input.txt");int N,G;in>>N>>G;vector<int> weight(G);for(auto &w:weight)in>>w;vector<array<vector<H>,2>> all(N);vector<int> lens(N);for(int k=0;k<N;k++){int id,L;in>>id>>L;lens[id]=L;for(int m=0;m<2;m++){int n;in>>n;all[id][m].resize(n);for(auto &h:all[id][m])in>>h.rec>>h.pos>>h.mm>>h.amb;}}int P;in>>P;ofstream out(p+"/fast_risks.tsv");out<<"index\tWC_le2\tWC_le3\tWC_le4\tWC_ambiguous\tGT_le2\tGT_ambiguous\n";
for(int z=0;z<P;z++){int f,r;in>>f>>r;out<<z;for(int model=0;model<2;model++){auto &a=all[f][model];auto &b=all[r][model];array<set<int>,4> found;size_t i=0,j=0;while(i<a.size()&&j<b.size()){if(a[i].rec<b[j].rec){i++;continue;}if(b[j].rec<a[i].rec){j++;continue;}size_t ie=i+1,je=j+1;while(ie<a.size()&&a[ie].rec==a[i].rec)ie++;while(je<b.size()&&b[je].rec==b[j].rec)je++;for(size_t x=i;x<ie;x++)for(size_t y=j;y<je;y++){int inner=b[y].pos-a[x].pos-lens[f];if(inner<0||inner>1000)continue;int group=a[x].rec/2;if(a[x].amb||b[y].amb){found[3].insert(group);continue;}for(int t=2;t<=4;t++)if(a[x].mm<=t&&b[y].mm<=t)found[t-2].insert(group);}i=ie;j=je;}for(int t=0;t<4;t++){if(model==1&&(t==1||t==2))continue;int sum=0;for(int g:found[t])sum+=weight[g];out<<'\t'<<sum;}}out<<'\n';if(z%10000==0)cerr<<z<<" / "<<P<<'\n';} }
