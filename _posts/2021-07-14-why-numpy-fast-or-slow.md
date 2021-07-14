추천 모델 연산에 행렬 곱셈이 많이 쓰이는데 참 신기하게도 사소한 코드에도 성능이 달라진다.
정확한 원리를 알고 시스템을 개선하고자 2개월에 걸쳐 틈틈히 정리해놓았다.
보통 ML Engineer라면 이러한 성능 optimize는 관심이 있을텐데 생각보다 잘 정리된 글을 못 봐서 직접 만들어버렸다 😎 

---

원래 numeric computation에 적합한 언어로 C, C++, Fortran(가장 성능이 좋음)이 꼽혔고 Python은 적합한 언어가 아니었다. 이를 보완하고자 2005년 numpy가 공개되었다.

numpy는 scipy와도 관계가 깊은데 scipy는 [검증된 scientific package를](http://www.netlib.org) wrapping한 것이고, 이에 사용되는 numeric object를 numpy에서 제공한다. <https://www.scipy.org/scipylib/faq.html#how-can-scipy-be-fast-if-it-is-written-in-an-interpreted-language-like-python>

numpy의 핵심은 ndarray(n-dimensional array) class와 numeric operation을 Cython 및 BLAS로 구현한 것이다. ndarray는 fixed size 객체이다. 따라서 append 동작은 new size copy를 생성하고 이전 size를 삭제한다. <https://scipy-lectures.org/advanced/advanced_numpy/>

array 저장 방식은 C order, F order가 있는데 각각 C와 Fortran의 구현체와 대응된다. C는 row-wise, F는 column-wise로 stride의 차이가 있다. tobytes()로 확인해보면 1차원 array의 index로 행/열을 구분함을 알 수 있다.

```
c = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]], dtype=np.int16, order='C')
assert c.strides == (6, 2)

f = np.array(x, order='F')
assert f.strides == (2, 6)

assert f.T.data.f_contiguous, 'transpose changed strides and c order'
```

---

## LAPACK과 BLAS

LAPACK은 Linear Algebra PACKage으로 fortran으로 작성되었으며 linear system algorithm을 제공한다. LAPACK의 내부는 대부분 BLAS 호출로 이뤄져있다. hardware acceleration으로 분류된다.

BLAS는 Strassen algorithm처럼 복잡한 code를 사용한 것이 아니라 cpu cache optimize에 대한 것이다. <https://stackoverflow.com/questions/1303182/how-does-blas-get-such-extreme-performance> SIMD(single instruction multiple data) 개념을 구현한 SSE(Streaming SIMD Extensions), AVX(Advanced Vector Extensions) 기술을 사용한다. C code에서 이를 호출하면 `#include <emmintrin.h> _mm_mul_pd`와 같은 특수한 함수를 사용한다. <http://www.mathematik.uni-ulm.de/~lehn/apfel/sghpc/gemm/> <https://software.intel.com/sites/landingpage/IntrinsicsGuide/#>
하지만 최근 GPU를 주로 사용하면서 AVX와 같은 CPU 최적화 기술은 성장둔화될 것으로 보인다.

---

matrix multiplication의 시간 복잡도는 n^3이지만 [슈트라센 알고리즘](https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication#Strassen's_algorithm)은 n^2.807이다.
numpy는 [blas를 사용하며](https://github.com/numpy/numpy/blob/v1.20.3/numpy/core/src/multiarray/arraytypes.c.src#L3539) multithread로 실행된다. 
blas는 mkl, openblas가 성능이 좋다. <https://software.intel.com/content/www/us/en/develop/articles/numpyscipy-with-intel-mkl.html>
scipy api로 blas를 직접 호출할 수 있다.

```
>>> import numpy as np
>>> np.show_config()
blas_mkl_info:
  NOT AVAILABLE
blis_info:
  NOT AVAILABLE
openblas_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
blas_opt_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
lapack_mkl_info:
  NOT AVAILABLE
openblas_lapack_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
lapack_opt_info:
    libraries = ['openblas', 'openblas']
    library_dirs = ['/usr/local/lib']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
```

별도 설정 없는 m1 mac에서 openblas linkage를 확인했다. intel cpu가 아니기 때문에 당연히 mkl은 안된다.

---

blas 직접 호출시의 성능

```
import numpy as np
from scipy.linalg.blas import dgemm, sgemm

a = np.random.rand(10000, 10000)

%timeit a@a
%timeit dgemm(1, a, a)
%timeit dgemm(1, a, a, trans_a=1, trans_b=1)
```

---

환경변수를 통해 multithread 개수를 지정할 수 있다.

```
OMP_NUM_THREADS: openmp,
OPENBLAS_NUM_THREADS: openblas,
MKL_NUM_THREADS: mkl,
VECLIB_MAXIMUM_THREADS: accelerate,
NUMEXPR_NUM_THREADS: numexpr
```

```
import os
os.environ["OMP_NUM_THREADS"] = "4" # export OMP_NUM_THREADS=4
os.environ["OPENBLAS_NUM_THREADS"] = "4" # export OPENBLAS_NUM_THREADS=4 
os.environ["MKL_NUM_THREADS"] = "6" # export MKL_NUM_THREADS=6
os.environ["VECLIB_MAXIMUM_THREADS"] = "4" # export VECLIB_MAXIMUM_THREADS=4
os.environ["NUMEXPR_NUM_THREADS"] = "6" # export NUMEXPR_NUM_THREADS=6
```

성능 실험을 해보자.

```
import os
os.environ["OPENBLAS_NUM_THREADS"] = "4"
import numpy as np
P = np.random.rand(10000, 500)
Q = np.random.rand(10000, 500)
%timeit P @ Q.T
```

```
1.78 s ± 161 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
P = np.random.rand(10000, 500)
Q = np.random.rand(10000, 500)
%timeit P @ Q.T
```

```
6.95 s ± 245 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

thread에 따른 성능 차이가 확연하다.


---

dtype을 기본적으로 np.float64(double)로 설정되는데 이를 np.float32(single)로 변경만 해도 성능 향상이 있다.


```
import numpy as np
P = np.random.rand(10000, 500)
Q = np.random.rand(10000, 500)
P, Q = np.asarray(P, dtype=np.float32), np.asarray(Q, dtype=np.float32)
%timeit P @ Q.T

237 ms ± 24.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

---

stride가 작으면 cpu에서 fetch를 적게 할 수 있어 성능이 좋다.

```
x = np.zeros((20000,))
y = np.zeros((20000*67,))[::67]
print(x.strides, y.strides)
# (8,) (536,)
%timeit x.sum()
%timeit y.sum()

6.83 µs ± 86.5 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
34.6 µs ± 1.59 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

---

numpy code를 어떻게 짜느냐에 따라 속도 차이가 큰데, 이는 temporary array를 만들면서 cache 사용을 제대로 하지 못하기 때문에 발생한다.

cache 사용에 따라 통상 2~4배 성능 차이가 있다. <https://numexpr.readthedocs.io/projects/NumExpr3/en/latest/intro.html#how-it-works>

cache 전략은 cache size만큼 chunk하기, 연산하는 data의 address를 가깝게 하기 (aligned data).

```
import numpy as np
P = np.random.rand(10000, 5000)
Q = np.random.rand(10000, 5000)
P, Q = np.asarray(P, dtype=np.float32), np.asarray(Q, dtype=np.float32)
import numexpr as ne
%timeit 3 * P + 2 * Q
%timeit ne.evaluate("3 * P + 2 * Q")

121 ms ± 990 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
42.4 ms ± 178 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

---

optimization을 위해 numpy를 numba, cython으로 바꾸기도 한다.

서로 성능은 비슷하나 numba는 numeric array 연산만 쉽고 다른 기능은 제한이 많으며 conda 환경을 권장한다. cython은 python code를 대부분 쓸 수 있고 robust하다. <http://stephanhoyer.com/2015/04/09/numba-vs-cython-how-to-choose/>

numpy + cython은 numpy C API를 써서 힘들다고는 한다. <https://cython.readthedocs.io/en/latest/src/tutorial/numpy.html>

하지만 실질적으로 MKL과 같은 kernel lib를 배제할순 없다. <https://stackoverflow.com/questions/56920713/numpy-faster-than-numba-and-cython-how-to-improve-numba-code>

---

distributed computing은 OpenMPI로 구현된다. https://mpi4py.readthedocs.io/en/stable/tutorial.html [uber 분산 학습 시스템](https://github.com/horovod/horovod)에서도 사용한다.

opencl은 cuda처럼 gpu programming

---

## octave benchmark

```
[_,_,t,_]=speed("p*q'", 'p=rand(30000,500); q=rand(30000,500)');
mean(t)
ans =  2.7118
```

## numpy benchmark

```
import numpy as np
p = np.random.rand(30000, 500)
q = np.random.rand(30000, 500)
Pf, Qf = np.asarray(p, dtype=np.float32, order='F'), np.asarray(q, dtype=np.float32, order='F')
Pc, Qc = np.asarray(p, dtype=np.float32, order='C'), np.asarray(q, dtype=np.float32, order='C')
%timeit Pf @ Qf.T
%timeit Pc @ Qc.T

# macbook pro 16 inch 2019
2.71 s ± 213 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
2.88 s ± 19 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# m5.16xlarge
2.11 s ± 827 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
1.82 s ± 136 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

## materials

https://developer.ibm.com/blogs/use-python-for-scientific-research/
https://developer.ibm.com/languages/python/articles/ba-accelerate-python/
https://users.ece.cmu.edu/~franzf/papers/gttse07.pdf

## cython

https://cython.readthedocs.io/en/latest/src/userguide/parallelism.html
https://github.com/pydata/bottleneck/issues/92
https://github.com/benfred/implicit/blob/master/implicit/nearest_neighbours.h
https://numpy.org/doc/1.17/reference/c-api.html

