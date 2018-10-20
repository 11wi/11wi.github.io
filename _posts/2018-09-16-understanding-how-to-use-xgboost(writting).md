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
eval_set(train/validation error)으로 early stop을 수행한다. 여기서 나온 값이 `num_boost_round`가 되고 `XGBRegressor`라면 `n_estimator`가 된다. validation error는 `eval_metric`이란 argument로 지정할 수 있는데, 만약 MAPE와 같은 cumstom error function을 원한다면 `f_eval` argument로 다음과 같은 형태 함수를 지정한다.
```
def my_custom(preds, dtrain):
    labels = dtrain.get_label()    
    return 'error', mean_absolute_error(labels, preds)
```


# gridsearch
파라미터 튜닝을 위해 꽤 많이 돌려봤지만, 생각보다 randomized search의 성능과 속도가 좋은 편은 아니었다.
오히려 잘 짜놓은 gridsearch가 적당한 값을 빠르게 찾아주었다. 아래 사용했던 소스를 올렸으며, 소스의 원안은 [포스팅을 참조](https://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/)
```
다음엔 꼭 잊지 말고 채우자.

```

# dart

간단히 비교 모델로 테스트해봤는데 딥러닝에서 쓰는 drop out이 가미된 xgboost라고 보면 될 것 같다. 결과만 따지면 예측력이 떨어졌는데, 그 이유는 내가 사용한 데이터가 row 개수가 적은 반면 동일한 X input값에 걸린 y 값의 분산이 상당히 크므로 학습이 까다로운 편이다. 그래서 전체적인 패턴을 캐치해서 애매모호한 예측을 하는 전략보다는 소수의 event를 정확히 맞추는 전략이 전체적인 MSE가 낮다. 그런 까닭에 genealized model에 가까운 dart는 오히려 성능이 떨어지고 XGBRegressor의 n_estimator를 올려 overfitting에 가까울수록 성능이 잘 나왔다고 생각한다.
