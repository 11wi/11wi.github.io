---
published: true
category: dev
---
신입사원 교육을 하기 위해 web server를 공부했다. 너무너무 어려워서 그냥 import해서 써야하는 개념은 아니란 걸 나도 이제서야 알았다. 나처럼 오해하는 사람을 위해 쉽게 정리했다.

---

server가 어떻게 request response를 처리하는지 간략하게 핵심만 소개한 영상이 있다. [reference](https://www.youtube.com/watch?v=5eQJ-0y8TzE)
go 코드로 보여주니 더욱 명확한 것 같다.

```go
package main

import (
	"net"
	"io"
)

func main() {
	li, _ := net.Listen("tcp", ":8080")
	for {
		c, _ := li.Accept()
		io.WriteString(c, "Hello World")
        c.close()
	}
}
```

요는 tcp socket을 생성하고 해당 port에 접속한 connection에 response를 보내는 무한 loop를 실행하는 것이다.

`telnet localhost 8080`으로 접속할 수 있다. 대신 request 형태가 없다.
browser로 접속시 GET request를 확인할 수 있다. `curl -v`와 같은 형태다.

정리하면 osi 7계층 가운데 L4 tcp 와 L7 http을 사용하며 tcp server에 http 규약에 맞는 request byte를 날리면 server를 이를 파싱하여 routing 및 response를 할 수 있다. 

---

## 간단한 용어 정리

http request는 크게 method, uri, header, body로 나뉜다.

REST는 http request byte에 GET, POST 등 약속된 키워드를 추가한 것으로 볼 수 있다.

packet은 http request (packet 유실 ≈ request 유실)

payload는 request body
