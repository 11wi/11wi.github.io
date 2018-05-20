---
updated: 2018-05-20 21:33:35 +0900
---

# 파이썬 쓰임새가 점차 넓어지다.
실전 프로젝트에서 사용하면서 배워나가고 있는 만큼 깊이는 부족하지만 무엇을 하던 쉽게 해낼 수 있다는 것만큼은 확연히 느꼈다.  
최근 데이터분석용 데이터마트를 구축하며 기존 oracle 데이터허브에서 분석서버의 mariaDB로 옮기는 일이 있었다. 최근 파이썬을 많이 쓰다보니 자연히 파이썬으로 짜게 됐는데 너무 간단히 소스를 짤 수 있어서 당황스러웠다...
  docplex 라이브러리에서도 pandas 덕을 많이 봤는데 이번에도 역시 pandas가 큰 일을 했다. 먼저 oracle에 붙어줄 `cx_oracle`과 mysql용 `sqlalchemy`가 필요하다. sqlalchemy는 mongodb용 `mongoose`와 유사한 느낌을 받았는데 클래스 형태로 데이터를 조작할 수 있는 기능이 있지만 다소 번거로워 db connect 기능만 사용했다.
```python
engine = create_engine("mysql+pymysql://~~~~", encoding='utf-8')
connection = engine.connect()
```

db connect 객체 생성 후, sql 쿼리를 파일로 읽고 pandas로 정말 쉽게 끝낼 수 있다.
```python
sql_file = open('./query.sql', 'r')
query = sql_file.read()
sql_file.close()

df = pd.read_sql(query, con=oracle_connection, params={'date_to_extract': Date})
df.to_sql(name='TABLE', con=mysql_connection, if_exists='append', index=False)
```

## 로깅 모듈
혹시 발생할지 모르는 DB에러를 잡기 위해 로그 저장 기능을 만들기는 다소 어려웠다. 여러 방법이 있겠지만 가장 보기에 깔끔하고 기능적으로도 괜찮은 건 이 정도가 아닐까 싶다. 다만 사전에 log설정 파일을 작성해야한다.
```python
except exc.SQLAlchemyError as exec:
    logging.config.fileConfig('./log/log.config.ini')
    logger = logging.getLogger()
    logger.debug(exec)
```

```ini
[loggers]
keys=root

[handlers]
keys=stream_handler, file_handler

[formatters]
keys=formatter

[logger_root]
level=DEBUG
handlers=stream_handler, file_handler

[handler_stream_handler]
class=StreamHandler
formatter=formatter
args=(sys.stderr,)

[handler_file_handler]
class=handlers.RotatingFileHandler
args=('./log/etl.log','a',10 * 1024 * 1024, 10)
formatter=formatter

[formatter_formatter]
format=%(asctime)-12s %(name)-4s [%(module)s:%(lineno)-4s]  %(message)s
datefmt='%Y-%m-%d %I:%M:%S %p'
```

pandas의 기능에 감사하게 되고 점점 개발자스러워지는 걸 느끼게 됐다. 다음엔 네이버 트렌드도 활용하고 hadoop에 저장된 웹행동 데이터도 긁어올 예정이니 점점 이런 작업에 익숙해지겠지. 그러면 또 정리해서 올리자.

  그리고 아직은 글 하나 올리는데 30분씩 걸리지만, 점차 빨라지겠지.
