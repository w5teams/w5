## APP 说明

- 查询 Splunk 中的数据

## 动作列表

### 查询信息

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **domain**  | text | `是` | Splunk 域名（包含协议头） |
| **user**  | number | `是` | Splunk 用户名 |
| **passwd**  | text | `是` | Splunk 密码 |
| **body**  | text | `是` | SPL 语句 |

**返回值：**

```
# 正常
{'Extra': None, 'StatusCode': 0, 'StatusMessage': 'success'}
```