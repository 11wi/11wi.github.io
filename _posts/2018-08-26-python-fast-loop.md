# Scheduling Optimization2
4월부터 시작한 쇼핑호스트 스케줄링 최적화 알고리즘은 얼추 개발이 끝난 상태이나,
IT개발팀이 바쁜 관계로 현업에서 사용할 사내 프로그램에 올리지 못하고 있다.
그 덕분에 틈틈이 수정하고 기능을 추가하여, 지금은 지난 달보다 훨씬
완성도가 높아졌다. 로직도 정교해지고, 최적화 과정에 대해 분석할 수 있는 함수도 추가했다.

단 하나 마음에 걸리는 점은 결과 출력까지 1분 가량 걸릴만큼 속도가 안 나온다는 점이었다.
회사 서버에서 Kong이라는 API 게이트웨이를 통해 AWS Lambda에 올린 최적화 소스를 돌리는데
전반적으로 과정도 길고 lambda에서 처리하는 시간도 길다보니 현업에서 불만이 나올법하다는 생각이 들었다.
이를 해결하기 위해 Python 로직을 빠르게 실행하는 방법을 공부했었고 이번 글에서 정리해보고자 한다.

# Fast Loop
이와 관련된 글은 쉽게 찾을 수 있는데 대체로 파편화된 글이 많아 이를 종합하여 정리해볼 필요를 느꼈다.

0. numpy
1. map
2. multiprocess module
3. concurrent.futures module

# 0. numpy
numpy는 숫자형 데이터 연산에 요긴한 모듈인데, 이번 프로젝트는 숫자와는 관련이 없어
실제 적용해보진 못했다. 일단 몇가지 numpy 모듈로 성능을 올리는 방법은,
- `numpy.float64`, `numpy.int64`처럼 numpy 데이터 타입으로 변환한다.
- `numpy.vetorize`로 스칼라 연산을 벡터 연산으로 변환한다.

# 1. map
실제 프로젝트에서 썼던 방법이고 data science만 공부했던 내겐 이해가 어려운 함수다.
map에 대해선 다른 분이 나보다 더 잘 알려줄 것 같아, 간단히 용법만 정리해보려 한다.

- `map(function, arg)`: `R`의 `lapply`와 유사한 느낌으로 input list를 함수 처리해준다.
- `map(function, arg1, arg2)` 형태를 쓰려면: `map(lambda x: function(x, y=fix),
arg)`처럼 fix 변수를 고정해서 쓸 수 있고 (또는 `from functools import partial`)
```
import itertools
args=itertools.product(x, y)
map(function, args)
```
`product`를 통해 x,y 변수쌍을 넣을 수 있다.

# 2. multiprocess module
회사 서버를 이용한다면 10 cpu로 연산이 가능하여 엄청난 성능 향상이 가능하나, lambda에서도
그 정도 향상이 있을지 불투명하고, 프로젝트의 핵심인 docplex 객체에는 적용이 불가한 것으로 판명.

- pickle이 가능한 함수/객체만 적용 가능하다.

```
import pickle
pickle.dumps(object or function)
```

위 소스로 pickle 가능 여부를 확인할 수 있다. 에러가 난다면, multiprocess는 어렵다. docplex 객체는 pickle이 불가능해 프로젝트에서 제외했다.

- 병렬 처리할 함수는 nested class나 function의 하위 레벨에 놓지 말고 따로 분리하여 작성한다.

```
<class 내부에서 구현할 경우>
import multiprocess

class A():

    def do_parallel(x, y):
        out = model.add_constraint_(x >= y)
        return out

    def run(x):
        pool = multiprocess.Pool()
        result = pool.map(do_parallel, x)
```

데이터 크롤링이나 pandas를 이용한 단순 데이터 전처리에는 엄청난 성능 향상이 있어 대용량 처리에는 종종 쓰게 된다. 12 core 회사 서버에서는 작업 속도가 10배 이상 향상된 경험이 있다.

- do_parallel 함수에서 미리 선언된 하나의 객체에 접근해선 안되고
함수에서 선언한 새로운 객체를 사용해야 올바른 결과를 볼 수 있다. (이 때문에 하나의 model 객체를 쓰는 docplex에서는 multiprocess를 쓸 수 없다)

# 3. concurrent.futures module
multiprocess 모듈을 개선한 모듈로 보이나, 쓰레드처리가 아닌 병렬처리를 원한다면
내부적으로 multiprocess 모듈을 사용하므로 굳이 사용할 이유가 없다고 생각한다.
multiprocess을 사용하기 때문에 동일한 제약이 있으며,
제대로 사용하지 못하면 multiprocess보다 못한 성능이 나온다.

# conclusion
프로젝트에서 실제로 사용한 건 map 함수였으며, 단순히 for 문으로 처리한 것보다 2/3 시간으로 단축할 수 있었다. 함수 용법도 한 번 익숙해지면 어렵지 않고, 데이터 전처리에서도 map 함수와 multiprocess를 활용하면 작업 시간을 크게 단축할 수 있어 데이터 사이언티스트에게 사용을 권해보고 싶다.
