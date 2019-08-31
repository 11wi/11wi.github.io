---
category: data-science
---


# bayesian mf

matrix factorization이 필요한 프로젝트가 있어서 공부하다보니 hyper parameter를 tuning하지 않아도 되는
편리한 mf를 발견했고 바로 구현해봤다. 
bayesian 이론에 대해 탄탄한 기초는 없지만 논문 저자가 올린 matlab 코드를 참조했기 때문에 어렵지 않았다.
08년 논문이지만 공부하기에도 좋고 참조할만한 github도 적어서 공유한다.   
  
구현해보니 장점은 bayesian의 장점인 빠른 수렴과 hyper parameter를 prior로 대체하여 latent 크기만 정하면 된다는 점,  
단점은 dataset이 작으면 성능이 매우 안 나온다는 점을 체감했다. (원래 mf면 dataset이 크기 마련인데
프로젝트 특성상 어쩔 수 없는 부분)
  
아쉬운 점은 parallel learning을 구현하려했지만 제대로 성능이 나오지 않아 일단 방치했다..

참고 자료는  
[논문링크](https://www.cs.toronto.edu/~rsalakhu/papers/bpmf.pdf)  
[논문저자matlab코드](http://www.utstat.toronto.edu/~rsalakhu/code_BPMF/bayespmf.m)  
[논문구현github](https://github.com/LoryPack/BPMF)

구현한 소스코드는  
[bpmf.py](../images/bpmf.py) - `sklearn estimator`로 구현  
[matrix_util.py](../images/matrix_util.py) - `bpmf.py`에서 사용하는 util 함수  
[test-data](../images/moviedata.mat) - sample dataset

```python
# train data
triplet_train = numpy.array([0, 0, 5], # user 0, item 0, rating 5
                            [3, 1, 3], # user 3, item 1, rating 3
                             ...) 

# test data 
triplet_test = numpy.array([0, 1, 5], # user 0, item 1, rating ignored
                           [3, 1, 3], # user 3, item 1, rating ignored
                            ...) 
also_triplet_test = numpy.array([0, 1], # user 0, item 1
                                [3, 1], # user 3, item 1
                                 ...) 
```

```python
# main function
from scipy import io

from model.bpmf import bpmf

# Triplets: {user_id, movie_id, rating}
raw = io.loadmat('moviedata.mat')
train_set = raw['train_vec'] - 1  # minus 1 to make data start from 0
test_set = raw['probe_vec'] - 1

n_user = 6040  # Abbreviation of person
n_item = 3952  # Abbreviation of movie

model = bpmf(max_value=5, min_value=0,
             n_user=n_user, n_item=n_item,
             early_stop_step=3, validatset=test_set,
             verbose=True)

model.fit(train_set[:, [0, 1]], train_set[:, 2])
model.predict(test_set)

# compatible with sklearn
from sklearn.model_selection import GridSearchCV


grid_search_pool = {'n_latent': [10, 15]}
cv_model = bpmf(max_value=5, min_value=0,
                n_user=n_user, n_item=n_item,
                early_stop_step=3)
grid_searcher = GridSearchCV(cv_model, grid_search_pool, cv=5, scoring='neg_mean_absolute_error',
                             n_jobs=2, error_score='raise')
grid_searcher.fit(train_set[:, [0, 1]], train_set[:, 2])
grid_searcher.best_params_
```