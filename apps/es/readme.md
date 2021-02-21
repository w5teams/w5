## APP 说明

- 查询 ES 服务器中的数据

## 动作列表

### 查询信息

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **host**  | text | `是` | ES 服务器地址 |
| **port**  | number | `是` | ES 端口号 |
| **index**  | text | `是` | 索引名称 |
| **body**  | text | `是` | DSL 语句 |
| **account**  | text | `否` | 认证账号 |
| **password**  | text | `否` | 认证密码 |

**返回值：**

```
# 正常
{'Extra': None, 'StatusCode': 0, 'StatusMessage': 'success'}
```