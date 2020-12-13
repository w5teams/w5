## APP 说明

> 查询QQ头像和昵称

## 动作列表

### 查询信息

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **domain**  | text | `是` | 域名 |

**返回值：**

```
wx	String	域名在微信中状态(danger 危险, unknown 未知, safe 安全)
qq	String	域名在QQ中状态(danger 危险, unknown 未知, safe 安全)
```