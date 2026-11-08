// Exhaustive ungapped paired scans, independent of the released Python matcher.
#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
int mask(char c){switch(c){case 'A':return 1;case 'C':return 2;case 'G':return 4;case 'T':return 8;case 'R':return 5;case 'Y':return 10;case 'S':return 6;case 'W':return 9;case 'K':return 12;case 'M':return 3;case 'B':return 14;case 'D':return 13;case 'H':return 11;case 'V':return 7;default:return 15;}}
int comp(int x){return ((x&1)?8:0)|((x&2)?4:0)|((x&4)?2:0)|((x&8)?1:0);}
vector<int> encode(string s,bool rev=false){vector<int> a;for(char c:s)a.push_back(mask(toupper(c)));if(rev){reverse(a.begin(),a.end());for(int &x:a)x=comp(x);}return a;}
struct Rec{string id;vector<int>s;};
vector<Rec> fasta(string file){ifstream in(file);if(!in)throw runtime_error(file);vector<Rec> a;string l;while(getline(in,l)){if(l.empty())continue;if(l[0]=='>'){istringstream ss(l.substr(1));string id;ss>>id;a.push_back({id,{}});}else for(char c:l)if(!isspace(c))a.back().s.push_back(mask(toupper(c)));}return a;}
struct Hit{int pos,mm,tail;};
vector<Hit> sites(const vector<int>&s,const vector<int>&q,bool rev){vector<Hit> out;for(int i=0;i+(int)q.size()<=(int)s.size();i++){int mm=0,tail=0;bool bad=false;for(int j=0;j<(int)q.size();j++){int b=s[i+j];if(b!=1&&b!=2&&b!=4&&b!=8){bad=true;break;}if(!(b&q[j])){mm++;if(rev?j<3:j>=(int)q.size()-3)tail++;}if(mm>2)break;}if(!bad&&mm<=2)out.push_back({i,mm,tail});}return out;}
int main(int argc,char**argv){if(argc!=6)return 2;auto target=fasta(argv[1]),bg=fasta(argv[2]);ifstream in(argv[3]);ofstream out(argv[4]),lens(argv[5]);out<<"name,role,accession,min_max_mismatches,min_max_terminal_compatible\n";lens<<"name,role,accession,threshold,span\n";string name,f,r;int inner_min,span_min;while(in>>name>>f>>r>>inner_min>>span_min){auto F=encode(f),R=encode(r,true);for(int role=0;role<2;role++){auto &recs=role?bg:target;for(auto &rec:recs){int best=3,strict=3;set<int> sizes[3];for(int ori=0;ori<2;ori++){auto s=rec.s;if(ori){reverse(s.begin(),s.end());for(int &x:s)x=comp(x);}auto fs=sites(s,F,false),rs=sites(s,R,true);for(auto &a:fs)for(auto &b:rs){int inner=b.pos-a.pos-(int)F.size(),span=b.pos+(int)R.size()-a.pos;if(role?inner<0||inner>1000:inner<inner_min||span<span_min||span>500)continue;int k=max(a.mm,b.mm);best=min(best,k);if(!a.tail&&!b.tail)strict=min(strict,k);for(int t=k;t<=2;t++)sizes[t].insert(span);}}if(best<=2){out<<name<<','<<(role?"background":"target")<<','<<rec.id<<','<<best<<','<<strict<<'\n';for(int t=0;t<3;t++)for(int n:sizes[t])lens<<name<<','<<(role?"background":"target")<<','<<rec.id<<','<<t<<','<<n<<'\n';}}cerr<<name<<' '<<role<<" done\n";}}}
