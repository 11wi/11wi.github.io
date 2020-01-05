---
category: data-science
---


# vector
모든 data는 vector로 표현된다. 
vector는 물리학 개념으로 속력+방향을 뜻한다. 또한 (0,0)이라는 원점을 전제로 한 것이다.
이 원점이 data를 연산할 때 중요한 역할을 한다. 

## vector space로 이해해보자
2개의 설명변수가 있는 회귀분석을 생각해보자.
![](/attachments/regression-matrix.png)

기본적으로 회귀분석은 에러인 e와 설명변수 X 사이의 연관성이 없도록 fitting 된다.
즉 e가 X에 대한 함수로 표현될 수 없다. 
이를 좌표평면으로 그리면 이렇게 된다.
![](/attachments/vector-space.png)

이 그림으로 이해할 수 있는 건 
1. y는 X로 만든 회귀식으로 100% 설명이 되지 않는다. (i.e. 오차 e가 있다) 
2. X는 2차원 평면에 있지만 e는 3차원 z축에 존재한다. (i.e. x1, x2는 e와 직교한다)
3. taylors expansion처럼 모르는 y를 유추하기 위해 알고 있는 x1, x2를 썼지만 e만큼 오차 존재
