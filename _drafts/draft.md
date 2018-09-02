# xgboost
프로젝트에서 주로 사용했던 xgboost 알고리즘을 깊이 이해하고자 정리했다.
- parameters
    - n_jobs: parallel computing
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

# application

- n_jobs
cpu version xgboost를 사용할 때 사용할 core 개수. -1일 경우 모든 core를 사용하는데 이미 core에 할당된 작업이 있으면 그 작업이 끝날 때까지 기다리므로 상당히 오래 걸릴 수 있다.

- booster
    gbtree은 tree based model로 `XGBRegressor`도 gbtree를 쓰기 때문에 엄밀히 regression은 아니다.
    다만 objective를 reg:linear로 사용하기 때문에 continuous y의 error를 계산해준다. 정확한 formula는 알지 못하나, 대강 MSE형태를 쓰는 것으로 보인다.

# not mentioned
- NaN
학습시 target variable에 NaN이 있으면 validation error를 구하지 못해 차질이 있으나, predictor의 NaN은 학습에 지장이 없으며 학습된 트리의 노드를 살펴보면
NaN은 부등식의 왼쪽 방향으로(조건식 True방향) 분류된다.
