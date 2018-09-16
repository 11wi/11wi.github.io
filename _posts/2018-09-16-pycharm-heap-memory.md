# pycharm-optimization
처음 tensorflow 모델을 돌리면 memory가 부족하다는 에러가 보인다.
굳이 딥러닝을 하지 않아도 pandas로 가끔 대용량 처리를 할 때면 오른쪽 하단의 하얀 바가 다 차곤 한다. 그럴 때면 체감상 속도가 느려지는 듯하다.

성능 향상에 도움되는 세팅
`ctrl-shift-a` - `Edit custom VM options` - `-Xmx750m`을 수정(`-Xmx2048m`)하고 재실행.
