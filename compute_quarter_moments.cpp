// Exact integer Horner columns for the pinned thermal construction.
// Extends the version 1.6 evaluator by twist 3 (pi/2), using Gaussian pairs.
// Earlier twists retain their original Eisenstein or real coordinates.
// No floating-point arithmetic enters the returned integer total.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
#include <omp.h>

using I = std::int64_t;
using Wide = __int128_t;
struct Big {
    std::array<std::uint64_t,4> limbs{};
    Big(int zero=0) { if(zero)throw std::runtime_error("Nonzero initializer"); }
    Big& operator+=(const Big& other) {
        __uint128_t carry=0;
        for(int k=0;k<4;k++) {
            carry+=static_cast<__uint128_t>(limbs[k])+other.limbs[k];
            limbs[k]=static_cast<std::uint64_t>(carry);carry>>=64;
        }
        if(carry)throw std::runtime_error("256-bit addition overflow");
        return *this;
    }
    std::string str() const {
        auto a=limbs;std::string out;
        while(a[0] || a[1] || a[2] || a[3]) {
            __uint128_t rem=0;
            for(int k=3;k>=0;k--) {auto x=(rem<<64)+a[k];a[k]=x/10;rem=x%10;}
            out.push_back('0'+static_cast<int>(rem));
        }
        if(out.empty())out="0";
        std::reverse(out.begin(),out.end());return out;
    }
};
struct Row { int diag; std::vector<int> plain, plus, minus; };
I floor32(I x) { return x/32 - (x%32 < 0); }
Big widen(Wide x) {
    if (x < 0) throw std::runtime_error("Negative norm total");
    auto u=static_cast<__uint128_t>(x);
    Big b;b.limbs[0]=static_cast<std::uint64_t>(u);b.limbs[1]=static_cast<std::uint64_t>(u>>64);return b;
}

