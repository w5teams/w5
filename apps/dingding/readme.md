## APP 说明

> 目前仅支持，`自定义关键字` 和 `IP地址(段)` 两种方式

- 钉钉官方文档：https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq

## 动作列表

### 钉钉通知

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **access_token**  | text | `是` | 钉钉机器人 access_token，Webhook 地址可以看到 |
| **msg**  | text | `是` | 通知内容 (自定义关键字方式，需有关键字方可生效)|

**返回值：**

```
# 正常
{'errcode': 0, 'errmsg': 'ok'}
```

更多看：https://ding-doc.dingtalk.com/doc#/faquestions/rftpfg