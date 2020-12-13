## APP说明

- **Github** : https://github.com/AlienVault-OTX/OTX-Python-SDK
- **官网** : https://otx.alienvault.com/ (需要注册账号)

## 动作列表

### ioc判断

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **api_key**  | text | `是` | otx key |
| **pulse_id**  | text | `是` | otx pulse_id |
| **ioc**  | text | `是` | ip 或 域名 |

**返回值：**

```
是返回 True，否返回 False
```