int main(int argc,char** argv) {
    if(argc!=5) { std::cerr<<"usage: engine LENGTH TWIST COEFFICIENTS THREADS\n";return 2; }
    int n=std::stoi(argv[1]),tw=std::stoi(argv[2]),threads=std::stoi(argv[4]);
    if(n<4 || n>12 || tw<0 || tw>3 || threads<1 || threads>8) return 2;
    omp_set_num_threads(threads);
    std::ifstream input(argv[3]);std::vector<I> coeff; I c;
    while(input>>c) {if(c<0 || c>(I(1)<<55)) return 2;coeff.push_back(c);}
    if(coeff.empty()) return 2;
    std::vector<int> pow3(n+1,1);for(int j=1;j<=n;j++)pow3[j]=3*pow3[j-1];
    auto digits=[&](int x) {
        std::vector<int> w(n);for(int j=0;j<n;j++)w[j]=(x/pow3[n-1-j])%3-1;return w;
    };
    std::vector<std::vector<int>> blocks(n+1);
    for(int x=0;x<pow3[n];x++) {
        auto w=digits(x);int m=0;for(int a:w)m+=a;
        if(m>=0)blocks[m].push_back(x);
    }
    Big total=0;long long multiplicity=0;int max_row_l1=0;
    for(int m=0;m<=n;m++) {
        auto start=std::chrono::steady_clock::now();
        const auto& words=blocks[m];int d=words.size();
        std::vector<int> lookup(pow3[n],-1);
        for(int i=0;i<d;i++)lookup[words[i]]=i;
        std::map<int,int> counts;
        std::vector<Row> rows(d);
        for(int i=0;i<d;i++) {
            auto w=digits(words[i]);int representative=words[i];
            for(int rev=0;rev<2;rev++)for(int k=0;k<n;k++) {
                int code=0;for(int j=0;j<n;j++) {
                    int idx=(j+k)%n;if(rev)idx=n-1-idx;
                    code=3*code+w[idx]+1;
                }
                representative=std::min(representative,code);
            }
            if(lookup[representative]<0)throw std::runtime_error("Representative block");
            counts[lookup[representative]]+=(m==0 ? 1:2);
            int zz=0;for(int j=0;j<n;j++)zz+=w[j]*w[(j+1)%n];
            auto& r=rows[i];r.diag=32-3*n-2*zz;
            for(int j=0;j<n;j++)for(int delta:{-1,1}) {
                int k=(j+1)%n;
                if(std::abs(w[j]-delta)>1 || std::abs(w[k]+delta)>1)continue;
                int code=words[i]-delta*pow3[n-1-j]+delta*pow3[n-1-k];
                int idx=lookup[code];if(idx<0)throw std::runtime_error("Hop block");
                int phase=(k==0 && tw!=0) ? delta:0;
                if(phase==-1 && tw==1)phase=1;
                (phase==0 ? r.plain : phase==1 ? r.plus:r.minus).push_back(idx);
            }
            // Absolute row sums of the two real coordinate recurrences.
            int l1u=std::abs(r.diag)+2*r.plain.size()+2*r.plus.size()+4*r.minus.size();
            int l1v=std::abs(r.diag)+2*r.plain.size()+4*r.plus.size()+2*r.minus.size();
            max_row_l1=std::max({max_row_l1,l1u,l1v});
        }
        std::vector<int> reps,weights;
        for(auto [r,w]:counts){reps.push_back(r);weights.push_back(w);multiplicity+=w;}
        constexpr int batch=64;
        int batches=(reps.size()+batch-1)/batch;
        std::vector<Big> subtotals(batches);
        #pragma omp parallel for schedule(dynamic)
        for(int block=0;block<batches;block++) {
            int offset=batch*block,w=std::min(batch,static_cast<int>(reps.size())-offset);
            std::vector<I> u(d*w),v(d*w),y(d*w),z(d*w);
            for(auto it=coeff.rbegin();it!=coeff.rend();it++) {
                for(int i=0;i<d;i++) {
                    const auto& r=rows[i];int base=i*w;
                    for(int a=0;a<w;a++){y[base+a]=r.diag*u[base+a];z[base+a]=r.diag*v[base+a];}
                    for(int j:r.plain)for(int a=0;a<w;a++){y[base+a]-=2*u[j*w+a];z[base+a]-=2*v[j*w+a];}
                    if(tw==1) {
                        for(int j:r.plus)for(int a=0;a<w;a++)y[base+a]+=2*u[j*w+a];
                    } else if(tw==2) {
                        for(int j:r.plus)for(int a=0;a<w;a++){y[base+a]+=2*v[j*w+a];z[base+a]+=2*v[j*w+a]-2*u[j*w+a];}
                        for(int j:r.minus)for(int a=0;a<w;a++){y[base+a]+=2*u[j*w+a]-2*v[j*w+a];z[base+a]+=2*u[j*w+a];}
                    } else if(tw==3) {
                        for(int j:r.plus)for(int a=0;a<w;a++){y[base+a]+=2*v[j*w+a];z[base+a]-=2*u[j*w+a];}
                        for(int j:r.minus)for(int a=0;a<w;a++){y[base+a]-=2*v[j*w+a];z[base+a]+=2*u[j*w+a];}
                    }
                    for(int a=0;a<w;a++){y[base+a]=floor32(y[base+a]);z[base+a]=floor32(z[base+a]);}
                }
                u.swap(y);v.swap(z);
                for(int a=0;a<w;a++)u[reps[offset+a]*w+a]+=*it;
            }
            std::vector<Wide> norms(w);
            for(int i=0;i<d;i++)for(int a=0;a<w;a++) {
                Wide x=u[i*w+a],y0=v[i*w+a];norms[a]+=tw==3 ? x*x+y0*y0 : x*x-x*y0+y0*y0;
            }
            Big subtotal=0;for(int a=0;a<w;a++)subtotal+=widen(weights[offset+a]*norms[a]);
            subtotals[block]=subtotal;
        }
        for(auto& s:subtotals)total+=s;
        double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cerr<<"n="<<n<<" twist="<<tw<<" M="<<m<<" dimension="<<d<<" representatives="<<reps.size()<<" seconds="<<seconds<<"\n";
    }
    if(multiplicity!=pow3[n])throw std::runtime_error("Multiplicity total");
    std::cout<<"{\"n\":"<<n<<",\"twist\":"<<tw<<",\"total\":\""<<total.str()<<"\",\"multiplicity_sum\":"<<multiplicity<<",\"maximum_coordinate_row_l1\":"<<max_row_l1<<"}\n";
}
