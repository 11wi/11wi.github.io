# python memory efficiency (manipulating big data)

9월 말부터 지금까지 추천 관련 업무를 하느라 바쁘게 지내서 오랫만에 정리글을 쓴다. ~~(지난 글도 아직 정리가 더 필요한데...)~~
이번 기회에 추천시스템에서 자주 보이는 MF/FM/FFM을 써봤고, 빅데이터라고 불릴 정도의 데이터를 다뤄보았다. 현재 작업한 양은 샘플 데이터임에도 회사 서버 메모리로 감당이 안되는 수준이다보니 작업하는데 애로사항이 많았다.

spark를 쓰는 게 제일 좋을 것 같지만, spark를 거부하며 준비한 (pandas에 익숙한 본인을 기준으로) 쓰기 쉽고 효과적인 memory error 해결법을 소개한다.  

## pandas memory error 해결법
1. dtype 변환
2. chunksize
3. dask 사용
4. modin.pandas 사용 ~~회사 서버에 인스톨이 안됨~~

몇가지 핵심적인 사항만 짚어보자.

* dtype 변환
1. 데이터가 메모리 사이즈보다 작지만, 원활한 전처리가 안될 때 시도.
    - 생각보다 pandas에서 reshape나 save 기능이 먹는 메모리가 상당하여 4GB 데이터인데도 16GB 램이 모자랄 수 있는데, 그럴 때 dtype 변환만으로 해결할 수 있다
1. `category` 를 적극 활용할 것.
    - 특히, category는 범주형 데이터 전처리에서 여러모로 좋으니 왠만하면 category 설정은 하자.
1. `int64`를 `int16`, `int8`등 작은 크기로 바꿀 것.
    - `get_dummies`에서 쓰는 `uint`는 음수가 아닌 양의 정수 타입을 뜻함.

* chunksize
1. `read_csv(..., chunksize=1000)` iterator 객체 형태로 데이터를 쓸 수 있다.
2. 고용량 text에서 간단히 샘플링할 때 쉽고 간편.
2. `..to_csv(..., chunksize=1000)` 1000개씩 끊어서 저장하기 때문에 작업에 걸리는 램 사용량이 굉장히 줄어들지만 성능이 비교적 느리다.

* dask
1. pandas와 유사해 사용법이 매우 쉬워보이지만, 생각보다 러닝 커브가 있음.
2. 일정 수준보다 `npartition`을 높게 잡아줘야하고, `Client`를 써야 성능을 제대로 낼 수 있을 것.
3. [dask tutorial](https://github.com/dask/dask-tutorial).

> 추가: parquet 자료형 추천한다. csv보다, pickle보다 용량/성능/호환성 면에서 나쁜 것도 없고 좋은 점이 더 많다. 특히 용량면에서는 sparse matrix의 경우 pickle의 1% 크기여서 파일이 잘못된 건지 체크할 정도.
