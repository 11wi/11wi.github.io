---
category: data-science
---


# java virtual machine

처음 tensorflow 모델을 돌리면 memory가 부족하다는 error가 뜨고 프로그램이 종료되는 현상을 겪었다.
굳이 deep learning을 하지 않아도 pandas로 가끔 대용량 처리를 할 때면 오른쪽 하단의 하얀색 바가 다 차곤 한다. 
그럴 때면 체감상 속도가 느려지는 듯하다.

그게 뭔가 했더니 pycharm이 java로 만들어져서 특성상 virtual machine을 띄우는데 그 vm의 메모리 용량을 나타내는 것이었다.
사실 이런 일은 `mecab`을 돌릴 때도 발생하는데 (정확히 기억은 안 나지만) 큰 작업을 돌리면 memmory 문제가 있다고 나타난다.
그래서 [koalaNLP](https://koalanlp.github.io/python-support/html/index.html)에서는 처음부터 명시하게 한다.


```python
from koalanlp.Util import initialize

initialize(java_options="-Xmx4g", EUNJEON='LATEST')
```


성능 향상에 도움이 되는 것으로 느껴져서 일단 적용하는 것을 추천한다.
설정법을 소개하기 위해 
[command palette](https://www.jetbrains.com/help/pycharm/searching-everywhere.html)
를 먼저 설명하면 모든 pycharm 기능을 검색으로 찾는 것이다.
단축키를 알면 아주 편리한데 shift를 `⇧⇧` 따닥 누르면 나온다. (Pycharm2019) 

``` 
Press ⇧⇧ (⇧ twice)
    | 
Edit custom VM options
    |
-Xmx750m  ->  -Xmx2048m (2GB)
    |
pycharm restart
```

>이 글로 유입되신 분이 많아 `2019-09-07` 업데이트 했습니다. 
>다른 곳에서도 많이 보이는 정보글이지만 찾아오신 분께 도움이 되도록 내용 추가합니다.

> `2019-09-29` 추가로 데이터 엔지니어가 추천한 설정 공유합니다. 
```
-Xms2048m
-Xmx4096m
-XX:ReservedCodeCacheSize=240m
-XX:+UseCompressedOops
-Dfile.encoding=UTF-8
-XX:+UseG1GC
-XX:SoftRefLRUPolicyMSPerMB=50
-ea
-XX:CICompilerCount=2
-Dsun.io.useCanonPrefixCache=false
-Djava.net.preferIPv4Stack=true
-Djdk.http.auth.tunneling.disabledSchemes=""
-XX:+HeapDumpOnOutOfMemoryError
-XX:-OmitStackTraceInFastThrow
-Djdk.attach.allowAttachSelf
-Dkotlinx.coroutines.debug=off
-Xverify:none
 
-XX:ErrorFile=$USER_HOME/java_error_in_pycharm_%p.log
-XX:HeapDumpPath=$USER_HOME/java_error_in_pycharm.hprof
```
