# xgboost
프로젝트에서 주로 사용했던 xgboost(v72) 알고리즘을 깊이 이해하고자 정리했다.
- parameters
    - n_jobs/nthread: parallel computing
    - booster: gbtree/gblinear/dart
    - objective: reg:linear etc
    - tree specifing args: max_dept/min_child_weight
    - gamma: hessian sum threshold which determine tree spliting point
    - alpha: lasso regression parameter
    - lambda: ridge regression parameter
    - tree_method: hist, exact, gpu_hist
- args
    - early_stop: eval_set/feval으로 num_boost_round validation 과정
    - eval_set: train/test set 설정
    - feval: eval_set에 적용할 metric


# performance
최적 모델을 뽑기 위해선 gridsearch와 같은 파라미터 튜닝이 필수다. 당연히 계산량이 상당히 많아서 실행속도를 줄여주는 파라미터에 관심이 갈 수 밖에 없다.

- n_jobs
cpu version xgboost wrapper(XGBRegressor)를 사용할 때 사용할 core 개수.
주의할 점은 -1로 설정할 경우 모든 core를 사용하는데 이미 core에 할당된 작업이 있으면 그 작업이 끝날 때까지 기다리므로 상당히 오래 걸릴 수 있다.

- nthread
xgboost wrapper가 아닌 xgboost의 본래 함수에서 쓰는 arg.
xgboost.cv와 gridsearch 함수를 돌린다면 n_jobs와 nthread를 둘 다 사용해야 cpu 점유율이 정상적으로 상승하는 것을 확인했다. cpu 점유율을 보면 n_jobs와 세부적 작동 방식과 다른 것 같지만 잘 모르겠다.


- tree_method
hist 방식이 체감상 가장 빠르다. gpu_hist 사용시 hist보다 약 6배 빨라진 것을 확인했다.


# not mentioned explictly on doc

- parameter tuning
경험상 가장 중요한 parameter는 max_dept, min_child_weight, num_boost_round 3가지 정도로 생각한다. 나머지는 드라마틱한 변화가 없는 편이니 튜닝보다는 feature engineering을 더 보는 게 성능이 좋다. 고려할 순서는
    1. y값 transform ex) sqrt, box-cox
    2. x값 transform ex) sqrt, box-cox
    3. x값 generate ex) x3 = x1/x2, x1*x2, x1^x2

- booster
    `gbtree`은 tree based model로 `XGBRegressor`도 `gbtree`를 쓰기 때문에 엄밀히 regression은 아니다.
    다만 `objective`를 `reg:linear`로 사용하기 때문에 continuous y의 error를 계산해준다. 정확한 formula는 알지 못하나, 대강 MSE형태를 쓰는 것으로 보인다.

    `gbliner`이 우리가 흔히 아는 regression 형태다. 실제로 predict를 해보면 `gblinear`은 피처와 증감 방향과 동일하게 움직이나, `gbtree`에선 monotonous가 아니다.
- gamma
    트리가 분기되는 지점을 결정할 때, obective function 2차 미분값의 합이 gamma보다 커야한다는 의미다. 그래서 목적 함수를 바꾸면 gamma값을 바꿔야 한다.


- NaN
학습시 target variable에 NaN이 있으면 validation error를 구하지 못해 차질이 있으나, predictor의 NaN은 학습에 지장이 없으며 학습된 트리의 노드를 살펴보면
NaN은 부등식의 왼쪽 방향으로(조건식 True방향) 분류된다.

- objective
프로젝트에서 예측의 MAPE도 굉장히 중요한 지표여서 튜닝의 최종단계에서 objective function을 수정해봤다. 기본값도 성능이 좋은 편이어서 굳이 수정할 필요는 없다. 수정을 할 땐 이런 함수를 작성해야하는데
```
def my_custom( preds, dtrain ):
    labels = dtrain.get_label()
    grad = # my formula 1st derivative
    hess = # my formula 2nd derivative
    return grad, hess
```
미분식을 구하기가 불편하다. 그럴 때 [미분계산기](https://www.wolframalpha.com/calculators/derivative-calculator/)를 이용하자.


- early_stop
xgboost의 과적합을 피하기 위해 eval_set(train/test error)를 감지한다. 여기서 나온 값이 `num_boost_round`가 되고 `XGBRegressor`라면 `n_estimator`가 된다. 여기서도 cumstom loss를 쓴다면
```
def my_custom(preds, dtrain):
    labels = dtrain.get_label()    
    return 'error', mean_absolute_error(labels, preds)
```
이런 형식이 필요하다.

# gridsearch
