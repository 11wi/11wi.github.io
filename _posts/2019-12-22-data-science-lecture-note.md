---
category: data-science
---


# data science 개론


## data science란

data science는 data에서 pattern을 추출하는 방법이다.
당연히 숨은 전제는 과거 pattern과 미래의 pattern이 유사하다는 것.
통계학 model과 차이점은 더욱 복잡한 non linear model을 쓴다는 것.
통계는 inference가 핵심이라고 생각하는데, data science 또는 machine learning은
computational mathematics에 가깝다. (e.g. deep learning)

## data science를 굳이 3개 과목으로 나누어 보면

* Vector
    * data는 vector, matrix, tensor로 존재한다.
    * data로 뭘 한다면 결국 전부 Linear Algebra 기반.
    * PCA는 Vector 좌표 공간의 원점을 변경하는 것.
* Function
    * Function은 model과 같은 말. 
    * Cost function도 중요.
    * 미분
        * 1차 미분
            * gradient descent
            * taylor expansion
            * jacobian
        * 2차 미분
            * hessian
            * laplacian
* Optimization
    * 학습은 cost function의 최적화
    * model을 최적화하기 쉽게 설계하는 것도 중요. 
    
~~아직은 조금 어렵다 더 공부하면서 쓰자~~